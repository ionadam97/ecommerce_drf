from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "title",
            "quantity",
            "price",
            "image",
        )


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = [ "id","product", "quantity"]
    
    

class CartSerializer(serializers.ModelSerializer):

    cart_item = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = [ "id","cart_item", "calculate_total"]
        read_only_fields = ["calculate_total",]



class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

