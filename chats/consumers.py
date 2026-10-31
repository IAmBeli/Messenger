from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class Chatconsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        if not user.is_authenticated or not user.chats.filter(pk=chat_id).exists():
            self.close()
            return

        self.group_name = f"chat_{chat_id}"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnetc(self, close_code):
        if hasattr(self, "group_name"):
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)