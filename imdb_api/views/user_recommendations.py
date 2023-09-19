from django.shortcuts import render
from imdb_api.recommendations import get_user_movie_recommendations

def user_recommendations(request):
    print("User Recommendations View")
    # Check if the user is logged in
    if not request.user.is_authenticated:
        # Handle when the user is not authenticated (redirect or show a message)
        return render(request, 'not_authenticated.html')

    # Get movie recommendations for the logged-in user
    recommendations = get_user_movie_recommendations(request.user)

    # Check if there are no recommendations
    if not recommendations:
        message = "Sorry, we couldn't find any movie recommendations for you. Please add some movies to your favorites."
        return render(request, 'core/user_recommendations.html', {'message': message})

    return render(request, 'core/user_recommendations.html', {'recommendations': recommendations})