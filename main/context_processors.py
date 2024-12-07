from django.db.models import Sum
from cart.models import Cart

# fix big


def cart_item_count(request):
    """
    Adds the total quantity of items in the user's cart to the context.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            # Sum up all item quantities in the cart
            total_quantity = cart.items.aggregate(total=Sum("quantity"))["total"] or 0
            return {"cart_item_count": total_quantity}
    return {"cart_item_count": 0}
