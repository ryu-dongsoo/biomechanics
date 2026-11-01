# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Example 2.8: Powered Flight of High-Altitude Rocket (n-t Coordinates and Radius of Curvature)
# Exact replication of Meriam Dynamics Sample Problem 2/8 textbook illustration with bottom-left legend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# Styling and fonts
plt.rcParams['font.family'] = 'DejaVu Serif'
plt.rcParams['mathtext.fontset'] = 'cm'

# --- 1. Physical Parameters and Kinematics Computation ---
v0_kmh = 20000.0
v0 = v0_kmh / 3.6  # 5555.56 m/s
theta_target_deg = 15.0
theta0 = np.radians(-theta_target_deg)

ax_phys = 6.0   # m/s² (horizontal thrust)
ay_phys = -9.0  # m/s² (downward gravity)

frames = 120
t_phys = np.linspace(-6.0, 0.0, frames)

vx = v0 * np.cos(theta0) + ax_phys * t_phys
vy = v0 * np.sin(theta0) + ay_phys * t_phys
v_phys = np.sqrt(vx**2 + vy**2)
theta_phys = np.arctan2(vy, vx)

at_phys = (vx * ax_phys + vy * ay_phys) / v_phys
an_phys = np.abs(vx * ay_phys - vy * ax_phys) / v_phys
rho_phys = v_phys**2 / an_phys
beta_dot = an_phys / v_phys

# --- 2. Visual Space Trajectory Mapping ---
et = np.array([np.cos(theta0), np.sin(theta0)])
en = np.array([-np.sin(theta_target_deg*np.pi/180), -np.cos(theta_target_deg*np.pi/180)])

s_full = np.linspace(-7.5, 5.0, 300)
curv = 0.035
x_path = s_full * et[0] + (curv * s_full**2) * en[0]
y_path = s_full * et[1] + (curv * s_full**2) * en[1]

s_flight = np.linspace(-5.5, 0.0, frames)
xG = s_flight * et[0] + (curv * s_flight**2) * en[0]
yG = s_flight * et[1] + (curv * s_flight**2) * en[1]

# --- 3. Canvas and Layout (12.0 x 7.5 Wide) ---
fig = plt.figure(figsize=(12.0, 7.5), dpi=140, facecolor='#cbe6f3')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#cbe6f3')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-8.2, 6.8)
ax.set_ylim(-6.8, 2.5)

# (1) Orange Dashed Path
ax.plot(x_path, y_path, color='#f39c12', lw=1.6, ls=(0, (10, 6)), zorder=2)

for s_val in [-5.0, 3.2]:
    idx = np.argmin(np.abs(s_full - s_val))
    xp, yp = x_path[idx], y_path[idx]
    dx = x_path[idx+1] - x_path[idx-1]
    dy = y_path[idx+1] - y_path[idx-1]
    ang = np.arctan2(dy, dx)
    d1 = np.array([-0.28 * np.cos(ang - 0.42), -0.28 * np.sin(ang - 0.42)])
    d2 = np.array([-0.28 * np.cos(ang + 0.42), -0.28 * np.sin(ang + 0.42)])
    ax.plot([xp+d1[0], xp, xp+d2[0]], [yp+d1[1], yp, yp+d2[1]], color='#f39c12', lw=1.6, zorder=3)

# (2) Horizontal Reference Line and "Horizontal"
ax.plot([-7.5, -1.6], [0, 0], color='#4a5568', ls=(0, (8, 5)), lw=1.5, zorder=1)
ax.text(-6.8, -0.45, 'Horizontal', fontsize=16, fontfamily='DejaVu Serif', color='#2d3748', va='top', ha='center')

# (3) Tangential Axis (t-axis)
ax.plot([0, 6.0*et[0]], [0, 6.0*et[1]], color='#4a5568', ls=(0, (8, 5)), lw=1.5, zorder=1)
ax.text(6.2*et[0], 6.2*et[1], r'$t$', fontsize=20, fontstyle='italic', va='center', ha='left', color='#2d3748')

# (4) Normal Axis (n-axis), rho, C
n_dist = 5.8
ax.plot([0, 1.4*en[0]], [0, 1.4*en[1]], color='#4a5568', ls=(0, (6, 4)), lw=1.5, zorder=1)
ax.plot([1.4*en[0], n_dist*en[0]], [1.4*en[1], n_dist*en[1]], color='#2d3748', ls='-', lw=1.0, zorder=1)

ax.text(1.9*en[0] - 0.22, 1.9*en[1], r'$n$', fontsize=20, fontstyle='italic', va='center', ha='right', color='#2d3748')
ax.text(3.7*en[0] - 0.22, 3.7*en[1], r'$\rho$', fontsize=20, fontstyle='italic', va='center', ha='right', color='#2d3748')

C_pos = n_dist * en
ax.plot([C_pos[0]], [C_pos[1]], marker='x', color='#2d3748', markersize=9, markeredgewidth=1.8, zorder=4)
ax.text(C_pos[0] - 0.05, C_pos[1] - 0.45, r'$C$', fontsize=20, fontstyle='italic', va='top', ha='center', color='#2d3748')

# (5) Gravity Vector g = 9 m/s²
ax.plot([0, 0], [0, -1.4], color='#4a5568', ls=(0, (6, 4)), lw=1.5, zorder=1)
arr_g_fixed = patches.FancyArrowPatch((0, -1.4), (0, -2.8), arrowstyle='->,head_width=0.22,head_length=0.42',
                                      color='#00a86b', lw=2.0, mutation_scale=13, zorder=5)
ax.add_patch(arr_g_fixed)
ax.text(0.25, -2.1, r'$g = 9\ \mathrm{m/s^2}$', fontsize=18, fontstyle='italic', color='#2d3748', va='center', ha='left')

# (6) Rocket Body
x_back = -1.6
x_front = 1.0
x_nose = 2.4
y_h = 0.22

def create_rocket_artists():
    body = patches.Rectangle((x_back, -y_h), (x_front - x_back), 2*y_h, facecolor='white', edgecolor='#2d3748', lw=1.6, zorder=6)
    
    nose_t = np.linspace(0, 1, 30)
    nx = x_front + (x_nose - x_front) * nose_t
    ny_u = y_h * (1 - nose_t**1.3)
    ny_l = -y_h * (1 - nose_t**1.3)
    nose_poly = np.column_stack([np.concatenate([nx, nx[::-1]]), np.concatenate([ny_u, ny_l[::-1]])])
    nose = patches.Polygon(nose_poly, facecolor='white', edgecolor='#2d3748', lw=1.6, zorder=6)
    
    band_w = 0.22
    band1 = patches.Rectangle((-0.9, -y_h), band_w, 2*y_h, facecolor='#1a202c', edgecolor='#2d3748', lw=0.8, zorder=7)
    band2 = patches.Rectangle((0.7, -y_h), band_w, 2*y_h, facecolor='#1a202c', edgecolor='#2d3748', lw=0.8, zorder=7)
    
    g_dot = patches.Circle((0, 0), 0.10, facecolor='#1a202c', edgecolor='none', zorder=8)
    nozzle = patches.Rectangle((x_back - 0.08, -y_h*0.65), 0.08, 1.3*y_h, facecolor='#718096', edgecolor='#2d3748', lw=1.0, zorder=6)
    
    return [body, nose, band1, band2, g_dot, nozzle]

rocket_patches = create_rocket_artists()
for p in rocket_patches:
    ax.add_patch(p)

flame_w, flame_h = 1.1, 0.17
flame_t = np.linspace(0, 2*np.pi, 50)
fx_out = (x_back - 0.08) - flame_w * (1 - np.cos(flame_t))/2
fy_out = flame_h * np.sin(flame_t)
flame_outer = patches.Polygon(np.column_stack([fx_out, fy_out]), facecolor='#ffffff', edgecolor='#f39c12', lw=1.2, zorder=5)

fx_in = (x_back - 0.08) - 0.65 * (1 - np.cos(flame_t))/2
fy_in = 0.08 * np.sin(flame_t)
flame_inner = patches.Polygon(np.column_stack([fx_in, fy_in]), facecolor='#f39c12', edgecolor='none', zorder=5)

ax.add_patch(flame_outer)
ax.add_patch(flame_inner)

txt_G = ax.text(0, y_h + 0.16, r'$G$', fontsize=22, fontstyle='italic', fontweight='bold', color='#2d3748', ha='center', va='bottom', zorder=9)

arr_thrust = patches.FancyArrowPatch((x_nose + 0.15, 0), (x_nose + 1.85, 0),
                                     arrowstyle='->,head_width=0.20,head_length=0.40',
                                     color='#00a86b', lw=2.0, mutation_scale=13, zorder=8)
ax.add_patch(arr_thrust)
txt_thrust = ax.text(x_nose + 1.0, 0.28, r'$6\ \mathrm{m/s^2}$', fontsize=18, fontstyle='italic', color='#2d3748', ha='center', va='bottom', zorder=9)

arr_v = patches.FancyArrowPatch((x_nose + 0.15, 0), (x_nose + 0.15 + 1.85*et[0], 1.85*et[1]),
                                arrowstyle='->,head_width=0.20,head_length=0.40',
                                color='#00a86b', lw=2.0, mutation_scale=13, zorder=8)
ax.add_patch(arr_v)
txt_v = ax.text(x_nose + 0.3 + 1.85*et[0], 1.85*et[1] - 0.05, r'$v = 20(10^3)\ \mathrm{km/h}$',
                fontsize=18, fontstyle='italic', color='#2d3748', va='center', ha='left', zorder=9)

arc_15 = patches.Arc((x_nose + 0.15, 0), 1.5, 1.5, angle=0, theta1=-15, theta2=0, color='#00a86b', lw=1.3, zorder=8)
ax.add_patch(arc_15)
txt_15 = ax.text(x_nose + 0.15 + 0.35, -0.28, r'$15^\circ$', fontsize=16, fontstyle='italic', color='#2d3748', ha='left', va='top', zorder=9)

# --- 4. Bottom-Left Legend / Information Panel ---
info_panel = fig.text(0.025, 0.035, '', fontsize=10.5, va='bottom', ha='left',
                      bbox=dict(facecolor='white', alpha=0.96, edgecolor='#e67e22', boxstyle='round,pad=0.55', lw=1.5))

dynamic_artists = []

def animate(i):
    global dynamic_artists
    for art in dynamic_artists:
        art.remove()
    dynamic_artists.clear()

    xg_curr = xG[i]
    yg_curr = yG[i]
    th_curr = theta_phys[i]
    th_deg_curr = abs(np.degrees(th_curr))

    trans = Affine2D().translate(xg_curr, yg_curr) + ax.transData
    for p in rocket_patches:
        p.set_transform(trans)

    flk = np.random.uniform(0.95, 1.25)
    fx_o = (x_back - 0.08) - (flame_w * flk) * (1 - np.cos(flame_t))/2
    fy_o = (flame_h * np.random.uniform(0.9, 1.1)) * np.sin(flame_t)
    flame_outer.set_xy(np.column_stack([fx_o, fy_o]))
    flame_outer.set_transform(trans)

    fx_i = (x_back - 0.08) - (0.65 * flk) * (1 - np.cos(flame_t))/2
    fy_i = 0.08 * np.sin(flame_t)
    flame_inner.set_xy(np.column_stack([fx_i, fy_i]))
    flame_inner.set_transform(trans)

    txt_G.set_position((xg_curr, yg_curr + y_h + 0.16))

    xn_curr, yn_curr = xg_curr + x_nose, yg_curr

    arr_thrust.set_positions((xn_curr + 0.15, yn_curr), (xn_curr + 1.85, yn_curr))
    txt_thrust.set_position((xn_curr + 1.0, yn_curr + 0.28))

    et_dyn = np.array([np.cos(th_curr), np.sin(th_curr)])
    arr_v.set_positions((xn_curr + 0.15, yn_curr), (xn_curr + 0.15 + 1.85*et_dyn[0], yn_curr + 1.85*et_dyn[1]))
    txt_v.set_position((xn_curr + 0.3 + 1.85*et_dyn[0], yn_curr + 1.85*et_dyn[1] - 0.05))

    arc_15.center = (xn_curr + 0.15, yn_curr)
    arc_15.theta1 = np.degrees(th_curr)
    arc_15.theta2 = 0
    txt_15.set_position((xn_curr + 0.15 + 0.35, yn_curr - 0.28))
    txt_15.set_text(f'{th_deg_curr:.1f}°' if i < frames - 1 else r'$15^\circ$')

    is_final = (i == frames - 1)
    status_header = "[Example 2/8 Exact Kinematics & Solution]" if is_final else f"[Example 2/8 In Flight (t = {t_phys[i]:+.1f} s)]"

    info_str = (
        f"{status_header}\n"
        f"─────────────────────────────────\n"
        f"• Velocity: $v = 20(10^3)$ km/h ($5,555.6$ m/s)\n"
        f"• Tangential Accel: $\\dot{{v}} = a_t = 8.13$ m/s²\n"
        f"• Normal Accel: $a_n = 7.14$ m/s²\n"
        f"• (a) Radius of Curvature: $\\rho = \\mathbf{{4,320\\ km}}$\n"
        f"• (d) Angular Rate: $\\dot{{\\beta}} = \\mathbf{{1.285 \\times 10^{{-3}}\\ rad/s}}$"
    )
    info_panel.set_text(info_str)

    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.55', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.95, edgecolor='#3498db', boxstyle='round,pad=0.55', lw=1.2))

    return []

ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)

gif_path = Path(__file__).parent / 'ex2_8_rocket_flight.gif'
writer = PillowWriter(fps=28)
writer._kwargs = {'loop': None}

print(f"Rendering GIF animation to {gif_path}...")
ani.save(str(gif_path), writer=writer)
print(f"GIF saved successfully: {gif_path}")

try:
    from PIL import Image
    im = Image.open(str(gif_path))
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 35))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(str(gif_path), save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("Hold last frame for 60s and set loop=1 completed.")
except Exception as e:
    print(f"Delay patch failed: {e}")
