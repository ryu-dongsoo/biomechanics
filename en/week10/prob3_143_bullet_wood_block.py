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
Practice 3 (Problem 3/143): 60 g Bullet Penetrating 3 kg Wooden Block and Sliding Friction
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Bullet mass m = 60 g = 0.060 kg
- Initial bullet velocity v1 = 600 m/s (horizontal leftward)
- Exiting bullet velocity v2 = 400 m/s (horizontal leftward)
- Wooden block mass M = 3.0 kg (initially at rest)
- Block stopping distance s = 2.70 m (sliding leftward to rest)
- Gravitational acceleration g = 9.81 m/s^2

Analytical Result:
- Velocity of block immediately after impact: vb = 4.0 m/s (leftward)
- Coefficient of kinetic friction between block and floor: mu_k = 0.302
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m = 0.060          # kg
v1 = 600.0         # m/s (leftward)
v2 = 400.0         # m/s (leftward)
M = 3.000          # kg
s_stop = 2.70      # m (leftward)
g = 9.81           # m/s^2

# Phase 1: Linear momentum conservation during impact (leftward positive)
vb0 = (m * (v1 - v2)) / M # 4.0 m/s

# Phase 2: Work-energy principle for sliding phase
mu_k = (vb0**2) / (2.0 * g * s_stop) # 0.302
a_dec = mu_k * g                     # 2.963 m/s^2
t_slide = vb0 / a_dec                # 1.350 s

# Animation setup
n_frames = 70
t_arr = np.linspace(-0.25, t_slide + 0.25, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def update(frame):
    t = t_arr[frame]

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] Bullet Penetration & Sliding
    # ==========================================
    ax1.set_xlim(-1.0, 3.8)
    ax1.set_ylim(-0.45, 1.15)
    ax1.set_title("Problem 3/143: Bullet Penetration & Sliding Deceleration", fontsize=12.5, fontweight='bold', pad=10)

    # Floor & hatched foundation
    ax1.plot([-0.9, 3.7], [-0.08, -0.08], color='#495057', lw=3.0)
    ax1.fill_between([-0.9, 3.7], -0.08, -0.22, color='#dee2e6', alpha=0.6)
    for hx in np.linspace(-0.85, 3.55, 30):
        ax1.plot([hx, hx + 0.08], [-0.08, -0.16], color='#adb5bd', lw=1.2)

    bk_w, bk_h = 0.65, 0.45
    init_x = 2.70
    final_x = 0.0

    # Dimension line for 2.70 m
    dim_y = -0.25
    ax1.plot([final_x, init_x], [dim_y, dim_y], color='#495057', lw=1.5)
    ax1.plot([final_x, final_x], [-0.08, dim_y - 0.05], color='#868e96', lw=1.2)
    ax1.plot([init_x, init_x], [-0.08, dim_y - 0.05], color='#868e96', lw=1.2)
    ax1.annotate('', xy=(final_x, dim_y), xytext=(final_x + 0.3, dim_y),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.annotate('', xy=(init_x, dim_y), xytext=(init_x - 0.3, dim_y),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.text((final_x + init_x)/2, dim_y - 0.12, "2.70 m", fontsize=10.5, fontweight='bold', color='#212529', ha='center')

    # Initial ghost block outline
    init_block_ghost = patches.Rectangle((init_x - bk_w/2, -0.08), bk_w, bk_h,
                                         facecolor='#fff4e6', edgecolor='#ffd8a8', lw=1.5, linestyle='--', zorder=2)
    ax1.add_patch(init_block_ghost)

    if t < 0:
        bk_x = init_x
        bullet_x = init_x + bk_w/2 + 0.8 + (t / 0.25) * 0.8
        bullet_v = v1
        status_text = f"Bullet Approaching (v1 = {v1:.0f} m/s Left)"
        status_col = '#1864ab'
    elif t <= 0.05:
        bk_x = init_x
        bullet_x = init_x - bk_w/2 - 0.15
        bullet_v = v2
        status_text = f"Penetration Instant! (v2 = {v2:.0f} m/s, Block vb = {vb0:.1f} m/s)"
        status_col = '#e03131'
        spark = patches.Circle((init_x, 0.15), 0.10, facecolor='#ffe066', edgecolor='#f59f00', lw=2, alpha=0.8, zorder=6)
        ax1.add_patch(spark)
    else:
        dt_slide = min(t, t_slide)
        s_curr = vb0 * dt_slide - 0.5 * a_dec * (dt_slide**2)
        bk_x = init_x - s_curr
        v_curr = max(0.0, vb0 - a_dec * dt_slide)
        bullet_x = -0.8
        bullet_v = v2
        if v_curr > 0:
            status_text = f"Block Sliding with Friction (v = {v_curr:.2f} m/s, s = {s_curr:.2f} m)"
            status_col = '#d9480f'
        else:
            status_text = f"Block Brought to Rest (Stopping Distance s = {s_stop:.2f} m)"
            status_col = '#2b8a3e'

    # Wooden block
    block = patches.Rectangle((bk_x - bk_w/2, -0.08), bk_w, bk_h,
                              facecolor='#ffd8a8', edgecolor='#d9480f', lw=2.2, zorder=3)
    ax1.add_patch(block)
    ax1.text(bk_x, 0.14, "3 kg", fontsize=10.5, fontweight='bold', color='#d9480f', ha='center', va='center')

    # Bullet path inside block
    ax1.plot([bk_x - bk_w/2, bk_x + bk_w/2], [0.14, 0.14], 'k:', lw=1.5, zorder=4)

    # Bullet approaching
    if t < 0.02:
        ax1.plot([bullet_x + 0.6, bullet_x], [0.14, 0.14], color='#f76707', linestyle='--', lw=1.8)
        ax1.annotate('', xy=(bullet_x - 0.20, 0.14), xytext=(bullet_x, 0.14),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        b_patch = patches.Rectangle((bullet_x, 0.10), 0.12, 0.08, facecolor='#ff8787', edgecolor='#c92a2a', lw=1.2, zorder=5)
        ax1.add_patch(b_patch)
        ax1.text(bullet_x + 0.06, 0.22, "600 m/s\n(60 g)", color='#212529', fontsize=9, fontweight='bold', ha='center')

    # Bullet exiting
    if t >= 0.02 and bullet_x > -0.6:
        ax1.annotate('', xy=(bullet_x - 0.20, 0.14), xytext=(bullet_x, 0.14),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        b_patch = patches.Rectangle((bullet_x, 0.10), 0.12, 0.08, facecolor='#ff8787', edgecolor='#c92a2a', lw=1.2, zorder=5)
        ax1.add_patch(b_patch)
        ax1.text(bullet_x - 0.10, 0.22, "400 m/s", color='#212529', fontsize=9.5, fontweight='bold', ha='center')

    # Friction force vector
    if t > 0.05 and t <= t_slide:
        f_fric = mu_k * M * g
        ax1.annotate('', xy=(bk_x + bk_w/2 + 0.35, -0.08), xytext=(bk_x + bk_w/2, -0.08),
                     arrowprops=dict(arrowstyle="-|>", color='#495057', lw=2.8, mutation_scale=14))
        ax1.text(bk_x + bk_w/2 + 0.40, -0.05, f"Ff = mu_k*N\n({f_fric:.1f} N)", color='#495057', fontsize=8.5, fontweight='bold')

    ax1.text(1.4, 0.96, f"Status: {status_text}", fontsize=10.5, fontweight='bold',
             color=status_col, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=status_col, lw=1.2))

    # ==========================================
    # [Right Panel] Velocity-Distance Curve
    # ==========================================
    ax2.set_xlim(-0.1, 3.0)
    ax2.set_ylim(-0.3, 4.6)
    ax2.set_title("Block Velocity-Distance v(s) Curve & Textbook Verification", fontsize=12.5, fontweight='bold', pad=10)

    s_plot = np.linspace(0, s_stop, 100)
    v_plot = np.sqrt(np.maximum(0, vb0**2 - 2.0 * a_dec * s_plot))
    ax2.plot(s_plot, v_plot, color='#1864ab', lw=2.8, label='Block Velocity v(s) [m/s]')

    ax2.plot([0.0], [vb0], 'bo', markersize=8)
    ax2.text(0.1, vb0 + 0.15, f"Initial Launch Speed: vb = {vb0:.1f} m/s (Left)", color='#1864ab', fontweight='bold', fontsize=9.5)

    ax2.plot([s_stop], [0.0], 'ro', markersize=8)
    ax2.text(s_stop, 0.55, f"Brought to Rest\n(s = {s_stop:.2f} m)", color='#c92a2a', fontweight='bold', fontsize=9.0, ha='center')

    if t > 0.05:
        curr_s_val = min(s_stop, vb0 * min(t, t_slide) - 0.5 * a_dec * (min(t, t_slide)**2))
        curr_v_val = max(0.0, vb0 - a_dec * min(t, t_slide))
        ax2.plot([curr_s_val], [curr_v_val], 'o', color='#f59f00', markersize=10, zorder=5)

    ax2.set_xlabel("Block Leftward Sliding Distance s (m)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Block Velocity v (m/s)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', color='#dee2e6')
    ax2.legend(loc='upper right', fontsize=10)

    theory_text = (
        "Phase 1: Linear Momentum Conservation during Impact (Leftward +):\n"
        "   m*v1 = m*v2 + M*vb\n"
        "   0.060(600) = 0.060(400) + 3*vb\n"
        "   36.0 = 24.0 + 3*vb  ==>  vb = 4.0 m/s (left)\n\n"
        "Phase 2: Work-Energy Principle for Sliding Phase:\n"
        "   -mu_k*M*g*s = 0 - 0.5*M*(vb)^2  ==>  mu_k*g*s = 0.5*(vb)^2\n"
        "   mu_k(9.81)(2.70) = 0.5(4.0)^2 = 8.0\n"
        "   mu_k = 8.0 / (9.81 * 2.70) = 0.3020\n"
        "Textbook Official Answer: vb = 4.0 m/s,  mu_k = 0.302"
    )
    ax2.text(0.05, 0.40, theory_text, fontsize=9.0,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "prob3_143_bullet_wood_block.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
