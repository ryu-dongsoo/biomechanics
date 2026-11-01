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
Dynamics 9th Edition - Chapter 3 Kinetics of Particles
Problem 3/44: Coriolis Acceleration and Normal Force in Rotating Tube (r-theta Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) standard layout (biomechanics-diagram-standard compliant)
- 1:1 textbook accurate geometry:
  * Base support bracket and pivot O bearing hub
  * Open hollow tube originating from pivot hub rim
  * Horizontal reference line, angle theta arc and label
  * Particle m = 0.1 kg sliding towards O with r_dot = -2 m/s
  * Constant CCW angular velocity theta_dot = 3 rad/s
- 100% verified against Wiley official solution manual:
  * Coriolis acceleration: a_theta = 2*r_dot*omega = 2(-2.0)(3.0) = -12.0 m/s^2
  * Normal force: N = m(g*cos 30° + a_theta) = 0.1(9.81*cos 30° - 12.0) = -0.350 N (|N| = 0.350 N, leading wall contact)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Matplotlib configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 1. Physical Parameters and Official Solutions
m = 0.1             # Particle mass (kg)
g = 9.81            # Gravity (m/s^2)
omega = 3.0         # Constant angular velocity (rad/s)
rdot = -2.0         # Relative velocity (m/s, towards O)
th_target_deg = 30.0
th_target = np.radians(th_target_deg)

# Wiley Official Solutions
a_theta_cor = 2.0 * rdot * omega            # -12.0 m/s^2
mg_theta = m * g * np.cos(th_target)        # +0.8496 N
N_theory = mg_theta + m * a_theta_cor       # -0.3504 N -> -0.350 N
N_mag = abs(N_theory)                       # 0.350 N

# 2. Animation Time Sampling
n_frames = 64
thetas = np.radians(np.linspace(12.0, 48.0, n_frames))
r_series = np.linspace(0.78, 0.32, n_frames)

# Canvas initialization (14 x 6.5, pure white background)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = thetas[frame]
    th_deg = np.degrees(th)
    r_curr = r_series[frame]
    
    cur_mg_th = m * g * np.cos(th)
    cur_N = cur_mg_th + m * a_theta_cor
    
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    
    # ---------------- 1. Main Physical View (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.25, 1.15)
    ax_main.set_ylim(-0.25, 0.95)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/44: Coriolis Acceleration and Normal Force in Rotating Tube', fontsize=13, fontweight='bold', pad=12)
    
    # (1) Base ground line
    ax_main.plot([-0.18, 0.18], [-0.12, -0.12], color='#37474f', lw=2.2, zorder=1)
    ax_main.add_patch(patches.Rectangle((-0.18, -0.16), 0.36, 0.04, facecolor='#ede7df', edgecolor='none', zorder=0))
    
    # (2) Triangular pivot bracket
    tri_pts = np.array([[-0.10, -0.12], [0.10, -0.12], [0.0, 0.0]])
    ax_main.add_patch(patches.Polygon(tri_pts, closed=True, facecolor='#cfd8dc', edgecolor='#455a64', lw=1.3, zorder=2))
    
    # (3) Circular bearing hub and pivot pin O
    hub_r = 0.055
    ax_main.add_patch(patches.Circle((0, 0), hub_r, facecolor='#eceff1', edgecolor='#37474f', lw=1.4, zorder=3))
    ax_main.add_patch(patches.Circle((0, 0), 0.022, facecolor='#263238', edgecolor='#263238', lw=1.0, zorder=4))
    ax_main.text(-0.11, 0.01, 'O', fontsize=16, fontweight='bold', color='#263238', zorder=5)
    
    # (4) Horizontal reference line
    ax_main.plot([0, 0.85], [0, 0], color='#78909c', lw=1.1, zorder=1)
    
    # (5) Angle theta arc
    arc_th = patches.Arc((0, 0), 0.40, 0.40, angle=0, theta1=0, theta2=th_deg, color='#263238', lw=1.2, zorder=4)
    ax_main.add_patch(arc_th)
    ax_main.text(0.24, 0.06, r'$\theta$', fontsize=13, fontweight='bold', color='#263238', zorder=5)
    
    # (6) Rotating Hollow Tube
    tube_len = 0.95
    tube_w = 0.075
    
    p1 = hub_r * u_r + (tube_w/2) * u_th
    p2 = tube_len * u_r + (tube_w/2) * u_th
    p3 = tube_len * u_r - (tube_w/2) * u_th
    p4 = hub_r * u_r - (tube_w/2) * u_th
    
    tube_poly = np.array([p1, p2, p3, p4])
    ax_main.add_patch(patches.Polygon(tube_poly, closed=True, facecolor='#e0f2f1', edgecolor='#37474f', lw=1.5, zorder=2))
    
    # Centerline
    ax_main.plot([0, (tube_len + 0.08)*u_r[0]], [0, (tube_len + 0.08)*u_r[1]],
                 color='#546e7a', ls='-.', lw=1.1, zorder=3)
    
    # (7) Particle m sliding inside tube
    pos_p = r_curr * u_r
    b_w, b_h = 0.09, tube_w * 0.88
    block = patches.Rectangle((-b_w/2, -b_h/2), b_w, b_h, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate(th).translate(pos_p[0], pos_p[1]) + ax_main.transData
    block.set_transform(t_blk)
    ax_main.add_patch(block)
    
    ax_main.text(pos_p[0], pos_p[1], 'm', fontsize=10, fontweight='bold', color='#4a2800',
                 ha='center', va='center', rotation=th_deg, zorder=6)
    
    # (8) Relative velocity r_dot
    v_arrow_len = 0.15
    v_start = pos_p
    v_end = pos_p - v_arrow_len * u_r
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.2), zorder=7)
    ax_main.text(v_end[0] - 0.06*u_r[0], v_end[1] + 0.04, r'$\dot{r} = -2\ \mathrm{m/s}$',
                 fontsize=10.5, fontweight='bold', color='#2e7d32', zorder=8)
    
    # (9) Angular velocity arrow
    om_r = 0.22
    arc_om = patches.Arc((0, 0), 2*om_r, 2*om_r, angle=0, theta1=th_deg + 15, theta2=th_deg + 45, color='#e65100', lw=1.8, zorder=5)
    ax_main.add_patch(arc_om)
    tip_th = np.radians(th_deg + 45)
    ax_main.annotate('', xy=(om_r*np.cos(tip_th), om_r*np.sin(tip_th)),
                     xytext=(om_r*np.cos(tip_th - 0.1), om_r*np.sin(tip_th - 0.1)),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.4', color='#e65100', lw=1.8), zorder=6)
    ax_main.text(om_r*np.cos(tip_th) - 0.04, om_r*np.sin(tip_th) + 0.04, r'$\dot{\theta} = 3\ \mathrm{rad/s}$',
                 fontsize=11, fontweight='bold', color='#e65100', zorder=7)
    
    # Status Banner
    if abs(th_deg - 30.0) < 2.0:
        pos_str = 'Passing Condition θ = 30.0°!'
        b_col, b_edge, b_txt = '#e8f5e9', '#81c784', '#1b5e20'
    else:
        pos_str = f'Rotating in Vertical Plane (θ = {th_deg:.1f}°)'
        b_col, b_edge, b_txt = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-0.20, 0.84, f'State: {pos_str}', fontsize=10.5, fontweight='bold', color=b_txt,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=b_col, edgecolor=b_edge, lw=1.2))
    
    # ---------------- 2. Analysis & Monitoring View (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD
    ax_calc.text(0.2, 9.7, '[Free Body Diagram - Polar Coordinates (r-θ)]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_bx, fbd_by = 4.5, 7.8
    fbd_sq = patches.Rectangle((fbd_bx - 0.7, fbd_by - 0.4), 1.4, 0.8,
                               facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_bx, fbd_by, r'$m = 0.1\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800', zorder=6)
    
    # Coordinate axes
    ax_calc.plot([fbd_bx + 1.8, fbd_bx + 3.0], [fbd_by, fbd_by], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 3.0, fbd_by), xytext=(fbd_bx + 1.8, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 3.1, fbd_by - 0.10, r'$+r$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([fbd_bx + 1.8, fbd_bx + 1.8], [fbd_by, fbd_by + 1.2], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 1.8, fbd_by + 1.2), xytext=(fbd_bx + 1.8, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 1.95, fbd_by + 1.15, r'$+\theta$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # Normal Force N
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 0.4 - 1.1), xytext=(fbd_bx, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by - 0.4 - 0.9, r'$N = 0.350\ \mathrm{N}$ (Leading Wall Contact)',
                 fontsize=10.5, fontweight='bold', color='#1565c0')
    
    # Gravity mg
    ax_calc.annotate('', xy=(fbd_bx - 0.6, fbd_by - 0.4 - 1.0), xytext=(fbd_bx - 0.6, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_bx - 1.45, fbd_by - 0.4 - 0.8, r'$mg$', fontsize=12, fontweight='bold', color='#d32f2f')
    
    # (2) Theoretical Derivation Card
    sol_text = (
        "[Theoretical Derivation (Polar Coordinates r-θ)]\n"
        r"• Parameters: $m = 0.1\ \mathrm{kg},\ \dot{\theta} = \omega = 3.0\ \mathrm{rad/s}\ (\ddot{\theta} = 0),\ \dot{r} = -2.0\ \mathrm{m/s}$" + "\n"
        r"• Transverse Acceleration (Coriolis):" + "\n"
        r"  $a_\theta = r\ddot{\theta} + 2\dot{r}\dot{\theta} = 0 + 2(-2.0)(3.0) = \mathbf{-12.0\ \mathrm{m/s^2}}$" + "\n"
        r"• Transverse Equation of Motion ($\sum F_\theta = m a_\theta,\ \theta = 30^\circ$):" + "\n"
        r"  $\sum F_\theta = N - mg\cos 30^\circ = m a_\theta$" + "\n"
        r"  $\Rightarrow N = mg\cos 30^\circ + m a_\theta = 0.1(9.81)\cos 30^\circ + 0.1(-12.0)$" + "\n"
        r"  $\Rightarrow N = 0.8496 - 1.200 = \mathbf{-0.350\ \mathrm{N}}$" + "\n"
        r"• Conclusion: Normal force magnitude is $\mathbf{|N| = 0.350\ \mathrm{N}}$, negative sign indicates" + "\n"
        r"  contact with the leading inside wall of the rotating tube!"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) Real-Time Dynamic Monitor
    live_text = (
        "[Real-Time Dynamic Monitor]\n"
        f"• Tube Angle: θ = {th_deg:.1f}° (Angular velocity ω = 3.0 rad/s)\n"
        f"• Radial Position: r = {r_curr:.3f} m (Relative speed r_dot = -2.0 m/s towards O)\n"
        f"• Coriolis Accel: 2·r_dot·ω = {a_theta_cor:.1f} m/s² (Constant)\n"
        f"• Gravity Transverse Component: mg cos θ = {cur_mg_th:.3f} N\n"
        f"• Normal Contact Force: N = {cur_N:+.3f} N (At θ = 30°: {N_theory:.3f} N)\n"
        f"• Wall Contact: Leading inside wall"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# Generate and save GIF animation
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_44_rotating_tube_particle.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Problem 3/44 English animation generated: {gif_path}")
