from django.db import models
from product.models import Product
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.user

    def calculate_total(self):
        total = 0
        for item in self.cart_item.all():
            total += item.product.price * item.quantity
        return total



class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product