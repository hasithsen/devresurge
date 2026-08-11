/* DevResurge — theme toggle + mobile nav + alert dismiss + copy-to-clipboard.
 * Vanilla JS, no external deps. Safe to load with `defer`. */
(function () {
  "use strict";

  var STORAGE_KEY = "devresurge:theme";

  /* ----- Theme ---------------------------------------------------------- */
  function preferredTheme() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "light") return "light";
    } catch (_) {}
    return "dark";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    var toggles = document.querySelectorAll("[data-theme-toggle]");
    toggles.forEach(function (btn) {
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
      var label = btn.querySelector("[data-theme-label]");
      if (label) label.textContent = theme === "light" ? "dark" : "light";
    });
  }

  applyTheme(preferredTheme());

  function toggleTheme() {
    var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch (_) {}
    applyTheme(next);
  }

  function bindThemeToggles() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", toggleTheme);
    });
  }

  /* ----- Live region announcements ------------------------------------ */
  function announce(message) {
    var live = document.getElementById("dr-live");
    if (!live) return;
    live.textContent = "";
    window.setTimeout(function () {
      live.textContent = message;
    }, 20);
  }

  function prefersReducedMotion() {
    try {
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch (_) {
      return false;
    }
  }

  /* ----- Mobile nav ---------------------------------------------------- */
  function initNav() {
    var nav = document.querySelector(".dr-nav");
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu = document.querySelector("[data-nav-menu]");
    var backdrop = document.querySelector("[data-nav-backdrop]");
    var main = document.getElementById("main");
    var footer = document.querySelector(".dr-footer");
    if (!toggle || !menu) return;

    function measure() {
      if (!nav) return;
      var h = Math.round(nav.getBoundingClientRect().height) || 56;
      document.documentElement.style.setProperty("--dr-nav-h", h + "px");
    }
    measure();
    window.addEventListener("resize", measure, { passive: true });
    if ("ResizeObserver" in window && nav) {
      try { new ResizeObserver(measure).observe(nav); } catch (_) {}
    }

    function setInert(on) {
      [main, footer].forEach(function (el) {
        if (!el) return;
        if (on) el.setAttribute("inert", "");
        else el.removeAttribute("inert");
      });
      if (backdrop) {
        if (on) backdrop.removeAttribute("hidden");
        else backdrop.setAttribute("hidden", "");
      }
    }

    function close() {
      if (!menu.classList.contains("is-open")) return;
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("dr-nav-open");
      setInert(false);
    }

    function open() {
      measure();
      menu.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("dr-nav-open");
      setInert(true);
    }

    toggle.addEventListener("click", function (event) {
      event.stopPropagation();
      if (menu.classList.contains("is-open")) close();
      else open();
    });

    if (backdrop) {
      backdrop.addEventListener("click", close);
    }

    document.addEventListener("click", function (event) {
      if (!menu.classList.contains("is-open")) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      close();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        if (menu.classList.contains("is-open")) {
          close();
          toggle.focus();
        }
      }
    });

    menu.addEventListener("click", function (event) {
      var target = event.target.closest("a");
      if (target) close();
    });

    var mql = window.matchMedia("(min-width: 721px)");
    var onMq = function (e) { if (e.matches) close(); };
    if (mql.addEventListener) mql.addEventListener("change", onMq);
    else if (mql.addListener) mql.addListener(onMq);
  }

  /* ----- Dismissible alerts ------------------------------------------- */
  function dismissAlert(target) {
    if (!target || !target.parentNode) return;
    var reduce = prefersReducedMotion();
    if (reduce) {
      target.parentNode.removeChild(target);
      return;
    }
    target.style.transition = "opacity 160ms ease, transform 160ms ease";
    target.style.opacity = "0";
    target.style.transform = "translateY(-4px)";
    window.setTimeout(function () {
      if (target.parentNode) target.parentNode.removeChild(target);
    }, 180);
  }

  function initAlerts() {
    document.querySelectorAll("[data-dismiss-alert]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        dismissAlert(btn.closest(".dr-alert"));
      });
    });
  }

  /* ----- Copy-to-clipboard -------------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "absolute";
        ta.style.left = "-9999px";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        resolve();
      } catch (e) {
        reject(e);
      }
    });
  }

  function initCopyButtons() {
    var nodes = document.querySelectorAll("[data-copy], [data-copy-from]");
    nodes.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var value = btn.getAttribute("data-copy");
        if (!value) {
          var ref = btn.getAttribute("data-copy-from");
          if (ref) {
            var src = document.querySelector(ref);
            if (src) value = (src.textContent || src.value || "").trim();
          }
        }
        if (!value) return;

        var label = btn.querySelector("[data-copy-label]");
        var original = label ? label.textContent : null;

        function flash(text, cls) {
          btn.classList.add(cls);
          if (label) label.textContent = text;
          announce(text);
          window.setTimeout(function () {
            btn.classList.remove(cls);
            if (label && original !== null) label.textContent = original;
          }, 1400);
        }

        copyText(value)
          .then(function () { flash("copied", "is-copied"); })
          .catch(function () { flash("copy failed", "is-error"); });
      });
    });
  }

  /* ----- Avatar preview ----------------------------------------------- */
  var MAX_AVATAR_BYTES = 2 * 1024 * 1024;

  function showInlineError(input, message) {
    var field = input.closest(".dr-field") || input.parentNode;
    if (!field) return;
    var existing = field.querySelector(".dr-errors[data-client-error]");
    if (existing) existing.remove();
    if (!message) return;
    var ul = document.createElement("ul");
    ul.className = "dr-errors";
    ul.setAttribute("data-client-error", "");
    var li = document.createElement("li");
    li.textContent = message;
    ul.appendChild(li);
    field.appendChild(ul);
  }

  function initAvatarPreview() {
    document.querySelectorAll("[data-avatar-input]").forEach(function (input) {
      input.addEventListener("change", function () {
        var preview = document.querySelector("[data-avatar-preview]");
        var file = input.files && input.files[0];
        if (!file) {
          showInlineError(input, null);
          return;
        }
        if (file.size > MAX_AVATAR_BYTES) {
          showInlineError(input, "image is too large — max 2 MB.");
          input.value = "";
          return;
        }
        if (!/^image\/(jpeg|png|webp|gif)$/i.test(file.type)) {
          showInlineError(input, "unsupported image type — use JPG, PNG, WEBP or GIF.");
          input.value = "";
          return;
        }
        showInlineError(input, null);
        if (!preview) return;
        var reader = new FileReader();
        reader.onload = function (evt) {
          preview.innerHTML = "";
          var img = document.createElement("img");
          img.src = evt.target.result;
          img.alt = "";
          preview.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    });
  }

  /* ----- Auto-hide flash messages ------------------------------------ */
  function initAutoFade() {
    if (prefersReducedMotion()) return;

    document.querySelectorAll("[data-autohide]").forEach(function (el) {
      var delay = parseInt(el.getAttribute("data-autohide"), 10) || 6000;
      var timer = null;

      function clear() {
        if (timer) {
          window.clearTimeout(timer);
          timer = null;
        }
      }

      function schedule() {
        clear();
        timer = window.setTimeout(function () {
          dismissAlert(el);
        }, delay);
      }

      el.addEventListener("mouseenter", clear);
      el.addEventListener("focusin", clear);
      el.addEventListener("mouseleave", schedule);
      el.addEventListener("focusout", function () {
        window.setTimeout(function () {
          if (!el.contains(document.activeElement)) schedule();
        }, 0);
      });
      schedule();
    });
  }

  /* ----- Form submit busy states -------------------------------------- */
  function initFormBusy() {
    document.addEventListener("submit", function (event) {
      var form = event.target;
      if (!form || form.tagName !== "FORM") return;
      if (form.getAttribute("data-no-busy") === "1") return;

      var submitter = event.submitter || form.querySelector("button[type=submit], input[type=submit]");
      if (!submitter || submitter.disabled) return;

      var keepLabel = submitter.classList.contains("dr-skill__btn");
      var label =
        form.getAttribute("data-busy-label") ||
        submitter.getAttribute("data-busy-label");
      if (!label) {
        if (form.hasAttribute("data-quiz-form") || form.querySelector(".dr-quiz-q")) {
          label = "grading…";
        } else if (form.closest(".dr-connect") || /connect|accept|decline|endorse|unendorse/i.test(form.getAttribute("action") || "")) {
          label = "sending…";
        } else {
          label = "saving…";
        }
      }

      submitter.setAttribute("aria-busy", "true");
      submitter.disabled = true;
      if (!keepLabel && submitter.tagName === "BUTTON") {
        if (!submitter.getAttribute("data-busy-original")) {
          submitter.setAttribute("data-busy-original", submitter.textContent);
        }
        submitter.textContent = label;
      }
    });
  }

  /* ----- Quiz progress HUD -------------------------------------------- */
  function initQuizProgress() {
    var form = document.querySelector("[data-quiz-form]");
    var hud = document.querySelector("[data-quiz-hud]");
    if (!form || !hud) return;

    var total = parseInt(hud.getAttribute("data-total"), 10) || 0;
    var bar = hud.querySelector("[data-quiz-bar]");
    var meta = hud.querySelector("[data-quiz-meta]");
    var groups = form.querySelectorAll(".dr-quiz-choices[role='radiogroup']");

    function answeredCount() {
      var n = 0;
      groups.forEach(function (group) {
        if (group.querySelector("input[type=radio]:checked")) n += 1;
      });
      return n;
    }

    function barGlyph(done, all) {
      var width = 10;
      if (!all) return "[" + "░".repeat(width) + "]";
      var filled = Math.round((done / all) * width);
      filled = Math.max(0, Math.min(width, filled));
      return "[" + "█".repeat(filled) + "░".repeat(width - filled) + "]";
    }

    function refresh() {
      var done = answeredCount();
      if (bar) bar.textContent = "progress " + barGlyph(done, total);
      if (meta) meta.textContent = "q " + done + "/" + total + " answered";
      hud.setAttribute("aria-valuenow", String(done));
    }

    form.addEventListener("change", refresh);
    refresh();

    form.addEventListener("submit", function (event) {
      var done = answeredCount();
      if (done >= total) return;
      var first = null;
      for (var i = 0; i < groups.length; i++) {
        if (!groups[i].querySelector("input[type=radio]:checked")) {
          first = groups[i].closest(".dr-quiz-q") || groups[i];
          break;
        }
      }
      if (first) {
        announce("Answer remaining questions before submitting (" + done + "/" + total + ").");
        try {
          first.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "center" });
        } catch (_) {
          first.scrollIntoView(true);
        }
      }
      // Let native `required` still fire; this soft-scrolls to the gap.
    });
  }

  /* ----- Connect popover Escape --------------------------------------- */
  function initConnect() {
    document.querySelectorAll("details.dr-connect").forEach(function (details) {
      details.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && details.open) {
          details.open = false;
          var summary = details.querySelector("summary");
          if (summary) summary.focus();
        }
      });
    });
  }

  /* ----- Sortable lists (drag to reorder, touch + mouse) -------------- */
  var DRAG_THRESHOLD_PX = 6;

  function csrfToken() {
    var input = document.querySelector("input[name=csrfmiddlewaretoken]");
    if (input && input.value) return input.value;
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function flashStatus(list, text, kind) {
    var slot =
      (list.parentNode && list.parentNode.querySelector("[data-sortable-status]")) ||
      document.querySelector("[data-sortable-status]");
    if (!slot) return;
    slot.textContent = text;
    slot.className = "dr-sortable__status" + (kind ? " is-" + kind : "");
    if (slot._timer) window.clearTimeout(slot._timer);
    slot._timer = window.setTimeout(function () {
      slot.textContent = "";
      slot.className = "dr-sortable__status";
    }, 2200);
  }

  function commitOrder(list) {
    var url = list.getAttribute("data-sortable-url");
    if (!url) return;
    var ids = Array.prototype.map.call(
      list.querySelectorAll("[data-sortable-item]"),
      function (el) { return parseInt(el.getAttribute("data-id"), 10); }
    ).filter(function (n) { return !isNaN(n); });
    list.setAttribute("data-saving", "");
    flashStatus(list, "saving…", null);
    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
      },
      body: JSON.stringify({ ids: ids })
    }).then(function (r) {
      list.removeAttribute("data-saving");
      if (r.ok) flashStatus(list, "order saved", "ok");
      else flashStatus(list, "save failed (" + r.status + ")", "err");
    }).catch(function () {
      list.removeAttribute("data-saving");
      flashStatus(list, "save failed", "err");
    });
  }

  function findInsertTarget(list, draggedItem, clientY) {
    var siblings = Array.prototype.filter.call(list.children, function (el) {
      return el !== draggedItem && el.hasAttribute && el.hasAttribute("data-sortable-item");
    });
    for (var i = 0; i < siblings.length; i++) {
      var rect = siblings[i].getBoundingClientRect();
      if (clientY < rect.top + rect.height / 2) return siblings[i];
    }
    return null; /* append to end */
  }

  function setupSortableItem(list, item) {
    var handle = item.querySelector("[data-sortable-handle]");
    if (!handle) return;

    handle.addEventListener("pointerdown", function (e) {
      // Mouse: only left button. Touch / pen: always.
      if (e.pointerType === "mouse" && e.button !== 0) return;
      startDrag(e, list, item, handle);
    });

    // Prevent the handle button from submitting any enclosing form.
    handle.addEventListener("click", function (e) { e.preventDefault(); });
  }

  function startDrag(e, list, item, handle) {
    e.preventDefault();
    var pointerId = e.pointerId;
    var rect = item.getBoundingClientRect();
    var offsetX = e.clientX - rect.left;
    var offsetY = e.clientY - rect.top;
    var startY = e.clientY;
    var startX = e.clientX;
    var dragging = false;

    var placeholder = document.createElement("li");
    placeholder.className = "dr-sortable__placeholder";
    placeholder.style.height = rect.height + "px";
    placeholder.style.margin = window.getComputedStyle(item).margin;

    var originalStyles = {
      position: item.style.position,
      top: item.style.top,
      left: item.style.left,
      width: item.style.width,
      zIndex: item.style.zIndex,
      pointerEvents: item.style.pointerEvents
    };

    function beginGhost() {
      dragging = true;
      item.classList.add("is-dragging");
      handle.style.cursor = "grabbing";
      item.style.position = "fixed";
      item.style.zIndex = "9999";
      item.style.width = rect.width + "px";
      item.style.left = (e.clientX - offsetX) + "px";
      item.style.top = (e.clientY - offsetY) + "px";
      item.style.pointerEvents = "none";
      if (item.nextSibling) {
        item.parentNode.insertBefore(placeholder, item.nextSibling);
      } else {
        item.parentNode.appendChild(placeholder);
      }
      try { handle.setPointerCapture(pointerId); } catch (_) {}
    }

    function onMove(ev) {
      if (ev.pointerId !== pointerId) return;
      if (!dragging) {
        var dx = Math.abs(ev.clientX - startX);
        var dy = Math.abs(ev.clientY - startY);
        if (Math.max(dx, dy) < DRAG_THRESHOLD_PX) return;
        beginGhost();
      }
      ev.preventDefault();
      item.style.left = (ev.clientX - offsetX) + "px";
      item.style.top = (ev.clientY - offsetY) + "px";

      var target = findInsertTarget(list, item, ev.clientY);
      if (target) list.insertBefore(placeholder, target);
      else list.appendChild(placeholder);
    }

    function cleanupItem() {
      item.style.position = originalStyles.position;
      item.style.top = originalStyles.top;
      item.style.left = originalStyles.left;
      item.style.width = originalStyles.width;
      item.style.zIndex = originalStyles.zIndex;
      item.style.pointerEvents = originalStyles.pointerEvents;
      item.classList.remove("is-dragging");
      handle.style.cursor = "";
    }

    function onUp(ev) {
      if (ev.pointerId !== pointerId) return;
      document.removeEventListener("pointermove", onMove);
      document.removeEventListener("pointerup", onUp);
      document.removeEventListener("pointercancel", onUp);
      try { handle.releasePointerCapture(pointerId); } catch (_) {}

      if (!dragging) return;

      if (placeholder.parentNode) {
        placeholder.parentNode.insertBefore(item, placeholder);
        placeholder.parentNode.removeChild(placeholder);
      }
      cleanupItem();
      commitOrder(list);
    }

    document.addEventListener("pointermove", onMove, { passive: false });
    document.addEventListener("pointerup", onUp);
    document.addEventListener("pointercancel", onUp);
  }

  function initSortable() {
    document.querySelectorAll("[data-sortable]").forEach(function (list) {
      list.querySelectorAll("[data-sortable-item]").forEach(function (item) {
        setupSortableItem(list, item);
      });
    });
  }

  // ---- Outbound link-click tracking (beacon) --------------------------------

  function initLinkTracking() {
    var scope = document.querySelector("[data-track-scope]");
    if (!scope) {
      return;
    }
    var url = scope.getAttribute("data-track-url");
    var handle = scope.getAttribute("data-track-handle");
    if (!url || !handle) {
      return;
    }

    function send(el) {
      var kind = el.getAttribute("data-track-kind");
      if (!kind) {
        return;
      }
      var payload = { handle: handle, kind: kind };
      var id = el.getAttribute("data-track-id");
      if (id) {
        payload.id = parseInt(id, 10);
      }
      var field = el.getAttribute("data-track-field");
      if (field) {
        payload.field = field;
      }
      var body = JSON.stringify(payload);
      // sendBeacon survives the page navigation that the click triggers.
      try {
        if (navigator.sendBeacon) {
          var blob = new Blob([body], { type: "application/json" });
          if (navigator.sendBeacon(url, blob)) {
            return;
          }
        }
      } catch (err) {
        /* fall through to fetch */
      }
      try {
        fetch(url, {
          method: "POST",
          body: body,
          keepalive: true,
          credentials: "omit",
          headers: { "Content-Type": "application/json" },
        });
      } catch (err) {
        /* tracking is best-effort */
      }
    }

    function onActivate(event) {
      var el = event.target.closest("[data-track-kind]");
      if (el && scope.contains(el)) {
        send(el);
      }
    }

    scope.addEventListener("click", onActivate);
    scope.addEventListener("auxclick", function (event) {
      if (event.button === 1) {
        onActivate(event);
      }
    });
  }

  function initAnalyticsChart() {
    var chart = document.querySelector("[data-analytics-chart]");
    var readout = document.querySelector("[data-chart-readout]");
    if (!chart || !readout) return;

    var cols = Array.prototype.slice.call(chart.querySelectorAll("[data-chart-day]"));
    var idle = readout.textContent;
    var pinned = null;

    function setReadout(col) {
      var label = col.getAttribute("data-label") || "";
      var views = col.getAttribute("data-views") || "0";
      var uniques = col.getAttribute("data-uniques") || "0";
      var share = col.getAttribute("data-share") || "0";
      var strong = document.createElement("strong");
      strong.textContent = label;
      readout.replaceChildren();
      readout.appendChild(strong);
      readout.appendChild(
        document.createTextNode(" · " + views + " views · " + uniques + " unique")
      );
      if (share && share !== "0") {
        readout.appendChild(document.createTextNode(" · " + share + "% of window"));
      }
      readout.setAttribute("data-active", "1");
    }

    function paintPressed(active) {
      cols.forEach(function (c) {
        c.setAttribute("aria-pressed", c === active ? "true" : "false");
      });
    }

    function activate(col, pin) {
      if (pin) pinned = col;
      paintPressed(col);
      setReadout(col);
    }

    function clear(force) {
      if (!force && pinned) {
        paintPressed(pinned);
        setReadout(pinned);
        return;
      }
      pinned = null;
      paintPressed(null);
      readout.textContent = idle;
      readout.setAttribute("data-active", "0");
    }

    cols.forEach(function (col) {
      col.addEventListener("mouseenter", function () { activate(col, false); });
      col.addEventListener("focus", function () { activate(col, false); });
      col.addEventListener("click", function (event) {
        event.preventDefault();
        if (pinned === col) {
          clear(true);
          return;
        }
        activate(col, true);
      });
    });

    chart.addEventListener("mouseleave", function () {
      if (!chart.querySelector("[data-chart-day]:focus")) clear(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") clear(true);
    });

    document.addEventListener("click", function (event) {
      if (!chart.contains(event.target) && !readout.contains(event.target)) {
        clear(true);
      }
    });
  }

  function initPasswordPeek() {
    var showLabel = "show";
    var hideLabel = "hide";
    var showAria = "Show password";
    var hideAria = "Hide password";

    function bindToggle(btn) {
      if (btn.getAttribute("data-bound") === "1") return;
      btn.setAttribute("data-bound", "1");
      btn.addEventListener("click", function () {
        var wrap = btn.closest(".dr-password");
        var input = (wrap && wrap.querySelector("input")) || null;
        if (!input) {
          var controls = btn.getAttribute("aria-controls");
          if (controls) input = document.getElementById(controls);
        }
        if (!input) return;

        var revealing = input.type === "password";
        input.type = revealing ? "text" : "password";
        btn.setAttribute("aria-pressed", revealing ? "true" : "false");
        btn.setAttribute("aria-label", revealing ? hideAria : showAria);
        var label = btn.querySelector("[data-password-label]");
        if (label) label.textContent = revealing ? hideLabel : showLabel;
      });
    }

    document.querySelectorAll("[data-password-toggle]").forEach(bindToggle);

    document.querySelectorAll('input[type="password"]').forEach(function (input) {
      if (input.closest(".dr-password") || input.hasAttribute("data-no-peek")) return;
      if (input.disabled || input.readOnly) return;

      var wrap = document.createElement("div");
      wrap.className = "dr-password";
      input.parentNode.insertBefore(wrap, input);
      wrap.appendChild(input);
      input.classList.add("dr-input", "dr-password__input");
      input.setAttribute("data-password-input", "");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "dr-password__toggle";
      btn.setAttribute("data-password-toggle", "");
      btn.setAttribute("aria-pressed", "false");
      btn.setAttribute("aria-label", showAria);
      if (input.id) btn.setAttribute("aria-controls", input.id);

      var icon = document.createElement("span");
      icon.className = "dr-password__icon";
      icon.setAttribute("aria-hidden", "true");
      var label = document.createElement("span");
      label.setAttribute("data-password-label", "");
      label.textContent = showLabel;
      btn.appendChild(icon);
      btn.appendChild(label);
      wrap.appendChild(btn);
      bindToggle(btn);
    });
  }

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    bindThemeToggles();
    initNav();
    initAlerts();
    initCopyButtons();
    initPasswordPeek();
    initAvatarPreview();
    initAutoFade();
    initSortable();
    initLinkTracking();
    initAnalyticsChart();
    initFormBusy();
    initQuizProgress();
    initConnect();
  });
})();
