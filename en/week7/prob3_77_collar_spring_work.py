"""
Dynamics 9th Edition Chapter 3 Part B: Work and Energy
Introductory Problem 1 - Problem 3/77 - Work of Weight and Spring on Slider in Vertical Slot
- Pure white background (#ffffff) & Extended vertical slot and complete bracket illustration
- Wiley Solution Manual verified:
  * (a) Work done by weight: U_g = mgh = 0.2(9.81)(0.8) = +1.570 J
  * (b) Work done by spring: U_s = 1/2*k*(x_A^2 - x_B^2) = -4.20 J
  * R = 0.8 m, k = 180 N/m, L_0 = 0.6 m
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
m = 0.2             # Slider mass (kg)
g = 9.81            # Gravity (m/s^2)
R = 0.8             # Track radius (m)
k = 180.0           # Spring stiffness (N/m)
L0 = 0.6            # Undeformed spring length (m)

# Point A: (R, 0) = (0.8, 0)
xA, yA = R, 0.0
LA = R
xA_stretch = LA - L0  # 0.2 m

# Point B: (-R/2, -R) = (-0.4, -0.8)
xB, yB = -R / 2.0, -R
LB = np.sqrt(xB**2 + yB**2)  # sqrt(0.80) ~ 0.8944 m
xB_stretch = LB - L0         # ~0.2944 m

# Work calculations
U_g_final = m * g * R                                # +1.570 J
U_s_final = 0.5 * k * (xA_stretch**2 - xB_stretch**2) # -4.202 J (~ -4.20 J)
U_tot_final = U_g_final + U_s_final                  # -2.632 J

# Trajectory
phi_arc = np.linspace(0, -np.pi / 2, 35)
x_arc = R * np.cos(phi_arc)
y_arc = R * np.sin(phi_arc)

x_line = np.linspace(0, xB, 16)[1:]
y_line = np.full_like(x_line, -R)

traj_x = np.concatenate([x_arc, x_line])
traj_y = np.concatenate([y_arc, y_line])
n_frames = len(traj_x)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_spring(ax, start, end, n_turns=11, width=0.038):
    vec = np.array(end) - np.array(start)
    length = np.linalg.norm(vec)
    if length < 1e-4:
        return
    unit_vec = vec / length
    norm_vec = np.array([-unit_vec[1], unit_vec[0]])
    
    lead = 0.12 * length
    active_len = length - 2 * lead
    xs = [0, lead]
    ys = [0, 0]
    turn_step = active_len / n_turns
    for i in range(n_turns):
        xs.append(lead + (i + 0.25) * turn_step)
        ys.append(width)
        xs.append(lead + (i + 0.75) * turn_step)
        ys.append(-width)
    xs.extend([length - lead, length])
    ys.extend([0, 0])
    
    pts = np.array([np.array(start) + x * unit_vec + y * norm_vec for x, y in zip(xs, ys)])
    ax.plot(pts[:, 0], pts[:, 1], color='#333333', lw=1.8)

def update(frame):
    cx = traj_x[frame]
    cy = traj_y[frame]
    
    L_curr = np.sqrt(cx**2 + cy**2)
    x_stretch_curr = L_curr - L0
    
    h_drop = -cy
    Ug_curr = m * g * h_drop
    Us_curr = 0.5 * k * (xA_stretch**2 - x_stretch_curr**2)
    Utot_curr = Ug_curr + Us_curr
    
    # ---------------- 1. Main View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.75, 1.15)
    ax_main.set_ylim(-1.25, 0.40)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Centerline
    ax_main.plot(traj_x, traj_y, color='#f57c00', ls='--', lw=1.5)
    
    # Groove walls
    w_slot = 0.08
    phi_dense = np.linspace(0, -np.pi/2, 60)
    out_arc_x = (R + w_slot/2) * np.cos(phi_dense)
    out_arc_y = (R + w_slot/2) * np.sin(phi_dense)
    in_arc_x = (R - w_slot/2) * np.cos(phi_dense)
    in_arc_y = (R - w_slot/2) * np.sin(phi_dense)
    
    y_top_ext = 0.22
    ax_main.plot(np.concatenate([[R + w_slot/2, R + w_slot/2], out_arc_x, [0, xB - 0.18]]),
                 np.concatenate([[y_top_ext, 0], out_arc_y, [-R - w_slot/2, -R - w_slot/2]]),
                 color='#333333', lw=2.0)
    ax_main.plot(np.concatenate([[R - w_slot/2, R - w_slot/2], in_arc_x, [0, xB - 0.18]]),
                 np.concatenate([[y_top_ext, 0], in_arc_y, [-R + w_slot/2, -R + w_slot/2]]),
                 color='#333333', lw=2.0)
    
    # Pin O bracket
    pin_sup = patches.Polygon([[-0.07, 0.08], [0.07, 0.08], [0, 0]], facecolor='#cfd8dc', edgecolor='#37474f', lw=1.2)
    ax_main.add_patch(pin_sup)
    ax_main.plot([-0.12, 0.12], [0.08, 0.08], color='#333333', lw=2.2)
    ax_main.plot(0, 0, 'ko', markersize=3.5)
    ax_main.text(-0.06, 0.02, r'$O$', fontsize=13, fontweight='bold')
    
    # Vertical line and R
    ax_main.plot([0, 0], [0, -R], color='#888888', ls='-.', lw=1.2)
    ax_main.text(0.04, -0.4, r'$R$', fontsize=11, fontweight='bold')
    
    # Dimension R/2
    ax_main.plot([xB, xB], [-R - 0.08, -R - 0.22], color='#888888', lw=1)
    ax_main.plot([0, 0], [-R - 0.08, -R - 0.22], color='#888888', lw=1)
    ax_main.annotate('', xy=(0, -R - 0.18), xytext=(xB, -R - 0.18),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(xB / 2, -R - 0.22, r'$\frac{R}{2}$', fontsize=12, fontweight='bold', ha='center', va='top')
    
    # Position A, B markers
    ax_main.plot(xA, yA, 'ko', markersize=3.5)
    ax_main.text(xA + 0.08, yA, r'$A$', fontsize=13, fontweight='bold', va='center')
    ax_main.plot(xB, yB, 'ko', markersize=3.5)
    ax_main.text(xB - 0.08, yB - 0.08, r'$B$', fontsize=13, fontweight='bold', ha='right')
    
    # Spring
    draw_spring(ax_main, (0, 0), (cx, cy), n_turns=10, width=0.035)
    
    # Slider
    sl_w, sl_h = 0.075, 0.07
    slider = patches.Rectangle((cx - sl_w/2, cy - sl_h/2), sl_w, sl_h,
                               facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    ax_main.add_patch(slider)
    ax_main.plot(cx, cy, 'ko', markersize=2.5)
    
    # Radius dimension
    ang_dim = np.radians(-42)
    p_dim = np.array([R * np.cos(ang_dim), R * np.sin(ang_dim)])
    ax_main.annotate('', xy=p_dim, xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#555555', lw=1.2))
    ax_main.text(p_dim[0]*0.5 + 0.04, p_dim[1]*0.5 + 0.04, r'$R = 0.8\ \mathrm{m}$', fontsize=11, fontweight='bold')
    
    ax_main.set_title('Problem 3/77: Slider and Spring in Vertical Curved Slot', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Given Parameters:\n"
        r"  $\bullet\ m = 0.2\ \mathrm{kg},\ R = 0.8\ \mathrm{m},\ k = 180\ \mathrm{N/m}$" "\n"
        r"  $\bullet\ $ Free spring length $L_0 = 0.6\ \mathrm{m}$" "\n\n"
        "(a) Work Done by Weight on Slider (U_g):\n"
        r"  $U_g = m g h = 0.2(9.81)(0.8)$" "\n"
        r"  $\mathbf{U_g = +1.570\ \mathrm{J}}$" "\n\n"
        "(b) Work Done by Spring on Slider (U_s):\n"
        r"  $\bullet\ x_A = L_A - L_0 = 0.8 - 0.6 = 0.2\ \mathrm{m}$" "\n"
        r"  $\bullet\ L_B = \sqrt{0.8^2 + 0.4^2} = \sqrt{0.80} \approx 0.8944\ \mathrm{m}$" "\n"
        r"  $\bullet\ x_B = 0.8944 - 0.6 = 0.2944\ \mathrm{m}$" "\n"
        r"  $U_s = \frac{1}{2} k (x_A^2 - x_B^2)$" "\n"
        r"  $U_s = \frac{1}{2}(180)[0.2^2 - (\sqrt{0.80}-0.6)^2]$" "\n"
        r"  $\mathbf{U_s = -4.20\ \mathrm{J}}$"
    )
    ax_calc.text(0.5, 6.2, sol_box, fontsize=10.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'Vertical Drop: $h = {h_drop:.3f}\\ \\mathrm{{m}}$\n'
        f'Spring Length: $L = {L_curr:.3f}\\ \\mathrm{{m}}$\n'
        f'Spring Stretch: $x = {x_stretch_curr:+.3f}\\ \\mathrm{{m}}$\n'
        f'Weight Work: $U_g = {Ug_curr:+.3f}\\ \\mathrm{{J}}$\n'
        f'Spring Work: $U_s = {Us_curr:+.3f}\\ \\mathrm{{J}}$\n'
        f'Net Cumulative Work: $U = {Utot_curr:+.3f}\\ \\mathrm{{J}}$'
    )
    ax_calc.text(0.5, 1.6, live_box, fontsize=10.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Quantitative Work-Energy Analysis', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_77_collar_spring_work.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
