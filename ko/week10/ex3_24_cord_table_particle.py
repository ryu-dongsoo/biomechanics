# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 유동수 (Dongsoo Ryu). All rights reserved.
#   - 소속 (Affiliation) : 전북대학교 생물산업기계공학과
#                          (Dept. of Bioindustrial Machinery Engineering,
#                           Jeonbuk National University)
#   - 성명 (Author)      : 유동수 (Dongsoo Ryu)
#   - 이메일 (Contact)   : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - 교과목 (Course)    : 생물역학 (Biomechanics)
# =============================================================================

"""
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
예제 3.24 (Sample Problem 3/24) - 3차원 공간 질점의 각운동량 H_O 및 시간 변화율 dH_O/dt
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * r = 3i + 6j + 4k m, m = 2 kg, v = 5j m/s, F = 10k N
  * H_O = r x mv = (3i + 6j + 4k) x 10j = -40i + 30k N·m·s (|H_O| = 50.0 N·m·s)
  * dH_O/dt = M_O = r x F = (3i + 6j + 4k) x 10k = 60i - 30j N·m (|M_O| = 67.1 N·m)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
m = 2.0
r0 = np.array([3.0, 6.0, 4.0])     # m
v0 = np.array([0.0, 5.0, 0.0])     # m/s
F_vec = np.array([0.0, 0.0, 10.0]) # N

G0 = m * v0                        # [0, 10, 0] N*s
H_O_0 = np.cross(r0, G0)           # [-40, 0, 30] N*m*s
M_O = np.cross(r0, F_vec)          # [60, -30, 0] N*m

# 3D 등각 투영 함수 (교재 원도 시점: x는 좌하향, y는 우하향, z는 연직 상향)
def proj3d(x, y, z):
    ang_x = np.radians(215)
    ang_y = np.radians(-18)
    px = x * np.cos(ang_x) * 0.85 + y * np.cos(ang_y) * 0.95
    py = x * np.sin(ang_x) * 0.85 + y * np.sin(ang_y) * 0.95 + z * 1.0
    return px, py

n_frames = 50
t_vals = np.linspace(0.0, 0.40, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    t = t_vals[frame]
    acc = F_vec / m  # [0, 0, 5] m/s^2
    r_curr = r0 + v0 * t + 0.5 * acc * t**2
    v_curr = v0 + acc * t
    H_curr = np.cross(r_curr, m * v_curr)

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-4.2, 9.2)
    ax_main.set_ylim(-3.5, 8.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('예제 3.24: 3차원 공간 구의 각운동량과 모멘트 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    # 원점 O 및 좌표축 x, y, z 그리기
    ox, oy = proj3d(0, 0, 0)
    xx, xy = proj3d(5.2, 0, 0)
    yx, yy = proj3d(0, 8.5, 0)
    zx, zy = proj3d(0, 0, 6.8)

    ax_main.plot([ox, xx], [oy, xy], color='#555555', ls='--', lw=1.4)
    ax_main.plot([ox, yx], [oy, yy], color='#555555', ls='--', lw=1.4)
    ax_main.plot([ox, zx], [oy, zy], color='#555555', ls='--', lw=1.4)
    ax_main.text(xx - 0.35, xy - 0.25, r'$x$', fontsize=12, fontweight='bold')
    ax_main.text(yx + 0.25, yy - 0.15, r'$y$', fontsize=12, fontweight='bold')
    ax_main.text(zx, zy + 0.25, r'$z$', fontsize=12, fontweight='bold', ha='center')
    ax_main.text(ox + 0.2, oy + 0.2, r'$O$', fontsize=12, fontweight='bold')

    # 초기 위치 (3, 6, 4) 투영 보조선 직육면체 바닥 및 기둥 (교재 원도 1:1)
    p_x0, p_y0 = proj3d(3, 0, 0)
    p_xy0_x, p_xy0_y = proj3d(3, 6, 0)
    p_0y_x, p_0y_y = proj3d(0, 6, 0)
    p_init_x, p_init_y = proj3d(3, 6, 4)

    ax_main.plot([p_x0, p_xy0_x], [p_y0, p_xy0_y], color='#222222', lw=1.2)
    ax_main.plot([p_0y_x, p_xy0_x], [p_0y_y, p_xy0_y], color='#222222', lw=1.2)
    ax_main.plot([p_xy0_x, p_init_x], [p_xy0_y, p_init_y], color='#222222', lw=1.2)

    # 치수 표기 (3 m, 6 m, 4 m)
    mid_3x, mid_3y = proj3d(1.6, 0, 0)
    ax_main.text(mid_3x - 0.85, mid_3y + 0.2, r'$3\ \mathrm{m}$', fontsize=10.5, fontweight='bold', color='#222222')
    mid_6x, mid_6y = proj3d(3, 3.0, 0)
    ax_main.text(mid_6x - 0.5, mid_6y - 0.55, r'$6\ \mathrm{m}$', fontsize=10.5, fontweight='bold', color='#222222')
    mid_4x, mid_4y = proj3d(3, 6, 1.8)
    ax_main.text(mid_4x + 0.25, mid_4y, r'$4\ \mathrm{m}$', fontsize=10.5, fontweight='bold', color='#222222')

    # 원점 O -> 질점 위치벡터 r 보조선
    px, py = proj3d(r_curr[0], r_curr[1], r_curr[2])
    ax_main.annotate('', xy=(px, py), xytext=(ox, oy),
                     arrowprops=dict(arrowstyle='->', color='#1f618d', lw=1.8, ls='-.', mutation_scale=13))
    ax_main.text((ox + px)*0.45 - 0.6, (oy + py)*0.45 + 0.35, r'$\mathbf{r}$', fontsize=11.5, color='#1f618d', fontweight='bold')

    # 미소 궤적 표시
    traj_pts = np.array([proj3d(*(r0 + v0 * tau + 0.5 * acc * tau**2)) for tau in np.linspace(0, 0.40, 30)])
    ax_main.plot(traj_pts[:, 0], traj_pts[:, 1], color='#e67e22', ls=':', lw=1.8)

    # 속도 벡터 v = 5 m/s (초록색 화살표)
    vx_end, vy_end = proj3d(r_curr[0], r_curr[1] + 2.2, r_curr[2])
    ax_main.annotate('', xy=(vx_end, vy_end), xytext=(px, py),
                     arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.5, mutation_scale=15), zorder=6)
    ax_main.text(vx_end + 0.2, vy_end - 0.1, r'$v = 5\ \mathrm{m/s}$', color='#2e7d32', fontsize=10.5, fontweight='bold')

    # 외력 벡터 F = 10 N (빨간색 상향 화살표)
    fx_end, fy_end = proj3d(r_curr[0], r_curr[1], r_curr[2] + 2.3)
    ax_main.annotate('', xy=(fx_end, fy_end), xytext=(px, py),
                     arrowprops=dict(arrowstyle='-|>', color='#d32f2f', lw=2.5, mutation_scale=15), zorder=6)
    ax_main.text(fx_end + 0.2, fy_end - 0.15, r'$F = 10\ \mathrm{N}$', color='#d32f2f', fontsize=10.5, fontweight='bold')

    # 원점 O에서의 각운동량 벡터 H_O 표시
    hx_end, hy_end = proj3d(-2.2, 0.0, 1.65)
    ax_main.annotate('', xy=(hx_end, hy_end), xytext=(ox, oy),
                     arrowprops=dict(arrowstyle='-|>', color='#6a1b9a', lw=2.4, mutation_scale=14), zorder=5)
    ax_main.text(hx_end - 1.3, hy_end + 0.2, r'$\mathbf{H}_O$', color='#6a1b9a', fontsize=11, fontweight='bold')

    # 질점 구 (2 kg)
    sphere = patches.Circle((px, py), 0.30, facecolor='#d99b82', edgecolor='#4a2c20', lw=1.8, zorder=7)
    highlight = patches.Circle((px - 0.08, py + 0.08), 0.10, facecolor='#f5dcd0', edgecolor='none', zorder=8)
    ax_main.add_patch(sphere)
    ax_main.add_patch(highlight)
    ax_main.text(px + 0.35, py + 0.28, r'$2\ \mathrm{kg}$', fontsize=10.5, fontweight='bold', color='#222222')

    # 우측 패널: 벡터 외적 유도 및 실시간 모니터
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('각운동량 외적 해석 및 정량 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_box = (
        "【3차원 위치·선운동량·외력 벡터 성분】\n"
        r"• 위치벡터: $\mathbf{r} = 3\mathbf{i} + 6\mathbf{j} + 4\mathbf{k}\ \mathrm{m}$" + "\n"
        r"• 선운동량: $\mathbf{G} = m\mathbf{v} = 2(5\mathbf{j}) = 10\mathbf{j}\ \mathrm{kg\cdot m/s}$" + "\n"
        r"• 작용외력: $\mathbf{F} = 10\mathbf{k}\ \mathrm{N}$"
    )
    ax_calc.text(0.35, 8.5, top_box, fontsize=9.8, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (Section 3.10)】\n"
        r"1) 원점 $O$에 대한 각운동량 ($\mathbf{H}_O = \mathbf{r} \times m\mathbf{v}$):" + "\n"
        r"   $\mathbf{H}_O = (3\mathbf{i} + 6\mathbf{j} + 4\mathbf{k}) \times 2(5\mathbf{j})$" + "\n"
        r"   $\mathbf{H}_O = \mathbf{-40\mathbf{i} + 30\mathbf{k}\ \mathrm{N\cdot m\cdot s}}$  ($|\mathbf{H}_O| = 50.0\ \mathrm{N\cdot m\cdot s}$)" + "\n\n"
        r"2) 각운동량의 시간 변화율 ($\dot{\mathbf{H}}_O = \mathbf{M}_O = \mathbf{r} \times \mathbf{F}$):" + "\n"
        r"   $\dot{\mathbf{H}}_O = (3\mathbf{i} + 6\mathbf{j} + 4\mathbf{k}) \times 10\mathbf{k}$" + "\n"
        r"   $\dot{\mathbf{H}}_O = \mathbf{60\mathbf{i} - 30\mathbf{j}\ \mathrm{N\cdot m}}$  ($|\dot{\mathbf{H}}_O| = 67.1\ \mathrm{N\cdot m}$)"
    )
    ax_calc.text(0.35, 4.9, sol_text, fontsize=9.8, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        rf"【실시간 각운동량 변화 모니터 ($t = {t:.2f}\ \mathrm{{s}}$)】" + "\n"
        rf"• 현재 위치: $\mathbf{{r}}(t) = ({r_curr[0]:.2f}\mathbf{{i}} + {r_curr[1]:.2f}\mathbf{{j}} + {r_curr[2]:.2f}\mathbf{{k}})\ \mathrm{{m}}$" + "\n"
        rf"• 순간 각운동량: $\mathbf{{H}}_O(t) = ({H_curr[0]:.1f}\mathbf{{i}} + {H_curr[1]:.1f}\mathbf{{j}} + {H_curr[2]:.1f}\mathbf{{k}})\ \mathrm{{N\cdot m\cdot s}}$" + "\n"
        r"• 이론 최종값 ($t=0$): $\mathbf{H}_O = -40\mathbf{i} + 30\mathbf{k}\ \mathrm{N\cdot m\cdot s},\ \ \dot{\mathbf{H}}_O = 60\mathbf{i} - 30\mathbf{j}\ \mathrm{N\cdot m}$"
    )
    ax_calc.text(0.35, 1.35, live_text, fontsize=9.4, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_24_cord_table_particle.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
