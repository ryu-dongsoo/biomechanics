"""
Dynamics 9th Edition Chapter 3 Part B: Work and Energy
Sample Problem 3/14 - Power and Acceleration of Log Pulled by Winch up an Incline
- Pure white background (#ffffff) & Realistic log lying flat on 30 deg incline
- Wiley Solution Manual verified:
  * N = 360(9.81) cos 30° = 3060 N
  * Steady state (P = 4 kW, v = 1.2 m/s): T = 3333 N, μ_k = 0.513
  * Power surge (P = 6 kW): T = 5000 N, a = 4.63 m/s^2
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
m = 360.0           # Log mass (kg)
g = 9.81            # Gravity (m/s^2)
theta_deg = 30.0    # Incline angle (deg)
theta = np.radians(theta_deg)
v0 = 1.2            # Steady speed (m/s)

# Force calculations
W = m * g                          # 3531.6 N
N = W * np.cos(theta)              # 3058.4 N (~3060 N)
W_tang = W * np.sin(theta)         # 1765.8 N

# Steady state (4 kW)
P1 = 4000.0         # 4 kW = 4000 W
T1 = P1 / v0        # 3333.3 N (~3333 N)
F_f = T1 - W_tang   # 1567.5 N
mu_k = F_f / N      # 0.5125 (~0.513)

# Power surge (6 kW)
P2 = 6000.0         # 6 kW = 6000 W
T2 = P2 / v0        # 5000.0 N
F_net2 = T2 - W_tang - F_f  # 1666.7 N
a2 = F_net2 / m             # 4.630 m/s^2 (~4.63 m/s^2)

# Animation setup
n_frames = 50
t_total = 2.5
dt = t_total / n_frames

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

# Unit vectors
tang_dir = np.array([np.cos(theta), np.sin(theta)])
norm_dir = np.array([-np.sin(theta), np.cos(theta)])

# Ramp geometry
x0, y0 = 1.0, 1.0
incline_len = 10.0
top_x = x0 + incline_len * np.cos(theta)
top_y = y0 + incline_len * np.sin(theta)

pulley_pos = np.array([top_x, top_y])
winch_pos = np.array([top_x + 2.4, top_y])

log_w, log_h = 3.2, 0.75

def update(frame):
    is_surge = (frame >= 25)
    t = frame * dt
    
    if not is_surge:
        s_travel = v0 * t
        v_curr = v0
        a_curr = 0.0
        P_curr = P1
        T_curr = T1
    else:
        t_surge = (frame - 25) * dt
        s_travel = v0 * (25 * dt) + v0 * t_surge + 0.5 * a2 * t_surge**2
        v_curr = v0 + a2 * t_surge
        a_curr = a2
        P_curr = P2
        T_curr = T2
        
    s_curr = 1.5 + s_travel * 0.75
    
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 14.5)
    ax_main.set_ylim(0.2, 8.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Incline ramp
    ax_main.plot([x0 - 0.6, top_x, top_x + 3.8], [y0 - 0.6 * np.tan(theta), top_y, top_y], color='#2b2b2b', lw=2.2)
    ground_poly = np.array([
        [x0 - 0.6, y0 - 0.6 * np.tan(theta)],
        [top_x, top_y],
        [top_x + 3.8, top_y],
        [top_x + 3.8, 0.6],
        [x0 - 0.6, 0.6]
    ])
    ax_main.fill(ground_poly[:, 0], ground_poly[:, 1], color='#f4ede4', edgecolor='none')
    
    # 30 deg arc
    y_base = y0 - 0.6 * np.tan(theta)
    ax_main.plot([x0 - 0.6, x0 + 2.6], [y_base, y_base], color='#777777', ls='--', lw=1.2)
    arc = patches.Arc((x0 - 0.6, y_base), 3.2, 3.2, angle=0, theta1=0, theta2=theta_deg, color='#222222', lw=1.5)
    ax_main.add_patch(arc)
    ax_main.text(x0 + 1.6, y_base + 0.28, r'$30^\circ$', fontsize=12, fontweight='bold', color='#222222')
    
    # Pulley and winch
    ax_main.add_patch(patches.Circle(pulley_pos + [0, 0.22], 0.22, facecolor='#cbe2ee', edgecolor='#133c4d', lw=1.4))
    
    winch_stand = patches.Polygon([[winch_pos[0]-0.4, top_y], [winch_pos[0]+0.4, top_y], [winch_pos[0], top_y+0.75]],
                                  facecolor='#b8cdd8', edgecolor='#133c4d', lw=1.4)
    ax_main.add_patch(winch_stand)
    drum_center = winch_pos + [0, 0.75]
    ax_main.add_patch(patches.Circle(drum_center, 0.52, facecolor='#d99b66', edgecolor='#7a4d25', lw=1.8))
    ax_main.add_patch(patches.Circle(drum_center, 0.14, facecolor='#ffffff', edgecolor='#333333', lw=1.4))
    ax_main.text(drum_center[0] + 0.75, drum_center[1], r'$A$', fontsize=13, fontweight='bold', va='center')
    
    rot_arc = patches.Arc(drum_center, 1.5, 1.5, angle=0, theta1=65, theta2=155, color='#2e7d32', lw=2.2)
    ax_main.add_patch(rot_arc)
    
    # Log position
    log_base = np.array([x0, y0]) + s_curr * tang_dir
    log_center = log_base + (log_h / 2.0) * norm_dir
    
    # Log body (single rotation!)
    log_poly = patches.Rectangle((-log_w/2, -log_h/2), log_w, log_h,
                                 facecolor='#d7a15c', edgecolor='#6d4013', lw=2.0)
    t_log = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(log_center[0], log_center[1]) + ax_main.transData
    log_poly.set_transform(t_log)
    ax_main.add_patch(log_poly)
    
    # Wood grain lines
    for frac in [-0.25, 0.0, 0.25]:
        p1 = log_center - 0.42 * log_w * tang_dir + frac * log_h * norm_dir
        p2 = log_center + 0.42 * log_w * tang_dir + frac * log_h * norm_dir
        ax_main.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#8b531b', lw=1.0)
    ax_main.text(log_center[0], log_center[1] + 0.05, '360 kg', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800', rotation=theta_deg)
    
    # Cable
    log_front = log_center + (log_w/2) * tang_dir
    pulley_cable_pt = pulley_pos + [0, 0.44]
    drum_cable_pt = drum_center + [0, 0.52]
    ax_main.plot([log_front[0], pulley_cable_pt[0]], [log_front[1], pulley_cable_pt[1]], color='#111111', lw=2)
    ax_main.plot([pulley_cable_pt[0], drum_cable_pt[0]], [pulley_cable_pt[1], drum_cable_pt[1]], color='#111111', lw=2)
    
    # Velocity vector
    v_arrow_start = log_center + 0.7 * norm_dir
    v_arrow_len = v_curr * 0.7
    v_arrow_end = v_arrow_start + v_arrow_len * tang_dir
    ax_main.annotate('', xy=v_arrow_end, xytext=v_arrow_start,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
    ax_main.text(v_arrow_start[0] + 0.5 * (v_arrow_end[0] - v_arrow_start[0]) - 0.2,
                 v_arrow_start[1] + 0.5 * (v_arrow_end[1] - v_arrow_start[1]) + 0.35,
                 f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$', color='#2e7d32', fontsize=11, fontweight='bold')
    
    # Status banner
    status_title = 'Power Surge (P = 6 kW, Accelerating)' if is_surge else 'Steady State (P = 4 kW, Constant v = 1.2 m/s)'
    status_bg = '#ffebee' if is_surge else '#e8f5e9'
    status_border = '#ef5350' if is_surge else '#66bb6a'
    banner_str = f'{status_title}\n$P = {P_curr/1000:.1f}\\ \\mathrm{{kW}},\\ T = {T_curr:.0f}\\ \\mathrm{{N}},\\ a = {a_curr:.2f}\\ \\mathrm{{m/s^2}}$'
    ax_main.text(7.2, 7.5, banner_str, ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor=status_bg, edgecolor=status_border))
    
    ax_main.set_title('Sample Problem 3/14: Winch Hauling Log up an Incline', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Free-Body Diagram (FBD) ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-2.8, 2.8)
    ax_fbd.set_ylim(-3.5, 3.2)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    fbd_w, fbd_h = 2.4, 0.65
    fbd_body = patches.Rectangle((-fbd_w/2, -fbd_h/2), fbd_w, fbd_h,
                                 facecolor='#f2dfc8', edgecolor='#6d4013', lw=2.0)
    t_fbd = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(0, 0.50) + ax_fbd.transData
    fbd_body.set_transform(t_fbd)
    ax_fbd.add_patch(fbd_body)
    
    fbd_c = np.array([0, 0.50])
    
    # x-axis dashed line
    ax_fbd.plot([fbd_c[0] - 1.8 * np.cos(theta), fbd_c[0] + 2.2 * np.cos(theta)],
                [fbd_c[1] - 1.8 * np.sin(theta), fbd_c[1] + 2.2 * np.sin(theta)], color='#888888', ls='--', lw=1.2)
    ax_fbd.text(fbd_c[0] + 2.3 * np.cos(theta), fbd_c[1] + 2.3 * np.sin(theta), r'$x$', fontsize=11, fontweight='bold')
    
    # Forces
    # 1) Gravity
    ax_fbd.annotate('', xy=fbd_c, xytext=fbd_c + np.array([0, 1.4]),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(fbd_c[0], fbd_c[1] + 1.55, r'$360(9.81)\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center')
    
    # 2) Normal force N
    bot_contact = fbd_c - (fbd_h/2) * norm_dir
    n_start = bot_contact - 1.05 * norm_dir
    ax_fbd.annotate('', xy=bot_contact, xytext=n_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(n_start[0], n_start[1] - 0.18, r'$N$', color='#d32f2f', fontsize=12, fontweight='bold', ha='center', va='top')
    
    # 3) Friction force mu_k * N
    f_start = bot_contact
    f_end = bot_contact - 1.2 * tang_dir
    ax_fbd.annotate('', xy=f_end, xytext=f_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(f_end[0] - 0.15, f_end[1] - 0.15, r'$\mu_k N$', color='#d32f2f', fontsize=11, fontweight='bold', ha='right')
    
    # 4) Cable tension T
    front_face = fbd_c + (fbd_w/2) * tang_dir
    T_len = 1.2 * (T_curr / T1)
    T_end = front_face + T_len * tang_dir
    ax_fbd.annotate('', xy=T_end, xytext=front_face,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(T_end[0] + 0.1, T_end[1] + 0.1, f'$T = {T_curr:.0f}\\ \\mathrm{{N}}$',
                color='#d32f2f', fontsize=11, fontweight='bold')
    
    calc_str = (
        r"1. Steady State ($P = 4\ \mathrm{kW},\ v = 1.2\ \mathrm{m/s}$):" "\n"
        r"  $\bullet\ T = \frac{4000}{1.2} = \mathbf{3333\ \mathrm{N}}$" "\n"
        r"  $\bullet\ \sum F_x = 0 \Rightarrow \mu_k = \mathbf{0.513}$" "\n"
        r"2. Power Surge ($P = 6\ \mathrm{kW}$ Instant):" "\n"
        r"  $\bullet\ T' = \frac{6000}{1.2} = \mathbf{5000\ \mathrm{N}}$" "\n"
        r"  $\bullet\ \sum F_x = m a \Rightarrow a = \mathbf{4.63\ \mathrm{m/s^2}}$"
    )
    ax_fbd.text(0, -2.25, calc_str, fontsize=9.8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('Free-Body Diagram (FBD) & Power Analysis', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_14_log_winch_power.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
