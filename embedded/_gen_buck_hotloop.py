"""Generate buck converter hot-loop layout diagram."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4.5)
ax.axis('off')
fig.patch.set_facecolor('#f7f7f4')
ax.set_title('Buck Converter — Layout View', fontsize=13, fontweight='bold',
             color='#1a2840', pad=10)

# ── Component geometry ─────────────────────────────────────────────────────
# Heights reduced ~40% vs first version; everything centred around y=2.25
CIN  = (0.5,  1.35, 1.1,  1.8)   # C_IN:       x=[0.5,  1.6],  y=[1.35, 3.15]
REG  = (2.5,  0.85, 2.8,  2.8)   # Regulator:  x=[2.5,  5.3],  y=[0.85, 3.65]
IND  = (7.0,  1.25, 2.0,  2.0)   # Inductor:   x=[7.0,  9.0],  y=[1.25, 3.25]
COUT = (9.5,  1.35, 1.1,  1.8)   # C_OUT:      x=[9.5, 10.6],  y=[1.35, 3.15]

CIN_R  = CIN[0]  + CIN[2]   # 1.6
REG_L  = REG[0]              # 2.5
REG_R  = REG[0]  + REG[2]   # 5.3
COUT_R = COUT[0] + COUT[2]  # 10.6

# Hot-trace y positions: near top / bottom of C_IN box
VIN_Y  = CIN[1] + CIN[3] - 0.3   # 2.85  (near top of C_IN)
GND_Y  = CIN[1] + 0.3             # 1.65  (near bottom of C_IN)
SW_Y   = CIN[1] + CIN[3] / 2     # 2.25  (midpoint)

# ── Fills ─────────────────────────────────────────────────────────────────
# Hot loop — spans C_IN through left portion of Regulator
hl = mpatches.Rectangle(
    (CIN[0] - 0.1, GND_Y - 0.2),
    (REG_L + REG[2]*0.35) - (CIN[0] - 0.1),
    (VIN_Y + 0.2) - (GND_Y - 0.2),
    lw=0, facecolor='#c05050', alpha=0.10, zorder=1)
ax.add_patch(hl)

# Ripple loop — inductor + C_OUT
rl = mpatches.Rectangle(
    (REG_R * 0.95, IND[1] - 0.25),
    COUT_R + 0.1 - REG_R * 0.95,
    IND[3] + 0.5,
    lw=0, facecolor='#3a6a8a', alpha=0.07, zorder=1)
ax.add_patch(rl)


def comp_box(rect, name, sub=None, ec='#c8a020', lw_border=1.5):
    x, y, w, h = rect
    box = mpatches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.07", lw=lw_border, edgecolor=ec,
        facecolor='white', zorder=3)
    ax.add_patch(box)
    cy = y + h / 2
    if sub:
        ax.text(x + w/2, cy + 0.18, name, ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1a2840', zorder=4)
        ax.text(x + w/2, cy - 0.18, sub,  ha='center', va='center',
            fontsize=10, color='#5a7a9a', family='monospace', zorder=4)
    else:
        ax.text(x + w/2, cy, name, ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1a2840', zorder=4)


comp_box(CIN,  'C_IN',      '10 µF')
comp_box(REG,  'Regulator', 'TPS62x / AP63', ec='#3a6a8a', lw_border=2)
comp_box(IND,  'L',         ec='#7ab8d4')
comp_box(COUT, 'C_OUT',     '22 µF', ec='#7ab8d4')

# ── Hot traces ─────────────────────────────────────────────────────────────
ax.plot([CIN_R, REG_L], [VIN_Y, VIN_Y], color='#c05050', lw=3, zorder=5)
ax.plot([CIN_R, REG_L], [GND_Y, GND_Y], color='#c05050', lw=3, zorder=5)

# ── Pin labels — offset ABOVE/BELOW their traces so lines don't cross text
ax.text(REG_L - 0.1, VIN_Y + 0.22, 'VIN', ha='right', va='bottom',
    fontsize=9, color='#5a7a9a', family='monospace', zorder=6)
ax.text(REG_L - 0.1, GND_Y - 0.22, 'GND', ha='right', va='top',
    fontsize=9, color='#5a7a9a', family='monospace', zorder=6)
ax.text(REG_R + 0.12, SW_Y + 0.22, 'SW', ha='left', va='bottom',
    fontsize=9, color='#5a7a9a', family='monospace', zorder=6)

# ── SW trace → inductor → C_OUT ────────────────────────────────────────────
ax.plot([REG_R, IND[0]], [SW_Y, SW_Y], color='#3a6a8a', lw=2, zorder=5)
ax.plot([IND[0] + IND[2], COUT[0]], [SW_Y, SW_Y], color='#3a6a8a', lw=2, zorder=5)

# VOUT
ax.plot([COUT_R, COUT_R + 1.1], [SW_Y, SW_Y], color='#40a060', lw=2, zorder=5)
ax.text(COUT_R + 1.25, SW_Y, 'VOUT', va='center',
    fontsize=9.5, color='#1a4020', family='monospace', zorder=4)

# ── GND plane ──────────────────────────────────────────────────────────────
GND_P = 0.22
ax.axhline(y=GND_P, xmin=0.03, xmax=0.93, color='#40a060', lw=1.5, zorder=2)
ax.fill_between([0.35, 11.2], GND_P - 0.15, GND_P,
    color='#40a060', alpha=0.25, zorder=2)
ax.text(6.0, GND_P - 0.32, 'GND plane', ha='center',
    fontsize=9, color='#1a4020', family='monospace', zorder=4)

for xc in [CIN[0] + CIN[2]/2, REG[0] + REG[2]/2, COUT[0] + COUT[2]/2]:
    ax.plot([xc, xc], [CIN[1], GND_P], color='#40a060', lw=1.5, zorder=5)

# ── HOT LOOP annotation — centred in the gap between C_IN and Regulator ────
GAP_CX = (CIN_R + REG_L) / 2   # 2.05
GAP_CY = (VIN_Y + GND_Y) / 2   # 2.25

ax.text(GAP_CX, GAP_CY + 0.2, 'HOT LOOP',
    ha='center', va='center', fontsize=11, fontweight='bold', color='#c05050',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffe8e8',
              edgecolor='#c05050', lw=0.9, alpha=0.93),
    zorder=6)
ax.text(GAP_CX, GAP_CY - 0.28, 'keep area small!',
    ha='center', va='center', fontsize=8.5, color='#c05050',
    style='italic', zorder=6)

# ── Ripple loop label ──────────────────────────────────────────────────────
rip_cx = (REG_R * 0.95 + COUT_R + 0.1) / 2
ax.text(rip_cx, IND[1] - 0.38, 'ripple loop (larger OK)',
    ha='center', va='top', fontsize=8.5, color='#3a6a8a',
    style='italic', zorder=4)

# ── Feedback trace (dashed arc) ────────────────────────────────────────────
fb_start = (COUT[0] + COUT[2]/2, COUT[1])
fb_end   = (REG[0]  + REG[2]/2,  REG[1])
ax.annotate('', xy=fb_end, xytext=fb_start,
    arrowprops=dict(arrowstyle='->', color='#c8a020', lw=1.5,
                    linestyle='dashed', connectionstyle='arc3,rad=0.4'),
    zorder=5)
fb_label_x = (fb_start[0] + fb_end[0]) / 2 + 0.2
fb_label_y = min(fb_start[1], fb_end[1]) - 0.5
ax.text(fb_label_x, fb_label_y, 'FB trace (away from L)',
    ha='center', fontsize=8, color='#7a6010', style='italic', zorder=4)

plt.tight_layout(pad=0.3)
plt.savefig('_buck_hotloop.svg', format='svg', bbox_inches='tight',
            facecolor='#f7f7f4')
plt.close()
print("Saved _buck_hotloop.svg")
