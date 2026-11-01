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
Dynamics 9th Edition Chapter 3: Kinetics of Particles
Sample Problem 3/6: Maximum Speed for Block on Curved Guide Rail to Maintain Contact (n-t Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) layout standard (biomechanics-diagram-standard compliant)
- Exact 1:1 textbook geometry reproduction (30° incline approach, circular arc rho, upper clearance rail, crest A)
- Wiley Solution Manual verified: v_max = sqrt(g * rho) = 6.26 m/s (22.55 km/h)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
rho = 4.0               # Radius of curvature (m)
g = 9.81                # Gravitational acceleration (m/s^2)
m = 10.0                # Block mass (kg)
W_val = m * g           # Weight (98.1 N)
v_max = np.sqrt(g * rho)# 6.264 m/s (22.55 km/h)

th_T = np.radians(30.0)
th_exit = np.radians(25.0)

thetas_arc = np.linspace(-th_T, th_exit, 60)
x_arc = rho * np.sin(thetas_arc)
y_arc = rho * np.cos(thetas_arc) - rho

p_T = np.array([-rho * np.sin(th_T), rho * np.cos(th_T) - rho])
incline_unit = np.array([-np.cos(th_T), -np.sin(th_T)])
s_inc_len = 2.5
s_inc = np.linspace(s_inc_len, 0, 30)
x_inc = p_T[0] + s_inc * incline_unit[0]
y_inc = p_T[1] + s_inc * incline_unit[1]

track_x = np.concatenate([x_inc, x_arc])
track_y = np.concatenate([y_inc, y_arc])
n_frames = len(track_x)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    px = track_x[frame]
    py = track_y[frame]
    
    if px < p_T[0]:
        phi = np.radians(30.0)
        theta_curr = -th_T
        cur_rho = np.inf
    else:
        theta_curr = np.arcsin(np.clip(px / rho, -1.0, 1.0))
        phi = -theta_curr
        cur_rho = rho
        
    cur_v = v_max
    cur_an = (cur_v**2) / cur_rho if cur_rho < 1e6 else 0.0
    cur_N = max(0.0, m * (g * np.cos(theta_curr) - cur_an))
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-4.5, 3.2)
    ax_main.set_ylim(-2.8, 1.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    ax_main.plot(0, -rho, 'k+', ms=10, mew=1.8)
    ax_main.text(0.12, -rho - 0.05, r'$C$', fontsize=11, fontweight='bold')
    ax_main.plot([0, 0], [-rho, 0.4], color='#888888', ls='-.', lw=1.2)
    ax_main.plot([0, p_T[0]], [-rho, p_T[1]], color='#888888', ls='--', lw=1.0)
    
    arc_patch = patches.Arc((0, -rho), 2.2, 2.2, angle=90, theta1=0, theta2=30, color='#333333', lw=1.2)
    ax_main.add_patch(arc_patch)
    ax_main.text(-0.35, -rho + 1.25, r'$30^\circ$', fontsize=10.5, fontweight='bold')
    
    ax_main.plot(track_x, track_y, color='#2b2b2b', lw=2.5)
    
    gap = 0.35
    norm_inc = np.array([-np.sin(th_T), np.cos(th_T)])
    up_inc_x = x_inc + gap * norm_inc[0]
    up_inc_y = y_inc + gap * norm_inc[1]
    up_arc_x = (rho + gap) * np.sin(thetas_arc)
    up_arc_y = (rho + gap) * np.cos(thetas_arc) - rho
    ax_main.plot(np.concatenate([up_inc_x, up_arc_x]),
                 np.concatenate([up_inc_y, up_arc_y]),
                 color='#666666', lw=1.8, ls='-')
    
    hatch_poly = np.vstack([
        np.column_stack([track_x, track_y]),
        np.column_stack([track_x[::-1], track_y[::-1] - 0.25])
    ])
    ax_main.add_patch(patches.Polygon(hatch_poly, facecolor='#ede9e4', edgecolor='none'))
    
    dim_th = np.radians(12.0)
    dim_p = np.array([rho * np.sin(dim_th), rho * np.cos(dim_th) - rho])
    ax_main.annotate('', xy=dim_p, xytext=(0, -rho),
                     arrowprops=dict(arrowstyle='<->', color='#1565c0', lw=1.4))
    ax_main.text(dim_p[0]/2 + 0.15, (dim_p[1] - rho)/2, r'$\rho = 4.0\ \mathrm{m}$',
                 color='#1565c0', fontsize=11, fontweight='bold')
    
    ax_main.plot(0, 0, 'ko', ms=4.5)
    ax_main.text(0.12, 0.12, r'$A$', fontsize=13, fontweight='bold')
    
    bw, bh = 0.45, 0.28
    block = patches.Rectangle((-bw/2, 0), bw, bh, facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(np.degrees(phi)).translate(px, py) + ax_main.transData
    block.set_transform(t_blk)
    ax_main.add_patch(block)
    
    blk_mid = np.array([px - np.sin(phi)*bh/2, py + np.cos(phi)*bh/2])
    ax_main.text(blk_mid[0], blk_mid[1], r'$m$', fontsize=10.5, fontweight='bold', color='#4a2800',
                 ha='center', va='center')
    
    v_dir = np.array([np.cos(phi), np.sin(phi)])
    v_len = cur_v * 0.16
    v_end = blk_mid + v_len * v_dir
    ax_main.annotate('', xy=v_end, xytext=blk_mid,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
    ax_main.text(v_end[0] + 0.08, v_end[1] + 0.10, f'$v = {cur_v:.2f}\\ \\mathrm{{m/s}}$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold')
    
    ax_main.set_title('Sample Problem 3/6: Block Traversing Curved Guide Rail', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Analysis & FBD View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    fbd_cx, fbd_cy = 3.2, 7.8
    fbd_w, fbd_h = 1.4, 0.9
    fbd_blk = patches.Rectangle((fbd_cx - fbd_w/2, fbd_cy - fbd_h/2), fbd_w, fbd_h,
                                facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    ax_calc.add_patch(fbd_blk)
    ax_calc.text(fbd_cx, fbd_cy, r'$m = 10\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800')
    
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - fbd_h/2 - 1.2), xytext=(fbd_cx, fbd_cy - fbd_h/2),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy - fbd_h/2 - 0.7, r'$mg = 98.1\ \mathrm{N}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold')
    
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy + fbd_h/2 + 0.9), xytext=(fbd_cx, fbd_cy + fbd_h/2),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy + fbd_h/2 + 0.5, r'$N\ (\to 0)$',
                 color='#1565c0', fontsize=10.5, fontweight='bold')
    
    ax_calc.annotate('', xy=(6.5, 7.8), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(6.6, 7.7, r'$t$', fontsize=11, fontweight='bold')
    ax_calc.annotate('', xy=(5.6, 6.9), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(5.5, 6.6, r'$n$', fontsize=11, fontweight='bold')
    ax_calc.text(5.6, 8.2, r'FBD at Crest $A$', fontsize=11, fontweight='bold', color='#333333')
    
    sol_box = (
        "Theoretical Derivation & Analysis:\n"
        r"$\bullet$ $n-t$ equation of motion: $\sum F_n = m a_n = m \frac{v^2}{\rho}$" "\n"
        r"$\bullet$ At crest $A$ ($\theta = 0^\circ$): $mg - N = m \frac{v^2}{\rho}$" "\n"
        r"$\bullet$ Contact maintenance condition ($N \geq 0$):" "\n"
        r"  $N = m\left(g - \frac{v^2}{\rho}\right) \geq 0 \Rightarrow v \leq \sqrt{g\rho}$" "\n"
        r"$\bullet$ Critical separation speed threshold:" "\n"
        r"  $\mathbf{v_{\max} = \sqrt{g\rho} = \sqrt{9.81 \times 4.0} = 6.26\ \mathrm{m/s}}$" "\n"
        r"  ($\mathbf{v_{\max} = 22.55\ \mathrm{km/h}}$)"
    )
    ax_calc.text(0.5, 4.3, sol_box, fontsize=10.0, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'Position: $x = {px:.2f}\\ \\mathrm{{m}},\\ y = {py:.2f}\\ \\mathrm{{m}}$\n'
        f'Speed: $v = {cur_v:.2f}\\ \\mathrm{{m/s}}$ ({cur_v*3.6:.1f} km/h)\n'
        f'Normal Accel: $a_n = {cur_an:.2f}\\ \\mathrm{{m/s^2}}$\n'
        f'Normal Force: $N = {cur_N:.1f}\\ \\mathrm{{N}}$ (Threshold: $v_{{\\max}} = 6.26\\ \\mathrm{{m/s}}$)'
    )
    ax_calc.text(0.5, 1.25, live_box, fontsize=10.2, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Normal-Tangential (n-t) Analysis & Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_6_curved_track_block.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
