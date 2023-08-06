import asyncio
import json
from datetime import datetime, timedelta

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Profile

from django.core.cache import cache


class OnlineConsumer(AsyncWebsocketConsumer):
    CACHE_TIMEOUT = 1000

    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()

        self.group_name = 'online'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Set user as online in cache
        cache.set(f'user_status_{self.user.pk}', 'Online', timeout=self.CACHE_TIMEOUT)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
