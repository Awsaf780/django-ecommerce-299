from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, SentimentForm
from .models import *
from .utils import *

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
import requests

from django.contrib.auth.decorators import login_required

domain = 'http://127.0.0.1:8000'


def get_recommended_quantity():
    return 3


def profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = request.user

    context = {'cartItems': cartItems, 'user': user}

    return render(request, 'store/profile.html', context)


def contact(request):
    context = {}

    data = cartData(request)
    cartItems = data['cartItems']
    context['cartItems'] = cartItems

    return render(request, 'store/contact.html', context)

def search_product(request):
    context = {}

    data = cartData(request)
    cartItems = data['cartItems']
    context['cartItems'] = cartItems

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        results = Product.objects.filter(name__contains=keyword) | \
                  Product.objects.filter(description__contains=keyword) | \
                  Product.objects.filter(category__contains=keyword) | \
                  Product.objects.filter(slug__contains=keyword)

        context['products'] = results
    else:
        context['products'] = Product.objects.all()

    return render(request, 'store/store.html', context)


def view_product(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']

    product = Product.objects.get(slug=slug)

    form = SentimentForm()

    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            # customer = User.objects.get(user=request.user)
            customer = request.user

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
    try:
        recommended = recommend_products(request, product.pk)
        related_title = "Suggested for You"
    except:
        # random_products = Product.objects.all().order_by('?')[:3]
        random_products = Product.objects.filter(category=product.category).order_by('?')[:3]
        recommended = random_products
        related_title = "Similar"

    context = {'product': product,
               'reviews': reviews,
               'form': form,
               'cartItems': cartItems,
               'recommended_products': recommended,
               'suggest_title': related_title,
               }

    return render(request, 'store/view_product.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
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


def products(request):
    page = 1

    if request.method == 'GET':
        query = request.GET.get('search')
        if query != None:
            return search(request, page, query)
        else:
            return products_pag(request, 1)
    else:
        return products_pag(request, 1)


def products_pag(request, page):
    data = cartData(request)
    cartItems = data['cartItems']

    try:
        r = requests.get('{}/api/product/list?page={}'.format(domain, page))
        data = r.json()

        next = data['next']
        try:
            next_page = next.replace("{}/api/product/list?page=".format(domain), "")
        except:
            next_page = None

        previous = data['previous']
        try:
            previous_page = previous.replace("{}/api/product/list?page=".format(domain), "")
            if (previous_page == '{}/api/product/list'.format(domain)):
                previous_page = 1


        except:
            previous_page = None

        count = data['count']

        products = data['results']
        uri_context = 'products'
        context = {
            'cartItems': cartItems,
            'count': count,
            'products': products,
            'next_page': next_page,
            'previous_page': previous_page,
            'uri_context': uri_context,
        }


    except:
        context = {'error': 'Forbidden'}

    return render(request, "store/test_hasan.html", context)


def search(request, page, query):
    data = cartData(request)
    cartItems = data['cartItems']

    try:
        r = requests.get('{}/api/product/list?page={}&search={}'.format(domain, page, query))
        data = r.json()

        next = data['next']
        try:
            next_page = next.replace("{}/api/product/list?page=".format(domain), "")
            next_page = next_page.replace("&search={}".format(query), "")

        except:
            next_page = None

        previous = str(data['previous'])
        try:
            previous_page = previous.replace("{}/api/product/list?search={}".format(domain, query), '1')
            previous_page = previous_page.replace("{}/api/product/list?page=".format(domain), "")
            previous_page = previous_page.replace("&search={}".format(page), "")

        except:
            previous_page = None

        count = data['count']

        products = data['results']
        uri_context = 'products'

        context = {
            'cartItems': cartItems,
            'count': count,
            'products': products,
            'next_page': next_page,
            'previous_page': previous_page,
            'uri_context': uri_context,
            'query': query,
        }


    except:
        context = {'error': 'Forbidden'}

    print(context)

    return render(request, "store/test_hasan.html", context)


def products_category(request, slug):
    page = 1
    slug = slug
    return products_category_pag(request, slug, page)


def products_category_pag(request, slug, page):
    data = cartData(request)
    cartItems = data['cartItems']

    try:
        r = requests.get('{}/api/category/{}?page={}'.format(domain, slug, page))
        data = r.json()

        next = data['next']
        try:
            next_page = next.replace("{}/api/category/{}?page=".format(domain, slug), "")
        except:
            next_page = None

        previous = data['previous']
        try:
            previous_page = previous.replace("{}/api/category/{}?page=".format(domain, slug), "")
            if (previous_page == '{}/api/category/{}'.format(domain, slug)):
                previous_page = 1
        except:
            previous_page = None

        count = data['count']

        products = data['results']
        uri_context = 'products/category/{}'.format(slug)
        context = {
            'cartItems': cartItems,
            'count': count,
            'products': products,
            'next_page': next_page,
            'previous_page': previous_page,
            'uri_context': uri_context,
        }


    except:
        context = {'error': 'Forbidden'}

    return render(request, "store/test_hasan.html", context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def view_category(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.filter(category=slug)
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

    customer = request.user
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
        customer = request.user
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
        )

    return JsonResponse('Payment Complete', safe=False)


############ All custom Functions
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# stopword_list = stopwords.words('english')
stopword_list = ['the', 'a', 'I', 'am', 'have', 'is', 'they', 'their', 'should']


# stopword_list.append('die')
# stopword_list.append('carbonara')
# stopword_list.append('cheese')
# stopword_list.append('ramen')
# stopword_list.append('stew')
# stopword_list.append("'ve")


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
        result = neg * -1
    else:
        result = neu * 0

    return result


def sentiment_score_to_rating(score):
    rating_1 = -0.8
    rating_2 = -0.2
    rating_4 = 0.2
    rating_5 = 0.8

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


############### MACHINE LEARNING #######################
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def recommend_products(request, id):
    product_id = id
    quantity = get_recommended_quantity()

    sentiment = pd.DataFrame.from_records(Sentiment.objects.all().values('id', 'product', 'customer', 'rating'))

    df_pivot = sentiment.pivot_table(index='product', columns='customer', values='rating').fillna(0)
    query_array = df_pivot.loc[product_id].values.reshape(1, -1)
    matrix = csr_matrix(df_pivot.values)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(matrix)
    distances, indices = model_knn.kneighbors(query_array, n_neighbors=quantity + 1)

    recommended = []
    for i in range(len(distances.flatten())):
        if i == 0:
            product_index = indices.flatten()[i]
        else:
            index = indices.flatten()[i]
            recommended.append(df_pivot.index[index])

    recommended_products = []
    for id in recommended:
        product = Product.objects.get(id=id)
        recommended_products.append(product)

    # original = Product.objects.get(id=product_id)
    # context = {'sentiment': sentiment,
    #            'product': original,
    #            'recommended': recommended_products,
    #            }

    print(recommended_products)

    return recommended_products
