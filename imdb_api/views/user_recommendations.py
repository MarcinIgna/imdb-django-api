from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from imdb_api.recommendations import get_user_movie_recommendations


@login_required
def user_recommendations(request):
    """
    This view displays a list of movie recommendations for the logged-in user.
    """

    # Get movie recommendations for the logged-in user
    recommendations = get_user_movie_recommendations(request.user)

    # Check if there are no recommendations
    if not recommendations:
        message = "Sorry, we couldn't find any movie recommendations for you. Please add some movies to your favorites."
        return render(request, 'core/user_recommendations.html', {'message': message})

    return render(request, 'core/user_recommendations.html', {'recommendations': recommendations})