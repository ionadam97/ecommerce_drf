from django.urls import path
from .views import (
    ProductsListAPIView,
    ProductDetailAPIView,
    CategoryListAPIView,
    CategoryAPIView,
    CreateProductView,
    SearchListAPIView
    )


urlpatterns = [
    path('product/', ProductsListAPIView.as_view(), name='products'),
    path('product/<slug:category_slug>/<slug:product_slug>/', ProductDetailAPIView.as_view(), 
        name='product_detail'),
    path('product/create/', CreateProductView.as_view(), name='create_product'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', CategoryAPIView.as_view(), name='category_detail'),
    path('search/', SearchListAPIView.as_view(), name='search'),
]