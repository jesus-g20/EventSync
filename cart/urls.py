from django.urls import path
from . import views
from django.shortcuts import render

app_name = "cart"

urlpatterns = [
    path("add/<int:event_id>/", views.add_to_cart, name="add_to_cart"),
    path("", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),  # Checkout page
    path("create-payment-intent/", views.create_payment_intent, name="create_payment_intent"),  # Payment Intent API
    path('thank-you/', lambda request: render(request, 'cart/thank_you.html'), name='thank_you'),
]

