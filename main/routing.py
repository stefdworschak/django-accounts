from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from notifications import consumers as notification_consumers

websocket_urlpatterns = [
    path('ws/notifications/<str:notification_id>/',
         notification_consumers.NotificationConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})