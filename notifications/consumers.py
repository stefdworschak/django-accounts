# trivia/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

CONSUMER_TYPE = 'notification'


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['notification_group_id']  # noqa: E501
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        category = text_data_json.get('category')
        subject = text_data_json.get('subject')
        message = text_data_json.get('message')
        extra_data = text_data_json.get('extra_data')
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {   
                # The type attribute needs to be the same name as the
                # "send_message" function name
                'type': 'send_message',
                'category': category,
                'subject': subject,
                'message': message,
                'extra_data': extra_data,
            }
        )

    # Receive message from room group
    async def send_message(self, event):
        category = event.get('category')
        subject = event.get('subject')
        message = event.get('message')
        extra_data = event.get('extra_data')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            # The type attribute needs to be the same name as the
            # "send_message" function name
            'type': 'send_message',
            'category': category,
            'subject': subject,
            'message': message,
            'extra_data': extra_data,
        }))
