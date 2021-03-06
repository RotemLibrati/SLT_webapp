from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta, datetime

from django.utils import timezone


class Notifications(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=256)
    seen = models.BooleanField(default=False)

class Users(models.Model):
    user_id = models.CharField(max_length=256)
    last_visit = models.DateTimeField()

class Chat(models.Model):
    sender = models.CharField(max_length=256)
    receiver = models.CharField(max_length=256)
    msg = models.TextField()
    time = models.DateTimeField()

class UserProfile(models.Model):
    TYPES = (('parent', 'parent'), ('student', 'student'))
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    son = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='dad')
    address = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPES, default='student')
    is_admin = models.BooleanField(default=False)
    suspention_time = models.DateTimeField(default=datetime(2000, 1, 1))
    total_minutes = models.FloatField(default=0)
    last_login = models.DateTimeField(default=datetime(2000, 1, 1))
    rank = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    limit = models.DateTimeField(default=datetime(2000, 1, 1))

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
    TYPES = (('time', 'time'), ('moves', 'moves'), ('mistakes', 'mistakes'))
    name = models.CharField(max_length=100)
    condition_type = models.CharField(max_length=20, choices=TYPES, default='time')
    condition = models.IntegerField(default=1000)
    points = models.IntegerField(default=0)


class Winning(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, default=1)
    win_date = models.DateTimeField()
    seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.win_date = timezone.now()
        return super(Winning, self).save(*args, **kwargs)


class Card(models.Model):
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', null=True)
    authorized = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.word


class GameSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    number_of_mistakes = models.IntegerField(default=0)
    number_of_moves = models.IntegerField(default=0)
    time_start = models.DateTimeField()
    time_stop = models.DateTimeField(null=True, blank=True)
    difficulty = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.time_start = timezone.now()
        return super(GameSession, self).save(*args, **kwargs)

    def get_time_in_seconds(self):
        td = self.time_stop - self.time_start
        return td.total_seconds()

class UserReoprt(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.SET_NULL, null=True)
    reported = models.ForeignKey(User, related_name='reported', on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=100)
