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
