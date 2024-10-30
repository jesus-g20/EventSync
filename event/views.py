from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import NewEventForm, EditEventForm
from .models import Category, Event


# DetailView for viewing an event's detail
class EventDetailView(DetailView):
    model = Event
    template_name = "event/detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_events"] = Event.objects.filter(
            category=self.object.category, is_sold=False
        ).exclude(pk=self.object.pk)
        return context


class EventListView(ListView):
    model = Event
    template_name = "event/events.html"
    context_object_name = "events"

    def get_queryset(self):
        queryset = Event.objects.filter(is_sold=False)
        query = self.request.GET.get("query", "")
        selected_category_ids = self.request.GET.getlist("category")

        # Display all events if no filter criteria are set
        if not query and not selected_category_ids:
            return queryset

        # Filter events by categories if selected
        if selected_category_ids:
            queryset = queryset.filter(category_id__in=selected_category_ids)

        # Filter by search query if provided
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("query", "")
        context["selected_category_ids"] = self.request.GET.getlist("category")
        return context


# CreateView for creating a new event
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = NewEventForm
    template_name = "event/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New item"
        return context


# UpdateView for editing an event
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EditEventForm
    template_name = "event/form.html"

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by

    def get_success_url(self):
        return reverse_lazy("event:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit item"
        return context


# DeleteView for deleting an event
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "event/confirm_delete.html"
    success_url = reverse_lazy("portal:index")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by