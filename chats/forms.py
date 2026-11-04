from django import forms
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()

class GroupCreateForm(forms.Form):
    name = forms.CharField(max_length=128)
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = User.objects.exclude(pk=user.pk).order_by("username")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Write a message...", "class": "form-control"}
            ),
        }