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
Sample Problem 3.21: 2D Particle Motion under Time-Varying Forces F1 and F2
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Particle mass m = 0.500 kg
- Initial velocity (t = 0): v1 = 10 m/s (+x direction, v1 = 10i m/s)
- Applied forces:
  * F1 (-x direction): 4 N for 0 <= t <= 1 s, 2 N for 1 < t <= 3 s
  * F2 (+y direction): 1 N for 0 <= t <= 2 s, ramps linearly 1 N to 3 N for 2 < t <= 3 s
- Target: Velocity v2 after 3 seconds

Analytical Result:
- (v2)x = -6 m/s, (v2)y = 8 m/s
- Velocity magnitude: v2 = 10 m/s
- Direction angle: theta_x = 126.9 deg
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

m = 0.500          # kg
v1_x = 10.0        # m/s
v1_y = 0.0         # m/s

imp_x = -8.0       # N*s
imp_y = 4.0        # N*s

v2_x = (m * v1_x + imp_x) / m # -6.0 m/s
v2_y = (m * v1_y + imp_y) / m # +8.0 m/s
v2_mag = np.hypot(v2_x, v2_y) # 10.0 m/s
theta_deg = np.degrees(np.arctan2(v2_y, v2_x)) # 126.9 deg

def get_state(t):
    if t <= 1.0:
        F1 = 4.0
    else:
        F1 = 2.0

    if t <= 2.0:
        F2 = 1.0
    else:
        F2 = 1.0 + 2.0 * (t - 2.0)

    if t <= 1.0:
        vx = 10.0 - 8.0 * t
        x = 10.0 * t - 4.0 * (t**2)
        vy = 2.0 * t
        y = t**2
    elif t <= 2.0:
        dt1 = t - 1.0
        vx = 2.0 - 4.0 * dt1
        x = 6.0 + 2.0 * dt1 - 2.0 * (dt1**2)
        vy = 2.0 + 2.0 * dt1
        y = 1.0 + 2.0 * dt1 + (dt1**2)
    else:
        dt2 = t - 2.0
        vx = -2.0 - 4.0 * dt2
        x = 6.0 - 2.0 * dt2 - 2.0 * (dt2**2)
        vy = 4.0 + 2.0 * dt2 + 2.0 * (dt2**2)
        y = 4.0 + 4.0 * dt2 + (dt2**2) + (2.0/3.0)*(dt2**3)

    return F1, F2, vx, vy, x, y

n_frames = 75
t_arr = np.linspace(0.0, 3.0, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def update(frame):
    t = t_arr[frame]
    F1, F2, vx, vy, x, y = get_state(t)

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] Textbook Schematic & Trajectory
    # ==========================================
    ax1.set_xlim(-2.0, 8.5)
    ax1.set_ylim(-1.5, 11.5)
    ax1.set_aspect('equal')
    ax1.set_title("Sample Problem 3.21: 2D Particle Motion and Trajectory", fontsize=12.5, fontweight='bold', pad=10)

    ax1.axhline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.axvline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.text(8.0, -0.6, "x, m", fontsize=11, fontweight='bold', color='#495057')
    ax1.text(-0.8, 10.8, "y, m", fontsize=11, fontweight='bold', color='#495057')

    t_full = np.linspace(0.0, 3.0, 100)
    traj_x = [get_state(tau)[4] for tau in t_full]
    traj_y = [get_state(tau)[5] for tau in t_full]
    ax1.plot(traj_x, traj_y, color='#f76707', linestyle='--', lw=2.2, label='Trajectory (0 to 3s)')

    for t_mark in [1.0, 2.0, 3.0]:
        _, _, _, _, mx, my = get_state(t_mark)
        ax1.plot([mx], [my], 'ko', markersize=4)
        ax1.text(mx + 0.3, my - 0.2, f"t = {t_mark:.0f} s", fontsize=8.5, color='#495057', fontweight='bold')

    particle = patches.Circle((x, y), 0.35, facecolor='#a5d8ff', edgecolor='#1971c2', lw=2, zorder=5)
    ax1.add_patch(particle)
    ax1.text(x, y, "m", fontsize=9, fontweight='bold', ha='center', va='center', color='#1971c2')

    f1_len = F1 * 0.45
    ax1.annotate('', xy=(x - f1_len, y), xytext=(x, y),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(x - f1_len - 0.2, y + 0.2, f"F1 = {F1:.1f} N", color='#e03131', fontsize=9.5, fontweight='bold', ha='right')

    f2_len = F2 * 0.45
    ax1.annotate('', xy=(x, y + f2_len), xytext=(x, y),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(x + 0.2, y + f2_len + 0.2, f"F2 = {F2:.1f} N", color='#e03131', fontsize=9.5, fontweight='bold')

    v_mag_curr = np.hypot(vx, vy)
    if v_mag_curr > 0.2:
        v_scale = 0.22
        ax1.annotate('', xy=(x + vx * v_scale, y + vy * v_scale), xytext=(x, y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.8, mutation_scale=14))
        ax1.text(x + vx * v_scale + 0.2, y + vy * v_scale, f"v = {v_mag_curr:.1f} m/s",
                 color='#2b8a3e', fontsize=9.5, fontweight='bold')

    if t >= 2.95:
        ax1.plot([x, x + vx * 0.35], [y, y], color='#1864ab', lw=2, linestyle=':')
        ax1.plot([x + vx * 0.35, x + vx * 0.35], [y, y + vy * 0.35], color='#2b8a3e', lw=2, linestyle=':')
        ax1.plot([x, x + vx * 0.35], [y + vy * 0.35, y + vy * 0.35], color='#adb5bd', lw=1, linestyle='--')
        ax1.plot([x, x], [y, y + vy * 0.35], color='#adb5bd', lw=1, linestyle='--')
        ax1.text(x - 1.2, y - 0.5, "-6i m/s", color='#1864ab', fontweight='bold', fontsize=10)
        ax1.text(x - 2.8, y + 1.5, "8j m/s", color='#2b8a3e', fontweight='bold', fontsize=10)
        ax1.text(x - 2.5, y + 3.2, f"v2 = 10 m/s\n(theta_x = {theta_deg:.1f} deg)", color='#c92a2a', fontweight='bold', fontsize=10.5)

    ax1.text(3.0, 11.2, f"Time: t = {t:.2f} s | Position: ({x:.2f}, {y:.2f}) m", fontsize=11, fontweight='bold',
             color='#212529', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

    # ==========================================
    # [Right Panel] F(t) Diagram & Textbook Solution
    # ==========================================
    ax2.set_xlim(-0.3, 3.5)
    ax2.set_ylim(-0.5, 5.0)
    ax2.set_title("Force-Time F(t) Impulse Curves & Solution", fontsize=12.5, fontweight='bold', pad=10)

    t_f = np.array([0.0, 1.0, 1.0, 3.0])
    f1_f = np.array([4.0, 4.0, 2.0, 2.0])
    ax2.plot(t_f, f1_f, color='#c92a2a', lw=2.5, label='F1 (-x dir: Impulse = -8 N s)')
    ax2.fill_between(t_f, f1_f, color='#ffc9c9', alpha=0.35)

    t_f2 = np.array([0.0, 2.0, 3.0])
    f2_f2 = np.array([1.0, 1.0, 3.0])
    ax2.plot(t_f2, f2_f2, color='#1864ab', lw=2.5, label='F2 (+y dir: Impulse = +4 N s)')
    ax2.fill_between(t_f2, f2_f2, color='#d0ebff', alpha=0.35)

    ax2.axvline(t, color='#f59f00', linestyle=':', lw=2)

    ax2.set_xlabel("Time t (s)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Force F (N)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', color='#dee2e6')
    ax2.legend(loc='upper right', fontsize=9.0)

    imp_card = (
        "Linear Impulse-Momentum Principle (Area Integrals):\n"
        "   m(v1)x + Int(-F1)dt = m(v2)x\n"
        "   0.5(10) - [4(1) + 2(2)] = 0.5(v2)x  ==>  5 - 8 = -3  ==>  (v2)x = -6 m/s\n\n"
        "   m(v1)y + Int(F2)dt = m(v2)y\n"
        "   0 + [1(2) + 0.5(1+3)(1)] = 0.5(v2)y  ==>  4 = 0.5(v2)y  ==>  (v2)y = +8 m/s\n\n"
        "Analytical Result (100% Parity):\n"
        "   v2 = -6i + 8j m/s  (|v2| = 10 m/s,  theta_x = 126.9 deg)"
    )
    ax2.text(-0.2, -0.35, imp_card, fontsize=8.8, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_21_variable_force_plane_impulse.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
