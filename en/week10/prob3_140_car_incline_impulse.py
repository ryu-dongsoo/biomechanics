"""
Practice 1 (Problem 3/140): 1500 kg Car Accelerating up a 10% Incline
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Car mass m = 1500 kg
- Grade: 10% (tan θ = 0.10 ==> θ = 5.71°)
- Initial speed v1 = 30 km/h = 8.333 m/s
- Final speed v2 = 60 km/h = 16.667 m/s
- Acceleration duration Δt = 8 s
- Gravitational acceleration g = 9.81 m/s^2

Analytical Result:
- Constant tractive force F = 3030 N (3.03 kN)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

m = 1500.0         # kg
grade = 0.10       # 10%
theta_rad = np.arctan(grade) # 5.71 deg
theta_deg = np.degrees(theta_rad)
g = 9.81           # m/s^2
v1 = 30.0 / 3.6    # 8.333 m/s
v2 = 60.0 / 3.6    # 16.667 m/s
dt = 8.0           # s

W = m * g          # 14715 N
W_x = W * np.sin(theta_rad) # 1464.2 N

a_acc = (v2 - v1) / dt     # 1.0417 m/s^2
F_tractive = W_x + m * a_acc # 3026.7 N -> 3030 N

n_frames = 60
t_arr = np.linspace(0.0, dt, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def update(frame):
    t_curr = t_arr[frame]
    v_curr = v1 + a_acc * t_curr
    v_kmh = v_curr * 3.6
    s_curr = v1 * t_curr + 0.5 * a_acc * (t_curr**2)

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] Textbook 1:1 Visualization
    # ==========================================
    ax1.set_xlim(-1.0, 7.5)
    ax1.set_ylim(-1.0, 3.2)
    ax1.set_aspect('equal')
    ax1.set_title("Problem 3/140: Acceleration on 10% Grade (Textbook 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # Incline road
    road_len = 8.5
    rx = np.array([-0.8, road_len * np.cos(theta_rad)])
    ry = np.array([-0.8 * np.tan(theta_rad), road_len * np.sin(theta_rad)])
    ax1.plot(rx, ry, color='#343a40', lw=3.0)

    ax1.fill_between([-0.8, road_len * np.cos(theta_rad), road_len * np.cos(theta_rad), -0.8],
                     [-0.8 * np.tan(theta_rad), road_len * np.sin(theta_rad), -0.8, -0.8],
                     color='#f8f9fa', alpha=0.5)

    # 10:1 Slope indicator triangle
    tri_x0, tri_y0 = 2.0, -0.45
    tri_len = 2.5
    tri_h = tri_len * 0.10
    ax1.plot([tri_x0, tri_x0 + tri_len, tri_x0 + tri_len, tri_x0],
             [tri_y0, tri_y0, tri_y0 + tri_h, tri_y0], color='#e03131', lw=2.0)
    ax1.text(tri_x0 + tri_len * 0.5, tri_y0 - 0.14, "10", color='#212529', fontsize=11, ha='center', fontweight='bold')
    ax1.text(tri_x0 + tri_len + 0.18, tri_y0 + tri_h * 0.5, "1", color='#212529', fontsize=11, va='center', fontweight='bold')

    # Car position
    pos_vis = 0.6 + (s_curr / (v1*dt + 0.5*a_acc*dt**2)) * 4.2
    car_x = pos_vis * np.cos(theta_rad)
    car_y = pos_vis * np.sin(theta_rad)

    c_th, s_th = np.cos(theta_rad), np.sin(theta_rad)
    R_mat = np.array([[c_th, -s_th], [s_th, c_th]])

    sedan_profile = np.array([
        [-0.65, 0.08], [0.65, 0.08], [0.65, 0.20], [0.45, 0.24],
        [0.15, 0.44], [-0.25, 0.44], [-0.48, 0.25], [-0.65, 0.22]
    ])
    sedan_rot = np.dot(sedan_profile, R_mat.T) + np.array([car_x, car_y])
    ax1.add_patch(patches.Polygon(sedan_rot, facecolor='#e9ecef', edgecolor='#495057', lw=1.8, zorder=3))

    win_profile = np.array([
        [-0.22, 0.41], [0.12, 0.41], [0.38, 0.26], [-0.42, 0.26]
    ])
    win_rot = np.dot(win_profile, R_mat.T) + np.array([car_x, car_y])
    ax1.add_patch(patches.Polygon(win_rot, facecolor='#d0ebff', edgecolor='#1864ab', lw=1.2, zorder=4))

    for wx_rel in [-0.40, 0.40]:
        w_pt = np.dot(np.array([wx_rel, 0.08]), R_mat.T) + np.array([car_x, car_y])
        ax1.add_patch(patches.Circle((w_pt[0], w_pt[1]), 0.08, facecolor='#212529', edgecolor='#495057', lw=1.5, zorder=5))
        ax1.add_patch(patches.Circle((w_pt[0], w_pt[1]), 0.045, facecolor='#ced4da', edgecolor='#868e96', lw=1, zorder=6))

    v_arrow_len = 0.55
    ax1.annotate('', xy=(car_x + 0.90 * c_th + v_arrow_len * c_th, car_y + 0.90 * s_th + 0.35 + v_arrow_len * s_th),
                 xytext=(car_x + 0.90 * c_th, car_y + 0.90 * s_th + 0.35),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=15))
    ax1.text(car_x + 0.90 * c_th + 0.25 * c_th, car_y + 0.90 * s_th + 0.50, f"v = {v_kmh:.1f} km/h",
             color='#2b8a3e', fontsize=10.5, fontweight='bold')

    ax1.annotate('', xy=(car_x + 0.55 * c_th, car_y + 0.55 * s_th - 0.05),
                 xytext=(car_x - 0.10 * c_th, car_y - 0.10 * s_th - 0.05),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=3.0, mutation_scale=15))
    ax1.text(car_x + 0.20 * c_th, car_y - 0.25, f"F = {F_tractive:.0f} N (3.03 kN)",
             color='#c92a2a', fontweight='bold', fontsize=10)

    ax1.text(3.0, 2.9, f"Elapsed Time: t = {t_curr:.1f} / 8.0 s  |  acc a = {a_acc:.3f} m/s^2",
             fontsize=10.5, fontweight='bold', color='#212529', ha='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

    # ==========================================
    # [Right Panel] Speed-Time Response & Impulse
    # ==========================================
    ax2.set_xlim(-0.5, 8.5)
    ax2.set_ylim(18.0, 75.0)
    ax2.set_title("Speed v(t) Response & Linear Impulse Formulation", fontsize=12.5, fontweight='bold', pad=10)

    t_full = np.linspace(0, 8.0, 100)
    v_full_kmh = (v1 + a_acc * t_full) * 3.6
    ax2.plot(t_full, v_full_kmh, color='#1864ab', lw=2.8, label='Car Speed v(t) [km/h]')

    ax2.plot([0.0], [30.0], 'bo', markersize=8)
    ax2.text(0.3, 31.0, "v1 = 30 km/h (8.33 m/s)", color='#1864ab', fontweight='bold', fontsize=9.5)
    ax2.plot([8.0], [60.0], 'ro', markersize=8)
    ax2.text(7.6, 62.0, "v2 = 60 km/h (16.67 m/s)", color='#c92a2a', fontweight='bold', fontsize=9.5, ha='right')

    ax2.plot(t_curr, v_kmh, 'o', color='#f59f00', markersize=10, zorder=5)
    ax2.axvline(t_curr, color='#f59f00', linestyle=':', lw=1.5)

    ax2.set_xlabel("Time t (s)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Vehicle Speed (km/h)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', color='#dee2e6')
    ax2.legend(loc='upper left', fontsize=10)

    imp_text = (
        "Linear Impulse-Momentum Principle (Incline Direction):\n"
        "   m*v1 + ∫[F - mg sin θ] dt = m*v2\n"
        "   [F - 1500(9.81)(sin 5.71°)] * (8 s) = 1500(16.667 - 8.333)\n"
        "   [F - 1464.2 N] * 8 s = 12,500 N*s (Total Momentum Change)\n"
        "   F - 1464.2 = 1562.5 N  ==>  F = 3026.7 N\n"
        "Textbook Official Answer: F = 3030 N (3.03 kN)"
    )
    ax2.text(0.0, 20.0, imp_text, fontsize=9.0,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "prob3_140_car_incline_impulse.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=100)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
