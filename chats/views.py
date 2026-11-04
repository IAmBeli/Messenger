from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import MessageForm, GroupCreateForm
from .models import Chat, Membership
from .broadcast import broadcast_message

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
        broadcast_message(message)
    return redirect("chat_detail", pk=chat.pk)

@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupCreateForm(request.POST, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                chat = Chat.objects.create(name=form.cleaned_data["name"], is_group=True)
                chat.members.add(request.user, through_defaults={"role": Membership.Role.ADMIN})
                chat.members.add(*form.cleaned_data["members"])
            return redirect("chat_detail", pk=chat.pk)

    else:
        form = GroupCreateForm(user=request.user)
    return render(request, "chats/group_create.html", {"form": form})