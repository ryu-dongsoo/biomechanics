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
Fundamental Practice 2 (Problem 3/112) - Slider on Vertical-Curved Track with Spring Bumper
- Pure white background (#ffffff) & exact 1:1 textbook layout
- Wiley Solution Manual Verified:
  * (a) Velocity at point B: v_B = sqrt(2 * g * h_B) = sqrt(2 * 9.81 * 4.5) = 9.40 m/s
  * (b) Maximum spring compression: delta = sqrt(2 * m * g * h_f / k) = 0.0542 m = 54.2 mm
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
m = 1.2             # Slider mass (kg)
g = 9.81            # Gravitational acceleration (m/s^2)
k = 24000.0         # Spring stiffness (N/m = 24 kN/m)
h_vert = 3.0        # Vertical drop height (m)
R = 1.5             # Bottom curve radius (m)
h_B = h_vert + R    # Total drop to point B = 4.5 m
h_f = h_vert        # Net drop to bumper E = 3.0 m

# Theoretical Values
v_B_exact = np.sqrt(2.0 * g * h_B)                # 9.40 m/s
delta_exact = np.sqrt(2.0 * m * g * h_f / k)      # 0.0542 m = 54.2 mm
v_E_contact = np.sqrt(2.0 * g * h_f)              # 7.67 m/s

n_frames = 55
t_stage = np.linspace(0, 1.0, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.25, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=10, width=0.12, color='#2b2b2b', lw=2.0):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-5:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.04
    active_len = max(length - 2 * lead_len, 0.02)
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

def get_slider_pos(tau):
    if tau < 0.28:
        frac = tau / 0.28
        y = 3.0 - 3.0 * (frac**1.3)
        x = 0.0
        tang = -np.pi / 2.0
        y_drop = 3.0 - y
        comp = 0.0
    elif tau < 0.52:
        frac = (tau - 0.28) / (0.52 - 0.28)
        ang = np.pi + frac * (np.pi / 2.0)
        x = 1.5 + 1.5 * np.cos(ang)
        y = 1.5 * np.sin(ang)
        tang = ang + np.pi / 2.0
        y_drop = 3.0 - y
        comp = 0.0
    elif tau < 0.72:
        frac = (tau - 0.52) / (0.72 - 0.52)
        ang = 1.5 * np.pi + frac * (np.pi / 6.0)
        x = 1.5 + 1.5 * np.cos(ang)
        y = 1.5 * np.sin(ang)
        tang = ang + np.pi / 2.0
        y_drop = 3.0 - y
        comp = 0.0
    elif tau < 0.88:
        frac = (tau - 0.72) / (0.88 - 0.72)
        x_start = 1.5 + 1.5 * np.cos(1.666 * np.pi)
        y_start = 1.5 * np.sin(1.666 * np.pi)
        x = x_start + frac * (3.8 - x_start)
        y = y_start + frac * (0.0 - y_start)
        tang = np.radians(30.0) * (1.0 - frac)
        y_drop = 3.0 - y
        comp = 0.0
    else:
        frac = (tau - 0.88) / (1.0 - 0.88)
        x = 3.8 + frac * 0.25
        y = 0.0
        tang = 0.0
        y_drop = 3.0
        comp = frac * delta_exact
    
    Vg = -m * g * y_drop
    Ve = 0.5 * k * comp**2
    T = max(- (Vg + Ve), 0.0)
    v = np.sqrt(2.0 * T / m)
    return x, y, tang, y_drop, comp, Vg, Ve, T, v

def update(frame):
    tau = t_stage[frame]
    x, y, tang, y_drop, comp, Vg, Ve, T, v = get_slider_pos(tau)
    
    # ---------------- 1. Main System View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.6, 5.0)
    ax_main.set_ylim(-2.2, 4.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Ceiling Mount A
    ax_main.plot([-0.3, 0.3], [3.8, 3.8], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.28, 0.24, 6):
        ax_main.plot([hx, hx + 0.06], [3.8, 4.0], color='#666666', lw=1.2)
    mount_top = patches.Polygon([[-0.25, 3.8], [0.25, 3.8], [0.15, 3.4], [-0.15, 3.4]],
                                facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_top)
    
    # Right Wall Mount E
    ax_main.plot([4.6, 4.6], [-0.4, 0.4], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.36, 0.32, 7):
        ax_main.plot([4.6, 4.75], [hy, hy + 0.06], color='#666666', lw=1.2)
    mount_right = patches.Polygon([[4.6, -0.3], [4.6, 0.3], [4.3, 0.15], [4.3, -0.15]],
                                  facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_right)
    
    # Guide Rod Profile
    ax_main.plot([0.0, 0.0], [0.0, 3.5], color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot([0.0, 0.0], [0.0, 3.5], color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    
    th_arc = np.linspace(np.pi, 1.666 * np.pi, 60)
    ax_main.plot(1.5 + 1.5 * np.cos(th_arc), 1.5 * np.sin(th_arc), color='#4682b4', lw=8.0, zorder=2)
    ax_main.plot(1.5 + 1.5 * np.cos(th_arc), 1.5 * np.sin(th_arc), color='#d0e4f7', lw=3.0, zorder=2)
    
    x_c = 1.5 + 1.5 * np.cos(1.666 * np.pi)
    y_c = 1.5 * np.sin(1.666 * np.pi)
    track_x = np.array([x_c, 3.2, 3.6, 4.3])
    track_y = np.array([y_c, -0.4, 0.0, 0.0])
    ax_main.plot(track_x, track_y, color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot(track_x, track_y, color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    
    # Bumper Spring at E
    sp_start_x = max(x + 0.15, 3.8 + (x - 3.8)) if tau >= 0.88 else 3.8
    draw_spring(ax_main, (sp_start_x, 0.0), (4.3, 0.0), nodes=8, width=0.10, color='#2b2b2b', lw=2.0)
    ax_main.text(4.0, -0.32, r'$k = 24\ \mathrm{kN/m}$', ha='center', fontsize=9.5, fontweight='bold', color='#1a5276')
    
    # Slider Collar
    collar = patches.Circle((x, y), 0.16, facecolor='#e67e22', edgecolor='#78341a', lw=1.8, zorder=5)
    ax_main.add_patch(collar)
    ax_main.plot(x, y, 'o', color='#2b2b2b', markersize=4, zorder=6)
    
    # Velocity Arrow
    if v > 0.3:
        v_scale = 0.045 * (v / v_B_exact)
        vx = np.cos(tang) * v_scale
        vy = np.sin(tang) * v_scale
        ax_main.annotate('', xy=(x + vx, y + vy), xytext=(x, y),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
    
    # Dimensions & Labels
    ax_main.plot([-0.35, -0.35], [0.0, 3.0], color='#333333', lw=1.2)
    ax_main.plot([-0.45, 0.0], [3.0, 3.0], color='#777777', ls='--', lw=1.0)
    ax_main.plot([-0.45, 0.0], [0.0, 0.0], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(-0.35, 3.0), xytext=(-0.35, 1.8), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(-0.35, 0.0), xytext=(-0.35, 1.2), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(-0.55, 1.5, r'$3\ \mathrm{m}$', va='center', fontsize=11, fontweight='bold')
    
    ax_main.plot([-0.35, -0.35], [-1.5, 0.0], color='#333333', lw=1.2)
    ax_main.plot([-0.45, 1.5], [-1.5, -1.5], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(-0.35, -1.5), xytext=(-0.35, -0.9), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(-0.35, 0.0), xytext=(-0.35, -0.6), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(-0.65, -0.75, r'$1.5\ \mathrm{m}$', va='center', fontsize=10.5)
    
    ax_main.plot([0.0, 3.8], [0.0, 0.0], color='#999999', ls='-.', lw=1.0)
    arc_30 = patches.Arc((1.5, 0.0), 1.2, 1.2, angle=270, theta1=0, theta2=30, color='#222222', lw=1.2)
    ax_main.add_patch(arc_30)
    ax_main.text(1.7, -0.5, r'$30^\circ$', fontsize=10)
    
    ax_main.text(0.25, 3.0, r'$A\ (1.2\ \mathrm{kg})$', fontsize=11, fontweight='bold')
    ax_main.text(1.5, -1.85, r'$B$', fontsize=12, fontweight='bold', ha='center')
    ax_main.text(3.6, 0.25, r'$E$', fontsize=12, fontweight='bold')
    
    ax_main.set_title('Problem 3/112: Vertical-Curved Track & Bumper Spring', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. Energy Monitor & Theory Card ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T, Ve, Vg, T + Ve + Vg]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$V_e$', r'$V_g$', r'$E_{\mathrm{tot}}$']
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 55.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"[Work-Energy Analysis (Problem 3/112)]\n"
        f"• (a) Velocity at B (Datum at A):\n"
        f"  $h_B = 3 + 1.5 = 4.5\\ \\mathrm{{m}}$\n"
        f"  $T_A + V_A = T_B + V_B\\ \\rightarrow\\ 0 + 0 = \\frac{{1}}{{2}}mv_B^2 - mgh_B$\n"
        f"  $v_B = \\sqrt{{2gh_B}} = \\sqrt{{2(9.81)(4.5)}} = \\mathbf{{9.40\\ \\mathrm{{m/s}}}}$\n"
        f"• (b) Maximum spring deflection $\\delta$ (State F):\n"
        f"  Net drop $h_f = 3.0\\ \\mathrm{{m}}$\n"
        f"  $0 + 0 = 0 - mgh_f + \\frac{{1}}{{2}}k\\delta^2$\n"
        f"  $\\delta = \\sqrt{{\\frac{{2mgh_f}}{{k}}}} = \\sqrt{{\\frac{{2(1.2)(9.81)(3)}}{{24000}}}}$\n"
        f"  $\\delta = 0.0542\\ \\mathrm{{m}} = \\mathbf{{54.2\\ \\mathrm{{mm}}}}$\n"
        f"─────────────────────────────\n"
        f"• Velocity: $v = {v:.2f}\\ \\mathrm{{m/s}},\\quad$ Drop: $h = {y_drop:.2f}\\ \\mathrm{{m}}$"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.2, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('Mechanical Energy Conservation & Validation', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_112_curved_guide_bumper.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
