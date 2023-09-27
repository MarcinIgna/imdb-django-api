from django.test import TestCase
from imdb_api.models.movie_model import Movie
from imdb_api.forms.movie_form import MovieForm
from imdb_api.models.genre_model import Genre

class MovieFormTestCase(TestCase):
    def test_movie_form_valid(self):
        genre = Genre.objects.create(name='Test Genre', tmdb_id=123)
        form_data = {
            'tmdb_id': 123,
            'title': 'Test Movie',
            'overview': 'Test Overview',
            'release_date': '2022-01-01',
            'poster_path': '/test/poster.jpg',
            'backdrop_path': '/test/backdrop.jpg',
            'original_language': 'en',
            'original_title': 'Test Movie',
            'popularity': 7.5,
            'vote_average': 8.0,
            'vote_count': 100,
            'adult': False,
            'video': False,
            'genres': [genre.id],
        }
        form = MovieForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form is not valid: {form.errors.as_data()}")
        movie = form.save()
        self.assertEqual(movie.tmdb_id, 123, f"Movie tmdb_id is not correct: {movie.tmdb_id}")
        self.assertEqual(movie.title, 'Test Movie', f"Movie title is not correct: {movie.title}")
        self.assertEqual(movie.overview, 'Test Overview', f"Movie overview is not correct: {movie.overview}")
        self.assertEqual(str(movie.release_date), '2022-01-01', f"Movie release date is not correct: {movie.release_date}")
        self.assertEqual(movie.poster_path, '/test/poster.jpg', f"Movie poster path is not correct: {movie.poster_path}")
        self.assertEqual(movie.backdrop_path, '/test/backdrop.jpg', f"Movie backdrop path is not correct: {movie.backdrop_path}")
        self.assertEqual(movie.original_language, 'en', f"Movie original language is not correct: {movie.original_language}")
        self.assertEqual(movie.original_title, 'Test Movie', f"Movie original title is not correct: {movie.original_title}")
        self.assertEqual(movie.popularity, 7.5, f"Movie popularity is not correct: {movie.popularity}")
        self.assertEqual(movie.vote_average, 8.0, f"Movie vote average is not correct: {movie.vote_average}")
        self.assertEqual(movie.genres.count(), 1, f"Movie genres count is not correct: {movie.genres.count()}")
        self.assertEqual(movie.genres.first(), genre, f"Movie genre is not correct: {movie.genres.first()}")