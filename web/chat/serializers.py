from rest_framework import serializers

from chat.models import Message, DuoMessage


class MessageSerializer(serializers.ModelSerializer):

    def getUsername(self, obj):
        return obj.user.username

    username = serializers.SerializerMethodField("getUsername")

    class Meta:
        model = Message
        fields = ['room', 'username', 'content', 'timestamp']


class MessageSerializerDuo(serializers.ModelSerializer):

    def getAuthor(self, obj):
        return obj.author.username

    author = serializers.SerializerMethodField("getAuthor")

    class Meta:
        model = DuoMessage
        fields = ['author', 'content', 'timestamp', 'read']
