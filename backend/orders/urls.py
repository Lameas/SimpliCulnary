from django.urls import path

from .views import (
    AddToCartView,
    CartDetailView,
    CheckoutSuccessView,
    CheckoutView,
    RemoveCartItemView,
    UpdateCartItemView,
)

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<int:pk>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/update/<int:pk>/", UpdateCartItemView.as_view(), name="update_cart_item"),
    path("cart/remove/<int:pk>/", RemoveCartItemView.as_view(), name="remove_cart_item"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/success/<int:pk>/", CheckoutSuccessView.as_view(), name="checkout_success"),
]
