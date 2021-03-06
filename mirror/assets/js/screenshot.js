function screenshot_detectPlatform() {
    if (navigator.platform.indexOf("Win32") !== -1 || navigator.platform.indexOf("Win64") !== -1) {
        return "win";
    }
    if (/android/i.test(navigator.userAgent)) {
        return "and";
    }
    if (/armv[6-7]l/.test(navigator.platform)) {
        return "and";
    }
    if (navigator.platform.indexOf("Linux") !== -1) {
        return "lin";
    }
    if (navigator.platform.indexOf("iPhone") !== -1 || navigator.platform.indexOf("iPad") !== -1 || navigator.platform.indexOf("iPod") !== -1) {
        return "ios";
    }
    if (navigator.userAgent.indexOf("Mac OS X") !== -1) {
        return "osx";
    }
    if (navigator.platform.indexOf("MacPPC") !== -1) {
        return "osx";
    }
    if (/Mac OS X 10.[0-5]/.test(navigator.userAgent)) {
        return "osx";
    }
    if (navigator.userAgent.indexOf("MSIE 5.2") !== -1) {
        return "osx";
    }
    if (navigator.platform.indexOf("Mac") !== -1) {
        return "osx";
    }
    return "unknown";
}
window.site = {
    platform: screenshot_detectPlatform(),
};
