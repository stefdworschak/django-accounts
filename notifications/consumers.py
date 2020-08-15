# trivia/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

CONSUMER_TYPE = 'notification'


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Route Kwargs: ", self.scope['url_route']['kwargs'])
        self.group_name = self.scope['url_route']['kwargs']['notification_id']
        self.room_group_name = f'{CONSUMER_TYPE}_{self.group_name}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_message(self, text_data):
        text_data_json = json.loads(text_data)
        category = text_data_json.get('category', 'default')
        message = text_data_json.get('message')
        extra_data = text_data_json.get('extra_data')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': CONSUMER_TYPE,
                'category': category,
                'message': message,
                'extra_data': extra_data,
            }
        )

    # Receive message from room group
    async def send_message(self, event):
        category = event.get('category', 'default')
        message = event.get('message')
        extra_data = event.get('extra_data')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': CONSUMER_TYPE,
            'category': category,
            'message': message,
            'extra_data': extra_data,
        }))
