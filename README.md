# MoviePMB

![Front page](front_site.png)

## Features

- Django-based user friendly project for accessing data.
- Our MoviePMB Django project retrieves and updates movie data from [The Movie Database (TMDb) API](https://developer.themoviedb.org/reference/intro/getting-started). This third-party integration allows us to keep our database up-to-date with the latest movie information.
- Multi-role authentication:
  - Admins: Full access to CRUD operations.
  - Registered Users: Access to read IMDb data.
  - Authenticated Users: 
    - Can create thier own favorite movie list and later get personal recommendation.
    - Can rate movies (html in progress).
    - Can comment movies (html in progress).
  - Anonymous Users: Limited access.
- Search functionality for finding movies by title.
- Testing.
- Security:
    - Authentication and authorization checks (registration by Google account in progress, also "Forgot Password?" in progress).
    - Protection against common web vulnerabilities.
- Swagger documentation for API endpoints.
- PostgreSQL database for efficient data storage(We used [Render](https://render.com/)).
- Cloud deployment for scalability and accessibility(We used [Amazon Web Services (AWS)](https://aws.amazon.com/)).
- Bootstrap 5 for responsive design.
- Newsletter (in progress)
- Filtering by Genre

### Movie Recommendation Algorithm

Our project includes a powerful recommendation algorithm that suggests movies to users based on their preferences, movie descriptions and genres. This algorithm analyzes the descriptions of movies you've interacted with and identifies similar movies that you might enjoy.

#### How It Works

1. **User Interaction Tracking**: The algorithm keeps track of the movies you've rated, liked, or interacted with in any way.

2. **Description Analysis**: It analyzes the descriptions and genres of these movies, extracting key features and keywords.

3. **Similarity Calculation**: Using advanced natural language processing (NLP) techniques, the algorithm calculates(TF-IDF) the similarity between movie descriptions.

4. **Recommendation Generation**: Based on the calculated similarities, the algorithm generates a list of movie recommendations that match your preferences and interests.

5. **Personalized Experience**: The more you interact with movies on our platform, the more personalized and accurate your recommendations become.

#### TF-IDF Vectorization:

**Term Frequency (TF):**
- Term Frequency measures how often a term (word) appears in a document. It's calculated as the ratio of the number of times a term appears in a document to the total number of terms in that document.
  $$\text{TF}(t, d) = \frac{\text{Number of times term \(t\) appears in document \(d\)}}{\text{Total number of terms in document \(d\)}}$$

**Inverse Document Frequency (IDF):**
- Inverse Document Frequency measures the importance of a term across a collection of documents. It's calculated as the logarithm of the ratio of the total number of documents to the number of documents containing the term, adjusted to prevent division by zero.
  $$\text{IDF}(t, D) = \log\left(\frac{\text{Total number of documents in corpus \(D\)}}{\text{Number of documents containing term \(t\) in corpus \(D\)} + 1}\right)$$
  - The addition of 1 in the denominator is to avoid division by zero.

**TF-IDF:**
- The TF-IDF score for a term in a document is the product of its Term Frequency and Inverse Document Frequency.
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

**Importance (Normalization):**
- The TF-IDF scores are then often normalized to ensure that the values fall within a specific range, typically between 0 and 1. This normalization can involve dividing each TF-IDF score by the Euclidean norm of the entire vector.
  $$\text{Normalized TF-IDF}(t, d, D) = \frac{\text{TF-IDF}(t, d, D)}{\sqrt{\sum_{i} (\text{TF-IDF}(t_i, d, D))^2}}$$

In the context of your algorithm, the TF-IDF values are normalized to a scale between 0 and 1, representing the importance of each term in the movie descriptions relative to the entire dataset. Higher values indicate higher importance. This is a crucial step in capturing the significance of words in a document for similarity calculations, such as cosine similarity.

#### Enhancing Your Movie Discovery

Our recommendation algorithm is designed to enhance your movie discovery experience. It helps you discover hidden gems and movies that align with your taste, making your time on our platform more enjoyable and tailored to your interests.


## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/MarcinIgna/imdb-django-api.git
   ```

2. Create a virtual environment (recommended) to isolate project dependencies:

   ```shell
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:

     ```shell
     source venv/bin/activate
     ```

   - On Windows (PowerShell):

     ```shell
     .\venv\Scripts\Activate
     ```

4. Install project dependencies from the `requirements.txt` file:

   ```shell
   pip install -r requirements.txt
   ```

## Database Setup

1. Create the database schema by running migrations:

   ```shell
   python manage.py makemigrations
   ```

   ```shell
   python manage.py migrate
   ```

## Running Custom Scripts
- To edit numbers for populating check files add_movies.py/add_person.py in management/commands folder.
- To run custom management scripts for populating your database with data, use the following command:

```shell
python manage.py run_custom_scripts
```


## Usage

1. Start the Django development server:

   ```shell
   python manage.py runserver
   ```

2. Open your web browser and navigate to [http://localhost:8000](http://localhost:8000) to access your Django project.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request to the original repository.

## License
Free to use
