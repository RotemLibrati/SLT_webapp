from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Card
from django.views import generic
from .forms import CardForm
from django.urls import reverse


def index(request):
    return HttpResponse("Hello world")


def profile(request, user_id):
    u1 = get_object_or_404(User, pk=user_id)
    context = {'user': u1}
    return render(request, 'registration/index.html', context)


class DetailView(generic.DetailView):
    model = User
    template_name = 'registration/details.html'


def make_new_card(request, user_id):
    u1 = get_object_or_404(User, pk=user_id)
    context = {'user': u1}
    context['form'] = CardForm()
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
