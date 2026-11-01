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
Engineering Dynamics (9th Ed.) Chapter 3 Section B: Work and Energy (Section 3.7 Potential Energy & Energy Conservation)
Sample Problem 3.16 (Sample Problem 3/16) - Collar on Curved Guide with Spring
- Pure white background (#ffffff) & exact 2-panel layout
- Wiley Solution Manual Verified:
  * State 1: V_1 = 63.0 J (elastic potential energy, x_1 = 0.6 m)
  * State 2: V_g2 = -17.66 J, V_e2 = 10.81 J (x_2 = 0.2485 m)
  * Conservation of Energy: T_1 + V_1 = T_2 + V_2  =>  v_2 = 6.82 m/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Matplotlib Font Configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Physical Parameters
m = 3.0             # Collar mass (kg)
g = 9.81            # Gravitational acceleration (m/s^2)
k = 350.0           # Spring stiffness (N/m)
L0 = 0.6            # Unstretched spring length (m)
R = 0.6             # Guide radius of curvature (m)

# Geometry Setup:
# Curve center: (R, 0) = (0.6, 0.0)
# Spring Anchor: (2*R, 0) = (1.2, 0.0)
# State 1 (Initial): (0.0, 0.0) -> Vertical tangent
# State 2 (Final): (0.6, -0.6) -> Horizontal tangent
x_center, y_center = 0.6, 0.0
x_anchor, y_anchor = 1.2, 0.0

# Energy at State 1
L1 = 1.2
x1 = L1 - L0          # 0.6 m
Ve1 = 0.5 * k * x1**2 # 63.0 J
Vg1 = 0.0
E_total = Ve1         # 63.0 J

# Energy at State 2
L2 = np.sqrt(0.6**2 + 0.6**2) # 0.6 * sqrt(2) = 0.8485 m
x2 = L2 - L0          # 0.2485 m
Ve2 = 0.5 * k * x2**2 # 10.81 J
Vg2 = -m * g * R      # -17.658 J
T2 = E_total - (Ve2 + Vg2) # 69.85 J
v2 = np.sqrt(2 * T2 / m)   # 6.82 m/s

# Animation Parameters (phi: 180 deg -> 270 deg)
n_frames = 50
phi_vals = np.linspace(np.pi, 1.5 * np.pi, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.05, color='#444444', lw=1.8):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-6:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    
    lead_len = 0.06
    active_len = max(length - 2 * lead_len, 0.05)
    
    pts = [start, start + lead_len * u_par]
    step = active_len / nodes
    for i in range(1, nodes):
        sgn = 1 if i % 2 == 1 else -1
        p = start + lead_len * u_par + i * step * u_par + sgn * width * u_perp
        pts.append(p)
    pts.append(end - lead_len * u_par)
    pts.append(end)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle='round')

def update(frame):
    phi = phi_vals[frame]
    
    # Current collar position
    x_c = x_center + R * np.cos(phi)
    y_c = y_center + R * np.sin(phi)
    
    # Spring length and deflection
    L_curr = np.sqrt((x_anchor - x_c)**2 + (y_anchor - y_c)**2)
    x_curr = L_curr - L0
    
    # Energetics
    Ve_curr = 0.5 * k * x_curr**2
    Vg_curr = m * g * y_c
    T_curr = max(E_total - (Ve_curr + Vg_curr), 0.0)
    v_curr = np.sqrt(2 * T_curr / m)
    
    # ---------------- 1. Main System View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.25, 1.45)
    ax_main.set_ylim(-0.85, 0.35)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Ceiling & Mount Hatching
    ax_main.plot([-0.15, 0.15], [0.08, 0.08], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.15, 0.12, 6):
        ax_main.plot([hx, hx + 0.04], [0.08, 0.14], color='#666666', lw=1.2)
    mount_top = patches.Rectangle((-0.06, 0.0), 0.12, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_top)
    
    # Right Spring Wall Anchor Mount
    ax_main.plot([x_anchor + 0.06, x_anchor + 0.06], [-0.15, 0.15], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.14, 0.11, 6):
        ax_main.plot([x_anchor + 0.06, x_anchor + 0.12], [hy, hy + 0.04], color='#666666', lw=1.2)
    anchor_mount = patches.Polygon([[x_anchor, 0.0], [x_anchor + 0.06, 0.08], [x_anchor + 0.06, -0.08]],
                                   facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(anchor_mount)
    ax_main.plot(x_anchor, y_anchor, 'o', color='#2b2b2b', markersize=5)
    
    # Bottom Position 2 Mount
    ax_main.plot([0.72, 0.72], [-0.75, -0.45], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.73, -0.48, 6):
        ax_main.plot([0.72, 0.78], [hy, hy + 0.04], color='#666666', lw=1.2)
    mount_bot = patches.Rectangle((0.64, -0.64), 0.08, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_bot)
    
    # Curved Rod Guide (Realistic blue steel texture)
    theta_rod = np.linspace(np.pi, 1.5 * np.pi, 100)
    rx = x_center + R * np.cos(theta_rod)
    ry = y_center + R * np.sin(theta_rod)
    ax_main.plot(rx, ry, color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot(rx, ry, color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    # Extension tangent
    ax_main.plot([0.6, 0.65], [-0.6, -0.6], color='#4682b4', lw=8.0, zorder=2)
    ax_main.plot([0.6, 0.65], [-0.6, -0.6], color='#d0e4f7', lw=3.0, zorder=2)
    
    # Spring Reference States 1 & 2 (Ghost dashed lines)
    draw_spring(ax_main, (0.0, 0.0), (x_anchor, y_anchor), nodes=16, width=0.04, color='#bbbbbb', lw=1.2)
    draw_spring(ax_main, (0.6, -0.6), (x_anchor, y_anchor), nodes=12, width=0.04, color='#bbbbbb', lw=1.2)
    
    # Dynamic Spring
    draw_spring(ax_main, (x_c, y_c), (x_anchor, y_anchor), nodes=14, width=0.045, color='#2b2b2b', lw=2.0)
    ax_main.text(0.70, -0.15, r'$k = 350\ \mathrm{N/m}$', fontsize=10.5, fontweight='bold', color='#1a5276', rotation=22)
    
    # Collar Box (Rotates along curve tangent)
    tang_angle = phi + np.pi / 2
    collar_w, collar_h = 0.12, 0.07
    c_poly = patches.Polygon([
        [-collar_w/2, -collar_h/2], [collar_w/2, -collar_h/2],
        [collar_w/2, collar_h/2], [-collar_w/2, collar_h/2]
    ], facecolor='#e67e22', edgecolor='#78341a', lw=1.8, zorder=5)
    t = patches.transforms.Affine2D().rotate(tang_angle).translate(x_c, y_c) + ax_main.transData
    c_poly.set_transform(t)
    ax_main.add_patch(c_poly)
    ax_main.plot(x_c, y_c, 'o', color='#2b2b2b', markersize=4, zorder=6)
    
    # Velocity Vector
    if v_curr > 0.3:
        v_scale = 0.035 * (v_curr / v2)
        vx = -np.sin(phi) * v_scale
        vy = np.cos(phi) * v_scale
        ax_main.annotate('', xy=(x_c + vx, y_c + vy), xytext=(x_c, y_c),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(x_c + vx * 1.1, y_c + vy * 1.1 - 0.05, f'$v$', color='#27ae60', fontsize=11, fontweight='bold')
    
    # Dimensions & Labels
    ax_main.plot([0.6, 1.2], [0.18, 0.18], color='#333333', lw=1.2)
    ax_main.plot([0.6, 0.6], [-0.6, 0.22], color='#777777', ls='--', lw=1.0)
    ax_main.plot([1.2, 1.2], [0.0, 0.22], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(0.6, 0.18), xytext=(0.85, 0.18), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(1.2, 0.18), xytext=(0.95, 0.18), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(0.90, 0.21, r'$0.6\ \mathrm{m}$', ha='center', fontsize=10)
    
    ax_main.annotate('', xy=(0.3, -0.3*np.sqrt(3)/1), xytext=(0.6, 0.0),
                     arrowprops=dict(arrowstyle='->', color='#777777', ls=':', lw=1.2))
    ax_main.text(0.28, -0.15, r'$0.6\ \mathrm{m}$', fontsize=10, color='#555555')
    
    ax_main.text(-0.12, 0.0, r'$\mathbf{1}$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(0.55, -0.73, r'$\mathbf{2}$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(-0.06, -0.22, r'$3\ \mathrm{kg}$', fontsize=10.5, color='#333333')
    
    ax_main.set_title('Sample Problem 3.16: Curved Guide Collar System', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. Energy Monitor & Theory Card ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    # Energy Bars
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, T_curr + Ve_curr + Vg_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$V_e$', r'$V_g$', r'$E_{\mathrm{tot}}$']
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 70.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"[Work-Energy Analysis (Section 3.7)]\n"
        f"• State 1: $x_1 = 1.2 - 0.6 = 0.6\\ \\mathrm{{m}},\\ V_1 = \\frac{{1}}{{2}}(350)(0.6)^2 = 63.0\\ \\mathrm{{J}}$\n"
        f"• State 2: $x_2 = 0.6\\sqrt{{2}} - 0.6 = 0.2485\\ \\mathrm{{m}},\\ V_{{e2}} = 10.81\\ \\mathrm{{J}}$\n"
        f"  Gravitational PE: $V_{{g2}} = -mgh = -3(9.81)(0.6) = -17.66\\ \\mathrm{{J}}$\n"
        f"• Energy Conservation: $T_1 + V_1 = T_2 + V_2$\n"
        f"  $0 + 63.0 = \\frac{{1}}{{2}}(3)v_2^2 - 17.66 + 10.81$\n"
        f"  $\\rightarrow\\ v_2 = \\mathbf{{6.82\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• Progress: {(frame+1)/n_frames*100:3.0f}%\n"
        f"• Current Velocity: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (Target: $6.82\\ \\mathrm{{m/s}}$)"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.5, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('Conservation of Energy Monitor & Validation', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_16_curved_rod_collar.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
