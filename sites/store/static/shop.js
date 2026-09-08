(function () {
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

  bindGalleries();
})();
