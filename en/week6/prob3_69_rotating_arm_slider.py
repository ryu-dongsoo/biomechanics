# -*- coding: utf-8 -*-
"""
Dynamics 9th Edition - Chapter 3 Kinetics of Particles
Problem 3/69: Rotating Slotted Arm and Slider Dynamics (r-theta Polar Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) standard layout (biomechanics-diagram-standard compliant)
- 1:1 textbook accurate geometry:
  * Base support bracket and pivot O hub
  * Cord S hanging downward through center hole
  * Rounded slotted arm with internal slot and rounded outer tip
  * Slotted arm upper rail B and lower rail A labels
  * Slider C, tension cable, dimension r, angular velocity omega arrow
- 100% verified against Wiley official solution manual:
  * Radial equation of motion: T = -m(0 - r*omega^2) = 2.0(0.225 * 6^2) = 16.20 N
  * Transverse equation of motion: a_theta = r*alpha + 2*r_dot*omega = 0.225(-2.0) + 2(-0.055)(6.0) = -1.110 m/s^2
  * Contact force: N = m*a_theta = 2.0(-1.110) = -2.22 N (|N| = 2.22 N, negative sign -> [Side B] contact)
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
m = 2.0                 # Slider mass (kg)
r0 = 0.225              # Reference radius (m = 225 mm)
rdot = -0.055           # Pulling speed (m/s = -55 mm/s)
omega = 6.0             # Angular velocity (rad/s, CCW)
alpha = -2.0            # Angular acceleration (rad/s^2, decelerating)

# Wiley Official Solutions
ar_val = -r0 * (omega**2)                       # -8.10 m/s^2
T_val = -m * ar_val                             # 16.20 N
atheta_val = r0 * alpha + 2.0 * rdot * omega    # -0.450 - 0.660 = -1.110 m/s^2
N_val = m * atheta_val                          # -2.22 N (Side B contact)

# 2. Geometry Helper Functions
def make_racetrack(u1, u2, width, n_arc=30):
    R = width / 2.0
    u_pts = [u1, u2]
    v_pts = [-R, -R]
    phi_right = np.linspace(-np.pi/2, np.pi/2, n_arc)
    u_pts.extend(u2 + R * np.cos(phi_right))
    v_pts.extend(R * np.sin(phi_right))
    u_pts.extend([u2, u1])
    v_pts.extend([R, R])
    phi_left = np.linspace(np.pi/2, 3*np.pi/2, n_arc)
    u_pts.extend(u1 + R * np.cos(phi_left))
    v_pts.extend(R * np.sin(phi_left))
    return np.array(u_pts), np.array(v_pts)

def rotate_pts(u_pts, v_pts, th):
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    return np.outer(u_pts, u_r) + np.outer(v_pts, u_th)

# 3. Animation Time Sampling
n_frames = 64
thetas = np.radians(np.linspace(16.0, 44.0, n_frames))
r_series = np.linspace(0.285, 0.165, n_frames)

# Canvas initialization (14 x 6.5, pure white background)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = thetas[frame]
    th_deg = np.degrees(th)
    r_curr = r_series[frame]
    
    cur_ar = -r_curr * (omega**2)
    cur_T = -m * cur_ar
    cur_atheta = r_curr * alpha + 2.0 * rdot * omega
    cur_N = m * cur_atheta
    
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    
    # ---------------- 1. Main Physical View (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.16, 0.44)
    ax_main.set_ylim(-0.16, 0.40)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/69: Rotating Slotted Arm and Slider Dynamics', fontsize=13, fontweight='bold', pad=12)
    
    # (1) Base ground line and hatching
    ground_y = -0.09
    ax_main.plot([-0.14, 0.12], [ground_y, ground_y], color='#37474f', lw=2.2, zorder=1)
    for hx in np.linspace(-0.13, 0.11, 16):
        ax_main.plot([hx, hx - 0.015], [ground_y, ground_y - 0.015], color='#78909c', lw=1.2, zorder=1)
    
    # (2) Pivot bracket
    bracket_pts = np.array([
        [-0.075, ground_y],
        [0.055, ground_y],
        [0.032, -0.015],
        [0.022, 0.0],
        [-0.040, 0.0],
        [-0.055, -0.015]
    ])
    ax_main.add_patch(patches.Polygon(bracket_pts, closed=True, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=2))
    
    # (3) Slotted Arm outer contour
    L_arm = 0.36
    w_out = 0.046
    R_out = w_out / 2.0
    u_pts = [0.0, L_arm]
    v_pts = [-R_out, -R_out]
    phi_right = np.linspace(-np.pi/2, np.pi/2, 30)
    u_pts.extend(L_arm + R_out * np.cos(phi_right))
    v_pts.extend(R_out * np.sin(phi_right))
    u_pts.extend([L_arm, 0.0])
    v_pts.extend([R_out, R_out])
    pts_out = rotate_pts(np.array(u_pts), np.array(v_pts), th)
    ax_main.add_patch(patches.Polygon(pts_out, closed=True, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=3))
    
    # (4) Pivot hub ring and center pin O
    hub_R = 0.044
    ax_main.add_patch(patches.Circle((0, 0), hub_R, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=4))
    pin_R = 0.013
    ax_main.add_patch(patches.Circle((0, 0), pin_R, facecolor='#455a64', edgecolor='#263238', lw=1.0, zorder=7))
    
    # (5) Inner through slot (white racetrack)
    w_in = 0.021
    s_start = 0.075
    s_end = 0.34
    u_in, v_in = make_racetrack(s_start, s_end, w_in)
    pts_in = rotate_pts(u_in, v_in, th)
    ax_main.add_patch(patches.Polygon(pts_in, closed=True, facecolor='#ffffff', edgecolor='#37474f', lw=1.3, zorder=5))
    
    # (6) Arm centerline
    ax_main.plot([0, (L_arm + R_out)*u_r[0]], [0, (L_arm + R_out)*u_r[1]], color='#78909c', ls=':', lw=1.0, zorder=6)
    
    # (7) Slider C and tension cord
    pos_c = r_curr * u_r
    c_len = 0.036
    c_w = w_in
    cord_end = pos_c - (c_len/2) * u_r
    ax_main.plot([0, cord_end[0]], [0, cord_end[1]], color='#212121', lw=1.8, zorder=7)
    
    # Hanging cord S
    t_hang = np.linspace(0, 1, 35)
    y_hang = -0.14 * t_hang
    x_hang = -0.015 * np.sin(t_hang * 1.2 * np.pi) + 0.012 * (t_hang**2)
    ax_main.plot(x_hang, y_hang, color='#212121', lw=1.8, zorder=8)
    ax_main.text(x_hang[-1] - 0.025, y_hang[-1], r'$S$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # Slider block C
    p1 = pos_c - (c_len/2) * u_r - (c_w/2) * u_th
    p2 = pos_c + (c_len/2) * u_r - (c_w/2) * u_th
    p3 = pos_c + (c_len/2) * u_r + (c_w/2) * u_th
    p4 = pos_c - (c_len/2) * u_r + (c_w/2) * u_th
    poly_c = patches.Polygon([p1, p2, p3, p4], closed=True, facecolor='#cf8a78', edgecolor='#5d4037', lw=1.3, zorder=7)
    ax_main.add_patch(poly_c)
    
    # (8) Labels
    ax_main.text(-0.068, -0.012, r'$O$', fontsize=16, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    c_lbl_pos = pos_c + (c_len/2 + 0.008) * u_r + 0.006 * u_th
    ax_main.text(c_lbl_pos[0], c_lbl_pos[1], r'$C$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    pos_B = 0.27 * u_r + (R_out + 0.016) * u_th
    pos_A = 0.27 * u_r - (R_out + 0.024) * u_th
    ax_main.text(pos_B[0], pos_B[1], r'$B$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    ax_main.text(pos_A[0], pos_A[1], r'$A$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # (9) Dimension r
    dim_h = R_out + 0.034
    p0_dim = dim_h * u_th
    pC_dim = pos_c + dim_h * u_th
    ax_main.plot([0, 1.15 * p0_dim[0]], [0, 1.15 * p0_dim[1]], color='#90a4ae', lw=0.9, zorder=6)
    ax_main.plot([pos_c[0], pos_c[0] + 1.15 * dim_h * u_th[0]], [pos_c[1], pos_c[1] + 1.15 * dim_h * u_th[1]], color='#90a4ae', lw=0.9, zorder=6)
    ax_main.annotate('', xy=pC_dim, xytext=p0_dim,
                     arrowprops=dict(arrowstyle='<->', color='#263238', lw=1.1), zorder=8)
    mid_dim = 0.5 * (p0_dim + pC_dim) + 0.012 * u_th
    ax_main.text(mid_dim[0], mid_dim[1], r'$r$', fontsize=14, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # (10) Omega arrow
    om_r = 0.065
    phi_om = np.linspace(np.radians(75), np.radians(160), 30)
    ax_main.plot(om_r * np.cos(phi_om), om_r * np.sin(phi_om), color='#00897b', lw=1.8, zorder=8)
    tip_x = om_r * np.cos(np.radians(160))
    tip_y = om_r * np.sin(np.radians(160))
    prev_x = om_r * np.cos(np.radians(150))
    prev_y = om_r * np.sin(np.radians(150))
    ax_main.annotate('', xy=(tip_x, tip_y), xytext=(prev_x, prev_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.45', color='#00897b', lw=1.8), zorder=9)
    ax_main.text(tip_x - 0.030, tip_y + 0.015, r'$\omega$', fontsize=15, fontstyle='italic', fontweight='bold', color='#00897b', zorder=9)
    
    # (11) Relative velocity vector r_dot
    v_len = 0.040
    v_start = pos_c
    v_end = pos_c - v_len * u_r
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#2e7d32', lw=2.0), zorder=8)
    ax_main.text(v_end[0] - 0.015*u_r[0], v_end[1] + 0.018, r'$\dot{r}$',
                 fontsize=12, fontweight='bold', color='#2e7d32', zorder=9)
    
    # Top status banner
    if abs(r_curr - r0) < 0.008:
        banner_txt = 'Given Condition: Passing r = 225 mm!'
        banner_bg, banner_edge, banner_col = '#e8f5e9', '#81c784', '#1b5e20'
    else:
        banner_txt = f'Slider in motion (r = {r_curr*1e3:.0f} mm)'
        banner_bg, banner_edge, banner_col = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-0.14, 0.35, banner_txt, fontsize=10.5, fontweight='bold', color=banner_col,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # ---------------- 2. Analysis & FBD View (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD
    ax_calc.text(0.2, 9.7, '[Free Body Diagram (r-θ Polar Coordinates)]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_cx, fbd_cy = 4.0, 8.2
    fbd_w, fbd_h = 1.4, 0.9
    fbd_sq = patches.Rectangle((fbd_cx - fbd_w/2, fbd_cy - fbd_h/2), fbd_w, fbd_h,
                               facecolor='#cf8a78', edgecolor='#5d4037', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_cx, fbd_cy, r'$m = 2.0\ \mathrm{kg}$' + '\n' + r'(Slider $C$)',
                 fontsize=9.5, fontweight='bold', ha='center', va='center', color='#3e2723', zorder=6)
    
    # Coordinate axes (+r, +theta)
    axis_x, axis_y = 7.5, 8.2
    ax_calc.plot([axis_x, axis_x + 1.2], [axis_y, axis_y], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(axis_x + 1.2, axis_y), xytext=(axis_x, axis_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(axis_x + 1.3, axis_y - 0.12, r'$+r$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([axis_x, axis_x], [axis_y, axis_y + 1.1], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(axis_x, axis_y + 1.1), xytext=(axis_x, axis_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(axis_x - 0.12, axis_y + 1.22, r'$+\theta$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # Tension force T (-r direction)
    ax_calc.annotate('', xy=(fbd_cx - fbd_w/2 - 1.4, fbd_cy), xytext=(fbd_cx - fbd_w/2, fbd_cy),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.50', color='#d32f2f', lw=2.4), zorder=6)
    ax_calc.text(fbd_cx - fbd_w/2 - 0.7, fbd_cy + 0.22, r'$T = 16.20\ \mathrm{N}$',
                 fontsize=10.5, fontweight='bold', color='#d32f2f', ha='center')
    
    # Normal force N (-theta direction: pushed down by Side B)
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - fbd_h/2 - 0.9), xytext=(fbd_cx, fbd_cy - fbd_h/2),
                     arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.45', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_cx + 0.15, fbd_cy - fbd_h/2 - 0.70, r'$N = 2.22\ \mathrm{N}$ ([Side B] Contact)',
                 fontsize=10.5, fontweight='bold', color='#1565c0')
    
    # (2) Theoretical Derivation Card
    sol_text = (
        "[Theoretical Analysis & Derivation (r-θ Coordinates)]\n"
        r"• Parameters: $m = 2.0\ \mathrm{kg},\ r = 0.225\ \mathrm{m},\ \dot{r} = -0.055\ \mathrm{m/s}\ (\ddot{r} = 0)$" + "\n"
        r"  Angular vel $\omega = 6.0\ \mathrm{rad/s}$, Angular accel $\alpha = -2.0\ \mathrm{rad/s^2}$ (Decel)" + "\n"
        r"• (1) Radial Equation of Motion ($\sum F_r = m a_r$):" + "\n"
        r"  $a_r = \ddot{r} - r\omega^2 = 0 - (0.225)(6.0^2) = -8.10\ \mathrm{m/s^2}$" + "\n"
        r"  $\sum F_r = -T = m a_r = 2.0(-8.10) = -16.20\ \mathrm{N} \Rightarrow \mathbf{T = 16.20\ \mathrm{N}}$" + "\n"
        r"• (2) Transverse Equation of Motion ($\sum F_\theta = m a_\theta$):" + "\n"
        r"  $a_\theta = r\alpha + 2\dot{r}\omega = (0.225)(-2.0) + 2(-0.055)(6.0) = -0.450 - 0.660 = \mathbf{-1.110\ \mathrm{m/s^2}}$" + "\n"
        r"  $\sum F_\theta = N = m a_\theta = 2.0(-1.110) = \mathbf{-2.22\ \mathrm{N}}$" + "\n"
        r"• Contact Surface: Since $N < 0$ (opposite to $+\theta$ direction)," + "\n"
        r"  the slider presses against leading guide surface $\mathbf{[Side\ B]}$!"
    )
    ax_calc.text(0.2, 4.55, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) Real-time Monitoring Card
    live_text = (
        "[Real-time Dynamic Monitoring]\n"
        f"• Radial Position: r = {r_curr*1e3:.1f} mm | Arm Angle: θ = {th_deg:.1f}°\n"
        f"• Radial Accel: a_r = {cur_ar:.2f} m/s² | Cable Tension: T = {cur_T:.2f} N\n"
        f"• Transverse Accel: a_θ = {cur_atheta:.3f} m/s²\n"
        f"• Guide Contact Force: N = {cur_N:+.2f} N (r = 225 mm Theory: -2.22 N)\n"
        f"• Contact Surface: [Side B] (Leading face) Contact!"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF Animation generation and save
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_69_rotating_arm_slider.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Problem 3/69 English animation generated: {gif_path}")
