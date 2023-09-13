from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

from imdb_api.models.movie_model import Movie

class TestMovieVote(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            vote_average=0.0,  # Initial average vote
            vote_count=0  # Initial vote count
        )

    def test_movie_vote(self):
        print("Running test_movie_vote...")
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Check initial movie vote count and average
        self.assertEqual(self.movie.vote_count, 0)
        self.assertEqual(self.movie.vote_average, 0.0)

        # Vote for the movie with a rating of 8.0
        response = self.client.post(reverse('imdb:vote_for_movie', args=(self.movie.id,)), {'rating': 8.0})

        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

        # Check that the vote was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

        # Refresh the movie object to get the updated values from the database
        self.movie.refresh_from_db()

        # Check updated movie vote count and average
        print("Updated vote count:", self.movie.vote_count)
        print("Updated vote average:", self.movie.vote_average)

        self.assertEqual(self.movie.vote_count, 1)
        self.assertEqual(self.movie.vote_average, Decimal('8.0'))

    def test_invalid_movie_vote(self):
        print("Running test_invalid_movie_vote...")
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Try to vote with an invalid rating (outside the allowed range)
        response = self.client.post(reverse('imdb:vote_for_movie', args=(self.movie.id,)), {'rating': 11.0})

        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

        # Check that the vote failed
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

        # Refresh the movie object to ensure it wasn't updated
        self.movie.refresh_from_db()

        # Check that vote count and average remain the same
        print("Updated vote count:", self.movie.vote_count)
        print("Updated vote average:", self.movie.vote_average)

        self.assertEqual(self.movie.vote_count, 0)
        self.assertEqual(self.movie.vote_average, 0.0)
