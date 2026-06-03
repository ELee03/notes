"""
migrate_examples.py — Convert old <details class="example-box"> pattern
to new flat semantic markup consumed by notes-components.js.

Old pattern:
  <details class="example-box">
    <summary><strong>Example N — Title</strong></summary>
    <div class="example-problem">...</div>
    <div class="example-body">...</div>
  </details>

New pattern:
  <div class="example-box">
    <div class="example-header"><strong>Example N — Title</strong></div>
    <div class="example-problem">...</div>
    <div class="example-body">...</div>
  </div>

Also converts old FFT answer pattern:
  <details class="fft-answer">
    <summary>Answer</summary>
    <div class="fft-answer-body">...</div>
  </details>

inside .fft-item li elements — notes-components.js handles the toggle injection.
"""

import os, re

ROOT = r'C:\Users\eugle\OneDrive\Documents\Personal\Subject Notes'
CLUSTERS = ['control', 'rl']

def migrate_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    content = original

    # ── Example box migration ──────────────────────────────────────────────
    # Step 1: replace <details class="example-box"> + <summary> with div + header
    content = re.sub(
        r'<details class="example-box">\s*\n\s*<summary><strong>(.*?)</strong></summary>',
        lambda m: f'<div class="example-box">\n        <div class="example-header"><strong>{m.group(1)}</strong></div>',
        content
    )

    # Step 2: replace the closing </details> that corresponds to each example-box.
    # After step 1, example-box is now a <div>. Its content ends with </div> (closing
    # example-body or example-problem), followed by optional whitespace, then </details>.
    # We replace that </details> with </div>.
    # Use a simple iterative approach: find </details> preceded by a closing </div> within
    # a reasonable distance, only when it's an example-box closer (not fft-answer or other).
    # Marker: after step 1, every converted example-box now has example-header inside it.
    # We can find blocks: <div class="example-box">...</details> and fix the last tag.

    def fix_example_box_closing(content):
        # Find each example-box div and replace its closing </details> with </div>
        result = []
        i = 0
        open_tag = '<div class="example-box">'
        while i < len(content):
            idx = content.find(open_tag, i)
            if idx == -1:
                result.append(content[i:])
                break
            result.append(content[i:idx])
            # Find the closing </details> for this block
            # It's the first </details> after opening the example-box
            close_idx = content.find('</details>', idx)
            if close_idx == -1:
                result.append(content[idx:])
                break
            # Replace </details> with </div>
            block = content[idx:close_idx] + '</div>'
            result.append(block)
            i = close_idx + len('</details>')
        return ''.join(result)

    if '<div class="example-box">' in content:
        content = fix_example_box_closing(content)

    # ── FFT answer migration ───────────────────────────────────────────────
    # Old: <details class="fft-answer"><summary>Answer...</summary><div class="fft-answer-body">...</div></details>
    # New: <div class="fft-answer">...</div>  (notes-components.js wraps it)
    # Remove the <details class="fft-answer"><summary>...</summary> opening
    content = re.sub(
        r'<details class="fft-answer">\s*\n\s*<summary>.*?</summary>\s*\n(\s*<div class="fft-answer-body">)',
        lambda m: m.group(1),
        content
    )
    # Close the fft-answer-body div, then remove the closing </details>
    # After the above, pattern is: <div class="fft-answer-body">...</div>\n</details>
    # The fft-answer-body closing </div> is followed by </details>
    # Replace: </div>\n            </details>  (inside fft-item) with just </div>
    content = re.sub(
        r'(</div>)\s*\n(\s*)</details>(\s*\n\s*</li>)',
        lambda m: m.group(1) + '\n' + m.group(2) + m.group(3),
        content
    )

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed = []
unchanged = []
for cluster in CLUSTERS:
    folder = os.path.join(ROOT, cluster)
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith('.html') or fn == 'index.html':
            continue
        path = os.path.join(folder, fn)
        if migrate_file(path):
            changed.append(f'{cluster}/{fn}')
        else:
            unchanged.append(f'{cluster}/{fn}')

print(f'\nMigrated {len(changed)} files:')
for f in changed:
    print(f'  + {f}')
print(f'\nUnchanged {len(unchanged)} files:')
for f in unchanged:
    print(f'  - {f}')
