from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User
from django.views import generic


def index(request):
    return HttpResponse("Hello world")


def profile(request, user_id):
    u1 = get_object_or_404(User, pk=user_id)
    context = {'user': u1}
    return render(request, 'registration/index.html', context)


class DetailView(generic.DetailView):
    model = User
    template_name = 'registration/details.html'

