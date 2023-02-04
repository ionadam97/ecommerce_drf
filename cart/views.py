from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from .serializers import CartItemSerializer, CartItemUpdateSerializer, CartSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from product.models import Product
from rest_framework.views import APIView


class CartAPIView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        queryset = Cart.objects.filter(user=user)
        print(cart, queryset)
        return queryset


class CartItemAPIView(APIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):

        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product = get_object_or_404(Product, pk=request.data["product"])
        current_item = CartItem.objects.filter(cart=cart, product=product)

        if current_item.count() > 0:
            raise NotAcceptable("You already have this item in your shopping cart")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.quantity:
            raise NotAcceptable("You order quantity more than the seller have")

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    # method_serializer_classes = {
    #     ('PUT',): CartItemUpdateSerializer
    # }
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        print(request.data)
        product = get_object_or_404(Product, pk=request.data["product"])

        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please, input vaild quantity")

        if quantity > product.quantity:
            raise NotAcceptable("Your order quantity more than the seller have")

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()
        # push_notifications(
        #     cart_item.cart.user,
        #     "deleted cart product",
        #     "you have been deleted this product: "
        #     + cart_item.product.title
        #     + " from your cart",
        # )

        return Response(
            {"detail": _("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )
