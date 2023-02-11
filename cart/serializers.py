from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product
from rest_framework.exceptions import NotAcceptable


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
    product = CartProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id","product", "quantity"]
    


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = [ "id","cart_item", "calculate_total"]
        read_only_fields = ["calculate_total",]


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1,required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]
    
    def quantity_order(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        if quantity > product.quantity:
            raise NotAcceptable("You order quantity more than the seller have")
        return quantity, product

    def create(self, validated_data):
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)
        quantity, product= self.quantity_order(validated_data)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product )
        cart_item.quantity = quantity
        cart_item.save()

        return cart_item

    def update(self, instance,  validated_data):
        quantity, product= self.quantity_order(validated_data)
        instance.quantity = quantity
        instance.save()
      
        return instance

