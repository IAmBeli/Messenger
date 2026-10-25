from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class ChatListView(LoginRequiredMixin, ListView):
    template_name = "chats/chat_list.html"
    context_object_name = "chats"

    def get_queryset(self):
        return (
            self.request.user.chats
            .prefetch_related("members")
            .order_by("-created_at")
        )