from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def chat_group_name(chat_id):
    return f"chat_{chat_id}"

def broadcast_message(message):
    """Send saved message to everyone currently connected to the chat"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        chat_group_name(message.chat_id),
        {
            "type": "chat.message",
            "id": message.pk,
            "author": str(message.author),
            "author_id": message.author_id,
            "text": message.text,
            "created_at": message.created_at.isoformat(),
        }
    )