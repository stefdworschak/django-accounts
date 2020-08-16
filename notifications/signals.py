from django.db.models.signals import post_save

from .models import NotificationThread, Notification


def send_notification(sender, instance, **kwargs):
    print("NotificationThread created")
    for recipient in instance.recipients.all():
        new_notification = Notification(
            recipient=recipient,
            notification_thread=instance,
            status='unread'
        )
        new_notification.save()
        print(f"Notifcation for {recipient.email} created.")
    pass


post_save.connect(send_notification, sender=NotificationThread)
