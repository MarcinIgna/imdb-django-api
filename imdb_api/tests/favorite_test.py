from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from imdb_api.models.movie_model import Movie
from imdb_api.models.user_favorite_model import UserFavorite
from django.http import JsonResponse

class ToggleFavoriteTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test movie
        self.movie = Movie.objects.create(title="Test Movie")

        # Create a test favorite entry for the user and movie
        UserFavorite.objects.create(user=self.user, movie=self.movie)

    def test_toggle_favorite_authenticated(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Toggle favorite for the movie
        response = self.client.post(reverse('imdb:toggle_favorite', args=[self.movie.pk]))

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['is_favorite'], False)  # Initial favorite status was True, so it should be False after toggling

    def test_toggle_favorite_unauthenticated(self):
        # Logout the user
        self.client.logout()

        # Toggle favorite for the movie
        response = self.client.post(reverse('imdb:toggle_favorite', args=[self.movie.pk]))

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])  # The user is not authenticated, so success should be False
        self.assertEqual(data['message'], "User not authenticated")  # The message should indicate user not authenticated
