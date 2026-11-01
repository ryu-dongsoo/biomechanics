"""
Engineering Mechanics: Dynamics 9th Ed. Chapter 3 Part C (Section 3.10 Angular Impulse & Momentum)
Problem 3/192 - Particle Sliding Down a Frictionless Funnel-Shaped Surface
- Pure white background (#ffffff) & 1:1 textbook visual parity in 2-panel layout (14 x 6.5)
- Quantitative Verification:
  * r = 0.9 m, v_0 = 0.55 m/s (released horizontally at 30° position)
  * State 1 (30° position) radius from axis: R_1 = 0.15r + (r - r sin 30°) = 0.65r = 0.585 m
  * State 2 (level O-O) radius from axis: R_2 = 0.15r = 0.135 m
  * Vertical drop: h = r cos 30° = 0.9 cos 30° = 0.7794 m
  * Work-Energy: 1/2 m v_0^2 + m g r cos 30° = 1/2 m v_2^2 => v_2 = 3.95 m/s
  * Angular momentum about vertical axis: H_1 = H_2 => m v_0 (0.65r) = m v_2 cos(theta) (0.15r) => theta = 52.9°
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

g = 9.81
r = 0.90
v0 = 0.55
alpha0 = np.radians(30.0)

R1 = 0.15 * r + r * (1.0 - np.sin(alpha0))
R2 = 0.15 * r
h_drop = r * np.cos(alpha0)

v2 = np.sqrt(v0**2 + 2.0 * g * h_drop)
cos_theta2 = (v0 * R1) / (v2 * R2)
theta2_deg = np.degrees(np.arccos(cos_theta2))

n_frames = 55
alpha_vals = np.linspace(np.radians(30.0), np.radians(90.0), n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    alp = alpha_vals[frame]
    R_curr = 1.15 * r - r * np.sin(alp)
    z_curr = r * np.cos(alp)
    drop_curr = r * np.cos(alpha0) - z_curr

    v_curr = np.sqrt(v0**2 + 2.0 * g * max(drop_curr, 0.0))
    v_horiz = v0 * (R1 / R_curr)
    cos_th = min(v_horiz / v_curr, 1.0)
    th_curr_deg = np.degrees(np.arccos(cos_th))

    phi_spiral = 0.4 + 3.2 * np.pi * ((alp - alpha0) / (np.pi/2 - alpha0))**1.35

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.35, 1.35)
    ax_main.set_ylim(-0.38, 1.22)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/192: Particle Helical Trajectory in Funnel (1:1 View)', fontsize=12.0, fontweight='bold', pad=10)

    ang_arc = np.linspace(0, np.pi/2, 80)
    x_right_in = 1.15 * r - r * np.sin(ang_arc)
    y_right_in = r * np.cos(ang_arc)
    x_left_in = -(1.15 * r - r * np.sin(ang_arc))

    wall_t = 0.075
    x_right_out = 1.15 * r - (r - wall_t) * np.sin(ang_arc)
    y_right_out = (r - wall_t) * np.cos(ang_arc)

    ax_main.fill_betweenx(y_right_in, x_left_in, x_right_in, color='#d4ebf8', alpha=0.65, zorder=1)
    ax_main.fill_between([-R2, R2], -0.18, 0.0, color='#d4ebf8', alpha=0.65, zorder=1)

    right_wall_x = np.concatenate([[1.15*r], x_right_in, [R2, R2 + wall_t], x_right_out[::-1], [1.15*r + wall_t, 1.15*r]])
    right_wall_y = np.concatenate([[r + 0.12], y_right_in, [-0.18, -0.18], y_right_out[::-1], [r + 0.12, r + 0.12]])
    ax_main.fill(right_wall_x, right_wall_y, facecolor='#e9ecef', edgecolor='#222222', lw=1.4, hatch='///', zorder=3)

    left_wall_x = -right_wall_x
    left_wall_y = right_wall_y
    ax_main.fill(left_wall_x, left_wall_y, facecolor='#e9ecef', edgecolor='#222222', lw=1.4, hatch='///', zorder=3)

    ax_main.plot([-1.15*r - wall_t, 1.15*r + wall_t], [r + 0.12, r + 0.12], color='#222222', lw=1.5, zorder=3)
    ax_main.plot([-1.15*r, 1.15*r], [r, r], color='#5c9ce6', lw=1.2, zorder=2)

    ax_main.plot([0, 0], [-0.28, 1.16], color='#222222', ls='-.', lw=1.2, zorder=4)

    x_O = 1.15 * r
    ax_main.plot([-x_O, -R2], [0, 0], color='#444444', lw=1.0)
    ax_main.plot([R2, x_O], [0, 0], color='#444444', lw=1.0)
    ax_main.plot([-x_O, -x_O], [0, r], color='#444444', lw=1.0)
    ax_main.plot([x_O, x_O], [0, r], color='#444444', lw=1.0)
    ax_main.plot(-x_O, 0, '+', color='#111111', markersize=8, markeredgewidth=1.4)
    ax_main.plot(x_O, 0, '+', color='#111111', markersize=8, markeredgewidth=1.4)
    ax_main.text(-x_O - 0.08, -0.11, '$O$', fontsize=12, fontweight='bold', ha='center')
    ax_main.text(x_O + 0.08, -0.11, '$O$', fontsize=12, fontweight='bold', ha='center')

    ang_r_lbl = np.radians(42.0)
    ax_main.annotate('', xy=(-x_O + r*np.sin(ang_r_lbl), r*np.cos(ang_r_lbl)), xytext=(-x_O, 0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.2), zorder=4)
    ax_main.text(-x_O + 0.25, 0.30, '$r$', fontsize=11.5, style='italic', fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.1', facecolor='#ffffff', edgecolor='none'))

    x_init = x_O - r * np.sin(alpha0)
    y_init = r * np.cos(alpha0)
    ax_main.plot([x_O, x_init], [0, y_init], color='#333333', lw=1.1, zorder=4)
    arc30 = np.linspace(np.pi/2, np.pi/2 + alpha0, 20)
    ax_main.plot(x_O + 0.42 * np.cos(arc30), 0.42 * np.sin(arc30), color='#222222', lw=1.1)
    ax_main.text(x_O - 0.16, 0.46, r'$30^\circ$', fontsize=10.5, fontweight='bold')

    ax_main.plot([-R2, -R2], [-0.18, -0.30], color='#333333', lw=1.0)
    ax_main.annotate('', xy=(0, -0.25), xytext=(0.22, -0.25), arrowprops=dict(arrowstyle='<-', color='#222222', lw=1.1))
    ax_main.annotate('', xy=(-R2, -0.25), xytext=(-0.38, -0.25), arrowprops=dict(arrowstyle='->', color='#222222', lw=1.1))
    ax_main.text(-0.52, -0.28, r'$0.15r$', fontsize=10.5, fontweight='bold')

    alp_traj = np.linspace(alpha0, np.pi/2, 160)
    R_traj = 1.15 * r - r * np.sin(alp_traj)
    z_traj = r * np.cos(alp_traj)
    phi_traj = 0.4 + 3.2 * np.pi * ((alp_traj - alpha0) / (np.pi/2 - alpha0))**1.35
    x_sp = R_traj * np.cos(phi_traj)
    y_sp = z_traj - 0.08 * R_traj * np.sin(phi_traj)
    ax_main.plot(x_sp, y_sp, color='#e67e22', ls='--', lw=1.8, zorder=4)

    ax_main.plot(x_init, y_init, 'o', color='#e74c3c', markersize=7.5, markeredgecolor='#641e16', zorder=5)
    ax_main.text(x_init - 0.02, y_init + 0.07, '$m$', fontsize=11, style='italic', fontweight='bold')
    ax_main.annotate('', xy=(x_init - 0.28, y_init + 0.04), xytext=(x_init, y_init),
                     arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=6)
    ax_main.text(x_init - 0.22, y_init + 0.08, '$v_0$', color='#2e7d32', fontsize=10.5, fontweight='bold')

    px_curr = R_curr * np.cos(phi_spiral)
    py_curr = z_curr - 0.08 * R_curr * np.sin(phi_spiral)
    ball_curr = patches.Circle((px_curr, py_curr), 0.038, facecolor='#e74c3c', edgecolor='#641e16', lw=1.5, zorder=8)
    ax_main.add_patch(ball_curr)

    ball_sec = patches.Circle((R_curr, z_curr), 0.035, facecolor='#e74c3c', edgecolor='#641e16', lw=1.3, alpha=0.85, zorder=7)
    ax_main.add_patch(ball_sec)

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('Coupled Funnel Angular Momentum & Energy Validation', fontsize=12.0, fontweight='bold', pad=10)

    top_card = (
        "[ Radii from Vertical Axis at State 1 & State 2 ]\n"
        r"• State 1 ($30^\circ$ release): $R_1 = 0.15r + (r - r\sin 30^\circ) = 0.65r = 0.585\ \mathrm{m}$" + "\n"
        r"• State 2 (level $O$-$O$): $R_2 = 0.15r = 0.135\ \mathrm{m}$" + "\n"
        r"• Vertical drop: $h = r\cos 30^\circ = 0.9\cos 30^\circ = 0.7794\ \mathrm{m}$"
    )
    ax_calc.text(0.35, 8.45, top_card, fontsize=9.2, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "[ Theoretical Derivation & Analysis (Section 3.10) ]\n"
        r"1) Angular momentum about vertical axis ($H_1 = H_2$):" + "\n"
        r"   $m v_0 [0.15r + (r - r\sin 30^\circ)] = m (v_2 \cos\theta)[0.15r] \quad \cdots (1)$" + "\n\n"
        r"2) Work-Energy equation ($T_1 + U_{1-2} = T_2$):" + "\n"
        r"   $\frac{1}{2}m v_0^2 + m g r\cos 30^\circ = \frac{1}{2}m v_2^2 \Rightarrow \mathbf{v_2 = 3.95\ \mathrm{m/s}} \quad \cdots (2)$" + "\n\n"
        r"3) Substitute $v_0 = 0.55\ \mathrm{m/s},\ v_2 = 3.95\ \mathrm{m/s}$ into (1):" + "\n"
        r"   $\cos\theta = \frac{0.55(0.65)}{3.95(0.15)} = 0.6035 \Rightarrow \mathbf{\theta = 52.9^\circ}$"
    )
    ax_calc.text(0.35, 4.7, sol_text, fontsize=9.2, va='center', ha='left', linespacing=1.35,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        rf"[ Live Funnel Trajectory Monitor (Angle $\alpha = {np.degrees(alp):.1f}^\circ$) ]" + "\n"
        rf"• Current axis radius: $R = {R_curr:.3f}\ \mathrm{{m}}$  |  Current speed: $v = {v_curr:.2f}\ \mathrm{{m/s}}$" + "\n"
        rf"• Velocity angle below horizontal: $\theta = {th_curr_deg:.1f}^\circ$" + "\n"
        r"• Theoretical Value (at level $O$-$O$): $v_2 = 3.95\ \mathrm{m/s}$,  angle $\theta = 52.9^\circ$"
    )
    ax_calc.text(0.35, 1.25, live_text, fontsize=9.1, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_192_slotted_disk_slider.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
