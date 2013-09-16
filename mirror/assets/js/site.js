function showScreenshot() {
    var a = $(document);
    var b = $(".yuno-rotation-backdrop");
    if (a.scrollTop() + (window.innerHeight * 0.75) >= b.offset().top) {
        b[0].style.backgroundPositionY = "0%";
        b[0].style.opacity = 1.0;
        $(document).off("mousewheel", null);
        return 1;
    }
    return 0;
}
$().ready(function() {
    /* Hide all elements that display only if there is no JS.
     * We know JS is on because duh, this code is running. */
    var h = document.getElementsByClassName("yuno-display-only-if-js-not-enabled");
    for (var i = 0; i < h.length; i++) {
        h[i].style.display = "none";
    }
    /* Then, show the elements that require JS. */
    var s = document.getElementsByClassName("yuno-display-only-if-js-enabled");
    for (i = 0; i < s.length; i++) {
        s[i].className = s[i].className.replace("yuno-display-only-if-js-enabled", "");
    }
    var d = document.getElementsByClassName("yuno-rotation-backdrop");
    d[0].className += " " + window.site.platform;
    if (!showScreenshot())
        $(document).on("mousewheel", null, null, showScreenshot);
    var l = document.getElementById("yuno-feature-link");
    l.href = "#features-carousel";
})
