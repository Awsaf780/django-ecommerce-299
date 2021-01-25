from rest_framework import serializers
from store.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'category', 'image']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

#### Hasan's Serializers ##########

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class CartUnitSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, min_value=1)
    # product = ProductForOrderDetail(read_only=True)

    class Meta:
        # model = OrderUnit
        fields = ('slug', 'quantity', 'product')

    def validate(self, data):
        slug = data['slug']
        quantity = data['quantity']

        try:
            product = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product does not exist')

        if product.num_in_stock < quantity:
            raise serializers.ValidationError('There are not enough units in stock')

        return data

class CartUnitSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, min_value=1)
    # product = ProductForOrderDetail(read_only=True)

    class Meta:
        # model = OrderUnit
        fields = ('slug', 'quantity', 'product')

    def validate(self, data):
        slug = data['slug']
        quantity = data['quantity']

        try:
            product = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product does not exist')

        if product.num_in_stock < quantity:
            raise serializers.ValidationError('There are not enough units in stock')

        return data

class OrderUnitSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        # model = OrderUnit
        fields = ('quantity', 'product')

    # def get_product(self, obj):
    #     # data = ProductForOrderDetail(obj.unit).data
    #
    #     # Use the price that was at the moment of purchase instead of current price.
    #     data['price'] = obj.unit_price
    #
    #     return data


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('name', 'address', 'phone')


class OrderListSerializer(serializers.ModelSerializer):
    product_num = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'product_num')

    def get_product_num(self, obj):
        return obj.items_ordered.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderUnitSerializer(
        many=True,
        read_only=True,
        source='orderunit_set'
    )

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'name', 'address', 'phone', 'products')


class DeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        # model = DeliveryInfo
        fields = ('name', 'address', 'phone')



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        # model = Review
        fields = ('id', 'user', 'product', 'comment')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        # model = Rating
        fields = ('id', 'user', 'product', 'rating')


class ProductListSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'price', 'discount_price', 'tags', 'num_in_stock', 'image')

    def get_images(self, obj):
        images = obj.productimage_set.all()

        if images.exists():
            return [image.image.url for image in images.all()]
        else:
            return []




class ProductForOrderDetail(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('title', 'image', 'slug', 'id', 'price', 'num_in_stock')

    def get_image(self, obj):
        image = obj.productimage_set.order_by('-is_main').first()

        if image is None:
            return None

        return image.image.url