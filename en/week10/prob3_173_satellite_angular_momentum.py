"""
Engineering Mechanics: Dynamics 9th Ed. Chapter 3 Part C (Section 3.10 Angular Impulse & Momentum)
Problem 3/173 - Magnitude of Angular Momentum H_O in x-y Plane (Vector vs Scalar Moment Arm)
- Pure white background (#ffffff) & 1:1 textbook visual parity in 2-panel layout (14 x 6.5)
- Quantitative Verification:
  * m = 2 kg, initial position r = -6i + 8j m, speed v = 7 m/s (30° left of downward vertical)
  * (a) Vector definition: H_O = r x mv = (-6i + 8j) x 2(7)(-sin 30° i - cos 30° j) = +128.7k kg·m^2/s
  * (b) Scalar moment arm: d_1 = 6 tan 30° = 3.46 m, d_2 = 8 - 3.46 = 4.54 m
        Perpendicular moment arm d = 6 / cos 30° + 4.54 sin 30° = 9.20 m
        H_O = m v d = 2(7)(9.20) = 128.7 kg·m^2/s (CCW)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m = 2.0
x0, y0 = -6.0, 8.0
v_mag = 7.0
ang_vert = np.radians(30.0)
vx = -v_mag * np.sin(ang_vert)
vy = -v_mag * np.cos(ang_vert)

d1 = 6.0 * np.tan(ang_vert)
d2 = 8.0 - d1
d_arm = 6.0 / np.cos(ang_vert) + d2 * np.sin(ang_vert)
H_O = m * v_mag * d_arm

u_line = np.array([vx, vy]) / v_mag
vec_OP0 = np.array([x0, y0])
proj_len = np.dot(vec_OP0, u_line)
foot_pt = vec_OP0 - proj_len * u_line

n_frames = 50
t_vals = np.linspace(0.0, 0.85, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    t = t_vals[frame]
    xc = x0 + vx * t
    yc = y0 + vy * t

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-10.5, 3.0)
    ax_main.set_ylim(-2.2, 10.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Problem 3/173: Planar Sphere Angular Momentum & Moment Arm (1:1 View)', fontsize=12.0, fontweight='bold', pad=10)

    ax_main.plot([-9.5, 2.2], [0, 0], color='#333333', ls='--', lw=1.4)
    ax_main.plot([0, 0], [-1.8, 9.2], color='#333333', ls='--', lw=1.4)
    ax_main.plot(0, 0, 'o', color='#111111', markersize=5.0)
    ax_main.text(2.35, -0.15, '$x$', fontsize=12, style='italic', fontweight='bold')
    ax_main.text(0.15, 9.3, '$y$', fontsize=12, style='italic', fontweight='bold')
    ax_main.text(0.25, 0.25, '$O$', fontsize=12, fontweight='bold')

    ax_main.plot([-6.0, -6.0], [0.0, 8.0], color='#333333', ls='--', lw=1.3)
    ax_main.text(-3.0, 0.28, r'$6\ \mathrm{m}$', fontsize=11, fontweight='bold', ha='center')
    ax_main.text(-5.65, 3.9, r'$8\ \mathrm{m}$', fontsize=11, fontweight='bold', ha='left')

    line_s = np.linspace(-1.0, 11.5, 50)
    ax_main.plot(x0 + u_line[0]*line_s, y0 + u_line[1]*line_s, color='#adb5bd', ls=':', lw=1.5, zorder=2)

    ax_main.plot([0, foot_pt[0]], [0, foot_pt[1]], color='#6a1b9a', ls='-.', lw=1.8, zorder=3)
    u_arm = foot_pt / np.linalg.norm(foot_pt)
    sq_size = 0.42
    sq_pts = np.array([
        foot_pt - u_arm * sq_size,
        foot_pt - u_arm * sq_size + u_line * sq_size,
        foot_pt + u_line * sq_size
    ])
    ax_main.plot(sq_pts[:, 0], sq_pts[:, 1], color='#6a1b9a', lw=1.3, zorder=3)
    ax_main.text(foot_pt[0]*0.55 - 1.15, foot_pt[1]*0.55 - 0.65, r'$d = 9.20\ \mathrm{m}$',
                 color='#6a1b9a', fontsize=10.2, fontweight='bold', rotation=-30)

    arc_ang = np.linspace(-np.pi/2 - ang_vert, -np.pi/2, 25)
    ax_main.plot(x0 + 2.3 * np.cos(arc_ang), y0 + 2.3 * np.sin(arc_ang), color='#222222', lw=1.2)
    ax_main.text(x0 - 0.72, y0 - 2.15, r'$30^\circ$', fontsize=10.5, fontweight='bold')

    if t > 0.02:
        ghost = patches.Circle((x0, y0), 0.38, facecolor='#f5dcd0', edgecolor='#8d6e63', ls='--', lw=1.2, alpha=0.55, zorder=4)
        ax_main.add_patch(ghost)

    ax_main.annotate('', xy=(xc, yc), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#1f618d', lw=1.6, ls=':', mutation_scale=13), zorder=4)
    ax_main.text(xc*0.48 + 0.35, yc*0.48 + 0.25, r'$\mathbf{r}$', color='#1f618d', fontsize=11, fontweight='bold')

    sphere = patches.Circle((xc, yc), 0.38, facecolor='#d99b82', edgecolor='#4a2c20', lw=1.6, zorder=6)
    hi = patches.Circle((xc - 0.12, yc + 0.12), 0.13, facecolor='#fae5dc', edgecolor='none', zorder=7)
    ax_main.add_patch(sphere)
    ax_main.add_patch(hi)
    ax_main.text(x0, y0 + 0.65, r'$2\ \mathrm{kg}$', fontsize=11, fontweight='bold', ha='center')

    v_len = 2.6
    ax_main.annotate('', xy=(xc + u_line[0]*v_len, yc + u_line[1]*v_len), xytext=(xc, yc),
                     arrowprops=dict(arrowstyle='-|>', color='#00897b', lw=2.5, mutation_scale=15), zorder=7)
    ax_main.text(xc + u_line[0]*v_len - 1.05, yc + u_line[1]*v_len + 0.15,
                 r'$7\ \mathrm{m/s}$', color='#00897b', fontsize=11, fontweight='bold')

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('Vector vs. Scalar Moment Arm Validation', fontsize=12.0, fontweight='bold', pad=10)

    top_card = (
        "[ Method (a): Vector Cross-Product Definition ]\n"
        r"• Position & Velocity: $\mathbf{r} = -6\mathbf{i} + 8\mathbf{j}\ \mathrm{m},\ \mathbf{v} = 7(-\sin 30^\circ\mathbf{i} - \cos 30^\circ\mathbf{j})\ \mathrm{m/s}$" + "\n"
        r"• $\mathbf{H}_O = \mathbf{r} \times m\mathbf{v} = (-6\mathbf{i} + 8\mathbf{j}) \times 2(7)(-0.5\mathbf{i} - 0.866\mathbf{j})$" + "\n"
        r"• $\mathbf{H}_O = \mathbf{+128.7\mathbf{k}\ \mathrm{kg\cdot m^2/s}} \Rightarrow H_O = \mathbf{128.7\ \mathrm{kg\cdot m^2/s}}$"
    )
    ax_calc.text(0.35, 8.35, top_card, fontsize=9.2, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "[ Method (b): Equivalent Scalar Moment-Arm Approach ]\n"
        r"1) Vertical intercept segments ($d_1, d_2$):" + "\n"
        r"   $d_1 = 6\tan 30^\circ = 3.46\ \mathrm{m},\quad d_2 = 8 - d_1 = 4.54\ \mathrm{m}$" + "\n\n"
        r"2) Perpendicular moment arm $d$ from $O$ to line of action:" + "\n"
        r"   $d = \frac{6}{\cos 30^\circ} + 4.54\sin 30^\circ = 6.93 + 2.27 = \mathbf{9.20\ \mathrm{m}}$" + "\n\n"
        r"3) Magnitude of angular momentum (CCW $+$):" + "\n"
        r"   $H_O = m v d = 2(7)(9.20) = \mathbf{128.7\ \mathrm{kg\cdot m^2/s}}$"
    )
    ax_calc.text(0.35, 4.7, sol_text, fontsize=9.3, va='center', ha='left', linespacing=1.35,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    H_inst = xc * (m * vy) - yc * (m * vx)
    live_text = (
        "[ Live Invariance Along Line of Action ]\n"
        rf"• Current coordinates: $\mathbf{{r}}(t) = ({xc:.2f}\mathbf{{i}} + {yc:.2f}\mathbf{{j}})\ \mathrm{{m}}$" + "\n"
        rf"• Instantaneous cross product: $x(mv_y) - y(mv_x) = +{H_inst:.1f}\ \mathrm{{kg\cdot m^2/s}}$" + "\n"
        r"• Theoretical Value: $H_O = 128.7\ \mathrm{kg\cdot m^2/s}$ ($d = 9.20\ \mathrm{m}$ constant)"
    )
    ax_calc.text(0.35, 1.3, live_text, fontsize=9.1, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_173_satellite_angular_momentum.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
