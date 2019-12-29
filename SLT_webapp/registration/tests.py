from django.test import TestCase
from .models import User
class UserModelTests(TestCase):
    def test_was_born_recently_with_negative_age(self):
        past_user = User (1,'rotemli', 'rotem', 'librati', 'bash', -4)
        self.assertIs(past_user.was_born_recently(), False)