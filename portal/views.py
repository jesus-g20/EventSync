from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Sum
from event.models import Event


class PortalIndexView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "portal/index.html"
    context_object_name = "events"

    def get_queryset(self):
        # Show only events created by the current user
        return Event.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all events created by the current user
        my_events = self.get_queryset()
        # Calculate total wallet balance
        total_balance = sum(event.calculate_revenue() for event in my_events)
        # Add balance to context
        context["total_balance"] = total_balance
        return context
