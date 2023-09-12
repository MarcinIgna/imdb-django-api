from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from imdb_api.recommendations import get_user_movie_recommendations

class Command(BaseCommand):
    help = "Recommend movies to users based on their favorites"

    def handle(self, *args, **options):
        # Specify the number of recommendations per user
        num_recommendations = 10

        # Get all users who have favorited movies
        users_with_favorites = User.objects.filter(userfavorite__isnull=False).distinct()

        for user in users_with_favorites:
            # Get movie recommendations for the user
            recommendations = get_user_movie_recommendations(user, num_recommendations)

            # Display recommendations
            self.stdout.write(f"Recommendations for user '{user.username}':")
            for movie_id in recommendations:
                self.stdout.write(f"- Movie ID: {movie_id}")

