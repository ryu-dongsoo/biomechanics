"""
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
예제 3.27 - 매끄러운 반구형 그릇 내부 질점의 3차원 나사선 활주
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * 수직 중심축 O-O에 대한 각운동량 보존: (H_O)_1 = (H_O)_2 => m v_0 r_0 = m v r cos(theta)
  * 역학적 에너지 보존: T_1 + V_1 = T_2 + V_2 => v = sqrt(v_0^2 + 2 g h)
  * 기하학: r^2 = r_0^2 - h^2
  * 연립 해: theta = arccos( 1 / [ sqrt(1 + 2gh / v_0^2) * sqrt(1 - h^2 / r_0^2) ] )
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

g = 9.81
r0 = 1.0       # 정규화 반경 1.0
v0 = 3.5       # m/s
h_max = 0.55   # B점 깊이 h = 0.55 * r0

def proj_bowl(x, y, z):
    px = x * 0.92 + y * 0.32
    py = z * 0.95 - y * 0.28
    return px, py

n_frames = 55
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

phi_full = np.linspace(2.35, 6.05, 120)
h_full = h_max * ((phi_full - 2.35) / (6.05 - 2.35))**1.15
r_full = np.sqrt(np.maximum(r0**2 - h_full**2, 1e-4))
x_full = r_full * np.cos(phi_full)
y_full = r_full * np.sin(phi_full)
z_full = -h_full
traj_2d = np.array([proj_bowl(x, y, z) for x, y, z in zip(x_full, y_full, z_full)])

def update(frame):
    idx = int((frame / (n_frames - 1)) * (len(phi_full) - 1))
    h_curr = max(h_full[idx], 1e-4)
    r_curr = r_full[idx]
    v_curr = np.sqrt(v0**2 + 2.0 * g * h_curr)
    cos_th = min((v0 * r0) / (v_curr * r_curr), 1.0)
    theta_deg = np.degrees(np.arccos(cos_th))

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.45)
    ax_main.set_ylim(-1.35, 0.65)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('예제 3.27: 반구형 그릇 내부 질점의 3차원 운동 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    ang_semi = np.linspace(np.pi, 2 * np.pi, 100)
    bowl_x = 1.0 * np.cos(ang_semi)
    bowl_y = 0.95 * np.sin(ang_semi)
    rim_t = np.linspace(0, 2 * np.pi, 120)
    rim_x, rim_y = proj_bowl(r0 * np.cos(rim_t), r0 * np.sin(rim_t), np.zeros_like(rim_t))

    ax_main.fill(bowl_x, bowl_y, color='#8ebad9', alpha=0.55, zorder=1)
    ax_main.plot(bowl_x, bowl_y, color='#2c5d8a', lw=2.0, zorder=2)

    ax_main.fill(rim_x, rim_y, color='#cce4f6', alpha=0.85, zorder=2)
    ax_main.plot(rim_x, rim_y, color='#2c5d8a', lw=1.8, zorder=3)

    ax_main.plot([0, 0], [-1.22, 0.45], color='#222222', lw=1.2, ls='-', zorder=4)
    ax_main.text(0.05, 0.40, '$O$', fontsize=11.5, fontweight='bold')
    ax_main.text(0.05, -1.22, '$O$', fontsize=11.5, fontweight='bold')
    ax_main.plot(0, 0, 'o', color='#222222', markersize=4.5, zorder=5)

    z_B = -h_max
    px_B, py_B = traj_2d[-1]
    ox_B, oy_B = proj_bowl(0, 0, z_B)
    ax_main.plot(ox_B, oy_B, 'o', color='#222222', markersize=4.5, zorder=5)
    ax_main.plot([ox_B, px_B], [oy_B, py_B], color='#222222', lw=1.2, zorder=4)
    ax_main.text((ox_B + px_B)*0.48, (oy_B + py_B)*0.48 + 0.06, '$r$', fontsize=11, style='italic', fontweight='bold')
    ax_main.text(0.05, oy_B * 0.5, '$h$', fontsize=11, style='italic', fontweight='bold')

    px_A, py_A = traj_2d[0]
    ax_main.plot([0, px_A], [0, py_A], color='#222222', lw=1.2, zorder=4)
    ax_main.text(px_A * 0.5 - 0.08, py_A * 0.5 - 0.10, '$r_0$', fontsize=11, style='italic', fontweight='bold')
    ax_main.plot(px_A, py_A, 'o', color='#111111', markersize=5.5, zorder=6)
    ax_main.text(px_A - 0.14, py_A + 0.06, '$A$', fontsize=11.5, fontweight='bold')

    ax_main.annotate('', xy=(px_A + 0.35, py_A + 0.11), xytext=(px_A, py_A),
                     arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=6)
    ax_main.text(px_A + 0.18, py_A + 0.14, r'$\mathbf{v}_0$', color='#2e7d32', fontsize=11, fontweight='bold')

    ax_main.plot(traj_2d[:, 0], traj_2d[:, 1], color='#e67e22', ls='--', lw=2.0, zorder=4)

    ax_main.plot(px_B, py_B, 'o', color='#111111', markersize=5.0, zorder=6)
    ax_main.text(px_B - 0.05, py_B + 0.08, '$B$', fontsize=11.5, fontweight='bold')
    ax_main.plot([px_B - 0.35, px_B + 0.08], [py_B - 0.15, py_B + 0.03], color='#333333', lw=1.1, zorder=5)
    ax_main.annotate('', xy=(px_B - 0.32, py_B - 0.30), xytext=(px_B, py_B),
                     arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=6)
    ax_main.text(px_B - 0.38, py_B - 0.28, r'$\mathbf{v}$', color='#2e7d32', fontsize=11, fontweight='bold')
    ax_main.text(px_B - 0.18, py_B - 0.25, r'$\theta$', color='#111111', fontsize=11, fontweight='bold')

    curr_px, curr_py = traj_2d[idx]
    particle = patches.Circle((curr_px, curr_py), 0.048, facecolor='#e74c3c', edgecolor='#78281f', lw=1.5, zorder=8)
    ax_main.add_patch(particle)

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('수직축 각운동량·에너지 연립 해석 및 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_card = (
        "【수직 중심축 $O$-$O$ 모멘트 평형 및 보존 원리】\n"
        r"• 작용하는 힘: 자중 $W = mg$ ($O$-$O$축과 평행) 및 수직항력 $N$ (구 중심 통과)" + "\n"
        r"• 두 힘 모두 $O$-$O$축에 대한 모멘트를 만들지 않음 ($\Sigma M_{O\text{-}O} = 0$)" + "\n"
        r"• 또한 매끄러운 면(마찰 $= 0$)이므로 역학적 에너지 보존 ($T_1 + V_1 = T_2 + V_2$)"
    )
    ax_calc.text(0.35, 8.5, top_card, fontsize=9.4, va='center', ha='left', linespacing=1.4,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (3.10절)】\n"
        r"1) $O$-$O$축 각운동량 보존 ($(H_O)_1 = (H_O)_2$):" + "\n"
        r"   $m v_0 r_0 = m (v \cos\theta) r \quad \cdots (1)$" + "\n\n"
        r"2) 역학적 에너지 보존 ($T_1 + V_1 = T_2 + V_2$):" + "\n"
        r"   $\frac{1}{2}m v_0^2 + mgh = \frac{1}{2}m v^2 \Rightarrow v = \sqrt{v_0^2 + 2gh} \quad \cdots (2)$" + "\n\n"
        r"3) $r = \sqrt{r_0^2 - h^2}$ 및 식 (2)를 식 (1)에 대입하여 $v$ 소거:" + "\n"
        r"   $v_0 r_0 = \sqrt{v_0^2 + 2gh}\sqrt{r_0^2 - h^2}\cos\theta$" + "\n"
        r"   $\Rightarrow \mathbf{\theta = \cos^{-1}\frac{1}{\sqrt{1 + 2gh/v_0^2} \sqrt{1 - h^2/r_0^2}}}$"
    )
    ax_calc.text(0.35, 4.75, sol_text, fontsize=9.4, va='center', ha='left', linespacing=1.35,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        rf"【실시간 3D 활주 상태 모니터 (깊이 비 $h/r_0 = {h_curr/r0:.2f}$)】" + "\n"
        rf"• 수평 회전반경 비: $r/r_0 = \sqrt{{1 - (h/r_0)^2}} = {r_curr/r0:.3f}$" + "\n"
        rf"• 현재 속력 비: $v/v_0 = {v_curr/v0:.3f}$  |  경사각: $\theta = {theta_deg:.1f}^\circ$" + "\n"
        r"• 이론 최종식: $\theta = \cos^{-1}[ 1 / (\sqrt{1 + 2gh/v_0^2} \cdot \sqrt{1 - h^2/r_0^2}) ]$"
    )
    ax_calc.text(0.35, 1.25, live_text, fontsize=9.2, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_27_hemispherical_bowl_particle.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
