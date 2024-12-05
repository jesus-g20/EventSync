import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from event.models import Event
from .models import Cart, CartItem
import stripe
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY

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

    # Redirect back to the event list or current page
    return redirect(request.META.get("HTTP_REFERER", "event:browse_events"))



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


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.total_with_tax == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:view_cart")

    # Pass the original amount for display
    total_with_tax_display = cart.total_with_tax  # Keep it in dollars
    total_with_tax_cents = int(cart.total_with_tax * 100)  # Convert to cents for Stripe

    return render(
        request,
        "cart/checkout.html",
        {
            "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "total_with_tax": total_with_tax_display,  # Send dollars for display
            "total_with_tax_cents": total_with_tax_cents,  # Send cents for Stripe
        },
    )


@login_required
@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if not cart or cart.total_with_tax == 0:
                return JsonResponse({"error": "Cart is empty."}, status=400)

            intent = stripe.PaymentIntent.create(
                amount=int(cart.total_with_tax * 100),  # Amount in cents
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )
            print("Generated client_secret:", intent["client_secret"])  # Debugging log
            return JsonResponse({"client_secret": intent["client_secret"]})
        except Exception as e:
            print("Error creating PaymentIntent:", str(e))  # Debugging log
            return JsonResponse({"error": str(e)}, status=403)



@login_required
def thank_you(request):
    return render(request, "cart/thank_you.html")
