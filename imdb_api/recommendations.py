from imdb_api.models.user_favorite_model import UserFavorite
from imdb_api.models.movie_model import Movie
from .utils import calculate_tfidf_matrix

def get_user_movie_recommendations(user, num_recommendations=10):
    # Get the user's favorite movie IDs using the UserFavorite model
    favorite_movie_ids = UserFavorite.objects.filter(user=user).values_list('movie', flat=True)

    # Check if the user has any favorite movies
    if not favorite_movie_ids:
        return []

    # Fetch the actual Movie objects based on the IDs
    favorite_movies = Movie.objects.filter(id__in=favorite_movie_ids)

    # Extract overviews and genres from favorite movies
    favorite_movie_overviews = [movie.overview for movie in favorite_movies]
    favorite_movie_genres = [' '.join(list(movie.genres.values_list('name', flat=True))) for movie in favorite_movies]

    # Print the movie names and genres
    # for movie, genres in zip(favorite_movies, favorite_movie_genres):
    #     print(f"{movie.title}: {genres}")

    # Calculate TF-IDF matrix and similarities
    similarities = calculate_tfidf_matrix(favorite_movie_overviews, favorite_movie_genres)
    print(similarities)
    # Exclude the user's favorite movies from the recommendations
    non_favorite_recommended_movies = Movie.objects.exclude(id__in=favorite_movie_ids)

    # Limit the number of recommendations to the specified value
    num_recommendations = min(num_recommendations, non_favorite_recommended_movies.count())

    return non_favorite_recommended_movies[:num_recommendations]