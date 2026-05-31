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
 */
document.addEventListener('DOMContentLoaded', function () {

  // ── Worked example solution toggles ──────────────────────────────────────
  document.querySelectorAll('.example-box').forEach(function (box) {
    if (box.tagName === 'DETAILS') return; // skip old-pattern <details.example-box>
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

});
