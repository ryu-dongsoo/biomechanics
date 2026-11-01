"""
Dynamics 9th Edition Chapter 3 Part B: Work and Energy
Advanced Problem 1 - Problem 3/101 - Motion of Slider on Vertical Loop and Rough Incline
- Pure white background (#ffffff) & Accurate tangency and rough incline illustration
- Wiley Solution Manual verified:
  * (a) Normal force just after B: N_B = 4 m g
  * (b) Normal force at bottom C: N_C = 7 m g
  * (c) Stopping distance along incline past D: s = 4 R / (1 + μ_k * sqrt(3))
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m = 1.0             # Mass (kg)
g = 9.81            # Gravity (m/s^2)
R = 1.0             # Radius (m)
mu_k = 0.25         # Friction coefficient
theta_deg = 30.0    # Incline angle (deg)
theta = np.radians(theta_deg)

# Theoretical solutions
NB_val = 4.0 * m * g
vB = np.sqrt(4.0 * g * R)
NC_val = 7.0 * m * g
vC = np.sqrt(6.0 * g * R)
s_stop = (4.0 * R) / (1.0 + mu_k * np.sqrt(3.0))  # ~2.791 m

# Trajectory
y_seg1 = np.linspace(2*R, 0, 16)
x_seg1 = np.zeros_like(y_seg1)

ang_seg2 = np.linspace(np.pi, 5.0 * np.pi / 3.0, 20)
x_seg2 = R + R * np.cos(ang_seg2)
y_seg2 = R * np.sin(ang_seg2)

p_tang = np.array([R + R*np.cos(-np.pi/3), R*np.sin(-np.pi/3)])
p_D = np.array([3.0 * R, 0.0])
dist_tang_D = np.linalg.norm(p_D - p_tang)
s_tang_D = np.linspace(0, dist_tang_D, 8)[1:]
incline_u = np.array([np.cos(theta), np.sin(theta)])
x_seg3 = p_tang[0] + s_tang_D * incline_u[0]
y_seg3 = p_tang[1] + s_tang_D * incline_u[1]

s_incline = np.linspace(0, s_stop, 15)[1:]
x_seg4 = p_D[0] + s_incline * incline_u[0]
y_seg4 = p_D[1] + s_incline * incline_u[1]

traj_x = np.concatenate([x_seg1, x_seg2, x_seg3, x_seg4])
traj_y = np.concatenate([y_seg1, y_seg2, y_seg3, y_seg4])
n_frames = len(traj_x)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    px = traj_x[frame]
    py = traj_y[frame]
    
    if px <= 3.0 * R:
        v_curr = np.sqrt(max(0.0, 2 * g * (2*R - py)))
        s_inc_curr = 0.0
    else:
        s_inc_curr = (px - 3.0*R) / np.cos(theta)
        U_f_curr = -mu_k * m * g * np.cos(theta) * s_inc_curr
        U_g_curr = m * g * (2*R - py)
        Utot = U_g_curr + U_f_curr
        v_curr = np.sqrt(max(0.0, 2 * Utot / m))
        
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.85, 6.2)
    ax_main.set_ylim(-1.6, 2.7)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    smooth_x = np.concatenate([x_seg1, x_seg2, x_seg3])
    smooth_y = np.concatenate([y_seg1, y_seg2, y_seg3])
    ax_main.plot(smooth_x, smooth_y, color='#2b2b2b', lw=2.5)
    
    end_x = p_D[0] + (s_stop + 0.6) * incline_u[0]
    end_y = p_D[1] + (s_stop + 0.6) * incline_u[1]
    ax_main.plot([p_D[0], end_x], [p_D[1], end_y], color='#2b2b2b', lw=2.5)
    
    rough_poly = np.array([
        p_D,
        [end_x, end_y],
        [end_x, end_y - 0.28],
        [p_D[0], -0.28]
    ])
    ax_main.fill(rough_poly[:, 0], rough_poly[:, 1], color='#f4ede4', edgecolor='none')
    ax_main.text(4.2, 0.2, r'$\mu_k$', fontsize=12, fontweight='bold', color='#6d4013')
    
    ax_main.plot([0, 3.8], [0, 0], color='#888888', ls='--', lw=1.2)
    
    # Center O_arc
    ax_main.plot(R, 0, 'k+', markersize=8, markeredgewidth=1.5)
    
    # Radius R
    ang_r = np.radians(-135)
    p_r = np.array([R + R*np.cos(ang_r), R*np.sin(ang_r)])
    ax_main.plot([R, p_r[0]], [0, p_r[1]], color='#555555', lw=1.2)
    ax_main.annotate('', xy=p_r, xytext=(R, 0),
                     arrowprops=dict(arrowstyle='->', color='#555555', lw=1.2))
    ax_main.text(R + 0.5*R*np.cos(ang_r) - 0.1, 0.5*R*np.sin(ang_r) + 0.05, r'$R$', fontsize=11, fontweight='bold')
    
    # 30 deg line
    ax_main.plot([R, R], [0, -R], color='#888888', ls='-.', lw=1.2)
    ax_main.plot([R, p_tang[0]], [0, p_tang[1]], color='#888888', ls='-.', lw=1.2)
    arc_30 = patches.Arc((R, 0), 1.2, 1.2, angle=0, theta1=-90, theta2=-60, color='#333333', lw=1.3)
    ax_main.add_patch(arc_30)
    ax_main.text(R + 0.18, -0.7, r'$30^\circ$', fontsize=10.5, fontweight='bold')
    
    # Dimension 2R
    ax_main.plot([-0.25, -0.4], [2*R, 2*R], color='#888888', lw=1)
    ax_main.plot([-0.05, -0.4], [0, 0], color='#888888', lw=1)
    ax_main.annotate('', xy=(-0.35, 2*R), xytext=(-0.35, 0),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(-0.42, R, r'$2R$', fontsize=12, fontweight='bold', ha='right', va='center')
    
    # Markers
    ax_main.plot(0, 2*R, 'ko', markersize=3.5)
    ax_main.text(0.12, 2*R, r'$A$', fontsize=13, fontweight='bold')
    ax_main.plot(0, 0, 'ko', markersize=3.5)
    ax_main.text(0.12, 0.08, r'$B$', fontsize=13, fontweight='bold')
    ax_main.plot(R, -R, 'ko', markersize=3.5)
    ax_main.text(R, -R - 0.22, r'$C$', fontsize=13, fontweight='bold', ha='center')
    ax_main.plot(p_D[0], p_D[1], 'ko', markersize=3.5)
    ax_main.text(p_D[0] + 0.1, -0.15, r'$D$', fontsize=13, fontweight='bold')
    
    # Dimension s
    norm_inc = np.array([-np.sin(theta), np.cos(theta)])
    p_E = p_D + s_stop * incline_u
    d_off = 0.35 * norm_inc
    ax_main.plot([p_D[0], (p_D + d_off)[0]], [p_D[1], (p_D + d_off)[1]], color='#888888', lw=1)
    ax_main.plot([p_E[0], (p_E + d_off)[0]], [p_E[1], (p_E + d_off)[1]], color='#888888', lw=1)
    ax_main.annotate('', xy=p_E + d_off, xytext=p_D + d_off,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    s_mid = 0.5 * (p_D + p_E) + d_off + 0.08 * norm_inc
    ax_main.text(s_mid[0], s_mid[1], r'$s$', fontsize=12, fontweight='bold', ha='center', va='bottom', rotation=theta_deg)
    
    # Slider
    if px == 0:
        slider_ang = 90
    elif px < p_tang[0]:
        phi_curr = np.arctan2(py, px - R)
        slider_ang = np.degrees(phi_curr) + 90
    else:
        slider_ang = theta_deg
        
    sl_w, sl_h = 0.24, 0.16
    slider = patches.Rectangle((-sl_w/2, 0), sl_w, sl_h,
                               facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    t_sl = plt.matplotlib.transforms.Affine2D().rotate_deg(slider_ang).translate(px, py) + ax_main.transData
    slider.set_transform(t_sl)
    ax_main.add_patch(slider)
    
    # Velocity vector
    if v_curr > 0.1:
        if px == 0:
            v_dir = np.array([0, -1])
        elif px < p_tang[0]:
            phi_curr = np.arctan2(py, px - R)
            v_dir = np.array([-np.sin(phi_curr), np.cos(phi_curr)])
        else:
            v_dir = incline_u
        v_arrow_len = v_curr * 0.08
        ax_main.annotate('', xy=(px + v_dir[0]*v_arrow_len, py + v_dir[1]*v_arrow_len), xytext=(px, py),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
        
    ax_main.set_title('Problem 3/101: Slider on Curved Track and Rough Incline', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Analysis:\n"
        "(a) Normal force just after B (N_B):\n"
        r"  $\bullet\ v_B^2 = 2 g (2R) = 4 g R$" "\n"
        r"  $\bullet\ \sum F_n = m \frac{v_B^2}{\rho} \Rightarrow N_B = m \frac{4gR}{R} = \mathbf{4 m g}$" "\n\n"
        "(b) Normal force at bottom C (N_C):\n"
        r"  $\bullet\ v_C^2 = 2 g (3R) = 6 g R$" "\n"
        r"  $\bullet\ N_C - mg = m \frac{v_C^2}{R} \Rightarrow N_C = mg + 6mg = \mathbf{7 m g}$" "\n\n"
        "(c) Stopping distance s along incline past D:\n"
        r"  $\bullet\ \Delta T = 0 \Rightarrow U_{A-E} = 0$" "\n"
        r"  $\bullet\ m g [2R - s \sin 30^\circ] - \mu_k (mg \cos 30^\circ) s = 0$" "\n"
        r"  $\bullet\ 2R - s [\frac{1}{2} + \mu_k \frac{\sqrt{3}}{2}] = 0$" "\n"
        r"  $\mathbf{s = \frac{4R}{1 + \mu_k \sqrt{3}}}$"
    )
    ax_calc.text(0.5, 5.75, sol_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'Position: $x = {px:.2f}\\ \\mathrm{{m}},\\ y = {py:.2f}\\ \\mathrm{{m}}$\n'
        f'Incline Distance: $s = {s_inc_curr:.2f}\\ /\\ {s_stop:.2f}\\ \\mathrm{{m}}$\n'
        f'Current Speed: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$\n'
        f'Theoretical: $N_B = 4mg,\\ N_C = 7mg,\\ s = {s_stop:.2f}\\ \\mathrm{{m}}$'
    )
    ax_calc.text(0.5, 1.5, live_box, fontsize=10.2, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Work-Energy Analysis & Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_101_slider_loop_incline.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
