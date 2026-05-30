/* DevResurge — theme toggle + mobile nav. No external deps. */
(function () {
  "use strict";

  var STORAGE_KEY = "devresurge:theme";

  function preferred() {
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

  // Hydrate immediately so first paint matches preference.
  applyTheme(preferred());

  function toggleTheme() {
    var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch (_) {}
    applyTheme(next);
  }

  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu = document.querySelector("[data-nav-menu]");
    if (!toggle || !menu) return;
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (event) {
      if (!menu.classList.contains("is-open")) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  }

  function bindThemeToggles() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", toggleTheme);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bindThemeToggles();
      initNav();
    });
  } else {
    bindThemeToggles();
    initNav();
  }
})();
