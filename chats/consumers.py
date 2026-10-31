import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .forms import MessageForm

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        if not user.is_authenticated:
            self.close()
            return
        self.chat = user.chats.filter(pk=chat_id).first()
        if self.chat is None:
            self.close()
            return

        self.group_name = f"chat_{self.chat.pk}"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self,"group_name"):
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        form = MessageForm(data={"text": data.get("text", "")})
        if not form.is_valid():
            return

        message = form.save(commit=False)
        message.chat = self.chat
        message.author = self.scope["user"]
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chat.message",
                "id": message.pk,
                "author": str(message.author),
                "author_id": message.author_id,
                "text": message.text,
                "created_at": message.created_at.isoformat(),
            },
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))