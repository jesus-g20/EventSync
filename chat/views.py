from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from event.models import Event
from .forms import ChatMessageForm
from .models import Chat, ChatMessage


class InboxView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/inbox.html"
    context_object_name = "chats"

    def get_queryset(self):
        return Chat.objects.filter(members__in=[self.request.user.id])


class ChatDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Chat
    template_name = "chat/detail.html"
    context_object_name = "chat"
    form_class = ChatMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ChatMessageForm()  # Initialize form for GET requests
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.conversation = self.object
            chat_message.created_by = request.user
            chat_message.save()
            return redirect("chat:detail", pk=self.object.pk)
        return self.form_invalid(form)


class NewChatView(LoginRequiredMixin, FormView):
    form_class = ChatMessageForm
    template_name = "chat/new.html"

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs["item_pk"])
        if self.event.created_by == request.user:
            return redirect("portal:index")

        # Check if conversation already exists
        self.conversations = Chat.objects.filter(event=self.event).filter(
            members__in=[request.user.id]
        )

        if self.conversations.exists():
            return redirect("chat:detail", pk=self.conversations.first().id)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Create a new chat
        chat = Chat.objects.create(event=self.event)
        chat.members.add(self.request.user)
        chat.members.add(self.event.created_by)
        chat.save()

        chat_message = form.save(commit=False)
        chat_message.conversation = chat
        chat_message.created_by = self.request.user
        chat_message.save()

        return redirect("chat:detail", pk=chat.id)
