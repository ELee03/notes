import re, pathlib

root = pathlib.Path(r'C:/Users/eugle/OneDrive/Documents/Personal/Subject Notes')
pattern = re.compile(r'<div class="lesson-nav">.*?</div>', re.DOTALL)
replacement = '<div id="lesson-nav"></div>'

changed_files = []
for html_file in root.rglob('*.html'):
    if html_file.name.startswith('_'):
        continue
    text = html_file.read_text(encoding='utf-8')
    new_text, count = pattern.subn(replacement, text)
    if count:
        html_file.write_text(new_text, encoding='utf-8')
        changed_files.append((str(html_file.relative_to(root)), count))

for f, n in changed_files:
    print(f'Replaced {n} block(s) in {f}')
print(f'Total files changed: {len(changed_files)}')
