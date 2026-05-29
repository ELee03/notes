"""Generate mixed-signal partition floorplan diagram."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(-0.3, 5)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#f7f7f4')

# Board outline
board = mpatches.FancyBboxPatch((0.15, 0.2), 9.7, 4.6,
    boxstyle="round,pad=0.08", lw=1.5, edgecolor='#aab8c8', facecolor='white')
ax.add_patch(board)

# ── Zones ─────────────────────────────────────────────────────────────────────
# Analog zone ends at x=3.65; Digital starts at x=5.05 → 1.4-unit gap for F circle
az = mpatches.FancyBboxPatch((0.35, 0.4), 3.3, 4.2,
    boxstyle="round,pad=0.05", lw=1.5, edgecolor='#c8a020',
    facecolor='#fffcf0', linestyle='--', zorder=1)
ax.add_patch(az)
ax.text(2.0, 4.42, 'Analog Zone', ha='center', va='center',
    fontsize=13, fontweight='bold', color='#7a5010')

dz = mpatches.FancyBboxPatch((5.05, 0.4), 4.6, 4.2,
    boxstyle="round,pad=0.05", lw=1.5, edgecolor='#3a6a8a',
    facecolor='#f0f4f8', linestyle='--', zorder=1)
ax.add_patch(dz)
ax.text(7.35, 4.42, 'Digital Zone', ha='center', va='center',
    fontsize=13, fontweight='bold', color='#1a3860')

# Partition boundary — centre of the gap at x=4.35
BND_X = 4.35
ax.axvline(x=BND_X, ymin=0.2/5, ymax=4.6/5,
    color='#9aabb8', lw=1.0, linestyle=(0, (3, 5)), zorder=2)
ax.text(BND_X, -0.1, 'partition boundary', ha='center', va='top',
    fontsize=8.5, color='#9aabb8', style='italic')


def comp(x, y, w, h, name, sub=None, ec='#c8a020', name_fs=11):
    box = mpatches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.05", lw=1.2, edgecolor=ec, facecolor='white', zorder=3)
    ax.add_patch(box)
    cy = y + h / 2
    if sub:
        ax.text(x + w/2, cy + 0.15, name, ha='center', va='center',
            fontsize=name_fs, fontweight='bold', color='#1a2840', zorder=4)
        ax.text(x + w/2, cy - 0.15, sub, ha='center', va='center',
            fontsize=9.5, color='#7a8a9a', family='monospace', zorder=4)
    else:
        ax.text(x + w/2, cy, name, ha='center', va='center',
            fontsize=name_fs, fontweight='bold', color='#1a2840', zorder=4)


# Analog components — right column ends at x=3.5 (well inside the analog zone)
comp(0.55, 2.9, 1.3, 0.8, 'Sensor',     'electrodes')
comp(2.05, 2.9, 1.45, 0.8, 'InAmp',     'INA128')
comp(0.55, 1.7, 1.3, 0.8, 'VREF',       '2.5 V')
comp(2.05, 1.7, 1.45, 0.8, 'Anti-alias','RC filter')

# Digital components
comp(5.25, 1.8, 2.1, 2.1, 'MCU',          'EFR32 / ADC0', ec='#3a6a8a', name_fs=12)
comp(7.7,  2.9, 1.75, 1.0, 'Flash / SRAM', 'SPI / QSPI',  ec='#3a6a8a')
comp(7.7,  1.6, 1.75, 0.9, 'J-Link / USB', None,           ec='#3a6a8a')

# ── Signal path in analog zone ─────────────────────────────────────────────
SIG_Y = 2.1   # signal exits Anti-alias at this y

# Sensor → InAmp
ax.annotate('', xy=(2.05, 3.3), xytext=(1.85, 3.3),
    arrowprops=dict(arrowstyle='->', color='#c8a020', lw=1.5), zorder=5)

# InAmp bottom → down to Anti-alias top
ax.plot([2.775, 2.775], [2.9, 2.5], color='#c8a020', lw=1.5, zorder=5)
ax.annotate('', xy=(2.775, 2.5), xytext=(2.775, 2.65),
    arrowprops=dict(arrowstyle='->', color='#c8a020', lw=1.5), zorder=5)

# Anti-alias right → dashed toward boundary gap
ax.plot([3.5, BND_X - 0.24], [SIG_Y, SIG_Y],
    color='#7a8a9a', lw=1.5, linestyle='--', zorder=5)

# ── Filter circle — sits in the middle of the gap ─────────────────────────
R = 0.23
fc = plt.Circle((BND_X, SIG_Y), R, color='white', ec='#e08030', lw=2.0, zorder=6)
ax.add_patch(fc)
ax.text(BND_X, SIG_Y, 'F', ha='center', va='center',
    fontsize=10, color='#c05050', family='monospace', fontweight='bold', zorder=7)

# Arrow from circle into MCU
ax.annotate('', xy=(5.25, SIG_Y), xytext=(BND_X + R + 0.05, SIG_Y),
    arrowprops=dict(arrowstyle='->', color='#7a8a9a', lw=1.5), zorder=5)

# ── "filter at boundary" callout ──────────────────────────────────────────
ax.annotate('filter at boundary',
    xy=(BND_X + 0.1, SIG_Y - R - 0.05),   # just below the circle
    xytext=(6.1, 1.1),
    fontsize=9.5, color='#c05050', style='italic', ha='left', va='center',
    arrowprops=dict(arrowstyle='->', color='#c05050', lw=1.0,
                    connectionstyle='arc3,rad=-0.3'),
    zorder=5)

plt.tight_layout(pad=0.2)
plt.savefig('_mixed_signal_partition.svg', format='svg', bbox_inches='tight',
            facecolor='#f7f7f4')
plt.close()
print("Saved _mixed_signal_partition.svg")
