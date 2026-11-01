# Problem 2/131: Baseball Throw and Radar Kinematics in Polar Coordinates (r-θ)
# Real-time trajectory, unit vectors (e_r, e_theta), velocity/acceleration vectors, homework hints and exact answers

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# Parameters
v0 = 35.0
th0_deg = 30.0
th0 = np.radians(th0_deg)
g = 9.81

t_target = 0.5
t_total = 0.55
frames = 110
t_arr = np.linspace(0.01, t_total, frames)

vx0 = v0 * np.cos(th0)
vy0 = v0 * np.sin(th0)

x_arr = vx0 * t_arr
y_arr = vy0 * t_arr - 0.5 * g * (t_arr**2)

vx_arr = np.full_like(t_arr, vx0)
vy_arr = vy0 - g * t_arr
v_mag_arr = np.sqrt(vx_arr**2 + vy_arr**2)

r_arr = np.sqrt(x_arr**2 + y_arr**2)
th_arr = np.arctan2(y_arr, x_arr)

vr_arr = vx_arr * np.cos(th_arr) + vy_arr * np.sin(th_arr)
vth_arr = -vx_arr * np.sin(th_arr) + vy_arr * np.cos(th_arr)

r_dot_arr = vr_arr
th_dot_arr = vth_arr / r_arr

ar_arr = -g * np.sin(th_arr)
ath_arr = -g * np.cos(th_arr)

r_ddot_arr = ar_arr + r_arr * (th_dot_arr**2)
th_ddot_arr = (ath_arr - 2.0 * r_dot_arr * th_dot_arr) / r_arr

fig, ax = plt.subplots(figsize=(12.8, 7.5))
fig.subplots_adjust(left=0.04, right=0.65, bottom=0.06, top=0.94)
ax.set_facecolor('#ebf5fb')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-2.0, 20.0)
ax.set_ylim(-1.5, 11.5)

bg_box = patches.Rectangle((-1.5, -1.0), 21.0, 12.0, facecolor='#ebf5fb', edgecolor='#85929e', lw=1.5, zorder=0)
ax.add_patch(bg_box)

ax.plot([-1.0, 19.0], [0, 0], 'k-', lw=1.5, zorder=2)
ax.plot([0, 0], [-0.5, 10.5], 'k--', lw=1.0, alpha=0.6, zorder=2)
ax.plot([-0.5, 18.5], [0, 0], 'k--', lw=1.0, alpha=0.6, zorder=2)

ax.text(18.8, 0, '$x$', fontsize=14, fontfamily='serif', fontstyle='italic', va='center', ha='left')
ax.text(0, 10.7, '$y$', fontsize=14, fontfamily='serif', fontstyle='italic', va='bottom', ha='center')

ax.plot(0, 0, 'ko', markersize=6, zorder=5)
ax.text(-0.5, -0.6, '$O$', fontsize=14, fontfamily='serif', fontweight='bold', ha='right', va='top')

ax.plot([0, 12 * np.cos(th0)], [0, 12 * np.sin(th0)], color='#7f8c8d', ls=':', lw=1.2, zorder=1)
arc_th0 = patches.Arc((0, 0), 5.0, 5.0, angle=0, theta1=0, theta2=th0_deg, color='#e67e22', lw=1.5, zorder=2)
ax.add_patch(arc_th0)
ax.text(3.0 * np.cos(np.radians(15)), 3.0 * np.sin(np.radians(15)), r'$30^\circ$', color='#e67e22', fontsize=11, fontweight='bold', ha='center', va='center')

ax.plot(x_arr, y_arr, color='#2980b9', ls='--', lw=1.5, alpha=0.7, zorder=2)

ball = patches.Circle((0, 0), 0.35, facecolor='white', edgecolor='#2c3e50', lw=1.5, zorder=10)
ax.add_patch(ball)

line_r, = ax.plot([], [], color='#e67e22', lw=2.0, ls='-', zorder=3)
txt_r_label = ax.text(0, 0, '', color='#d35400', fontsize=11, fontweight='bold', ha='center', va='center',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=1))

arc_theta = patches.Arc((0, 0), 6.0, 6.0, angle=0, theta1=0, theta2=0, color='#2980b9', lw=1.8, zorder=3)
ax.add_patch(arc_theta)
txt_theta_label = ax.text(0, 0, r'$\theta$', color='#2980b9', fontsize=12, fontweight='bold', ha='center', va='center')

arr_er = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=3,head_length=6', color='#2c3e50', lw=1.5, zorder=6)
arr_eth = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=3,head_length=6', color='#2c3e50', lw=1.5, zorder=6)
ax.add_patch(arr_er)
ax.add_patch(arr_eth)
txt_er = ax.text(0, 0, r'$\mathbf{e}_r$', color='#2c3e50', fontsize=11, fontweight='bold', ha='center', va='center')
txt_eth = ax.text(0, 0, r'$\mathbf{e}_\theta$', color='#2c3e50', fontsize=11, fontweight='bold', ha='center', va='center')

arr_v = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=4,head_length=8', color='#27ae60', lw=2.4, zorder=8)
ax.add_patch(arr_v)
txt_v = ax.text(0, 0, r'$\mathbf{v}$', color='#27ae60', fontsize=12, fontweight='bold')

arr_a = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=4,head_length=8', color='#c0392b', lw=2.4, zorder=8)
ax.add_patch(arr_a)
txt_a = ax.text(0, 0, r'$\mathbf{a} = -g\mathbf{j}$', color='#c0392b', fontsize=11, fontweight='bold')

info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    t_curr = t_arr[i]
    x_curr = x_arr[i]
    y_curr = y_arr[i]
    r_curr = r_arr[i]
    th_curr = th_arr[i]

    ball.center = (x_curr, y_curr)

    line_r.set_data([0, x_curr], [0, y_curr])
    txt_r_label.set_position((0.5 * x_curr - 0.4 * np.sin(th_curr), 0.5 * y_curr + 0.4 * np.cos(th_curr)))
    txt_r_label.set_text(f'$r = {r_curr:.2f}$ m')

    arc_theta.theta2 = np.degrees(th_curr)
    th_mid = th_curr / 2.0
    txt_theta_label.set_position((3.5 * np.cos(th_mid), 3.5 * np.sin(th_mid)))
    txt_theta_label.set_text(f'$\\theta = {np.degrees(th_curr):.1f}^\\circ$')

    er = np.array([np.cos(th_curr), np.sin(th_curr)])
    eth = np.array([-np.sin(th_curr), np.cos(th_curr)])
    u_len = 1.6

    arr_er.set_positions((x_curr, y_curr), (x_curr + u_len * er[0], y_curr + u_len * er[1]))
    arr_eth.set_positions((x_curr, y_curr), (x_curr + u_len * eth[0], y_curr + u_len * eth[1]))
    txt_er.set_position((x_curr + (u_len + 0.3) * er[0], y_curr + (u_len + 0.3) * er[1]))
    txt_eth.set_position((x_curr + (u_len + 0.3) * eth[0], y_curr + (u_len + 0.3) * eth[1]))

    v_scale = 0.10
    v_vec = np.array([vx_arr[i], vy_arr[i]])
    arr_v.set_positions((x_curr, y_curr), (x_curr + v_vec[0] * v_scale, y_curr + v_vec[1] * v_scale))
    txt_v.set_position((x_curr + v_vec[0] * v_scale + 0.2, y_curr + v_vec[1] * v_scale + 0.2))

    a_scale = 0.20
    a_vec = np.array([0, -g])
    arr_a.set_positions((x_curr, y_curr), (x_curr + a_vec[0] * a_scale, y_curr + a_vec[1] * a_scale))
    txt_a.set_position((x_curr + 0.3, y_curr - g * a_scale))

    is_final = (i == frames - 1)
    status_hdr = "★ [Homework Task & Exact Answers (t = 0.5 s)] ★" if is_final else "■ [Problem 2/131: Baseball Throw Polar Kinematics]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【Initial Conditions】\n"
        f" • Speed: $v_0 = {v0:.0f}$ m/s, Angle: $\\theta_0 = {th0_deg:.0f}^\\circ$\n"
        f" • Gravity: $g = {g:.2f}$ m/s² (downward)\n"
        f" • Target time: $t = 0.5$ s\n"
        f"─────────────────────────────────────\n"
        f"【Real-time Kinematic Monitoring】\n"
        f" • Time $t = {t_curr:.3f}$ s ($x = {x_curr:.2f}$ m, $y = {y_curr:.2f}$ m)\n"
        f" • Speed $|\\mathbf{{v}}| = {v_mag_arr[i]:.2f}$ m/s (Green)\n"
        f" • Accel $|\\mathbf{{a}}| = {g:.2f}$ m/s² (Red)\n"
        f"─────────────────────────────────────\n"
        f"▶ [Key Hints]\n"
        f" • $x = v_0\\cos\\theta_0 t,\\ y = v_0\\sin\\theta_0 t - \\frac{{1}}{{2}}gt^2$\n"
        f" • $r = \\sqrt{{x^2+y^2}},\\ \\theta = \\arctan(y/x)$\n"
        f" • $\\dot{{r}} = \\dot{{x}}\\cos\\theta + \\dot{{y}}\\sin\\theta$\n"
        f"   $r\\dot{{\\theta}} = -\\dot{{x}}\\sin\\theta + \\dot{{y}}\\cos\\theta$\n"
        f" • $\\ddot{{r}} - r\\dot{{\\theta}}^2 = -g\\sin\\theta$\n"
        f"   $r\\ddot{{\\theta}} + 2\\dot{{r}}\\dot{{\\theta}} = -g\\cos\\theta$\n"
        f"─────────────────────────────────────\n"
        f"★ [Exact Answers at $t = 0.5$ s]\n"
        f" (1) Radius: $r = 16.59$ m\n"
        f" (2) Radial speed: $\\dot{{r}} = 34.33$ m/s\n"
        f" (3) Radial accel: $\\ddot{{r}} = -2.85$ m/s²\n"
        f" (4) Angle: $\\theta = 23.4^\\circ$ ($0.408$ rad)\n"
        f" (5) Angular speed: $\\dot{{\\theta}} = -0.409$ rad/s\n"
        f" (6) Angular accel: $\\ddot{{\\theta}} = 1.144$ rad/s²"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)
    gif_path = Path(__file__).parent / 'prob2_131_baseball_throw.gif'
    writer = PillowWriter(fps=28)
    writer._kwargs = {'loop': None}
    ani.save(str(gif_path), writer=writer)
