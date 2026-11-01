"""
Engineering Dynamics (9th Ed.) Chapter 3 Section B: Work and Energy (Section 3.7 Potential Energy & Energy Conservation)
Fundamental Practice 3 (Problem 3/113) - Pulley-Spring Suspended Cylinder System
- Pure white background (#ffffff) & exact 1:1 textbook layout
- Wiley Solution Manual Verified:
  * Kinematics: cylinder drop h = 12 mm => spring extension Delta x = 2 * h = 24 mm
  * Initial stretch: x_1 = 0.075 m, final stretch: x_2 = 0.075 + 0.024 = 0.099 m
  * Gravitational PE: Delta V_g = -45 * 9.81 * 0.012 = -5.297 J
  * Elastic PE: Delta V_e = 0.5 * 1050 * (0.099^2 - 0.075^2) = 2.192 J
  * Energy Conservation: Delta T + Delta V_g + Delta V_e = 0  =>  v = 0.371 m/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Matplotlib Font Configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Physical Parameters
m = 45.0            # Cylinder mass (kg)
g = 9.81            # Gravitational acceleration (m/s^2)
k = 1050.0          # Spring stiffness (N/m)
x1 = 0.075          # Initial spring stretch (m = 75 mm)
h_drop = 0.012      # Cylinder drop distance (m = 12 mm)
x2 = x1 + 2.0 * h_drop # Final spring stretch = 0.099 m (99 mm)

# Energetics
Delta_Vg = -m * g * h_drop                     # -5.2974 J
Delta_Ve = 0.5 * k * (x2**2 - x1**2)           # +2.1924 J
T_final = - (Delta_Vg + Delta_Ve)              # 3.1050 J
v_final = np.sqrt(2.0 * T_final / m)           # 0.371 m/s

n_frames = 50
tau_vals = np.linspace(0, 1.0, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.1, 1.1]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.06, color='#2b2b2b', lw=2.0):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-5:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.06
    active_len = max(length - 2 * lead_len, 0.04)
    pts = [start, start + lead_len * u_par]
    step = active_len / nodes
    for i in range(1, nodes):
        sgn = 1 if i % 2 == 1 else -1
        p = start + lead_len * u_par + i * step * u_par + sgn * width * u_perp
        pts.append(p)
    pts.append(end - lead_len * u_par)
    pts.append(end)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle='round')

def update(frame):
    tau = tau_vals[frame]
    h_curr = h_drop * (tau**1.2)
    s_curr_disp = h_curr * 18.0
    sp_ext_disp = 2.0 * s_curr_disp
    
    x_curr = x1 + 2.0 * h_curr
    Vg_curr = -m * g * h_curr
    Ve_curr = 0.5 * k * (x_curr**2 - x1**2)
    T_curr = max(- (Vg_curr + Ve_curr), 0.0)
    v_curr = np.sqrt(2.0 * T_curr / m)
    
    # ---------------- 1. Main System View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.6, 0.9)
    ax_main.set_ylim(-1.8, 0.5)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # Ceiling
    ax_main.plot([-0.4, 0.4], [0.35, 0.35], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.38, 0.34, 10):
        ax_main.plot([hx, hx + 0.04], [0.35, 0.42], color='#666666', lw=1.2)
    
    # Left rope anchor: x = -0.15
    ax_main.plot([-0.15, -0.15], [0.35, 0.28], color='#2b2b2b', lw=2.0)
    ax_main.plot(-0.15, 0.28, 'o', color='#2b2b2b', markersize=4)
    
    # Spring anchor: x = 0.08
    ax_main.plot([0.08, 0.08], [0.35, 0.25], color='#2b2b2b', lw=2.0)
    ax_main.plot(0.08, 0.25, 'o', color='#2b2b2b', markersize=4)
    
    # Spring
    y_sp_bottom = -0.55 - sp_ext_disp
    draw_spring(ax_main, (0.08, 0.25), (0.08, y_sp_bottom), nodes=14, width=0.065, color='#2b2b2b', lw=2.0)
    ax_main.plot(0.08, y_sp_bottom, 'o', color='#2b2b2b', markersize=4)
    ax_main.text(0.18, -0.15 - sp_ext_disp * 0.5, r'$k = 1050\ \mathrm{N/m}$', fontsize=10.5, fontweight='bold', color='#1a5276')
    
    # Pulley
    r_p = 0.115
    xc_p = (-0.15 + 0.08) / 2.0
    yc_p = -0.75 - s_curr_disp
    
    ax_main.plot([-0.15, -0.15], [0.28, yc_p], color='#2b2b2b', lw=2.0, zorder=3)
    rope_arc = patches.Arc((xc_p, yc_p), 2*r_p, 2*r_p, angle=180, theta1=0, theta2=180, color='#2b2b2b', lw=2.0, zorder=3)
    ax_main.add_patch(rope_arc)
    ax_main.plot([0.08, 0.08], [yc_p, y_sp_bottom], color='#2b2b2b', lw=2.0, zorder=3)
    
    pulley = patches.Circle((xc_p, yc_p), r_p, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.8, zorder=4)
    ax_main.add_patch(pulley)
    ax_main.plot(xc_p, yc_p, 'o', color='#2b2b2b', markersize=4, zorder=5)
    
    # Link
    y_cyl_top = yc_p - r_p - 0.10
    ax_main.plot([xc_p, xc_p], [yc_p, y_cyl_top], color='#2b2b2b', lw=2.5, zorder=4)
    
    # 45 kg Cylinder
    cyl_w, cyl_h = 0.38, 0.42
    cyl = patches.Rectangle((xc_p - cyl_w/2, y_cyl_top - cyl_h), cyl_w, cyl_h,
                            facecolor='#b87333', edgecolor='#5a2d0c', lw=1.8, zorder=5)
    ax_main.add_patch(cyl)
    ax_main.text(xc_p, y_cyl_top - cyl_h/2, r'$45\ \mathrm{kg}$', color='#ffffff',
                 ha='center', va='center', fontsize=11, fontweight='bold', zorder=6)
    
    # Velocity Arrow
    if v_curr > 0.05:
        v_scale = 0.25 * (v_curr / v_final)
        ax_main.annotate('', xy=(xc_p, y_cyl_top - cyl_h - v_scale), xytext=(xc_p, y_cyl_top - cyl_h),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(xc_p + 0.10, y_cyl_top - cyl_h - v_scale/2, f'$v$', color='#27ae60', fontsize=11, fontweight='bold')
    
    ax_main.plot([-0.4, 0.3], [-0.75 - r_p - 0.10, -0.75 - r_p - 0.10], color='#999999', ls=':', lw=1.0)
    ax_main.text(-0.45, -0.85, r'$h = 12\ \mathrm{mm}$', fontsize=9.5, color='#444444')
    
    ax_main.set_title('Problem 3/113: Pulley-Spring Suspended System', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. Energy Monitor & Theory Card ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, T_curr + Ve_curr + Vg_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$\Delta V_e$', r'$\Delta V_g$', r'$\Delta E_{\mathrm{tot}}$']
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 6.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.2f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"[Work-Energy Analysis (Problem 3/113)]\n"
        f"• System Work-Energy: $T_1 + V_1 + U'_{{1-2}} = T_2 + V_2$\n"
        f"  $\\frac{{1}}{{2}}mv_1^2 + \\frac{{1}}{{2}}kx_1^2 + 0 = \\frac{{1}}{{2}}mv^2 + \\frac{{1}}{{2}}kx_2^2 - mgh$\n"
        f"• Pulley Kinematics: Spring extension is twice cylinder drop!\n"
        f"  $h = 12\\ \\mathrm{{mm}} = 0.012\\ \\mathrm{{m}}$\n"
        f"  $x_2 = 0.075 + 2(0.012) = 0.099\\ \\mathrm{{m}}$\n"
        f"• Numerical Substitution:\n"
        f"  $\\frac{{1}}{{2}}(1050)(0.075)^2 = \\frac{{1}}{{2}}(45)v^2 + \\frac{{1}}{{2}}(1050)(0.099)^2$\n"
        f"                                        $- 45(9.81)(0.012)$\n"
        f"  $2.953 = 22.5 v^2 + 5.146 - 5.297$\n"
        f"  $22.5 v^2 = 3.105\\ \\rightarrow\\ v = \\mathbf{{0.371\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• Drop: $h = {h_curr*1000:.1f}\\ \\mathrm{{mm}},\\quad$ Velocity: $v = {v_curr:.3f}\\ \\mathrm{{m/s}}$"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.0, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('Mechanical Energy Conservation & Validation', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_113_pulley_cylinder_spring.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
