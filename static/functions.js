function convertMS(milliseconds, count) {
    var minute, seconds;
    seconds = Math.floor(milliseconds / 1000);
    minute = Math.floor(seconds / 60);
    seconds = seconds % 60;
    seconds = (seconds <10 ? '0' : '') + seconds;
    minute = minute % 60;
    document.getElementById(count).innerText = minute+':'+seconds+" mins";
}