from django.contrib import admin

from .models import NotificationThread, Notification

admin.site.register(NotificationThread)
admin.site.register(Notification)
