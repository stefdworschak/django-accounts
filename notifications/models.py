from django.db import models

from accounts.models import CustomUser


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Using "accounts.CustomUser" here to avoid a partially initialized
    # module error
    created_by = models.ForeignKey(CustomUser,
                                   related_name='sent_notifications',
                                   on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    text = models.TextField()

    recipients = models.ManyToManyField("accounts.CustomUser",
                                        related_name="notifications",
                                        null=True, blank=True)

    def __str__(self):
        return self.subject
