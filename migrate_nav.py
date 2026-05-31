"""
migrate_nav.py
Replaces hardcoded cluster nav HTML in every lesson file with a single
  <div id="cluster-nav" data-cluster="X" data-current="filename.html"></div>
and adds a <script src="../notes-nav.js"></script> tag before </body>.

Safe to re-run: skips files that already have id="cluster-nav".
"""

import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# (cluster_dir, cluster_id, lesson_filenames, has_prereqs_section)
CLUSTERS = [
    ('control', 'control', [
        'control-problem.html', 'transfer-functions.html', 'bode.html',
        'routh.html', 'root-locus.html', 'nyquist.html',
        'pid.html', 'lead-lag.html',
        'state-space.html', 'state-response.html', 'controllability.html',
        'state-feedback.html', 'lqr.html', 'observers.html',
    ], False),
    ('rl', 'rl', [
        'rl-problem.html', 'bandits.html', 'mdp.html',
        'value-functions.html', 'dp.html', 'monte-carlo.html',
        'td-learning.html', 'function-approx.html', 'policy-gradients.html',
    ], True),
    ('embedded', 'embedded', [
        'mcu-architecture.html', 'memory-clocks.html', 'interrupts-nvic.html', 'dma.html',
        'gpio.html', 'timers-pwm.html', 'adc-dac.html',
        'uart.html', 'spi.html', 'i2c.html', 'can.html', 'usb.html',
        'bare-metal.html', 'rtos.html', 'debug.html',
        'layout.html', 'mixed-signal.html', 'power-thermal.html', 'high-speed-rf.html',
    ], False),
]

SCRIPT_TAG = '    <script src="../notes-nav.js"></script>\n'

def process_file(path, cluster_id, filename, has_prereqs):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already migrated
    if 'id="cluster-nav"' in html:
        print(f'  SKIP (already done): {filename}')
        return

    placeholder = (
        f'      <div id="cluster-nav" '
        f'data-cluster="{cluster_id}" '
        f'data-current="{filename}"></div>\n'
    )

    # ── Locate the sidebar boundaries ────────────────────────────────────────
    sidebar_open = html.find('    <div class="sidebar">')
    if sidebar_open == -1:
        # try without leading spaces
        sidebar_open = html.find('<div class="sidebar">')
    if sidebar_open == -1:
        print(f'  WARN no sidebar: {filename}')
        return

    hr_pos = html.find('      <hr class="sidebar-rule">', sidebar_open)
    if hr_pos == -1:
        hr_pos = html.find('<hr class="sidebar-rule">', sidebar_open)
    if hr_pos == -1:
        print(f'  WARN no hr rule: {filename}')
        return

    sidebar_tag_end = html.index('>', sidebar_open) + 1  # end of <div class="sidebar">

    # ── Build replacement ─────────────────────────────────────────────────────
    if has_prereqs:
        # Find the Prerequisites nav-section and keep it; replace cluster nav
        prereq_label = html.find('<div class="nav-label">Prerequisites</div>', sidebar_tag_end, hr_pos)
        if prereq_label != -1:
            # Find opening of the nav-section containing Prerequisites
            prereq_section_open = html.rfind('<div class="nav-section">', sidebar_tag_end, prereq_label)
            # Find its closing </div> — the next \n      </div> after the label
            close_marker = '\n      </div>'
            prereq_close_pos = html.find(close_marker, prereq_label)
            if prereq_close_pos == -1:
                print(f'  WARN cannot find prereq close: {filename}')
                return
            prereq_block_end = prereq_close_pos + len(close_marker)
            # Reconstruct: keep up to prereq_block_end, inject placeholder, then hr onwards
            new_html = (
                html[:prereq_block_end] +
                '\n\n' + placeholder +
                '\n      ' + html[hr_pos:]
            )
        else:
            # No prereq section found — treat like a non-prereq file
            new_html = html[:sidebar_tag_end] + '\n' + placeholder + '      ' + html[hr_pos:]
    else:
        # Replace everything between sidebar opening tag and hr
        new_html = html[:sidebar_tag_end] + '\n' + placeholder + '      ' + html[hr_pos:]

    # ── Add script tag before </body> if not already present ─────────────────
    if 'notes-nav.js' not in new_html:
        new_html = new_html.replace('</body>', SCRIPT_TAG + '</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  OK: {filename}')


def main():
    for cluster_dir, cluster_id, lessons, has_prereqs in CLUSTERS:
        print(f'\n[{cluster_id}]')
        for lesson in lessons:
            path = os.path.join(ROOT, cluster_dir, lesson)
            if not os.path.exists(path):
                print(f'  MISSING: {lesson}')
                continue
            process_file(path, cluster_id, lesson, has_prereqs)
    print('\nDone.')

if __name__ == '__main__':
    main()
