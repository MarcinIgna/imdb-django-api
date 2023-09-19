from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from imdb_api.forms.SignUp_form import SignUpForm
from imdb_api.forms.login_form import LoginForm


class SignUpViewTestCase(TestCase):
    def test_signup_success(self):
        # Simulate a successful signup POST request
        response = self.client.post(reverse('imdb:signup'), {'username': 'testuser', 'password1': 'testpass123', 'password2': 'testpass123'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect status code

    def test_signup_invalid_data(self):
        # Simulate a signup POST request with invalid data
        response = self.client.post(reverse('imdb:signup'), {'username': '', 'password1': '', 'password2': ''})
        self.assertEqual(response.status_code, 200)  # Expect a response with status code 200 (form re-rendered)

class LoginViewTestCase(TestCase):
    def setUp(self):
        # Create a test user for login testing
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_success(self):
        # Simulate a successful login POST request
        response = self.client.post(reverse('imdb:login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect status code

    def test_login_invalid_credentials(self):
        # Simulate a login POST request with invalid credentials
        response = self.client.post(reverse('imdb:login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Expect a response with status code 200 (form re-rendered)

class LogoutViewTestCase(TestCase):
    def test_logout(self):
        # Simulate a logout GET request
        response = self.client.get(reverse('imdb:logout'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect status code

