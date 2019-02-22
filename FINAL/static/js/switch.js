$(function() {
    var a = $('<div id="right-suspend">'), b = $('<div class="rs-close" style="width: 9px; height: 9px; overflow: hidden; font-size: 0; line-height: 0; background: url(rs-close.png) no-repeat; position: absolute; right: 5px; top: 0; cursor: pointer;">');
    c = $('<div id="backtotop">');
    $("body").append(a).append(c);
    a.append('').append(b);
    b.click(function(event) {
        a.css("display", "none");
    });
    $(window).scroll(function() {
        $(document).scrollTop() > 500 ? c.fadeIn() :c.fadeOut();
    });
    c.click(function() {
        $("html, body").animate({
            scrollTop:0
        }, 500);
    });
});