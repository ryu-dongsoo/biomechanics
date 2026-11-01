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
Fundamental Practice 1 (Problem 3/111) - Collar on Circular-Horizontal Guide with Spring
- Pure white background (#ffffff) & exact 1:1 textbook layout
- Wiley Solution Manual Verified:
  * U'_{1-2} = 0 (frictionless, mechanical energy conservation)
  * Delta V_g = -3 * 9.81 * 0.8 = -23.54 J
  * Delta V_e = 0.5 * 200 * [(1.0 - 0.4)^2 - (0.8 - 0.4)^2] = 20.0 J
  * 0 = (3/2) v^2 - 23.54 + 20.0  =>  v = 1.537 m/s
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
k = 200.0           # Spring stiffness (N/m)
L0 = 0.4            # Unstretched length (m)
R = 0.8             # Circular guide radius (m)
L_horiz = 0.6       # Horizontal guide length (m)

x_anchor, y_anchor = 0.0, 0.0

s_arc = R * (np.pi / 2.0)
s_total = s_arc + L_horiz

n_frames = 50
s_vals = np.linspace(0, s_total, n_frames)

def get_state(s):
    if s <= s_arc:
        phi = np.pi + (s / s_arc) * (np.pi / 2.0)
        xc = R * np.cos(phi)
        yc = R * np.sin(phi)
        tang_angle = phi + np.pi / 2.0
    else:
        x_lin = s - s_arc
        xc = x_lin
        yc = -R
        tang_angle = 0.0
    
    L_curr = np.sqrt(xc**2 + yc**2)
    x_curr = L_curr - L0
    
    Ve_curr = 0.5 * k * x_curr**2
    Vg_curr = m * g * yc
    Ve_A = 0.5 * k * (R - L0)**2
    Vg_A = 0.0
    E_total = Ve_A + Vg_A
    
    T_curr = max(E_total - (Ve_curr + Vg_curr), 0.0)
    v_curr = np.sqrt(2.0 * T_curr / m)
    return xc, yc, tang_angle, L_curr, x_curr, Ve_curr, Vg_curr, T_curr, v_curr

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.045, color='#444444', lw=1.8):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-6:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.06
    active_len = max(length - 2 * lead_len, 0.04)
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
    s = s_vals[frame]
    xc, yc, tang_angle, L_curr, x_curr, Ve_curr, Vg_curr, T_curr, v_curr = get_state(s)
    
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.15, 0.95)
    ax_main.set_ylim(-1.15, 0.35)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Ceiling Mount A
    ax_main.plot([-0.95, -0.65], [0.08, 0.08], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.94, -0.68, 6):
        ax_main.plot([hx, hx + 0.04], [0.08, 0.14], color='#666666', lw=1.2)
    mount_A = patches.Rectangle((-0.84, 0.0), 0.08, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_A)
    
    # Anchor Wall Mount (0, 0)
    ax_main.plot([-0.18, 0.18], [0.08, 0.08], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.16, 0.14, 7):
        ax_main.plot([hx, hx + 0.04], [0.08, 0.14], color='#666666', lw=1.2)
    anchor_mount = patches.Polygon([[-0.06, 0.08], [0.06, 0.08], [0.0, 0.0]],
                                   facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(anchor_mount)
    ax_main.plot(x_anchor, y_anchor, 'o', color='#2b2b2b', markersize=5, zorder=5)
    
    # Right Wall Mount B
    ax_main.plot([0.80, 0.80], [-0.95, -0.65], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.93, -0.68, 6):
        ax_main.plot([0.80, 0.86], [hy, hy + 0.04], color='#666666', lw=1.2)
    mount_B = patches.Rectangle((0.74, -0.84), 0.06, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_B)
    
    # Guide Rod (Arc + Horizontal)
    th_arc = np.linspace(np.pi, 1.5 * np.pi, 60)
    ax_main.plot(R * np.cos(th_arc), R * np.sin(th_arc), color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot(R * np.cos(th_arc), R * np.sin(th_arc), color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    ax_main.plot([0.0, 0.74], [-R, -R], color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot([0.0, 0.74], [-R, -R], color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    
    # Ghost Springs
    draw_spring(ax_main, (-0.8, 0.0), (0.0, 0.0), nodes=14, width=0.035, color='#bbbbbb', lw=1.2)
    draw_spring(ax_main, (0.6, -0.8), (0.0, 0.0), nodes=16, width=0.035, color='#bbbbbb', lw=1.2)
    
    # Dynamic Spring
    draw_spring(ax_main, (xc, yc), (0.0, 0.0), nodes=15, width=0.045, color='#2b2b2b', lw=2.0)
    
    # Collar Box
    cw, ch = 0.14, 0.08
    c_poly = patches.Polygon([
        [-cw/2, -ch/2], [cw/2, -ch/2], [cw/2, ch/2], [-cw/2, ch/2]
    ], facecolor='#e67e22', edgecolor='#78341a', lw=1.8, zorder=5)
    t = patches.transforms.Affine2D().rotate(tang_angle).translate(xc, yc) + ax_main.transData
    c_poly.set_transform(t)
    ax_main.add_patch(c_poly)
    ax_main.plot(xc, yc, 'o', color='#2b2b2b', markersize=4, zorder=6)
    
    # Velocity Vector
    if v_curr > 0.1:
        v_scale = 0.04 * (v_curr / 3.96)
        vx = np.cos(tang_angle) * v_scale
        vy = np.sin(tang_angle) * v_scale
        ax_main.annotate('', xy=(xc + vx, yc + vy), xytext=(xc, yc),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
    
    # Dimensions
    ax_main.plot([0.0, 0.0], [0.0, -R], color='#777777', ls='-.', lw=1.0)
    ax_main.annotate('', xy=(-0.8*np.cos(np.pi/4), -0.8*np.sin(np.pi/4)), xytext=(0.0, 0.0),
                     arrowprops=dict(arrowstyle='->', color='#555555', ls=':', lw=1.2))
    ax_main.text(-0.25, -0.42, r'$0.8\ \mathrm{m}$', fontsize=10, color='#333333')
    
    ax_main.plot([0.0, 0.0], [-R, -0.98], color='#999999', ls='--', lw=1.0)
    ax_main.plot([0.6, 0.6], [-R, -0.98], color='#999999', ls='--', lw=1.0)
    ax_main.annotate('', xy=(0.0, -0.95), xytext=(0.25, -0.95), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(0.6, -0.95), xytext=(0.35, -0.95), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(0.30, -0.93, r'$0.6\ \mathrm{m}$', ha='center', fontsize=10.5)
    
    ax_main.text(-0.92, -0.06, r'$A$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(0.58, -0.68, r'$B$', fontsize=13, fontweight='bold', color='#111111')
    
    ax_main.set_title('Problem 3/111: Curved-Horizontal Guide Collar System', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. Energy Monitor & Theory Card ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, T_curr + Ve_curr + Vg_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$V_e$', r'$V_g$', r'$E_{\mathrm{tot}}$']
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 40.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"[Work-Energy Analysis (Problem 3/111)]\n"
        f"• State 1 (Point A): $L_1 = 0.8\\ \\mathrm{{m}},\\ x_1 = 0.8 - 0.4 = 0.4\\ \\mathrm{{m}}$\n"
        f"• State 2 (Point B): $L_2 = \\sqrt{{0.8^2 + 0.6^2}} = 1.0\\ \\mathrm{{m}},\\ x_2 = 0.6\\ \\mathrm{{m}}$\n"
        f"• Gravitational PE: $\\Delta V_g = -3(9.81)(0.8) = -23.54\\ \\mathrm{{J}}$\n"
        f"• Elastic PE Change:\n"
        f"  $\\Delta V_e = \\frac{{1}}{{2}}(200)(0.6^2 - 0.4^2) = 100(0.20) = 20.0\\ \\mathrm{{J}}$\n"
        f"• Conservation of Energy: $0 = \\Delta T + \\Delta V_g + \\Delta V_e$\n"
        f"  $0 = \\frac{{1}}{{2}}(3)v^2 - 23.54 + 20.0$\n"
        f"  $\\frac{{3}}{{2}}v^2 = 3.54\\ \\rightarrow\\ v = \\mathbf{{1.537\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• Current Velocity: $v = {v_curr:.3f}\\ \\mathrm{{m/s}}$ (Target at B: $1.537\\ \\mathrm{{m/s}}$)"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.5, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('Energy Conservation Monitor & Validation', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_111_vertical_rod_collar.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
