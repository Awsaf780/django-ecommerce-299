from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)

    CAT_CHOICES = (
        ('apparel-men', 'Apparel-men'),
        ('apparel-women', 'Apparel-women'),
        ('apparel-kids', 'Apparel-kids'),

        ('electronics-smartphone', 'Electronics-smartphone'),
        ('electronics-accessory', 'Electronics-accessory'),
        ('electronics-computer', 'Electronics-computer'),

        ('fashion-footwear', 'Fashion-footwear'),
        ('fashion-watch', 'Fashion-watch'),
        ('fashion-accessory', 'Fashion-accessory'),
        ('fashion-cosmetic', 'Fashion-cosmetic'),

        ('misc', 'Misc'),

    )

    category = models.CharField(max_length=200, choices=CAT_CHOICES, blank=True, null=True, default="")
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    # state = models.CharField(max_length=200, null=True)
    # zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Sentiment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    review = models.TextField()
    score = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review