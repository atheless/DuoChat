import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path


# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from chat.Consumers import RoomConsumer, DuoChat, Online

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/room_chat/(?P<room_name>\w+)/$', RoomConsumer.ChatConsumer.as_asgi()),
                re_path(r'ws/duochat/(?P<uuid>[^/]+)/$', DuoChat.DuoChatConsumer.as_asgi()),
                re_path(r'ws/onlinestatus/', Online.OnlineConsumer.as_asgi()),
            ])
        )
    ),
})
