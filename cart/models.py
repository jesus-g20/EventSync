from django.db import models
from django.contrib.auth.models import User
from event.models import Event


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    TAX_RATE = 0.07  # Example: 7% tax rate

    @property
    def total_cost(self):
        """Calculate the total cost of the cart."""
        return sum(item.total_price for item in self.items.all())

    @property
    def tax_amount(self):
        """Calculate the tax amount."""
        return self.total_cost * self.TAX_RATE

    @property
    def total_with_tax(self):
        """Calculate the total including tax."""
        return self.total_cost + self.tax_amount

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        """Calculate the total price of the cart item."""
        return self.event.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.event.name} in {self.cart}"
