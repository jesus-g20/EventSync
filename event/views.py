from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from cart.models import Cart, CartItem
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import NewEventForm, EditEventForm
from .models import Category, Event


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

        if selected_category_ids:
            queryset = queryset.filter(category_id__in=selected_category_ids)

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
        context["title"] = "New Event"
        return context


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
        context["title"] = "Edit Event"
        return context


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "event/confirm_delete.html"
    success_url = reverse_lazy("portal:index")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by


@login_required
def add_to_cart(request, event_id):
    """
    Adds an event to the user's cart and redirects to the previous page.
    """
    # Fetch or create the cart for the current user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Fetch or create the cart item
    event = get_object_or_404(Event, pk=event_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, event=event)

    if not created:
        cart_item.quantity += 1  # Increment quantity if it already exists
        cart_item.save()

    # Calculate total quantity of items in the cart
    total_quantity = cart.items.aggregate(total=Sum("quantity"))["total"] or 0

    # Redirect back to the previous page
    return redirect(request.META.get("HTTP_REFERER", "event:browse_events"))
