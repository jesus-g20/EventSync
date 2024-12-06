from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from event.models import Event
from .models import Cart, CartItem
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.db.models import Sum  # Import Sum here to fix the error

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def add_to_cart(request, event_id):
    """
    Adds an event to the user's cart and redirects to the event's detail page.
    """
    # Fetch or create the cart for the current user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Fetch or create the cart item
    event = get_object_or_404(Event, pk=event_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, event=event)

    if not created:
        cart_item.quantity += 1  # Increment quantity if already exists
        cart_item.save()

    # Calculate total quantity of items in the cart
    total_quantity = cart.items.aggregate(total=Sum("quantity"))["total"] or 0

    # Redirect to the event's detail page with event_id
    return redirect("event:detail", pk=event_id)  # Pass the event_id as pk


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


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.total_with_tax == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:view_cart")

    # Debugging
    print(
        f"Checkout - User: {request.user}, Authenticated: {request.user.is_authenticated}"
    )
    print(f"Session Key (Checkout): {request.session.session_key}")

    request.session.modified = True  # Persist session explicitly

    return render(
        request,
        "cart/checkout.html",
        {
            "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "total_with_tax": cart.total_with_tax,
        },
    )


@login_required
@csrf_exempt
def create_payment_intent(request):
    """
    Creates a payment intent for Stripe.
    """
    if request.method == "POST":
        try:
            # Fetch the user's cart
            cart = Cart.objects.filter(user=request.user).first()
            if not cart or cart.total_with_tax == 0:
                return JsonResponse({"error": "Cart is empty."}, status=400)

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(cart.total_with_tax * 100),  # Convert total to cents
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )

            return JsonResponse({"client_secret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)


@login_required
def thank_you(request):
    # Retrieve the user's active cart
    cart = Cart.objects.filter(user=request.user, active=True).first()
    if cart:
        # Update the cart's payment status to confirmed
        cart.payment_status = "confirmed"
        cart.active = False  # Close the cart after successful payment
        cart.save()

        # Add the revenue to the event creator's wallet for each item in the cart
        for cart_item in cart.items.all():
            event = cart_item.event
            creator_wallet, created = Wallet.objects.get_or_create(
                user=event.created_by
            )
            creator_wallet.add_balance(cart_item.total_price)

        # Debugging: Log the update process
        print(f"Cart {cart.id} payment confirmed for user {request.user}")

    request.session.modified = True  # Persist session explicitly
    return render(request, "cart/thank_you.html")
