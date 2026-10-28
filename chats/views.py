from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import MessageForm

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
        context["form"] = MessageForm()
        return context

@login_required
@require_POST
def send_message(request, pk):
    chat = get_object_or_404(request.user.chats, pk=pk)
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.chat = chat
        message.author = request.user
        message.save()
    return redirect("chat_detail", pk=chat.pk)