from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
    user_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.user_name


    def was_born_recently(self):
        return self.age < 18

class Friend(models.Model):
    user_friend = models.ManyToManyField(User)

class Prize(models.Model):
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=200)
    points = models.IntegerField()

class Winning(models.Model):
    win_date = models.DateTimeField(auto_now_add=True)
    win_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.win_date
