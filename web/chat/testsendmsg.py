# Required for channel communication
import time

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import asyncio


def send_channel_message():

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('changes', {"type": "hello"})
    time.sleep(6)





# import channels.layers
# channel_layer = channels.layers.get_channel_layer()
# from asgiref.sync import async_to_sync
# async_to_sync(channel_layer.send)('changes', {"type": "hello"})
# async_to_sync(channel_layer.receive)('changes')