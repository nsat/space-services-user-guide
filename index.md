---
title: Spire Space Services

language_tabs: # must be one of https://git.io/vQNgJ
  - shell
  - c
  - python

includes:
  - Readme

search: true

code_clipboard: true

columns: 2
---
<script>
window.onload = function() {
    var anchors = document.getElementsByTagName("a");

    for (var i = 0; i < anchors.length; i++) {
        href = anchors[i].getAttribute("href");
        if ((href.startsWith("http") || href.startsWith("//")) || !(href.endsWith(".md") || href.contains(".md#"))){
            continue;
        }
        href = href.replace(/.md$/, ".html");
        anchors[i].setAttribute("href", href);
    }
}
</script>