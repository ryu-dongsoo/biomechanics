"""
Engineering Mechanics: Dynamics 9th Ed. Chapter 3 Part C (Section 3.10 Angular Impulse & Momentum)
Sample Problem 3.26 - Pivoted Rod-Mass Assembly Struck by Falling Putty
- Pure white background (#ffffff) & 1:1 textbook visual parity in 2-panel layout (14 x 6.5)
- Quantitative Verification:
  * Left mass 4m (at 2l), Right mass 2m (at l), Falling putty m (velocity v_1)
  * Conservation of system angular momentum about pivot O: (H_O)_1 = (H_O)_2
  * m v_1 l = (m + 2m)(l * omega_2) l + 4m (2l * omega_2)(2l) = 19 m l^2 omega_2
  * omega_2 = theta_dot_2 = v_1 / (19 l) (CW)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

l_val = 1.0
v1_val = 9.5
omega2_val = v1_val / (19.0 * l_val)

n_frames = 54
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.65, 1.85)
    ax_main.set_ylim(-1.45, 1.55)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Sample Problem 3.26: Pivoted Bar Assembly & Putty Impact (1:1 View)', fontsize=12.0, fontweight='bold', pad=10)

    base_y = -0.45
    ax_main.fill_between([-0.42, 0.42], base_y - 0.14, base_y, color='#d5cbb8', alpha=0.8, zorder=1)
    ax_main.plot([-0.42, 0.42], [base_y, base_y], color='#333333', lw=2.0, zorder=2)
    bracket = patches.Polygon([[-0.22, base_y], [0.22, base_y], [0.09, 0.0], [-0.09, 0.0]],
                              facecolor='#b0c4de', edgecolor='#2b2b2b', lw=1.6, zorder=3)
    ax_main.add_patch(bracket)

    if frame < 20:
        theta_cw = 0.0
        putty_y = 0.95 - (frame / 20.0) * 0.72
        phase_str = r"Pre-impact: Putty ($m$) falling vertically at speed $v_1$"
        phase_col = '#1971c2'
    elif frame < 25:
        theta_cw = 0.0
        putty_y = 0.18
        phase_str = r"Impact: Putty adheres to right mass ($2m$)!"
        phase_col = '#d32f2f'
    else:
        dt_rot = (frame - 24) / 29.0
        theta_cw = dt_rot * 0.52
        putty_y = 0.18
        phase_str = r"Post-impact: Clockwise rotation ($\dot{\theta}_2 = v_1 / 19l\ \mathrm{CW}$)"
        phase_col = '#2e7d32'

    ang = -theta_cw
    t_rot = patches.transforms.Affine2D().rotate(ang) + ax_main.transData

    rod_rect = patches.Rectangle((-2.0, -0.035), 3.0, 0.07, facecolor='#d99b66', edgecolor='#5c3a21', lw=1.5, zorder=4)
    rod_rect.set_transform(t_rot)
    ax_main.add_patch(rod_rect)

    m4_rect = patches.Rectangle((-2.22, -0.22), 0.44, 0.44, facecolor='#a9cce3', edgecolor='#1f618d', lw=1.6, zorder=5)
    m4_rect.set_transform(t_rot)
    ax_main.add_patch(m4_rect)
    p_left = np.array([-2.0 * np.cos(ang), -2.0 * np.sin(ang)])
    ax_main.text(p_left[0], p_left[1], '$4m$', fontsize=11, fontweight='bold', ha='center', va='center', zorder=6)

    m2_rect = patches.Rectangle((0.82, -0.16), 0.36, 0.32, facecolor='#a9cce3', edgecolor='#1f618d', lw=1.6, zorder=5)
    m2_rect.set_transform(t_rot)
    ax_main.add_patch(m2_rect)
    p_right = np.array([1.0 * np.cos(ang), 1.0 * np.sin(ang)])
    ax_main.text(p_right[0], p_right[1], '$2m$', fontsize=11, fontweight='bold', ha='center', va='center', zorder=6)

    pin_outer = patches.Circle((0, 0), 0.085, facecolor='#b0c4de', edgecolor='#222222', lw=1.5, zorder=7)
    pin_inner = patches.Circle((0, 0), 0.038, facecolor='#ffffff', edgecolor='#222222', lw=1.2, zorder=8)
    ax_main.add_patch(pin_outer)
    ax_main.add_patch(pin_inner)
    ax_main.text(0.0, 0.16, '$O$', fontsize=12, fontweight='bold', ha='center', zorder=8)

    if frame < 20:
        px_c, py_c = 1.0, putty_y
        putty_blob = patches.Ellipse((px_c, py_c), 0.28, 0.20, angle=-10,
                                     facecolor='#d96b6b', edgecolor='#641e16', lw=1.5, zorder=6)
        ax_main.add_patch(putty_blob)
        ax_main.text(px_c + 0.05, py_c + 0.18, '$m$', fontsize=11, fontweight='bold')
        ax_main.annotate('', xy=(1.08, py_c - 0.38), xytext=(1.08, py_c - 0.05),
                         arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=7)
        ax_main.text(1.24, py_c - 0.22, '$v_1$', color='#2e7d32', fontsize=11, fontweight='bold')
    else:
        putty_attached = patches.Ellipse((1.0, 0.19), 0.32, 0.14,
                                         facecolor='#d96b6b', edgecolor='#641e16', lw=1.5, zorder=6)
        putty_attached.set_transform(t_rot)
        ax_main.add_patch(putty_attached)
        p_putty = np.array([1.0 * np.cos(ang) - 0.32 * np.sin(ang), 1.0 * np.sin(ang) + 0.32 * np.cos(ang)])
        ax_main.text(p_putty[0] + 0.12, p_putty[1], '$m$', fontsize=10.5, fontweight='bold', color='#641e16', zorder=7)

        if frame >= 25:
            arc_t = np.linspace(0.3, -0.5, 25)
            ax_main.plot(0.45 * np.cos(arc_t), 0.45 * np.sin(arc_t), color='#2e7d32', lw=2.0)
            ax_main.annotate('', xy=(0.45 * np.cos(-0.55), 0.45 * np.sin(-0.55)),
                             xytext=(0.45 * np.cos(-0.40), 0.45 * np.sin(-0.40)),
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12))
            ax_main.text(0.42, -0.45, r'$\dot{\theta}_2 = \frac{v_1}{19l}$', color='#2e7d32', fontsize=10.5, fontweight='bold')

            t_vec_r = np.array([np.sin(theta_cw), -np.cos(theta_cw)]) * 0.38
            ax_main.annotate('', xy=p_right + t_vec_r, xytext=p_right,
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=7)
            t_vec_l = np.array([-np.sin(theta_cw), np.cos(theta_cw)]) * 0.65
            ax_main.annotate('', xy=p_left + t_vec_l, xytext=p_left,
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=7)

    y_dim = -0.95
    ax_main.plot([-2.0, -2.0], [-0.25, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.plot([0.0, 0.0], [-0.48, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.plot([1.0, 1.0], [-0.25, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.annotate('', xy=(-2.0, y_dim), xytext=(0.0, y_dim), arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
    ax_main.annotate('', xy=(0.0, y_dim), xytext=(1.0, y_dim), arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
    ax_main.text(-1.0, y_dim, '$2l$', ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='#ffffff', edgecolor='none'))
    ax_main.text(0.5, y_dim, '$l$', ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='#ffffff', edgecolor='none'))

    ax_main.text(-0.4, 1.32, phase_str, fontsize=10.0, fontweight='bold', color=phase_col, ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8f9fa', edgecolor=phase_col, lw=1.3))

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('Pivot Angular Momentum Conservation & Validation', fontsize=12.0, fontweight='bold', pad=10)

    top_card = (
        "[ Conservation of Angular Momentum about Pivot $O$ ]\n"
        r"• Pivot reaction $\mathbf{R}_O$ passes through $O \Rightarrow$ zero moment arm ($d = 0$)" + "\n"
        r"• Gravity impulse ($mg\Delta t$) during short impact is negligible" + "\n"
        r"• Total angular momentum about $O$ is conserved: $(H_O)_1 = (H_O)_2$"
    )
    ax_calc.text(0.4, 8.45, top_card, fontsize=9.3, va='center', ha='left', linespacing=1.4,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "[ Theoretical Derivation & Analysis (CW Positive) ]\n"
        r"1) Initial angular momentum $(H_O)_1$:" + "\n"
        r"   $(H_O)_1 = m v_1 l$" + "\n\n"
        r"2) Final angular momentum $(H_O)_2$ ($v_{\mathrm{right}} = l\dot{\theta}_2,\ v_{\mathrm{left}} = 2l\dot{\theta}_2$):" + "\n"
        r"   $(H_O)_2 = (m + 2m)(l\dot{\theta}_2)l + 4m(2l\dot{\theta}_2)(2l)$" + "\n"
        r"   $(H_O)_2 = 3m l^2 \dot{\theta}_2 + 16m l^2 \dot{\theta}_2 = 19m l^2 \dot{\theta}_2$" + "\n\n"
        r"3) Final angular velocity: $m v_1 l = 19m l^2 \dot{\theta}_2 \Rightarrow \mathbf{\dot{\theta}_2 = \frac{v_1}{19l}\ \mathrm{CW}}$"
    )
    ax_calc.text(0.4, 4.85, sol_text, fontsize=9.4, va='center', ha='left', linespacing=1.36,
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        "[ Angular Momentum Partition & Energy Ratio ]\n"
        r"• Right mass ($3m$ at $l$) share: $3 m l^2 \dot{\theta}_2$ ($3/19 = 15.8\%$)" + "\n"
        r"• Left mass ($4m$ at $2l$) share: $16 m l^2 \dot{\theta}_2$ ($16/19 = 84.2\%$)" + "\n"
        r"• Theoretical Value: $\dot{\theta}_2 = \frac{v_1}{19l}\ \mathrm{CW}$  (Energy ratio $T_2/T_1 = \frac{1}{19} = 5.26\%$)"
    )
    ax_calc.text(0.4, 1.35, live_text, fontsize=9.2, va='center', ha='left', linespacing=1.4,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_26_rotating_T_bar_spheres.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
