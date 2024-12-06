from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
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
        user = self.request.user
        my_events = Event.objects.filter(created_by=user)

        # Debugging
        print(f"Calculating total balance for user: {user}")

        # Calculate the total revenue by summing up all event revenues
        total_balance = sum(event.calculate_revenue() for event in my_events)

        # Debugging
        print(f"Total Balance: {total_balance}")

        context["total_balance"] = total_balance
        return context
