from django.shortcuts import render
from imdb_api.recommendations import get_user_movie_recommendations

def user_recommendations(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        # Handle when the user is not authenticated (redirect or show a message)
        return render(request, 'not_authenticated.html')

    # Get movie recommendations for the logged-in user
    recommendations = get_user_movie_recommendations(request.user)

    return render(request, 'core/user_recommendations.html', {'recommendations': recommendations})
