/**
 * notes-components.js — shared component enhancement
 *
 * Include in every lesson page. Wraps semantic markup with interactive
 * behaviour at runtime, so HTML files only encode content — never widgets.
 *
 * Patterns handled
 * ─────────────────
 * 1. Worked examples
 *    HTML:  <div class="example-box">
 *             <div class="example-header">…</div>
 *             <div class="example-problem">…</div>   ← always visible
 *             <div class="example-body">…</div>       ← wrapped in <details>
 *           </div>
 *
 * 2. Food-for-thought answers
 *    HTML:  <li class="fft-item">
 *             Question text?
 *             <div class="fft-answer">…</div>          ← wrapped in <details>
 *           </li>
 *
 * 3. Page outline (auto-generated)
 *    Scans all .section-head elements in .main, assigns IDs where missing,
 *    and injects an "On this page" nav block into .sidebar. Removes any
 *    hardcoded outline that may already be in the sidebar HTML.
 */
document.addEventListener('DOMContentLoaded', function () {

  // ── Worked example solution toggles ──────────────────────────────────────
  document.querySelectorAll('.example-box').forEach(function (box) {
    if (box.tagName === 'DETAILS') return;
    var body = box.querySelector('.example-body');
    if (!body) return;
    var details = document.createElement('details');
    details.className = 'example-solution-toggle';
    var summary = document.createElement('summary');
    summary.textContent = 'Show solution';
    details.appendChild(summary);
    body.parentNode.insertBefore(details, body);
    details.appendChild(body);
  });

  // ── Proof / derivation toggles ───────────────────────────────────────────
  document.querySelectorAll('.proof-box').forEach(function (box) {
    var body = box.querySelector('.proof-body');
    if (!body) return;
    var details = document.createElement('details');
    details.className = 'proof-toggle';
    var summary = document.createElement('summary');
    summary.textContent = 'Show derivation';
    details.appendChild(summary);
    body.parentNode.insertBefore(details, body);
    details.appendChild(body);
  });

  // ── Food-for-thought answer toggles ──────────────────────────────────────
  document.querySelectorAll('.fft-item').forEach(function (item) {
    var answer = item.querySelector('.fft-answer');
    if (!answer) return;
    var details = document.createElement('details');
    details.className = 'fft-answer';
    var summary = document.createElement('summary');
    summary.textContent = 'One angle on this';
    details.appendChild(summary);
    answer.className = 'fft-answer-body';
    answer.parentNode.insertBefore(details, answer);
    details.appendChild(answer);
  });

  // ── Page outline ──────────────────────────────────────────────────────────
  var sidebar = document.querySelector('.sidebar');
  var main    = document.querySelector('.main');
  if (!sidebar || !main) return;

  // Collect section headings and ensure each has an ID
  var heads = main.querySelectorAll('.section-head');
  var items = [];
  heads.forEach(function (el) {
    var text = el.textContent.trim();
    if (!text) return;
    if (!el.id) {
      el.id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }
    items.push({ id: el.id, text: text });
  });

  if (items.length === 0) return;

  // Remove any hardcoded outline already in the sidebar (HR + nav-section
  // that are direct children of .sidebar, outside #cluster-nav)
  sidebar.querySelectorAll(':scope > hr.sidebar-rule').forEach(function (el) { el.remove(); });
  sidebar.querySelectorAll(':scope > .nav-section').forEach(function (el) { el.remove(); });

  // Build and inject the outline
  var hr = document.createElement('hr');
  hr.className = 'sidebar-rule';
  sidebar.appendChild(hr);

  var section = document.createElement('div');
  section.className = 'nav-section';

  var label = document.createElement('div');
  label.className = 'nav-label';
  label.textContent = 'On this page';
  section.appendChild(label);

  items.forEach(function (item) {
    var a = document.createElement('a');
    a.href = '#' + item.id;
    a.className = 'nav-item';
    a.textContent = item.text;
    section.appendChild(a);
  });

  sidebar.appendChild(section);

});
