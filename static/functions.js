function convertMS(milliseconds) {
    var minute, seconds;
    seconds = Math.floor(milliseconds / 1000);
    minute = Math.floor(seconds / 60);
    seconds = seconds % 60;
    seconds = (seconds < 10 ? '0' : '') + seconds;
    minute = minute % 60;
    return (minute + ':' + seconds + " mins");
}

$(window).scroll(function () {
    var height = $(window).scrollTop();
    if (height > 10) {
        $('.gotoTop').fadeIn();
    } else {
        $('.gotoTop').fadeOut();
    }
});
$(document).ready(function () {
    $(".gotoTop").click(function (event) {
        event.preventDefault();
        $("html, body").animate({scrollTop: 0}, "slow");
        return false;
    });
});

$(document).ready(function () {
    $(".songlist").click(function () {
        console.log(this.id)
        $.ajax({
            type: 'POST',
            data: {"id": this.id},
            url: '/hmm',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                console.log(data);
                $('.contentbharbc div div div img').attr("src", data[1]);
                $('#songName').text(data[0]);
                $('#artists').text('Artists: ' + artists(data[2]));
                $('#Length').text('Length: ' + convertMS(data[3]));
                $('#link').html("<a href=\"" + data[4] + "\" target=\"_blank\">Spotify Link</a>");
            }
        });
    });
});

function artists(data) {
    if (data.length === 1) {
        return data[0];
    }
    else {
        return data[0] + ' feat. ' + data.slice(1);
    }
}