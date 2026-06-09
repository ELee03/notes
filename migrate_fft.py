import os, re, glob

base = r'C:\Users\eugle\OneDrive\Documents\Personal\Subject Notes'
files = glob.glob(base + r'\rl\*.html') + glob.glob(base + r'\control\*.html')

changed = []
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'fft-answer-body' not in content:
        continue

    original = content

    # Step 1: rename fft-answer-body -> fft-answer on the div tags
    content = content.replace('class="fft-answer-body"', 'class="fft-answer"')

    # Step 2: add class="fft-item" to plain <li> elements that contain a fft-answer div
    content = re.sub(
        r'<li>(?=(?:(?!</li>).)*?<div class="fft-answer")',
        '<li class="fft-item">',
        content,
        flags=re.DOTALL
    )

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.basename(path))

print('Migrated', len(changed), 'files:')
for f in sorted(changed): print(' ', f)
