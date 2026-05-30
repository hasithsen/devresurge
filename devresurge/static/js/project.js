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
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu = document.querySelector("[data-nav-menu]");
    if (!toggle || !menu) return;

    function close() {
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (event) {
      if (!menu.classList.contains("is-open")) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      close();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });
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
  });
})();
