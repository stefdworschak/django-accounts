from asgiref.sync import async_to_sync
import channels.layers

from django.db import models
from django.db.models.signals import post_save
# from django.dispatch import receiver

from accounts.models import CustomUser

STATUS = [
    ('unread', 'Unread'),
    ('read', 'Read'),
    ('deleted', 'Deleted')
]
channel_layer = channels.layers.get_channel_layer()


class NotificationThread(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser,
                                   related_name='sent_notifications',
                                   on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    text = models.TextField()

    recipients = models.ManyToManyField("accounts.CustomUser",
                                        related_name="notification_threads",
                                        blank=True)

    def __str__(self):
        return self.subject


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipient = models.ForeignKey(CustomUser,
                                  related_name='notifications',
                                  on_delete=models.CASCADE)
    notification_thread = models.ForeignKey(NotificationThread,
                                            related_name='notification_thread',
                                            on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS)

    def __str__(self):
        return f"Notification to: {self.recipient.username}"


def send_notification(sender, instance, **kwargs):
    print("NotificationThread created")
    for recipient in instance.recipients.all():
        new_notification = Notification(
            recipient=recipient,
            notification_thread=instance,
            status='unread'
        )
        new_notification.save()
        async_to_sync(channel_layer.group_send)(f'user{recipient.id}', {
            'type': 'send_message',
            'subject': instance.subject,
            'message': instance.text,
            'category': 'notification',
            'extra_data': {}
            })
        print(f"Notifcation for {recipient.email} created.")
    pass


post_save.connect(send_notification, sender=NotificationThread)
