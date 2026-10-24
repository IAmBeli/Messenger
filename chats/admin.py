from django.contrib import admin

from .models import Chat, Membership, Message

admin.site.register(Chat)
admin.site.register(Membership)
admin.site.register(Message)