"""
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
문제 3/175 - 평면 운동 3 kg 구의 선형운동량 G, 각운동량 H_O 및 운동에너지 T
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * m = 3 kg, r = 2 m (x축 아래 15°), v = 5 m/s (반경선 기준 45° -> -x축 아래 30°)
  * (a) 선형운동량: G = m v = 3(5)(-cos 30° i - sin 30° j) = -12.99i - 7.50j kg·m/s
  * (b) 각운동량: H_O = r x G = 2(cos 15° i - sin 15° j) x (-12.99i - 7.50j) = -21.2k kg·m^2/s
  * (c) 운동에너지: T = 1/2 m v^2 = 1/2 (3)(5^2) = 37.5 J
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m = 3.0
r_mag = 2.0
ang_r = np.radians(-15.0)
x0 = r_mag * np.cos(ang_r)
y0 = r_mag * np.sin(ang_r)

v_mag = 5.0
ang_v = np.radians(-150.0)
vx = v_mag * np.cos(ang_v)
vy = v_mag * np.sin(ang_v)

Gx, Gy = m * vx, m * vy
H_z = x0 * Gy - y0 * Gx
T_val = 0.5 * m * v_mag**2

n_frames = 50
t_vals = np.linspace(0.0, 0.28, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    t = t_vals[frame]
    xc = x0 + vx * t
    yc = y0 + vy * t

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.85, 2.75)
    ax_main.set_ylim(-1.85, 0.95)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/175: 3 kg 구의 선운동량·각운동량·운동에너지 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    ax_main.plot([-0.65, 2.35], [0, 0], color='#333333', ls='--', lw=1.4)
    ax_main.plot([0, 0], [-1.55, 0.78], color='#333333', ls='--', lw=1.4)
    ax_main.plot(0, 0, 'o', color='#111111', markersize=5.5)
    ax_main.text(2.42, -0.04, '$x$', fontsize=12, style='italic', fontweight='bold')
    ax_main.text(-0.03, 0.82, '$y$', fontsize=12, style='italic', fontweight='bold')
    ax_main.text(-0.18, 0.08, '$O$', fontsize=12, fontweight='bold')

    ax_main.plot([0, x0], [0, y0], color='#333333', ls='--', lw=1.4)
    ax_main.text(0.88, -0.38, r'$2\ \mathrm{m}$', fontsize=11, fontweight='bold', rotation=-15)

    arc15 = np.linspace(ang_r, 0, 20)
    ax_main.plot(0.62 * np.cos(arc15), 0.62 * np.sin(arc15), color='#222222', lw=1.2)
    ax_main.text(0.66, -0.13, r'$15^\circ$', fontsize=10.5, fontweight='bold')

    arc45 = np.linspace(np.radians(165.0), np.radians(210.0), 25)
    ax_main.plot(x0 + 0.45 * np.cos(arc45), y0 + 0.45 * np.sin(arc45), color='#222222', lw=1.2)
    ax_main.text(x0 - 0.48, y0 - 0.16, r'$45^\circ$', fontsize=10.5, fontweight='bold')

    u_v = np.array([vx, vy]) / v_mag
    s_line = np.linspace(-0.2, 2.4, 40)
    ax_main.plot(x0 + u_v[0]*s_line, y0 + u_v[1]*s_line, color='#adb5bd', ls=':', lw=1.4, zorder=2)

    proj_s = np.dot(np.array([0 - x0, 0 - y0]), u_v)
    foot_x = x0 + proj_s * u_v[0]
    foot_y = y0 + proj_s * u_v[1]
    ax_main.plot([0, foot_x], [0, foot_y], color='#6a1b9a', ls='-.', lw=1.6, zorder=3)
    ax_main.text(foot_x*0.55 - 0.35, foot_y*0.55 + 0.05, r'$d = 2\sin 45^\circ$',
                 color='#6a1b9a', fontsize=9.5, fontweight='bold')

    if t > 0.01:
        ghost = patches.Circle((x0, y0), 0.14, facecolor='#f5dcd0', edgecolor='#8d6e63', ls='--', lw=1.1, alpha=0.5, zorder=4)
        ax_main.add_patch(ghost)

    sphere = patches.Circle((xc, yc), 0.14, facecolor='#d99b82', edgecolor='#4a2c20', lw=1.6, zorder=6)
    hi = patches.Circle((xc - 0.04, yc + 0.04), 0.05, facecolor='#fae5dc', edgecolor='none', zorder=7)
    ax_main.add_patch(sphere)
    ax_main.add_patch(hi)
    ax_main.text(x0 + 0.19, y0 - 0.03, r'$3\ \mathrm{kg}$', fontsize=11, fontweight='bold')

    v_draw_len = 0.85
    ax_main.annotate('', xy=(xc + u_v[0]*v_draw_len, yc + u_v[1]*v_draw_len), xytext=(xc, yc),
                     arrowprops=dict(arrowstyle='-|>', color='#00897b', lw=2.4, mutation_scale=15), zorder=7)
    ax_main.text(xc + u_v[0]*v_draw_len - 0.05, yc + u_v[1]*v_draw_len - 0.18,
                 r'$5\ \mathrm{m/s}$', color='#00897b', fontsize=11, fontweight='bold', ha='center')

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('선형운동량·각운동량·운동에너지 정량 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_card = (
        "【기하학적 각도 분해 (속도 벡터의 $x$축 기준 각도)】\n"
        r"• 반경선 각도: $+x$축 아래 $15^\circ \Rightarrow \mathbf{r} = 2(\cos 15^\circ\mathbf{i} - \sin 15^\circ\mathbf{j})\ \mathrm{m}$" + "\n"
        r"• 속도벡터 각도: 반경선 대비 $45^\circ \Rightarrow -x$축 아래 $45^\circ - 15^\circ = 30^\circ$" + "\n"
        r"• 속도벡터: $\mathbf{v} = 5(-\cos 30^\circ\mathbf{i} - \sin 30^\circ\mathbf{j})\ \mathrm{m/s}$"
    )
    ax_calc.text(0.35, 8.4, top_card, fontsize=9.3, va='center', ha='left', linespacing=1.4,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (3.10절)】\n"
        r"(a) 선형운동량 ($\mathbf{G} = m\mathbf{v}$):" + "\n"
        r"    $\mathbf{G} = 3(5)(-\cos 30^\circ\mathbf{i} - \sin 30^\circ\mathbf{j}) = \mathbf{-12.99\mathbf{i} - 7.50\mathbf{j}\ \mathrm{kg\cdot m/s}}$" + "\n\n"
        r"(b) 원점 $O$에 대한 각운동량 ($\mathbf{H}_O = \mathbf{r} \times \mathbf{G}$):" + "\n"
        r"    $\mathbf{H}_O = 2(\cos 15^\circ\mathbf{i} - \sin 15^\circ\mathbf{j}) \times (-12.99\mathbf{i} - 7.50\mathbf{j})$" + "\n"
        r"    $\mathbf{H}_O = \mathbf{-21.2\mathbf{k}\ \mathrm{kg\cdot m^2/s}}$  (시계방향 CW, $mvr\sin 45^\circ = 21.2$)" + "\n\n"
        r"(c) 운동에너지 ($T = \frac{1}{2}m v^2$):" + "\n"
        r"    $T = \frac{1}{2}(3)(5)^2 = \mathbf{37.5\ \mathrm{J}}$"
    )
    ax_calc.text(0.35, 4.65, sol_text, fontsize=9.3, va='center', ha='left', linespacing=1.35,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        rf"【실시간 운동 상태량 요약 ($t = {t:.2f}\ \mathrm{{s}}$)】" + "\n"
        r"• 선형운동량: $\mathbf{G} = -12.99\mathbf{i} - 7.50\mathbf{j}\ \mathrm{kg\cdot m/s}$ ($|\mathbf{G}| = 15.0\ \mathrm{kg\cdot m/s}$)" + "\n"
        r"• 각운동량: $\mathbf{H}_O = -21.2\mathbf{k}\ \mathrm{kg\cdot m^2/s}$  |  운동에너지: $T = 37.5\ \mathrm{J}$"
    )
    ax_calc.text(0.35, 1.25, live_text, fontsize=9.2, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_175_particle_angular_impulse.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
