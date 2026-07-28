/* DevResurge — interactive force-directed network map.
 * Vanilla Canvas 2D; no external deps. Expects #dr-network-graph-data (json_script)
 * and/or [data-network-map][data-map-src] for a live JSON refresh. */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function cssVar(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  function readEmbeddedGraph() {
    var el = document.getElementById("dr-network-graph-data");
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (_) {
      return null;
    }
  }

  function isCoarsePointer() {
    return window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
  }

  function NetworkMap(canvas, graph) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.graph = graph || { nodes: [], edges: [], me_id: null, stats: {} };
    this.nodes = [];
    this.edges = [];
    this.nodeById = {};
    this.scale = 1;
    this.tx = 0;
    this.ty = 0;
    this.running = true;
    this.dragNode = null;
    this.pan = null;
    this.hover = null;
    this.relationFilter = "";
    this.intentFilters = [];
    this.showMutual = true;
    this.raf = 0;
    this.pointers = new Map();
    this.pinch = null;
    this.gesture = null;
    this.tooltip = document.querySelector("[data-map-tooltip]");
    this.sheet = document.querySelector("[data-map-sheet]");
    this.status = document.querySelector("[data-map-status]");
    this.emptyMsg = canvas.getAttribute("data-map-empty") || "No connections yet.";
    this.dataSrc = canvas.getAttribute("data-map-src") || "";
    this.coarse = isCoarsePointer();

    this._bindUI();
    this._syncControlsOpen();
    this._loadGraph(this.graph);
    this._resize();
    this._fit(true);
    this._loop();

    window.addEventListener("resize", this._onResizeBound(this), { passive: true });
    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", this._onResize.bind(this), { passive: true });
    }
    if (typeof ResizeObserver !== "undefined") {
      var self = this;
      this._ro = new ResizeObserver(function () { self._onResize(); });
      this._ro.observe(this.canvas.parentElement);
    }
  }

  NetworkMap.prototype._syncControlsOpen = function () {
    /* Sidebar is a fixed aside with its own scroll region — nothing to sync. */
  };

  NetworkMap.prototype._bindUI = function () {
    var self = this;
    var filter = document.querySelector("[data-map-filter]");
    if (filter) {
      filter.addEventListener("change", function () {
        self.relationFilter = filter.value || "";
        self._draw();
      });
    }
    var mutual = document.querySelector("[data-map-mutual]");
    if (mutual) {
      this.showMutual = mutual.checked;
      mutual.addEventListener("change", function () {
        self.showMutual = mutual.checked;
        self._reloadGraph({ mutual: self.showMutual ? "1" : "0" });
      });
    }

    document.querySelectorAll("[data-map-intent]").forEach(function (box) {
      box.addEventListener("change", function () {
        self.intentFilters = Array.prototype.slice
          .call(document.querySelectorAll("[data-map-intent]:checked"))
          .map(function (el) { return el.getAttribute("data-map-intent"); })
          .filter(Boolean);
        self._draw();
      });
    });
    var fitBtn = document.querySelector("[data-map-fit]");
    if (fitBtn) fitBtn.addEventListener("click", function () { self._fit(false); });
    var pauseBtn = document.querySelector("[data-map-pause]");
    if (pauseBtn) {
      pauseBtn.addEventListener("click", function () {
        self.running = !self.running;
        pauseBtn.textContent = self.running ? "pause" : "resume";
        if (self.status) self.status.textContent = self.running ? "sim" : "paused";
        if (self.running) self._loop();
      });
    }
    var zin = document.querySelector("[data-map-zoom-in]");
    var zout = document.querySelector("[data-map-zoom-out]");
    if (zin) zin.addEventListener("click", function () { self._zoomAt(1.18); });
    if (zout) zout.addEventListener("click", function () { self._zoomAt(0.85); });

    var sheetClose = document.querySelector("[data-map-sheet-close]");
    if (sheetClose) sheetClose.addEventListener("click", function () { self._hideSheet(); });

    document.querySelectorAll("[data-map-focus]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = parseInt(btn.getAttribute("data-map-focus"), 10);
        self._focusNode(id);
        if (self.coarse) {
          var node = self.nodeById[id];
          if (node) self._showSheet(node);
        }
      });
      btn.addEventListener("dblclick", function () {
        var url = btn.getAttribute("data-map-url");
        if (url) window.location.href = url;
      });
    });

    canvasEvents(this);
  };

  NetworkMap.prototype._reloadGraph = function (params) {
    var self = this;
    if (!this.dataSrc) {
      this._draw();
      return;
    }
    var url;
    try {
      url = new URL(this.dataSrc, window.location.origin);
    } catch (_) {
      this._draw();
      return;
    }
    Object.keys(params || {}).forEach(function (key) {
      url.searchParams.set(key, params[key]);
    });
    this.dataSrc = url.pathname + url.search;
    this.canvas.setAttribute("data-map-src", this.dataSrc);
    if (this.status) this.status.textContent = "load";
    fetch(url.toString(), { credentials: "same-origin", headers: { Accept: "application/json" } })
      .then(function (res) {
        if (!res.ok) throw new Error("map fetch failed");
        return res.json();
      })
      .then(function (graph) {
        var keepRunning = self.running;
        self._loadGraph(graph);
        self._fit(true);
        if (self.status) self.status.textContent = keepRunning ? "sim" : "paused";
        self._draw();
        if (keepRunning && !self.raf) self._loop();
        try {
          var page = new URL(window.location.href);
          page.searchParams.set("mutual", self.showMutual ? "1" : "0");
          window.history.replaceState({}, "", page.pathname + page.search);
        } catch (_) { /* ignore */ }
      })
      .catch(function () {
        if (self.status) self.status.textContent = "err";
        self._draw();
      });
  };

  NetworkMap.prototype._zoomAt = function (factor, sx, sy) {
    var mx = sx == null ? this.width / 2 : sx;
    var my = sy == null ? this.height / 2 : sy;
    var before = this._screenToWorld(mx, my);
    this.scale = Math.min(3.5, Math.max(0.35, this.scale * factor));
    var after = this._screenToWorld(mx, my);
    this.tx += (after.x - before.x) * this.scale;
    this.ty += (after.y - before.y) * this.scale;
    this._draw();
  };

  function canvasEvents(map) {
    var c = map.canvas;

    c.addEventListener("wheel", function (e) {
      e.preventDefault();
      var rect = c.getBoundingClientRect();
      var mx = e.clientX - rect.left;
      var my = e.clientY - rect.top;
      map._zoomAt(e.deltaY < 0 ? 1.08 : 0.92, mx, my);
    }, { passive: false });

    c.addEventListener("pointerdown", function (e) {
      map.coarse = isCoarsePointer();
      map.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      try { c.setPointerCapture(e.pointerId); } catch (_) {}

      if (map.pointers.size === 2) {
        map.dragNode = null;
        map.pan = null;
        var pts = Array.from(map.pointers.values());
        var dx = pts[1].x - pts[0].x;
        var dy = pts[1].y - pts[0].y;
        map.pinch = {
          dist: Math.sqrt(dx * dx + dy * dy) || 1,
          scale: map.scale,
          cx: (pts[0].x + pts[1].x) / 2,
          cy: (pts[0].y + pts[1].y) / 2,
        };
        map.gesture = null;
        return;
      }

      var p = map._eventWorld(e);
      var hit = map._hitTest(p.x, p.y);
      map.gesture = {
        hit: hit,
        startX: e.clientX,
        startY: e.clientY,
        moved: false,
        started: Date.now(),
      };
      if (hit) {
        map.dragNode = hit;
        hit.fx = hit.x;
        hit.fy = hit.y;
        map.running = true;
        if (map.status) map.status.textContent = "sim";
      } else {
        map.pan = { x: e.clientX, y: e.clientY, tx: map.tx, ty: map.ty };
      }
    });

    c.addEventListener("pointermove", function (e) {
      if (map.pointers.has(e.pointerId)) {
        map.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      }

      if (map.pinch && map.pointers.size >= 2) {
        var pts = Array.from(map.pointers.values());
        var dx = pts[1].x - pts[0].x;
        var dy = pts[1].y - pts[0].y;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
        var rect = c.getBoundingClientRect();
        var mx = map.pinch.cx - rect.left;
        var my = map.pinch.cy - rect.top;
        var factor = dist / map.pinch.dist;
        var before = map._screenToWorld(mx, my);
        map.scale = Math.min(3.5, Math.max(0.35, map.pinch.scale * factor));
        var after = map._screenToWorld(mx, my);
        map.tx += (after.x - before.x) * map.scale;
        map.ty += (after.y - before.y) * map.scale;
        map._draw();
        return;
      }

      if (map.gesture) {
        var gdx = e.clientX - map.gesture.startX;
        var gdy = e.clientY - map.gesture.startY;
        if ((gdx * gdx + gdy * gdy) > 64) map.gesture.moved = true;
      }

      if (map.dragNode) {
        var p = map._eventWorld(e);
        map.dragNode.fx = p.x;
        map.dragNode.fy = p.y;
        map.dragNode.x = p.x;
        map.dragNode.y = p.y;
        map._draw();
        if (!map.coarse) map._showTooltip(map.dragNode, e);
        return;
      }
      if (map.pan) {
        map.tx = map.pan.tx + (e.clientX - map.pan.x);
        map.ty = map.pan.ty + (e.clientY - map.pan.y);
        map._draw();
        return;
      }
      if (map.coarse) return;
      var w = map._eventWorld(e);
      var hover = map._hitTest(w.x, w.y);
      if (hover !== map.hover) {
        map.hover = hover;
        map._draw();
      }
      if (hover) map._showTooltip(hover, e);
      else map._hideTooltip();
      c.style.cursor = hover ? "pointer" : "grab";
    });

    function endPointer(e) {
      map.pointers.delete(e.pointerId);
      if (map.pointers.size < 2) map.pinch = null;

      var gesture = map.gesture;
      var hit = map.dragNode || (gesture && gesture.hit);
      var wasTap = gesture && !gesture.moved && (Date.now() - gesture.started) < 450;

      if (map.dragNode) {
        map.dragNode.fx = null;
        map.dragNode.fy = null;
        map.dragNode = null;
      }
      map.pan = null;
      map.gesture = null;
      try { c.releasePointerCapture(e.pointerId); } catch (_) {}

      if (wasTap && hit) {
        map.hover = hit;
        map._draw();
        if (map.coarse) {
          map._hideTooltip();
          map._showSheet(hit);
        } else {
          map._showTooltip(hit, e);
        }
      }
    }
    c.addEventListener("pointerup", endPointer);
    c.addEventListener("pointercancel", endPointer);

    c.addEventListener("dblclick", function (e) {
      if (map.coarse) return;
      var w = map._eventWorld(e);
      var hit = map._hitTest(w.x, w.y);
      if (hit && hit.url) window.location.href = hit.url;
    });
  }

  NetworkMap.prototype._loadGraph = function (graph) {
    this.graph = graph || { nodes: [], edges: [], me_id: null };
    this.nodeById = {};
    var coarse = this.coarse;
    this.nodes = (graph.nodes || []).map(function (n, i) {
      var angle = (i / Math.max(graph.nodes.length, 1)) * Math.PI * 2;
      var radius = n.is_self ? 0 : 160 + (i % 5) * 18;
      var node = {
        id: n.id,
        handle: n.handle,
        name: n.name,
        initials: n.initials || "?",
        role: n.role || "",
        location: n.location || "",
        avatar: n.avatar || "",
        url: n.url || "",
        open_to_work: !!n.open_to_work,
        open_to_collaborate: !!n.open_to_collaborate,
        open_to_mentor: !!n.open_to_mentor,
        open_to_learning: !!n.open_to_learning,
        intents: Array.isArray(n.intents) ? n.intents.slice() : [],
        is_self: !!n.is_self,
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        vx: 0,
        vy: 0,
        fx: null,
        fy: null,
        r: n.is_self ? (coarse ? 26 : 22) : (coarse ? 20 : 16),
        img: null,
      };
      if (n.avatar) {
        var img = new Image();
        img.crossOrigin = "anonymous";
        img.src = n.avatar;
        node.img = img;
      }
      return node;
    });
    var self = this;
    this.nodes.forEach(function (n) { self.nodeById[n.id] = n; });
    this.edges = (graph.edges || []).map(function (e) {
      return {
        source: e.source,
        target: e.target,
        relation: e.relation,
        label: e.label,
        kind: e.kind || "direct",
      };
    });
  };

  NetworkMap.prototype._onResize = function () {
    this._resize();
    this._draw();
  };

  NetworkMap.prototype._resize = function () {
    var wrap = this.canvas.parentElement;
    var w = Math.max(280, wrap.clientWidth || 320);
    var h = Math.max(240, wrap.clientHeight || 320);
    var dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    this.canvas.width = Math.floor(w * dpr);
    this.canvas.height = Math.floor(h * dpr);
    this.canvas.style.width = w + "px";
    this.canvas.style.height = h + "px";
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.width = w;
    this.height = h;
  };

  NetworkMap.prototype._screenToWorld = function (sx, sy) {
    return {
      x: (sx - this.width / 2 - this.tx) / this.scale,
      y: (sy - this.height / 2 - this.ty) / this.scale,
    };
  };

  NetworkMap.prototype._eventWorld = function (e) {
    var rect = this.canvas.getBoundingClientRect();
    return this._screenToWorld(e.clientX - rect.left, e.clientY - rect.top);
  };

  NetworkMap.prototype._hitTest = function (x, y) {
    var pad = this.coarse ? 16 : 4;
    for (var i = this.nodes.length - 1; i >= 0; i--) {
      var n = this.nodes[i];
      var dx = n.x - x;
      var dy = n.y - y;
      var r = n.r + pad;
      if (dx * dx + dy * dy <= r * r) return n;
    }
    return null;
  };

  NetworkMap.prototype._nodeMatchesIntent = function (node) {
    if (!this.intentFilters.length) return true;
    if (node.is_self) return true;
    var intents = node.intents || [];
    for (var i = 0; i < this.intentFilters.length; i++) {
      if (intents.indexOf(this.intentFilters[i]) !== -1) return true;
    }
    return false;
  };

  NetworkMap.prototype._relationColor = function (relation, accent, warn, muted) {
    switch (relation) {
      case "collaborator":
        return cssVar("--link", accent);
      case "mentor":
      case "mentee":
        return warn;
      case "recruiter":
      case "hiring":
        return cssVar("--accent-strong", warn);
      case "friend":
        return muted;
      default:
        return accent;
    }
  };

  NetworkMap.prototype._visibleEdges = function () {
    var self = this;
    return this.edges.filter(function (e) {
      if (!self.showMutual && e.kind === "mutual") return false;
      if (!self.relationFilter) return true;
      if (e.kind === "mutual") return true;
      return e.relation === self.relationFilter;
    });
  };

  NetworkMap.prototype._visibleNodeIds = function (edges) {
    var ids = {};
    var me = this.graph.me_id;
    if (me != null) ids[me] = true;
    if (!this.relationFilter) {
      this.nodes.forEach(function (n) { ids[n.id] = true; });
      return ids;
    }
    edges.forEach(function (e) {
      if (e.kind === "direct" && e.relation === this.relationFilter) {
        ids[e.source] = true;
        ids[e.target] = true;
      }
    }, this);
    return ids;
  };

  NetworkMap.prototype._tick = function () {
    var nodes = this.nodes;
    var edges = this._visibleEdges();
    var i, j, a, b, dx, dy, dist, f;

    // Repulsion
    for (i = 0; i < nodes.length; i++) {
      for (j = i + 1; j < nodes.length; j++) {
        a = nodes[i];
        b = nodes[j];
        dx = b.x - a.x;
        dy = b.y - a.y;
        dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        f = 2800 / (dist * dist);
        dx = (dx / dist) * f;
        dy = (dy / dist) * f;
        if (a.fx == null) { a.vx -= dx; a.vy -= dy; }
        if (b.fx == null) { b.vx += dx; b.vy += dy; }
      }
    }

    // Springs
    for (i = 0; i < edges.length; i++) {
      var e = edges[i];
      a = this.nodeById[e.source];
      b = this.nodeById[e.target];
      if (!a || !b) continue;
      dx = b.x - a.x;
      dy = b.y - a.y;
      dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      var ideal = e.kind === "mutual" ? 140 : 110;
      f = (dist - ideal) * 0.035;
      dx = (dx / dist) * f;
      dy = (dy / dist) * f;
      if (a.fx == null) { a.vx += dx; a.vy += dy; }
      if (b.fx == null) { b.vx -= dx; b.vy -= dy; }
    }

    // Center pull (ego slightly stronger)
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      if (a.fx != null) {
        a.x = a.fx;
        a.y = a.fy;
        a.vx = 0;
        a.vy = 0;
        continue;
      }
      var pull = a.is_self ? 0.02 : 0.004;
      a.vx += -a.x * pull;
      a.vy += -a.y * pull;
      a.vx *= 0.86;
      a.vy *= 0.86;
      a.x += a.vx;
      a.y += a.vy;
    }
  };

  NetworkMap.prototype._loop = function () {
    var self = this;
    if (!this.running) return;
    this._tick();
    this._draw();
    this.raf = requestAnimationFrame(function () { self._loop(); });
  };

  NetworkMap.prototype._draw = function () {
    var ctx = this.ctx;
    var w = this.width;
    var h = this.height;
    ctx.clearRect(0, 0, w, h);

    // Atmosphere
    var bg = cssVar("--bg-elev", "#11181a");
    var grid = cssVar("--grid", "rgba(124,240,168,0.06)");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);
    ctx.save();
    ctx.translate(w / 2 + this.tx, h / 2 + this.ty);
    ctx.scale(this.scale, this.scale);

    // Grid
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1 / this.scale;
    var step = 40;
    for (var gx = -400; gx <= 400; gx += step) {
      ctx.beginPath(); ctx.moveTo(gx, -400); ctx.lineTo(gx, 400); ctx.stroke();
    }
    for (var gy = -400; gy <= 400; gy += step) {
      ctx.beginPath(); ctx.moveTo(-400, gy); ctx.lineTo(400, gy); ctx.stroke();
    }

    var edges = this._visibleEdges();
    var visible = this._visibleNodeIds(edges);
    var accent = cssVar("--accent", "#7cf0a8");
    var muted = cssVar("--text-dim", "#4f5d59");
    var text = cssVar("--text", "#d8e8df");
    var border = cssVar("--border-strong", "#2d3f44");
    var warn = cssVar("--warn", "#ffb86b");

    // Edges
    for (var i = 0; i < edges.length; i++) {
      var e = edges[i];
      var a = this.nodeById[e.source];
      var b = this.nodeById[e.target];
      if (!a || !b) continue;
      if (!visible[a.id] || !visible[b.id]) continue;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      if (e.kind === "mutual") {
        ctx.setLineDash([6 / this.scale, 5 / this.scale]);
        ctx.strokeStyle = muted;
        ctx.globalAlpha = 0.55;
      } else {
        ctx.setLineDash([]);
        ctx.strokeStyle = this._relationColor(e.relation, accent, warn, muted);
        ctx.globalAlpha = 0.8;
      }
      ctx.lineWidth = (e.kind === "mutual" ? 1.2 : 1.8) / this.scale;
      ctx.stroke();
      ctx.globalAlpha = 1;
      ctx.setLineDash([]);
    }

    // Nodes
    for (var n = 0; n < this.nodes.length; n++) {
      var node = this.nodes[n];
      if (!visible[node.id] && !node.is_self) continue;
      var intentOk = this._nodeMatchesIntent(node);
      var isHover = this.hover === node;
      var r = node.r + (isHover ? 3 : 0);
      var ring = accent;
      if (!node.is_self) {
        if (node.open_to_work) ring = warn;
        else if (node.open_to_collaborate) ring = cssVar("--link", accent);
        else if (node.open_to_mentor || node.open_to_learning) ring = cssVar("--accent-strong", warn);
      }

      ctx.globalAlpha = intentOk ? 1 : 0.18;

      ctx.beginPath();
      ctx.arc(node.x, node.y, r + 3, 0, Math.PI * 2);
      ctx.fillStyle = node.is_self ? accent : ring;
      ctx.globalAlpha = intentOk ? 0.25 : 0.08;
      ctx.fill();
      ctx.globalAlpha = intentOk ? 1 : 0.18;

      ctx.beginPath();
      ctx.arc(node.x, node.y, r, 0, Math.PI * 2);
      ctx.fillStyle = cssVar("--bg", "#0b0f0d");
      ctx.fill();
      ctx.lineWidth = 2 / this.scale;
      ctx.strokeStyle = node.is_self ? accent : ring;
      ctx.stroke();

      if (node.img && node.img.complete && node.img.naturalWidth) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(node.x, node.y, r - 1.5, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(node.img, node.x - r, node.y - r, r * 2, r * 2);
        ctx.restore();
      } else {
        ctx.fillStyle = text;
        ctx.font = "600 " + Math.round(r * 0.7) + "px " + cssVar("--font-mono", "monospace");
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.initials.slice(0, 2), node.x, node.y + 0.5);
      }

      ctx.fillStyle = text;
      ctx.font = "500 " + Math.round(11 / Math.min(this.scale, 1.4)) + "px " + cssVar("--font-mono", "monospace");
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      var label = node.handle ? "@" + node.handle : node.name;
      ctx.fillText(label, node.x, node.y + r + 6);
      ctx.globalAlpha = 1;
    }

    ctx.restore();

    if (!this.nodes.length || this.nodes.length === 1) {
      ctx.fillStyle = muted;
      ctx.font = "14px " + cssVar("--font-mono", "monospace");
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(this.emptyMsg, w / 2, h / 2);
    }
  };

  NetworkMap.prototype._fit = function (instant) {
    if (!this.nodes.length) return;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    this.nodes.forEach(function (n) {
      minX = Math.min(minX, n.x); maxX = Math.max(maxX, n.x);
      minY = Math.min(minY, n.y); maxY = Math.max(maxY, n.y);
    });
    var bw = Math.max(120, maxX - minX + 80);
    var bh = Math.max(120, maxY - minY + 80);
    var sx = this.width / bw;
    var sy = this.height / bh;
    this.scale = Math.min(1.6, Math.max(0.45, Math.min(sx, sy) * 0.85));
    var cx = (minX + maxX) / 2;
    var cy = (minY + maxY) / 2;
    this.tx = -cx * this.scale;
    this.ty = -cy * this.scale;
    if (!instant) this._draw();
  };

  NetworkMap.prototype._focusNode = function (id) {
    var n = this.nodeById[id];
    if (!n) return;
    this.tx = -n.x * this.scale;
    this.ty = -n.y * this.scale;
    this.hover = n;
    this._draw();
    if (this.coarse) this._showSheet(n);
    else this._showTooltip(n, null);
  };

  NetworkMap.prototype._peerRelation = function (node) {
    if (!node || node.is_self) return null;
    var me = this.graph.me_id;
    for (var i = 0; i < this.edges.length; i++) {
      var e = this.edges[i];
      if (e.kind !== "direct") continue;
      if (
        (e.source === me && e.target === node.id) ||
        (e.target === me && e.source === node.id)
      ) {
        return { relation: e.relation, label: e.label || e.relation };
      }
    }
    return null;
  };

  NetworkMap.prototype._intentLabels = function (node) {
    var labels = [];
    if (node.open_to_work) labels.push("open to work");
    if (node.open_to_collaborate) labels.push("collaborate");
    if (node.open_to_mentor) labels.push("mentor");
    if (node.open_to_learning) labels.push("learning");
    return labels;
  };

  NetworkMap.prototype._showTooltip = function (node, event) {
    if (!this.tooltip || this.coarse) return;
    var rel = this._peerRelation(node);
    var intents = this._intentLabels(node);
    var lines = [
      "<strong>" + escapeHtml(node.name) + "</strong>",
      node.handle ? "@" + escapeHtml(node.handle) : "",
      node.role ? escapeHtml(node.role) : "",
      node.location ? escapeHtml(node.location) : "",
      rel ? escapeHtml(rel.label) : "",
      intents.length ? escapeHtml(intents.join(" · ")) : "",
      node.is_self ? "(you)" : "double-click to open",
    ].filter(Boolean);
    this.tooltip.innerHTML = lines.join("<br>");
    this.tooltip.hidden = false;
    if (event) {
      var rect = this.canvas.getBoundingClientRect();
      var left = event.clientX - rect.left + 14;
      var top = event.clientY - rect.top + 14;
      this.tooltip.style.left = "0px";
      this.tooltip.style.top = "0px";
      var tw = this.tooltip.offsetWidth || 160;
      var th = this.tooltip.offsetHeight || 60;
      left = Math.max(8, Math.min(left, this.width - tw - 8));
      top = Math.max(8, Math.min(top, this.height - th - 8));
      this.tooltip.style.left = left + "px";
      this.tooltip.style.top = top + "px";
    }
  };

  NetworkMap.prototype._hideTooltip = function () {
    if (this.tooltip) this.tooltip.hidden = true;
  };

  NetworkMap.prototype._showSheet = function (node) {
    if (!this.sheet || !node) return;
    var nameEl = this.sheet.querySelector("[data-map-sheet-name]");
    var handleEl = this.sheet.querySelector("[data-map-sheet-handle]");
    var extraEl = this.sheet.querySelector("[data-map-sheet-extra]");
    var openEl = this.sheet.querySelector("[data-map-sheet-open]");
    var rel = this._peerRelation(node);
    var intents = this._intentLabels(node);
    if (nameEl) nameEl.textContent = node.name || "";
    if (handleEl) {
      handleEl.textContent = node.handle
        ? "@" + node.handle + (node.is_self ? " · you" : "")
        : (node.is_self ? "you" : "");
    }
    if (extraEl) {
      var bits = [];
      if (rel && rel.label) bits.push(rel.label);
      if (intents.length) bits.push(intents.join(" · "));
      if (node.role) bits.push(node.role);
      extraEl.textContent = bits.join(" · ");
      extraEl.hidden = !bits.length;
    }
    if (openEl) {
      if (node.url) {
        openEl.href = node.url;
        openEl.hidden = false;
      } else {
        openEl.hidden = true;
      }
    }
    this.sheet.hidden = false;
  };

  NetworkMap.prototype._hideSheet = function () {
    if (this.sheet) this.sheet.hidden = true;
  };

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  ready(function () {
    var canvas = document.querySelector("[data-network-map]");
    if (!canvas) return;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var graph = readEmbeddedGraph();
    var map = new NetworkMap(canvas, graph);
    if (reduce) {
      map.running = false;
      if (map.status) map.status.textContent = "static";
      var pauseBtn = document.querySelector("[data-map-pause]");
      if (pauseBtn) pauseBtn.textContent = "resume";
      // Settle a few ticks then stop.
      for (var i = 0; i < 90; i++) map._tick();
      map._fit(true);
      map._draw();
    }
  });
})();
