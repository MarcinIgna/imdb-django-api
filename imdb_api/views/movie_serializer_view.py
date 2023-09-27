from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from imdb_api.models.movie_model import Movie
from imdb_api.serializers.movie_serializer import MovieSerializer


class MovieView(APIView):
    """
    This class is used to get,add, edit and delete movies.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        
        elif pk is None:
            print(request.user.username)
            movie = Movie.objects.all()
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        else:
            return Response("Movie not found")
    
    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            
            return Response("You are not authorized to add movie")
    def put(self, request, pk):
        if request.user.is_authenticated and request.user.is_staff:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
            
        else:
            return Response("You are not authorized to update movie")
    def delete(self, request,pk):
        if request.user.is_authenticated and request.user.is_staff:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response("Movie Deleted")
        else:
            return Response("You are not authorized to delete movie")