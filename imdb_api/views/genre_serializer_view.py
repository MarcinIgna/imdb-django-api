from rest_framework.views import APIView
from rest_framework.response import Response
from imdb_api.models.genre_model import Genre
from imdb_api.serializers.genre_serializer import GenreSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class GenresView(APIView):
    """
    This class is used to get,add, edit and delete genres.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        else:
            genres = Genre.objects.all()
            serializer = GenreSerializer(genres, many=True)
            return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            serializer = GenreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("You are not authorized to add a genre")

    def put(self, request, pk):
        if request.user.is_authenticated and request.user.is_staff:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("You are not authorized to update a genre")

    def delete(self, request, pk):
        if request.user.is_authenticated and request.user.is_staff:
            genre = Genre.objects.get(pk=pk)
            genre.delete()
            return Response("Genre Deleted")
        else:
            return Response("You are not authorized to delete a genre")
