from django.urls import path
from . import views  # Import all views from the current module
from django.shortcuts import render

app_name = "cart"


urlpatterns = [
    path("add/<int:event_id>/", views.add_to_cart, name="add_to_cart"),
    path("", views.view_cart, name="view_cart"),
    path("delete/<int:cart_item_id>/", views.delete_from_cart, name="delete_from_cart"),
    path("checkout/", views.checkout, name="checkout"),  # Checkout page
    path(
        "create-payment-intent/",
        views.create_payment_intent,
        name="create_payment_intent",
    ),  # Payment Intent API
    path("thank-you/", views.thank_you, name="thank_you"),
]
