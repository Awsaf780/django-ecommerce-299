from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, SentimentForm
from . models import *
from .utils import *

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required


def view_product(request, slug):
    context = {}
    product = Product.objects.get(slug=slug)

    form = SentimentForm()

    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            customer = Customer.objects.get(user=request.user)

            score = sentiment_analyse(review)
            rating = sentiment_score_to_rating(score)

            Sentiment.objects.create(
                customer=customer,
                product=product,
                review=review,
                score=score,
                rating=rating
            )
            form = SentimentForm()

    reviews = Sentiment.objects.filter(product=product)
    context = {'product': product, 'reviews': reviews, 'form': form}

    return render(request, 'store/view_product.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)

            name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            Customer.objects.create(
                user = user,
                name = name,
                email = email,
            )
            print("Customer created")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                # messages.success(request, "Account Created Successfully, " + user)
                return redirect('loginPage')

    context = {'form': form}
    return render(request, 'store/register.html', context)

def loginPage(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')

        # print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Incorrect Username or Password')
            context = {'error': 'Incorrect username or password'}

    return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store')

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# @login_required(login_url='loginPage')
def checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('Product Id: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'cancel':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt
#
# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse('Payment Complete', safe=False)


def dashboard(request):
    context = {}
    return render(request, 'store/dashboard.html', context)



############ All custom Functions
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



stopword_list = stopwords.words('english')

# stopword_list.append('die')
stopword_list.append('carbonara')
stopword_list.append('cheese')
stopword_list.append('ramen')
stopword_list.append('stew')
stopword_list.append("'ve")


def list_to_string(word_list):
    sentence = ""
    for word in word_list:
        sentence += "{} ".format(word)

    return sentence

def sentiment_analyse(text):
    text = text.lower()

    text = word_tokenize(text, "english")

    final_words = []
    for word in text:
        if word not in stopword_list:
            final_words.append(word)

    text = list_to_string(final_words)

    score = SentimentIntensityAnalyzer().polarity_scores(text)
    neg = score['neg']
    pos = score['pos']
    neu = score['neu']

    if pos > neg:
        result = pos
    elif pos < neg:
        result = neg*-1
    else:
        result = neu*0

    return result


def sentiment_score_to_rating(score):
    rating_1 = -0.6
    rating_2 = -0.2
    rating_4 = 0.2
    rating_5 = 0.6

    if score == 0:
        rating = 0

    elif score > rating_5:
        rating = 5

    elif score > rating_4:
        rating = 4

    elif score < rating_1:
        rating = 1

    elif score < rating_2:
        rating = 2

    else:
        rating = 3

    return rating