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
Sample Problem 4/7 - Optimum Vane Speed for Maximum Power (u = v/3)
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Theoretical validation:
  * Single moving vane power: P = F*u = rho*A*(v - u)^2 * u * (1 - cos(theta))
  * Extremum condition: dP/du = rho*A*(1 - cos(theta))*(v^2 - 4*u*v + 3*u^2) = 0 -> (v - 3u)(v - u) = 0
  * Optimum speed: u_opt = v / 3 (Single vane), Note: Multi-blade turbine wheel (m'=rho*A*v) has u_opt = v / 2
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
A = 0.002
v = 15.0
theta_deg = 120.0
theta = np.radians(theta_deg)

n_frames = 50
ratio_vals = np.linspace(0.02, 0.98, n_frames)  # u / v

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_vane_curve(x0, y0, R_arc=1.7, th_max=theta):
    ang = np.linspace(-np.pi / 2, -np.pi / 2 + th_max, 40)
    cx, cy = x0, y0 + R_arc
    xs = cx + R_arc * np.cos(ang)
    ys = cy + R_arc * np.sin(ang)
    nx = -np.cos(ang)
    ny = -np.sin(ang)
    return xs, ys, nx, ny


def update(frame):
    r_curr = ratio_vals[frame]
    u_curr = r_curr * v
    phase_t = (frame * 0.09) % 1.0

    # ---------------- 1. Left Panel: Physical Mechanism + Power Curve ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 10.0)
    ax_main.set_ylim(0, 9.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    y_jet = 5.8
    x_vane = 2.8 + 2.8 * r_curr
    xs, ys, nx, ny = get_vane_curve(x_vane, y_jet, R_arc=1.55, th_max=theta)
    jet_h = 0.30
    vane_thick = 0.20

    # Nozzle
    noz_x0, noz_x1 = 0.5, 1.7
    noz_poly = np.array([
        [noz_x0, y_jet - 0.28],
        [noz_x1, y_jet - jet_h / 2],
        [noz_x1, y_jet + jet_h / 2],
        [noz_x0, y_jet + 0.28]
    ])
    ax_main.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.8, zorder=4))

    # Incoming fluid stream
    ax_main.fill_between([noz_x1, x_vane], y_jet - jet_h / 2, y_jet + jet_h / 2,
                         color='#bbdefb', alpha=0.85, zorder=2)
    ax_main.plot([noz_x1, x_vane], [y_jet + jet_h / 2, y_jet + jet_h / 2], color='#1976d2', lw=1.2, zorder=3)
    ax_main.plot([noz_x1, x_vane], [y_jet - jet_h / 2, y_jet - jet_h / 2], color='#1976d2', lw=1.2, zorder=3)

    # Stream along vane
    upper_x = xs + (jet_h / 2) * nx
    upper_y = ys + (jet_h / 2) * ny
    lower_x = xs - (jet_h / 2) * nx
    lower_y = ys - (jet_h / 2) * ny
    stream_poly = np.column_stack([
        np.concatenate([lower_x, upper_x[::-1]]),
        np.concatenate([lower_y, upper_y[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(stream_poly, facecolor='#bbdefb', edgecolor='#1976d2', lw=1.2, alpha=0.85, zorder=2))

    for k in range(5):
        frac = ((k / 5.0) + phase_t * (1.0 - r_curr)) % 1.0
        idx = int(frac * (len(xs) - 1))
        ax_main.plot(xs[idx], ys[idx], 'o', color='#0d47a1', markersize=4.2, zorder=4)

    # Vane body
    vane_top_x = xs - (jet_h / 2) * nx
    vane_top_y = ys - (jet_h / 2) * ny
    vane_bot_x = xs - (jet_h / 2 + vane_thick) * nx
    vane_bot_y = ys - (jet_h / 2 + vane_thick) * ny
    vane_poly = np.column_stack([
        np.concatenate([vane_bot_x, vane_top_x[::-1]]),
        np.concatenate([vane_bot_y, vane_top_y[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(vane_poly, facecolor='#78909c', edgecolor='#263238', lw=2.0, zorder=5))

    # Inlet jet speed v
    ax_main.annotate('', xy=(noz_x1 + 0.95, y_jet), xytext=(noz_x1 + 0.1, y_jet),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=6)
    ax_main.text(noz_x1 + 0.52, y_jet + 0.26, f'$v = {v:.0f}\\ \\mathrm{{m/s}}$',
                 fontsize=10.0, fontweight='bold', color='#2e7d32', ha='center')

    # Driving force F_fluid and vane speed u
    mid_i = len(xs) // 3
    px_f, py_f = vane_bot_x[mid_i], vane_bot_y[mid_i]
    f_scale = 1.4 * (1.0 - r_curr)**2
    if f_scale > 0.12:
        ax_main.annotate('', xy=(px_f + f_scale + 0.25, py_f), xytext=(px_f + 0.05, py_f),
                         arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14), zorder=6)
    ax_main.text(px_f + max(f_scale, 0.2) + 0.32, py_f + 0.08, r'$F_{\mathrm{fluid}} = F$',
                 fontsize=10.2, fontweight='bold', color='#d32f2f', va='center')

    u_scale = 1.4 * r_curr
    ax_main.annotate('', xy=(px_f + u_scale + 0.25, py_f - 0.50), xytext=(px_f + 0.05, py_f - 0.50),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=13), zorder=6)
    ax_main.text(px_f + u_scale + 0.32, py_f - 0.50,
                 f'$u = {u_curr:.2f}\\ \\mathrm{{m/s}}\\ ({r_curr:.2f}v)$',
                 fontsize=10.0, fontweight='bold', color='#1565c0', va='center')

    ax_main.text(0.5, 8.55, r'Power Transferred to Vane: $P = F \cdot u = \rho A(v-u)^2 u(1-\cos\theta)$',
                 fontsize=10.2, fontweight='bold', color='#1d4564',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    # ---------------- Bottom Half: Power Curve P(u/v) ----------------
    gx0, gy0 = 1.2, 0.95
    gw, gh = 7.8, 3.25

    ax_main.annotate('', xy=(gx0 + gw + 0.3, gy0), xytext=(gx0, gy0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.6))
    ax_main.annotate('', xy=(gx0, gy0 + gh + 0.3), xytext=(gx0, gy0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.6))
    ax_main.text(gx0 + gw + 0.35, gy0, r'$u / v$', fontsize=11, fontweight='bold', va='center')
    ax_main.text(gx0, gy0 + gh + 0.38, r'Power $P / P_{\max}$', fontsize=10.2, fontweight='bold', ha='center')

    r_grid = np.linspace(0, 1.0, 200)
    p_single_norm = (27.0 / 4.0) * ((1.0 - r_grid)**2) * r_grid
    p_turb_norm = 4.0 * (1.0 - r_grid) * r_grid * 0.85

    ax_main.plot(gx0 + r_grid * gw, gy0 + p_single_norm * gh, color='#d32f2f', lw=2.5, label='Single Vane')
    ax_main.plot(gx0 + r_grid * gw, gy0 + p_turb_norm * gh, color='#78909c', ls='--', lw=1.6)

    x_opt = gx0 + (1.0 / 3.0) * gw
    y_opt = gy0 + 1.0 * gh
    ax_main.plot([x_opt, x_opt], [gy0, y_opt], color='#2e7d32', ls=':', lw=1.6)
    ax_main.plot(x_opt, y_opt, 'o', color='#2e7d32', markersize=7, zorder=5)
    ax_main.text(x_opt, y_opt + 0.18, r'Max Power ($u = \frac{v}{3}$)', fontsize=10.0,
                 fontweight='bold', color='#2e7d32', ha='center')

    x_turb = gx0 + 0.5 * gw
    y_turb = gy0 + 0.85 * gh
    ax_main.plot([x_turb, x_turb], [gy0, y_turb], color='#607d8b', ls=':', lw=1.2)
    ax_main.text(x_turb + 0.15, y_turb + 0.08, r'Multi-Blade Turbine ($u = \frac{v}{2}$)',
                 fontsize=9.0, color='#455a64', fontweight='bold')

    for rv, lbl in [(0.0, '0'), (1.0/3.0, '1/3'), (0.5, '1/2'), (1.0, '1.0')]:
        xp = gx0 + rv * gw
        ax_main.plot([xp, xp], [gy0 - 0.08, gy0 + 0.08], color='#222222', lw=1.3)
        ax_main.text(xp, gy0 - 0.32, lbl, fontsize=9.6, fontweight='bold', ha='center')

    p_curr_norm = (27.0 / 4.0) * ((1.0 - r_curr)**2) * r_curr
    xc = gx0 + r_curr * gw
    yc = gy0 + p_curr_norm * gh
    ax_main.plot([xc, xc], [gy0, yc], color='#1565c0', lw=1.4, alpha=0.7)
    ax_main.plot(xc, yc, 'o', color='#1565c0', markersize=8.5, zorder=6)

    ax_main.set_title('Sample Problem 4/7: Optimum Vane Speed for Max Power ($u = v / 3$)',
                      fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Derivation & Live Monitor ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.45, 'Power Mechanism ($P = F \\cdot u$) & Extremum Condition',
                 fontsize=11.2, fontweight='bold', ha='center', color='#1d4564')

    box_top = (
        "• Power Definition: Normal force " + r"$R \perp u \Rightarrow U_R = 0$" + "\n"
        r"   Power developed by fluid force $F$ on moving vane:" + "\n"
        r"   $P = F u = \rho A(v - u)^2 u (1 - \cos\theta)$"
    )
    ax_calc.text(5.0, 8.20, box_top, fontsize=9.6, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8f9fa', edgecolor='#cfd8dc'))

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$dP / du = 0$" + ")]\n"
        r"1) Expand power polynomial in $u$:" + "\n"
        r"   $P(u) = \rho A(1 - \cos\theta)(v^2 u - 2 v u^2 + u^3)$" + "\n"
        r"2) Differentiate with respect to $u$ ($\frac{dP}{du} = 0$):" + "\n"
        r"   $\frac{dP}{du} = \rho A(1 - \cos\theta)(v^2 - 4 u v + 3 u^2) = 0$" + "\n"
        r"   $\Rightarrow (v - 3u)(v - u) = 0$" + "\n"
        r"3) Optimum speed & max power (single vane):" + "\n"
        "   " + r"$\mathbf{u_{\mathrm{opt}} = \frac{v}{3}}$" + "   (" + r"$u = v$" + " gives minimum " + r"$P = 0$" + ")\n"
        r"   $P_{\max} = \frac{4}{27}\rho A v^3(1 - \cos\theta)$  (Note: Turbine wheel gives $u = \frac{v}{2}$)"
    )
    ax_calc.text(5.0, 4.90, sol_text, fontsize=9.5, ha='center', va='center', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    F_curr = rho * A * (v - u_curr)**2 * (1.0 - np.cos(theta))
    P_curr = F_curr * u_curr
    P_max = (4.0 / 27.0) * rho * A * (v**3) * (1.0 - np.cos(theta))
    dP_du = rho * A * (1.0 - np.cos(theta)) * (v**2 - 4.0 * u_curr * v + 3.0 * u_curr**2)

    live_text = (
        f"[Live Monitor ($v={v:.1f}\\ \\mathrm{{m/s}},\\ u_{{\\mathrm{{opt}}}} = v/3 = {v/3:.2f}\\ \\mathrm{{m/s}}$)]\n"
        f"Vane speed: $u = {u_curr:.2f}\\ \\mathrm{{m/s}}$ ($u/v = {r_curr:.2f}$)  |  Force: $F = {F_curr:.1f}\\ \\mathrm{{N}}$\n"
        f"Power output: $P = {P_curr/1000:.2f}\\ \\mathrm{{kW}}$ ({p_curr_norm*100:.1f}% of $P_{{\\max}} = {P_max/1000:.2f}\\ \\mathrm{{kW}}$)\n"
        f"Slope: $dP/du = {dP_du:+.1f}\\ \\mathrm{{N}}$  $\\rightarrow$  Theoretical Value: $\\mathbf{{u = v/3}}$"
    )
    ax_calc.text(5.0, 1.30, live_text, fontsize=9.3, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_7_moving_vane_max_power.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
