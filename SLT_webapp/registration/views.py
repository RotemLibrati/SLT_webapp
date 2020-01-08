from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Card, User, Friend, Message, GameSession
from django.views import generic
from .forms import CardForm, UserForm, ProfileForm, CompleteUserForm, LoginForm, ParentForm, FriendForm, MessageForm
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.contrib.sessions.models import Session
from django.utils import timezone



def info(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    return render(request, 'registration/info.html', context)


def index(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    return render(request, 'registration/index.html', context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('registration:profile'))
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)


def logout(request):
    request.session.flush()

    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return HttpResponseRedirect(reverse('registration:index'))


def inbox(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    current_user = request.user
    messages_received = list(
        Message.objects.filter(receiver=current_user, deleted_by_receiver=False).order_by('-sent_date'))
    messages_sent = list(Message.objects.filter(sender=current_user, deleted_by_sender=False).order_by('-sent_date'))
    return render(request, 'registration/inbox.html', {'user': current_user,
                                                       'messages_received': messages_received,
                                                       'messages_sent': messages_sent
                                                       })


def view_message(request, message_id):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    try:
        message = Message.objects.get(id=message_id)
    except (TypeError, Message.DoesNotExist):
        message = None
    return render(request, 'registration/message.html', {'user': request.user, 'message': message})


def delete_message(request, message_id):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    try:
        message = Message.objects.get(id=message_id)
        if request.user == message.receiver:
            message.deleted_by_receiver = True
        if request.user == message.sender:
            message.deleted_by_sender = True

        message.save()

        if message.deleted_by_sender and message.deleted_by_receiver:
            message.delete()
    except (TypeError, Message.DoesNotExist):
        error = "Message deletion failed."
        render(request, 'registration/failure.html', {'error': error})
    return HttpResponseRedirect(reverse('registration:inbox'))


def new_message(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user_list = User.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            receiver_name = form.cleaned_data['receiver']
            try:
                receiver = User.objects.get(username=receiver_name)
            except (TypeError, User.DoesNotExist):
                error = "Could not find user."
                render(request, 'registration/failure.html', {'error': error})
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            sent_date = datetime.now()
            message = Message(sender=sender, receiver=receiver, subject=subject, body=body, sent_date=sent_date)
            message.save()
            HttpResponseRedirect(reverse('registration:inbox'))
    else:
        form = MessageForm()
    return render(request, 'registration/new-message.html', {
        'form': form, 'users': user_list, 'user': request.user
    })


def profile(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    u1 = request.user
    try:
        friend = Friend.objects.get(current_user=u1)
        friends = list(map(lambda x: x.username, friend.users.all()))
    except (TypeError, Friend.DoesNotExist):
        friends = []
    up1 = get_object_or_404(UserProfile, user=u1)
    return render(request, 'registration/details.html', {'user': u1, 'profile': up1, 'friends': friends})


def add_friend(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            try:
                new_friend = User.objects.get(username=form.cleaned_data['new_friend'])
                if form.cleaned_data['action'] == 'Add':
                    Friend.make_friend(request.user, new_friend)
                else:
                    Friend.remove_friend(request.user, new_friend)
                return HttpResponseRedirect(reverse('registration:index'))
            except (TypeError, User.DoesNotExist):
                form = FriendForm()
    else:
        form = FriendForm()
        user_list = User.objects.all()
    return render(request, 'registration/add-friend.html', {
        'form': form, 'users': user_list
    })


def new_user(request):
    if request.method == 'POST':
        user_form = CompleteUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = get_object_or_404(User, username=user_form.cleaned_data['username'])
            return HttpResponseRedirect(reverse('registration:new-profile', args=[str(user.username)]))
    else:
        user_form = CompleteUserForm()
    return render(request, 'registration/new-user.html', {
        'user_form': user_form,
    })


def new_profile(request, username):
    # if request.user is None:
    #     return HttpResponse("Not logged in")

    def attach_user(sender, **kwargs):
        userprofile = kwargs['instance']
        userprofile.user = user
        post_save.disconnect(attach_user, sender=UserProfile)
        userprofile.save()

    if request.method == 'POST':
        user = User.objects.get(username=username)
        form = ProfileForm(request.POST)
        if form.is_valid():
            post_save.connect(attach_user, sender=UserProfile)
            form.save()
            if form.cleaned_data['type'] == 'parent':
                return HttpResponseRedirect(reverse('registration:new-profile-parent', args=[str(user.username)]))
            return HttpResponseRedirect(reverse('registration:index'))
    else:
        user = User.objects.get(username=username)
        form = ProfileForm()
    return render(request, 'registration/new-profile.html', {'user': user, 'form': form})


def new_profile_parent(request, username):
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=username)
            userprofile = get_object_or_404(UserProfile, user=user)
            son_user = get_object_or_404(User, username=form.cleaned_data['chosen_son'])
            userprofile.son = son_user
            userprofile.save()
            return HttpResponseRedirect(reverse('registration:index'))
    else:
        form = ParentForm()
    return render(request, 'registration/new-profile-parent.html', {'username': username, 'form': form})


# class DetailView(generic.DetailView):
#     model = UserProfile
#     template_name = 'registration/details.html'


def make_new_card(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    u1 = request.user
    up1 = get_object_or_404(UserProfile, user=u1)
    context = {'user': u1, 'profile': up1, 'form': CardForm()}
    return render(request, 'registration/make-new-card.html', context)


def card_check(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            word = form.cleaned_data.get('word')
            image = form.cleaned_data.get('image')
            cards = Card.objects.all()
            exist = False
            for c in cards:
                if c.word == word:
                    exist = True
            if not exist:
                obj = Card.objects.create(word=word, image=image)
                obj.user = request.user
                obj.save()
                return HttpResponseRedirect(reverse('registration:success'))
    else:
        form = CardForm()
    return render(request, 'registration/make-new-card.html', {'form': form})


def success(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    return render(request, 'registration/success.html', {'user': user})


def game(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    suspended = datetime.now() < context['profile'].suspention_time
    timeleft = context['profile'].suspention_time - datetime.now()
    context['suspended'] = suspended
    context['timeleft'] = timeleft
    if not suspended:
        session = GameSession(user=context['profile'])
        session.save()
        return render(request, 'registration/game.html', context)
    else:
        return render(request, 'registration/suspended.html', context)


def active_games(request):
    games = GameSession.objects.filter(time_stop__isnull=True)
    game_list = list(games)
    return render(request, 'registration/active-games.html', {'games': game_list})


def exit(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    session = GameSession.objects.filter(user=user_profile, time_stop__isnull=True)
    for i in session:
        i.time_stop = datetime.now()
        i.save()
    return HttpResponseRedirect(reverse('registration:index'))


def active_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_id_list)


def active_users_page(request):
    users = active_users()
    users = list(users)
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    return render(request, 'registration/active-users.html', {'current_user': user, 'users': users})