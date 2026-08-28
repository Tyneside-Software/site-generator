(function () {
  function mail(name) {
    return "mailto:katie@tyneside.software?subject=" + encodeURIComponent("Order " + name);
  }

  function slidePhoto(src, alt) {
    if (src) {
      return (
        '<div class="slide"><img src="' + src + '" alt="' + alt.replace(/"/g, "") +
        '" onerror="this.parentNode.innerHTML=\'<div class=empty><strong>Photo</strong>Picture coming</div>\'"></div>'
      );
    }
    return '<div class="slide"><div class="empty"><strong>Photo</strong>Picture coming</div></div>';
  }

  function renderStock(root, items) {
    root.innerHTML = items.map(function (item) {
      var photos = item.photos && item.photos.length ? item.photos : [""];
      var slides = photos.map(function (src) {
        return slidePhoto(src, item.name);
      });
      slides.push('<div class="slide"><div class="empty"><strong>Video</strong>Slide here for the video</div></div>');
      if (item.video) {
        slides[slides.length - 1] =
          '<div class="slide"><video src="' + item.video + '" controls playsinline></video></div>';
      }
      var dots = slides.map(function (_, i) {
        return '<button type="button" data-dot' + (i === 0 ? ' class="is-on"' : "") +
          ' aria-label="Slide ' + (i + 1) + '"></button>';
      }).join("");
      slides[0] = slides[0].replace('class="slide"', 'class="slide is-on"');
      return (
        '<article class="product">' +
          '<div class="gallery" data-gallery>' +
            '<div class="slides">' + slides.join("") + "</div>" +
            '<button type="button" class="g-btn g-prev" data-prev aria-label="Previous">‹</button>' +
            '<button type="button" class="g-btn g-next" data-next aria-label="Next">›</button>' +
            '<div class="dots">' + dots + "</div>" +
          "</div>" +
          '<p class="price">' + item.price + "</p>" +
          "<h2>" + item.name + "</h2>" +
          '<p class="meta">' + item.description + "</p>" +
          '<a class="buy" href="' + mail(item.name) + '">Email to buy</a>' +
        "</article>"
      );
    }).join("");
  }

  var stockRoot = document.querySelector("[data-stock]");
  if (stockRoot) {
    var src = stockRoot.getAttribute("data-stock") || "stock.json";
    fetch(src).then(function (r) { return r.json(); }).then(function (data) {
      renderStock(stockRoot, data.items || []);
      bindGalleries();
    }).catch(function () {
      stockRoot.innerHTML = "<p>Could not load the shop list. Email katie@tyneside.software.</p>";
    });
  } else {
    bindGalleries();
  }

  function show(gallery, index) {
    var slides = gallery.querySelectorAll(".slide");
    var dots = gallery.querySelectorAll("[data-dot]");
    var n = slides.length;
    if (!n) return;
    var i = (index + n) % n;
    gallery.dataset.index = String(i);
    for (var s = 0; s < n; s++) {
      slides[s].classList.toggle("is-on", s === i);
      var video = slides[s].querySelector("video");
      if (video) {
        if (s === i) {
          video.play().catch(function () {});
        } else {
          video.pause();
        }
      }
    }
    for (var d = 0; d < dots.length; d++) {
      dots[d].classList.toggle("is-on", d === i);
    }
  }

  function bindGalleries() {
    document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
    if (gallery.dataset.bound) return;
    gallery.dataset.bound = "1";
    var slides = gallery.querySelectorAll(".slide");
    gallery.dataset.index = "0";
    show(gallery, 0);

    var prev = gallery.querySelector("[data-prev]");
    var next = gallery.querySelector("[data-next]");
    if (prev) {
      prev.addEventListener("click", function () {
        show(gallery, Number(gallery.dataset.index) - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        show(gallery, Number(gallery.dataset.index) + 1);
      });
    }
    gallery.querySelectorAll("[data-dot]").forEach(function (dot, j) {
      dot.addEventListener("click", function () { show(gallery, j); });
    });

    if (slides.length < 2) {
      if (prev) prev.hidden = true;
      if (next) next.hidden = true;
    }
    });
  }
})();
