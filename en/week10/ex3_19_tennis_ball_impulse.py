"""
Sample Problem 3.19: Tennis Racquet Impact Impulse and Linear Momentum
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Ball mass m = 60 g = 0.060 kg
- Initial horizontal velocity v1 = 15 m/s (at peak of bounce, to the left)
- Rebound velocity v2 = 21 m/s (15 deg above horizontal to the right)
- Contact duration dt = 0.02 s
- Gravitational acceleration g = 9.81 m/s^2

Analytical Result:
- Impact force components: Rx = 105.9 N, Ry = 16.89 N
- Average impact force: R = 107.2 N, angle beta = 9.07 deg
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

m = 0.060          # kg
v1 = 15.0          # m/s
v2 = 21.0          # m/s
theta_deg = 15.0
theta_rad = np.radians(theta_deg)
dt = 0.02          # s
g = 9.81           # m/s^2
W = m * g          # 0.5886 N

G1_x = -m * v1
G2_x = m * v2 * np.cos(theta_rad)
G2_y = m * v2 * np.sin(theta_rad)

Rx = (G2_x - G1_x) / dt              # 105.85 N -> 105.9 N
Ry = ((G2_y) + W * dt) / dt          # 16.89 N
R = np.hypot(Rx, Ry)                 # 107.19 N -> 107.2 N
beta_deg = np.degrees(np.arctan2(Ry, Rx))

n_frames = 60
t_arr = np.linspace(-0.6, 0.6, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def draw_tennis_player(ax, px, py):
    ax.add_patch(patches.Circle((px - 0.22, py + 0.48), 0.045, facecolor='#fcc419', edgecolor='#d9480f', lw=1.2, zorder=4))
    ax.add_patch(patches.Circle((px - 0.20, py + 0.46), 0.038, facecolor='#ffec99', edgecolor='#fcc419', lw=1, zorder=5))

    shirt_pts = np.array([
        [px - 0.25, py + 0.43], [px - 0.16, py + 0.43],
        [px - 0.13, py + 0.28], [px - 0.25, py + 0.28]
    ])
    ax.add_patch(patches.Polygon(shirt_pts, facecolor='#a5d8ff', edgecolor='#1971c2', lw=1.5, zorder=4))

    ax.plot([px - 0.16, px - 0.02], [py + 0.42, py + 0.42], color='#ffec99', lw=4, solid_capstyle='round', zorder=4)
    ax.plot([px - 0.22, px - 0.10, px - 0.02], [py + 0.40, py + 0.32, py + 0.30],
            color='#ffec99', lw=4.5, solid_capstyle='round', zorder=4)

    skirt_pts = np.array([
        [px - 0.26, py + 0.28], [px - 0.12, py + 0.28],
        [px - 0.08, py + 0.16], [px - 0.29, py + 0.16]
    ])
    ax.add_patch(patches.Polygon(skirt_pts, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5, zorder=3))

    ax.plot([px - 0.25, px - 0.32, px - 0.38], [py + 0.16, py + 0.06, py - 0.05],
            color='#ffec99', lw=5, solid_capstyle='round', zorder=2)
    ax.add_patch(patches.Rectangle((px - 0.44, py - 0.08), 0.08, 0.035, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2, zorder=3))

    ax.plot([px - 0.12, px - 0.08, px - 0.05], [py + 0.16, py + 0.05, py - 0.05],
            color='#ffec99', lw=5, solid_capstyle='round', zorder=2)
    ax.add_patch(patches.Rectangle((px - 0.08, py - 0.08), 0.08, 0.035, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2, zorder=3))

    ax.plot([px - 0.02, px + 0.02], [py + 0.30, py + 0.26], color='#343a40', lw=5, solid_capstyle='round', zorder=5)
    racket_head = patches.Ellipse((px + 0.03, py + 0.31), 0.05, 0.15, angle=-10,
                                  facecolor='none', edgecolor='#e03131', lw=3.5, zorder=5)
    ax.add_patch(racket_head)
    for dy in np.linspace(-0.05, 0.05, 5):
        ax.plot([px + 0.01, px + 0.05], [py + 0.31 + dy, py + 0.31 + dy], color='#ced4da', lw=1, zorder=4)

def update(frame):
    t = t_arr[frame]
    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] Textbook Schematic & Kinematics
    # ==========================================
    ax1.set_xlim(-0.6, 1.4)
    ax1.set_ylim(-0.2, 0.8)
    ax1.set_aspect('equal')
    ax1.set_title("Sample Problem 3.19: Tennis Racquet Impact Dynamics", fontsize=13, fontweight='bold', pad=12)

    ax1.fill_between([-0.6, 1.4], -0.2, -0.08, color='#dee2e6', alpha=0.5)
    ax1.plot([-0.6, 1.4], [-0.08, -0.08], color='#495057', lw=2.5)

    impact_x, impact_y = 0.08, 0.31
    draw_tennis_player(ax1, 0.0, 0.0)

    bx_pts = np.linspace(0.85, impact_x, 50)
    by_pts = impact_y - 0.658 * (bx_pts - impact_x)**2
    ax1.plot(bx_pts, by_pts, color='#f76707', linestyle='--', lw=1.8, label='Incoming Bounce')

    bx_pre = np.linspace(1.2, 0.85, 30)
    by_pre = -0.08 + 1.2 * (bx_pre - 0.85)
    ax1.plot(bx_pre, by_pre, color='#f76707', linestyle='--', lw=1.8)

    rx_pts = np.linspace(impact_x, 1.35, 50)
    ry_pts = impact_y + np.tan(theta_rad) * (rx_pts - impact_x) - 0.15 * (rx_pts - impact_x)**2
    ax1.plot(rx_pts, ry_pts, color='#f76707', linestyle='--', lw=1.8, label='Rebound Flight')

    ax1.plot([impact_x, impact_x + 0.6], [impact_y, impact_y], color='#868e96', lw=1.2, linestyle='-')
    arc_ang = np.linspace(0, theta_rad, 25)
    ax1.plot(impact_x + 0.35 * np.cos(arc_ang), impact_y + 0.35 * np.sin(arc_ang), color='#2b8a3e', lw=1.5)
    ax1.text(impact_x + 0.38, impact_y + 0.04, "15 deg", color='#2b8a3e', fontsize=10, fontweight='bold')

    if t < 0:
        curr_x = impact_x + (-t / 0.6) * 0.77
        curr_y = impact_y - 0.658 * (curr_x - impact_x)**2
        ball_state = f"Incoming Flight (v1 = {v1:.0f} m/s left)"
        state_col = '#1864ab'
    elif t <= 0.05:
        curr_x = impact_x
        curr_y = impact_y
        ball_state = f"Impact / Collision Zone (dt = {dt*1000:.0f} ms)"
        state_col = '#e03131'
        arrow_len = 0.32
        ax1.annotate('', xy=(impact_x + arrow_len * np.cos(np.radians(beta_deg)),
                             impact_y + arrow_len * np.sin(np.radians(beta_deg))),
                     xytext=(impact_x, impact_y),
                     arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.5, mutation_scale=18))
        ax1.text(impact_x + 0.15, impact_y + 0.12, f"R = {R:.1f} N\n(beta = {beta_deg:.2f} deg)",
                 color='#e03131', fontweight='bold', fontsize=10)
        spark = patches.Circle((impact_x, impact_y), 0.05, facecolor='#ffe066', edgecolor='#f59f00', lw=1.5, alpha=0.8, zorder=6)
        ax1.add_patch(spark)
    else:
        tau = t - 0.05
        curr_x = impact_x + (tau / 0.55) * 0.90
        curr_y = impact_y + np.tan(theta_rad) * (curr_x - impact_x) - 0.15 * (curr_x - impact_x)**2
        ball_state = f"Rebound Flight (v2 = {v2:.0f} m/s, 15 deg)"
        state_col = '#2b8a3e'

    ball = patches.Circle((curr_x, curr_y), 0.026, facecolor='#ccff00', edgecolor='#5c940d', lw=1.5, zorder=6)
    ax1.add_patch(ball)

    if t < 0:
        ax1.annotate('', xy=(curr_x - 0.18, curr_y), xytext=(curr_x, curr_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.2, mutation_scale=12))
        ax1.text(curr_x, curr_y - 0.06, f"v1 = {v1:.0f} m/s", color='#2b8a3e', fontsize=9.5, fontweight='bold', ha='center')
    elif t > 0.05:
        ax1.annotate('', xy=(curr_x + 0.18 * np.cos(theta_rad), curr_y + 0.18 * np.sin(theta_rad)), xytext=(curr_x, curr_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.2, mutation_scale=12))
        ax1.text(curr_x, curr_y + 0.06, f"v2 = {v2:.0f} m/s", color='#2b8a3e', fontsize=9.5, fontweight='bold')

    ax1.text(0.40, 0.72, f"Status: {ball_state}", fontsize=11, fontweight='bold',
             color=state_col, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=state_col, lw=1.2))

    # ==========================================
    # [Right Panel] Impulse-Momentum Diagram
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("Impulse-Momentum Diagram & Textbook Verification", fontsize=13, fontweight='bold', pad=12)

    rect_box = patches.Rectangle((-0.12, 0.45), 1.32, 0.55, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ Textbook 3-Stage Impulse-Momentum Diagram ]", fontsize=11, fontweight='bold', color='#212529')

    ax2.annotate('', xy=(0.02, 0.72), xytext=(0.25, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.8, mutation_scale=14))
    ax2.text(0.13, 0.76, "m v1 = 0.90 N s", color='#1864ab', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(0.30, 0.70, "+", fontsize=18, fontweight='bold', color='#495057')

    ax2.annotate('', xy=(0.60, 0.72), xytext=(0.42, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=2.8, mutation_scale=14))
    ax2.annotate('', xy=(0.60, 0.86), xytext=(0.60, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=2.5, mutation_scale=12))
    ax2.annotate('', xy=(0.60, 0.65), xytext=(0.60, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#868e96', lw=1.8, mutation_scale=10))
    ax2.text(0.51, 0.64, "Int Rx dt", color='#e03131', fontsize=9, fontweight='bold')
    ax2.text(0.63, 0.80, "Int Ry dt", color='#e03131', fontsize=9, fontweight='bold')
    ax2.text(0.63, 0.65, "mg dt", color='#868e96', fontsize=8)
    ax2.text(0.72, 0.70, "=", fontsize=18, fontweight='bold', color='#495057')

    ax2.annotate('', xy=(0.82 + 0.28 * np.cos(theta_rad), 0.70 + 0.28 * np.sin(theta_rad)),
                 xytext=(0.82, 0.70),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.0, mutation_scale=15))
    ax2.text(0.96, 0.82, "m v2 = 1.26 N s\n(15 deg)", color='#2b8a3e', fontsize=9, fontweight='bold')

    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.50, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.34, "Impulse-Momentum Equation (Impact Force R):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.27, f"   x: -0.060(15) + Rx(0.02) = 0.060(21 cos 15 deg)  ==>  Rx = {Rx:.1f} N", fontsize=9.2, color='#212529')
    ax2.text(-0.08, 0.20, f"   y: 0 + (Ry - mg)(0.02) = 0.060(21 sin 15 deg)   ==>  Ry = {Ry:.2f} N", fontsize=9.2, color='#212529')

    ax2.text(-0.08, 0.11, "Impulsive vs Nonimpulsive Force Comparison:", fontsize=10, fontweight='bold', color='#495057')
    ax2.text(-0.08, 0.05, f"   Ry ({Ry:.2f} N) >> Weight mg (0.589 N)  ==>  Without gravity Ry = 16.31 N", fontsize=9.0, color='#495057')

    ax2.text(-0.08, -0.04, "Theoretical Verification (100% Textbook Parity):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.08, f"   R = sqrt(Rx^2 + Ry^2) = {R:.1f} N,   beta = tan^-1(Ry/Rx) = {beta_deg:.2f} deg",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_19_tennis_ball_impulse.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
