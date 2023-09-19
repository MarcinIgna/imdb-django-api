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

    # Extract overviews from favorite movies
    favorite_movie_overviews = [movie.overview for movie in favorite_movies]

    # Calculate TF-IDF matrix and similarities
    similarities = calculate_tfidf_matrix(favorite_movie_overviews)

    # Exclude the user's favorite movies from the recommendations
    non_favorite_recommended_movies = Movie.objects.exclude(id__in=favorite_movie_ids)

    # Limit the number of recommendations to the specified value
    num_recommendations = min(num_recommendations, non_favorite_recommended_movies.count())
    recommended_movies = non_favorite_recommended_movies[:num_recommendations]

    return recommended_movies


# from imdb_api.models.user_favorite_model import UserFavorite
# from imdb_api.models.movie_model import Movie
# from .utils import calculate_tfidf_matrix

# from imdb_api.models import Movie  # Import the Movie model

# def get_user_movie_recommendations(user, num_recommendations=10):
#     # Get the user's favorite movie IDs using the UserFavorite model
#     favorite_movie_ids = UserFavorite.objects.filter(user=user).values_list('movie', flat=True)
#     # print("Favorite Movie IDs:", favorite_movie_ids)  # Print the favorite movie IDs for debugging
#     # Fetch the actual Movie objects based on the IDs
#     favorite_movies = Movie.objects.filter(id__in=favorite_movie_ids)

#     # print("Favorite Movies:", favorite_movies)  # Print the favorite movies for debugging

#     # Extract overviews from favorite movies
#     favorite_movie_overviews = [movie.overview for movie in favorite_movies]

#     # print("Favorite Movie Overviews:")
#     # for i, overview in enumerate(favorite_movie_overviews):
#     #     print(f"{i + 1}: {overview}")
    
#     # Calculate TF-IDF matrix and similarities
#     # print("Calculating TF-IDF matrix and similarities...")
#     similarities = calculate_tfidf_matrix(favorite_movie_overviews)

#     # Get recommended movie indices based on similarity
#     recommended_movie_indices = list(range(len(favorite_movies)))  # Just use indices 0 to n-1

#     # Filter out indices that are out of range
#     recommended_movie_indices = [idx for idx in recommended_movie_indices if idx < len(favorite_movies)]

#     # Get the recommended movies from the indices
#     recommended_movies = [favorite_movies[idx] for idx in recommended_movie_indices]
#     # print("Recommended Movies:")
#     # for i, movie in enumerate(recommended_movies):
#     #     print(f"{i + 1}: {movie.title}")

#     # Check if each recommended movie has the same TMDB ID as a favorite movie
    
#     # print("Checking for TMDB ID matches...")
#     # for recommended_movie in recommended_movies:
#     #     for favorite_movie in favorite_movies:
#     #         if recommended_movie.tmdb_id == favorite_movie.tmdb_id:
#     #             print(f"Match found between {recommended_movie.title} and {favorite_movie.title}")
#     #             # You can perform actions here if a match is found
#     #             break
    
#     # Exclude the user's favorite movies from the recommendations
#     non_favorite_recommended_movies = Movie.objects.exclude(id__in=favorite_movie_ids)
    
#     # Limit the number of recommendations to the specified value
#     num_recommendations = min(num_recommendations, non_favorite_recommended_movies.count())
#     recommended_movies = non_favorite_recommended_movies[:num_recommendations]
    
#     # print("Non-favorite Recommended Movies:")
#     # for i, movie in enumerate(recommended_movies):
#     #     print(f"{i + 1}: {movie.title}")
    
#     return recommended_movies
