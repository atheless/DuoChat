from django.urls import re_path

from chat.Consumers import RoomConsumer, DuoChat
from chat.Consumers import Online

websocket_urlpatterns = [
    re_path(r'ws/room_chat/(?P<room_name>\w+)/$', RoomConsumer.ChatConsumer.as_asgi()),

    re_path(r'ws/duochat/(?P<uuid>[^/]+)/$', DuoChat.DuoChatConsumer.as_asgi()),

    re_path(r'ws/onlinestatus/', Online.OnlineConsumer.as_asgi()),
]
