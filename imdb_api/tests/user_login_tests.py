from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('imdb:login')
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_view_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertContains(response, "Hello, Login to watch")
        
