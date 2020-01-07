from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


class UserProfile(models.Model):
    TYPES = (('parent', 'parent'), ('student', 'student'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    son = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='son')
    address = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPES, default='student')
    is_admin = models.BooleanField(default=False)
    suspention_time = models.DateTimeField(auto_now_add=True)

    def was_born_recently(self):
        if self.age <= 0:
            return False
        return self.age < 18

    def __str__(self):
        return str(self.user)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=50, blank=True)
    body = models.CharField(max_length=250, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender + ' to ' + self.receiver)


class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friends')
    current_user = models.ForeignKey(User, related_name="owner", null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    @classmethod
    def is_friend_of(cls, current_user, other_user):
        if Friend.objects.filter(current_user=current_user):
            if Friend.objects.filter(current_user=current_user)[0].users.filter(username=other_user.username):
                return True
        return False

    def __str__(self):
        return str(self.current_user)


class Prize(models.Model):
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=200)
    points = models.IntegerField()


class Winning(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, default=1)
    win_date = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', null=True)
    authorized = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.word


class GameSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    number_of_mistakes = models.IntegerField()
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    time_signature = models.DateTimeField(auto_now_add=True)
