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

$(document).on("click", ".data", function () {
    var abc = $(this).closest(".row");
    $.ajax({
        type: 'GET',
        data: {"id": $(this).closest(".row").attr('id'), "query": "delete", "type": $(this).closest(".tab-pane").attr('id').split('-')[1]},
        url: '/list',
        success: function () {
            abc.remove();
            return false;
        }
    });
});

$('#Modal').on('hidden.bs.modal', function (e) {
  $('#p-tracks').empty();
  $('#p-albums').empty();
  $('#p-artists').empty();
  $('#p-playlists').empty();
});

$(document).ready(function() {
    $('#limit').change(function() {
      if(this.value) {
          var newurl = "/getrecom?limit=" + $('#limit').val();
          $('a.target').attr('href', newurl);
      }
      else
          $('a.target').attr('href', '/getrecom');
    });
});

$(document).ready(function () {
    $("#getList").click(function () {
        $.ajax({
            type: 'GET',
            url: '/data',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                for(var i in data) {
                    var dat = ('p-').concat(data[i].type);
                    $('#'+dat).append("<div class=\"row no-gutters mb-2\" id=" + data[i].d_id + ">\n" +
                    "                        <div class=\"col-2\">\n" +
                    "                            <img src=" + data[i].d_src + "\n" +
                    "                                 class=\"card-img img-fluid\">\n" +
                    "                        </div>\n" +
                    "                        <div class=\"col-10 my-auto\">\n" +
                    "                            <div class=\"card-body\">\n" +
                    "                                <div class=\"card-text d-inline text-center\">" + data[i].d_name + "</div>\n" +
                    "                                <button type=\"button\" class=\"close text-white my-auto data\">\n" +
                    "                                    <span aria-hidden=\"true\">&times;</span>\n" +
                    "                                </button>\n" +
                    "                            </div>\n" +
                    "                        </div>\n" +
                    "                    </div>");
                }
            }
        });
    });
});

$(document).ready(function () {
    $(".add-song").click(function () {
        $.ajax({
            type: 'GET',
            data: {
                "id": $(this).closest(".modalDisplay").attr('id'),
                "query": "add",
                "src": $('.contentbharbc div div div img').attr("src"),
                "name": $('#songName').text(),
                "type": "tracks"
            },
            url: '/list',
            success: function (data) {
                if(data === 404) {
                    $('.failure').toast('show');
                }
                else {
                    $('.successful').toast('show');
                }
                return false;
            }
        });
    });
});

$(document).ready(function () {
    $(".add-artist").click(function () {
        $.ajax({
            type: 'GET',
            data: {
                "id": $(this).closest(".modalDisplay").attr('id'),
                "query": "add",
                "src": $('.contentbharbc div div div img').attr("src"),
                "name": $('#artistName').text(),
                "type": "artists"
            },
            url: '/list',
            success: function (data) {
                if(data === 404) {
                    $('.failure').toast('show');
                }
                else {
                    $('.successful').toast('show');
                }
                return false;
            }
        });
    });
});

$(document).ready(function () {
    $(".songclick").click(function () {
        var id = this.id;
        var recom;
        if(document.getElementsByTagName("title")[0].innerHTML === 'Recommendations')
            recom = "true";
        else
            recom = "false";
        $.ajax({
            type: 'POST',
            data: {"id": this.id, "recom": recom},
            url: '/hmm',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                $('.contentbharbc div div div img').attr("src", data[1]);
                $('#songName').text(data[0]);
                $('#artists').text('Artists: ' + artists(data[2]));
                $('#Length').text('Length: ' + convertMS(data[3]));
                $('#link').html("<a href=\"" + data[4] + "\" target=\"_blank\">Spotify Link</a>");
                $('.modalDisplay').attr('id', id);
            }
        });
    });
});

$(document).ready(function () {
    $(".albums").click(function () {
        $.ajax({
            type: 'POST',
            data: {"id": this.id},
            url: '/play',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                $('.contentbharbc div div div img').attr("src", data[1]);
                $('#albumName').text(data[0]);
                $('#artists2').text('Artists: ' + artists(data[2]));
                $('#tracks2').text('Tracks: ' + data[3]);
                $('#date').text('Release Date: ' + data[5]);
                $('#link4').html("<a href=\"" + data[4] + "\" target=\"_blank\">Spotify Link</a>");
            }
        });
    });
});

$(document).ready(function () {
    $(".playlist").click(function () {
        $.ajax({
            type: 'POST',
            data: {"id": this.id},
            url: '/alb',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                $('.contentbharbc div div div img').attr("src", data[1]);
                $('#playlistName').text(data[0]);
                $('#description').text('Description: ' + data[2]);
                $('#owner').text('Owner: ' + data[3]);
                $('#tracks').text('Tracks: ' + data[5]);
                $('#link3').html("<a href=\"" + data[4] + "\" target=\"_blank\">Spotify Link</a>");
            }
        });
    });
});

$(document).ready(function () {
    $(".artistlist").click(function () {
        var id = this.id;
        $.ajax({
            type: 'POST',
            data: {"id": this.id},
            url: '/foo',
            beforeSend: function () {
                $('#loading').show();
            },
            complete: function () {
                $('#loading').hide();
            },
            success: function (data) {
                $('.contentbharbc div div div img').attr("src", data[1]);
                $('#artistName').text(data[0]);
                $('#popularity').text('Popularity: ' + data[2]);
                $('#followers').text('Followers: ' + data[3]);
                $('#link2').html("<a href=\"" + data[4] + "\" target=\"_blank\">Spotify Link</a>");
                $('.modalDisplay').attr('id', id);
            }
        });
    });
});

function artists(data) {
    if (data.length === 1) {
        return data[0];
    } else {
        return data[0] + ' feat. ' + data.slice(1);
    }
}

(function () {
    const form = document.querySelector('#search');
    const checkboxes = form.querySelectorAll('input[type=checkbox]');
    const checkboxLength = checkboxes.length;
    const firstCheckbox = checkboxLength > 0 ? checkboxes[0] : null;

    function init() {
        if (firstCheckbox) {
            for (let i = 0; i < checkboxLength; i++) {
                checkboxes[i].addEventListener('change', checkValidity);
            }
            checkValidity();
        }
    }

    function isChecked() {
        for (let i = 0; i < checkboxLength; i++) {
            if (checkboxes[i].checked) return true;
        }
        return false;
    }

    function checkValidity() {
        const errorMessage = !isChecked() ? 'At least one checkbox must be selected.' : '';
        firstCheckbox.setCustomValidity(errorMessage);
    }

    init();
})();