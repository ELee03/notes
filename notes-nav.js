/**
 * notes-nav.js — shared cluster nav renderer
 *
 * Populates #cluster-nav with the lesson sidebar from nav.json.
 * Also populates #lesson-nav (if present) with prev/next buttons
 * derived from the same nav.json — single source of truth for
 * lesson order and titles.
 *
 * Each lesson only needs:
 *   <div id="cluster-nav" data-cluster="control" data-current="bode.html"></div>
 *   <div id="lesson-nav"></div>
 */
document.addEventListener('DOMContentLoaded', function () {
  var el = document.getElementById('cluster-nav');
  if (!el) return;

  var current = el.dataset.current;

  fetch('nav.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {

      // ── Sidebar nav ──────────────────────────────────────────────────────
      var html = '';
      data.sections.forEach(function (section) {
        html += '<div class="nav-section">';
        html += '<div class="nav-label">' + section.label + '</div>';
        section.items.forEach(function (item) {
          if (item.planned) {
            html += '<span class="nav-item planned">' + item.text + '</span>';
          } else {
            var active = (item.href === current) ? ' active' : '';
            html += '<a href="' + item.href + '" class="nav-item' + active + '">' + item.text + '</a>';
          }
        });
        html += '</div>';
      });
      el.innerHTML = html;

      // ── Prev / next lesson nav ────────────────────────────────────────────
      var navEl = document.getElementById('lesson-nav');
      if (!navEl) return;

      // Flatten all items from every section (skip planned items)
      var allItems = [];
      data.sections.forEach(function (section) {
        section.items.forEach(function (item) {
          if (!item.planned) allItems.push(item);
        });
      });

      // Find position of current page
      var idx = -1;
      for (var i = 0; i < allItems.length; i++) {
        if (allItems[i].href === current) { idx = i; break; }
      }
      if (idx === -1) return; // current file is not a lesson (e.g. index.html)

      var prev = idx > 0               ? allItems[idx - 1] : null;
      var next = idx < allItems.length - 1 ? allItems[idx + 1] : null;

      var prevHtml = prev
        ? '<a href="' + prev.href + '" class="lesson-nav-btn">← ' + prev.text + '</a>'
        : '<span class="lesson-nav-btn disabled">← Start of cluster</span>';

      var nextHtml = next
        ? '<a href="' + next.href + '" class="lesson-nav-btn">' + next.text + ' →</a>'
        : '<span class="lesson-nav-btn disabled">Cluster complete ✓</span>';

      navEl.innerHTML = '<div class="lesson-nav">' + prevHtml + nextHtml + '</div>';
    })
    .catch(function (e) {
      console.warn('notes-nav: failed to load nav.json', e);
    });
});
