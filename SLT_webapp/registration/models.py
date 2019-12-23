from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.user_name


class Friend(models.Model):
    user_friend = models.ForeignKey(User, on_delete=models.CASCADE)
