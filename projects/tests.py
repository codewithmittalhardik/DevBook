from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileEditViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='oldname',
            email='user@example.com',
            password='secret123',
        )
        self.client.force_login(self.user)

    def test_user_can_change_username_from_profile_page(self):
        response = self.client.post(reverse('profile_edit'), {
            'username': 'newname',
            'bio': 'Updated bio',
            'linkedin_url': 'https://linkedin.com/in/newname',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newname')
