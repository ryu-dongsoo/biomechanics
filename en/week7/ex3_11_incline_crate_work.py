"""
Dynamics 9th Edition Chapter 3 Part B: Work and Energy
Sample Problem 3/11 - Work-Energy Analysis of a Crate Sliding Down an Incline
- Pure white background (#ffffff) & Textbook illustration style
- Wiley Solution Manual verified:
  * U_g = +1269.5 J, U_f = -1421.4 J, U_total = -151.9 J
  * v_1 = 4.00 m/s -> v_2 = 3.15 m/s
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
m = 50.0            # Mass (kg)
g = 9.81            # Gravity (m/s^2)
theta_deg = 15.0    # Incline angle (deg)
theta = np.radians(theta_deg)
mu_k = 0.30         # Kinetic friction coefficient
v1 = 4.0            # Initial speed (m/s)
s_total = 10.0      # Displacement (m)

# Force calculations
W = m * g                          # 490.5 N
N = W * np.cos(theta)              # Normal force R = 473.8 N
F_f = mu_k * N                     # Friction force = 142.1 N

# Acceleration (down incline)
a = g * np.sin(theta) - mu_k * g * np.cos(theta)  # Negative (deceleration)

# Work and Energy calculations
U_g = W * np.sin(theta) * s_total  # +1269.5 J
U_f = -F_f * s_total               # -1421.4 J
U_total = U_g + U_f                # -151.9 J
T1 = 0.5 * m * v1**2               # 400.0 J
T2 = T1 + U_total                  # 248.1 J
v2 = np.sqrt(2 * T2 / m)           # 3.15 m/s

# Motion duration
t_total = (v2 - v1) / a            # ~2.79 s

# Animation setup
n_frames = 50
t_vals = np.linspace(0, t_total, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

# Unit vectors (down slope, normal upward)
tang_vec = np.array([-np.cos(theta), -np.sin(theta)])
norm_vec = np.array([-np.sin(theta), np.cos(theta)])

# Ramp geometry
x_B, y_B = 2.2, 1.8
x_A = x_B + s_total * np.cos(theta)
y_A = y_B + s_total * np.sin(theta)

box_w, box_h = 1.3, 0.75

def update(frame):
    t = t_vals[frame]
    s_curr = v1 * t + 0.5 * a * t**2
    v_curr = v1 + a * t
    T_curr = 0.5 * m * v_curr**2
    Ug_curr = W * np.sin(theta) * s_curr
    Uf_curr = -F_f * s_curr
    Utot_curr = Ug_curr + Uf_curr
    
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 14.5)
    ax_main.set_ylim(0.2, 6.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Ramp line and hatching
    ax_main.plot([x_B - 1.5, x_B, x_A + 1.2], [y_B, y_B, y_A + 1.2 * np.sin(theta)], color='#2b2b2b', lw=2.2)
    ramp_poly = np.array([
        [x_B - 1.5, y_B],
        [x_B, y_B],
        [x_A + 1.2, y_A + 1.2 * np.sin(theta)],
        [x_A + 1.2, 0.6],
        [x_B - 1.5, 0.6]
    ])
    ax_main.fill(ramp_poly[:, 0], ramp_poly[:, 1], color='#f4ede4', edgecolor='none')
    ax_main.plot([x_B - 1.5, x_A + 1.2], [0.6, 0.6], color='#b0a89f', lw=1.0)
    
    # Horizontal line and 15 deg arc
    ax_main.plot([x_B - 0.6, x_B + 3.2], [y_B, y_B], color='#777777', ls='--', lw=1.2)
    arc = patches.Arc((x_B, y_B), 3.2, 3.2, angle=0, theta1=0, theta2=theta_deg, color='#222222', lw=1.5)
    ax_main.add_patch(arc)
    ax_main.text(x_B + 2.0, y_B + 0.25, r'$15^\circ$', fontsize=12, fontweight='bold', color='#222222')
    
    # Dimension line: 10 m
    offset = 1.4
    pA_dim = np.array([x_A, y_A]) + offset * norm_vec
    pB_dim = np.array([x_B, y_B]) + offset * norm_vec
    ax_main.plot([x_A, pA_dim[0]], [y_A, pA_dim[1]], color='#888888', lw=1)
    ax_main.plot([x_B, pB_dim[0]], [y_B, pB_dim[1]], color='#888888', lw=1)
    ax_main.annotate('', xy=pB_dim, xytext=pA_dim,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.3))
    dim_center = 0.5 * (pA_dim + pB_dim) + 0.22 * norm_vec
    ax_main.text(dim_center[0], dim_center[1], '10 m', fontsize=11, ha='center', va='bottom',
                 rotation=theta_deg, fontweight='bold')
    
    # Position A, B markers
    ax_main.plot(x_A, y_A, 'ko', markersize=4)
    ax_main.text(x_A + 0.1, y_A + 0.35, r'$A$', fontsize=13, fontweight='bold')
    ax_main.plot(x_B, y_B, 'ko', markersize=4)
    ax_main.text(x_B - 0.35, y_B + 0.35, r'$B$', fontsize=13, fontweight='bold')
    
    # Crate position
    crate_base = np.array([x_A, y_A]) + s_curr * tang_vec
    crate_center = crate_base + (box_h / 2.0) * norm_vec
    
    # Crate body
    crate_poly = patches.Rectangle((-box_w/2, -box_h/2), box_w, box_h,
                                   facecolor='#bdd8ea', edgecolor='#1d4564', lw=2.0)
    trans = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(crate_center[0], crate_center[1]) + ax_main.transData
    crate_poly.set_transform(trans)
    ax_main.add_patch(crate_poly)
    
    # Text on crate
    ax_main.text(crate_center[0], crate_center[1], '50 kg', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#1d4564')
    
    # Velocity vector
    v_start = crate_center + (box_w/2 + 0.1) * tang_vec - 0.15 * norm_vec
    v_len = v_curr * 0.35
    v_end = v_start + v_len * tang_vec
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
    ax_main.text(v_start[0] + 0.5 * (v_end[0] - v_start[0]) - 0.2, v_start[1] + 0.32,
                 f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$', color='#2e7d32', fontsize=11, fontweight='bold', ha='center')
    
    ax_main.set_title('Sample Problem 3/11: Crate Sliding Down an Incline', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Free Body Diagram (FBD) ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-2.8, 2.8)
    ax_fbd.set_ylim(-3.2, 3.2)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    # FBD crate
    fbd_w, fbd_h = 1.6, 0.85
    fbd_crate = patches.Rectangle((-fbd_w/2, -fbd_h/2), fbd_w, fbd_h,
                                  facecolor='#bdd8ea', edgecolor='#1d4564', lw=2.0)
    t_fbd = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(0, 0.35) + ax_fbd.transData
    fbd_crate.set_transform(t_fbd)
    ax_fbd.add_patch(fbd_crate)
    
    fbd_center = np.array([0, 0.35])
    
    # FBD vectors
    # 1) Gravity
    ax_fbd.annotate('', xy=fbd_center, xytext=fbd_center + np.array([0, 1.4]),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(fbd_center[0], fbd_center[1] + 1.55, r'$50(9.81)\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center')
    
    # 2) Normal force R
    norm_dir = np.array([-np.sin(theta), np.cos(theta)])
    contact_pt = fbd_center - (fbd_h/2) * norm_dir
    r_start = contact_pt - 1.1 * norm_dir
    ax_fbd.annotate('', xy=contact_pt, xytext=r_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(r_start[0], r_start[1] - 0.22, r'$R = 474\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center', va='top')
    
    # 3) Friction force mu_k * R
    up_slope = np.array([np.cos(theta), np.sin(theta)])
    friction_end = contact_pt
    friction_start = friction_end - 1.2 * up_slope
    ax_fbd.annotate('', xy=friction_end, xytext=friction_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(friction_start[0] - 0.15, friction_start[1] - 0.1,
                r'$\mu_k R = 142.1\ \mathrm{N}$', color='#d32f2f', fontsize=10.5, fontweight='bold', ha='right')
    
    # Summary info box
    info_text = (
        f'Displacement: $s = {s_curr:.2f}\\ /\\ 10.00\\ \\mathrm{{m}}$\n'
        f'Gravity Work: $U_g = {Ug_curr:+.1f}\\ \\mathrm{{J}}$   Friction Work: $U_f = {Uf_curr:+.1f}\\ \\mathrm{{J}}$\n'
        f'Total Work: $U_{{1-2}} = {Utot_curr:+.1f}\\ \\mathrm{{J}}$   Kinetic Energy: $T = {T_curr:.1f}\\ \\mathrm{{J}}$\n'
        f'Speed: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (Final: $3.15\\ \\mathrm{{m/s}}$)'
    )
    ax_fbd.text(0, -2.35, info_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('Free-Body Diagram (FBD) & Work-Energy', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_11_incline_crate_work.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
