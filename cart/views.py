from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from event.models import Event
from .models import Cart, CartItem
from django.contrib import messages


@login_required
def add_to_cart(request, event_id):
    """
    Adds an event to the user's cart. If the event is already in the cart,
    it increments the quantity. Returns the updated cart count as JSON.
    """
    # Get the event and cart
    event = get_object_or_404(Event, id=event_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, event=event)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Return the updated cart count
    return JsonResponse({"cart_count": cart.items.count()})


@login_required
def view_cart(request):
    """
    Displays the user's cart with a list of items, total cost, tax, and final total.
    """
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


@login_required
def delete_from_cart(request, cart_item_id):
    """
    Deletes a specific item from the user's cart and redirects to the cart page.
    """
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Silently fail if the item does not exist

    # Redirect back to the cart page
    return redirect("cart:view_cart")
