/* DevResurge — theme toggle + mobile nav + alert dismiss + copy-to-clipboard.
 * Vanilla JS, no external deps. Safe to load with `defer`. */
(function () {
  "use strict";

  var STORAGE_KEY = "devresurge:theme";

  /* ----- Theme ---------------------------------------------------------- */
  function preferredTheme() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "light" || stored === "dark") return stored;
    } catch (_) {}
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
      return "light";
    }
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

  /* ----- Mobile nav ---------------------------------------------------- */
  function initNav() {
    var nav = document.querySelector(".dr-nav");
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu = document.querySelector("[data-nav-menu]");
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

    function close() {
      if (!menu.classList.contains("is-open")) return;
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("dr-nav-open");
    }

    function open() {
      measure();
      menu.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("dr-nav-open");
    }

    toggle.addEventListener("click", function (event) {
      event.stopPropagation();
      if (menu.classList.contains("is-open")) close();
      else open();
    });

    document.addEventListener("click", function (event) {
      if (!menu.classList.contains("is-open")) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      close();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        close();
        toggle.focus();
      }
    });

    // Auto-close when navigating to a menu link (esp. anchor links on the same
    // page — otherwise the open menu would sit on top of the new section).
    menu.addEventListener("click", function (event) {
      var target = event.target.closest("a");
      if (target) close();
    });

    // If the viewport grows past mobile, ensure the menu state is clean.
    var mql = window.matchMedia("(min-width: 721px)");
    var onMq = function (e) { if (e.matches) close(); };
    if (mql.addEventListener) mql.addEventListener("change", onMq);
    else if (mql.addListener) mql.addListener(onMq);
  }

  /* ----- Dismissible alerts ------------------------------------------- */
  function initAlerts() {
    document.querySelectorAll("[data-dismiss-alert]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = btn.closest(".dr-alert");
        if (!target) return;
        target.style.transition = "opacity 160ms ease, transform 160ms ease";
        target.style.opacity = "0";
        target.style.transform = "translateY(-4px)";
        window.setTimeout(function () {
          if (target.parentNode) target.parentNode.removeChild(target);
        }, 180);
      });
    });
  }

  /* ----- Copy-to-clipboard -------------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    // Fallback for old browsers / http
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
    // Match either an explicit `data-copy` value or a `data-copy-from` selector.
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
    document.querySelectorAll("[data-autohide]").forEach(function (el) {
      var delay = parseInt(el.getAttribute("data-autohide"), 10) || 6000;
      window.setTimeout(function () {
        el.style.transition = "opacity 200ms ease";
        el.style.opacity = "0";
        window.setTimeout(function () {
          if (el.parentNode) el.parentNode.removeChild(el);
        }, 220);
      }, delay);
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
    initAvatarPreview();
    initAutoFade();
    initSortable();
    initLinkTracking();
    initAnalyticsChart();
  });
})();
