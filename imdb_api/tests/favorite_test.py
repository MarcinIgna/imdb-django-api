from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User

from imdb_api.models.movie_model import Movie
from imdb_api.models.user_favorite_model import UserFavorite

class ToggleFavoriteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.movie = Movie.objects.create(title='Test Movie', overview='Test Overview', release_date='2022-01-01')
        self.url = reverse('imdb:toggle_favorite', args=[self.movie.id])

    def test_toggle_favorite_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "is_favorite": True})
        self.assertTrue(UserFavorite.objects.filter(user=self.user, movie=self.movie).exists())

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "is_favorite": False})
        self.assertFalse(UserFavorite.objects.filter(user=self.user, movie=self.movie).exists())

