(function () {
  var PRODUCTS = [
    { group: "squishies", name: "Dumpling", price: "£4", meta: "Glow in the dark mystery dumpling", photos: ["photos/mystery-dumpling.jpeg"], mail: "Order Dumpling" },
    { group: "squishies", name: "4 pack of mini squishies", price: "Email for price", meta: "Four mini squishies in a pack.", photos: ["photos/4-pack-of-mini-squishies.jpeg"], mail: "Order 4 pack of mini squishies" },
    { group: "squishies", name: "Noodles and mochies", price: "£2", meta: "Stretchy", photos: [], mail: "Order Noodles and mochies" },
    { group: "squishies", name: "Santa popit", price: "£5.49", meta: "Red and white popit", photos: ["photos/santa-popit.jpeg"], mail: "Order Santa popit" },
    { group: "squishies", name: "Popit", price: "£4.99", meta: "Fidget dice popit", photos: ["photos/popit-die.jpeg"], mail: "Order Popit" },
    { group: "squishies", name: "Taba dumplings", price: "£2.49", meta: "Sticky taba dumplings", photos: [], mail: "Order Taba dumplings" },
    { group: "squishies", name: "Fidget spinner", price: "£3.99", meta: "Earth fidget spinner", photos: ["photos/earth-fidget-spinner.jpeg"], mail: "Order Fidget spinner" },
    { group: "squishies", name: "Capybara watermelon", price: "£1.99", meta: "Slow-rise capybara squishie", photos: [], mail: "Order Capybara watermelon" },
    { group: "squishies", name: "Cheese", price: "£4.99", meta: "Super slow-rise cheese", photos: ["photos/slowrise-cheese.jpeg"], mail: "Order Cheese" },
    { group: "homemade", name: "Homemade balloon squishy", price: "10p – £1", meta: "There might be extras, or a balloon to fill and squish.", photos: [], mail: "Order homemade balloon squishy" },
    { group: "homemade", name: "Homemade balloon squishy", price: "10p – £1", meta: "Matches the photo.", photos: [], mail: "Order homemade balloon squishy" },
    { group: "homemade", name: "Non-balloon homemade squishy", price: "£2 – £5", meta: "Homemade, not balloon.", photos: [], mail: "Order non-balloon homemade squishy" },
    { group: "homemade", name: "Non-balloon homemade squishy", price: "£2 – £5", meta: "Matches the photo. No returns.", photos: [], mail: "Order non-balloon homemade squishy" },
    { group: "slime", name: "Water slime", price: "Email for price", meta: "At some point. Matches the photo.", photos: [], mail: "Order water slime" },
    { group: "slime", name: "Cloud slime", price: "Email for price", meta: "At some point. Matches the photo.", photos: [], mail: "Order cloud slime" },
    { group: "slime", name: "Normal slime", price: "Email for price", meta: "A few for sale.", photos: [], mail: "Order normal slime" },
    { group: "slime", name: "Homemade slime", price: "Email for price", meta: "There might be homemade slimes too.", photos: [], mail: "Order homemade slime" }
  ];

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function query() {
    var input = document.querySelector("[data-search] input");
    return ((input && input.value) || "").trim().toLowerCase();
  }

  function matches(p, q) {
    if (!q) return true;
    return (p.name + " " + p.meta + " " + p.group + " " + p.price).toLowerCase().indexOf(q) !== -1;
  }

  function galleryHtml(p) {
    var photos = p.photos || [];
    var slides;
    if (photos.length) {
      slides = photos.map(function (src, i) {
        var on = i === 0 ? " is-on" : "";
        return '<div class="slide' + on + '"><img src="' + esc(src) + '" alt="' + esc(p.name) + '"></div>';
      });
    } else {
      slides = ['<div class="slide is-on"><div class="empty"><strong>Photo</strong>Picture coming</div></div>'];
    }
    var nav = "";
    if (slides.length > 1) {
      var dots = slides.map(function (_, i) {
        var on = i === 0 ? ' class="is-on"' : "";
        return '<button type="button" data-dot' + on + ' aria-label="Photo ' + (i + 1) + '"></button>';
      }).join("");
      nav =
        '<button type="button" class="g-btn g-prev" data-prev aria-label="Previous">‹</button>' +
        '<button type="button" class="g-btn g-next" data-next aria-label="Next">›</button>' +
        '<div class="dots">' + dots + "</div>";
    }
    return '<div class="gallery" data-gallery><div class="slides">' + slides.join("") + "</div>" + nav + "</div>";
  }

  function cardHtml(p) {
    var mail = "mailto:katie@tyneside.software?subject=" + encodeURIComponent(p.mail);
    return (
      '<article class="product" data-name="' + esc(p.name) + '">' +
        galleryHtml(p) +
        '<p class="price">' + esc(p.price) + "</p>" +
        "<h2>" + esc(p.name) + "</h2>" +
        '<p class="meta">' + esc(p.meta) + "</p>" +
        '<a class="buy" href="' + mail + '">Email to buy</a>' +
      "</article>"
    );
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

  function bindGalleries(root) {
    (root || document).querySelectorAll("[data-gallery]").forEach(function (gallery) {
      if (gallery.dataset.bound) return;
      gallery.dataset.bound = "1";
      gallery.dataset.index = "0";
      show(gallery, 0);

      gallery.querySelectorAll("img").forEach(function (img) {
        img.addEventListener("error", function () {
          var empty = document.createElement("div");
          empty.className = "empty";
          empty.innerHTML = "<strong>Photo</strong>Picture coming";
          img.replaceWith(empty);
        });
      });

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

      var slides = gallery.querySelectorAll(".slide");
      if (slides.length < 2) {
        if (prev) prev.hidden = true;
        if (next) next.hidden = true;
      }
    });
  }

  function render() {
    var q = query();
    var shown = 0;
    document.querySelectorAll("[data-products]").forEach(function (el) {
      var group = el.dataset.products;
      var items = PRODUCTS.filter(function (p) {
        return p.group === group && matches(p, q);
      });
      el.innerHTML = items.map(cardHtml).join("");
      bindGalleries(el);
      shown += items.length;
      var section = el.closest(".group");
      if (section) section.hidden = items.length === 0;
    });
    var empty = document.querySelector("[data-search-empty]");
    if (empty) empty.classList.toggle("is-on", shown === 0);
  }

  function bindSearch() {
    var form = document.querySelector("[data-search]");
    if (!form) return;
    var input = form.querySelector("input");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      render();
    });
    if (input) {
      input.addEventListener("input", render);
    }
  }

  bindSearch();
  render();
})();
