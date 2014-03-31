$(document).ready(function() {
    $('.vote').click(function() {
        var snippet_id = $(this).attr('snippet_id');
        $.ajax({
            url: "/vote/for_snippet/%id/%opinion/".replace("%id", snippet_id).replace('%opinion', $(this).hasClass('vote_up') ? 'up' : 'down'),
            type: 'POST',
            data: { csrfmiddlewaretoken: $('#parameters input').val() },
        }).done(function(data) {
            if(data.answer && data.answer == 'ok') {
               $('#score'+snippet_id).html(data.new_score); 
            }
        });
    });
});
