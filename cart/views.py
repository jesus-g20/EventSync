from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from event.models import Event
from .models import Cart, CartItem
from django.contrib import messages


@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, event=event)
    if not created:
        cart_item.quantity += 1  # Increment the quantity if it already exists
        cart_item.save()

    # Use a success message to notify the user
    messages.success(request, f"{event.name} has been added to your cart.")

    # Redirect back to the event list or current page instead of cart
    return redirect(request.META.get("HTTP_REFERER", "event:browse_events"))


@login_required
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_cost = cart.total_cost if cart else 0
    tax_amount = cart.tax_amount if cart else 0
    total_with_tax = cart.total_with_tax if cart else 0

    return render(
        request,
        "cart/view_cart.html",
        {
            "cart_items": cart_items,
            "total_cost": total_cost,
            "tax_amount": tax_amount,
            "total_with_tax": total_with_tax,
        },
    )
