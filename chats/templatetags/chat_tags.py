from django import template

register = template.Library()

@register.filter
def title_for(chat, user):
    """Usage in templates: {{ chat|title_for:user }}"""
    return chat.title_for(user)