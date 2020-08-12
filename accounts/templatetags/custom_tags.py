from django import template
from django.conf import settings

register = template.Library()


@register.filter
def generate_media_url(filename):
    return f"{settings.MEDIA_URL}{filename}"
