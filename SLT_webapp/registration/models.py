from django.db import models
import datetime



class User(models.Model):
    user_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    age = models.IntegerField()
    points= models.IntegerField(default=0)

    def was_born_recently(self):
        return self.age < 18

    def __str__(self):
        return self.user_name


class Friend(models.Model):
    users = models.ManyToManyField(User)
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

    def __str__(self):
        return str(self.current_user)


class Prize(models.Model):
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=200)
    points = models.IntegerField()


class Winning(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,default=1)
    win_date = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/',null=True)
    authorized = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    number_of_mistakes = models.IntegerField()
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    time_signature = models.DateTimeField(auto_now_add=True)

