from django.db import models
from django.contrib.auth.models import User
from event.models import Wallet


class Cart(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("failed", "Failed"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track updates
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )

    TAX_RATE = 0.07  # Example: 7% tax rate

    @property
    def total_cost(self):
        """Calculate the total cost of the cart."""
        return sum(item.total_price for item in self.items.all())

    @property
    def tax_amount(self):
        """Calculate the tax amount."""
        return round(self.total_cost * self.TAX_RATE, 2)

    @property
    def total_with_tax(self):
        """Calculate the total including tax."""
        return round(self.total_cost + self.tax_amount, 2)

    def confirm_payment(self):
        """Set the payment status to confirmed, update wallet balance, and remove cart items."""
        self.payment_status = "confirmed"
        self.active = False  # Deactivate the cart after payment
        self.save()

        # Update the organizer's wallet balance for each event item
        from event.models import Wallet  # Import dynamically to avoid circular import

        for item in self.items.all():
            organizer = item.event.created_by  # Get the event organizer
            organizer_wallet, created = Wallet.objects.get_or_create(user=organizer)
            organizer_wallet.balance += (
                item.total_price
            )  # Add the total price to balance
            organizer_wallet.save()

        # Debugging: Print items in the cart before deletion
        print(f"Cart {self.id} has {self.items.count()} items before deletion.")

        # Explicitly delete items with error handling
        deleted_items_count = 0
        try:
            for item in self.items.all():
                item.delete()
                deleted_items_count += 1
        except Exception as e:
            print(f"Error deleting items: {e}")
            # You can log this error to the database or external service if needed

        # Debugging: Log how many items were deleted
        print(f"Deleted {deleted_items_count} items from Cart {self.id}.")

        # Ensure that cart is now empty (optional)
        if self.items.count() == 0:
            print(f"Cart {self.id} is now empty.")
        else:
            print(f"Cart {self.id} still has {self.items.count()} items.")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        """Calculate the total price of the cart item."""
        return round(self.event.price * self.quantity, 2)

    def __str__(self):
        return f"{self.quantity}x {self.event.name} in {self.cart}"
