/**
 * notes-nav.js — shared cluster nav renderer
 *
 * Populates #cluster-nav with the lesson sidebar from nav.json.
 * Lesson numbers are auto-computed from sequential position in the nav
 * (planned items are skipped). Numbers are NEVER stored in nav.json text fields.
 *
 * Also:
 *   - Updates the breadcrumb's last element to "Lesson N" (the correct number)
 *   - Populates #lesson-nav (if present) with prev/next buttons derived from nav.json
 *
 * Each lesson only needs:
 *   <div id="cluster-nav" data-cluster="control" data-current="bode.html"></div>
 *   <div id="lesson-nav"></div>   <!-- optional: auto prev/next -->
 */
document.addEventListener('DOMContentLoaded', function () {
  var el = document.getElementById('cluster-nav');
  if (!el) return;

  var current = el.dataset.current;

  fetch('nav.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {

      // ── Flatten published items and assign sequential numbers ─────────────
      var allItems = [];
      data.sections.forEach(function (section) {
        section.items.forEach(function (item) {
          if (!item.planned) {
            allItems.push(item);
            item._num = allItems.length;   // 1-based sequential lesson number
          }
        });
      });

      // ── Sidebar nav ───────────────────────────────────────────────────────
      var html = '';
      data.sections.forEach(function (section) {
        html += '<div class="nav-section">';
        html += '<div class="nav-label">' + section.label + '</div>';
        section.items.forEach(function (item) {
          var label = item._num ? item._num + ' · ' + item.text : item.text;
          if (item.planned) {
            html += '<span class="nav-item planned">' + label + '</span>';
          } else {
            var active = (item.href === current) ? ' active' : '';
            html += '<a href="' + item.href + '" class="nav-item' + active + '">' + label + '</a>';
          }
        });
        html += '</div>';
      });
      el.innerHTML = html;

      // ── Find current item ─────────────────────────────────────────────────
      var idx = -1;
      for (var i = 0; i < allItems.length; i++) {
        if (allItems[i].href === current) { idx = i; break; }
      }
      if (idx === -1) return;

      var lessonNum = allItems[idx]._num;

      // ── Update breadcrumb last text node ──────────────────────────────────
      var breadcrumb = document.querySelector('.breadcrumb');
      if (breadcrumb) {
        var nodes = breadcrumb.childNodes;
        for (var n = nodes.length - 1; n >= 0; n--) {
          if (nodes[n].nodeType === 3 && nodes[n].textContent.trim()) {
            nodes[n].textContent = '\n        Lesson ' + lessonNum + '\n      ';
            break;
          }
        }
      }

      // ── Prev / next lesson nav ────────────────────────────────────────────
      var navEl = document.getElementById('lesson-nav');
      if (!navEl) return;

      var prev = idx > 0                   ? allItems[idx - 1] : null;
      var next = idx < allItems.length - 1 ? allItems[idx + 1] : null;

      var prevHtml = prev
        ? '<a href="' + prev.href + '" class="lesson-nav-btn">← Lesson ' + prev._num + ' · ' + prev.text + '</a>'
        : '<span class="lesson-nav-btn disabled">← Start of cluster</span>';

      var nextHtml = next
        ? '<a href="' + next.href + '" class="lesson-nav-btn">Lesson ' + next._num + ' · ' + next.text + ' →</a>'
        : '<span class="lesson-nav-btn disabled">Cluster complete ✓</span>';

      navEl.innerHTML = '<div class="lesson-nav">' + prevHtml + nextHtml + '</div>';
    })
    .catch(function (e) {
      console.warn('notes-nav: failed to load nav.json', e);
    });
});
