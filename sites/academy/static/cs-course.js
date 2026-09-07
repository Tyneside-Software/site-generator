/* CS course quizzes — self-mark only. Never lock, never hide the rest of the page. */
(function () {
  function splitCorrect(value) {
    return String(value || "")
      .split("|")
      .map(function (s) {
        return s.trim();
      })
      .filter(Boolean);
  }

  function norm(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
  }

  function selected(fieldset) {
    var type = fieldset.getAttribute("data-type") || "single";
    if (type === "short") {
      var input = fieldset.querySelector("input[type='text']");
      return input ? [input.value] : [];
    }
    var picked = [];
    fieldset.querySelectorAll("input:checked").forEach(function (el) {
      picked.push(el.value);
    });
    return picked;
  }

  function sameSet(a, b) {
    if (a.length !== b.length) return false;
    var na = a.map(norm).sort();
    var nb = b.map(norm).sort();
    for (var i = 0; i < na.length; i++) {
      if (na[i] !== nb[i]) return false;
    }
    return true;
  }

  function shortMatch(given, accepted) {
    var g = norm(given[0] || "");
    return accepted.some(function (ans) {
      return g === norm(ans);
    });
  }

  function markFieldset(fieldset, reveal) {
    var type = fieldset.getAttribute("data-type") || "single";
    var correct = splitCorrect(fieldset.getAttribute("data-correct"));
    var got = selected(fieldset);
    var ok =
      type === "short" ? shortMatch(got, correct) : sameSet(got, correct);

    fieldset.classList.remove("is-right", "is-wrong", "is-revealed");
    if (reveal) {
      fieldset.classList.add("is-revealed");
      if (type !== "short") {
        fieldset.querySelectorAll("input").forEach(function (el) {
          var want = correct.map(norm).indexOf(norm(el.value)) !== -1;
          el.checked = want;
        });
      } else {
        var input = fieldset.querySelector("input[type='text']");
        if (input && !norm(input.value)) input.value = correct[0] || "";
      }
    } else if (got.length === 0 && type !== "short") {
      /* unanswered: leave neutral unless revealing */
    } else {
      fieldset.classList.add(ok ? "is-right" : "is-wrong");
    }

    var explain = fieldset.querySelector(".cs-q-explain");
    if (explain) explain.hidden = !(reveal || got.length || type === "short");
    if (explain && !reveal && type === "short" && !norm(got[0] || "")) {
      explain.hidden = true;
    }

    return { ok: ok, answered: type === "short" ? Boolean(norm(got[0] || "")) : got.length > 0 };
  }

  function scoreForm(form) {
    var sets = form.querySelectorAll(".cs-q");
    var right = 0;
    var answered = 0;
    sets.forEach(function (fs) {
      var result = markFieldset(fs, false);
      if (result.answered) answered += 1;
      if (result.ok) right += 1;
    });
    var out = form.querySelector(".cs-quiz-score");
    if (!out) return;
    out.hidden = false;
    out.textContent =
      "Checked: " +
      right +
      " / " +
      sets.length +
      " match the mark scheme. This is a check, not a gate — every other page stays open.";
  }

  function revealForm(form) {
    form.querySelectorAll(".cs-q").forEach(function (fs) {
      markFieldset(fs, true);
    });
    var out = form.querySelector(".cs-quiz-score");
    if (out) {
      out.hidden = false;
      out.textContent =
        "Answers shown. Read the explanations, then try again if you want. Nothing on the course is locked behind this quiz.";
    }
  }

  function resetForm(form) {
    form.querySelectorAll(".cs-q").forEach(function (fs) {
      fs.classList.remove("is-right", "is-wrong", "is-revealed");
      fs.querySelectorAll("input[type='radio'], input[type='checkbox']").forEach(function (el) {
        el.checked = false;
      });
      fs.querySelectorAll("input[type='text']").forEach(function (el) {
        el.value = "";
      });
      var explain = fs.querySelector(".cs-q-explain");
      if (explain) explain.hidden = true;
    });
    var out = form.querySelector(".cs-quiz-score");
    if (out) {
      out.hidden = true;
      out.textContent = "";
    }
  }

  document.querySelectorAll("[data-cs-quiz]").forEach(function (form) {
    var check = form.querySelector(".js-check-all");
    var reveal = form.querySelector(".js-reveal-all");
    var reset = form.querySelector(".js-reset");
    if (check) check.addEventListener("click", function () { scoreForm(form); });
    if (reveal) reveal.addEventListener("click", function () { revealForm(form); });
    if (reset) reset.addEventListener("click", function () { resetForm(form); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      scoreForm(form);
    });
  });

  function unofficialBand(pct) {
    if (pct >= 90) return "roughly grade 8–9 territory";
    if (pct >= 80) return "roughly grade 7 territory";
    if (pct >= 70) return "roughly grade 6 territory";
    if (pct >= 60) return "roughly grade 5 territory";
    if (pct >= 50) return "roughly grade 4 territory";
    if (pct >= 40) return "roughly grade 3 territory";
    if (pct >= 30) return "roughly grade 2 territory";
    return "working towards a pass on this multiple-choice paper";
  }

  function formatTime(secs) {
    var m = Math.floor(Math.max(0, secs) / 60);
    var s = Math.max(0, secs) % 60;
    return m + ":" + String(s).padStart(2, "0");
  }

  function mockBreakdown(form) {
    var by = {};
    form.querySelectorAll(".cs-q").forEach(function (fs) {
      var unit = fs.getAttribute("data-unit") || "other";
      var title = fs.getAttribute("data-unit-title") || unit;
      if (!by[unit]) by[unit] = { title: title, right: 0, total: 0 };
      by[unit].total += 1;
      var correct = splitCorrect(fs.getAttribute("data-correct"));
      if (sameSet(selected(fs), correct)) by[unit].right += 1;
    });
    return by;
  }

  function renderMockResults(form, right, total, unanswered, elapsed) {
    var box = form.querySelector(".cs-mock-results");
    if (!box) return;
    var pct = total ? Math.round((100 * right) / total) : 0;
    var by = mockBreakdown(form);
    var rows = Object.keys(by)
      .sort()
      .map(function (unit) {
        var g = by[unit];
        var href = unit + ".html";
        var weak = g.right < g.total ? ' class="is-weak"' : "";
        return (
          "<li" +
          weak +
          "><a href=\"" +
          href +
          "\">" +
          g.title +
          "</a> — " +
          g.right +
          "/" +
          g.total +
          "</li>"
        );
      })
      .join("");
    var timeLine = elapsed == null ? "Untimed sit." : "Time used: " + formatTime(elapsed) + ".";
    box.hidden = false;
    box.innerHTML =
      "<p class=\"cs-mock-scoreline\"><strong>" +
      right +
      " / " +
      total +
      "</strong> <span>(" +
      pct +
      "%)</span></p>" +
      "<p>" +
      unanswered +
      " unanswered (count as 0). " +
      timeLine +
      "</p>" +
      "<p>Unofficial band: <strong>" +
      unofficialBand(pct) +
      "</strong>. This is a multiple-choice drill, not an OCR paper and not official grade boundaries.</p>" +
      "<p>A score does not lock or unlock anything. Use the misses as a map, then jump into those lessons.</p>" +
      "<h3>By topic</h3><ul class=\"cs-mock-topics\">" +
      rows +
      "</ul>";
    box.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function setMockLocked(form, locked) {
    form.classList.toggle("is-marked", locked);
    form.querySelectorAll("input[type='radio']").forEach(function (el) {
      el.disabled = locked;
    });
    var arm = form.querySelector(".js-timer-arm");
    if (arm) arm.disabled = locked;
  }

  function submitMock(form, elapsed) {
    var sets = form.querySelectorAll(".cs-q");
    var right = 0;
    var unanswered = 0;
    sets.forEach(function (fs) {
      var result = markFieldset(fs, false);
      if (!result.answered) {
        unanswered += 1;
        fs.classList.add("is-wrong");
      }
      if (result.ok) right += 1;
      var explain = fs.querySelector(".cs-q-explain");
      if (explain) explain.hidden = false;
    });
    setMockLocked(form, true);
    renderMockResults(form, right, sets.length, unanswered, elapsed);
    try {
      localStorage.setItem(
        "cs-" + (form.getAttribute("data-mock-id") || "mock"),
        JSON.stringify({
          right: right,
          total: sets.length,
          pct: sets.length ? Math.round((100 * right) / sets.length) : 0,
          at: new Date().toISOString(),
        })
      );
    } catch (e) {
      /* private mode — fine */
    }
  }

  document.querySelectorAll("[data-cs-mock]").forEach(function (form) {
    var timerEl = form.querySelector("[data-cs-timer]");
    var arm = form.querySelector(".js-timer-arm");
    var reset = form.querySelector(".js-reset-mock");
    var minutes = parseInt(form.getAttribute("data-minutes") || "35", 10);
    var tick = null;
    var remaining = minutes * 60;
    var startedAt = null;
    var submitted = false;

    function stopTick() {
      if (tick) {
        clearInterval(tick);
        tick = null;
      }
    }

    function elapsedSecs() {
      if (startedAt == null) return null;
      return Math.round((Date.now() - startedAt) / 1000);
    }

    function finish() {
      if (submitted) return;
      submitted = true;
      stopTick();
      submitMock(form, elapsedSecs());
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      finish();
    });

    if (arm && timerEl) {
      arm.addEventListener("change", function () {
        if (submitted) return;
        stopTick();
        if (!arm.checked) {
          timerEl.hidden = true;
          startedAt = null;
          remaining = minutes * 60;
          timerEl.textContent = "Time left: " + formatTime(remaining);
          return;
        }
        remaining = minutes * 60;
        startedAt = Date.now();
        timerEl.hidden = false;
        timerEl.textContent = "Time left: " + formatTime(remaining);
        tick = setInterval(function () {
          remaining -= 1;
          timerEl.textContent = "Time left: " + formatTime(remaining);
          if (remaining <= 0) finish();
        }, 1000);
      });
    }

    if (reset) {
      reset.addEventListener("click", function () {
        submitted = false;
        stopTick();
        startedAt = null;
        remaining = minutes * 60;
        if (arm) {
          arm.checked = false;
          arm.disabled = false;
        }
        if (timerEl) {
          timerEl.hidden = true;
          timerEl.textContent = "Time left: " + formatTime(remaining);
        }
        setMockLocked(form, false);
        resetForm(form);
        var box = form.querySelector(".cs-mock-results");
        if (box) {
          box.hidden = true;
          box.innerHTML = "";
        }
      });
    }
  });

  document.querySelectorAll("[data-cs-last-score]").forEach(function (el) {
    try {
      var raw = localStorage.getItem("cs-" + el.getAttribute("data-cs-last-score"));
      if (!raw) return;
      var data = JSON.parse(raw);
      if (!data || data.right == null) return;
      var when = data.at ? data.at.slice(0, 10) : "";
      el.textContent =
        "Last sit: " + data.right + "/" + data.total + " (" + data.pct + "%)" + (when ? " · " + when : "");
    } catch (e) {
      /* ignore */
    }
  });
})();
