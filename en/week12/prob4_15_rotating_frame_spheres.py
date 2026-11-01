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
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.5: Conservation of Energy and Momentum
Problem 4/15 - Angular Impulse and Momentum of a Light Rigid Frame with Three Welded Spheres
- Pure white background (#ffffff) & faithful recreation of textbook geometry
- Verified quantitative values:
  * Σ(m_i r_i^2) = 3(0.5)^2 + 4(0.4)^2 + 3(0.6)^2 = 2.47 kg·m^2
  * M_O t = 30 × 5 = 150 N·m·s = 2.47 (θ̇' - 20)
  * θ̇' = 60.7 + 20 = 80.7 rad/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m1, r1, ang1_0 = 3.0, 0.5, 90.0    # Top sphere (3 kg, 0.5 m)
m2, r2, ang2_0 = 4.0, 0.4, 180.0   # Left sphere (4 kg, 0.4 m)
m3, r3, ang3_0 = 3.0, 0.6, -45.0   # Bottom-right sphere (3 kg, 0.6 m)

I_O = m1 * r1**2 + m2 * r2**2 + m3 * r3**2  # 0.75 + 0.64 + 1.08 = 2.47 kg·m^2
M_O = 30.0          # N·m (Clockwise CW)
t_total = 5.0       # s
w0 = 20.0           # rad/s (CW)
alpha = M_O / I_O   # 12.1457 rad/s^2
wf = w0 + alpha * t_total  # 80.729 -> 80.7 rad/s

n_frames = 52
t_vals = np.linspace(0, t_total, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    t = t_vals[frame]
    w_curr = w0 + alpha * t
    H_curr = I_O * w_curr
    th_vis = 0.045 * (w0 * t + 0.5 * alpha * t**2)

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.85, 0.85)
    ax_main.set_ylim(-0.82, 0.82)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    base_poly = patches.Polygon([[-0.18, -0.22], [0.18, -0.22], [0.18, -0.32], [-0.18, -0.32]],
                                facecolor='#dfd6cc', edgecolor='none', zorder=1)
    ax_main.add_patch(base_poly)
    ax_main.plot([-0.18, 0.18], [-0.22, -0.22], color='#444444', lw=2.2, zorder=2)

    bracket = patches.Polygon([[-0.09, -0.22], [0.09, -0.22], [0.055, 0.0], [-0.055, 0.0]],
                              facecolor='#a6c8e0', edgecolor='#2b4c65', lw=1.6, zorder=2)
    ax_main.add_patch(bracket)
    ax_main.text(0.0, -0.15, r'$O$', fontsize=12, fontweight='bold', ha='center', va='center', zorder=7)

    spheres = [
        (m1, r1, np.radians(ang1_0) - th_vis, 0.082, '0.5 m', '3 kg'),
        (m2, r2, np.radians(ang2_0) - th_vis, 0.092, '0.4 m', '4 kg'),
        (m3, r3, np.radians(ang3_0) - th_vis, 0.082, '0.6 m', '3 kg'),
    ]

    for m_i, r_i, ang, rad_draw, r_txt, m_txt in spheres:
        u_vec = np.array([np.cos(ang), np.sin(ang)])
        n_vec = np.array([-np.sin(ang), np.cos(ang)])
        p_end = r_i * u_vec

        circ_guide = patches.Circle((0, 0), r_i, fill=False, edgecolor='#e0e0e0', ls=':', lw=1.1, zorder=1)
        ax_main.add_patch(circ_guide)

        rod = patches.Polygon([-0.015*n_vec, 0.015*n_vec, p_end + 0.015*n_vec, p_end - 0.015*n_vec],
                              facecolor='#b8d0e0', edgecolor='#375a75', lw=1.6, zorder=3)
        ax_main.add_patch(rod)

        sph = patches.Circle(p_end, rad_draw, facecolor='#c95b5b', edgecolor='#6b1d1d', lw=2.0, zorder=5)
        ax_main.add_patch(sph)
        hl = patches.Circle(p_end + np.array([-0.25*rad_draw, 0.25*rad_draw]), 0.28*rad_draw,
                            facecolor='#e8a5a5', edgecolor='none', zorder=6)
        ax_main.add_patch(hl)

        lbl_pos = (r_i + rad_draw + 0.075) * u_vec
        ax_main.text(lbl_pos[0], lbl_pos[1], m_txt, fontsize=10.5, fontweight='bold',
                     ha='center', va='center', color='#4a1212', zorder=7)

        mid_pos = 0.52 * r_i * u_vec + 0.068 * n_vec
        ax_main.text(mid_pos[0], mid_pos[1], r_txt, fontsize=9.8, fontweight='bold',
                     ha='center', va='center', color='#1d4564',
                     bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.85), zorder=6)

        t_dir = -n_vec
        v_start = p_end + (rad_draw + 0.01) * t_dir
        v_len = (r_i * w_curr) * 0.0042
        v_end = v_start + v_len * t_dir
        ax_main.annotate('', xy=v_end, xytext=v_start,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=7)

    hub = patches.Circle((0, 0), 0.065, facecolor='#9ec3db', edgecolor='#2b4c65', lw=1.8, zorder=4)
    ax_main.add_patch(hub)
    ax_main.plot(0, 0, 'ko', markersize=5.5, zorder=6)

    arc_M = patches.Arc((0, 0), 0.30, 0.30, angle=0, theta1=15, theta2=145, color='#d32f2f', lw=2.4, zorder=7)
    ax_main.add_patch(arc_M)
    ax_main.annotate('', xy=(0.15*np.cos(np.radians(15)), 0.15*np.sin(np.radians(15))),
                     xytext=(0.15*np.cos(np.radians(35)), 0.15*np.sin(np.radians(35))),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=13), zorder=7)
    ax_main.text(0.46, 0.66, r'$M_O = 30\ \mathrm{N\cdot m}\ (\mathrm{CW})$',
                 fontsize=11, fontweight='bold', color='#d32f2f', ha='center',
                 bbox=dict(boxstyle='round,pad=0.18', facecolor='#ffffff', edgecolor='#f5c6cb', alpha=0.92), zorder=8)

    arc_w = patches.Arc((0, 0), 0.48, 0.48, angle=0, theta1=230, theta2=310, color='#2e7d32', lw=2.0, zorder=2)
    ax_main.add_patch(arc_w)
    ax_main.annotate('', xy=(0.24*np.cos(np.radians(230)), 0.24*np.sin(np.radians(230))),
                     xytext=(0.24*np.cos(np.radians(245)), 0.24*np.sin(np.radians(245))),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0, mutation_scale=13), zorder=2)
    ax_main.text(0.0, -0.74, rf'Angular Speed $\dot{{\theta}} = {w_curr:.1f}\ \mathrm{{rad/s}}$',
                 fontsize=11, fontweight='bold', color='#2e7d32', ha='center',
                 bbox=dict(boxstyle='round,pad=0.18', facecolor='#ffffff', edgecolor='#c8e6c9', alpha=0.92), zorder=8)

    ax_main.set_title(r'Problem 4/15: Rotating 3-Sphere Frame & Moment $M_O$', fontsize=13.0, fontweight='bold', pad=12)

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        r"1. Angular Momentum about $O$ & Rotational Inertia:" "\n"
        r"  $\bullet\ \sum M_O = \dot{H}_O = \frac{dH_O}{dt} \Rightarrow \int_0^t \sum M_O\, dt = \Delta H_O$" "\n"
        r"  $\bullet\ H_O = \sum m_i r_i (r_i \dot{\theta}) = \left(\sum m_i r_i^2\right) \dot{\theta}$" "\n"
        r"  $\bullet\ \sum m_i r_i^2 = 3(0.5)^2 + 4(0.4)^2 + 3(0.6)^2$" "\n"
        r"  $\quad\quad\quad\ \ = 0.75 + 0.64 + 1.08 = 2.47\ \mathrm{kg\cdot m^2}$" "\n\n"
        r"2. Angular Impulse-Momentum Equation ($t = 5\ \mathrm{s}$, CW $+$):" "\n"
        r"  $\int_0^5 M_O\,dt = M_O t = \left(\sum m_i r_i^2\right)(\dot{\theta}' - \dot{\theta}_0)$" "\n"
        r"  $30 \times 5 = \left[3(0.5)^2 + 4(0.4)^2 + 3(0.6)^2\right](\dot{\theta}' - 20)$" "\n"
        r"  $150 = 2.47(\dot{\theta}' - 20) \Rightarrow \dot{\theta}' - 20 = 60.73$" "\n"
        r"  $\mathbf{\dot{\theta}' = 60.7 + 20 = 80.7\ \mathrm{rad/s}}\ (\mathrm{CW})$"
    )
    ax_calc.text(0.4, 6.0, sol_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'Elapsed Time: $t = {t:.2f}\\ /\\ 5.00\\ \\mathrm{{s}}$  (Angular Impulse: ${M_O*t:.1f}\\ \\mathrm{{N\\cdot m\\cdot s}}$)\n'
        f'Current Angular Velocity: $\\dot{{\\theta}} = {w_curr:.1f}\\ \\mathrm{{rad/s}}$  (Initial: $20.0\\ \\mathrm{{rad/s}}$ CW)\n'
        f'Current Angular Momentum: $H_O = {H_curr:.1f}\\ \\mathrm{{kg\\cdot m^2/s}}$\n'
        f'Theoretical Value ($t = 5\\ \\mathrm{{s}}$): $\\mathbf{{\\dot{{\\theta}}\' = 80.7\\ \\mathrm{{rad/s}}}}$ (CW)'
    )
    ax_calc.text(0.4, 1.45, live_box, fontsize=9.9, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title(r'Theoretical Derivation & Analysis ($\Delta H_O$ Angular Momentum)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_15_rotating_frame_spheres.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
