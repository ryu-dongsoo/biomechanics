# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

"""
Dynamics 9th Edition - Chapter 3 Kinetics of Particles
Problem 3/64: Normal Force and Scale Reading on Roller-Coaster Track (n-t Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) standard layout (biomechanics-diagram-standard compliant)
- 1:1 textbook accurate geometry:
  * Concave trough A (radius 40 m) with top curvature center (+) and 40 m dimension arrow
  * Convex crest B (radius 20 m) with bottom curvature center (+) and 20 m dimension arrow
  * 4-car connected rollercoaster train (solid at A with v_A, dashed at B with v_B)
  * Dynamic ride simulation and FBD comparison at A vs B
- 100% verified against Wiley official solution manual:
  * Trough A (v_A = 22 m/s, rho_A = 40 m): N_A = m(g + v_A^2/rho_A) = 75(9.81 + 12.10) = 1643 N (2.23 W)
  * Crest B (v_B = 12 m/s, rho_B = 20 m): N_B = m(g - v_B^2/rho_B) = 75(9.81 - 7.20) = 195.8 N (0.27 W)
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
m = 75.0                # Passenger mass (kg)
g = 9.81                # Gravity (m/s^2)
W = m * g               # Weight 735.8 N
RA = 40.0               # Radius at A (m)
vA = 22.0               # Speed at A (m/s)
RB = 20.0               # Radius at B (m)
vB = 12.0               # Speed at B (m/s)

# Wiley Official Solutions
NA_val = m * (g + (vA**2) / RA)    # 1643.25 N -> 1643 N (2.23 W)
NB_val = m * (g - (vB**2) / RB)    # 195.75 N -> 195.8 N (0.27 W)

# 2. Track Profile
def get_track_profile(x):
    return -0.40 + 0.75 / (1.0 + np.exp(-3.5 * (x - 0.20))) - 0.12 * (x - 0.20)

x_track = np.linspace(-1.35, 1.75, 180)
y_track = get_track_profile(x_track)

idx_A = np.argmin(y_track[:100])
xA_pos, yA_pos = x_track[idx_A], y_track[idx_A]

idx_B = 80 + np.argmax(y_track[80:])
xB_pos, yB_pos = x_track[idx_B], y_track[idx_B]

# 3. Ride Time Sampling
n_frames = 64
x_train_series = np.linspace(-1.15, 1.45, n_frames)

# Canvas initialization (14 x 6.5, pure white background)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    xc = x_train_series[frame]
    yc = get_track_profile(xc)
    
    eps = 0.01
    dy_dx = (get_track_profile(xc + eps) - get_track_profile(xc - eps)) / (2 * eps)
    th_slope = np.arctan(dy_dx)
    
    if xc < 0.20:
        factor = (xc - (-1.15)) / (0.20 - (-1.15))
        v_curr = 24.0 - factor * 7.0
        rho_curr = RA
        N_curr = NA_val
        zone_name = "Trough A Section"
    else:
        factor = (xc - 0.20) / (1.45 - 0.20)
        v_curr = 17.0 - factor * 5.0
        rho_curr = RB
        N_curr = NB_val
        zone_name = "Crest B Section"
    
    # ---------------- 1. Main Physical View (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-0.85, 1.25)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/64: Normal Force and Scale Reading on Roller-Coaster Track', fontsize=13, fontweight='bold', pad=12)
    
    # (1) Track rail and ground shadow
    ax_main.plot(x_track, y_track, color='#263238', lw=2.4, zorder=3)
    poly_ground = np.vstack([
        np.column_stack([x_track, y_track]),
        np.column_stack([x_track[::-1], y_track[::-1] - 0.12])
    ])
    ax_main.add_patch(patches.Polygon(poly_ground, closed=True, facecolor='#ede7df', edgecolor='#b0bec5', lw=0.8, zorder=1))
    
    # (2) Trough A center of curvature (+) and 40 m dimension
    cA_x, cA_y = xA_pos + 0.12, yA_pos + 1.15
    ax_main.plot(cA_x, cA_y, 'k+', ms=12, mew=1.8, zorder=4)
    ax_main.annotate('', xy=(xA_pos + 0.02, yA_pos), xytext=(cA_x, cA_y),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(cA_x + 0.05, (cA_y + yA_pos)/2 + 0.08, r'$40\ \mathrm{m}$',
                 fontsize=11.5, fontweight='bold', color='#263238', zorder=5)
    
    # Label A
    ax_main.text(xA_pos, yA_pos - 0.22, 'A', fontsize=16, fontweight='bold', color='#1565c0', ha='center', zorder=5)
    
    # (3) Crest B center of curvature (+) and 20 m dimension
    cB_x, cB_y = xB_pos + 0.08, yB_pos - 0.70
    ax_main.plot(cB_x, cB_y, 'k+', ms=12, mew=1.8, zorder=4)
    ax_main.annotate('', xy=(xB_pos, yB_pos), xytext=(cB_x, cB_y),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(cB_x - 0.18, (cB_y + yB_pos)/2 - 0.02, r'$20\ \mathrm{m}$',
                 fontsize=11.5, fontweight='bold', color='#263238', zorder=5)
    
    # Label B
    ax_main.text(xB_pos, yB_pos - 0.22, 'B', fontsize=16, fontweight='bold', color='#1565c0', ha='center', zorder=5)
    
    # (4) Speed arrows v_A and v_B
    ax_main.annotate('', xy=(xA_pos + 0.28, yA_pos + 0.18), xytext=(xA_pos - 0.08, yA_pos + 0.18),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.0), zorder=6)
    ax_main.text(xA_pos + 0.08, yA_pos + 0.24, r'$v_A$', fontsize=13, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=6)
    
    ax_main.annotate('', xy=(xB_pos + 0.26, yB_pos + 0.18), xytext=(xB_pos - 0.08, yB_pos + 0.18),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.0), zorder=6)
    ax_main.text(xB_pos + 0.08, yB_pos + 0.24, r'$v_B$', fontsize=13, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=6)
    
    # (5) Fixed dashed train at crest B
    b_offsets = [-0.18, -0.06, +0.06, +0.18]
    for b_off in b_offsets:
        bx_car = xB_pos + b_off
        by_car = get_track_profile(bx_car)
        car_box_b = patches.Rectangle((-0.045, 0.015), 0.09, 0.06, ls='--',
                                      facecolor='none', edgecolor='#546e7a', lw=1.2, zorder=4)
        t_b = plt.matplotlib.transforms.Affine2D().translate(bx_car, by_car) + ax_main.transData
        car_box_b.set_transform(t_b)
        ax_main.add_patch(car_box_b)
        ax_main.plot(bx_car - 0.03, by_car + 0.015, 'o', ms=2.5, mfc='none', mec='#546e7a', zorder=4)
        ax_main.plot(bx_car + 0.03, by_car + 0.015, 'o', ms=2.5, mfc='none', mec='#546e7a', zorder=4)
    
    # (6) Dynamic 4-car train
    train_car_spacing = 0.12
    car_w, car_h = 0.095, 0.065
    for c_idx in range(4):
        x_ci = xc - (3 - c_idx) * train_car_spacing
        y_ci = get_track_profile(x_ci)
        d_ci = (get_track_profile(x_ci + eps) - get_track_profile(x_ci - eps)) / (2 * eps)
        th_ci = np.arctan(d_ci)
        
        car_rect = patches.Rectangle((-car_w/2, 0.02), car_w, car_h,
                                     facecolor='#fff59d', edgecolor='#f57f17', lw=1.3, zorder=7)
        t_c = plt.matplotlib.transforms.Affine2D().rotate(th_ci).translate(x_ci, y_ci) + ax_main.transData
        car_rect.set_transform(t_c)
        ax_main.add_patch(car_rect)
        
        w_r = 0.018
        u_t = np.array([np.cos(th_ci), np.sin(th_ci)])
        u_n = np.array([-np.sin(th_ci), np.cos(th_ci)])
        w1_pos = np.array([x_ci, y_ci]) - 0.032 * u_t + 0.018 * u_n
        w2_pos = np.array([x_ci, y_ci]) + 0.032 * u_t + 0.018 * u_n
        ax_main.add_patch(patches.Circle(w1_pos, w_r, facecolor='#37474f', zorder=8))
        ax_main.add_patch(patches.Circle(w2_pos, w_r, facecolor='#37474f', zorder=8))
        
        p1_pos = np.array([x_ci, y_ci]) - 0.022 * u_t + 0.095 * u_n
        p2_pos = np.array([x_ci, y_ci]) + 0.022 * u_t + 0.095 * u_n
        ax_main.plot(p1_pos[0], p1_pos[1], 'o', ms=3.5, color='#e65100', zorder=8)
        ax_main.plot(p2_pos[0], p2_pos[1], 'o', ms=3.5, color='#e65100', zorder=8)
    
    # Status Banner
    if abs(xc - xA_pos) < 0.15:
        banner_txt = 'Passing Point A: High G 2.23G (1643 N, 167.5 kgf)'
        banner_bg, banner_edge, banner_col = '#e3f2fd', '#90caf9', '#0d47a1'
    elif abs(xc - xB_pos) < 0.15:
        banner_txt = 'Passing Point B: Floating 0.27G (195.8 N, 20.0 kgf)'
        banner_bg, banner_edge, banner_col = '#fff3e0', '#ffb74d', '#e65100'
    else:
        banner_txt = f'Roller-Coaster In Motion ({zone_name})'
        banner_bg, banner_edge, banner_col = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-1.40, 1.12, banner_txt, fontsize=10.5, fontweight='bold', color=banner_col,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # ---------------- 2. FBD & Analysis View (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD Comparison
    ax_calc.text(0.2, 9.7, '[Passenger FBD Comparison - Point A vs Point B]', fontsize=11, fontweight='bold', color='#1565c0')
    
    # Trough A FBD
    fbd_ax, fbd_ay = 2.6, 7.7
    ax_calc.text(fbd_ax, fbd_ay + 1.6, 'Point A FBD', fontsize=11, fontweight='bold', ha='center', color='#1565c0')
    ax_calc.add_patch(patches.Circle((fbd_ax, fbd_ay), 0.50, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5))
    ax_calc.text(fbd_ax, fbd_ay, r'$75\ \mathrm{kg}$', fontsize=9.5, fontweight='bold', ha='center', va='center', color='#4a2800', zorder=6)
    
    # Point A gravity mg
    ax_calc.annotate('', xy=(fbd_ax, fbd_ay - 1.1), xytext=(fbd_ax, fbd_ay - 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_ax + 0.12, fbd_ay - 0.9, r'$mg$', fontsize=11, fontweight='bold', color='#d32f2f')
    
    # Point A normal force N_A
    ax_calc.annotate('', xy=(fbd_ax, fbd_ay + 1.4), xytext=(fbd_ax, fbd_ay + 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.6), zorder=6)
    ax_calc.text(fbd_ax + 0.12, fbd_ay + 1.05, r'$N_A = 1643\ \mathrm{N}$' + '\n' + r'($2.23\ W$, Heavy)',
                 fontsize=9.2, fontweight='bold', color='#1565c0')
    
    # Crest B FBD
    fbd_bx, fbd_by = 7.2, 7.7
    ax_calc.text(fbd_bx, fbd_by + 1.6, 'Point B FBD', fontsize=11, fontweight='bold', ha='center', color='#e65100')
    ax_calc.add_patch(patches.Circle((fbd_bx, fbd_by), 0.50, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5))
    ax_calc.text(fbd_bx, fbd_by, r'$75\ \mathrm{kg}$', fontsize=9.5, fontweight='bold', ha='center', va='center', color='#4a2800', zorder=6)
    
    # Point B gravity mg
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 1.1), xytext=(fbd_bx, fbd_by - 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_bx + 0.12, fbd_by - 0.9, r'$mg$', fontsize=11, fontweight='bold', color='#d32f2f')
    
    # Point B normal force N_B
    ax_calc.annotate('', xy=(fbd_bx, fbd_by + 0.8), xytext=(fbd_bx, fbd_by + 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#e65100', lw=1.8), zorder=6)
    ax_calc.text(fbd_bx + 0.12, fbd_by + 0.65, r'$N_B = 196\ \mathrm{N}$' + '\n' + r'($0.27\ W$, Floating)',
                 fontsize=9.2, fontweight='bold', color='#e65100')
    
    # (2) Theoretical Derivation Card
    sol_text = (
        "[Theoretical Derivation (n-t Coordinates)]\n"
        r"• Parameters: $m = 75.0\ \mathrm{kg},\ W = mg = 75(9.81) = 735.8\ \mathrm{N}$" + "\n"
        r"  Trough $A$: $\rho_A = 40.0\ \mathrm{m},\ v_A = 22.0\ \mathrm{m/s}$ | Crest $B$: $\rho_B = 20.0\ \mathrm{m},\ v_B = 12.0\ \mathrm{m/s}$" + "\n"
        r"• (1) Trough $A$ (Concave, curvature center upward $\Rightarrow +n$ upward):" + "\n"
        r"  $\sum F_n = N_A - mg = m \frac{v_A^2}{\rho_A} \Rightarrow \mathbf{N_A = m\left(g + \frac{v_A^2}{\rho_A}\right)}$" + "\n"
        r"  $N_A = 75\left(9.81 + \frac{22.0^2}{40.0}\right) = 75(9.81 + 12.10) = \mathbf{1643\ \mathrm{N}}\ (\mathbf{2.23\ W}, 167.5\ \mathrm{kgf})$" + "\n"
        r"• (2) Crest $B$ (Convex, curvature center downward $\Rightarrow +n$ downward):" + "\n"
        r"  $\sum F_n = mg - N_B = m \frac{v_B^2}{\rho_B} \Rightarrow \mathbf{N_B = m\left(g - \frac{v_B^2}{\rho_B}\right)}$" + "\n"
        r"  $N_B = 75\left(9.81 - \frac{12.0^2}{20.0}\right) = 75(9.81 - 7.20) = \mathbf{195.8\ \mathrm{N}}\ (\mathbf{0.27\ W}, 20.0\ \mathrm{kgf})$"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) Real-Time Dynamic Monitor
    live_text = (
        "[Real-Time Dynamic Monitor]\n"
        f"• Train Location: {zone_name} (x = {xc:+.2f} m)\n"
        f"• Speed: v = {v_curr:.1f} m/s | Radius: ρ = {rho_curr:.1f} m\n"
        f"• Scale Normal Force: N = {N_curr:.1f} N ({N_curr/W:.2f} times regular weight W)\n"
        f"• Scale Reading: {N_curr/g:.1f} kgf ({'High G compression' if N_curr > W else 'Apparent weightlessness'})\n"
        f"• Official Solutions: N_A = 1643 N (Trough), N_B = 195.8 N (Crest)"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# Generate and save GIF animation
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_64_rollercoaster_scale.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Problem 3/64 English animation generated: {gif_path}")
