from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# from store.models import Product
from store.api.serializers import *


@api_view(['GET', ])
def api_detail_user_view(request, username):
    try:
        user = User.objects.get(username=username)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['GET', ])
def api_detail_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['PUT', ])
def api_update_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = 'Update Successful'
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_delete_product_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = product.delete()
        data = {}
        if operation:
            data['success'] = "Successfully Deleted"
        else:
            data['failure'] = 'Failed to Delete'

        return Response(data=data)


@api_view(['POST', ])
def api_create_product_view(request):

    product = Product()

    if request.method == 'POST':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination