from main.helpers import create_presigned_s3_url

from django import template
from django.conf import settings
from django.core.cache import cache

register = template.Library()


@register.filter
def generate_media_url(filename):
    if settings.DEBUG:
        return f"{settings.MEDIA_URL}{filename}"
    else:
        if cache.get(filename):
            return cache.get(filename)
        custom_domain = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/'
        media_prefix = settings.MEDIA_URL.replace(custom_domain, '')
        presigned_url = create_presigned_s3_url(f'{media_prefix}{filename}')
        if presigned_url:
            cache.set(filename, presigned_url)
            return presigned_url
        return settings.DEFAULT_PROFILE_IMAGE
