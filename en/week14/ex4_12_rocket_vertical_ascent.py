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
Engineering Mechanics: Dynamics 9th Ed. Chapter 4 (4.7 Variable Mass)
Sample Problem 4/12 - Vertical Rocket Ascent & Burnout Velocity (Tsiolkovsky Rocket Equation)
- Pure white background (#ffffff) & 1:1 textbook schematic fidelity
- Theoretical verification:
  * Equation of motion: T - m*g = m*v_dot  (T = m'*u = -m_dot*u)
  * Velocity at time t: v(t) = u*ln(m_0/m) - g*t
  * Maximum burnout velocity: v_max = u*ln(m_0/m_b) + (g/m_dot)*(m_0 - m_b)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Representative numerical parameters alongside symbolic derivation
m0 = 1000.0     # Initial total mass (kg)
mb = 250.0      # Burnout structural mass (kg), mass ratio m0/mb = 4.0
m_dot = -15.0   # Time rate of change of mass dm/dt (kg/s, negative)
m_prime = -m_dot
u = 2000.0      # Exhaust velocity relative to nozzle (m/s)
g = 9.81        # Gravitational acceleration (m/s^2)

tb = (m0 - mb) / m_prime                     # 50.0 s
T_thrust = m_prime * u                       # 30,000 N (30.0 kN)
v_max = u * np.log(m0 / mb) + (g / m_dot) * (m0 - mb)  # 2282.1 m/s

n_frames = 50
t_vals = np.linspace(0.0, tb, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_rocket(ax, xc, yc, fuel_frac):
    bw, bh = 0.44, 1.45
    body = patches.Rectangle((xc - bw / 2, yc), bw, bh,
                             facecolor='#e0e6ed', edgecolor='#263238', lw=1.8, zorder=4)
    ax.add_patch(body)

    if fuel_frac > 0.01:
        fh = (bh * 0.78) * fuel_frac
        fuel_rect = patches.Rectangle((xc - bw * 0.36, yc + 0.12), bw * 0.72, fh,
                                      facecolor='#ffca28', edgecolor='#f57f17', lw=1.0, alpha=0.85, zorder=5)
        ax.add_patch(fuel_rect)

    ys_nose = np.linspace(0, 0.65, 25)
    xs_half = (bw / 2) * (1.0 - (ys_nose / 0.65)**1.6)
    nose_pts = np.vstack([
        np.column_stack([xc - xs_half, yc + bh + ys_nose]),
        np.column_stack([xc + xs_half[::-1], yc + bh + ys_nose[::-1]])
    ])
    ax.add_patch(patches.Polygon(nose_pts, facecolor='#cfd8dc', edgecolor='#263238', lw=1.8, zorder=4))

    fin_l = patches.Polygon([
        [xc - bw / 2, yc + 0.52],
        [xc - bw / 2 - 0.28, yc + 0.30],
        [xc - bw / 2 - 0.28, yc - 0.08],
        [xc - bw / 2, yc + 0.05]
    ], facecolor='#cfd8dc', edgecolor='#263238', lw=1.6, zorder=3)
    fin_r = patches.Polygon([
        [xc + bw / 2, yc + 0.52],
        [xc + bw / 2 + 0.28, yc + 0.30],
        [xc + bw / 2 + 0.28, yc - 0.08],
        [xc + bw / 2, yc + 0.05]
    ], facecolor='#cfd8dc', edgecolor='#263238', lw=1.6, zorder=3)
    fin_c = patches.Rectangle((xc - 0.045, yc - 0.06), 0.09, 0.58,
                              facecolor='#263238', edgecolor='#263238', lw=1.2, zorder=5)
    ax.add_patch(fin_l)
    ax.add_patch(fin_r)
    ax.add_patch(fin_c)

    fin_r_black = patches.Polygon([
        [xc + bw / 2, yc + 0.52],
        [xc + bw / 2 + 0.14, yc + 0.41],
        [xc + bw / 2 + 0.14, yc - 0.01],
        [xc + bw / 2, yc + 0.05]
    ], facecolor='#212121', edgecolor='none', zorder=4)
    ax.add_patch(fin_r_black)

    flame_outer = patches.Polygon([
        [xc - 0.14, yc],
        [xc + 0.14, yc],
        [xc, yc - 0.65]
    ], facecolor='#ff7043', edgecolor='none', alpha=0.85, zorder=2)
    flame_inner = patches.Polygon([
        [xc - 0.07, yc],
        [xc + 0.07, yc],
        [xc, yc - 0.38]
    ], facecolor='#ffee58', edgecolor='none', alpha=0.95, zorder=3)
    ax.add_patch(flame_outer)
    ax.add_patch(flame_inner)


def update(frame):
    t = t_vals[frame]
    m_curr = m0 + m_dot * t
    fuel_frac = (m_curr - mb) / (m0 - mb)
    v_curr = u * np.log(m0 / m_curr) - g * t
    a_curr = (T_thrust - m_curr * g) / m_curr
    W_curr = m_curr * g

    yc = 0.85 + 2.10 * (frame / (n_frames - 1))**1.35

    # ---------------- 1. Main Physical Mechanism View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.6, 2.8)
    ax_main.set_ylim(-0.6, 5.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # Launch pad ground
    ax_main.fill_between([-2.3, 2.3], -0.45, 0.0, color='#eceff1')
    ax_main.plot([-2.3, 2.3], [0.0, 0.0], color='#37474f', lw=2.2)
    ax_main.text(-2.15, -0.28, 'Launch Datum (Vertical Ascent at North Pole)', fontsize=9.5, color='#455a64', fontweight='bold')

    ax_main.plot([0.0, 0.0], [0.0, yc], color='#90a4ae', ls='--', lw=1.5, zorder=1)

    draw_rocket(ax_main, 0.0, yc, fuel_frac)

    # Gravity force vector mg (Red, downward)
    cg_y = yc + 0.82
    ax_main.annotate('', xy=(0.0, cg_y - 0.52), xytext=(0.0, cg_y + 0.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=16), zorder=6)
    ax_main.text(0.28, cg_y - 0.15, f'$mg = {W_curr/1000:.2f}\\ \\mathrm{{kN}}$\n$(m = {m_curr:.0f}\\ \\mathrm{{kg}})$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', va='center')

    # Thrust vector T = -m_dot * u (Red, upward at nozzle)
    ax_main.annotate('', xy=(0.0, yc - 0.02), xytext=(0.0, yc - 0.78),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18), zorder=6)
    ax_main.text(0.22, yc - 0.58, f'$T = -\\dot{{m}}u = m\'u$\n$({T_thrust/1000:.1f}\\ \\mathrm{{kN}})$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', va='center')

    # Velocity vector v (Green, upward)
    ax_main.annotate('', xy=(-0.48, yc + 1.45), xytext=(-0.48, yc + 0.65),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=16), zorder=6)
    ax_main.text(-0.62, yc + 1.05, f'$v = {v_curr:.0f}\\ \\mathrm{{m/s}}$\n$(a = {a_curr:.1f}\\ \\mathrm{{m/s^2}})$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right', va='center')

    ax_main.set_title('Sample Problem 4/12: Vertical Rocket Ascent Dynamics', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. Right Panel (Velocity Profile & Tsiolkovsky Derivation) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # Top mini-plot: Velocity v(t) vs Ideal Gravity-Free u*ln(m0/m)
    gx0, gy0, gw, gh = 1.1, 6.65, 8.2, 2.75
    ax_calc.add_patch(patches.Rectangle((gx0, gy0), gw, gh, facecolor='#ffffff', edgecolor='#b0bec5', lw=1.2))
    t_dense = np.linspace(0, tb, 100)
    m_dense = m0 + m_dot * t_dense
    v_ideal = u * np.log(m0 / m_dense)
    v_actual = v_ideal - g * t_dense
    v_top = 3000.0

    tx_plot = gx0 + (t_dense / tb) * gw
    ty_ideal = gy0 + (v_ideal / v_top) * gh
    ty_act = gy0 + (v_actual / v_top) * gh
    ax_calc.plot(tx_plot, ty_ideal, color='#90a4ae', ls='--', lw=1.6)
    ax_calc.plot(tx_plot, ty_act, color='#1565c0', lw=2.2)

    cur_px = gx0 + (t / tb) * gw
    cur_py = gy0 + (v_curr / v_top) * gh
    ax_calc.plot(cur_px, cur_py, 'ro', markersize=6, zorder=5)
    ax_calc.text(gx0 + 0.2, gy0 + gh - 0.35, r'Solid: $v(t) = u\ln(m_0/m) - gt$   |   Dashed: $u\ln(m_0/m)$',
                 fontsize=9.2, fontweight='bold', color='#1e3a5f')
    ax_calc.text(gx0 + gw - 0.15, gy0 + 0.20, f'$t_b = {tb:.0f}\\ \\mathrm{{s}},\\ v_{{\\max}} = {v_max:.0f}\\ \\mathrm{{m/s}}$',
                 fontsize=9.2, fontweight='bold', color='#d32f2f', ha='right')
    ax_calc.text(gx0 - 0.15, gy0 + gh / 2, r'$v$', fontsize=11, fontweight='bold', ha='right', va='center')

    # Middle Card: Theoretical Derivation
    sol_text = (
        r"■ Method I ($F = ma$ Thrust Model) & Method II ($\Sigma F = m\dot{v} + \dot{m}u$):" "\n"
        r"  $\bullet\ T - mg = m\dot{v},\quad T = m'u = -\dot{m}u \Rightarrow -\dot{m}u - mg = m\frac{dv}{dt}$" "\n"
        r"  $\bullet\ $Integration: $\int_0^v dv = -u\int_{m_0}^m \frac{dm}{m} - g\int_0^t dt \Rightarrow \mathbf{v = u\ln\frac{m_0}{m} - gt}$" "\n"
        r"■ Burnout Time $t_b = \frac{m_0 - m_b}{-\dot{m}}$ (Maximum Velocity $v_{\max}$):" "\n"
        r"  $\bullet\ $Theoretical Value: $\mathbf{v_{\max} = u\ln\frac{m_0}{m_b} + \frac{g}{\dot{m}}(m_0 - m_b)} \quad (\dot{m} < 0)$"
    )
    ax_calc.text(0.35, 4.25, sol_text, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # Bottom Card: Real-Time Monitor
    live_text = (
        f"[Real-Time Flight Monitor: $m_0={m0:.0f}\\ \\mathrm{{kg}} \\to m_b={mb:.0f}\\ \\mathrm{{kg}},\\ u={u:.0f}\\ \\mathrm{{m/s}}$]\n"
        f"• Elapsed Time: $t = {t:.1f}\\ /\\ {tb:.1f}\\ \\mathrm{{s}}$   |   Current Mass: $m(t) = {m_curr:.0f}\\ \\mathrm{{kg}}$ (Fuel: {fuel_frac*100:.0f}%)\n"
        f"• Instantaneous Acceleration: $a(t) = {a_curr:.2f}\\ \\mathrm{{m/s^2}}$ ({a_curr/g:.2f}$g$)\n"
        f"• Current Velocity: $v(t) = {v_curr:.1f}\\ \\mathrm{{m/s}}$ (Burnout Max: $v_{{\\max}} = {v_max:.1f}\\ \\mathrm{{m/s}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_12_rocket_vertical_ascent.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
