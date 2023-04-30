from django.contrib import admin

from chat.models import DuoMessage, Room, Message, DuoConnectionEstablished

admin.site.register(Room)
admin.site.register(Message)

admin.site.register(DuoMessage)
admin.site.register(DuoConnectionEstablished)
