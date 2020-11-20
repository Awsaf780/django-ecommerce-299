from django.urls import path

from store.api.views import *

app_name = 'store'

urlpatterns = [
    path('product/<slug>/', api_detail_product_view, name='detail'),
    path('product/<slug>/update', api_update_product_view, name='update'),
    path('product/<slug>/delete', api_delete_product_view, name='delete'),
    path('product/create', api_create_product_view, name='create'),

    path('product/list', ApiProductListView.as_view(), name='product_all'),

    path('users/<username>/', api_detail_user_view, name='users'),
]