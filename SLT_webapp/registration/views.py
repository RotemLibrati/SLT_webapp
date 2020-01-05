from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Card, User
from django.views import generic
from .forms import CardForm, UserForm, ProfileForm, CompleteUserForm, LoginForm, ParentForm
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from datetime import datetime

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


def profile(request):
    if request.user is None:
        return HttpResponse("Not logged in")
    u1 = request.user
    up1 = get_object_or_404(UserProfile, user=u1)
    return render(request, 'registration/details.html', {'user': u1, 'profile': up1})


def new_user(request):
    if request.method == 'POST':
        # request.user.userprofile.points = request.POST.get('points', 0)
        # request.user.userprofile.age = request.POST.get('age', 0)
        # request.user.userprofile.address = request.POST.get('address', '')

        user_form = CompleteUserForm(request.POST)
        # profile_form = ProfileForm(request.POST)  # , instance=request.POST.get('profile_form'))
        if user_form.is_valid():  # and profile_form.is_valid():
            user_form.save()
            user = get_object_or_404(User, username=user_form.cleaned_data['username'])
            # profile_form.save()
            return HttpResponseRedirect(reverse('registration:new-profile', args=[str(user.username)]))
    else:
        # user_form = UserForm()
        # profile_form = ProfileForm()
        user_form = CompleteUserForm()
    return render(request, 'registration/new-user.html', {
        'user_form': user_form,
        # 'profile_form': profile_form
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
    if request.user is None:
        return HttpResponse("Not logged in")
    u1 = request.user
    up1 = get_object_or_404(UserProfile, user=u1)
    context = {'user': u1, 'profile': up1, 'form': CardForm()}
    return render(request, 'registration/make-new-card.html', context)


def card_check(request):
    if request.user is None:
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
    if request.user is None:
        return HttpResponse("Not logged in")
    user = request.user
    return render(request, 'registration/success.html', {'user': user})


def game(request):
    if request.user is None:
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
        return render(request, 'registration/game.html', context)
    else:
        return render(request, 'registration/suspended.html', context)
