from django.contrib.auth.models import User
from django.contrib.auth import login
from django.test import TestCase, Client
from django.urls import reverse, resolve
from . import views
from .models import UserProfile, Message
from datetime import datetime


class TestUserProfileModel(TestCase):
    def test_was_born_recently_with_negative_age(self):
        past_user = UserProfile(user=None, son=None, address='asd', age=-5, points=0, type='student', is_admin=False,
                                suspention_time=datetime.now())
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


class TestIndexView(TestCase):
    def test_title(self):
        response = self.client.get(reverse('registration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Language Teacher")

    def test_menu(self):
        response = self.client.get(reverse('registration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Main menu")

    def test_game_links_without_login(self):
        response = self.client.get(reverse("registration:index"))
        self.assertContains(response, 'Login with existing user')
        self.assertContains(response, 'Make a new user')


class TestUrl(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_registration_index_url_is_resolved(self):
        url = reverse('registration:index')
        self.assertEquals(resolve(url).func, views.index)

    def test_registration_login_url_is_resolved(self):
        url = reverse('registration:login')
        self.assertEquals(resolve(url).func, views.login_view)

    def test_registration_new_user_url_is_resolved(self):
        url = reverse('registration:new-user')
        self.assertEquals(resolve(url).func, views.new_user)

    def test_registration_new_profile_url_is_resolved(self):
        url = reverse('registration:new-profile', args=['testuser'])
        self.assertEquals(resolve(url).func, views.new_profile)

    def test_registration_new_profile_parent_url_is_resolved(self):
        url = reverse('registration:new-profile-parent', args=['tsetuser'])
        self.assertEquals(resolve(url).func, views.new_profile_parent)

    def test_registration_profile_url_is_resolved(self):
        url = reverse('registration:profile')
        self.assertEquals(resolve(url).func, views.profile)

    def test_registration_logout_url_is_resolved(self):
        url = reverse('registration:logout')
        self.assertEquals(resolve(url).func, views.logout)

    def test_registration_game_url_is_resolved(self):
        url = reverse('registration:game')
        self.assertEquals(resolve(url).func, views.game)

    def test_registration_make_new_card_url_is_resolved(self):
        url = reverse('registration:make-new-card')
        self.assertEquals(resolve(url).func, views.make_new_card)

    def test_registration_card_check_url_is_resolved(self):
        url = reverse('registration:card-check')
        self.assertEquals(resolve(url).func, views.card_check)

    def test_registration_success_url_is_resolved(self):
        url = reverse('registration:success')
        self.assertEquals(resolve(url).func, views.success)

    def test_registration_info_url_is_resolved(self):
        url = reverse('registration:info')
        self.assertEquals(resolve(url).func, views.info)

    def test_registration_add_friend_url_is_resolved(self):
        url = reverse('registration:add-friend')
        self.assertEquals(resolve(url).func, views.add_friend)

    def test_registration_inbox_url_is_resolved(self):
        url = reverse('registration:inbox')
        self.assertEquals(resolve(url).func, views.inbox)

    def test_registration_view_message_url_is_resolved(self):
        m = Message(id=1)
        m.save()
        url = reverse('registration:view-message', args=[m.id])
        self.assertEquals(resolve(url).func, views.view_message)

    def test_registration_delete_message_url_is_resolved(self):
        m = Message(id=2)
        m.save()
        url = reverse('registration:delete-message', args=[m.id])
        self.assertEquals(resolve(url).func, views.delete_message)

    def test_registration_new_message_url_is_resolved(self):
        url = reverse('registration:new-message')
        self.assertEquals(resolve(url).func, views.new_message)

    def test_registration_new_message_with_arg_url_is_resolved(self):
        url = reverse('registration:new-message', args=['reply'])
        self.assertEquals(resolve(url).func, views.new_message)

    def test_registration_active_games_url_is_resolved(self):
        url = reverse('registration:active-games')
        self.assertEquals(resolve(url).func, views.active_games)

    def test_registration_exit_url_is_resolved(self):
        url = reverse('registration:exit')
        self.assertEquals(resolve(url).func, views.exit_game)

    def test_registration_send_game_url_is_resolved(self):
        url = reverse('registration:send-game')
        self.assertEquals(resolve(url).func, views.send_game)

    def test_registration_total_time_son_url_is_resolved(self):
        url = reverse('registration:total-time-son')
        self.assertEquals(resolve(url).func, views.total_time_son)

    def test_registration_reports_menu_url_is_resolved(self):
        url = reverse('registration:reports-menu')
        self.assertEquals(resolve(url).func, views.reports_menu)

    def test_registration_details_of_users_url_is_resolved(self):
        url = reverse('registration:details-of-users')
        self.assertEquals(resolve(url).func, views.reports_users)

    def test_registration_avg_points_url_is_resolved(self):
        url = reverse('registration:avg-points')
        self.assertEquals(resolve(url).func, views.avg_points)

    def test_registration_rank_game_url_is_resolved(self):
        url = reverse('registration:rank-game')
        self.assertEquals(resolve(url).func, views.rank_game)

    def test_registration_rank_success_url_is_resolved(self):
        url = reverse('registration:rank-success')
        self.assertEquals(resolve(url).func, views.rank_success)