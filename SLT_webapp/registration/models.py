from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    address = models.CharField(max_length=100, default='')
    age = models.IntegerField(blank=True, default=0)
    points = models.IntegerField(default=0)

    def was_born_recently(self):
        return self.age < 18

    def __str__(self):
        return self.user.username


# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])
#
#
# post_save.connect(create_profile, sender=User)


class Friend(models.Model):
    users = models.ManyToManyField(UserProfile)
    current_user = models.ForeignKey(UserProfile, related_name="owner", null=True, on_delete=models.CASCADE)

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
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.word


class GameSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    number_of_mistakes = models.IntegerField()
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    time_signature = models.DateTimeField(auto_now_add=True)
