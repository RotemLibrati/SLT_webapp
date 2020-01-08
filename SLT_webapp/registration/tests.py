from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile
from datetime import datetime


class UserProfileModelTests(TestCase):
    def test_was_born_recently_with_negative_age(self):
        past_user = UserProfile(user=None, son=None, address='asd', age=-5,points=0, type='student', is_admin=False, suspention_time=datetime.now())
        self.assertIs(past_user.was_born_recently(), False)

    def test_was_born_recently_with_zero_age(self):
        zero_user = UserProfile(user=None, son=None, address='asd', age=0, points=0, type='student', is_admin=False,
                                suspention_time=datetime.now())
        self.assertIs(zero_user.was_born_recently(), False)

    def test_was_born_recently_with_positive_age_less_then_18(self):
        user = UserProfile(user=None, son=None, address='asd', age=5, points=0, type='student', is_admin=False,
                                suspention_time=datetime.now())
        self.assertIs(user.was_born_recently(), True)

    def test_was_born_recently_with_positive_age_greater_then_18(self):
        user = UserProfile(user=None, son=None, address='asd', age=25, points=0, type='student', is_admin=False,
                                suspention_time=datetime.now())
        self.assertIs(user.was_born_recently(), False)


class IndexViewTests(TestCase):
    def test_title(self):
        response = self.client.get(reverse('registration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Language Teacher")

    def test_game_links_without_login(self):
        response = self.client.get(reverse("registration:index"))
        self.assertContains(response, 'Login with existing user')
        self.assertContains(response, 'Make a new user')


# class LogInTest(TestCase):
#     def setUp(self):
#         self.credentials = {
#             'username': 'testuser',
#             'password': 'secret'}
#         u1 = User(**self.credentials)
#         u1.save()
#
#     def test_login(self):
#         # send login data
#         response = self.client.post(reverse('registration:login'), self.credentials, follow=True)
#         # should be logged in now
#         self.assertTrue(response.context['user'].is_authenticated)
