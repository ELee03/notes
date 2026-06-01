/**
 * notes-portal.js — renders the portal page from portal.json.
 *
 * Structure of portal.json:
 *   { "sections": [ <node>, ... ] }
 *
 * A node is either:
 *   - Branch: { "label": "...", "children": [ <node>, ... ] }
 *   - Leaf:   { "name": "...", "desc": "...", "planned": true }
 *             { "name": "...", "desc": "...", "href": "...", "lessons": N }
 *
 * Branches at depth 0 render as .section-head.
 * Branches at depth 1+ render as .subsection-head.
 * Leaves always render as .cluster-card.
 * Any depth is supported — CSS distinguishes depth 0 vs 1+.
 */

function renderPortal(containerId) {
  var container = document.getElementById(containerId || 'portal-content');
  if (!container) return;

  fetch('portal.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var html = '';
      data.sections.forEach(function (section) {
        html += renderNode(section, 0);
      });
      container.innerHTML = html;
    })
    .catch(function (e) {
      console.warn('notes-portal: failed to load portal.json', e);
    });
}

function renderNode(node, depth) {
  // Leaf: has "name" → cluster card
  if (node.name !== undefined) {
    return renderCard(node);
  }

  // Branch: has "label" + "children"
  var html = '';
  var headClass = depth === 0 ? 'section-head' : 'subsection-head';
  html += '<div class="' + headClass + '">' + node.label + '</div>';

  // Separate children into branches and leaves
  var branches = node.children.filter(function (c) { return c.children !== undefined; });
  var leaves   = node.children.filter(function (c) { return c.name  !== undefined; });

  if (branches.length > 0) {
    // Has sub-groupings — recurse into them, then append any loose leaves
    branches.forEach(function (child) {
      html += renderNode(child, depth + 1);
    });
    if (leaves.length > 0) {
      html += '<div class="cluster-grid" style="margin-bottom:20px;">';
      leaves.forEach(function (leaf) { html += renderCard(leaf); });
      html += '</div>';
    }
  } else {
    // All children are leaves — render as a flat grid
    var mb = depth === 0 ? '28px' : '20px';
    html += '<div class="cluster-grid" style="margin-bottom:' + mb + ';">';
    leaves.forEach(function (leaf) { html += renderCard(leaf); });
    html += '</div>';
  }

  return html;
}

function renderCard(cluster) {
  var badge = cluster.planned
    ? '<span class="cluster-badge planned">planned</span>'
    : '<span class="cluster-badge active">' + cluster.lessons + ' lessons</span>';

  var inner = '<div class="cluster-card-top">'
            +   '<div class="cluster-name">' + cluster.name + '</div>'
            +   badge
            + '</div>'
            + '<div class="cluster-divider"></div>'
            + '<div class="cluster-desc">' + cluster.desc + '</div>';

  if (cluster.href) {
    return '<a href="' + cluster.href + '" class="cluster-card">' + inner + '</a>';
  } else {
    return '<div class="cluster-card planned">' + inner + '</div>';
  }
}
