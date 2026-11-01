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
Problem 4/70 - Rocket-Propelled Sled Vehicle Accelerating Up a 10-Degree Incline
- Pure white background (#ffffff) & 1:1 textbook schematic fidelity (inclined rocket sled + checkered bands)
- Theoretical verification:
  * m_0 = 60 kg (including 10 kg fuel -> m_b = 50 kg), m' = 1 kg/s (t_b = 10 s), u = 120 m/s
  * Constant thrust T = m'*u = (1)(120) = 120 N
  * v(t) = u ln[m_0 / (m_0 - m't)] - g*t*sin(10°)
  * At t = 10 s: v_max = 120 ln(60/50) - 9.81(10) sin 10° = 21.88 - 17.04 = 4.84 m/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters (Problem 4/70)
m0 = 60.0               # Initial total mass (kg)
dm_fuel = 10.0          # Fuel mass (kg)
mb = m0 - dm_fuel       # 50.0 kg
m_prime = 1.0           # Fuel burn rate (kg/s)
tb = dm_fuel / m_prime  # 10.0 s
u = 120.0               # Exhaust speed relative to nozzle (m/s)
theta_deg = 10.0        # Incline angle (deg)
theta = np.radians(theta_deg)
g = 9.81

T_thrust = m_prime * u  # 120.0 N
v_max = u * np.log(m0 / mb) - g * tb * np.sin(theta)  # 4.84 m/s

n_frames = 50
t_vals = np.linspace(0.0, tb, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

tang_vec = np.array([np.cos(theta), np.sin(theta)])
norm_vec = np.array([-np.sin(theta), np.cos(theta)])


def draw_rocket_sled(ax, base_pt, ang_deg):
    trans = plt.matplotlib.transforms.Affine2D().rotate_deg(ang_deg).translate(base_pt[0], base_pt[1]) + ax.transData

    r_w = 0.16
    for bx in (-0.82, 0.72):
        bogie = patches.Rectangle((bx - 0.36, 2 * r_w - 0.04), 0.72, 0.09,
                                  facecolor='#263238', edgecolor='#212121', lw=1.2, zorder=4)
        bogie.set_transform(trans)
        ax.add_patch(bogie)
        for dx in (-0.20, 0.20):
            w_out = patches.Circle((bx + dx, r_w), r_w, facecolor='#81d4fa', edgecolor='#263238', lw=1.5, zorder=5)
            w_in = patches.Circle((bx + dx, r_w), r_w * 0.35, facecolor='#263238', edgecolor='none', zorder=6)
            w_out.set_transform(trans)
            w_in.set_transform(trans)
            ax.add_patch(w_out)
            ax.add_patch(w_in)

    yc_bot = 2 * r_w + 0.05
    bh = 0.60
    body = patches.Rectangle((-1.35, yc_bot), 2.45, bh,
                             facecolor='#eceff1', edgecolor='#263238', lw=1.8, zorder=4)
    body.set_transform(trans)
    ax.add_patch(body)

    for band_x in (-1.05, 0.68):
        for row in range(3):
            for col in range(2):
                c_col = '#dfc16d' if (row + col) % 2 == 0 else '#37474f'
                chk = patches.Rectangle((band_x + col * 0.12, yc_bot + row * (bh / 3)), 0.12, bh / 3,
                                        facecolor=c_col, edgecolor='#263238', lw=0.6, zorder=5)
                chk.set_transform(trans)
                ax.add_patch(chk)

    nose = patches.Polygon([
        [1.10, yc_bot],
        [1.10, yc_bot + bh],
        [2.15, yc_bot + bh / 2]
    ], facecolor='#cfd8dc', edgecolor='#263238', lw=1.8, zorder=4)
    nose_tip = patches.Polygon([
        [1.82, yc_bot + bh * 0.34],
        [1.82, yc_bot + bh * 0.66],
        [2.15, yc_bot + bh / 2]
    ], facecolor='#263238', edgecolor='none', zorder=5)
    nose.set_transform(trans)
    nose_tip.set_transform(trans)
    ax.add_patch(nose)
    ax.add_patch(nose_tip)

    for ny in (yc_bot + 0.06, yc_bot + 0.34):
        noz = patches.Polygon([
            [-1.35, ny], [-1.52, ny - 0.04], [-1.52, ny + 0.24], [-1.35, ny + 0.20]
        ], facecolor='#546e7a', edgecolor='#263238', lw=1.3, zorder=3)
        noz.set_transform(trans)
        ax.add_patch(noz)

    flame = patches.Polygon([
        [-1.52, yc_bot + 0.04],
        [-1.52, yc_bot + bh - 0.04],
        [-2.65, yc_bot + bh * 0.72],
        [-2.25, yc_bot + bh * 0.50],
        [-2.65, yc_bot + bh * 0.28]
    ], facecolor='#ffcc80', edgecolor='#ff8a65', lw=1.2, alpha=0.88, zorder=2)
    flame.set_transform(trans)
    ax.add_patch(flame)


def update(frame):
    t = t_vals[frame]
    m_curr = m0 - m_prime * t
    v_curr = u * np.log(m0 / m_curr) - g * t * np.sin(theta)
    a_curr = (T_thrust - m_curr * g * np.sin(theta)) / m_curr
    W_sin = m_curr * g * np.sin(theta)

    s_vis = 2.35 * (frame / (n_frames - 1))**1.6

    # ---------------- 1. Main Physical Mechanism View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.2, 7.6)
    ax_main.set_ylim(-0.6, 4.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    p_start = np.array([-0.8, 0.35])
    L_ramp = 8.0
    p_end = p_start + L_ramp * tang_vec
    ramp_poly = np.array([
        p_start,
        p_end,
        p_end - 0.45 * norm_vec,
        p_start - 0.45 * norm_vec
    ])
    ax_main.add_patch(patches.Polygon(ramp_poly, facecolor='#e0dcd3', edgecolor='none', zorder=1))
    ax_main.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], color='#3e2723', lw=2.4, zorder=2)

    p_ang = p_start + 1.2 * tang_vec - 0.35 * norm_vec
    ax_main.plot([p_ang[0], p_ang[0] + 2.6], [p_ang[1], p_ang[1]], color='#424242', lw=1.3)
    ax_main.text(p_ang[0] + 1.45, p_ang[1] + 0.08, r'$10^\circ$', fontsize=12, fontweight='bold', color='#212121')

    sled_base = p_start + (2.35 + s_vis) * tang_vec
    draw_rocket_sled(ax_main, sled_base, theta_deg)

    smoke_base = sled_base - 2.35 * tang_vec + 0.45 * norm_vec
    for idx, (ds, dn, sr) in enumerate([(-0.4, 0.0, 0.38), (-0.85, 0.15, 0.46), (-1.25, 0.35, 0.52)]):
        sc = smoke_base + ds * tang_vec + dn * norm_vec
        ax_main.add_patch(patches.Circle(sc, sr, facecolor='#eceff1', edgecolor='#cfd8dc', lw=1.2, zorder=1))

    v_start = sled_base + 2.25 * tang_vec + 0.65 * norm_vec
    v_end = v_start + (0.65 + 0.12 * v_curr) * tang_vec
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=16), zorder=7)
    ax_main.text(v_start[0] + 0.25, v_start[1] + 0.42,
                 f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$\n$(a = {a_curr:.2f}\\ \\mathrm{{m/s^2}})$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='center')

    ax_main.text(2.8, 3.65,
                 f'Thrust $T = m\'u = 120\\ \\mathrm{{N}}$   |   Gravity Component $mg\\sin 10^\\circ = {W_sin:.1f}\\ \\mathrm{{N}}$',
                 fontsize=10.0, fontweight='bold', color='#1e3a5f', ha='center',
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f8f9fa', edgecolor='#90caf9', lw=1.3))

    ax_main.set_title('Problem 4/70: Rocket-Propelled Sled on 10° Incline', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. Right Panel (FBD & Quantitative Analysis) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # Top FBD Box
    fbd_box = patches.FancyBboxPatch((0.3, 6.45), 9.4, 3.25, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[Free-Body Diagram] Motion Up 10° Incline ($+x$ Direction)',
                 fontsize=10.0, fontweight='bold', ha='center', color='#1e3a5f')

    fbd_center = np.array([3.6, 7.75])
    fbd_rect = patches.Rectangle((-0.65, -0.35), 1.30, 0.70, facecolor='#eceff1', edgecolor='#263238', lw=1.6)
    t_fbd = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(fbd_center[0], fbd_center[1]) + ax_calc.transData
    fbd_rect.set_transform(t_fbd)
    ax_calc.add_patch(fbd_rect)

    t_start = fbd_center - 1.55 * tang_vec
    t_end = fbd_center - 0.68 * tang_vec
    ax_calc.annotate('', xy=t_end, xytext=t_start,
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.2))
    ax_calc.text(t_start[0] - 0.15, t_start[1], r'$T = 120\ \mathrm{N}$',
                 color='#d32f2f', fontsize=9.8, fontweight='bold', ha='right', va='center')

    ax_calc.annotate('', xy=fbd_center + np.array([0.0, 0.35]), xytext=fbd_center + np.array([0.0, 1.30]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(fbd_center[0] + 0.15, fbd_center[1] + 1.05, r'$mg = (60-t)g$',
                 color='#d32f2f', fontsize=9.5, fontweight='bold')

    n_end = fbd_center - 0.35 * norm_vec
    n_start = fbd_center - 1.20 * norm_vec
    ax_calc.annotate('', xy=n_end, xytext=n_start,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.0))
    ax_calc.text(n_start[0] + 0.18, n_start[1] - 0.05, r'$N$', color='#1565c0', fontsize=9.8, fontweight='bold')

    ax_calc.plot([5.8, 7.8], [7.6, 7.6], color='#78909c', ls='--', lw=1.2)
    ax_calc.annotate('', xy=(7.8, 7.6 + 2.0 * np.tan(theta)), xytext=(5.8, 7.6),
                     arrowprops=dict(arrowstyle='->', color='#212121', lw=1.6))
    ax_calc.text(7.3, 8.15, r'$+x\ (10^\circ)$', fontsize=9.5, fontweight='bold')

    # Middle Card: Theoretical Derivation
    sol_text = (
        r"■ Equation of Motion ($\Sigma F_x = ma_x$) & Time Integration:" "\n"
        r"  $\bullet\ T = m'u = (1)(120) = 120\ \mathrm{N},\quad m(t) = m_0 - m't = 60 - t\ \mathrm{kg}\ (t_b = 10\ \mathrm{s})$" "\n"
        r"  $\bullet\ m'u - (m_0 - m't)g\sin\theta = (m_0 - m't)\frac{dv}{dt} \Rightarrow \int_0^t \left[\frac{m'u}{m_0 - m't} - g\sin\theta\right]dt = \int_0^v dv$" "\n"
        r"  $\bullet\ \mathbf{v(t) = u\ln\left(\frac{m_0}{m_0 - m't}\right) - gt\sin\theta}$" "\n"
        r"■ At $t = 10\ \mathrm{s}$: $v = 120\ln\left(\frac{60}{60-10}\right) - 9.81(10)\sin 10^\circ \Rightarrow \mathbf{v_{\max} = 4.84\ \mathrm{m/s}}$"
    )
    ax_calc.text(0.35, 4.25, sol_text, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # Bottom Card: Real-Time Monitor
    live_text = (
        f"[Real-Time Sled Monitor: $t = {t:.1f}\\ /\\ 10.0\\ \\mathrm{{s}}$]\n"
        f"• Current Mass: $m(t) = {m_curr:.1f}\\ \\mathrm{{kg}}$   |   Net Driving Force: $T - mg\\sin 10^\\circ = {T_thrust - W_sin:.1f}\\ \\mathrm{{N}}$\n"
        f"• Current Acceleration: $a(t) = {a_curr:.3f}\\ \\mathrm{{m/s^2}}$\n"
        f"• Current Velocity: $v(t) = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (Theoretical Value: $\\mathbf{{v_{{\\max}} = 4.84\\ \\mathrm{{m/s}}}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_70_rocket_incline_sled.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
