from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:event_id>/", views.add_to_cart, name="add_to_cart"),
    path("", views.view_cart, name="view_cart"),
]