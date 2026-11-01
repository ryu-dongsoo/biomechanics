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
Dynamics 9th Edition - Chapter 3 Kinetics of Particles - Problem 3/44 Concept Deep Dive (GIF Animation)
Coriolis Acceleration Geometric Origins and Leading Wall Contact Mechanism
- 2-panel (15x7.5) pure white background (#ffffff) standard layout (biomechanics-diagram-standard compliant)
- Left: Dynamic rotating tube, inward particle motion, and real-time contact force N
- Right: Dynamic vector decomposition of Origin 1 (circumferential speed reduction) and Origin 2 (radial vector rotation) with live monitoring
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Matplotlib configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 1. Physical Parameters
m = 0.1             # Particle mass (kg)
g = 9.81            # Gravitational acceleration (m/s^2)
omega = 3.0         # Constant angular velocity (rad/s)
rdot = -2.0         # Relative speed toward O (m/s)

# Coriolis acceleration & components
a1_val = rdot * omega               # -6.0 m/s^2 (Circumferential speed reduction rate)
a2_val = rdot * omega               # -6.0 m/s^2 (Radial vector rotation rate)
a_coriolis = a1_val + a2_val        # -12.0 m/s^2

# 2. Time Sampling (angle: 12° -> 48°, r: 0.78 m -> 0.32 m)
n_frames = 64
thetas = np.radians(np.linspace(12.0, 48.0, n_frames))
r_series = np.linspace(0.78, 0.32, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 7.5), gridspec_kw={'width_ratios': [1.02, 1.28]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.06, left=0.05, right=0.96, wspace=0.14)

def update(frame):
    th = thetas[frame]
    th_deg = np.degrees(th)
    r_curr = r_series[frame]
    
    cur_mg_th = m * g * np.cos(th)          # Gravity transverse component (+u_th)
    cur_N = cur_mg_th + m * a_coriolis      # Normal force (negative -> Leading Wall contact)
    cur_v_theta = r_curr * omega            # Current circumferential speed (m/s)
    
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    
    # =========================================================================
    # Left Panel: Physical System & Contact Force Mechanism
    # =========================================================================
    ax1.cla()
    ax1.set_facecolor('#ffffff')
    ax1.set_xlim(-0.25, 1.15)
    ax1.set_ylim(-0.25, 1.05)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Problem 3/44: Normal Contact Force N and Coriolis Mechanism', fontsize=10.5, fontweight='bold', pad=10)
    
    # Ground line & hatching
    ground_y = -0.12
    ax1.plot([-0.20, 0.20], [ground_y, ground_y], color='#37474f', lw=2.2, zorder=1)
    for hx in np.linspace(-0.19, 0.19, 17):
        ax1.plot([hx, hx - 0.015], [ground_y, ground_y - 0.015], color='#90a4ae', lw=1.2, zorder=1)
    
    # Pivot bracket
    tri_pts = np.array([[-0.10, ground_y], [0.10, ground_y], [0.0, 0.0]])
    ax1.add_patch(patches.Polygon(tri_pts, closed=True, facecolor='#cfd8dc', edgecolor='#455a64', lw=1.3, zorder=2))
    
    # Pivot O
    hub_r = 0.055
    ax1.add_patch(patches.Circle((0, 0), hub_r, facecolor='#eceff1', edgecolor='#37474f', lw=1.4, zorder=3))
    ax1.add_patch(patches.Circle((0, 0), 0.020, facecolor='#263238', edgecolor='#263238', lw=1.0, zorder=4))
    ax1.text(-0.12, 0.01, r'$O$', fontsize=16, fontstyle='italic', fontweight='bold', color='#263238', zorder=5)
    
    # Horizontal reference & angle arc
    ax1.plot([0, 0.85], [0, 0], color='#78909c', lw=1.1, ls=':', zorder=1)
    arc_th = patches.Arc((0, 0), 0.40, 0.40, angle=0, theta1=0, theta2=th_deg, color='#263238', lw=1.3, zorder=4)
    ax1.add_patch(arc_th)
    ax1.text(0.24, 0.06, rf'$\theta = {th_deg:.1f}^\circ$', fontsize=10.5, fontweight='bold', color='#263238', zorder=5)
    
    # Rotating tube
    tube_len = 0.95
    tube_w = 0.08
    p1 = hub_r * u_r + (tube_w/2) * u_th
    p2 = tube_len * u_r + (tube_w/2) * u_th
    p3 = tube_len * u_r - (tube_w/2) * u_th
    p4 = hub_r * u_r - (tube_w/2) * u_th
    
    ax1.add_patch(patches.Polygon(np.array([p1, p2, p3, p4]), closed=True, facecolor='#f4fbf7', edgecolor='#37474f', lw=1.4, zorder=2))
    
    # Leading Wall (red highlight)
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#c62828', lw=3.2, zorder=3)
    ax1.text(p2[0] - 0.28*u_r[0] + 0.045*u_th[0], p2[1] - 0.28*u_r[1] + 0.045*u_th[1],
             'Leading Wall [Contact Surface!]', fontsize=9.5, fontweight='bold', color='#c62828', zorder=6)
    
    # Trailing Wall
    ax1.text(p3[0] - 0.28*u_r[0] - 0.055*u_th[0], p3[1] - 0.28*u_r[1] - 0.055*u_th[1],
             'Trailing Wall (Non-contact)', fontsize=9.5, fontweight='bold', color='#546e7a', zorder=6)
    
    # Centerline
    ax1.plot([0, (tube_len + 0.05)*u_r[0]], [0, (tube_len + 0.05)*u_r[1]], color='#90a4ae', ls='-.', lw=1.0, zorder=3)
    
    # Particle block (r_curr position)
    pos_p = r_curr * u_r
    b_w, b_h = 0.09, tube_w * 0.94
    p_c1 = pos_p - (b_w/2)*u_r - (b_h/2)*u_th
    p_c2 = pos_p + (b_w/2)*u_r - (b_h/2)*u_th
    p_c3 = pos_p + (b_w/2)*u_r + (b_h/2)*u_th
    p_c4 = pos_p - (b_w/2)*u_r + (b_h/2)*u_th
    ax1.add_patch(patches.Polygon(np.array([p_c1, p_c2, p_c3, p_c4]), closed=True, facecolor='#d7a15c', edgecolor='#5d4037', lw=1.4, zorder=4))
    ax1.text(pos_p[0], pos_p[1], r'$m = 0.1\ \mathrm{kg}$', fontsize=9.5, fontweight='bold', color='#3e2723', ha='center', va='center', zorder=5)
    
    # Relative velocity r_dot (toward O)
    v_len = 0.15
    ax1.annotate('', xy=pos_p - v_len*u_r, xytext=pos_p,
                 arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.45', color='#2e7d32', lw=2.4), zorder=6)
    ax1.text(pos_p[0] - (v_len+0.04)*u_r[0], pos_p[1] - (v_len+0.04)*u_r[1] + 0.03,
             r'$\dot{r} = -2.0\ \mathrm{m/s}$', fontsize=10.5, fontweight='bold', color='#2e7d32', zorder=7)
    
    # Angular velocity omega arrow
    om_r = 0.22
    phi_om = np.linspace(np.radians(th_deg + 15), np.radians(th_deg + 55), 30)
    ax1.plot(om_r*np.cos(phi_om), om_r*np.sin(phi_om), color='#e65100', lw=2.0, zorder=5)
    tip_om = np.radians(th_deg + 55)
    ax1.annotate('', xy=(om_r*np.cos(tip_om), om_r*np.sin(tip_om)),
                 xytext=(om_r*np.cos(tip_om - 0.12), om_r*np.sin(tip_om - 0.12)),
                 arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.45', color='#e65100', lw=2.0), zorder=6)
    ax1.text(om_r*np.cos(tip_om) - 0.08, om_r*np.sin(tip_om) + 0.03,
             r'$\omega = 3.0\ \mathrm{rad/s}$', fontsize=10.5, fontweight='bold', color='#e65100', zorder=7)
    
    # Normal contact force N (-u_th direction)
    f_N_len = 0.16
    ax1.annotate('', xy=pos_p - f_N_len*u_th, xytext=pos_p,
                 arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.50', color='#1565c0', lw=2.6), zorder=7)
    ax1.text(pos_p[0] - f_N_len*u_th[0] + 0.02, pos_p[1] - f_N_len*u_th[1] - 0.04,
             rf'$N = {abs(cur_N):.3f}\ \mathrm{{N}}$' + '\n' + '(Leading wall normal force)', fontsize=9.5, fontweight='bold', color='#1565c0', zorder=8)
    
    # Gravity mg (downward)
    f_mg_len = 0.18
    ax1.annotate('', xy=(pos_p[0], pos_p[1] - f_mg_len), xytext=pos_p,
             arrowprops=dict(arrowstyle='->,head_width=0.30,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax1.text(pos_p[0] - 0.08, pos_p[1] - f_mg_len - 0.03, r'$mg = 0.981\ \mathrm{N}$', fontsize=9.5, fontweight='bold', color='#d32f2f', zorder=7)
    
    # Gravity transverse component (+u_th)
    f_mg_th_len = 0.12 * (cur_mg_th / 0.850)
    ax1.annotate('', xy=pos_p + f_mg_th_len*u_th, xytext=pos_p,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#d32f2f', lw=1.5, ls='--'), zorder=6)
    ax1.text(pos_p[0] + f_mg_th_len*u_th[0] - 0.22, pos_p[1] + f_mg_th_len*u_th[1] + 0.015,
             rf'$mg\cos\theta = {cur_mg_th:.3f}\ \mathrm{{N}}$', fontsize=9.0, fontweight='bold', color='#d32f2f', zorder=7)
    
    # Top banner
    if abs(th_deg - 30.0) < 1.5:
        banner_txt = 'Given Condition θ = 30.0° Instant! (N = -0.350 N)'
        banner_bg, banner_edge, banner_col = '#e8f5e9', '#81c784', '#1b5e20'
    else:
        banner_txt = f'Rotating in Vertical Plane (θ = {th_deg:.1f}°, r = {r_curr:.2f} m)'
        banner_bg, banner_edge, banner_col = '#f5f5f5', '#e0e0e0', '#424242'
    ax1.text(-0.20, 0.88, banner_txt, fontsize=10, fontweight='bold', color=banner_col,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # =========================================================================
    # Right Panel: Geometric Decomposition of Coriolis Accel
    # =========================================================================
    ax2.cla()
    ax2.set_facecolor('#ffffff')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title(r'Geometric Decomposition of Coriolis Accel: $2\dot{r}\dot{\theta} = \dot{r}\dot{\theta} + \dot{r}\dot{\theta}$',
                  fontsize=12.5, fontweight='bold', pad=12)
    
    # ----------------- [Origin 1] Top Area -----------------
    ax2.text(0.2, 9.6, r'[Origin 1] Circumferential Speed ($v_\theta = r\omega$) Magnitude Reduction',
             fontsize=11, fontweight='bold', color='#1565c0')
    
    t1_desc = (
        r"• Particle moves inward by $\Delta r = \dot{r}\Delta t$ toward $O$ in $\Delta t$ ($r_2 < r_1$)" + "\n"
        r"• Tangential speed at $r_1$: $v_{\theta 1} = r_1 \omega$" + "\n"
        r"• Tangential speed at $r_2$: $v_{\theta 2} = (r_1 + \dot{r}\Delta t)\omega = v_{\theta 1} + (\dot{r}\omega)\Delta t$" + "\n"
        r"• Transverse acceleration from speed magnitude drop:" + "\n"
        r"  $\mathbf{a_1 = \frac{\Delta v_\theta}{\Delta t} = \dot{r}\omega = (-2.0)(3.0) = -6.0\ \mathrm{m/s^2}}$"
    )
    ax2.text(0.2, 8.0, t1_desc, fontsize=9.0, va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f4fd', edgecolor='#90caf9', lw=1.2))
    
    # Dynamic vector diagram 1
    arc_r1 = patches.Arc((6.6, 6.4), 4.5, 4.5, angle=0, theta1=20, theta2=55, color='#b0bec5', lw=1.2, ls=':')
    arc_r2 = patches.Arc((6.6, 6.4), 3.0, 3.0, angle=0, theta1=20, theta2=55, color='#b0bec5', lw=1.2, ls=':')
    ax2.add_patch(arc_r1)
    ax2.add_patch(arc_r2)
    
    p_v1 = np.array([8.3, 8.1])
    ax2.annotate('', xy=p_v1 + np.array([-1.2, 0.9]), xytext=p_v1,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#1565c0', lw=2.2))
    ax2.text(p_v1[0] - 0.4, p_v1[1] + 0.65, r'$v_{\theta 1} = r_1\omega$', fontsize=8.8, fontweight='bold', color='#1565c0')
    
    v2_scale = 0.5 + 0.5 * (r_curr - 0.32) / (0.78 - 0.32)
    p_v2 = np.array([7.8, 7.5])
    ax2.annotate('', xy=p_v2 + np.array([-1.2 * v2_scale, 0.9 * v2_scale]), xytext=p_v2,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#1565c0', lw=2.2))
    ax2.text(p_v2[0] + 0.1, p_v2[1] + 0.15, rf'$v_\theta(t) = {cur_v_theta:.2f}\ \mathrm{{m/s}}$', fontsize=8.8, fontweight='bold', color='#1565c0')
    
    ax2.annotate('', xy=p_v1 + np.array([0.45, -0.35]), xytext=p_v1,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#d32f2f', lw=2.0))
    ax2.text(p_v1[0] + 0.5, p_v1[1] - 0.35, r'$\Delta v_\theta = \dot{r}\omega\Delta t$' + '\n' + r'(Speed drop)',
             fontsize=8.3, fontweight='bold', color='#d32f2f')
    
    # ----------------- [Origin 2] Middle Area -----------------
    ax2.text(0.2, 6.3, r'[Origin 2] Radial Velocity ($\mathbf{v}_r$) Vector Rotation with Coordinate Frame',
             fontsize=11, fontweight='bold', color='#2e7d32')
    
    t2_desc = (
        r"• Radial velocity vector of particle: $\mathbf{v}_r = \dot{r}\mathbf{e}_r$" + "\n"
        r"• As the tube rotates by $\Delta\theta = \omega\Delta t$ CCW," + "\n"
        r"  the radial unit vector $\mathbf{e}_r$ rotates into transverse direction $\mathbf{e}_\theta$:" + "\n"
        r"  $\frac{d\mathbf{e}_r}{dt} = \dot{\theta}\mathbf{e}_\theta = \omega\mathbf{e}_\theta$" + "\n"
        r"• Transverse acceleration from vector rotation:" + "\n"
        r"  $\mathbf{a_2 = \dot{r}\frac{d\mathbf{e}_r}{dt} = \dot{r}\omega = (-2.0)(3.0) = -6.0\ \mathrm{m/s^2}}$"
    )
    ax2.text(0.2, 4.7, t2_desc, fontsize=9.0, va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f8f0', edgecolor='#a5d6a7', lw=1.2))
    
    # Dynamic vector diagram 2
    p_orig = np.array([7.6, 4.2])
    v_r1 = np.array([1.5, 0.5])
    ax2.annotate('', xy=p_orig - v_r1, xytext=p_orig,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#2e7d32', lw=2.2))
    ax2.text(p_orig[0] - 1.1, p_orig[1] - 0.55, r'$\mathbf{v}_r(t)$', fontsize=9.0, fontweight='bold', color='#2e7d32')
    
    rot_angle = np.radians(18.0) * np.sin(np.pi * frame / n_frames)
    c_rot, s_rot = np.cos(rot_angle), np.sin(rot_angle)
    v_r2_dyn = np.array([v_r1[0]*c_rot - v_r1[1]*s_rot, v_r1[0]*s_rot + v_r1[1]*c_rot])
    ax2.annotate('', xy=p_orig - v_r2_dyn, xytext=p_orig,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#2e7d32', lw=1.8, ls='--'))
    ax2.text(p_orig[0] - 1.4, p_orig[1] + 0.45, r'$\mathbf{v}_r(t+\Delta t)$', fontsize=9.0, fontweight='bold', color='#2e7d32')
    
    ax2.annotate('', xy=p_orig - v_r2_dyn, xytext=p_orig - v_r1,
                 arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#d32f2f', lw=2.2))
    ax2.text(p_orig[0] - 1.9, p_orig[1] - 0.05, r'$\Delta\mathbf{v}_r = v_r\Delta\theta\mathbf{e}_\theta$' + '\n' + r'$= \dot{r}\omega\Delta t\mathbf{e}_\theta$',
             fontsize=8.3, fontweight='bold', color='#d32f2f')
    
    # ----------------- [Live Monitoring & Final Synthesis] Bottom Area -----------------
    sum_desc = (
        "[Real-time Monitoring & Total Coriolis Accel Synthesis]\n"
        f"• Tube Angle: θ = {th_deg:.1f}° | Radius: r = {r_curr:.3f} m | Tangential Speed: v_θ = {cur_v_theta:.2f} m/s\n"
        r"• Total Transverse Accel: $a_\theta = a_1 + a_2 = \dot{r}\omega + \dot{r}\omega = 2\dot{r}\omega = \mathbf{-12.0\ \mathrm{m/s^2}}$ (Constant)" + "\n"
        rf"• Newton's Law: $N = mg\cos\theta + m a_\theta = {cur_mg_th:.3f} + (-1.200) = \mathbf{{{cur_N:+.3f}\ \mathrm{{N}}}}$" + "\n"
        r"• Verdict: $N < 0$ proves Leading Wall presses backward on particle throughout motion!"
    )
    ax2.text(0.2, 1.6, sum_desc, fontsize=9.1, va='center',
             bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#37474f', lw=1.4))

# GIF Animation generation and save
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_44_coriolis_explanation.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Problem 3/44 Coriolis explanation GIF animation generated: {gif_path}")
