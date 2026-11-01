"""
Supplementary Concept Animation 2 (Sec. 3.10): Central-Force Motion (ΣM_O = 0) & Angular Momentum Conservation
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

m = 1.0
r1 = 2.0
v1 = 2.0
H_const = m * r1 * v1  # 4.0 kg·m^2/s
T1 = 0.5 * m * (v1 ** 2)  # 2.0 J

n_frames = 68
dt = 0.065

r_hist = np.zeros(n_frames)
phi_hist = np.zeros(n_frames)
for i in range(n_frames):
    if i < 16:
        r_hist[i] = 2.0
    elif i < 48:
        s = (i - 16) / 32.0
        r_hist[i] = 2.0 - 1.0 * (0.5 - 0.5 * np.cos(np.pi * s))
    else:
        r_hist[i] = 1.0
    if i > 0:
        r_mid = 0.5 * (r_hist[i] + r_hist[i - 1])
        omega_mid = H_const / (m * (r_mid ** 2))
        phi_hist[i] = phi_hist[i - 1] + omega_mid * dt

x_hist = r_hist * np.cos(phi_hist)
y_hist = r_hist * np.sin(phi_hist)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.12, 1.08], height_ratios=[0.90, 1.10],
              left=0.04, right=0.97, top=0.87, bottom=0.08, wspace=0.14, hspace=0.28)

ax_orb = fig.add_subplot(gs[:, 0])
ax_bar = fig.add_subplot(gs[0, 1])
ax_tip = fig.add_subplot(gs[1, 1])

fig.suptitle(r"Concept Animation 2: Central-Force Motion ($\Sigma\mathbf{M}_O = \mathbf{0}$) — Why Decreasing $r$ Increases Speed!",
             fontsize=13.4, fontweight='bold', color='#111827', y=0.96)


def update(frame):
    rc = float(r_hist[frame])
    phic = float(phi_hist[frame])
    xc, yc = float(x_hist[frame]), float(y_hist[frame])
    v_th = H_const / (m * rc)
    T_curr = 0.5 * m * (v_th ** 2)

    ax_orb.clear()
    ax_bar.clear()
    ax_tip.clear()
    for ax in (ax_orb, ax_bar, ax_tip):
        ax.set_facecolor('#ffffff')

    ax_orb.set_xlim(-2.65, 2.65)
    ax_orb.set_ylim(-2.55, 2.75)
    ax_orb.set_aspect('equal')
    ax_orb.axis('off')
    ax_orb.set_title(r"1. Central Force Through $O$ ($d = 0 \Rightarrow \mathbf{M}_O = \mathbf{0}$) & Radial Contraction",
                     fontsize=11.0, fontweight='bold', color='#1e293b', pad=6)

    # Fixed top-left HUD pill
    ax_orb.text(-2.50, 2.36,
                rf"Live Readout:  $r = {rc:.2f}\ \mathrm{{m}}$,   $v_\theta = {v_th:.2f}\ \mathrm{{m/s}}$",
                fontsize=9.2, fontweight='bold', color='#047857', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.26', fc='#ecfdf5', ec='#6ee7b7', lw=1.2))

    th_c = np.linspace(0, 2 * np.pi, 160)
    ax_orb.plot(r1 * np.cos(th_c), r1 * np.sin(th_c), color='#94a3b8', ls='--', lw=1.4, zorder=1)
    ax_orb.plot(1.0 * np.cos(th_c), 1.0 * np.sin(th_c), color='#60a5fa', ls='--', lw=1.5, zorder=1)
    ax_orb.text(1.48, 1.52, r"$r_1 = 2.0\ \mathrm{m}$", fontsize=9.2, color='#475569', fontweight='bold')
    ax_orb.text(0.55, 0.85, r"$r_2 = 1.0\ \mathrm{m}$", fontsize=9.2, color='#1d4ed8', fontweight='bold')

    k0 = max(0, frame - 4)
    if frame >= 4:
        sec_phis = np.linspace(phi_hist[k0], phi_hist[frame], 20)
        sec_rs = np.linspace(r_hist[k0], r_hist[frame], 20)
        poly_pts = [(0.0, 0.0)] + [(rr * np.cos(pp), rr * np.sin(pp)) for rr, pp in zip(sec_rs, sec_phis)]
        ax_orb.add_patch(patches.Polygon(poly_pts, facecolor='#fde68a', edgecolor='#f59e0b', alpha=0.50, lw=1.0, zorder=2))

    ax_orb.plot(x_hist[:frame + 1], y_hist[:frame + 1], color='#0284c7', lw=2.0, alpha=0.8, zorder=3)

    ax_orb.add_patch(patches.Circle((0, 0), 0.11, facecolor='#1e293b', edgecolor='#0f172a', zorder=6))
    ax_orb.text(0.14, -0.22, '$O$', fontsize=12, fontweight='bold', color='#0f172a')
    ax_orb.plot([0, xc], [0, yc], color='#475569', lw=1.8, zorder=4)

    u_in = np.array([-xc, -yc]) / rc
    f_len = 0.58 if (16 <= frame < 48) else 0.42
    ax_orb.annotate('', xy=(xc + u_in[0] * f_len, yc + u_in[1] * f_len), xytext=(xc, yc),
                    arrowprops=dict(arrowstyle='-|>', color='#e11d48', lw=2.6, mutation_scale=15), zorder=7)
    u_perp = np.array([-u_in[1], u_in[0]])
    ax_orb.text(xc + u_in[0] * 0.48 + u_perp[0] * 0.24, yc + u_in[1] * 0.48 + u_perp[1] * 0.24,
                r"$\mathbf{F}$", fontsize=10.5, fontweight='bold', color='#be123c', ha='center', va='center')

    u_tan = np.array([-np.sin(phic), np.cos(phic)])
    v_draw = 0.28 * v_th
    ax_orb.annotate('', xy=(xc + u_tan[0] * v_draw, yc + u_tan[1] * v_draw), xytext=(xc, yc),
                    arrowprops=dict(arrowstyle='-|>', color='#059669', lw=2.8, mutation_scale=16), zorder=7)
    ax_orb.text(xc + u_tan[0] * (v_draw + 0.24), yc + u_tan[1] * (v_draw + 0.24),
                r"$\mathbf{v}_\theta$", fontsize=10.5, fontweight='bold', color='#047857', ha='center', va='center')

    ax_orb.add_patch(patches.Circle((xc, yc), 0.15, facecolor='#bae6fd', edgecolor='#0f172a', lw=1.8, zorder=6))

    if frame < 16:
        st_txt = r"State 1: Radius $r_1 = 2.0\ \mathrm{m},\ v_{\theta 1} = 2.0\ \mathrm{m/s}$"
    elif frame < 48:
        st_txt = r"Pulling cord: $\mathbf{F}$ passes through $O$ ($\Sigma M_O = 0$) $\Rightarrow r v_\theta = 4.0$ constant!"
    else:
        st_txt = r"State 2: Radius halved ($r_2 = 1.0\ \mathrm{m}$) $\Rightarrow$ Speed doubled ($v_{\theta 2} = 4.0\ \mathrm{m/s}$)!"
    ax_orb.text(0.0, -2.32, st_txt, fontsize=9.2, fontweight='bold', color='#1e3a8a', ha='center',
                bbox=dict(boxstyle='round,pad=0.32', fc='#eff6ff', ec='#93c5fd', lw=1.3))

    ax_bar.set_xlim(0, 6.4)
    ax_bar.set_ylim(-0.6, 2.7)
    ax_bar.set_yticks([0.0, 1.0, 2.0])
    ax_bar.set_yticklabels([r'Energy $T/T_1$', r'Speed $v_\theta/v_1$', r'Ang. Mom. $H_O/H_{O1}$'],
                           fontsize=9.2, fontweight='bold')
    ax_bar.set_title(r"2. Live Comparison: $H_O$ Conserved ($1\times$), Speed $2\times$, Energy $4\times$!",
                     fontsize=10.2, fontweight='bold', color='#1e293b', pad=6)
    ax_bar.axvline(1.0, color='#64748b', ls='--', lw=1.2)
    ax_bar.grid(axis='x', ls=':', alpha=0.5)

    ax_bar.barh(2.0, 1.0, height=0.50, color='#6ee7b7', edgecolor='#047857', lw=1.5)
    ax_bar.text(1.10, 2.0, rf"$H_O = {H_const:.1f}\ \mathrm{{kg\cdot m^2/s}}$ (Conserved!)",
                va='center', fontsize=8.8, fontweight='bold', color='#065f46')

    v_rat = v_th / v1
    ax_bar.barh(1.0, v_rat, height=0.50, color='#93c5fd', edgecolor='#1d4ed8', lw=1.4)
    ax_bar.text(v_rat + 0.10, 1.0, rf"$v_\theta / v_1 = r_1 / r = {v_rat:.2f}\times$",
                va='center', fontsize=8.8, fontweight='bold', color='#1e40af')

    T_rat = T_curr / T1
    ax_bar.barh(0.0, T_rat, height=0.50, color='#fda4af', edgecolor='#be123c', lw=1.4)
    ax_bar.text(T_rat + 0.10, 0.0, rf"$T / T_1 = (r_1/r)^2 = {T_rat:.2f}\times\ ({T_curr:.1f}\ \mathrm{{J}})$",
                va='center', fontsize=8.8, fontweight='bold', color='#9f1239')

    ax_tip.set_xlim(0, 10)
    ax_tip.set_ylim(0, 10)
    ax_tip.axis('off')

    bubble = (
        "[Callout] Why Does Kinetic Energy Increase 4x While H_O Is Conserved?\n"
        "• Because inward force " + r"$\mathbf{F}$" + " passes directly through " + r"$O$" + ", its moment arm is " + r"$d = 0 \Rightarrow \Sigma M_O = 0$" + "!\n"
        "  Hence angular momentum " + r"$H_O = m r v_\theta$" + " is 100% conserved (" + r"$r_1 v_{\theta 1} = r_2 v_{\theta 2}$" + ").\n"
        "• However, pulling the cord inward does positive radial work (" + r"$U_{1-2} > 0$" + "),\n"
        "  so kinetic energy " + r"$T = \frac{1}{2}mv^2$" + " increases fourfold! (Do not confuse $H_O$ with $T$!)"
    )
    ax_tip.text(0.15, 9.85, bubble, fontsize=8.9, color='#78350f', va='top', ha='left', linespacing=1.35,
                bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_card = (
        "Central-Force Conservation Summary (Skater Spin · Cord Table · Ex. 3.25 Comet):\n"
        + r"$\Sigma\mathbf{M}_O = \mathbf{r}\times\mathbf{F} = \mathbf{0} \;\Rightarrow\; (H_O)_1 = (H_O)_2 \;\Rightarrow\; m r_1 v_{\theta 1} = m r_2 v_{\theta 2}$" + "\n"
        + "• For gravitational orbits (Ex. 3.25), gravity is conservative, so both $H_O$ and $T + V_g$ are conserved!"
    )
    ax_tip.text(0.15, 3.55, eq_card, fontsize=8.9, color='#0f172a', va='top', ha='left', linespacing=1.38,
                bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4))


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_central_force_orbit.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=85)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved concept_central_force_orbit.gif")
