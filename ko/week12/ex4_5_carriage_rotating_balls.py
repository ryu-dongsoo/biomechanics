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
동역학 9판 제4장 4.5절: 에너지와 운동량 보존
예제 4.5 (Sample Problem 4/5) - 수평 이동하는 운반대와 역회전하는 4구 조립체의 운동에너지·운동량 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영
- 정량 계산 검증:
  * (v_rel)_1,2 = 3.77 m/s, (v_rel)_3,4 = 3.14 m/s
  * (a) T = 16.13 + 38.5 = 54.7 J
  * (b) G = 26.9 kg·m/s
  * (c) H_O = 5.43 - 3.02 = 2.41 kg·m^2/s (반시계방향, CCW)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m_A = 16.0          # 운반대 질량 (kg)
m_ball = 1.6        # 공 1개 질량 (kg)
m_total = m_A + 4 * m_ball  # 22.4 kg
v_O = 1.2           # 운반대 속도 (m/s)

r12 = 0.450         # 공 1, 2 반지름 (m)
r34 = 0.300         # 공 3, 4 반지름 (m)
rpm12 = 80.0        # 반시계방향 (CCW, +)
rpm34 = 100.0       # 시계방향 (CW, -)

w12 = rpm12 * 2 * np.pi / 60.0   # 8.3776 rad/s (CCW)
w34 = rpm34 * 2 * np.pi / 60.0   # 10.4720 rad/s (CW)

v_rel12 = r12 * w12              # 3.770 m/s
v_rel34 = r34 * w34              # 3.142 m/s

n_frames = 54
t_vals = np.linspace(0, 0.45, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    t = t_vals[frame]
    xO = -0.25 + v_O * t
    yO = 0.0

    th12 = np.radians(28.0) + w12 * t     # CCW 회전
    th34 = np.radians(82.0) - w34 * t     # CW 회전

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.88, 1.04)
    ax_main.set_ylim(-0.62, 0.62)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    rail_y_top, rail_y_bot = 0.22, -0.22
    for ry in [rail_y_top, rail_y_bot]:
        rail_rect = patches.Rectangle((-0.82, ry - 0.018), 1.78, 0.036,
                                      facecolor='#b0bec5', edgecolor='#455a64', lw=1.5, zorder=1)
        ax_main.add_patch(rail_rect)

    car_w, car_h = 0.56, 0.39
    car_rect = patches.Rectangle((xO - car_w/2, yO - car_h/2), car_w, car_h,
                                 facecolor='#cfe2f3', edgecolor='#1d4564', lw=2.0, zorder=2)
    ax_main.add_patch(car_rect)
    ax_main.text(xO + 0.16, yO - 0.12, r'$A$ ($16\ \mathrm{kg}$)', fontsize=10, fontweight='bold',
                 color='#1d4564', ha='center', zorder=3)

    u34 = np.array([np.cos(th34), np.sin(th34)])
    n34 = np.array([-np.sin(th34), np.cos(th34)])
    p3 = np.array([xO, yO]) + r34 * u34
    p4 = np.array([xO, yO]) - r34 * u34
    rod34 = patches.Polygon([p4 - 0.014*n34, p4 + 0.014*n34, p3 + 0.014*n34, p3 - 0.014*n34],
                            facecolor='#d7ccc8', edgecolor='#5d4037', lw=1.4, zorder=3)
    ax_main.add_patch(rod34)

    for pt, lbl in [(p3, '3'), (p4, '4')]:
        c = patches.Circle(pt, 0.052, facecolor='#ef9a9a', edgecolor='#b71c1c', lw=1.8, zorder=4)
        ax_main.add_patch(c)
        ax_main.text(pt[0], pt[1], lbl, fontsize=10, fontweight='bold', ha='center', va='center', color='#4a0000', zorder=5)

    u12 = np.array([np.cos(th12), np.sin(th12)])
    n12 = np.array([-np.sin(th12), np.cos(th12)])
    p2 = np.array([xO, yO]) + r12 * u12
    p1 = np.array([xO, yO]) - r12 * u12
    rod12 = patches.Polygon([p1 - 0.016*n12, p1 + 0.016*n12, p2 + 0.016*n12, p2 - 0.016*n12],
                            facecolor='#b0bec5', edgecolor='#263238', lw=1.6, zorder=5)
    ax_main.add_patch(rod12)

    for pt, lbl in [(p1, '1'), (p2, '2')]:
        c = patches.Circle(pt, 0.055, facecolor='#90caf9', edgecolor='#0d47a1', lw=1.8, zorder=6)
        ax_main.add_patch(c)
        ax_main.text(pt[0], pt[1], lbl, fontsize=10, fontweight='bold', ha='center', va='center', color='#0d47a1', zorder=7)

    pin_O = patches.Circle((xO, yO), 0.026, facecolor='#ffffff', edgecolor='#222222', lw=2.0, zorder=8)
    ax_main.add_patch(pin_O)
    ax_main.plot(xO, yO, 'ko', markersize=4, zorder=9)
    ax_main.text(xO - 0.06, yO + 0.045, r'$O$', fontsize=12, fontweight='bold', zorder=9)

    # 회전 방향 안내 텍스트 (상·하단 고정 여백에 선명하게 배치하여 막대와 겹침 방지)
    ax_main.text(0.08, 0.52, r'공 1, 2 ($r_1 = 450\ \mathrm{mm}$): $80\ \mathrm{rpm}$ (반시계, CCW)',
                 fontsize=9.8, fontweight='bold', color='#0d47a1', ha='center',
                 bbox=dict(boxstyle='round,pad=0.18', facecolor='#eff6ff', edgecolor='#93c5fd', lw=1.0), zorder=9)
    ax_main.text(0.08, -0.53, r'공 3, 4 ($r_2 = 300\ \mathrm{mm}$): $100\ \mathrm{rpm}$ (시계, CW)',
                 fontsize=9.8, fontweight='bold', color='#b71c1c', ha='center',
                 bbox=dict(boxstyle='round,pad=0.18', facecolor='#fef2f2', edgecolor='#fca5a5', lw=1.0), zorder=9)

    v_start = np.array([xO + car_w/2 + 0.02, yO])
    v_end = v_start + np.array([0.26, 0.0])
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15), zorder=8)
    ax_main.text(v_end[0] + 0.02, v_end[1], r'$\bar{v} = 1.2\ \mathrm{m/s}$',
                 fontsize=10.8, fontweight='bold', color='#2e7d32', va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.10', facecolor='#ffffff', edgecolor='none', alpha=0.88), zorder=9)

    ax_main.set_title(r'예제 4.5: 수평 이동 운반대($16\ \mathrm{kg}$)와 역회전 4구 조립체', fontsize=13.3, fontweight='bold', pad=12)

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        r"(a) 총 운동에너지 ($T = \frac{1}{2}m\bar{v}^2 + \sum \frac{1}{2}m_i |\dot{\boldsymbol{\rho}}_i|^2$):" "\n"
        r"  $\bullet\ (v_{\mathrm{rel}})_{1,2} = 0.450 \frac{80(2\pi)}{60} = 3.77\ \mathrm{m/s},\ \ (v_{\mathrm{rel}})_{3,4} = 0.300 \frac{100(2\pi)}{60} = 3.14\ \mathrm{m/s}$" "\n"
        r"  $\bullet\ \frac{1}{2}m\bar{v}^2 = \frac{1}{2}[16 + 4(1.6)](1.2^2) = 16.13\ \mathrm{J}$" "\n"
        r"  $\bullet\ \sum \frac{1}{2}m_i |\dot{\boldsymbol{\rho}}_i|^2 = 2\left[\frac{1}{2}(1.6)(3.77^2)\right] + 2\left[\frac{1}{2}(1.6)(3.14^2)\right] = 38.5\ \mathrm{J}$" "\n"
        r"  $\bullet\ \mathbf{T = 16.13 + 38.5 = 54.7\ \mathrm{J}}$" "\n\n"
        "2. 선운동량 ($\\mathbf{G}$) 및 점 $O$에 대한 각운동량 ($H_O$, 반시계 $+$):\n"
        r"  $\bullet\ G = m\bar{v} = [16 + 4(1.6)](1.2) = \mathbf{26.9\ \mathrm{kg\cdot m/s}}\ (\rightarrow)$" "\n"
        r"  $\bullet\ H_O = [2(1.6)(0.450)(3.77)]_{(1,2)} - [2(1.6)(0.300)(3.14)]_{(3,4)}$" "\n"
        r"  $\bullet\ \mathbf{H_O = 5.43 - 3.02 = +2.41\ \mathrm{kg\cdot m^2/s}\ (\mathrm{CCW})}$"
    )
    ax_calc.text(0.32, 6.0, sol_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'운반대 중심 위치: $x_O = {xO + 0.25:.2f}\\ \\mathrm{{m}}$  (속도 $\\bar{{v}} = 1.20\\ \\mathrm{{m/s}}$)\n'
        f'병진 / 회전 에너지: $T_{{\\mathrm{{trans}}}} = 16.13\\ \\mathrm{{J}},\\ T_{{\\mathrm{{rot}}}} = 38.5\\ \\mathrm{{J}}$\n'
        f'이론 최종값: $T = 54.7\\ \\mathrm{{J}},\\ G = 26.9\\ \\mathrm{{kg\\cdot m/s}},\\ H_O = 2.41\\ \\mathrm{{kg\\cdot m^2/s}}$'
    )
    ax_calc.text(0.32, 1.45, live_box, fontsize=9.7, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title(r'이론 해석 및 정량 유도 ($T,\ \mathbf{G},\ H_O$)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_5_carriage_rotating_balls.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
