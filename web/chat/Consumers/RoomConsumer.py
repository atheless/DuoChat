import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Room, Message
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_DM = None

    @database_sync_to_async
    def get_or_create_Room(self):
        room, already_exist = Room.objects.get_or_create(name=self.room_name)
        return room

    @database_sync_to_async
    def reject_multiple_connections_from_same_user(self):
        if self.scope['user'] in self.room.members.all():
            return 1

    @database_sync_to_async
    def get_list_of_user(self):
        return [user.username for user in self.room.members.all()]

    # Deletes empty room.
    @database_sync_to_async
    def empty_remove_Room(self):
        if not self.room.members.exists():
            self.room.delete()

    @sync_to_async
    def add_to_Room(self):
        self.room.members.add(self.user)

    @sync_to_async
    def remove_from_Room(self):
        self.room.members.remove(self.user)

    @database_sync_to_async
    def save_message_to_db(self, message):
        Message.objects.create(user=self.user, room=self.room, content=message)

    @database_sync_to_async
    def load_messages_db(self):
        return self.room.originRoom.all()
    @database_sync_to_async
    def get_ser_msg(self, previous_messages):
        return MessageSerializer(previous_messages, many=True).data




    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = f'chat_{self.room_name}'  # Public group.

        self.user = self.scope['user']
        self.user_DM = f'DM_{self.user.username}'  # Group for direct messages.

        # Call database in a safe synchronous way.
        self.room = await self.get_or_create_Room()  # Room object database

        # Security: Check if user is authenticated.
        if not self.user.is_authenticated:
            await self.close()

        # Adds this channel to a public group.
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Accepts an incoming socket
        await self.accept()

        # Add current channel to direct messaging group
        await self.channel_layer.group_add(self.user_DM, self.channel_name)

        # Send the user list to the newly joined user
        await self.send(json.dumps({'type': 'user_list', 'users': await self.get_list_of_user(), }))

        # Load Messages
        previous_messages = await self.load_messages_db()
        await self.send(json.dumps({"type": "previous_messages", "messages": await self.get_ser_msg(previous_messages), }))

        # Call database in a safe synchronous way.
        # Adds self.user to list of members.
        await self.add_to_Room()

        # Send notification on join to public group.
        await self.channel_layer.group_send(self.room_group_name, {'type': 'user_join', 'user': self.user.username, })


    async def disconnect(self, close_code):  # Leaving
        # Remove this channel from public group.
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name, )

        # Remove this channel from direct messaging group.
        await self.channel_layer.group_discard(self.user_DM, self.channel_name, )

        # Send the notification event to the public group.
        await self.channel_layer.group_send(self.room_group_name, {'type': 'user_leave', 'user': self.user.username, })

        # Remove user from DB members list.
        await self.remove_from_Room()

        await self.empty_remove_Room()


    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message.startswith('/msg '):
            split = message.split(' ', 2)

            target = split[1]
            target_msg = split[2]

            # Send private message to the target
            await self.channel_layer.group_send(f'DM_{target}', {'type': 'private_message', 'user': self.user.username, 'message': target_msg, })

            # Send notification that message were delivered to the user. Sends a reply back down to this WebSocket.
            await self.send(json.dumps({'type': 'private_message_delivered', 'target': target, 'message': target_msg, }))
            return

        # If message is not special.
        # Send chat message to public group.
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': self.user.username, 'message': message, })

        # Save message to database.
        await self.save_message_to_db(message)

    async def chat_message(self, event):
        message = event["message"]
        username = event["user"]
        await self.send(text_data=json.dumps(event))

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))

    async def private_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def private_message_delivered(self, event):
        await self.send(text_data=json.dumps(event))



