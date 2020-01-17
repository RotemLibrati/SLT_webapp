from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve

from .views import logout
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
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='qwerty246')

    def test_with_student_login(self):
        # self.profile.type = 'student'
        # self.profile.save()
        response = self.client.get(reverse('registration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Language Teacher")
        self.assertContains(response, "Main menu")
        self.assertContains(response, 'Play the game')
        self.assertContains(response, 'Profile menu')
        self.assertContains(response, 'Manage friends')
        self.assertContains(response, 'Mail')
        self.assertContains(response, 'Make a new card')
        self.assertContains(response, 'Rank game')
        self.assertTemplateUsed(response, 'registration/index.html')

    def test_with_admin_login(self):
        u1 = User(username='testuser1')
        u1.set_password('qwerty246')
        u1.save()
        up = UserProfile(user=u1, is_admin=True)
        up.save()
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.get(reverse('registration:index'))
        # print(response.context['profile'].is_admin)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mail')
        # self.assertContains(response, "Reports Menu")

    def test_with_parent_login(self):
        self.profile.type = 'parent'
        self.profile.save()
        # self.client.login(username='testuser', password='qwerty246')
        response = self.client.get(reverse('registration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Language Teacher")
        self.assertContains(response, "Main menu")
        self.assertContains(response, 'Play the game')
        self.assertContains(response, 'Profile menu')
        self.assertContains(response, 'Manage friends')
        self.assertContains(response, 'Mail')
        self.assertContains(response, 'Report total time of son')
        self.assertContains(response, 'Rank game')

    def test_without_login(self):
        self.client.logout()
        response = self.client.get(reverse("registration:index"))
        self.assertContains(response, 'Login with existing user')
        self.assertContains(response, 'Make a new user')


class TestInfoView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()

    def test_with_login(self):
        self.client.login(username='testuser', password='qwerty246')
        response = self.client.get(reverse('registration:info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "THE RULES FOR PLAYING \"MEMORY\"")
        self.assertTemplateUsed(response, 'registration/info.html')

    def test_with_logout(self):
        self.client.login(username='testuser', password='qwerty246')
        self.client.logout()
        response = self.client.get(reverse('registration:info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "THE RULES FOR PLAYING \"MEMORY\"")


class TestLoginView(TestCase):
    def setUp(self):
        self.credentials = {
            'user_name': 'testuser',
            'password': 'qwerty246'}
        self.user = User.objects.create_user(username=self.credentials['user_name'], password=self.credentials['password'])
        self.user.save()
        self.profile = UserProfile(user=self.user)
        self.profile.save()
        self.client = Client()

    def test_template_content(self):
        self.client.logout()
        response = self.client.get(reverse('registration:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login(self):
        self.client.logout()
        response = self.client.post(reverse('registration:login'), data=self.credentials, follow=True)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse('registration:profile'))


class TestInboxView(TestCase):

    def test_without_login(self):
        c = Client()
        response = c.get(reverse('registration:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not logged in")

    def test_with_no_messages(self):
        c = Client()
        user = User.objects.create_user(username='tester', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('registration:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 0)
        self.assertEquals(len(response.context['messages_sent']), 0)

    def test_with_message_received(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user)
        response = c.get(reverse('registration:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 1)
        self.assertEquals(len(response.context['messages_sent']), 0)

    def test_with_message_sent(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user2)
        response = c.get(reverse('registration:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 0)
        self.assertEquals(len(response.context['messages_sent']), 1)


class TestViewMessage(TestCase):

    def test_message_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user2)
        response = c.get(reverse('registration:view-message', args=[message.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/message.html')
        self.assertContains(response, 'hello')

    def test_message_does_not_exist(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('registration:view-message', args=[3]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/failure.html')
        self.assertContains(response, 'Message getting failed')


class TestDeleteMessage(TestCase):

    def test_delete(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user)
        response = c.get(reverse('registration:delete-message', args=[message.id]))
        self.assertRedirects(response, reverse('registration:inbox'))
        response = c.get(reverse('registration:inbox'))
        self.assertEquals(len(response.context['messages_received']), 0)
        self.assertEquals(len(response.context['messages_sent']), 0)


class TestNewMessage(TestCase):

    def test_new_message_template_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('registration:new-message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/new-message.html')
        self.assertContains(response, 'New message')

    def test_message_post(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = {'receiver': user, 'subject': 'subject', 'body': 'body'}
        c.force_login(user2)
        response = c.post(reverse('registration:new-message'), data=message)
        self.assertRedirects(response, reverse('registration:inbox'))
        m = Message.objects.get(receiver=user, sender=user2)
        self.assertIsNotNone(m)


class TestProfile(TestCase):

    def test_template_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('registration:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/details.html')
        self.assertContains(response, 'Profile menu')

    def test_without_login(self):
        c = Client()
        response = c.get(reverse('registration:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not logged in')


class TestAddFriend(TestCase):

    def test_template_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        c.force_login(user)
        response = c.get(reverse('registration:add-friend'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/add-friend.html')
        self.assertContains(response, 'Friend addition menu')

    def test_post_add_friend(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        c.force_login(user)
        data = {'new_friend': str(user2.username), 'action': 'Add'}
        response = c.post(reverse('registration:add-friend'), data=data)
        self.assertRedirects(response, reverse('registration:index'))
        response = c.get(reverse('registration:profile'))
        self.assertContains(response, f'{str(user2.username)}')

    def test_remove_friend(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        c.force_login(user)
        data = {'new_friend': str(user2.username), 'action': 'Remove'}
        response = c.post(reverse('registration:add-friend'), data=data)
        self.assertRedirects(response, reverse('registration:index'))
        response = c.post(reverse('registration:add-friend'), data=data)
        self.assertRedirects(response, reverse('registration:index'))
        response = c.get(reverse('registration:profile'))
        self.assertNotContains(response, f'{str(user2.username)}')


class TestGame(TestCase):

    def test_template_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('registration:game'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/game.html')
        self.assertContains(response, 'Exit game')


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
