$(document).ready(function() {
    // Handle the favorite button click event
    $('.btn-group button').click(function() {
      var movieId = $(this).data('movie-id');
      var isFavorite = $(this).data('is-favorite');
  
      // Send an AJAX request to the server to toggle the favorite status of the movie
      $.ajax({
        url: '/movies/toggle_favorite/',
        method: 'POST',
        data: {
          'movie_id': movieId,
          'is_favorite': !isFavorite
        },
        success: function(response) {
          // Update the button state based on the server response
          if (response.is_favorite) {
            $('.btn-group button').addClass('active');
          } else {
            $('.btn-group button').removeClass('active');
          }
          $('.btn-group button').data('is-favorite', response.is_favorite);
          $('.btn-group button').attr('aria-pressed', response.is_favorite);
        },
        error: function(xhr, status, error) {
          console.log('Error:', error);
        }
      });
    });
  });