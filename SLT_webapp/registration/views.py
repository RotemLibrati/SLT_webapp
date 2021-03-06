import json
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Card, User, Friend, Message, GameSession, Prize, Winning, Notifications, UserReoprt
from .forms import CardForm, UserForm, ProfileForm, CompleteUserForm, LoginForm, ParentForm, FriendForm, MessageForm, \
    RankGameForm, PrizeForm, SuspendUsers, OnlineLimitForm, InviteSon, InviteFriend, ChooseLevelSon, \
    ReportUserForm
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from datetime import datetime, timedelta
from braces.views import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from django.contrib.sessions.models import Session


def delete_notification(request, notification_id):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    try:
        notification = Notifications.objects.get(id=notification_id)
        notification.delete()
    except (TypeError, Notifications.DoesNotExist):
        error = "Notification deletion failed."
        render(request, 'registration/failure.html', {'error': error})
    return HttpResponseRedirect(reverse('registration:notifications'))


def notifications(request):  # TODO: fix links menu in template
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    # try:
    #     message = Message.objects.get(id=message_id)
    # except (TypeError, Message.DoesNotExist):
    #     message = None
    notifications = Notifications.objects.filter(receiver=request.user)
    return render(request, 'registration/notifications.html', {'notifications': notifications})


class UserListView(LoginRequiredMixin, generic.ListView):  # TODO: fix links menu in template
    model = get_user_model()
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'registration/chat.html'
    login_url = 'login/'


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
                user = request.user
                userprofile = UserProfile.objects.get(user=user)
                if userprofile.last_login.date() < timezone.now().date():
                    userprofile.daily_minutes = 0
                userprofile.last_login = timezone.now()
                userprofile.save()
                return HttpResponseRedirect(reverse('registration:profile'))
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)


def logout(request):
    userprofile = UserProfile.objects.get(user=request.user)
    td = timezone.now() - userprofile.last_login
    userprofile.total_minutes += (td.total_seconds() / 60)
    userprofile.save()
    request.session.flush()

    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return HttpResponseRedirect(reverse('registration:index'))


def inbox(request):  # TODO: fix links menu in template
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
        error = "Message getting failed."
        return render(request, 'registration/failure.html', {'error': error})
    return render(request, 'registration/message.html', {'user': request.user,
                                                         'message': message,
                                                         })


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


def new_message(request, **kwargs):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user_profile = UserProfile.objects.get(user=request.user)
    user_list = User.objects.all()
    profile_list = UserProfile.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        request.user.reply = None
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
            sent_date = timezone.now()
            message = Message(sender=sender, receiver=receiver, subject=subject, body=body, sent_date=sent_date)
            message.save()
            return HttpResponseRedirect(reverse('registration:inbox'))
            return HttpResponseRedirect(reverse('registration:success-message'))
    else:
        form = MessageForm()
        if kwargs:
            if kwargs['reply']:
                form = MessageForm({'receiver': kwargs['reply']})
    return render(request, 'registration/new-message.html', {
        'form': form, 'users': user_list, 'user': request.user, 'user_profile': user_profile, 'profiles': profile_list
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
        # messages.add_message(request, messages.INFO, 'Hello world.')
    try:
        parent_profile = UserProfile.objects.get(son=u1)
        parent_user = User.objects.get(username=parent_profile.user.username)
        if parent_profile[0]:
            alert = Notifications(receiver=parent_user[0], message='your son has won a new prize')
            alert.save()
    except (TypeError, UserProfile.DoesNotExist):
        parent_user = []
    up1 = get_object_or_404(UserProfile, user=u1)
    messagesList = Notifications.objects.filter(receiver=request.user, seen=False)
    winningList = Winning.objects.filter(user=up1, seen=False)
    for m in messagesList:
        messages.add_message(request, messages.INFO, m.message)
        m.seen = True
        m.save()
    for m in winningList:
        messages.add_message(request, messages.INFO, f'you have won {m.prize.name}')
        m.seen = True
        m.save()
    # Alerts.objects.filter(receiver=request.user).delete()
    return render(request, 'registration/profile-details.html', {'user': u1, 'profile': up1, 'friends': friends})


def add_friend(request):  # TODO: fix links menu in template
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            try:
                new_friend = User.objects.get(username=form.cleaned_data['new_friend'])
                if form.cleaned_data['action'] == 'Add':
                    Friend.make_friend(request.user, new_friend)
                    alert = Notifications(receiver=new_friend,
                                          message=f"{request.user.username} has added you to the friend list")
                    alert.save()
                else:
                    Friend.remove_friend(request.user, new_friend)
                    alert = Notifications(receiver=new_friend,
                                          message=f"{request.user.username} has removed you from the friend list")
                    alert.save()
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
            user = get_object_or_404(User, username=username)
            userprofile = get_object_or_404(UserProfile, user=user)
            son_user = get_object_or_404(User, username=form.cleaned_data['chosen_son'])
            userprofile.son = son_user
            userprofile.save()
            return HttpResponseRedirect(reverse('registration:index'))
    else:
        users = UserProfile.objects.filter(type='student')
        form = ParentForm()
    return render(request, 'registration/new-profile-parent.html', {'username': username, 'form': form, 'users': users})


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
    suspended = timezone.now() < context['profile'].suspention_time
    timeleft = context['profile'].suspention_time - timezone.now()
    context['suspended'] = suspended
    context['timeleft'] = timeleft
    if not suspended:
        session = GameSession(user=context['profile'])
        session.save()
        user4level = UserProfile.objects.get(user=request.user)
        image = list(Card.objects.all())
        if user4level.level == 1:
            rand = random.sample(image, 6)
        elif user4level.level == 2:
            rand = random.sample(image, 8)
        else:
            rand = random.sample(image, 10)
        context['image'] = rand
        context['level'] = user4level.level
        return render(request, 'registration/game.html', context)
    else:
        return render(request, 'registration/suspended.html', context)


# def active_games(request):
#     games = GameSession.objects.filter(time_stop__isnull=True)
#     game_list = list(games)
#     return render(request, 'registration/active-games.html', {'games': game_list})
def active_games(request):  # TODO: fix links menu in template
    user = request.user
    up1 = get_object_or_404(UserProfile, user=user)
    games = GameSession.objects.filter(time_stop__isnull=True)
    game_list = list(games)
    return render(request, 'registration/active-games.html', {'games': game_list, 'up': up1})


def reports_menu(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    return render(request, 'registration/reports-menu.html', {'user': user_profile, 'user_list': user_list})


def reports_menu_users(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    return render(request, 'registration/reports-menu-users.html', {'user': user_profile, 'user_list': user_list})


def reports_users(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    return render(request, 'registration/details-of-users.html', {'user': user_profile, 'user_list': user_list})


def parent_list(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    return render(request, 'registration/parent-list.html', {'user': user_profile, 'user_list': user_list})


def avg_points(request):
    user = request.user
    up1 = get_object_or_404(UserProfile, user=user)
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    sum = 0
    for p in user_list:
        sum += p.points
    avg = sum / len(user_list)
    return render(request, 'registration/avg-points.html',
                  {'user': user_profile, 'user_list': user_list, 'u1': user, 'up': up1, 'avg': avg})


def exit_game(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    session = GameSession.objects.filter(user=user_profile, time_stop__isnull=True)
    for i in session:
        i.time_stop = timezone.now()
        i.save()
    session = GameSession.objects.filter(user=user_profile)
    game_session = list(session)[-1]
    if game_session.finished:
        game_time = game_session.get_time_in_seconds()
        game_moves = game_session.number_of_moves
        game_mistakes = game_session.number_of_mistakes
        prizes = Prize.objects.all()
        for prize in prizes:  # TODO: add notification for winning
            if prize.condition_type == 'time' and game_time < prize.condition:
                win = Winning(prize=prize, user=user_profile)
                win.save()
                user_profile.points += prize.points
                user_profile.save()
            elif prize.condition_type == 'moves' and game_moves < prize.condition:
                win = Winning(prize=prize, user=user_profile)
                win.save()
                user_profile.points += prize.points
                user_profile.save()
            elif prize.condition_type == 'mistakes' and game_mistakes < prize.condition:
                win = Winning(prize=prize, user=user_profile)
                win.save()
                user_profile.points += prize.points
                user_profile.save()
    return HttpResponseRedirect(reverse('registration:index'))


def total_time_son(request):  # TODO: fix links menu in template
    current_user_profile = UserProfile.objects.get(user=request.user)
    son_user = User.objects.get(username=current_user_profile.son.username)
    son_profile = UserProfile.objects.get(user=son_user)
    if son_profile:
        context = {'user': current_user_profile, 'son_user': son_user, 'son_profile': son_profile}
        return render(request, 'registration/total-time-son.html', context)
    return HttpResponseRedirect(reverse('registration:index'))


def rank_game(request):  # TODO: fix links menu in template
    if request.method == 'POST':
        form = RankGameForm(request.POST)
        if form.is_valid():
            rank_val = form.cleaned_data['rank']
            user = request.user
            up1 = get_object_or_404(UserProfile, user=user)
            up1.rank = rank_val
            up1.save()
        return HttpResponseRedirect(reverse('registration:rank-success'))
    else:
        form = RankGameForm()

    return render(request, 'registration/rank-game.html', {'form': form})


def rank_success(request):
    return render(request, 'registration/rank-success.html')


def success_message(request):
    return render(request, 'registration/success-message.html')


def success_level(request):
    return render(request, 'registration/success-level.html')


def success_invite(request):
    return render(request, 'registration/success-invite.html')


def rank_for_admin(request):
    user = request.user
    user_profile = UserProfile.objects.all()
    user_list = list(user_profile)
    sum = 0
    for p in user_list:
        sum += p.rank
    avg = sum / len(user_list)
    return render(request, 'registration/rank-for-admin.html',
                  {'user': user_profile, 'user_list': user_list, 'avg': avg})


def active_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_id_list)


def active_users_page(request):
    user = request.user
    up1 = get_object_or_404(UserProfile, user=user)
    users = active_users()
    users = list(users)
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    return render(request, 'registration/active-users.html', {'current_user': user, 'users': users, 'up': up1})


def report_user(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    if request.method == 'POST':
        form = ReportUserForm(request.POST)
        if form.is_valid():
            reporter = request.user
            reported_s = form.cleaned_data.get('user_name')
            reported = User.objects.get(username=reported_s)
            reason = form.cleaned_data.get('reason')
            user_report = UserReoprt(reporter=reporter, reported=reported, reason=reason)
            user_report.save()
            return HttpResponseRedirect(reverse('registration:index'))
    else:
        users = list(User.objects.all())
        form = ReportUserForm()
    return render(request, 'registration/report-user.html', {'form': form, 'users': users})


def level_of_son(request):  # TODO: add design to template and fix links menu
    if request.method == 'POST':
        form = ChooseLevelSon(request.POST)
        if form.is_valid():
            level_val = form.cleaned_data['level']
            user = request.user
            up1 = get_object_or_404(UserProfile, user=user)
            current_user_profile = UserProfile.objects.get(user=request.user)
            son_user = User.objects.get(username=current_user_profile.son.username)
            son_profile = UserProfile.objects.get(user=son_user)
            son_profile.level = level_val
            son_profile.save()
        return HttpResponseRedirect(reverse('registration:success-level'))
    else:
        form = ChooseLevelSon()
    current_user_profile = UserProfile.objects.get(user=request.user)
    son_user = User.objects.get(username=current_user_profile.son.username)
    son_profile = UserProfile.objects.get(user=son_user)
    context = {'user': current_user_profile, 'son_user': son_user, 'son_profile': son_profile, 'form': form}
    return render(request, 'registration/level-of-son.html', context)


def lottery_for_tournament(request):  # TODO: fix links menu in template
    user = request.user
    user_names = map(lambda x: x.user.username, UserProfile.objects.all())
    user_name_list = list(user_names)
    listof2 = []
    lastlist = []
    templist = user_name_list
    i = len(templist) // 2
    for _ in range(i):
        listof2 = random.choices(templist, k=2)
        while listof2[0] == listof2[1]:
            listof2 = random.choices(templist, k=2)
        tuple1 = (listof2[0], listof2[1])
        lastlist.append(tuple1)
        templist.remove(listof2[0])
        templist.remove(listof2[1])
    j = 0
    while j < i:
        alert = Notifications(receiver=User.objects.get(username=lastlist[j][0]), message=f'You have 2 day to play against {lastlist[j][1]}')
        alert.save()
        alert = Notifications(receiver=User.objects.get(username=lastlist[j][1]), message=f'You have 2 day to play against {lastlist[j][0]}')
        alert.save()
        j = j + 2
    return render(request, 'registration/lottery.html', {'pairs_list': lastlist})


def send_game(request):
    data = request.body.decode('utf-8')
    received_json_data = json.loads(data)
    moves = received_json_data['moves']
    mistakes = received_json_data['mistakes']
    finished = received_json_data['finished']
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        sessions = list(GameSession.objects.filter(user=user_profile, time_stop__isnull=True))
        gs = sessions[-1]
        gs.number_of_mistakes = mistakes
        gs.number_of_moves = moves
        gs.finished = finished
        gs.save()
        for i in sessions:
            i.time_stop = timezone.now()
            i.save()
    except (TypeError, GameSession.DoesNotExist):
        pass
    return HttpResponse("hello")


def invite_friend(request):  # TODO: fix links menu in template
    user = request.user
    if request.method == 'POST':
        form = InviteFriend(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['chosen_friend']
            receiver_user = User.objects.get(username=receiver)
            alert = Notifications(receiver=receiver_user, message=f'You have been invited to a game by {user.username}')
            alert.save()
        return HttpResponseRedirect(reverse('registration:success-invite'))
    else:
        form = InviteFriend()
        friend, created = Friend.objects.get_or_create(current_user=user)
        friend_list = list(map(lambda x: x.username, friend.users.all()))
    return render(request, 'registration/invite-friend.html',
                  {'form': form, 'friend': friend, 'friend_list': friend_list})


def suspend_users(request):  # TODO: fix links menu in template
    user = request.user
    if request.method == 'POST':
        form = SuspendUsers(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['chosen_suspend']
            receiver_user = User.objects.get(username=receiver)
            alert = Notifications(receiver=receiver_user, message=f'You are suspended fot 5 hours by {user.username}')
            alert.save()
            user_profile = UserProfile.objects.get(user=receiver_user)
            user_profile.suspention_time = timezone.now() + timedelta(hours=5)
            user_profile.save()
        return HttpResponseRedirect(reverse('registration:index'))
    else:
        form = SuspendUsers()
        users = User.objects.all()

    return render(request, 'registration/suspend-users.html', {'form': form, 'users': users})


# def invite_friend(request, username):
#     if request.method == 'POST':
#         form = InviteFriend(request.POST)
#         if form.is_valid():
#             form.save()
#             user = get_object_or_404(User, username=username)
#             userprofile = get_object_or_404(UserProfile, user=user)
#             son_user = get_object_or_404(User, username=form.cleaned_data['chosen_friend'])
#             userprofile.friend = friend_user
#             userprofile.save()
#             return HttpResponseRedirect(reverse('registration:index'))
#     else:
#         form = ParentForm()
#     return render(request, 'registration/new-profile-parent.html', {'username': username, 'form': form})
#
# def send_game(request):
#     data = request.body.decode('utf-8')
#     received_json_data = json.loads(data)
#     moves = received_json_data['moves']
#     mistakes = received_json_data['mistakes']
#     user = request.user
#     up1 = get_object_or_404(UserProfile, user=user)
#     up1.points += 100 - mistakes
#     up1.save()
#     print(up1.points)
#     return HttpResponse("hello")
# def logout(request):
#     userprofile = UserProfile.objects.get(user=request.user)
#     td = datetime.now() - userprofile.last_login
#     userprofile.total_minutes += (td.total_seconds() / 60)
#     userprofile.save()
#     request.session.flush()
#
#     if hasattr(request, 'user'):
#         request.user = AnonymousUser()
#     return HttpResponseRedirect(reverse('registration:index'))
# def send_game(request):
#     data = request.body.decode('utf-8')
#     received_json_data = json.loads(data)
#     moves = received_json_data['moves']
#     mistakes = received_json_data['mistakes']
#     print(f'moves={moves}. mistakes={mistakes}')
#     return HttpResponse("hello")


# def time_restriction(request):
#     if request.user is None or not request.user.is_authenticated:
#         return HttpResponse("Not logged in")
#     user_profile = UserProfile.objects.get(user=request.user)
#     son_profile = UserProfile.objects.get(user=user_profile.son)
#     son_user = User.objects.get(username=son_profile.user.username)
#     if request.method == 'POST':
#         form = OnlineLimitForm(request.POST)
#         if form.is_valid():
#             minutes = form.cleaned_data.get('minutes')
#             son_profile.limitation = minutes
#             son_profile.save()
#             return HttpResponseRedirect(reverse('registration:index'))
#     else:
#         form = OnlineLimitForm()
#     return render(request, 'registration/time-restriction.html')


def exceeded_limitation(user):
    profile = UserProfile.objects.get(user=user)
    return profile.daily_limitation > profile.limitation


def limit_son(request):  # TODO: fix links menu in template
    user_profile = UserProfile.objects.get(user=request.user)
    son_user = user_profile.son
    son_profile = UserProfile.objects.get(user=son_user)
    if request.method == 'POST':
        son_profile.limit = timezone.now() + timedelta(hours=2)
        son_profile.save()
        alert = Notifications(receiver=son_user, message=f'You have passed the limit set by your dad')
        alert.save()
        return HttpResponseRedirect(reverse('registration:index'))
    return render(request, 'registration/limit-son.html', {'son': son_profile})


def game_sessions_report(request):  # TODO: fix links menu in template
    user_profile = UserProfile.objects.get(user=request.user)
    son_user = user_profile.son
    son_profile = UserProfile.objects.get(user=son_user)
    game_list = GameSession.objects.filter(user=son_profile)
    return render(request, 'registration/game-sessions-report.html', {'game_list': game_list})


# def invite_friend(request):
#     user = request.user
#     if request.method == 'POST':
#         form = InviteFriend(request.POST)
#         if form.is_valid():
#             receiver = form.cleaned_data['chosen_friend']
#             receiver_user = User.objects.get(username=receiver)
#             alert = Notifications(receiver=receiver_user, message=f'You have been invited to a game by {user.username}')
#             alert.save()
#         return HttpResponseRedirect(reverse('registration:success-invite'))
#     else:
#         form = InviteFriend()
#         friend = Friend.objects.filter(current_user=user)[0]
#         friend_list = list(map(lambda x: x.username, friend.users.all()))
#     return render(request, 'registration/invite-friend.html', {'form': form, 'friend': friend, 'friend_list':friend_list})

def suspend_users(request):
    user = request.user
    if request.method == 'POST':
        form = SuspendUsers(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['chosen_suspend']
            receiver_user = User.objects.get(username=receiver)
            alert = Notifications(receiver=receiver_user, message=f'You are suspended fot 5 hours by {user.username}')
            alert.save()
            user_profile = UserProfile.objects.get(user=receiver_user)
            user_profile.suspention_time = timezone.now() + timedelta(hours=5)
            user_profile.save()
        return HttpResponseRedirect(reverse('registration:index'))
    else:
        form = SuspendUsers()
        users = User.objects.all()

    return render(request, 'registration/suspend-users.html', {'form': form, 'users': users})


def pending_cards(request):  # TODO: fix links menu in template
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    cardtoaccept = Card.objects.filter(authorized=False)
    if request.method == 'POST':
        checkscards = request.POST.getlist('checks[]')
        for word in checkscards:
            for card in cardtoaccept:
                if word == card.word:
                    card.authorized = True
                    card.save()
        return HttpResponseRedirect(reverse('registration:pending-cards'))
    else:
        return render(request, 'registration/pending-cards.html', {'image': cardtoaccept})


def points_users(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.all()
    return render(request, 'registration/points-users.html', {'user': user, 'user_profile': user_profile})


def personal_tournament(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = list(UserProfile.objects.all())
    i = 0
    while i < len(user_profile):
        receiver_user = User.objects.get(username=user_profile[i])
        alert = Notifications(receiver=receiver_user, message=f'You have 2 day to play in personal tournament')
        alert.save()
        i += 1
    return render(request, 'registration/send-notification.html', {'user': user, 'user_profile': user_profile})


def points_of_son(request):  # TODO: fix links menu in template
    user = request.user
    user_profile = UserProfile.objects.get(user=request.user)
    son_user = user_profile.son
    son_profile = UserProfile.objects.filter(user=son_user)
    return render(request, 'registration/points-of-son.html', {'user': user, 'son_profile': son_profile[0]})


def invite_son(request):  # TODO: fix links menu in template
    user = request.user
    if request.method == 'POST':
        form = InviteSon(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['chosen_son_for_game']
            receiver_user = User.objects.get(username=receiver)
            alert = Notifications(receiver=receiver_user, message=f'You have been invited to a game by {user.username}')
            alert.save()
        return HttpResponseRedirect(reverse('registration:success-invite'))
    else:
        form = InviteSon()
        user = request.user
        user_profile = UserProfile.objects.get(user=request.user)
        son_user = user_profile.son
        son_profile = UserProfile.objects.filter(user=son_user)
    return render(request, 'registration/invite-son.html', {'form': form, 'son_profile': son_profile, 'user': user})


def new_prize(request):  # TODO: fix links menu in template
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    if request.method == 'POST':
        form = PrizeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('registration:index'))
    else:
        form = PrizeForm()
    return render(request, 'registration/new-prize.html', {
        'form': form, 'user': request.user
    })


def winnings(request):  # TODO: fix links menu in template
    winnings_list = Winning.objects.filter(user=UserProfile.objects.get(user=request.user))
    return render(request, 'registration/winnings.html', {'winnings': winnings_list})
