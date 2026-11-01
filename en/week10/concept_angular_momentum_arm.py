"""
Supplementary Concept Animation 1 (Sec. 3.10): Angular Momentum H_O = m v d = m r v sin(theta) & Invariant Moment Arm d
Engineering Mechanics: Dynamics 9th Edition - Section 3.10 Angular Impulse and Angular Momentum
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m = 2.0
v_mag = 5.0
d_arm = 3.0
H_O = m * v_mag * d_arm  # 30.0 kg·m^2/s

n_frames = 60
x_vals = np.linspace(4.5, -4.5, n_frames)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.15, 1.05], height_ratios=[0.92, 1.08],
              left=0.05, right=0.97, top=0.87, bottom=0.08, wspace=0.14, hspace=0.28)

ax_geom = fig.add_subplot(gs[:, 0])
ax_bars = fig.add_subplot(gs[0, 1])
ax_note = fig.add_subplot(gs[1, 1])

fig.suptitle(r"Concept Animation 1: Why $H_O = m v d = m r v\sin\theta$ Remains Constant Along Straight-Line Motion",
             fontsize=13.4, fontweight='bold', color='#111827', y=0.96)


def update(frame):
    xc = float(x_vals[frame])
    yc = d_arm
    r_curr = np.hypot(xc, yc)
    theta_rad = np.arccos(np.clip(-xc / r_curr, -1.0, 1.0))
    theta_deg = np.degrees(theta_rad)
    v_theta = v_mag * np.sin(theta_rad)

    ax_geom.clear()
    ax_bars.clear()
    ax_note.clear()
    for ax in (ax_geom, ax_bars, ax_note):
        ax.set_facecolor('#ffffff')

    ax_geom.set_xlim(-5.8, 5.8)
    ax_geom.set_ylim(-1.9, 5.3)
    ax_geom.set_aspect('equal')
    ax_geom.axis('off')
    ax_geom.set_title(r"1. Even as $\mathbf{r}$ and $\theta$ Vary, Perpendicular Arm $d = r\sin\theta$ Is Constant!",
                      fontsize=11.0, fontweight='bold', color='#1e293b', pad=6)

    # Fixed top-left HUD pill (zero collision with moving vectors!)
    ax_geom.text(-5.45, 4.65,
                 rf"Live Readout:  $r = {r_curr:.2f}\ \mathrm{{m}}$,   $\theta = {theta_deg:.0f}^\circ$,   $r\sin\theta = {d_arm:.2f}\ \mathrm{{m}}$",
                 fontsize=9.4, fontweight='bold', color='#1e40af', ha='left', va='center',
                 bbox=dict(boxstyle='round,pad=0.30', fc='#eff6ff', ec='#93c5fd', lw=1.3))

    ax_geom.plot([-5.3, 5.3], [0, 0], color='#64748b', lw=1.3, ls='--')
    ax_geom.plot([0, 0], [-0.8, 4.15], color='#64748b', lw=1.3, ls='--')
    ax_geom.text(5.45, -0.08, '$x$', fontsize=12, fontweight='bold', color='#334155')
    ax_geom.text(0.14, 4.12, '$y$', fontsize=12, fontweight='bold', color='#334155')

    ax_geom.plot([-5.3, 5.3], [d_arm, d_arm], color='#94a3b8', lw=1.8, ls=':', zorder=2)
    ax_geom.text(5.25, d_arm - 0.34, "Line of Action of Velocity", fontsize=8.8, color='#475569', ha='right', fontweight='bold')

    ax_geom.plot([0, 0], [0, d_arm], color='#7c3aed', lw=3.0, zorder=3)
    sq = 0.28
    ax_geom.plot([0, sq, sq], [d_arm - sq, d_arm - sq, d_arm], color='#7c3aed', lw=1.5, zorder=3)
    if xc >= 0.0:
        ax_geom.text(-0.25, 1.45, r"$d = r\sin\theta = 3.0\ \mathrm{m}$" + "\n(Constant!)",
                     fontsize=9.3, fontweight='bold', color='#6d28d9', ha='right', va='center',
                     bbox=dict(boxstyle='round,pad=0.22', fc='#f5f3ff', ec='#c4b5fd', lw=1.1))
    else:
        ax_geom.text(0.25, 1.45, r"$d = r\sin\theta = 3.0\ \mathrm{m}$" + "\n(Constant!)",
                     fontsize=9.3, fontweight='bold', color='#6d28d9', ha='left', va='center',
                     bbox=dict(boxstyle='round,pad=0.22', fc='#f5f3ff', ec='#c4b5fd', lw=1.1))

    ax_geom.plot(0, 0, 'o', color='#0f172a', markersize=6.5, zorder=6)
    ax_geom.text(0.18, -0.42, '$O$', fontsize=12, fontweight='bold', color='#0f172a')
    arc_ccw = np.linspace(-0.25, 1.30, 30)
    ax_geom.plot(0.55 * np.cos(arc_ccw), 0.55 * np.sin(arc_ccw), color='#0284c7', lw=2.0)
    ax_geom.annotate('', xy=(0.55 * np.cos(1.36), 0.55 * np.sin(1.36)),
                     xytext=(0.55 * np.cos(1.12), 0.55 * np.sin(1.12)),
                     arrowprops=dict(arrowstyle='-|>', color='#0284c7', lw=2.0, mutation_scale=12))
    ax_geom.text(-0.68, -0.45, r"$+\mathbf{k}$ (CCW)", fontsize=9.1, fontweight='bold', color='#0369a1', ha='right')

    ax_geom.annotate('', xy=(xc, yc), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='-|>', color='#1d4ed8', lw=2.3, mutation_scale=14), zorder=4)
    if abs(xc) > 0.65:
        off_x = 0.28 if xc > 0 else -0.28
        ax_geom.text(xc * 0.52 + off_x, yc * 0.52 - 0.18, r"$\mathbf{r}$",
                     fontsize=11.5, fontweight='bold', color='#1d4ed8', ha='center', va='center')

    u_r = np.array([xc, yc]) / r_curr
    ax_geom.plot([xc, xc + 0.95 * u_r[0]], [yc, yc + 0.95 * u_r[1]], color='#1d4ed8', lw=1.2, ls='--', zorder=3)
    ang_r_dir = np.arctan2(yc, xc)
    ang_v_dir = np.pi
    a1, a2 = min(ang_r_dir, ang_v_dir), max(ang_r_dir, ang_v_dir)
    arc_th = np.linspace(a1, a2, 24)
    ax_geom.plot(xc + 0.68 * np.cos(arc_th), yc + 0.68 * np.sin(arc_th), color='#d97706', lw=1.8, zorder=5)
    mid_a = 0.5 * (a1 + a2)
    ax_geom.text(xc + 0.92 * np.cos(mid_a), yc + 0.92 * np.sin(mid_a), r"$\theta$",
                 fontsize=10.5, fontweight='bold', color='#b45309', ha='center', va='center')

    ball = patches.Circle((xc, yc), 0.25, facecolor='#bae6fd', edgecolor='#0f172a', lw=1.8, zorder=6)
    ax_geom.add_patch(ball)
    ax_geom.text(xc + 0.35, yc - 0.38, r"$m = 2\ \mathrm{kg}$", fontsize=9.4, fontweight='bold', ha='left', color='#0f172a')

    v_len = 1.60
    ax_geom.annotate('', xy=(xc - v_len, yc), xytext=(xc, yc),
                     arrowprops=dict(arrowstyle='-|>', color='#059669', lw=2.8, mutation_scale=16), zorder=7)
    ax_geom.text(xc - 0.85, yc + 0.34, r"$m\mathbf{v}\ (5\ \mathrm{m/s})$",
                 fontsize=9.4, fontweight='bold', color='#047857', ha='center')

    ax_geom.text(0.0, -1.35,
                 r"Right-Hand Rule ($\mathbf{r} \to m\mathbf{v}$):  "
                 r"CCW $= +\mathbf{k}$ (thumb $\odot$)  |  CW $= -\mathbf{k}$ (thumb $\otimes$)",
                 fontsize=9.1, fontweight='bold', color='#1e293b', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.35', fc='#f8fafc', ec='#cbd5e1', lw=1.3))

    ax_bars.set_xlim(0, 48)
    ax_bars.set_ylim(-0.6, 2.7)
    ax_bars.set_yticks([0.0, 1.0, 2.0])
    ax_bars.set_yticklabels([r'$H_O$', r'Arm $d \times 5$', r'Dist $r(t) \times 5$'],
                            fontsize=9.3, fontweight='bold')
    ax_bars.set_title(r"2. Live Check: $r(t)$ Changes, Yet $d = r\sin\theta$ and $H_O$ Stay Constant!",
                      fontsize=10.3, fontweight='bold', color='#1e293b', pad=6)
    ax_bars.grid(axis='x', ls=':', alpha=0.5)

    ax_bars.barh(2.0, r_curr * 5.0, height=0.52, color='#93c5fd', edgecolor='#1d4ed8', lw=1.4)
    ax_bars.text(r_curr * 5.0 + 0.7, 2.0, rf"$r = {r_curr:.2f}\ \mathrm{{m}},\ v_\theta = {v_theta:.2f}\ \mathrm{{m/s}}$",
                 va='center', fontsize=8.8, fontweight='bold', color='#1e40af')

    ax_bars.barh(1.0, d_arm * 5.0, height=0.52, color='#ddd6fe', edgecolor='#6d28d9', lw=1.4)
    ax_bars.text(d_arm * 5.0 + 0.7, 1.0, rf"$d = r\sin\theta = {d_arm:.2f}\ \mathrm{{m}}$ (Constant!)",
                 va='center', fontsize=8.8, fontweight='bold', color='#5b21b6')

    ax_bars.barh(0.0, H_O, height=0.52, color='#6ee7b7', edgecolor='#047857', lw=1.5)
    ax_bars.text(H_O + 0.7, 0.0, r"$H_O = +30.0\ \mathrm{kg\cdot m^2/s}$",
                 va='center', fontsize=8.9, fontweight='bold', color='#065f46')

    ax_note.set_xlim(0, 10)
    ax_note.set_ylim(0, 10)
    ax_note.axis('off')

    bubble = (
        "[Callout] Why Does a Straight-Moving Particle Have Angular Momentum?\n"
        "• Angular momentum " + r"$\mathbf{H}_O = \mathbf{r} \times m\mathbf{v}$" + " is the 'moment of linear momentum' about " + r"$O$" + "!\n"
        "• Whenever the line of action of " + r"$m\mathbf{v}$" + " misses point " + r"$O$" + " (" + r"$d > 0$" + "),\n"
        "  its perpendicular moment arm " + r"$d = r\sin\theta$" + " stays constant along the straight path."
    )
    ax_note.text(0.15, 9.75, bubble, fontsize=9.0, color='#78350f', va='top', ha='left', linespacing=1.36,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_card = (
        "Three Equivalent Planar Forms (Sec. 3.10):\n"
        + r"$\mathbf{H}_O = \mathbf{r} \times m\mathbf{v} \quad\Longrightarrow\quad "
        + r"H_O = m v d = m r v\sin\theta = m r v_\theta = m r^2\dot{\theta}$" + "\n"
        + "• Use " + r"$mvd$" + " directly when perpendicular arm " + r"$d$" + " is clear; use determinant in 3D!"
    )
    ax_note.text(0.15, 3.85, eq_card, fontsize=9.0, color='#0f172a', va='top', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4))


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_angular_momentum_arm.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=85)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved concept_angular_momentum_arm.gif")
