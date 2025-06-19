from django.urls import path
from .views_api import (
    RegisterView, LoginView, ProductListView,
    ContactView, CheckoutView, UserOrdersView, CartDetailView, AddToCartView, RemoveFromCartView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('products/', ProductListView.as_view()),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path("cart/remove/", RemoveFromCartView.as_view(), name='cart-remove'),
    path('contacts/', ContactView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('my-orders/', UserOrdersView.as_view()),

]