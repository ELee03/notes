/**
 * notes-nav.js — shared cluster nav renderer
 * Fetches nav.json from the current cluster directory and injects
 * the lesson list into #cluster-nav. Each lesson sidebar only needs:
 *   <div id="cluster-nav" data-cluster="control" data-current="bode.html"></div>
 */
document.addEventListener('DOMContentLoaded', function () {
  var el = document.getElementById('cluster-nav');
  if (!el) return;

  var current = el.dataset.current;

  fetch('nav.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
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
    })
    .catch(function (e) {
      console.warn('notes-nav: failed to load nav.json', e);
    });
});
