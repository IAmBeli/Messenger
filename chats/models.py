from django.conf import settings
from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=128, blank=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Membership",
        related_name="chats",
    )

    def __str__(self):
        return self.name or f"Chat {self.pk}"

    def title_for(self, user):
        """Return the chat title as seen by the given user."""
        if self.is_group:
            return self.name or f"Group {self.pk}"
        for member in self.members.all():
            if member != user:
                return str(member)
        return "Deleted account"

class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "chat"], name="unique_membership"),
        ]

    def __str__(self):
        return f"{self.user} in {self.chat}"

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="messages",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"