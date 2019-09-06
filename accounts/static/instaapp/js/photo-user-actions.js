/******************
* photo-comment.js
* Handles ajax requests to submit a comment on a photo
******************/
$(document).ready(function() {
    var opts = {
        success: successcall
    }
    $('.post_comment').on('submit', function(e) {
        e.preventDefault();
        $(this).ajaxSubmit(opts);

    });

    $('.like-button').on('click', function(e) {
        var t = $(this),
            pid = t.data('pid'),
            req_url = t.data('url');
        t.addClass('liked_photo');

        $.ajax({
            data: {
                photo_id: pid
            },
            url: req_url,
            dataType: 'json',
            type: 'post',
            success: function(data) {
                console.log(data);

            }
        });
    });

    function successcall(responseText, statusText, xhr, $form) {
        console.log("it's me");

    }

});


