/* DevResurge — universal search typeahead.
 * Debounced fetch, keyboard nav, abortable requests. No deps. */
(function () {
  "use strict";

  var MIN_LEN = 2;
  var DEBOUNCE_MS = 180;
  var MAX_SHOW = 12;

  function scriptEl() {
    return document.querySelector("script[data-search-api]");
  }

  function apiUrl() {
    var s = scriptEl();
    return (s && s.getAttribute("data-search-api")) || "/search/api/";
  }

  function pageUrl() {
    var s = scriptEl();
    return (s && s.getAttribute("data-search-page")) || "/search/";
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function initUniversalSearch() {
    var root = document.querySelector("[data-universal-search]");
    if (!root) return;
    var input = root.querySelector("[data-search-input]");
    var panel = root.querySelector("[data-search-panel]");
    var form = root.querySelector("[data-search-form]");
    if (!input || !panel || !form) return;

    var timer = null;
    var controller = null;
    var active = -1;
    var items = [];

    function close() {
      panel.hidden = true;
      panel.innerHTML = "";
      input.setAttribute("aria-expanded", "false");
      active = -1;
      items = [];
      if (controller) {
        controller.abort();
        controller = null;
      }
    }

    function setActive(idx) {
      active = idx;
      var nodes = panel.querySelectorAll("[data-search-option]");
      nodes.forEach(function (node, i) {
        var on = i === idx;
        node.classList.toggle("is-active", on);
        if (on) node.setAttribute("aria-selected", "true");
        else node.removeAttribute("aria-selected");
      });
      if (idx >= 0 && nodes[idx]) {
        nodes[idx].scrollIntoView({ block: "nearest" });
      }
    }

    function render(payload) {
      var results = (payload && payload.results) || [];
      items = results.slice(0, MAX_SHOW);
      if (!items.length) {
        panel.innerHTML =
          '<div class="dr-nav-search__empty" role="option">no matches</div>';
        panel.hidden = false;
        input.setAttribute("aria-expanded", "true");
        active = -1;
        return;
      }
      var html = items
        .map(function (hit, i) {
          return (
            '<a class="dr-nav-search__option" role="option" id="dr-sopt-' +
            i +
            '" href="' +
            escapeHtml(hit.url) +
            '" data-search-option data-idx="' +
            i +
            '">' +
            '<span class="dr-nav-search__type">' +
            escapeHtml(hit.type) +
            "</span>" +
            '<span class="dr-nav-search__title">' +
            escapeHtml(hit.title) +
            "</span>" +
            (hit.subtitle
              ? '<span class="dr-nav-search__sub">' +
                escapeHtml(hit.subtitle) +
                "</span>"
              : "") +
            "</a>"
          );
        })
        .join("");
      html +=
        '<a class="dr-nav-search__more" href="' +
        escapeHtml(pageUrl() + "?q=" + encodeURIComponent(payload.query || input.value)) +
        '">view all results →</a>';
      panel.innerHTML = html;
      panel.hidden = false;
      input.setAttribute("aria-expanded", "true");
      active = -1;
    }

    function fetchSuggest(q) {
      if (controller) controller.abort();
      controller = new AbortController();
      var url = apiUrl() + "?q=" + encodeURIComponent(q) + "&limit=4";
      fetch(url, {
        signal: controller.signal,
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      })
        .then(function (res) {
          if (res.status === 429) {
            panel.innerHTML =
              '<div class="dr-nav-search__empty">slow down — try again shortly</div>';
            panel.hidden = false;
            return null;
          }
          if (!res.ok) throw new Error("search failed");
          return res.json();
        })
        .then(function (data) {
          if (data) render(data);
        })
        .catch(function (err) {
          if (err && err.name === "AbortError") return;
          close();
        });
    }

    function onInput() {
      var q = (input.value || "").trim();
      window.clearTimeout(timer);
      if (q.length < MIN_LEN) {
        close();
        return;
      }
      timer = window.setTimeout(function () {
        fetchSuggest(q);
      }, DEBOUNCE_MS);
    }

    input.addEventListener("input", onInput);
    input.addEventListener("focus", function () {
      if ((input.value || "").trim().length >= MIN_LEN && panel.innerHTML) {
        panel.hidden = false;
        input.setAttribute("aria-expanded", "true");
      }
    });

    input.addEventListener("keydown", function (ev) {
      var open = !panel.hidden;
      if (ev.key === "Escape") {
        close();
        input.blur();
        return;
      }
      if (ev.key === "ArrowDown" && open) {
        ev.preventDefault();
        setActive(Math.min(active + 1, items.length - 1));
        return;
      }
      if (ev.key === "ArrowUp" && open) {
        ev.preventDefault();
        setActive(Math.max(active - 1, 0));
        return;
      }
      if (ev.key === "Enter" && open && active >= 0 && items[active]) {
        ev.preventDefault();
        window.location.href = items[active].url;
      }
    });

    document.addEventListener("click", function (ev) {
      if (!root.contains(ev.target)) close();
    });

    /* Focus search with "/" when not typing in an input */
    document.addEventListener("keydown", function (ev) {
      if (ev.key !== "/" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
      var tag = (ev.target && ev.target.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (ev.target && ev.target.isContentEditable) return;
      ev.preventDefault();
      input.focus();
      input.select();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initUniversalSearch);
  } else {
    initUniversalSearch();
  }
})();
