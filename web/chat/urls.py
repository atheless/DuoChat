from django.urls import path

from .views import FindRoomView, RoomView, DuoChatView, SearchUsers

urlpatterns = [

    path('chat/', FindRoomView.as_view(), name='find-room'),
    path('chat/<str:room_name>/', RoomView.as_view(), name='chat-room'),

    path('duochat/', DuoChatView.as_view(), name='duo-chat'),
    path('duochat/<uuid:profile_uuid>', DuoChatView.as_view(), name='duo-chat'),

    path('SearchUsers', SearchUsers.as_view(), name='search-users'),

]
