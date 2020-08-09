from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime
from datetime import date, timedelta

LANG_CHOICES = (
    ('de', 'German'),
    ('en', 'English'),
)

class CustomUser(AbstractUser):
    """ Representing an application user 
    
    Default fieldsets: Permissions, Personal info, Important dates

    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    language = models.CharField(
        null=False,
        default="en",
        max_length=255,
        choices=LANG_CHOICES,
    )
    language.fieldset = 'Personal info'
    language.is_registration = True
    language.is_custom = True

    pass

    def __str__(self):
        return self.first_name + ' ' + self.last_name
