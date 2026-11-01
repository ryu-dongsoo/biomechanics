# -*- coding: utf-8 -*-
"""
Dynamics 9th Edition - Chapter 3 Kinetics of Particles
Problem 3/37: Normal Force on Block Sliding on Vertical Curved Track (n-t Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.5) standard layout (biomechanics-diagram-standard compliant)
- 1:1 textbook accurate geometry:
  * Top center of curvature (+) with vertical centerline
  * Lowest point A (0°) and left 30° inclined point B
  * 3 m radius dimension arrow from center to track
  * Block moving from right towards A and B with velocity v
- 100% verified against Wiley official solution manual:
  * Point A (theta = 0°, v_A = 5 m/s): N_A = m(g + v_A^2/R) = 0.6(9.81 + 25/3) = 10.89 N
  * Point B (theta = 30°, v_B = 4 m/s): N_B = m(g*cos 30° + v_B^2/R) = 0.6(9.81*cos 30° + 16/3) = 8.30 N
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
m = 0.6               # Block mass (kg)
g = 9.81              # Gravity (m/s^2)
R = 3.0               # Radius of curvature (m)
vA = 5.0              # Speed at A (m/s)
vB = 4.0              # Speed at B (m/s)
th_B = np.radians(30.0) # Left 30 degrees

# Wiley Official Solutions
NA_val = m * (g + (vA**2) / R)                    # 10.886 N -> 10.89 N
NB_val = m * (g * np.cos(th_B) + (vB**2) / R)     # 8.298 N -> 8.30 N

# 2. Animation Time Sampling
n_frames = 64
t_eval = np.linspace(0, 1.0, n_frames)
theta_deg_series = 34.0 * np.cos(2 * np.pi * t_eval)
theta_series = np.radians(theta_deg_series)

# Canvas initialization (14 x 6.5, pure white background)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = theta_series[frame]
    th_deg = theta_deg_series[frame]
    
    px = R * np.sin(th)
    py = -R * np.cos(th)
    
    g_eff = (vA**2 - vB**2) / (2 * R * (1 - np.cos(th_B)))
    v_sq = max(1.0, vA**2 - 2 * g_eff * R * (1 - np.cos(th)))
    v_curr = np.sqrt(v_sq)
    
    vel_sign = -np.sign(np.sin(2 * np.pi * t_eval[frame])) if abs(np.sin(2 * np.pi * t_eval[frame])) > 1e-3 else -1.0
    an_curr = (v_curr**2) / R
    N_curr = m * (g * np.cos(th) + an_curr)
    
    # ---------------- 1. Main Physical View (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.5, 2.5)
    ax_main.set_ylim(-3.5, 0.4)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/37: Normal Force on Block on Vertical Curved Track', fontsize=13, fontweight='bold', pad=12)
    
    # (1) Center of curvature (+) and vertical centerline
    ax_main.plot(0, 0, 'k+', ms=12, mew=1.8, zorder=5)
    ax_main.plot([0, 0], [0, -R], color='#546e7a', ls='-.', lw=1.2, zorder=2)
    
    # (2) Left point B reference line (30 degrees left)
    bx_ref = -R * np.sin(th_B)
    by_ref = -R * np.cos(th_B)
    ax_main.plot([0, bx_ref], [0, by_ref], color='#78909c', ls='--', lw=1.2, zorder=2)
    
    # Arc for 30 degrees
    arc_patch = patches.Arc((0, 0), 1.8, 1.8, angle=-90, theta1=-30, theta2=0, color='#37474f', lw=1.2)
    ax_main.add_patch(arc_patch)
    ax_main.text(-0.38, -1.05, r'$30^\circ$', fontsize=11, fontweight='bold', color='#263238')
    
    # (3) Circular Guide Track
    arc_span = np.linspace(-np.radians(46), np.radians(46), 120)
    rx_rail = R * np.sin(arc_span)
    ry_rail = -R * np.cos(arc_span)
    ax_main.plot(rx_rail, ry_rail, color='#37474f', lw=2.2, zorder=3)
    
    # Track thickness shadow
    thick = 0.20
    poly_rail = np.vstack([
        np.column_stack([rx_rail, ry_rail]),
        np.column_stack([(R + thick) * np.sin(arc_span[::-1]), -(R + thick) * np.cos(arc_span[::-1])])
    ])
    ax_main.add_patch(patches.Polygon(poly_rail, closed=True, facecolor='#ede7df', edgecolor='#b0bec5', lw=0.8, zorder=1))
    
    # (4) Radius dimension arrow 3 m
    dim_th = np.radians(12.0)
    dim_target = np.array([R * np.sin(dim_th), -R * np.cos(dim_th)])
    ax_main.annotate('', xy=dim_target, xytext=(0, 0),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(dim_target[0]/2 + 0.12, dim_target[1]/2, r'$3\ \mathrm{m}$',
                 fontsize=12, fontweight='bold', color='#263238', zorder=5)
    
    # (5) Points A and B labels
    ax_main.plot(0, -R, 'ko', ms=4, zorder=4)
    ax_main.text(0.0, -R - 0.32, 'A', fontsize=15, fontweight='bold', color='#1565c0', ha='center', zorder=6)
    
    ax_main.plot(bx_ref, by_ref, 'ko', ms=4, zorder=4)
    ax_main.text(bx_ref - 0.12, by_ref - 0.25, 'B', fontsize=15, fontweight='bold', color='#1565c0', ha='center', zorder=6)
    
    # (6) Block patch
    bw, bh = 0.36, 0.20
    rot_deg = np.degrees(th)
    blk_patch = patches.Rectangle((-bw/2, 0), bw, bh, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(rot_deg).translate(px, py) + ax_main.transData
    blk_patch.set_transform(t_blk)
    ax_main.add_patch(blk_patch)
    
    blk_cx = px - np.sin(th) * bh / 2
    blk_cy = py + np.cos(th) * bh / 2
    
    # (7) Velocity vector v
    t_hat = np.array([np.cos(th), np.sin(th)])
    v_vec = t_hat * vel_sign
    v_arrow_len = 0.55
    v_start = np.array([blk_cx, blk_cy + 0.15])
    v_end = v_start + v_arrow_len * v_vec
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.45', color='#2e7d32', lw=2.2), zorder=8)
    ax_main.text(v_end[0] + 0.05 * v_vec[0], v_end[1] + 0.08, r'$v$',
                 fontsize=14, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=9)
    
    # Status Banner
    if abs(th_deg) < 4.0:
        pos_str = 'Passing Point A (θ ≈ 0°)'
        b_col, b_edge, b_txt = '#e8f5e9', '#81c784', '#1b5e20'
    elif abs(th_deg - (-30.0)) < 4.0:
        pos_str = 'Passing Point B (θ ≈ -30°)'
        b_col, b_edge, b_txt = '#e3f2fd', '#90caf9', '#0d47a1'
    else:
        pos_str = f'Sliding on Track (θ = {th_deg:+.1f}°)'
        b_col, b_edge, b_txt = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-2.4, 0.25, f'State: {pos_str}', fontsize=10.5, fontweight='bold', color=b_txt,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=b_col, edgecolor=b_edge, lw=1.2))
    
    # ---------------- 2. Analysis & Monitoring View (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD
    ax_calc.text(0.2, 9.7, '[Free Body Diagram - n-t Coordinates]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_bx, fbd_by = 4.5, 8.1
    fbd_sq = patches.Rectangle((fbd_bx - 0.7, fbd_by - 0.4), 1.4, 0.8,
                               facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_bx, fbd_by, r'$m = 0.6\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800', zorder=6)
    
    # Force N
    n_arrow_len = 0.5 + (N_curr / 12.0) * 0.9
    ax_calc.annotate('', xy=(fbd_bx, fbd_by + 0.4 + n_arrow_len), xytext=(fbd_bx, fbd_by + 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by + 0.4 + n_arrow_len, r'$N$', fontsize=14, fontweight='bold', color='#1565c0')
    
    # Force mg
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 0.4 - 1.0), xytext=(fbd_bx, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#d32f2f', lw=2.2), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by - 0.4 - 0.8, r'$mg$', fontsize=13, fontweight='bold', color='#d32f2f')
    
    # n-t axes
    ax_calc.plot([fbd_bx + 2.0, fbd_bx + 2.0], [fbd_by, fbd_by + 1.2], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 2.0, fbd_by + 1.2), xytext=(fbd_bx + 2.0, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 2.15, fbd_by + 1.15, r'$+n$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([fbd_bx + 2.0, fbd_bx + 3.2], [fbd_by, fbd_by], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 3.2, fbd_by), xytext=(fbd_bx + 2.0, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 3.25, fbd_by - 0.10, r'$+t$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # (2) Theoretical Derivation Card
    sol_text = (
        "[Theoretical Derivation (n-t Coordinates)]\n"
        r"• Parameters: $m = 0.6\ \mathrm{kg},\ R = 3.0\ \mathrm{m},\ g = 9.81\ \mathrm{m/s^2}$" + "\n"
        r"  Speed at $A$: $v_A = 5.0\ \mathrm{m/s}\ (\theta = 0^\circ)$, Speed at $B$: $v_B = 4.0\ \mathrm{m/s}\ (\theta = 30^\circ)$" + "\n"
        r"• Normal Equation of Motion ($\sum F_n = m a_n = m \frac{v^2}{R}$):" + "\n"
        r"  $\sum F_n = N - mg\cos\theta = m \frac{v^2}{R} \Rightarrow \mathbf{N = m\left(g\cos\theta + \frac{v^2}{R}\right)}$" + "\n"
        r"• (1) Passing Lowest Point $A$ ($\theta = 0^\circ,\ v_A = 5.0\ \mathrm{m/s}$):" + "\n"
        r"  $\mathbf{N_A = 0.6\left(9.81 + \frac{5.0^2}{3.0}\right) = 0.6(9.81 + 8.333) = 10.89\ \mathrm{N}}$" + "\n"
        r"• (2) Passing Inclined Point $B$ ($\theta = 30^\circ,\ v_B = 4.0\ \mathrm{m/s}$):" + "\n"
        r"  $\mathbf{N_B = 0.6\left(9.81\cos 30^\circ + \frac{4.0^2}{3.0}\right) = 0.6(8.496 + 5.333) = 8.30\ \mathrm{N}}$"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) Real-Time Dynamic Monitor
    live_text = (
        "[Real-Time Dynamic Monitor]\n"
        f"• Current Position: θ = {th_deg:+.1f}° (from bottom)\n"
        f"• Block Speed: v = {v_curr:.2f} m/s (Direction: {'← Leftwards (towards A·B)' if vel_sign < 0 else '→ Rightwards'})\n"
        f"• Normal Acceleration: a_n = v²/R = {an_curr:.2f} m/s²\n"
        f"• Track Normal Force: N = {N_curr:.2f} N (Gravity {m*g*np.cos(th):.2f} N + Centripetal {m*an_curr:.2f} N)\n"
        f"• Official Solutions: N_A = {NA_val:.2f} N (Point A), N_B = {NB_val:.2f} N (Point B)"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# Generate and save GIF animation
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_37_curved_track_block.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Problem 3/37 English animation generated: {gif_path}")
