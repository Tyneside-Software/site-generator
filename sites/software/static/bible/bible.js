(function () {
  var body = document.body;
  var toggle = document.getElementById("nav-toggle");
  var closeBtn = document.getElementById("nav-close");
  var backdrop = document.getElementById("nav-backdrop");
  var side = document.getElementById("chapter-side");
  var jumpForm = document.getElementById("jump-form");
  var jumpInput = document.getElementById("jump-input");
  var jumpErr = document.getElementById("jump-err");
  var filter = document.getElementById("nav-filter");
  var canon = window.BIBLE_CANON || [];

  function isMobileNav() {
    return window.matchMedia("(max-width: 900px)").matches;
  }
  function openNav() {
    body.classList.add("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "true");
    if (backdrop) backdrop.hidden = false;
  }
  function closeNav() {
    body.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    if (backdrop) backdrop.hidden = true;
  }

  if (toggle && side) {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (body.classList.contains("nav-open")) closeNav();
      else openNav();
    });
    if (closeBtn) {
      closeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        closeNav();
      });
    }
    if (backdrop) {
      backdrop.addEventListener("click", function (e) {
        e.preventDefault();
        closeNav();
      });
    }
    side.querySelectorAll("a.nav-item").forEach(function (a) {
      a.addEventListener("click", function () {
        if (isMobileNav()) setTimeout(closeNav, 10);
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
    window.addEventListener("resize", function () {
      if (!isMobileNav()) closeNav();
    });
  }

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/[’']/g, "")
      .replace(/[^a-z0-9]+/g, "");
  }

  var lookup = [];
  canon.forEach(function (book) {
    var keys = [book.name, book.slug].concat(book.aliases || []);
    keys.forEach(function (k) {
      lookup.push({ key: norm(k), book: book });
    });
  });
  lookup.sort(function (a, b) { return b.key.length - a.key.length; });

  function findBook(raw) {
    var n = norm(raw);
    if (!n) return null;
    var numbered = n.match(/^([123])(.+)$/);
    var candidates = [n];
    if (numbered) {
      candidates.push(numbered[1] + numbered[2]);
    }
    for (var i = 0; i < lookup.length; i++) {
      for (var c = 0; c < candidates.length; c++) {
        if (lookup[i].key === candidates[c] || candidates[c].indexOf(lookup[i].key) === 0 && candidates[c].length - lookup[i].key.length < 3) {
          if (lookup[i].key === candidates[c]) return lookup[i].book;
        }
      }
    }
    for (var j = 0; j < lookup.length; j++) {
      if (lookup[j].key === n) return lookup[j].book;
    }
    var starts = lookup.filter(function (row) { return row.key.indexOf(n) === 0 || n.indexOf(row.key) === 0; });
    if (starts.length) {
      starts.sort(function (a, b) { return b.key.length - a.key.length; });
      return starts[0].book;
    }
    return null;
  }

  function parseRef(q) {
    var s = String(q || "").trim();
    if (!s) return null;
    var m = s.match(/^(.+?)\s+(\d+)(?:\s*[:.]\s*(\d+))?$/);
    var bookName;
    var chapter = null;
    var verse = null;
    if (m) {
      bookName = m[1];
      chapter = parseInt(m[2], 10);
      if (m[3]) verse = parseInt(m[3], 10);
    } else {
      bookName = s;
    }
    var book = findBook(bookName);
    if (!book) return null;
    if (chapter != null && (chapter < 1 || chapter > book.chapters)) return null;
    if (verse != null && verse < 1) return null;
    return { book: book, chapter: chapter, verse: verse };
  }

  function hrefFor(ref, fromBookPage) {
    var prefix = fromBookPage ? "" : "books/";
    if (body.getAttribute("data-page") === "book") {
      var current = body.getAttribute("data-book");
      if (ref.book.slug === current) prefix = "";
      else prefix = "";
      var file = (ref.book.slug === current) ? "" : (ref.book.slug + ".html");
      var hash = "";
      if (ref.chapter && ref.verse) hash = "#c-" + ref.chapter + "-v-" + ref.verse;
      else if (ref.chapter) hash = "#c-" + ref.chapter;
      if (!file) return hash || "#c-1";
      return file + hash;
    }
    var hash2 = "";
    if (ref.chapter && ref.verse) hash2 = "#c-" + ref.chapter + "-v-" + ref.verse;
    else if (ref.chapter) hash2 = "#c-" + ref.chapter;
    return "books/" + ref.book.slug + ".html" + hash2;
  }

  if (jumpForm && jumpInput) {
    jumpForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var ref = parseRef(jumpInput.value);
      if (!ref) {
        if (jumpErr) jumpErr.textContent = "Try John 3:16 or Psalm 23";
        return;
      }
      if (jumpErr) jumpErr.textContent = "";
      var url = hrefFor(ref);
      window.location.href = url;
      if (isMobileNav()) closeNav();
    });
  }

  if (filter && side) {
    filter.addEventListener("input", function () {
      var q = filter.value.trim().toLowerCase();
      side.querySelectorAll("[data-filter]").forEach(function (el) {
        var hay = (el.getAttribute("data-filter") || "").toLowerCase();
        el.classList.toggle("is-hidden", q && hay.indexOf(q) === -1);
      });
      side.querySelectorAll(".nav-group").forEach(function (g) {
        var next = g.nextElementSibling;
        var any = false;
        while (next && !next.classList.contains("nav-group")) {
          if (next.matches(".nav-item") && !next.classList.contains("is-hidden")) any = true;
          next = next.nextElementSibling;
        }
        g.classList.toggle("is-hidden", q && !any);
      });
    });
  }

  var chapters = Array.prototype.slice.call(document.querySelectorAll("article.chapter[id]"));
  var navById = {};
  if (side) {
    side.querySelectorAll("a.nav-item[href^='#']").forEach(function (a) {
      navById[a.getAttribute("href").slice(1)] = a;
    });
  }
  if (chapters.length && "IntersectionObserver" in window) {
    var currentId = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) currentId = entry.target.id;
      });
      Object.keys(navById).forEach(function (id) {
        navById[id].classList.toggle("is-active", id === currentId);
      });
    }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });
    chapters.forEach(function (ch) { io.observe(ch); });
  }

  var bookSlug = body.getAttribute("data-book");
  if (bookSlug) {
    try {
      localStorage.setItem("tyneside-bible-last", JSON.stringify({
        slug: bookSlug,
        hash: location.hash || "#c-1",
        at: Date.now()
      }));
    } catch (e) {}
  }

  var resume = document.getElementById("resume-link");
  if (resume) {
    try {
      var last = JSON.parse(localStorage.getItem("tyneside-bible-last") || "null");
      if (last && last.slug) {
        resume.href = "books/" + last.slug + ".html" + (last.hash || "");
        resume.hidden = false;
      }
    } catch (e) {}
  }

  var audio = document.getElementById("bible-audio");
  var bars = Array.prototype.slice.call(document.querySelectorAll(".ch-audio[data-src]"));
  var dock = document.getElementById("audio-dock");
  var dockToggle = document.getElementById("dock-toggle");
  var dockLabel = document.getElementById("dock-label");
  var dockTime = document.getElementById("dock-time");
  var currentBar = null;
  var currentSrc = "";

  function fmt(t) {
    if (!isFinite(t)) return "0:00";
    var m = Math.floor(t / 60);
    var s = Math.floor(t % 60);
    return m + ":" + String(s).padStart(2, "0");
  }

  function setBarState(bar, state) {
    bars.forEach(function (b) {
      var on = b === bar && state === "playing";
      var loading = b === bar && state === "loading";
      var btn = b.querySelector(".btn-play");
      var wrap = b.querySelector(".progress-wrap");
      var time = b.querySelector(".audio-time");
      b.classList.toggle("playing", on);
      if (btn) {
        btn.classList.toggle("playing", on);
        btn.textContent = loading ? "Starting…" : on ? "Pause" : "Play";
      }
      if (wrap) wrap.hidden = !on && !loading;
      if (time) time.hidden = !on && !loading;
    });
    if (dock) {
      var show = state === "playing" || state === "loading" || state === "paused";
      dock.hidden = !show || !bar;
      body.classList.toggle("audio-on", show && !!bar);
      if (dockToggle) dockToggle.textContent = state === "playing" ? "Pause" : "Play";
      if (dockLabel && bar) dockLabel.textContent = bar.getAttribute("data-label") || "";
    }
  }

  function preloadNext(bar) {
    var i = bars.indexOf(bar);
    var next = i >= 0 ? bars[i + 1] : null;
    var url = next && next.getAttribute("data-src");
    var id = "bible-audio-preload";
    var old = document.getElementById(id);
    if (!url) {
      if (old) old.remove();
      return;
    }
    if (old && old.getAttribute("href") === url) return;
    if (old) old.remove();
    var link = document.createElement("link");
    link.id = id;
    link.rel = "preload";
    link.as = "audio";
    link.href = url;
    document.head.appendChild(link);
  }

  function playBar(bar) {
    if (!audio || !bar) return;
    var src = bar.getAttribute("data-src");
    if (!src) return;
    var err = bar.querySelector(".audio-err");
    if (err) {
      err.hidden = true;
      err.textContent = "";
    }
    currentBar = bar;
    if (currentSrc !== src) {
      currentSrc = src;
      audio.src = src;
    } else if (audio.ended) {
      audio.currentTime = 0;
    }
    setBarState(bar, "loading");
    var p = audio.play();
    if (p && p.catch) {
      p.catch(function () {
        if (err) {
          err.hidden = false;
          err.textContent = "Could not play this chapter. Use Download.";
        }
        setBarState(bar, "paused");
      });
    }
    preloadNext(bar);
  }

  if (audio && bars.length) {
    bars.forEach(function (bar) {
      var btn = bar.querySelector(".btn-play");
      if (btn) {
        btn.addEventListener("click", function () {
          if (currentBar === bar && !audio.paused && !audio.ended) {
            audio.pause();
            setBarState(bar, "paused");
            return;
          }
          playBar(bar);
        });
      }
      var pbar = bar.querySelector(".progress-bar");
      if (pbar) {
        pbar.addEventListener("click", function (e) {
          if (!audio.duration || currentBar !== bar) return;
          var r = pbar.getBoundingClientRect();
          audio.currentTime = ((e.clientX - r.left) / r.width) * audio.duration;
        });
      }
    });

    audio.addEventListener("canplay", function () {
      if (currentBar && !audio.paused) setBarState(currentBar, "playing");
    });
    audio.addEventListener("playing", function () {
      if (currentBar) {
        setBarState(currentBar, "playing");
        preloadNext(currentBar);
      }
    });
    audio.addEventListener("pause", function () {
      if (currentBar && !audio.ended) setBarState(currentBar, "paused");
    });
    audio.addEventListener("timeupdate", function () {
      if (!currentBar) return;
      var fill = currentBar.querySelector(".progress-fill");
      var time = currentBar.querySelector(".audio-time");
      var stamp = fmt(audio.currentTime) + " / " + fmt(audio.duration);
      if (fill && audio.duration) {
        fill.style.width = (100 * audio.currentTime / audio.duration) + "%";
      }
      if (time) time.textContent = stamp;
      if (dockTime) dockTime.textContent = stamp;
    });
    audio.addEventListener("ended", function () {
      if (!currentBar) return;
      var art = currentBar.closest("article.chapter");
      var nextArt = art && art.nextElementSibling;
      var nextBar = nextArt && nextArt.querySelector && nextArt.querySelector(".ch-audio[data-src]");
      if (nextBar) {
        playBar(nextBar);
        var nextEl = nextBar.closest("article.chapter");
        if (nextEl) nextEl.scrollIntoView({ block: "start" });
        return;
      }
      setBarState(currentBar, "paused");
    });
    audio.addEventListener("error", function () {
      if (!currentBar) return;
      var err = currentBar.querySelector(".audio-err");
      if (err) {
        err.hidden = false;
        err.textContent = "Could not load audio. Use Download.";
      }
      setBarState(currentBar, "paused");
    });

    if (dockToggle) {
      dockToggle.addEventListener("click", function () {
        if (!currentBar) return;
        if (audio.paused) playBar(currentBar);
        else {
          audio.pause();
          setBarState(currentBar, "paused");
        }
      });
    }
  }
})();
