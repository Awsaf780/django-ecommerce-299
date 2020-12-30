from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import *

class TestUrls(SimpleTestCase):
    def test_store_url_is_resolved(self):
        url = reverse('store')
        self.assertEquals(resolve(url).func, store)

    def test_cart_url_is_resolved(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)

    def test_checkout_url_is_resolved(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_update_item_url_is_resolved(self):
        url = reverse('update_item')
        self.assertEquals(resolve(url).func, updateItem)

    def test_process_order_url_is_resolved(self):
        url = reverse('processOrder')
        self.assertEquals(resolve(url).func, processOrder)

    def test_register_url_is_resolved(self):
        url = reverse('registerPage')
        self.assertEquals(resolve(url).func, registerPage)

    def test_login_url_is_resolved(self):
        url = reverse('loginPage')
        self.assertEquals(resolve(url).func, loginPage)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

    def test_view_product_url_is_resolved(self):
        url = reverse('view_product', args=['some-slug'])
        self.assertEquals(resolve(url).func, view_product)

    def test_view_category_url_is_resolved(self):
        url = reverse('view_category', args=['some-slug'])
        self.assertEquals(resolve(url).func, view_category)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    # products, test_page, products_cat, cat_pag are unnecessary

    # def test_view_product_url_is_resolved(self):
    #     url = reverse('view_product', args=['some-slug'])
    #     self.assertEquals(resolve(url).func, view_product)
    #
    # def test_view_product_url_is_resolved(self):
    #     url = reverse('view_product', args=['some-slug'])
    #     self.assertEquals(resolve(url).func, view_product)
    #
    # def test_view_product_url_is_resolved(self):
    #     url = reverse('view_product', args=['some-slug'])
    #     self.assertEquals(resolve(url).func, view_product)
    #
    # def test_view_product_url_is_resolved(self):
    #     url = reverse('view_product', args=['some-slug'])
    #     self.assertEquals(resolve(url).func, view_product)



