<script>
window.onload = function() {
    var anchors = document.getElementsByTagName("a");

    for (var i = 0; i < anchors.length; i++) {
        href = anchors[i].getAttribute("href");
        if ((href.startsWith("http") || href.startsWith("//")) || !(href.endsWith(".md") || href.includes(".md#"))){
            continue;
        }
        href = href.replace(/.md$/, ".html");
        anchors[i].setAttribute("href", href);
    }
}
</script>