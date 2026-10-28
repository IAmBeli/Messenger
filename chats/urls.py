from django.urls import path

from .views import ChatListView, ChatDetailView

urlpatterns = [
    path("", ChatListView.as_view(), name="chat_list"),
    path("chats/<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
]