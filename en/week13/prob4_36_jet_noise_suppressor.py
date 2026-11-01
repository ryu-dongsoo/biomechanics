# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

"""
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.6: Steady Mass Flow
Problem 4/36 - Tension T in Cable A Holding Mobile Jet-Engine Noise Suppressor Duct
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Quantitative verification:
  * Air intake rate m'_a = 43 kg/s, fuel burn rate m'_f = 0.8 kg/s -> Total exhaust flow m' = 43.8 kg/s
  * Exhaust velocity v_1 = 720 m/s (+x inlet), vertical discharge (+y) -> v_2x = 0
  * Sigma F_x = m' * Delta v_x -> -T * cos(15 deg) = (43 + 0.8) * (0 - 720) = -31,536 N
  * T = 31536 / cos(15 deg) = 32,648 N -> T = 32.6 kN (32 600 N)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m_dot_a = 43.0         # Air intake rate (kg/s)
m_dot_f = 0.8          # Fuel burn rate (kg/s)
m_dot = m_dot_a + m_dot_f  # 43.8 kg/s
v1 = 720.0             # Exhaust speed (m/s)
ang_cable_deg = 15.0   # Cable angle (deg)
ang_cable = np.radians(ang_cable_deg)

Fx_mag = m_dot * v1                    # 31,536 N
T_val = Fx_mag / np.cos(ang_cable)     # 32,648.5 N -> 32.6 kN

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_wheel(ax, wx, wy, r=0.22):
    ax.add_patch(patches.Circle((wx, wy), r, facecolor='#263238', edgecolor='#111111', lw=1.5, zorder=6))
    ax.add_patch(patches.Circle((wx, wy), r * 0.42, facecolor='#eceff1', edgecolor='#263238', lw=1.0, zorder=7))


def update(frame):
    phase_t = (frame * 0.09) % 1.0

    # ---------------- 1. Left Panel: Jet Aircraft + Noise Suppressor Duct ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.8)
    ax_main.set_ylim(0.8, 7.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    y_ground = 2.0
    ax_main.fill_between([0.4, 9.4], y_ground - 0.45, y_ground, color='#e5dfd5', zorder=1)
    ax_main.plot([0.4, 9.4], [y_ground, y_ground], color='#333333', lw=2.0, zorder=3)

    # 1) Ground test jet aircraft
    jet_body = np.array([
        [0.65, 2.95],
        [1.55, 3.22],
        [2.35, 3.45],
        [3.15, 3.30],
        [4.55, 3.24],
        [5.15, 4.15],
        [5.48, 4.15],
        [5.32, 3.28],
        [5.48, 3.25],
        [5.48, 2.98],
        [4.55, 2.86],
        [2.45, 2.80],
        [1.55, 2.82]
    ])
    ax_main.add_patch(patches.Polygon(jet_body, facecolor='#cfd8dc', edgecolor='#263238', lw=1.8, zorder=4))

    canopy_pts = np.array([
        [1.60, 3.20],
        [2.35, 3.43],
        [3.05, 3.28],
        [2.35, 3.16]
    ])
    ax_main.add_patch(patches.Polygon(canopy_pts, facecolor='#81d4fa', edgecolor='#0277bd', lw=1.3, zorder=5))

    wing_pts = np.array([
        [2.55, 3.05],
        [4.15, 2.92],
        [4.35, 3.04],
        [2.95, 3.12]
    ])
    ax_main.add_patch(patches.Polygon(wing_pts, facecolor='#90a4ae', edgecolor='#263238', lw=1.4, zorder=5))

    ax_main.plot([1.72, 1.55], [2.82, y_ground + 0.18], color='#263238', lw=2.2, zorder=3)
    draw_wheel(ax_main, 1.55, y_ground + 0.18, r=0.18)
    ax_main.plot([3.55, 3.55], [2.80, y_ground + 0.24], color='#263238', lw=2.6, zorder=3)
    draw_wheel(ax_main, 3.55, y_ground + 0.24, r=0.24)

    ax_main.fill_between([5.48, 5.85], 3.00, 3.23, color='#64b5f6', alpha=0.75, zorder=3)

    # 2) Mobile noise suppressor duct
    duct_segs = [
        np.array([[5.82, 2.90], [6.45, 2.72], [6.45, 3.52], [5.82, 3.34]]),
        np.array([[6.45, 2.72], [7.25, 2.78], [7.25, 3.62], [6.45, 3.52]]),
        np.array([[7.25, 2.78], [7.95, 3.02], [7.62, 3.88], [7.25, 3.62]]),
        np.array([[7.95, 3.02], [8.42, 3.58], [7.82, 4.25], [7.62, 3.88]]),
        np.array([[8.42, 3.58], [8.62, 4.45], [7.88, 4.65], [7.82, 4.25]]),
        np.array([[8.62, 4.45], [8.70, 5.10], [7.85, 5.10], [7.88, 4.65]])
    ]
    colors_duct = ['#b0bec5', '#cfd8dc', '#b0bec5', '#cfd8dc', '#b0bec5', '#cfd8dc']
    for seg, col in zip(duct_segs, colors_duct):
        ax_main.add_patch(patches.Polygon(seg, facecolor=col, edgecolor='#37474f', lw=1.6, zorder=4))

    ax_main.plot([7.82, 8.73], [5.10, 5.10], color='#263238', lw=2.4, zorder=5)

    # Support columns and wheels
    ax_main.add_patch(patches.Rectangle((6.25, 2.52), 0.14, 1.15, facecolor='#90caf9', edgecolor='#1d4564', lw=1.5, zorder=5))
    ax_main.plot([6.32, 6.32], [2.52, y_ground + 0.22], color='#263238', lw=2.4, zorder=4)
    draw_wheel(ax_main, 6.32, y_ground + 0.22, r=0.22)

    ax_main.add_patch(patches.Rectangle((8.88, 2.52), 0.14, 2.58, facecolor='#90caf9', edgecolor='#1d4564', lw=1.5, zorder=5))
    ax_main.plot([8.52, 8.88], [4.00, 4.00], color='#263238', lw=2.2, zorder=3)
    ax_main.plot([8.66, 8.88], [4.82, 4.82], color='#263238', lw=2.2, zorder=3)
    ax_main.plot([8.95, 8.95], [2.52, y_ground + 0.22], color='#263238', lw=2.4, zorder=4)
    draw_wheel(ax_main, 8.95, y_ground + 0.22, r=0.22)

    # 3) Holding cable A (15 deg)
    p_anchor = np.array([4.65, y_ground])
    p_attach = np.array([6.25, y_ground + 1.60 * np.tan(ang_cable)])
    ax_main.plot([p_anchor[0], p_attach[0]], [p_anchor[1], p_attach[1]], color='#d32f2f', lw=2.6, zorder=6)
    ax_main.plot(p_anchor[0], p_anchor[1], 'ko', markersize=4.5, zorder=7)
    ax_main.plot(p_attach[0], p_attach[1], 'ko', markersize=4.5, zorder=7)
    ax_main.text(5.28, 2.38, r'$A\ (T)$', fontsize=11.2, fontweight='bold', color='#d32f2f', ha='center')

    arc_c = patches.Arc(p_anchor, 1.5, 1.5, angle=0, theta1=0, theta2=ang_cable_deg, color='#222222', lw=1.4)
    ax_main.add_patch(arc_c)
    ax_main.text(p_anchor[0] + 1.05, y_ground + 0.14, r'$15^\circ$', fontsize=10.0, fontweight='bold')

    # 4) Vertical exhaust arrows and moving particles
    for x_arr in [8.02, 8.28, 8.54]:
        ax_main.annotate('', xy=(x_arr, 6.25), xytext=(x_arr, 5.25),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.2, mutation_scale=13), zorder=5)
    ax_main.text(8.28, 6.45, r'Vertical Exhaust ($v_{2x} = 0$)', fontsize=10.2, fontweight='bold', color='#00695c', ha='center')

    path_pts = np.array([
        [5.65, 3.12],
        [6.35, 3.12],
        [7.15, 3.20],
        [7.75, 3.45],
        [8.12, 4.00],
        [8.25, 4.65],
        [8.28, 5.45],
        [8.28, 6.10]
    ])
    for k in range(6):
        s_p = ((k / 6.0) + phase_t) % 1.0
        idx_f = s_p * (len(path_pts) - 1)
        i0 = int(np.floor(idx_f))
        i1 = min(i0 + 1, len(path_pts) - 1)
        w = idx_f - i0
        pt = (1 - w) * path_pts[i0] + w * path_pts[i1]
        ax_main.plot(pt[0], pt[1], 'o', color='#e65100', markersize=4.8, zorder=6)

    ax_main.text(5.0, 1.08,
                 r"Air intake $m'_a = 43\ \mathrm{kg/s}$,  Fuel burn $m'_f = 0.8\ \mathrm{kg/s}$,  Exhaust speed $v_1 = 720\ \mathrm{m/s}$",
                 fontsize=9.8, fontweight='bold', color='#1d4564', ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    ax_main.set_title('Problem 4/36: Jet-Engine Noise Suppressor Cable Tension $T$', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Duct FBD & Derivation ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.50, 'Noise Suppressor Duct FBD & Inlet/Exit Velocities',
                 fontsize=10.8, fontweight='bold', ha='center', color='#1d4564')

    fbd_duct = np.array([
        [3.2, 7.2],
        [5.4, 7.0],
        [6.5, 7.4],
        [6.8, 8.7],
        [5.7, 8.7],
        [5.5, 8.0],
        [3.2, 7.8]
    ])
    ax_calc.add_patch(patches.Polygon(fbd_duct, facecolor='#eceff1', edgecolor='#263238', lw=1.8))

    ax_calc.annotate('', xy=(3.1, 7.5), xytext=(1.7, 7.5),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=13))
    ax_calc.text(2.4, 7.80, r'$v_1 = 720\ \mathrm{m/s}$', fontsize=9.6, fontweight='bold', color='#2e7d32', ha='center')

    ax_calc.annotate('', xy=(6.25, 9.55), xytext=(6.25, 8.75),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=13))
    ax_calc.text(6.65, 9.20, r'$v_2\ (v_{2x}=0)$', fontsize=9.6, fontweight='bold', color='#2e7d32', va='center')

    ax_calc.annotate('', xy=(2.1, 6.75), xytext=(3.5, 7.12),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14))
    ax_calc.text(1.95, 6.70, r'$T\ (15^\circ)$', fontsize=10.2, fontweight='bold', color='#d32f2f', ha='right', va='center')

    ax_calc.annotate('', xy=(3.8, 7.10), xytext=(3.8, 6.30),
                     arrowprops=dict(arrowstyle='->', color='#78909c', lw=1.8, mutation_scale=11))
    ax_calc.text(4.05, 6.45, r'$R_1$', fontsize=9.3, fontweight='bold', color='#546e7a')
    ax_calc.annotate('', xy=(6.4, 7.35), xytext=(6.4, 6.30),
                     arrowprops=dict(arrowstyle='->', color='#78909c', lw=1.8, mutation_scale=11))
    ax_calc.text(6.65, 6.45, r'$R_2$', fontsize=9.3, fontweight='bold', color='#546e7a')

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$\Sigma F_x = m'\Delta v_x$" + ")]\n"
        r"1) Total exhaust mass flow rate entering suppressor ($m'$):" + "\n"
        r"   $m' = m'_a + m'_f = 43 + 0.8 = 43.8\ \mathrm{kg/s}$" + "\n"
        r"2) Horizontal ($+x$) velocity change ($\Delta v_x = v_{2x} - v_{1x}$):" + "\n"
        r"   Inlet: $v_{1x} = +720\ \mathrm{m/s}$,  Exit (vertical): $v_{2x} = 0$" + "\n"
        r"3) Horizontal force-momentum equation:" + "\n"
        r"   $-T\cos 15^\circ = (43 + 0.8)(0 - 720) = -31,536\ \mathrm{N}$" + "\n"
        r"   $\Rightarrow T = \frac{31,536}{\cos 15^\circ} = 32,648\ \mathrm{N} \approx \mathbf{32.6\ \mathrm{kN}}$"
    )
    ax_calc.text(5.0, 4.05, sol_text, fontsize=9.3, ha='center', va='center', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.48', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_text = (
        f"[Quantitative Summary ($m' = {m_dot:.1f}\\ \\mathrm{{kg/s}},\\ \\Delta v_x = -{v1:.0f}\\ \\mathrm{{m/s}}$)]\n"
        f"Horizontal momentum force: $|m'\\Delta v_x| = {Fx_mag:,.0f}\\ \\mathrm{{N}} = {Fx_mag/1000:.2f}\\ \\mathrm{{kN}}$\n"
        f"Cable A Tension (Theoretical Value): $\\mathbf{{T = 32,600\\ \\mathrm{{N}} = 32.6\\ \\mathrm{{kN}}}}$"
    )
    ax_calc.text(5.0, 1.10, live_text, fontsize=9.2, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_36_jet_noise_suppressor.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
