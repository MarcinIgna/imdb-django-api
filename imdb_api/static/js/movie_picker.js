// JavaScript to handle modal data
$(document).ready(function () {
    $('.btn-primary').on('click', function () {
        var movieTitle = $(this).data('movie-title');
        var movieOverview = $(this).data('movie-overview');

        // Set the data attributes within the modal
        $('#movieDetailsModal').find('.modal-title').text(movieTitle);
        $('#movieDetailsModal').find('.modal-body p').text(movieOverview);
    });
});
