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
기초문제 3 - 문제 4/22 (Problem 4/22) - 강체 봉으로 연결된 2구 조립체의 편심 선충격량 및 각충격량 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림(초기 위치 및 파선 정렬 위치) 완벽 반영
- 정량 계산 검증:
  * ∫_{t1}^{t2} ΣF_x dt = 0 => ΔG_x = 0, ∫_{t1}^{t2} ΣF_y dt = ΔG_y: 10 = 2(1.5) v_y => v_y = 3.33 m/s
  * ∫_{t1}^{t2} ΣM_G dt = ΔH_G: 10(0.3) = 2(1.5) v_x (0.3) => v_x = 3.33 m/s
  * 파선 위치 통과 시 각 구의 속력: v = 3.33√2 = 4.71 m/s (두 구 모두 동일)
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
m = 1.5             # 각 구의 질량 (kg)
L = 0.600           # 연결봉 길이 600 mm = 0.6 m
r = 0.300           # 질량중심 G로부터 거리 (m)
Imp = 10.0          # 충격량 (N·s)

vy_G = Imp / (2.0 * m)                # 3.333 m/s
vx_rel = (Imp * r) / (2.0 * m * r)    # 3.333 m/s
omega = vx_rel / r                    # 11.111 rad/s
v_both = np.sqrt(vy_G**2 + vx_rel**2) # 4.714 -> 4.71 m/s

# 교재 다이어그램처럼 G가 y축을 따라 충분히 이동한 뒤 파선 위치에 도달하도록 θ = 5π/2 (1.25 회전)까지 시뮬레이션
t_target = (2.5 * np.pi) / omega      # 0.7069 s (y_G = 2.356 m)

n_frames = 54
t_vals = np.linspace(0, t_target, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def to_screen(x_phys, y_phys):
    return np.array([y_phys, -x_phys])

def update(frame):
    t = t_vals[frame]
    yG = vy_G * t
    th = omega * t

    x1, y1 = r * np.cos(th), yG + r * np.sin(th)
    x2, y2 = -r * np.cos(th), yG - r * np.sin(th)

    vx1_p, vy1_p = -vx_rel * np.sin(th), vy_G + vx_rel * np.cos(th)
    vx2_p, vy2_p = vx_rel * np.sin(th), vy_G - vx_rel * np.cos(th)
    v1_mag = np.sqrt(vx1_p**2 + vy1_p**2)
    v2_mag = np.sqrt(vx2_p**2 + vy2_p**2)

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.72, 3.18)
    ax_main.set_ylim(-0.84, 0.84)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 매끄러운 수평 테이블 평면 배경
    table = patches.Rectangle((-0.52, -0.58), 3.52, 1.16,
                              facecolor='#ede6df', edgecolor='#8d7b6d', lw=1.8, zorder=1)
    ax_main.add_patch(table)
    edge = patches.Polygon([[-0.52, -0.58], [3.00, -0.58], [3.00, -0.65], [-0.52, -0.65]],
                           facecolor='#cfc2b6', edgecolor='#8d7b6d', lw=1.2, zorder=1)
    ax_main.add_patch(edge)

    # 좌표축 x (하향), y (우측 수평 파선)
    ax_main.plot([0, 0], [0.52, -0.74], color='#333333', ls='--', lw=1.3, zorder=2)
    ax_main.text(0.06, -0.73, r'$x$', fontsize=12, fontweight='bold')
    ax_main.plot([-0.38, 3.06], [0, 0], color='#333333', ls='--', lw=1.3, zorder=2)
    ax_main.text(3.09, 0.0, r'$y$', fontsize=12, fontweight='bold', va='center')

    # 초기 위치 (y=0) 잔상 및 600 mm 치수선, 충격력 F 화살표
    p1_init = to_screen(r, 0)
    p2_init = to_screen(-r, 0)
    ax_main.plot([p1_init[0], p2_init[0]], [p1_init[1], p2_init[1]], color='#999999', ls=':', lw=2.0, zorder=2)
    for p_i in [p1_init, p2_init]:
        c_init = patches.Circle(p_i, 0.075, fill=False, edgecolor='#888888', ls=':', lw=1.4, zorder=2)
        ax_main.add_patch(c_init)

    # 600 mm 치수선 (좌측)
    ax_main.annotate('', xy=(-0.22, p1_init[1]), xytext=(-0.22, p2_init[1]),
                     arrowprops=dict(arrowstyle='<->', color='#444444', lw=1.2), zorder=3)
    ax_main.text(-0.26, 0.0, '600 mm', fontsize=10, fontweight='bold', ha='right', va='center', color='#333333',
                 bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.9))

    # 충격력 F 화살표 및 정적분 범위 명시 (겹침 없이 하단 여백 배치)
    ax_main.annotate('', xy=(p1_init[0] - 0.085, p1_init[1]), xytext=(p1_init[0] - 0.46, p1_init[1]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=15), zorder=5)
    ax_main.text(p1_init[0] - 0.27, p1_init[1] - 0.17, r'$\int_{t_1}^{t_2} F_y\,dt = 10\ \mathrm{N\cdot s}$',
                 fontsize=9.8, fontweight='bold', color='#d32f2f', ha='center',
                 bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.92))

    # 목표 파선(dashed line) 위치 표시
    yG_end = vy_G * t_target
    p1_dash = to_screen(0.0, yG_end + r)
    p2_dash = to_screen(0.0, yG_end - r)
    ax_main.plot([p2_dash[0], p1_dash[0]], [0, 0], color='#555555', ls='--', lw=2.2, zorder=2)
    for pd in [p1_dash, p2_dash]:
        cd = patches.Circle(pd, 0.075, fill=False, edgecolor='#444444', ls='--', lw=1.5, zorder=2)
        ax_main.add_patch(cd)

    # 현재 조립체 그리기
    p1_curr = to_screen(x1, y1)
    p2_curr = to_screen(x2, y2)
    pG_curr = to_screen(0.0, yG)

    rod_vec = p1_curr - p2_curr
    rod_u = rod_vec / np.linalg.norm(rod_vec)
    rod_n = np.array([-rod_u[1], rod_u[0]])
    rod_poly = patches.Polygon([p2_curr - 0.016*rod_n, p2_curr + 0.016*rod_n,
                                p1_curr + 0.016*rod_n, p1_curr - 0.016*rod_n],
                               facecolor='#ffffff', edgecolor='#263238', lw=1.6, zorder=4)
    ax_main.add_patch(rod_poly)

    for pt in [p1_curr, p2_curr]:
        sph = patches.Circle(pt, 0.078, facecolor='#c95b5b', edgecolor='#6b1d1d', lw=1.8, zorder=5)
        ax_main.add_patch(sph)

    ax_main.plot(pG_curr[0], pG_curr[1], 'ko', markersize=5, zorder=6)
    ax_main.text(pG_curr[0], pG_curr[1] - 0.10, r'$G$', fontsize=11, fontweight='bold', ha='center', zorder=7)

    # 회전 각속도 ω 호 (G 주변 반시계방향 화살표만 깔끔히 표시, 텍스트는 상단 안전 영역에 배치하여 겹침 0%)
    arc_r = 0.145
    arc_w = patches.Arc(pG_curr, 2*arc_r, 2*arc_r, angle=0, theta1=35, theta2=145, color='#00897b', lw=2.0, zorder=6)
    ax_main.add_patch(arc_w)
    tip_ang, tail_ang = np.radians(145), np.radians(125)
    ax_main.annotate('', xy=(pG_curr[0] + arc_r*np.cos(tip_ang), pG_curr[1] + arc_r*np.sin(tip_ang)),
                     xytext=(pG_curr[0] + arc_r*np.cos(tail_ang), pG_curr[1] + arc_r*np.sin(tail_ang)),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.0, mutation_scale=11), zorder=6)

    # 상단 안전 여백에 병진 속도 및 회전 각속도 배지 배치 (구 회전 반경 0.38 밖!)
    ax_main.text(1.28, 0.70,
                 r'$\bar{v}_y = 3.33\ \mathrm{m/s}\ (\rightarrow),\quad \omega = 11.1\ \mathrm{rad/s}\ (\mathrm{CCW})$',
                 fontsize=10.2, fontweight='bold', color='#00695c', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.22', facecolor='#e0f2f1', edgecolor='#80cbc4', lw=1.2), zorder=8)

    # 두 구의 현재 속도 벡터 (초록색 표준)
    v1_scr = np.array([vy1_p, -vx1_p]) * 0.062
    v2_scr = np.array([vy2_p, -vx2_p]) * 0.062
    ax_main.annotate('', xy=p1_curr + v1_scr, xytext=p1_curr,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=7)
    ax_main.annotate('', xy=p2_curr + v2_scr, xytext=p2_curr,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=7)

    if frame >= n_frames - 3:
        ax_main.text(p1_curr[0] + 0.04, p1_curr[1] + 0.36, r'$v_1 = 4.71\ \mathrm{m/s}$',
                     fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center',
                     bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.88))
        ax_main.text(p2_curr[0] - 0.04, p2_curr[1] - 0.38, r'$v_2 = 4.71\ \mathrm{m/s}$',
                     fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center',
                     bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.88))

    ax_main.set_title(r'문제 4/22: 강체 봉으로 연결된 두 구($1.5\ \mathrm{kg}\times 2$)의 충격 후 운동', fontsize=13.2, fontweight='bold', pad=12)

    # ---------------- 우측 패널: 이론 해석 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        "1. 선충격량-선운동량 방정식 (질량중심 $G$ 병진 속도):\n"
        r"  $\bullet\ \int_{t_1}^{t_2} \sum F_x\,dt = 0 \Rightarrow \Delta G_x = 0 \Rightarrow \bar{v}_x = 0$" "\n"
        r"  $\bullet\ \int_{t_1}^{t_2} \sum F_y\,dt = \Delta G_y:\ \ 10 = 2(1.5)\,\bar{v}_y \Rightarrow \mathbf{\bar{v}_y = 3.33\ \mathrm{m/s}}$" "\n\n"
        "2. 질량중심 $G$에 대한 각충격량-각운동량 방정식:\n"
        r"  $\bullet\ \int_{t_1}^{t_2} \sum M_G\,dt = \Delta H_G:\ \ 10(0.3) = 2(1.5)\,v_{\mathrm{rel}}\,(0.3)$" "\n"
        r"  $\bullet\ \mathbf{v_{\mathrm{rel}} = 3.33\ \mathrm{m/s}}\quad (\omega = v_{\mathrm{rel}} / 0.3 = 11.11\ \mathrm{rad/s})$" "\n\n"
        "3. 파선($y$축 정렬) 위치 통과 시 각 구의 속력:\n"
        r"  $\bullet\ \bar{v}_y = 3.33\ \mathrm{m/s}\ (\rightarrow),\quad v_x = \pm 3.33\ \mathrm{m/s}\ (\uparrow\downarrow)$" "\n"
        r"  $\bullet\ \mathbf{v = \sqrt{3.333^2 + 3.333^2} = 4.71\ \mathrm{m/s}}$" " (두 구 모두 동일)"
    )
    ax_calc.text(0.32, 6.0, sol_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'질량중심 이동: $y_G = {yG:.2f}\\ \\mathrm{{m}}$  (병진 속도 $\\bar{{v}}_y = 3.33\\ \\mathrm{{m/s}}$)\n'
        f'현재 두 구 속력: $v_1 = {v1_mag:.2f}\\ \\mathrm{{m/s}},\\ v_2 = {v2_mag:.2f}\\ \\mathrm{{m/s}}$\n'
        f'보존 각운동량 (일정): $H_G = 3.00\\ \\mathrm{{kg\\cdot m^2/s}}$\n'
        f'이론 최종값 (파선 통과 시): $\\mathbf{{v_1 = v_2 = 4.71\\ \\mathrm{{m/s}}}}$ (두 구 모두 동일)'
    )
    ax_calc.text(0.32, 1.45, live_box, fontsize=9.7, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도 (선·각충격량 및 보존)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_22_rigid_rod_two_spheres.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
