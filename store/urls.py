from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='processOrder'),

    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logout'),
    # path('dashboard/', views.dashboard, name='dashboard'),

    path('product/<slug>', views.view_product, name='view_product'),
    path('category/<slug>', views.view_category, name='view_category'),

    path('accounts/profile/', views.profile, name='profile'),

    path('products', views.products, name='products'),
    path('products/<page>', views.products_pag, name='test_page'),

    path('products/category/<slug>', views.products_category, name='products_cat'),
    path('products/category/<slug:slug>/<int:page>', views.products_category_pag, name='cat_pag'),


    # path('recommend', views.recommend_products, name="test_recom")

]
