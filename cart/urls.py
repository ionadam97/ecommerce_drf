from django.urls import path
from . import views


urlpatterns = [
    path("cart/", views.CartAPIView.as_view()),
    path("cart-create/", views.CartItemAPIView.as_view()),
    path("cart-item/<int:pk>/", views.CartItemView.as_view()),
]
