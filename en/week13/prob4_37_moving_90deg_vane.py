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
Problem 4/37 - Forces Fx and Fy Required to Drive 90-deg Vane Moving Against Water Jet
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Quantitative verification:
  * Nozzle diameter d = 25 mm = 0.025 m, jet speed v = 20 m/s (right), vane speed u = 10 m/s (left, +x)
  * Relative speed v_rel = v + u = 20 + 10 = 30 m/s
  * Mass flow rate m' = rho * A * v_rel = 1000 * (pi/4)*(0.025)^2 * (20 + 10) = 14.726 kg/s (~= 14.73 kg/s)
  * Final absolute velocity: v'_x = +u = +10 m/s (left), v'_y = +v_rel = +30 m/s (upward)
  * Sigma F_x = m' * Delta v_x -> F_x = 14.73 * (10 - (-20)) = 442 N
  * Sigma F_y = m' * Delta v_y -> F_y = 14.73 * (20 + 10 - 0) = 442 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

rho = 1000.0
d = 0.025
A = 0.25 * np.pi * d**2      # 4.9087e-4 m^2
v_jet = 20.0                 # Jet speed to the right (m/s)
u_vane = 10.0                # Vane speed to the left (m/s)
v_rel = v_jet + u_vane       # 30.0 m/s
m_dot = rho * A * v_rel      # 14.7262 kg/s (~= 14.73 kg/s)

Fx_val = m_dot * (u_vane - (-v_jet))  # 441.79 N -> 442 N
Fy_val = m_dot * (v_rel - 0.0)        # 441.79 N -> 442 N

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_90deg_vane_shapes(x_lip, y_jet, R_arc=2.15, jet_h=0.38):
    r_water_center = R_arc
    cx, cy = x_lip, y_jet + r_water_center
    ang = np.linspace(-np.pi / 2, 0.0, 40)

    r_in = R_arc - jet_h / 2
    r_out = R_arc + jet_h / 2
    xw_in = cx + r_in * np.cos(ang)
    yw_in = cy + r_in * np.sin(ang)
    xw_out = cx + r_out * np.cos(ang)
    yw_out = cy + r_out * np.sin(ang)

    r_liner = r_out + 0.14
    xl_out = cx + r_liner * np.cos(ang)
    yl_out = cy + r_liner * np.sin(ang)
    liner_poly = np.vstack([
        np.column_stack([xw_out, yw_out]),
        np.column_stack([xl_out[::-1], yl_out[::-1]])
    ])

    x_back = cx + r_liner + 0.38
    y_bot = y_jet - jet_h / 2 - 0.42
    y_top = cy
    block_poly = np.vstack([
        [x_lip, y_bot],
        [x_back, y_bot],
        [x_back, y_top],
        [cx + r_liner, y_top],
        np.column_stack([xl_out[::-1], yl_out[::-1]])
    ])

    return (cx, cy, r_in, r_out, xw_in, yw_in, xw_out, yw_out, liner_poly, block_poly, x_back, y_bot, y_top)


def update(frame):
    phase_t = (frame * 0.09) % 1.0
    x_lip = 4.85 - 1.25 * (frame / (n_frames - 1))
    y_jet = 2.65
    jet_h = 0.38
    R_arc = 2.10

    (cx, cy, r_in, r_out, xw_in, yw_in, xw_out, yw_out,
     liner_poly, block_poly, x_back, y_bot, y_top) = get_90deg_vane_shapes(x_lip, y_jet, R_arc, jet_h)

    # ---------------- 1. Left Panel: 90-deg Moving Vane Mechanism ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(0.8, 7.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    ax_main.plot([0.65, 2.1], [y_jet, y_jet], color='#555555', ls='--', lw=1.2, zorder=1)
    ax_main.text(0.48, y_jet, r'$x$', fontsize=11.5, fontweight='bold', va='center')
    x_exit_center = cx + 0.5 * (r_in + r_out)
    ax_main.plot([x_exit_center, x_exit_center], [y_top + 0.2, 7.15], color='#555555', ls='--', lw=1.2, zorder=1)
    ax_main.text(x_exit_center, 7.30, r'$y$', fontsize=11.5, fontweight='bold', ha='center')

    noz_x0, noz_x1 = 1.45, 2.75
    noz_poly = np.array([
        [noz_x0, y_jet - 0.30],
        [noz_x1, y_jet - jet_h / 2],
        [noz_x1, y_jet + jet_h / 2],
        [noz_x0, y_jet + 0.30]
    ])
    ax_main.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.9, zorder=4))
    ax_main.add_patch(patches.Ellipse((noz_x0, y_jet), 0.14, 0.60, facecolor='#b8860b', edgecolor='#5c4811', lw=1.5, zorder=5))

    ax_main.fill_between([noz_x1, x_lip], y_jet - jet_h / 2, y_jet + jet_h / 2,
                         color='#cce7f8', alpha=0.88, zorder=2)
    ax_main.plot([noz_x1, x_lip], [y_jet + jet_h / 2, y_jet + jet_h / 2], color='#90caf9', lw=1.2, zorder=3)
    ax_main.plot([noz_x1, x_lip], [y_jet - jet_h / 2, y_jet - jet_h / 2], color='#90caf9', lw=1.2, zorder=3)

    y_plume_top = y_top + 1.45
    stream_poly = np.vstack([
        np.column_stack([xw_in, yw_in]),
        [cx + r_in, y_plume_top],
        [cx + r_out, y_plume_top],
        np.column_stack([xw_out[::-1], yw_out[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(stream_poly, facecolor='#cce7f8', edgecolor='#90caf9', lw=1.1, alpha=0.88, zorder=2))

    ax_main.add_patch(patches.Polygon(block_poly, facecolor='#e2b49a', edgecolor='#3e2723', lw=1.8, zorder=4))
    ax_main.add_patch(patches.Polygon(liner_poly, facecolor='#81b29a', edgecolor='#1b4332', lw=1.6, zorder=5))

    x_arr_in = 0.5 * (noz_x1 + x_lip)
    ax_main.annotate('', xy=(x_arr_in + 0.42, y_jet), xytext=(x_arr_in - 0.42, y_jet),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.2, mutation_scale=13), zorder=5)
    ax_main.text(x_arr_in + 0.15, y_jet + 0.52, r'$20\ \mathrm{m/s}$', fontsize=10.8, fontweight='bold', color='#111111')
    ax_main.annotate('', xy=(x_arr_in - 0.05, y_jet + 0.06), xytext=(x_arr_in + 0.12, y_jet + 0.48),
                     arrowprops=dict(arrowstyle='-', color='#333333', lw=0.9, connectionstyle='arc3,rad=0.25'), zorder=5)

    for ang_deg_a in [-65, -25]:
        a1 = np.radians(ang_deg_a - 12)
        a2 = np.radians(ang_deg_a + 12)
        rm = 0.5 * (r_in + r_out)
        p1 = np.array([cx + rm * np.cos(a1), cy + rm * np.sin(a1)])
        p2 = np.array([cx + rm * np.cos(a2), cy + rm * np.sin(a2)])
        ax_main.annotate('', xy=p2, xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.1, mutation_scale=12,
                                         connectionstyle='arc3,rad=0.2'), zorder=5)

    rm = 0.5 * (r_in + r_out)
    for k in range(6):
        s_p = ((k / 6.0) + phase_t) % 1.0
        ang_p = -np.pi / 2 + s_p * (np.pi / 2)
        ax_main.plot(cx + rm * np.cos(ang_p), cy + rm * np.sin(ang_p), 'o', color='#0277bd', markersize=4.5, zorder=6)

    ax_main.annotate('', xy=(x_lip + 0.05, y_bot - 0.25), xytext=(x_lip + 0.95, y_bot - 0.25),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13), zorder=6)
    ax_main.text(x_lip + 0.50, y_bot - 0.62, r'$10\ \mathrm{m/s}$', fontsize=10.8, fontweight='bold', color='#111111', ha='center')

    ax_main.annotate('', xy=(x_back, y_bot + 0.65), xytext=(x_back + 1.25, y_bot + 0.65),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=16), zorder=6)
    ax_main.text(x_back + 1.32, y_bot + 0.65, r'$F_x = 442\ \mathrm{N}$',
                 fontsize=11.2, fontweight='bold', color='#d32f2f', va='center')

    x_fy = x_back - 0.55
    ax_main.annotate('', xy=(x_fy, y_bot), xytext=(x_fy, y_bot - 1.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=16), zorder=6)
    ax_main.text(x_fy, y_bot - 1.38, r'$F_y = 442\ \mathrm{N}$',
                 fontsize=11.2, fontweight='bold', color='#d32f2f', ha='center')

    ax_main.set_title('Problem 4/37: $90^\\circ$ Vane Moving Against Water Jet', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Velocity Triangle & Derivation ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.50, r"Exit Velocity Addition ($\mathbf{v}' = \mathbf{u} + \mathbf{v}_{\mathrm{rel}}$) & Relative Mass Flow",
                 fontsize=10.6, fontweight='bold', ha='center', color='#1d4564')

    p_br = np.array([5.8, 6.75])
    p_bl = np.array([3.8, 6.75])
    p_tl = np.array([3.8, 9.05])
    p_tr = np.array([5.8, 9.05])

    ax_calc.plot([p_bl[0], p_tl[0]], [p_bl[1], p_tl[1]], color='#90a4ae', ls='--', lw=1.2)
    ax_calc.plot([p_tl[0], p_tr[0]], [p_tl[1], p_tr[1]], color='#90a4ae', ls='--', lw=1.2)

    ax_calc.annotate('', xy=p_bl, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=13))
    ax_calc.text(4.8, 6.42, r'$u = 10\ \mathrm{m/s}\ (+x)$', fontsize=9.8, fontweight='bold', color='#1565c0', ha='center')

    ax_calc.annotate('', xy=p_tr, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13))
    ax_calc.text(6.05, 7.90, r'$v_{\mathrm{rel}} = v + u = 30\ \mathrm{m/s}\ (+y)$',
                 fontsize=9.8, fontweight='bold', color='#00897b', va='center')

    ax_calc.annotate('', xy=p_tl, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(4.25, 8.15, r"$\mathbf{v}'$", fontsize=11.5, fontweight='bold', color='#2e7d32', ha='right')

    ax_calc.annotate('', xy=(1.2, 7.2), xytext=(2.4, 7.2),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))
    ax_calc.text(1.0, 7.2, r'$+x$', fontsize=10, fontweight='bold', va='center', ha='right')
    ax_calc.annotate('', xy=(2.4, 8.4), xytext=(2.4, 7.2),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))
    ax_calc.text(2.4, 8.55, r'$+y$', fontsize=10, fontweight='bold', ha='center')

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$v_{\mathrm{rel}} = v + u$" + ")]\n"
        r"1) Relative speed & effective mass flow rate ($m'$):" + "\n"
        r"   $v_{\mathrm{rel}} = v + u = 20 + 10 = 30\ \mathrm{m/s}$" + "\n"
        r"   $m' = \rho A v_{\mathrm{rel}} = 1000\left(\frac{\pi}{4}\right)(0.025)^2(20 + 10) = \mathbf{14.73\ \mathrm{kg/s}}$" + "\n"
        r"2) Exit absolute velocity ($\mathbf{v}' = \mathbf{u} + \mathbf{v}_{\mathrm{rel}}$, $+x$ left, $+y$ up):" + "\n"
        r"   Inlet: $v_{1x} = -20\ \mathrm{m/s},\ v_{1y} = 0$  |  Exit: $v'_{x} = +10\ \mathrm{m/s},\ v'_{y} = +30\ \mathrm{m/s}$" + "\n"
        r"3) Force-momentum equations ($\Sigma F = m'\Delta v$):" + "\n"
        r"   $\Sigma F_x = m'\Delta v_x:\ F_x = 14.73(10 - [-20]) = \mathbf{442\ \mathrm{N}}$" + "\n"
        r"   $\Sigma F_y = m'\Delta v_y:\ F_y = 14.73(20 + 10 - 0) = \mathbf{442\ \mathrm{N}}$"
    )
    ax_calc.text(5.0, 3.90, sol_text, fontsize=9.2, ha='center', va='center', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_text = (
        f"[Quantitative Summary ($d = 25\\ \\mathrm{{mm}},\\ v = 20\\ \\mathrm{{m/s}},\\ u = 10\\ \\mathrm{{m/s}}$)]\n"
        f"Relative mass flow: $m' = {m_dot:.2f}\\ \\mathrm{{kg/s}}$  |  Velocity change: $\\Delta v_x = +30\\ \\mathrm{{m/s}},\\ \\Delta v_y = +30\\ \\mathrm{{m/s}}$\n"
        f"Theoretical Values: $\\mathbf{{F_x = {Fx_val:.0f}\\ \\mathrm{{N}}}}$,   $\\mathbf{{F_y = {Fy_val:.0f}\\ \\mathrm{{N}}}}$"
    )
    ax_calc.text(5.0, 1.05, live_text, fontsize=9.2, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_37_moving_90deg_vane.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
