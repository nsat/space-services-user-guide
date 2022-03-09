<link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css" rel="stylesheet">

<!-- updates slatedocs internal links from .md to .html, and tags external links -->
<script>
$(function() {
    var anchors = document.getElementsByTagName("a");

    for (var i = 0; i < anchors.length; i++) {
        var a = anchors[i];
        var href = a.getAttribute("href");

        if (href.startsWith("http") || href.startsWith("//")){
            a.setAttribute("target", "_tab");
            a.innerHTML += " <i class=\"icon-external-link\"></i>";
            continue;
        }
        if (href.endsWith(".md") || href.includes(".md#")){
            a.setAttribute("href", href.replace(/.md/, ".html"));
        }
    }
});
</script>
