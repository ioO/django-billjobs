from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from billjobs.models import UserProfile


class SignupAndSlack(TestCase):
    ''' Test signup when project owner doesn't define slack settings '''

    def test_slack_invitation(self):
        ''' Test signup and slack invitation '''
        data = {
                'username': 'noslack',
                'password': 'motdepasse',
                'first_name': 'Bill',
                'last_name': 'Jobs',
                'email': 'billjobs_noslack@yopmail.com',
                'billing_address': 'une adresse'
                }
        response = self.client.post(
                reverse('billjobs_signup'), data, follow=True)
        self.assertRedirects(
                response,
                reverse('billjobs_signup_success'),
                status_code=302,
                target_status_code=200
                )

        user = User.objects.get(username = 'noslack')
        self.assertEqual(user.check_password('motdepasse'), True)

        profile = user.userprofile
        self.assertEqual(profile.billing_address, 'une adresse')
