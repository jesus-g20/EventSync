from django.urls import path
from .views import add_to_cart, view_cart, delete_from_cart

app_name = "cart"

urlpatterns = [
    path("add/<int:event_id>/", add_to_cart, name="add_to_cart"),
    path("", view_cart, name="view_cart"),
    path("delete/<int:cart_item_id>/", delete_from_cart, name="delete_from_cart"),
]
