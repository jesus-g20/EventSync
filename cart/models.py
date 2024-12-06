from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from django.db import transaction


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
        """Set the payment status to confirmed and update wallet balance."""
        self.payment_status = "confirmed"
        self.active = False  # Deactivate the cart after payment
        self.save()

        # Update the organizer's wallet balance
        for item in self.items.all():
            organizer = item.event.created_by  # Get the event organizer
            organizer_wallet, created = Wallet.objects.get_or_create(user=organizer)
            organizer_wallet.balance += item.total_price  # Add the item's total price
            organizer_wallet.save()

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        """Calculate the total price of the cart item."""
        return round(self.event.price * self.quantity, 2)

    def __str__(self):
        return f"{self.quantity}x {self.event.name} in {self.cart}"
