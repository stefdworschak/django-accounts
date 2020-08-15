from django.contrib import admin

from .models import Notification
from accounts.models import CustomUser

admin.site.register(Notification)
