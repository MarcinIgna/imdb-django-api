from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from imdb_api.models.movie_model import Movie
from imdb_api.models.genre_model import Genre
from imdb_api.forms.movie_form import MovieForm

class UpdateMovieViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='testpass', is_staff=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='testpass')
        self.genre = Genre.objects.create(name='Test Genre', tmdb_id=123)
        self.movie = Movie.objects.create(
            tmdb_id=123,
            title='Test Movie',
            overview='Test Overview',
            release_date='2022-01-01',
            poster_path='/test/poster.jpg',
            backdrop_path='/test/backdrop.jpg',
            original_language='en',
            original_title='Test Movie',
            popularity=7.5,
            vote_average=8.0,
            vote_count=100,
            adult=False,
            video=False,
        )
        self.movie.genres.set([self.genre])

    def test_update_movie_view_with_valid_data(self):
        self.client.login(username='staffuser', password='testpass')
        form_data = {
            'tmdb_id': 123,
            'title': 'Updated Test Movie',
            'overview': 'Updated Test Overview',
            'release_date': '2022-01-01',
            'poster_path': '/test/poster.jpg',
            'backdrop_path': '/test/backdrop.jpg',
            'original_language': 'en',
            'original_title': 'Updated Test Movie',
            'popularity': 7.5,
            'vote_average': 8.0,
            'vote_count': 100,
            'adult': False,
            'video': False,
            'genres': [self.genre.id],
        }
        response = self.client.post(reverse('imdb:update_movie', args=[self.movie.id]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('imdb:see_all_movies'))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Updated Test Movie')
        self.assertEqual(self.movie.overview, 'Updated Test Overview')
        self.assertEqual(self.movie.original_title, 'Updated Test Movie')
        self.assertEqual(self.movie.genres.count(), 1)
        self.assertEqual(self.movie.genres.first(), self.genre)

    def test_update_movie_view_with_invalid_data(self):
        self.client.login(username='staffuser', password='testpass')
        form_data = {
            'tmdb_id': 123,
            'title': '',
            'overview': 'Updated Test Overview',
            'release_date': '2022-01-01',
            'poster_path': '/test/poster.jpg',
            'backdrop_path': '/test/backdrop.jpg',
            'original_language': 'en',
            'original_title': 'Updated Test Movie',
            'popularity': 7.5,
            'vote_average': 8.0,
            'vote_count': 100,
            'adult': False,
            'video': False,
            'genres': [self.genre.id],
        }
        response = self.client.post(reverse('imdb:update_movie', args=[self.movie.id]), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.movie.refresh_from_db()
        self.assertNotEqual(self.movie.title, '')
        self.assertNotEqual(self.movie.overview, 'Updated Test Overview')
        self.assertNotEqual(self.movie.original_title, '')
        self.assertEqual(self.movie.genres.count(), 1)
        self.assertEqual(self.movie.genres.first(), self.genre)
    def test_update_movie_view_with_superuser(self):
        self.client.login(username='superuser', password='testpass')
        response = self.client.get(reverse('imdb:update_movie', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], MovieForm)
        self.assertEqual(response.context['movie'], self.movie)