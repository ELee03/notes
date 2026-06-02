/**
 * notes-portal.js — renders the portal page and sidebar from portal.json.
 *
 * Structure of portal.json:
 *   { "sections": [ <node>, ... ] }
 *
 * A node is either:
 *   Branch: { "label": "...", "children": [ <node>, ... ] }
 *   Leaf:   { "name": "...", "desc": "...", "planned": true }
 *           { "name": "...", "desc": "...", "href": "...", "lessons": N }
 *
 * Depth 0 branches → .portal-section-head  (large, accented, dominant)
 * Depth 1+ branches → .subsection-head      (small caps, subordinate)
 * Leaves → .cluster-card
 *
 * Any depth is supported by the recursive renderer.
 */

// ─── Slug helper ──────────────────────────────────────────────────────────────

function slugify(text) {
  return text
    .replace(/&amp;/g, 'and')
    .replace(/&/g, 'and')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

// ─── Main content renderer ────────────────────────────────────────────────────

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
  if (node.name !== undefined) {
    return renderCard(node);
  }

  var id = slugify(node.label);
  var html = '';

  if (depth === 0) {
    html += '<div class="portal-section-head" id="' + id + '">' + node.label + '</div>';
  } else {
    html += '<div class="subsection-head" id="' + id + '">' + node.label + '</div>';
  }

  var branches = node.children.filter(function (c) { return c.children !== undefined; });
  var leaves   = node.children.filter(function (c) { return c.name  !== undefined; });

  if (branches.length > 0) {
    branches.forEach(function (child) {
      html += renderNode(child, depth + 1);
    });
    if (leaves.length > 0) {
      html += '<div class="cluster-grid" style="margin-bottom:20px;">';
      leaves.forEach(function (leaf) { html += renderCard(leaf); });
      html += '</div>';
    }
  } else {
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

// ─── Sidebar renderer ─────────────────────────────────────────────────────────

function renderPortalSidebar(containerId) {
  var container = document.getElementById(containerId || 'portal-sidebar-nav');
  if (!container) return;

  fetch('portal.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var html = '<div class="portal-nav">';
      data.sections.forEach(function (section) {
        var sectionId = slugify(section.label);

        // Collect subcategory labels (depth-1 branches) for the dropdown items
        var items = '';
        section.children.forEach(function (child) {
          if (child.children !== undefined) {
            // Subcategory — link to its anchor
            var childId = slugify(child.label);
            items += '<a href="#' + childId + '" class="portal-nav-item">' + child.label + '</a>';
          } else {
            // Section has no subcategories — link to the section itself
            items += '<a href="#' + sectionId + '" class="portal-nav-item">' + child.name + '</a>';
          }
        });

        html += '<details class="portal-nav-details">';
        html += '<summary><a href="#' + sectionId + '" style="color:inherit;text-decoration:none;">' + section.label + '</a></summary>';
        html += '<div class="portal-nav-items">' + items + '</div>';
        html += '</details>';
      });
      html += '</div>';
      container.innerHTML = html;
    })
    .catch(function (e) {
      console.warn('notes-portal: failed to load portal.json for sidebar', e);
    });
}
