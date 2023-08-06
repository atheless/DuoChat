from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from chat.models import Room, Profile, DuoConnectionEstablished
from django.core.cache import cache
from django.db.models import Q


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('login')


class SearchUsers(TemplateView):
    template_name = 'SearchUsers.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("search")
        if query:
            users_list = User.objects.filter(username__contains=query)
            print(users_list)
            return render(request, self.template_name, {'users_list': users_list, })

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def get_or_create_uuid_for_users(user1, user2):
    try:
        connection = DuoConnectionEstablished.objects.get(user1=user1, user2=user2)
        return connection.id
    except DuoConnectionEstablished.DoesNotExist:
        try:
            connection = DuoConnectionEstablished.objects.get(user1=user2, user2=user1)
            return connection.id
        except DuoConnectionEstablished.DoesNotExist:
            connection = DuoConnectionEstablished.objects.create(user1=user1, user2=user2)
            return connection.id


def get_user_status(user):
    # Try to get user status from cache
    status = cache.get(f'user_status_{user.pk}')
    if status is None:
        return 'Offline'
    if status is not None:
        return status


class DuoChatView(TemplateView):
    template_name = 'DuoChatView.html'

    def get(self, request, *args, **kwargs):
        if 'profile_uuid' in kwargs:
            try:
                self.target = Profile.objects.get(id=kwargs['profile_uuid'])
                self.uuid_con = get_or_create_uuid_for_users(self.request.user, self.target.user)
            except Profile.DoesNotExist:
                # return HttpResponseNotFound("UUID is incorrect.")
                return redirect(reverse('search-users'))
        else:
            # My contacts request.
            self.mycontacts_request = True
            return super().get(request, *args, **kwargs)

        self.mycontacts_request = False
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_uuid' in kwargs:

            try:
                context['contacts'] = DuoConnectionEstablished.objects.filter(
                    Q(user1=self.request.user) | Q(user2=self.request.user))
            except DuoConnectionEstablished.DoesNotExist:
                raise Exception

            context['user2'] = self.target.user
            context['uuid'] = self.uuid_con

            for c in context['contacts']:
                c.user1.profile.status = get_user_status(c.user1)
                c.user2.profile.status = get_user_status(c.user2)
                context['user2_onlinestatus'] = get_user_status(self.target.user)

        if self.mycontacts_request:
            try:
                context['contacts'] = DuoConnectionEstablished.objects.filter(
                    Q(user1=self.request.user) | Q(user2=self.request.user))
                context['mycontacts_request'] = 1
            except DuoConnectionEstablished.DoesNotExist:
                raise Exception

        return context


class FindRoomView(TemplateView):
    template_name = 'findroom.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context


class RoomView(TemplateView):
    template_name = 'viewroom.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_room, created = Room.objects.get_or_create(name=kwargs['room_name'])
        context['room'] = chat_room
        return context
