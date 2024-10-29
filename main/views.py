from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy

from event.models import Category, Event
from .forms import RegistrationForm


class HomeView(ListView):
    model = Event
    template_name = "main/index.html"
    context_object_name = "events"

    def get_queryset(self):
        # Only fetch the first 6 unsold events
        return Event.objects.filter(is_sold=False)[:6]

    def get_context_data(self, **kwargs):
        # Add categories to the context
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class RegistrationView(FormView):
    template_name = "main/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("main:login")  # Redirect to login after registration

    def form_valid(self, form):
        # Save the form and redirect
        form.save()
        return super().form_valid(form)
