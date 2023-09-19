import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Avg, Count

from imdb_api.models.user_vote_model import MovieVote

if not nltk.data.find('corpora/stopwords'):
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

def calculate_tfidf_matrix(movie_overviews):
    # Preprocess the movie overviews
    preprocessed_overviews = [preprocess_text(overview) for overview in movie_overviews]

    # Add a print statement to check the preprocessed overviews
    # print("Preprocessed Overviews:")
    # for i, overview in enumerate(preprocessed_overviews):
    #     print(f"{i + 1}: {overview}")

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the preprocessed movie overviews to calculate TF-IDF scores
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_overviews)

    # Add print statements to check vocabulary size and feature names
    # print("Vocabulary Size:", len(tfidf_vectorizer.vocabulary_))
    # print("Feature Names:", tfidf_vectorizer.get_feature_names_out())

    # Calculate cosine similarity between TF-IDF vectors
    similarities = cosine_similarity(tfidf_matrix)

    return similarities




def update_movie_vote_average(movie):
    # Calculate the new vote_average and vote_count for the movie
    movie_data = MovieVote.objects.filter(movie=movie).aggregate(Avg('rating'), Count('rating'))
    movie.vote_average = movie_data['rating__avg'] or 0.0
    movie.vote_count = movie_data['rating__count']
    movie.save()
