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
Sample Problem 3/7: Motion Analysis of Circular Chute and No-Slip Conveyor Belt (n-t Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) standard layout (biomechanics-diagram-standard compliant)
- Exact 1:1 textbook geometry reproduction (radius R circular chute, lowest point B, conveyor pulley & belt)
- Wiley Solution Manual verified: N(θ) = 3mg sin(θ), point B N = 294.3 N, pulley ω = 21.9 rad/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
R = 3.0             # Chute curvature radius (m)
r_p = 0.35          # Pulley radius (m)
m = 10.0            # Mass (kg)
g = 9.81            # Gravitational acceleration (m/s^2)
W = m * g           # 98.1 N

# Theoretical values
v_B = np.sqrt(2.0 * g * R)      # 7.672 m/s
omega_p = v_B / r_p             # 21.92 rad/s (209.3 RPM)
N_B = 3.0 * W                   # 294.3 N

# Trajectory generation
n_chute = 45
thetas = np.linspace(0.02, np.pi/2, n_chute)
x_chute = -R * np.cos(thetas)
y_chute = R - R * np.sin(thetas)

n_belt = 25
x_belt = np.linspace(0, 2.5, n_belt)
y_belt = np.zeros_like(x_belt)

traj_x = np.concatenate([x_chute, x_belt])
traj_y = np.concatenate([y_chute, y_belt])
n_frames = len(traj_x)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    px = traj_x[frame]
    py = traj_y[frame]
    
    if frame < n_chute:
        th = thetas[frame]
        v_curr = np.sqrt(2.0 * g * R * np.sin(th))
        N_curr = 3.0 * m * g * np.sin(th)
        an_curr = (v_curr**2) / R
        phi = np.pi/2 - th
        mode_str = "Sliding on Chute"
    else:
        th = np.pi/2
        v_curr = v_B
        N_curr = m * g
        an_curr = 0.0
        phi = 0.0
        mode_str = "Conveyor Transport"
        
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-3.8, 3.8)
    ax_main.set_ylim(-1.5, 3.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    ax_main.plot(0, R, 'k+', ms=9, mew=1.6)
    ax_main.text(0.12, R + 0.1, r'$O$', fontsize=12, fontweight='bold')
    ax_main.plot([-R, 0], [R, R], color='#888888', ls='--', lw=1.2)
    ax_main.plot([0, 0], [0, R], color='#888888', ls='-.', lw=1.2)
    
    th_full = np.linspace(0, np.pi/2, 100)
    ax_main.plot(-R * np.cos(th_full), R - R * np.sin(th_full), color='#2b2b2b', lw=2.6)
    
    hatch_poly = np.vstack([
        np.column_stack([-R * np.cos(th_full), R - R * np.sin(th_full)]),
        np.column_stack([- (R - 0.25) * np.cos(th_full[::-1]), R - (R - 0.25) * np.sin(th_full[::-1])])
    ])
    ax_main.add_patch(patches.Polygon(hatch_poly, facecolor='#ede9e4', edgecolor='none'))
    
    dim_th = np.radians(45.0)
    dim_pt = np.array([-R * np.cos(dim_th), R - R * np.sin(dim_th)])
    ax_main.annotate('', xy=dim_pt, xytext=(0, R),
                     arrowprops=dict(arrowstyle='<->', color='#1565c0', lw=1.4))
    ax_main.text(dim_pt[0]/2 - 0.2, (dim_pt[1] + R)/2 + 0.15, r'$R = 3.0\ \mathrm{m}$',
                 color='#1565c0', fontsize=10.5, fontweight='bold')
    
    ax_main.plot(-R, R, 'ko', ms=4.5)
    ax_main.text(-R - 0.35, R + 0.05, r'$A$', fontsize=13, fontweight='bold')
    ax_main.plot(0, 0, 'ko', ms=4.5)
    ax_main.text(-0.25, -0.32, r'$B$', fontsize=13, fontweight='bold')
    
    p_center = np.array([0, -r_p])
    pulley_circ = patches.Circle(p_center, r_p, facecolor='#d8e4eb', edgecolor='#456678', lw=1.8)
    ax_main.add_patch(pulley_circ)
    ax_main.plot(p_center[0], p_center[1], 'ko', ms=3.5)
    ax_main.plot([0, 2.8], [0, 0], color='#2b2b2b', lw=2.4)
    ax_main.plot([0, 2.8], [-2*r_p, -2*r_p], color='#2b2b2b', lw=1.8)
    
    ax_main.annotate('', xy=(p_center[0] - r_p, p_center[1]), xytext=p_center,
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))
    ax_main.text(p_center[0] - r_p/2 - 0.1, p_center[1] + 0.08, r'$r$', fontsize=10.5, fontweight='bold')
    
    rot_arc = patches.Arc(p_center, 1.2*r_p, 1.2*r_p, angle=0, theta1=-60, theta2=60, color='#e65100', lw=1.8)
    ax_main.add_patch(rot_arc)
    ax_main.annotate('', xy=(p_center[0] + 0.6*r_p, p_center[1]), xytext=(p_center[0] + 0.6*r_p, p_center[1] + 0.1),
                     arrowprops=dict(arrowstyle='->', color='#e65100', lw=2.0))
    ax_main.text(p_center[0] + 0.7*r_p, p_center[1] - 0.1, r'$\omega$', color='#e65100', fontsize=12, fontweight='bold')
    
    bw, bh = 0.35, 0.22
    blk_angle = -np.degrees(phi)
    block = patches.Rectangle((-bw/2, 0), bw, bh, facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(blk_angle).translate(px, py) + ax_main.transData
    block.set_transform(t_blk)
    ax_main.add_patch(block)
    
    if v_curr > 0.2:
        v_dir = np.array([np.cos(phi), -np.sin(phi)])
        v_len = v_curr * 0.14
        blk_center = np.array([px - np.sin(phi)*bh/2, py + np.cos(phi)*bh/2])
        v_end = blk_center + v_len * v_dir
        ax_main.annotate('', xy=v_end, xytext=blk_center,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
        ax_main.text(v_end[0] + 0.08, v_end[1] + 0.12, f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$',
                     color='#2e7d32', fontsize=10.5, fontweight='bold')
        
    ax_main.set_title('Sample Problem 3/7: Circular Chute and No-Slip Conveyor', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Analysis & FBD View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    fbd_cx, fbd_cy = 3.2, 7.8
    fbd_blk = patches.Rectangle((fbd_cx - 0.6, fbd_cy - 0.4), 1.2, 0.8,
                                facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    ax_calc.add_patch(fbd_blk)
    ax_calc.text(fbd_cx, fbd_cy, r'$10\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800')
    
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - 1.5), xytext=(fbd_cx, fbd_cy - 0.4),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy - 1.1, r'$mg = 98.1\ \mathrm{N}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold')
    
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy + 1.3), xytext=(fbd_cx, fbd_cy + 0.4),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.4, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy + 0.85, r'$N(\theta) = 3mg\sin\theta$',
                 color='#1565c0', fontsize=10.5, fontweight='bold')
    
    ax_calc.annotate('', xy=(6.5, 7.8), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(6.6, 7.7, r'$t$', fontsize=11, fontweight='bold')
    ax_calc.annotate('', xy=(5.6, 8.7), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(5.5, 8.8, r'$n$', fontsize=11, fontweight='bold')
    ax_calc.text(5.6, 7.2, r'FBD along Chute', fontsize=11, fontweight='bold', color='#333333')
    
    sol_box = (
        "Theoretical Derivation & Analysis:\n"
        r"(1) Contact force $N(\theta)$ derivation:" "\n"
        r"  $\bullet\ v^2 = 2gR\sin\theta$" "\n"
        r"  $\bullet\ \sum F_n = N - mg\sin\theta = m\frac{v^2}{R} = 2mg\sin\theta$" "\n"
        r"  $\bullet\ \mathbf{N(\theta) = 3mg\sin\theta = 294.3\sin\theta\ \mathrm{N}}$" "\n"
        r"  $\bullet\ $At bottom point B ($\theta = 90^\circ$): $\mathbf{N_B = 3mg = 294\ \mathrm{N}}$" "\n\n"
        r"(2) Belt no-slip pulley angular velocity $\omega$:" "\n"
        r"  $\bullet\ v_B = \sqrt{2gR} = \sqrt{2(9.81)(3.0)} = 7.67\ \mathrm{m/s}$" "\n"
        r"  $\bullet\ v_{\mathrm{belt}} = r\omega \Rightarrow \mathbf{\omega = \frac{v_B}{r} = \frac{7.67}{0.35} = 21.9\ \mathrm{rad/s}}$" "\n"
        r"  ($N_{\mathrm{rpm}} = 209\ \mathrm{RPM}$)"
    )
    ax_calc.text(0.5, 3.8, sol_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'Status: {mode_str} | Angle: $\\theta = {np.degrees(th):.1f}^\\circ$\n'
        f'Speed: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ ({v_curr*3.6:.1f} km/h)\n'
        f'Normal Accel: $a_n = {an_curr:.2f}\\ \\mathrm{{m/s^2}}$\n'
        f'Contact Force: $N = {N_curr:.1f}\\ \\mathrm{{N}}$ (Theoretical B: $N_B = 294\\ \\mathrm{{N}}$)'
    )
    ax_calc.text(0.5, 0.95, live_box, fontsize=10.0, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Normal-Tangential (n-t) Analysis & Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_7_chute_conveyor.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
