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
Problem 4/31 - Horizontal Force F Required to Hold Stationary Air-Jet Splitter Vane
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Quantitative verification:
  * Air density rho = 1.206 kg/m^3, volume flow rate Q = 0.2 m^3/s, jet speed v = 100 m/s
  * Mass flow rate m' = rho * Q = 1.206 * 0.2 = 0.2412 kg/s (~= 0.241 kg/s)
  * Sigma F_x = m' * Delta v_x -> F = 0.2412 * (0 - (-100)) = 24.12 N -> F = 24.1 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

rho = 1.206           # Air density (kg/m^3)
Q = 0.20              # Volume flow rate (m^3/s)
v_jet = 100.0         # Nozzle exit speed (m/s)
m_dot = rho * Q       # 0.2412 kg/s
F_val = m_dot * v_jet # 24.12 N -> 24.1 N

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_splitter_geometry(x_back=2.8, y_mid=4.2):
    R_cusp = 0.93
    x_tip = x_back + 0.42 + R_cusp
    ang1 = np.linspace(-np.pi / 2, -np.pi, 35)
    xu = x_tip + R_cusp * np.cos(ang1)
    yu = (y_mid + R_cusp) + R_cusp * np.sin(ang1)

    ang2 = np.linspace(np.pi, np.pi / 2, 35)
    xl = x_tip + R_cusp * np.cos(ang2)
    yl = (y_mid - R_cusp) + R_cusp * np.sin(ang2)

    poly_pts = np.vstack([
        [x_back, y_mid - 2.25],
        [x_back + 0.42, y_mid - 2.25],
        np.column_stack([xl, yl]),
        np.column_stack([xu, yu]),
        [x_back + 0.42, y_mid + 2.25],
        [x_back, y_mid + 2.25]
    ])
    return poly_pts, x_tip, R_cusp


vane_pts, x_tip, R_cusp = get_splitter_geometry(x_back=2.8, y_mid=4.2)


def update(frame):
    phase_t = (frame * 0.08) % 1.0
    x_back, y_mid = 2.8, 4.2

    # ---------------- 1. Left Panel: Air-Jet Splitter Vane Mechanism ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.4, 9.6)
    ax_main.set_ylim(0.8, 7.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    ax_main.plot([1.2, 9.1], [y_mid, y_mid], color='#777777', ls='--', lw=1.1, zorder=1)
    ax_main.text(9.2, y_mid, r'$x$', fontsize=11.5, fontweight='bold', va='center')
    ax_main.plot([x_back + 0.21, x_back + 0.21], [1.2, 7.1], color='#777777', ls='--', lw=1.1, zorder=1)
    ax_main.text(x_back + 0.21, 7.22, r'$y$', fontsize=11.5, fontweight='bold', ha='center')

    noz_x_tip = 6.35
    noz_x_base = 8.25
    noz_body = np.array([
        [noz_x_tip, y_mid - 0.36],
        [noz_x_base, y_mid - 0.50],
        [noz_x_base, y_mid + 0.50],
        [noz_x_tip, y_mid + 0.36]
    ])
    ax_main.add_patch(patches.Polygon(noz_body, facecolor='#ecc94b', edgecolor='#5c4811', lw=1.9, zorder=4))
    ax_main.add_patch(patches.FancyBboxPatch((noz_x_tip - 0.12, y_mid - 0.42), 0.16, 0.84,
                                             boxstyle='round,pad=0.04', facecolor='#f6e05e', edgecolor='#5c4811', lw=1.7, zorder=5))

    ax_main.fill_between([x_tip, noz_x_tip], y_mid - 0.32, y_mid + 0.32, color='#e1f5fe', alpha=0.65, zorder=2)
    ax_main.add_patch(patches.Polygon(vane_pts, facecolor='#b3d4e5', edgecolor='#263238', lw=2.0, zorder=4))

    for y_off in [-0.22, 0.0, 0.22]:
        for x_st in [5.95, 4.95]:
            if y_off == 0.0 and x_st == 5.95:
                continue
            ax_main.annotate('', xy=(x_st - 0.65, y_mid + y_off), xytext=(x_st, y_mid + y_off),
                             arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)
    ax_main.annotate('', xy=(4.75, y_mid), xytext=(5.55, y_mid),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.9, mutation_scale=12), zorder=5)
    ax_main.text(5.35, y_mid - 0.52, r'$v = 100\ \mathrm{m/s}$', fontsize=10.8, fontweight='bold', color='#00695c', ha='center')

    for sign in [+1, -1]:
        ang_a1 = np.radians(25)
        ang_a2 = np.radians(65)
        p1 = np.array([x_tip - R_cusp * np.sin(ang_a1), y_mid + sign * R_cusp * (1 - np.cos(ang_a1)) + sign * 0.14])
        p2 = np.array([x_tip - R_cusp * np.sin(ang_a2) + 0.14, y_mid + sign * R_cusp * (1 - np.cos(ang_a2)) + sign * 0.14])
        rad_val = -0.25 * sign
        ax_main.annotate('', xy=p2, xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11,
                                         connectionstyle=f'arc3,rad={rad_val}'), zorder=5)
        xv_line = x_back + 0.62
        y_st1 = y_mid + sign * 1.25
        y_ed1 = y_mid + sign * 1.85
        ax_main.annotate('', xy=(xv_line + 0.08, y_ed1), xytext=(xv_line + 0.08, y_st1),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)
        y_st2 = y_mid + sign * 2.00
        y_ed2 = y_mid + sign * 2.65
        ax_main.annotate('', xy=(xv_line - 0.04, y_ed2), xytext=(xv_line - 0.04, y_st2),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)

    for k in range(6):
        s_p = ((k / 6.0) + phase_t) % 1.0
        if s_p < 0.45:
            u_f = s_p / 0.45
            px = noz_x_tip - u_f * (noz_x_tip - x_tip)
            ax_main.plot(px, y_mid + 0.12, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, y_mid - 0.12, 'o', color='#0277bd', markersize=4.5, zorder=6)
        elif s_p < 0.75:
            u_f = (s_p - 0.45) / 0.30
            ang = u_f * (np.pi / 2)
            r_s = R_cusp - 0.16
            px = x_tip - r_s * np.sin(ang)
            py_u = y_mid + R_cusp - r_s * np.cos(ang)
            py_l = y_mid - R_cusp + r_s * np.cos(ang)
            ax_main.plot(px, py_u, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, py_l, 'o', color='#0277bd', markersize=4.5, zorder=6)
        else:
            u_f = (s_p - 0.75) / 0.25
            px = x_back + 0.58
            py_u = (y_mid + R_cusp) + u_f * 1.65
            py_l = (y_mid - R_cusp) - u_f * 1.65
            ax_main.plot(px, py_u, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, py_l, 'o', color='#0277bd', markersize=4.5, zorder=6)

    ax_main.annotate('', xy=(x_back, y_mid), xytext=(x_back - 1.45, y_mid),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=3.0, mutation_scale=17), zorder=6)
    ax_main.text(x_back - 1.55, y_mid, r'$F = 24.1\ \mathrm{N}$',
                 fontsize=11.8, fontweight='bold', color='#d32f2f', ha='right', va='center')

    ax_main.text(5.0, 1.15, r'Flow rate $Q = 0.2\ \mathrm{m^3/s}$,  Jet speed $v = 100\ \mathrm{m/s}$,  Air density $\rho = 1.206\ \mathrm{kg/m^3}$',
                 fontsize=10.0, fontweight='bold', color='#1d4564', ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    ax_main.set_title('Problem 4/31: Air Jet Impinging on Stationary Splitter Vane', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Control Volume FBD & Derivation ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.50, 'Control Volume FBD (Vane + Air Stream) & Momentum Change',
                 fontsize=10.8, fontweight='bold', ha='center', color='#1d4564')

    mini_pts = (vane_pts - np.array([x_back, y_mid])) * 0.48 + np.array([4.2, 7.85])
    ax_calc.add_patch(patches.Polygon(mini_pts, facecolor='#e1f5fe', edgecolor='#37474f', lw=1.6))
    ax_calc.annotate('', xy=(4.2, 7.85), xytext=(2.7, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14))
    ax_calc.text(2.55, 7.85, r'$F$', fontsize=11.5, fontweight='bold', color='#d32f2f', ha='right', va='center')

    ax_calc.annotate('', xy=(5.2, 7.85), xytext=(6.6, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
    ax_calc.text(6.75, 7.85, r'$v_{1x} = -100\ \mathrm{m/s}$', fontsize=9.8, fontweight='bold', color='#2e7d32', va='center')

    ax_calc.annotate('', xy=(4.45, 9.25), xytext=(4.45, 8.65),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.8, mutation_scale=11))
    ax_calc.annotate('', xy=(4.45, 6.45), xytext=(4.45, 7.05),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.8, mutation_scale=11))
    ax_calc.text(4.75, 9.05, r'$v_{2x} = 0$', fontsize=9.6, fontweight='bold', color='#2e7d32')

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$\Sigma F_x = m'\Delta v_x$" + ")]\n"
        r"1) Air mass flow rate ($m'$):" + "\n"
        r"   $m' = \rho Q = 1.206\ \mathrm{kg/m^3} \times 0.2\ \mathrm{m^3/s} = 0.2412\ \mathrm{kg/s}$" + "\n"
        r"2) Velocity change in $x$-direction ($\Delta v_x = v_{2x} - v_{1x}$, $+x$ right):" + "\n"
        r"   Inlet: $v_{1x} = -100\ \mathrm{m/s}$,  Exit (vertical split): $v_{2x} = 0$" + "\n"
        r"   $\Delta v_x = 0 - (-100) = +100\ \mathrm{m/s}$" + "\n"
        r"3) Horizontal force-momentum equation:" + "\n"
        r"   $\Sigma F_x = m'\Delta v_x \Rightarrow F = 0.2412(0 - [-100]) = \mathbf{24.1\ \mathrm{N}}$"
    )
    ax_calc.text(5.0, 4.15, sol_text, fontsize=9.4, ha='center', va='center', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.48', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_text = (
        f"[Quantitative Summary ($Q = {Q:.1f}\\ \\mathrm{{m^3/s}},\\ \\rho = {rho:.3f}\\ \\mathrm{{kg/m^3}}$)]\n"
        f"Mass flow: $m' = {m_dot:.4f}\\ \\mathrm{{kg/s}} \\approx 0.241\\ \\mathrm{{kg/s}}$  |  "
        f"Vertical $y$-momentum cancels ($\\Sigma F_y = 0$)\n"
        f"Required Horizontal Support Force (Theoretical Value): $\\mathbf{{F = {F_val:.1f}\\ \\mathrm{{N}}}}$"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.2, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_31_air_jet_vane.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
