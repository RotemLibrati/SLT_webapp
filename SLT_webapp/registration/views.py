from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    return HttpResponse("Hello world")


def profile(request, user_id):
    u1 = User.objects.get(pk=user_id)
    context = {'user': u1}
    return render(request, 'registration/index.html', context)