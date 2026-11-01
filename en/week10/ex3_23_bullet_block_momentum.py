"""
Sample Problem 3.23: 2D Bullet-Block Impact and Conservation of Linear Momentum
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Bullet mass m1 = 50 g = 0.050 kg, velocity v1 = 600 m/s (+y direction)
- Wooden block mass m2 = 4.0 kg, velocity v2 = 12 m/s (30 deg above horizontal x-axis)
- Plastic collision on smooth horizontal surface (bullet embeds in block)
- Combined mass M = m1 + m2 = 4.050 kg

Analytical Result:
- Combined velocity magnitude: v = 16.83 m/s
- Direction angle: theta = 52.4 deg (relative to +x axis)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m1 = 0.050          # kg
v1 = 600.0          # m/s (+y)
m2 = 4.000          # kg
v2 = 12.0           # m/s (30 deg)
ang2_deg = 30.0
ang2_rad = np.radians(ang2_deg)

# Momentum vector components
G1_x = 0.0
G1_y = m1 * v1                     # 30.00 kg*m/s
G2_x = m2 * v2 * np.cos(ang2_rad)  # 41.57 kg*m/s
G2_y = m2 * v2 * np.sin(ang2_rad)  # 24.00 kg*m/s

G_tot_x = G1_x + G2_x              # 41.57 kg*m/s
G_tot_y = G1_y + G2_y              # 54.00 kg*m/s
G_mag = np.hypot(G_tot_x, G_tot_y) # 68.15 kg*m/s

M_tot = m1 + m2                    # 4.050 kg
v_final = G_mag / M_tot            # 16.83 m/s
theta_rad = np.arctan2(G_tot_y, G_tot_x)
theta_deg = np.degrees(theta_rad)        # 52.41 deg -> 52.4 deg

T_init = 0.5 * m1 * (v1**2) + 0.5 * m2 * (v2**2) # 9288 J
T_final = 0.5 * M_tot * (v_final**2)             # 573.3 J
delta_T = T_init - T_final                       # 8714.7 J

n_frames = 60
t_arr = np.linspace(-0.6, 0.6, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def update(frame):
    t = t_arr[frame]
    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] 2D Collision Geometry & Trajectories
    # ==========================================
    ax1.set_xlim(-0.8, 0.8)
    ax1.set_ylim(-0.6, 0.8)
    ax1.set_aspect('equal')
    ax1.set_title("Sample Problem 3.23: 2D Particle Impact Kinematics", fontsize=12.5, fontweight='bold', pad=10)

    ax1.axhline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.axvline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.text(0.72, -0.07, "x", fontsize=11, fontweight='bold', color='#495057')
    ax1.text(0.04, 0.72, "y", fontsize=11, fontweight='bold', color='#495057')

    ax1.plot([0, 0], [-0.6, 0], 'r--', lw=1.2, alpha=0.5)
    ax1.plot([-0.6 * np.cos(ang2_rad), 0], [-0.6 * np.sin(ang2_rad), 0], 'b--', lw=1.2, alpha=0.5)
    ax1.plot([0, 0.7 * np.cos(theta_rad)], [0, 0.7 * np.sin(theta_rad)], 'g--', lw=1.5, alpha=0.6)

    arc_30 = np.linspace(0, ang2_rad, 20)
    ax1.plot(0.25 * np.cos(arc_30), 0.25 * np.sin(arc_30), color='#1864ab', lw=1.2)
    ax1.text(0.28, 0.05, "30 deg", color='#1864ab', fontsize=9.5, fontweight='bold')

    arc_52 = np.linspace(0, theta_rad, 25)
    ax1.plot(0.40 * np.cos(arc_52), 0.40 * np.sin(arc_52), color='#2b8a3e', lw=1.5)
    ax1.text(0.42 * np.cos(theta_rad/2), 0.42 * np.sin(theta_rad/2), f"theta = {theta_deg:.1f} deg",
             color='#2b8a3e', fontsize=10, fontweight='bold')

    scale_pos = 0.8
    if t < 0:
        b_x = 0.0
        b_y = t * scale_pos
        bk_x = t * scale_pos * np.cos(ang2_rad)
        bk_y = t * scale_pos * np.sin(ang2_rad)

        rect = patches.Rectangle((bk_x - 0.08, bk_y - 0.06), 0.16, 0.12, angle=30,
                                 facecolor='#ffd8a8', edgecolor='#e8590c', lw=2, zorder=3)
        ax1.add_patch(rect)
        ax1.text(bk_x - 0.05, bk_y + 0.08, "Block (4 kg)", color='#e8590c', fontsize=9, fontweight='bold')

        bullet = patches.Circle((b_x, b_y), 0.025, facecolor='#ff6b6b', edgecolor='#c92a2a', lw=1.5, zorder=4)
        ax1.add_patch(bullet)
        ax1.text(b_x + 0.04, b_y, "Bullet\n(50 g)", color='#c92a2a', fontsize=8.5, fontweight='bold')

        ax1.annotate('', xy=(b_x, b_y + 0.12), xytext=(b_x, b_y),
                     arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=2.2, mutation_scale=12))
        ax1.annotate('', xy=(bk_x + 0.12 * np.cos(ang2_rad), bk_y + 0.12 * np.sin(ang2_rad)), xytext=(bk_x, bk_y),
                     arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.2, mutation_scale=12))

        status_text = "Approaching Impact Point"
        status_color = '#1864ab'
    elif abs(t) <= 0.02:
        spark = patches.Circle((0, 0), 0.08, facecolor='#ffe066', edgecolor='#f59f00', lw=2, alpha=0.8, zorder=5)
        ax1.add_patch(spark)
        status_text = "Impact Instant (Sigma F_ext = 0)"
        status_color = '#e03131'
    else:
        c_x = t * scale_pos * np.cos(theta_rad)
        c_y = t * scale_pos * np.sin(theta_rad)

        rect = patches.Rectangle((c_x - 0.08, c_y - 0.06), 0.16, 0.12, angle=np.degrees(theta_rad),
                                 facecolor='#b2f2bb', edgecolor='#2b8a3e', lw=2, zorder=3)
        ax1.add_patch(rect)
        bullet_embedded = patches.Circle((c_x, c_y), 0.02, facecolor='#ff6b6b', edgecolor='#c92a2a', lw=1, zorder=4)
        ax1.add_patch(bullet_embedded)

        v_arrow_len = 0.22
        ax1.annotate('', xy=(c_x + v_arrow_len * np.cos(theta_rad), c_y + v_arrow_len * np.sin(theta_rad)), xytext=(c_x, c_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.0, mutation_scale=15))
        ax1.text(c_x + 0.05, c_y + 0.15, f"v = {v_final:.2f} m/s\n(theta = {theta_deg:.1f} deg)",
                 color='#2b8a3e', fontweight='bold', fontsize=10)

        status_text = f"Combined Motion (v = {v_final:.2f} m/s, theta = {theta_deg:.1f} deg)"
        status_color = '#2b8a3e'

    ax1.text(0.0, -0.52, f"Status: {status_text}", fontsize=11, fontweight='bold',
             color=status_color, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=status_color, lw=1.2))

    # ==========================================
    # [Right Panel] Momentum Vector Polygon & Solution
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("Linear Momentum Conservation & Textbook Verification", fontsize=12.5, fontweight='bold', pad=10)

    rect_box = patches.Rectangle((-0.12, 0.45), 1.32, 0.55, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ Vector Addition: G1 + G2 = G_total ]", fontsize=10.5, fontweight='bold', color='#212529')

    v_ox, v_oy = 0.10, 0.55
    v_scale = 0.009

    ax2.annotate('', xy=(v_ox + G2_x * v_scale, v_oy + G2_y * v_scale), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.5, mutation_scale=14))
    ax2.text(v_ox + G2_x * v_scale * 0.4, v_oy + G2_y * v_scale * 0.4 - 0.05,
             f"G2 = m2 v2\n({G2_x:.1f}i + {G2_y:.1f}j)", color='#1864ab', fontsize=9, fontweight='bold')

    p_mid_x = v_ox + G2_x * v_scale
    p_mid_y = v_oy + G2_y * v_scale
    ax2.annotate('', xy=(p_mid_x, p_mid_y + G1_y * v_scale), xytext=(p_mid_x, p_mid_y),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=2.5, mutation_scale=14))
    ax2.text(p_mid_x + 0.03, p_mid_y + G1_y * v_scale * 0.5,
             f"G1 = m1 v1\n({G1_y:.1f}j)", color='#c92a2a', fontsize=9, fontweight='bold')

    p_final_x = p_mid_x
    p_final_y = p_mid_y + G1_y * v_scale
    ax2.annotate('', xy=(p_final_x, p_final_y), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.2, mutation_scale=16))
    ax2.text(v_ox + 0.12, v_oy + 0.25, f"G_tot = (m1+m2)v\n= {G_mag:.1f} kg m/s\n(theta = {theta_deg:.1f} deg)",
             color='#2b8a3e', fontsize=9.5, fontweight='bold')

    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.50, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.34, "Momentum Component Analysis (F_ext = 0):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.27, f"   x-axis: 4(12 cos 30 deg) = (4.050) vx  ==>  vx = {G_tot_x/M_tot:.2f} m/s", fontsize=9.2, color='#212529')
    ax2.text(-0.08, 0.20, f"   y-axis: 0.050(600) + 4(12 sin 30 deg) = (4.050) vy  ==>  vy = {G_tot_y/M_tot:.2f} m/s", fontsize=9.2, color='#212529')

    ax2.text(-0.08, 0.11, "Kinetic Energy Dissipation:", fontsize=10, fontweight='bold', color='#495057')
    ax2.text(-0.08, 0.05, f"   T_initial = 9288 J  ==>  T_final = 573 J  (Loss: {delta_T/T_init*100:.1f}%)", fontsize=9.2, color='#495057')

    ax2.text(-0.08, -0.04, "Theoretical Verification (100% Textbook Parity):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.08, f"   v = sqrt(vx^2 + vy^2) = {v_final:.2f} m/s,   theta = tan^-1(vy/vx) = {theta_deg:.1f} deg",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_23_bullet_block_momentum.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
