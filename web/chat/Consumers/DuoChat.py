import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import DuoConnectionEstablished, DuoMessage
from chat.serializers import MessageSerializerDuo


class DuoChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_message_to_db(self, message):
        DuoMessage.objects.create(connection_established_id=self.UUID, author=self.user, content=message)

    @database_sync_to_async
    def load_messages_db(self):
        return DuoMessage.objects.filter(connection_established_id=self.UUID).order_by("timestamp")

    @database_sync_to_async
    def obtain_both_users_id(self):
        try:
            x = DuoConnectionEstablished.objects.get(id=self.UUID)
            return x.user1.id, x.user2.id
        except Exception:  # Security: Forged Request.
            self.close()

    @database_sync_to_async
    def get_ser_msg(self, previous_messages):
        return MessageSerializerDuo(previous_messages, many=True).data

    async def connect(self):

        # Security: Check if user is authenticated.
        if not self.scope['user'].is_authenticated:
            await self.close()

        self.UUID = self.scope['url_route']['kwargs']['uuid']
        self.user = self.scope['user']

        self.user1, self.user2 = await self.obtain_both_users_id()
        if self.user.id not in [self.user1, self.user2]:
            await self.close()

        # Accept incoming socket.
        await self.accept()

        # Load Messages.
        previous_messages = await self.load_messages_db()
        await self.send(
            json.dumps({"type": "previous_messages", "messages": await self.get_ser_msg(previous_messages), }))

        # Join room group.
        await self.channel_layer.group_add(self.UUID, self.channel_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.UUID, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message == 'typing':
            user_typing = text_data_json["user"]
            await self.channel_layer.group_send(self.UUID, {"type": "chat_typing", 'user': user_typing})
        elif message == 'stop_typing':
            user_stoped_typing = text_data_json["user"]
            await self.channel_layer.group_send(self.UUID, {"type": "chat_stop_typing", 'user': user_stoped_typing})
        else:
            # Send message to group_name.
            await self.channel_layer.group_send(self.UUID, {"type": "chat_message", 'user': self.user.username,
                                                            "message": message})
            # Save message to database.
            await self.save_message_to_db(message)

    ########
    # Events
    ########

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    # Receive message from room group
    async def chat_typing(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    # Receive message from room group
    async def chat_stop_typing(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
