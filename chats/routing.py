from django.urls import path

from .consumers import Chatconsumer

websocket_urlpatterns = [
    path("ws/chats/<int:chat_id>/", Chatconsumer.as_asgi()),
]