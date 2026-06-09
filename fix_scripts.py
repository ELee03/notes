import os, glob

base = r'C:\Users\eugle\OneDrive\Documents\Personal\Subject Notes'
files = glob.glob(base + r'\rl\*.html') + glob.glob(base + r'\control\*.html')

fixed = []
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # Fix 1: broken closing comment in dp.html
    if '<!-- /site-wrap">' in content:
        content = content.replace('<!-- /site-wrap">', '<!-- /site-wrap -->')
        changed = True

    # Fix 2: add notes-components.js after notes-nav.js where missing
    if 'notes-nav.js' in content and 'notes-components.js' not in content:
        content = content.replace(
            '<script src="../notes-nav.js"></script>',
            '<script src="../notes-nav.js"></script>\n<script src="../notes-components.js"></script>'
        )
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed.append(os.path.basename(path))

print(f'Fixed {len(fixed)} files:')
for f in sorted(fixed): print(f'  {f}')
