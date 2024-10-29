from django.urls import path
from .views import InboxView, ChatDetailView, NewChatView

app_name = "chat"

urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("<int:pk>/", ChatDetailView.as_view(), name="detail"),
    path("new/<int:item_pk>/", NewChatView.as_view(), name="new_chat"),
]
