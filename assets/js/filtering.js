---
layout: null
sitemap: false
---


function filterUsingCategory(selectedCategory) {
  var id = 0;
  {% assign posts = site.posts | sort: "last_published" | reverse %}

  {% for post in posts %}
  var cats = {{ post.categories | jsonify}}

  var postDiv = document.getElementById(++id);
  postDiv.style.display =
    (selectedCategory == 'All' || cats.includes(selectedCategory))
      ? 'flex'
      : 'none';
  {% endfor %}
}


function filterUsingLanguage(selectedLanguage) {
  var all_cards = document.getElementsByClassName("podcast-card");
  Array.from(all_cards).forEach((el) => {
    el.style.display =
      (selectedLanguage == 'All' || el.classList.contains(selectedLanguage))
        ? 'flex'
        : 'none';
  })
}
