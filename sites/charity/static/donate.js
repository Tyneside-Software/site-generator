/**
 * Charity donate form — name, location, amount →
 * optional Cloud Run intent API (WhatsApp Master) + Tide (if configured).
 */
(function () {
  var cfg = window.TYNESIDE_DONATE || {};
  var form = document.getElementById("donate-form");
  if (!form) return;

  var nameEl = document.getElementById("donate-name");
  var locationEl = document.getElementById("donate-location");
  var amountEls = form.querySelectorAll('input[name="donate-amount"]');
  var statusEl = document.getElementById("donate-status");
  var refBox = document.getElementById("donate-ref-box");
  var refText = document.getElementById("donate-ref-text");
  var copyBtn = document.getElementById("donate-copy-ref");
  var waBtn = document.getElementById("donate-whatsapp-ref");
  var payBtn = document.getElementById("donate-pay");

  function selectedAmount() {
    for (var i = 0; i < amountEls.length; i++) {
      if (amountEls[i].checked) return parseInt(amountEls[i].value, 10);
    }
    return null;
  }

  function todayISO() {
    var d = new Date();
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, "0");
    var day = String(d.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + day;
  }

  function clean(s) {
    return String(s || "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function buildRefLine(name, location, amount) {
    return (
      "WHC £" + amount + " | " + name + " | " + location + " | " + todayISO()
    );
  }

  function setStatus(msg, isError) {
    if (!statusEl) return;
    statusEl.hidden = !msg;
    statusEl.textContent = msg || "";
    statusEl.classList.toggle("is-error", !!isError);
  }

  function tideUrlFor(amount) {
    var links = cfg.tideLinks || {};
    var url = links[amount] || links[String(amount)] || "";
    return typeof url === "string" ? url.trim() : "";
  }

  function apiBase() {
    var base = (cfg.apiBaseUrl || "").trim().replace(/\/$/, "");
    return base;
  }

  /**
   * POST donate intent to Cloud Run (notifies Master via WhatsApp Business API).
   * Never uses the donor's WhatsApp. Fails soft if API is down/unconfigured.
   */
  function postDonateIntent(name, location, amount) {
    var base = apiBase();
    if (!base) {
      return Promise.resolve({ skipped: true, reason: "no apiBaseUrl" });
    }
    var headers = { "Content-Type": "application/json", Accept: "application/json" };
    if (cfg.apiKey) headers["X-Tyneside-Key"] = cfg.apiKey;

    return fetch(base + "/v1/donate/intent", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        name: name,
        location: location,
        amount_gbp: amount,
        site: "charity",
        donor_date: todayISO(),
      }),
    }).then(function (res) {
      return res.json().then(function (data) {
        return { httpOk: res.ok, data: data };
      });
    });
  }

  function showRef(line) {
    if (refBox) refBox.hidden = false;
    if (refText) refText.textContent = line;
    if (waBtn) {
      var msg =
        "Hello — I have donated (or am about to donate) to the welcome-home cleans programme.\n\n" +
        line +
        "\n\nPlease add me to the public donor list when the payment lands in Tide.";
      waBtn.href =
        "https://wa.me/" +
        (cfg.whatsappNumber || "447411949215") +
        "?text=" +
        encodeURIComponent(msg);
    }
  }

  function openPayment(amount) {
    var tide = tideUrlFor(amount);
    if (tide) {
      window.open(tide, "_blank", "noopener,noreferrer");
      if (payBtn) payBtn.textContent = "Open payment again";
      return;
    }
    // No Tide link yet — optional donor WhatsApp as fallback
    if (waBtn) {
      window.open(waBtn.href, "_blank", "noopener,noreferrer");
    }
    if (payBtn) payBtn.textContent = "Message on WhatsApp again";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = clean(nameEl && nameEl.value);
    var location = clean(locationEl && locationEl.value);
    var amount = selectedAmount();

    if (!name) {
      setStatus("Please enter the name you want on the donor list.", true);
      if (nameEl) nameEl.focus();
      return;
    }
    if (!location) {
      setStatus("Please enter a location (town or area).", true);
      if (locationEl) locationEl.focus();
      return;
    }
    if (!amount) {
      setStatus("Please choose a donation amount.", true);
      return;
    }

    var line = buildRefLine(name, location, amount);
    showRef(line);

    if (payBtn) {
      payBtn.disabled = true;
      payBtn.textContent = "Working…";
    }

    postDonateIntent(name, location, amount)
      .then(function (result) {
        var apiNote = "";
        if (result && result.skipped) {
          apiNote =
            " (Background notify not configured yet — set apiBaseUrl after Cloud Run deploy.)";
        } else if (result && result.httpOk && result.data && result.data.donor_line) {
          line = result.data.donor_line;
          showRef(line);
          var wa = result.data.whatsapp || {};
          if (wa.ok) {
            apiNote = " Master has been notified automatically.";
          } else if (wa.skipped) {
            apiNote =
              " Intent received by API; WhatsApp on the server not configured yet.";
          } else if (wa.error) {
            apiNote = " Intent saved path had a WhatsApp error — payment can still go ahead.";
          }
        } else if (result && !result.httpOk) {
          apiNote = " Could not reach the notify API — payment can still go ahead.";
        }

        setStatus(
          "Your donor line is ready." +
            apiNote +
            " Tide Instant Checkout cannot take a custom payment reference — " +
            "we match by amount and date. We list you on the public tracker within 3 business days of payment.",
          false
        );
        openPayment(amount);
      })
      .catch(function () {
        setStatus(
          "Your donor line is ready. Notify API unreachable — payment can still go ahead. " +
            "We list you within 3 business days of payment.",
          false
        );
        openPayment(amount);
      })
      .finally(function () {
        if (payBtn) {
          payBtn.disabled = false;
          if (!payBtn.textContent || payBtn.textContent === "Working…") {
            payBtn.textContent = "Pay donation";
          }
        }
      });
  });

  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var text = refText ? refText.textContent : "";
      if (!text) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () {
            setStatus("Copied donor line to clipboard.", false);
          },
          function () {
            setStatus("Could not copy — select the line and copy manually.", true);
          }
        );
      } else {
        setStatus("Select the line and copy it manually.", true);
      }
    });
  }
})();
