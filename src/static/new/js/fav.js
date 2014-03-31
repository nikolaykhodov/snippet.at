/*
 * Класс faved означает, что сниппет добавлен в избранное
 */
$(document).ready(function() {
    $('.favourite').click(function() {
        $(this).attr('src', STATIC_URL + 'img/loader_16.gif');
        var snippet_id = $(this).attr('snippet_id');
        $.ajax({
            url: "/snippet/%id/favourite/".replace("%id", snippet_id),
            type: 'POST', 
            data: { csrfmiddlewaretoken: $('#parameters input').val() },
        }).done(function(data) {
            if(data.answer && data.answer == 'ok') {
                $('#fav'+snippet_id).attr('src', STATIC_URL + 'img/' + (data.is_fav ? '' : 'un') + 'bookmarked.png');
            }
        });
    });
});
