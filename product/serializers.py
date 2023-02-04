from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'description',
            'price',
            'get_image',
        )


class ProductsSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'get_thumbnail',
            'get_absolute_url',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'title',
            'get_absolute_url',
        )


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    class Meta:
        model = Category
        fields = (
            'title',
            'get_absolute_url',
            'products',
        )

class ProductCreateSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'description',
            'price',
            'delivery',
            'image',
        )