import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Avg, Count
import numpy as np

from imdb_api.models.user_vote_model import MovieVote


nltk.download('stopwords')

# Function to preprocess text
def preprocess_text(text):
    # Tokenize the text
    tokens = text.lower().split()  # Convert to lowercase and split by whitespace

    # Remove stopwords using NLTK's list of English stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Join the filtered tokens back into a string
    preprocessed_text = ' '.join(filtered_tokens)

    return preprocessed_text

def calculate_tfidf_matrix(movie_overviews, movie_genres):
    # Preprocess the movie overviews
    preprocessed_overviews = [preprocess_text(overview) for overview in movie_overviews]

    # Create a TF-IDF vectorizer for the movie overviews
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_overviews = tfidf_vectorizer.fit_transform(preprocessed_overviews)

    # Create a TF-IDF vectorizer for the movie genres
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_genres = tfidf_vectorizer.fit_transform(movie_genres)

    # Combine the TF-IDF matrices for the movie overviews and genres
    tfidf_matrix = np.hstack((tfidf_matrix_overviews.toarray(), tfidf_matrix_genres.toarray()))

    # Calculate cosine similarity between TF-IDF vectors
    similarities = cosine_similarity(tfidf_matrix)

    return similarities




def update_movie_vote_average(movie):
    # Calculate the new vote_average and vote_count for the movie
    movie_data = MovieVote.objects.filter(movie=movie).aggregate(Avg('rating'), Count('rating'))
    movie.vote_average = movie_data['rating__avg'] or 0.0
    movie.vote_count = movie_data['rating__count']
    movie.save()
