from django.contrib.auth.models import User
from django.db import models
import uuid


class Room(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, related_name="members")
    admins = models.ManyToManyField(User, related_name="admins")

    def get_members_count(self):
        return self.members.count()

    def join(self, user):
        self.members.add(user)
        self.save()

    def leave(self, user):
        self.members.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_members_count()})'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='originRoom')
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.content} [{self.timestamp}]'


class DuoConnectionEstablished(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='established_connection1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='established_connection')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user1} <|> {self.user2}'

    class Meta:
        verbose_name_plural = ("Duo Established Connections")
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name="unique_name_1"),
            models.UniqueConstraint(fields=['user2', 'user1'], name="unique_user_2"),
        ]


class DuoMessage(models.Model):
    connection_established = models.ForeignKey(DuoConnectionEstablished, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='messages')

    content = models.CharField(max_length=1000)
    upload = models.FileField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = ("Duo Messages")

    def __str__(self):
        return f'{self.connection_established} > {self.content} | {self.upload.name}'

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    STATUS = [
        ('Online', 'On-line'),
        ('Offline', 'Offline'),
    ]

    status = models.CharField(max_length=100, choices=STATUS, default="Offline")

    def __str__(self):
        return f'{self.user} - {self.id} - {self.status}'

    class Meta:
        verbose_name_plural = ("Profiles")
