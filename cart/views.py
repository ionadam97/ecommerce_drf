from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from .serializers import CartSerializer, ItemCreateUpdateSerializer
from .models import Cart, CartItem
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserCart


class CartAPIView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        Cart.objects.get_or_create(user=user)
        queryset = Cart.objects.filter(user=user)

        return queryset


class ItemCreateAPIView(CreateAPIView):
    serializer_class = ItemCreateUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemCreateUpdateSerializer
    permission_classes = (IsUserCart,)
    queryset = CartItem.objects.all()

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response(
            {"detail": _("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )

