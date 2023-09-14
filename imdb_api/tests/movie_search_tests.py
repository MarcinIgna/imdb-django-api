from django.test import TestCase
from django.urls import reverse
from imdb_api.models.movie_model import Movie

class MovieSearchTestCase(TestCase):
    def setUp(self):
        # Create some movie entries for testing
        Movie.objects.create(title="Princess Mononoke")
        Movie.objects.create(title="The Princess Diaries")
        Movie.objects.create(title="Cinderella")

    def test_search_exact_case(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'Princess Mononoke'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Princess Mononoke")

    def test_search_lowercase(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'princess mononoke'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Princess Mononoke")

    def test_search_mixed_case(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'PrInCeSs MoNoNoKe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Princess Mononoke")

    def test_search_partial_title(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'Prin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Princess Mononoke")
        self.assertContains(response, "The Princess Diaries")

    def test_search_no_results(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'Nonexistent Movie'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies found")

    def test_empty_search(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies found")

    def test_multiple_results(self):
        response = self.client.get(reverse('imdb:movie_search'), {'query': 'Princess'})
        self.assertEqual(response.status_code, 200)
        # Modify this assertion to check for titles in 'results'
        self.assertContains(response, "Princess Mononoke")
        self.assertContains(response, "The Princess Diaries")
