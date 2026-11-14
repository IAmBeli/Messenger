from django.urls import path


from .views import ChatListView, ChatDetailView, send_message, create_group, start_chat

urlpatterns = [
    path("", ChatListView.as_view(), name="chat_list"),
    path("chats/<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
    path("chats/<int:pk>/send/", send_message, name="send_message"),
    path("groups/new/", create_group, name="create_group"),
    path("chats/new/", start_chat, name="start_chat"),
]