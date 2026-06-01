/**
 * notes-index.js — renders the lesson table on cluster index pages from nav.json.
 * The sidebar is handled separately by notes-nav.js.
 *
 * Expects a <tbody id="lesson-tbody"> inside a .lesson-list table.
 * Call renderLessonTable() after DOMContentLoaded (or inline at bottom of body).
 */
function renderLessonTable() {
  var tbody = document.getElementById('lesson-tbody');
  if (!tbody) return;

  fetch('nav.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var num = 1;
      var html = '';
      data.sections.forEach(function (section) {
        html += '<tr class="part-head"><td colspan="3">' + section.label + '</td></tr>';
        section.items.forEach(function (item) {
          // Strip the leading "N · " from item.text for the title cell
          var title = item.text.replace(/^\d+\s*·\s*/, '');
          var titleCell = item.planned
            ? '<td><span style="color:#8a9ab0;">' + title + '</span></td>'
            : '<td><a href="' + item.href + '">' + title + '</a></td>';
          var topicsCell = '<td>' + (item.topics || '') + '</td>';
          html += '<tr class="lesson-row"><td>' + num + '</td>' + titleCell + topicsCell + '</tr>';
          num++;
        });
      });
      tbody.innerHTML = html;
    })
    .catch(function (e) {
      console.warn('notes-index: failed to load nav.json', e);
    });
}
