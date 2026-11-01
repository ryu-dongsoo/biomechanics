"""
Dynamics 9th Edition Chapter 3 Part B: Work and Energy
Introductory Problem 2 - Problem 3/84 - Collar Sliding Down Inclined Rod to Compress Spring
- Pure white background (#ffffff) & Complete support and dimension illustration
- Wiley Solution Manual verified:
  * N = 2(9.81) cos 60° = 9.81 N, F = μ_k N = 3.92 N
  * (a) Speed just before hitting spring: v = 2.56 m/s
  * (b) Maximum spring compression: x = 0.0989 m = 98.9 mm
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
m = 2.0             # Collar mass (kg)
g = 9.81            # Gravity (m/s^2)
theta_deg = 60.0    # Incline angle (deg)
theta = np.radians(theta_deg)
mu_k = 0.40         # Friction coefficient
s0 = 0.5            # Free slide distance (m)
k = 1600.0          # Spring stiffness (N/m)

# Force calculations
W = m * g                          # 19.62 N
N = W * np.cos(theta)              # 9.81 N
F_f = mu_k * N                     # 3.924 N
F_down = W * np.sin(theta) - F_f   # 13.067 N

# (a) Speed before spring contact
U1_2 = F_down * s0                 # 6.5337 J
v_hit = np.sqrt(2 * U1_2 / m)      # 2.556 m/s (~2.56 m/s)
a_free = F_down / m                # 6.5337 m/s^2
t_free = v_hit / a_free            # 0.391 s

# (b) Max compression
x_max = (F_down + np.sqrt(F_down**2 + 4 * 0.5 * k * U1_2)) / k  # 0.09891 m (~98.9 mm)

# Animation sequence
n_frames = 50
t1 = np.linspace(0, t_free, 26)
s1 = 0.5 * a_free * t1**2

t2 = np.linspace(0, np.pi/2, 15)
s2 = s0 + x_max * np.sin(t2)

t3 = np.linspace(np.pi/2, 0, 10)[1:]
s3 = s0 + x_max * np.sin(t3)

s_profile = np.concatenate([s1, s2, s3])
v_profile = np.zeros_like(s_profile)
for i in range(len(s_profile)):
    s_val = s_profile[i]
    if s_val <= s0:
        v_profile[i] = np.sqrt(2 * max(0.0, F_down * s_val) / m)
    else:
        x_val = s_val - s0
        Utot = F_down * s_val - 0.5 * k * x_val**2
        v_profile[i] = np.sqrt(2 * max(0.0, Utot) / m)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

p_top = np.array([0.65, 0.95])
down_dir = np.array([-np.cos(theta), -np.sin(theta)])
norm_dir = np.array([-np.sin(theta), np.cos(theta)])
p_bot = p_top + (s0 + 0.30) * down_dir

def draw_spring_axial(ax, start, end, n_turns=8, width=0.035):
    vec = np.array(end) - np.array(start)
    length = np.linalg.norm(vec)
    if length < 1e-4:
        return
    u_vec = vec / length
    n_vec = np.array([-u_vec[1], u_vec[0]])
    
    lead = 0.05 * length
    act_len = length - 2 * lead
    xs = [0, lead]
    ys = [0, 0]
    step = act_len / n_turns
    for i in range(n_turns):
        xs.append(lead + (i + 0.25) * step)
        ys.append(width)
        xs.append(lead + (i + 0.75) * step)
        ys.append(-width)
    xs.extend([length - lead, length])
    ys.extend([0, 0])
    
    pts = np.array([np.array(start) + x * u_vec + y * n_vec for x, y in zip(xs, ys)])
    ax.plot(pts[:, 0], pts[:, 1], color='#333333', lw=1.8)

def update(frame):
    s_curr = s_profile[frame]
    v_curr = v_profile[frame]
    x_comp_curr = max(0.0, s_curr - s0)
    
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.25, 1.15)
    ax_main.set_ylim(-0.30, 1.25)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Top support
    sup_top1 = p_top + 0.08 * norm_dir
    sup_top2 = p_top - 0.08 * norm_dir
    ax_main.plot([sup_top1[0], sup_top2[0]], [sup_top1[1], sup_top2[1]], color='#333333', lw=3.0)
    ax_main.plot([sup_top1[0] - 0.04*down_dir[0], sup_top2[0] - 0.04*down_dir[0]],
                 [sup_top1[1] - 0.04*down_dir[1], sup_top2[1] - 0.04*down_dir[1]], color='#999999', lw=1.5)
    
    # Bottom support
    sup_bot1 = p_bot + 0.09 * norm_dir
    sup_bot2 = p_bot - 0.09 * norm_dir
    ax_main.plot([sup_bot1[0], sup_bot2[0]], [sup_bot1[1], sup_bot2[1]], color='#333333', lw=3.5)
    hatch_poly = patches.Polygon([sup_bot1, sup_bot2, sup_bot2 + 0.04*down_dir, sup_bot1 + 0.04*down_dir],
                                 facecolor='#d0dbe2', edgecolor='#60889f', lw=1)
    ax_main.add_patch(hatch_poly)
    
    # Horizontal reference and 60 deg arc
    ax_main.plot([p_bot[0] - 0.15, p_bot[0] + 0.35], [p_bot[1], p_bot[1]], color='#777777', ls='--', lw=1.2)
    arc = patches.Arc(p_bot, 0.45, 0.45, angle=0, theta1=0, theta2=theta_deg, color='#222222', lw=1.5)
    ax_main.add_patch(arc)
    ax_main.text(p_bot[0] + 0.26, p_bot[1] + 0.08, r'$60^\circ$', fontsize=11, fontweight='bold')
    
    # Guide rod
    rod_poly = patches.Polygon([p_top + 0.014*norm_dir, p_top - 0.014*norm_dir,
                                p_bot - 0.014*norm_dir, p_bot + 0.014*norm_dir],
                               facecolor='#b8d5e5', edgecolor='#466f85', lw=1.5)
    ax_main.add_patch(rod_poly)
    
    # Spring
    spring_top = p_top + (s0 + x_comp_curr) * down_dir
    draw_spring_axial(ax_main, spring_top, p_bot, n_turns=7, width=0.04)
    ax_main.text(p_bot[0] + 0.30, p_bot[1] + 0.16, r'$k = 1.6\ \mathrm{kN/m}$',
                 fontsize=10.5, fontweight='bold', color='#1565c0')
    
    # Friction label
    ax_main.text(p_top[0] - 0.32, p_top[1] - 0.35, r'$\mu_k = 0.40$', fontsize=11, fontweight='bold', color='#4a2800')
    
    # 0.5 m dimension line
    dim_offset = 0.14 * norm_dir
    d_start = p_top + dim_offset
    d_end = p_top + s0 * down_dir + dim_offset
    ax_main.plot([p_top[0], d_start[0]], [p_top[1], d_start[1]], color='#888888', lw=1)
    ax_main.plot([(p_top + s0*down_dir)[0], d_end[0]], [(p_top + s0*down_dir)[1], d_end[1]], color='#888888', lw=1)
    ax_main.annotate('', xy=d_end, xytext=d_start,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    dim_mid = 0.5 * (d_start + d_end) + 0.05 * norm_dir
    ax_main.text(dim_mid[0], dim_mid[1], '0.5 m', fontsize=11, fontweight='bold',
                 ha='center', va='bottom', rotation=theta_deg)
    
    # Collar
    c_w, c_h = 0.10, 0.13
    collar_pos = p_top + s_curr * down_dir
    collar = patches.Rectangle((-c_w/2, -c_h/2), c_w, c_h,
                               facecolor='#e8b88a', edgecolor='#7a4d25', lw=2.0)
    t_c = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg - 90).translate(collar_pos[0], collar_pos[1]) + ax_main.transData
    collar.set_transform(t_c)
    ax_main.add_patch(collar)
    
    ax_main.text(p_top[0] + 0.10, p_top[1] - 0.05, r'$A$', fontsize=13, fontweight='bold')
    ax_main.text(p_top[0] - 0.18, p_top[1] - 0.08, '2 kg', fontsize=11, fontweight='bold', color='#4a2800')
    
    # Velocity vector
    if v_curr > 0.05:
        v_start = collar_pos - 0.14 * norm_dir
        v_len = v_curr * 0.07
        v_end = v_start + v_len * down_dir
        ax_main.annotate('', xy=v_end, xytext=v_start,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
        ax_main.text(v_start[0] - 0.08, v_start[1] + 0.06,
                     f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$', color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right')
        
    ax_main.set_title('Problem 3/84: Collar Sliding on Inclined Rod Compressing Spring', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Parameters & Normal Force:\n"
        r"  $\bullet\ m = 2\ \mathrm{kg},\ \theta = 60^\circ,\ \mu_k = 0.40,\ k = 1600\ \mathrm{N/m}$" "\n"
        r"  $\bullet\ N = m g \cos 60^\circ = 2(9.81)(0.5) = 9.81\ \mathrm{N}$" "\n"
        r"  $\bullet\ F_f = \mu_k N = 0.40(9.81) = 3.92\ \mathrm{N}$" "\n"
        r"  $\bullet\ \sum F_{\mathrm{down}} = mg \sin 60^\circ - F_f = 13.07\ \mathrm{N}$" "\n\n"
        "(a) Speed Just Before Striking Spring (v):\n"
        r"  $T_1 + U_{1-2} = T_2 \quad (s = 0.5\ \mathrm{m})$" "\n"
        r"  $0 + (13.07)(0.5) = \frac{1}{2}(2) v^2$" "\n"
        r"  $\mathbf{v = 2.56\ \mathrm{m/s}}$" "\n\n"
        "(b) Maximum Spring Compression (x):\n"
        r"  $0 + 13.07(0.5 + x) - \frac{1}{2}(1600) x^2 = 0$" "\n"
        r"  $800 x^2 - 13.07 x - 6.53 = 0$" "\n"
        r"  $\mathbf{x = 0.0989\ \mathrm{m}\ =\ 98.9\ \mathrm{mm}}$"
    )
    ax_calc.text(0.5, 6.2, sol_box, fontsize=10.2, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'Displacement: $s = {s_curr:.3f}\\ /\\ 0.500\\ \\mathrm{{m}}$\n'
        f'Spring Compression: $x = {x_comp_curr*1000:.1f}\\ /\\ 98.9\\ \\mathrm{{mm}}$\n'
        f'Collar Speed: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$\n'
        f'State: {"Free Slide" if s_curr <= s0 else "Spring Compression"}'
    )
    ax_calc.text(0.5, 1.5, live_box, fontsize=10.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Work-Energy Analysis & Solution Verification', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_84_collar_incline_spring.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
