from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Card, User
from django.views import generic
from .forms import CardForm, UserForm, ProfileForm, CompleteUserForm
from django.urls import reverse


def index(request):
    return HttpResponse("Hello world")


def profile(request, username):
    u1 = get_object_or_404(User, username=username)
    context = {'user': u1}
    return render(request, 'registration/index.html', context)


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
            return HttpResponseRedirect(reverse('registration:new-profile', args=(user.username,)))
    else:
        # user_form = UserForm()
        # profile_form = ProfileForm()
        user_form = CompleteUserForm()
    return render(request, 'registration/new-user.html', {
        'user_form': user_form,
        # 'profile_form': profile_form
    })


def new_profile(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('registration:profile', args=(user.username,)))
    else:
        user = get_object_or_404(User, username=username)
        form = ProfileForm()
    return render(request, 'registration/new-profile.html', {'user': user, 'form': form})


class DetailView(generic.DetailView):
    model = UserProfile
    template_name = 'registration/details.html'


def make_new_card(request, user_id):
    u1 = get_object_or_404(UserProfile, pk=user_id)
    context = {'user': u1, 'form': CardForm()}
    return render(request, 'registration/make-new-card.html', context)


def card_check(request, user_id):
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
                obj.save()
                return HttpResponseRedirect(reverse('registration:success', args=(user_id,)))
    else:
        form = CardForm()
    return render(request, 'registration/make-new-card.html', {'form': form})


def success(request, user_id):
    return render(request, 'registration/success.html', {'user_id': user_id})


def game(request, user_id):
    return render(request, 'registration/game.html', {'user_id': user_id})
