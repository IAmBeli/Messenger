from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

class ChatListView(LoginRequiredMixin, ListView):
    template_name = "chats/chat_list.html"
    context_object_name = "chats"

    def get_queryset(self):
        return (
            self.request.user.chats
            .prefetch_related("members")
            .order_by("-created_at")
        )

class ChatDetailView(LoginRequiredMixin, DetailView):
    template_name = "chats/chat_detail.html"
    context_object_name = "chat"

    def get_queryset(self):
        return self.request.user.chats.prefetch_related("members")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_messages"] = self.object.messages.select_related("author")
        return context
