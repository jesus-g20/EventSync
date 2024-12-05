from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    category = models.ForeignKey(
        Category, related_name="events", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="events_images", blank=True, null=True)
    location = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, related_name="events", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_revenue(self):
        """
        Calculate the total revenue for this event from ticket sales.
        """
        from cart.models import CartItem  # Import CartItem model dynamically

        revenue = (
            CartItem.objects.filter(event=self).aggregate(
                total_revenue=Sum("quantity") * self.price
            )["total_revenue"]
            or 0
        )
        return revenue

    def __str__(self):
        return self.name
