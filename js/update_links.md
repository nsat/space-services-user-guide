<!-- updates slatedocs internal links from .md to .html -->
<script>
$(function() {
var anchors = document.getElementsByTagName("a");

for (var i = 0; i < anchors.length; i++) {
    var href = anchors[i].getAttribute("href");
    if ((href.startsWith("http") || href.startsWith("//")) || !(href.endsWith(".md") || href.includes(".md#"))){
        continue;
    }
    href = href.replace(/.md/, ".html");
    anchors[i].setAttribute("href", href);
}
});
</script>