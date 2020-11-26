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
    path('accounts/profile/', views.profile, name='profile'),

    path('test/', views.test, name='test'),

]
