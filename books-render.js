/**
 * books-render.js -- shared reference library renderer
 *
 * Two entry points:
 *
 *   renderBooks({ containerId, clusterId, jsonPath })
 *     Fetches books.json, filters by clusterId, injects <li> items into
 *     the element with id=containerId. Used by cluster pages.
 *
 *   initLibrary({ containerId, jsonPath })
 *     Fetches books.json, renders all books, and wires up filter buttons
 *     (elements with data-cluster attribute). Used by references.html.
 */

// -- Shared helpers -----------------------------------------------------------

function _bookHTML(book) {
  var authors = Array.isArray(book.authors)
    ? book.authors.join(', ')
    : String(book.authors);

  var editionStr = book.edition ? ' (' + book.edition + ' ed.)' : '';
  var pubYear    = [book.publisher, book.year].filter(Boolean).join(', ');
  var byline     = pubYear ? authors + ' -- ' + pubYear : authors;

  return '<li class="book-entry">'
    + '<div class="book-title">' + book.title + editionStr + '</div>'
    + '<div class="book-authors">' + byline + '</div>'
    + (book.annotation ? '<div class="book-annotation">' + book.annotation + '</div>' : '')
    + '</li>';
}

function _renderList(books, container) {
  if (books.length === 0) {
    container.innerHTML = '<li class="book-empty">No references listed for this cluster yet.</li>';
    return;
  }
  container.innerHTML = books.map(_bookHTML).join('\n');
}

// -- Cluster-page entry point -------------------------------------------------

function renderBooks(opts) {
  var containerId = opts.containerId;
  var clusterId   = opts.clusterId || null;
  var jsonPath    = opts.jsonPath  || '../books.json';

  var container = document.getElementById(containerId);
  if (!container) return;

  fetch(jsonPath)
    .then(function(res) { return res.json(); })
    .then(function(all) {
      var books = clusterId
        ? all.filter(function(b) {
            return Array.isArray(b.clusters) && b.clusters.indexOf(clusterId) !== -1;
          })
        : all;
      _renderList(books, container);
    })
    .catch(function(e) {
      console.error('books-render: failed to load', jsonPath, e);
    });
}

// -- Library-page entry point -------------------------------------------------

function initLibrary(opts) {
  var containerId = opts.containerId;
  var jsonPath    = opts.jsonPath || 'books.json';

  var container = document.getElementById(containerId);
  if (!container) return;

  fetch(jsonPath)
    .then(function(res) { return res.json(); })
    .then(function(allBooks) {
      // Initial render -- all books
      _renderList(allBooks, container);

      // Wire up filter buttons
      document.querySelectorAll('[data-cluster]').forEach(function(btn) {
        btn.addEventListener('click', function() {
          // Active state
          document.querySelectorAll('[data-cluster]').forEach(function(b) {
            b.classList.remove('filter-active');
          });
          btn.classList.add('filter-active');

          var cluster = btn.dataset.cluster;
          var filtered = cluster === 'all'
            ? allBooks
            : allBooks.filter(function(b) {
                return Array.isArray(b.clusters) && b.clusters.indexOf(cluster) !== -1;
              });

          _renderList(filtered, container);
        });
      });
    })
    .catch(function(e) {
      console.error('books-render: failed to load', jsonPath, e);
    });
}
