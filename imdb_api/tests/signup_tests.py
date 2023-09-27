from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('imdb:signup')
        self.login_url = reverse('imdb:login')
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpass123'

    def test_signup_view(self):
        # Submit a valid form
        response = self.client.post(self.signup_url, {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        })

        # Check if the user is created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, self.login_url, status_code=302, target_status_code=200)