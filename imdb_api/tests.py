from .models.user_model import CustomUser
from django.test import TestCase, Client
from django.urls import reverse


# class CustomUserTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpass'
#         )

#     def test_user_creation(self):
#         self.assertEqual(self.user.username, 'testuser')
#         self.assertEqual(self.user.email, 'testuser@example.com')
#         self.assertTrue(self.user.is_active)
#         self.assertFalse(self.user.is_staff)
#         self.assertTrue(self.user.check_password('testpass'))
        
        
        


