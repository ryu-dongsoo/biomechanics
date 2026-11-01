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
동역학 9판 제4장 질점계의 운동역학 (4.7 가변질량)
기초문제 1 - 문제 4/60 (Problem 4/60) - 도로청소 살수 탱크 트럭의 가변질량 견인력 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영
- 이론 검증 결과:
  * (a) 살수기 작동 시 (m_dot = -40 kg/s, u = 20 m/s, 30 deg): P = 10^4(0.6) - 40(20 cos 30°) = 5310 N
  * (b) 살수기 미작동 시 (m_dot = 0): P = 10^4(0.6) = 6000 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수 (문제 4/60)
m0 = 10000.0            # 만재 시 트럭 총질량 10 Mg (kg)
a = 0.60                # 출발 수평 가속도 (m/s^2)
u = 20.0                # 트럭에 대한 살수 상대속도 (m/s)
theta_deg = 30.0        # 살수 경사각 (도)
theta = np.radians(theta_deg)
m_dot_on = -40.0        # 살수 시 질량 변화율 (kg/s)
g = 9.81

ux = u * np.cos(theta)  # 17.3205 m/s
P_on = m0 * a + m_dot_on * ux   # 6000 - 692.8 = 5307.2 -> 5310 N
P_off = m0 * a                  # 6000 N

n_frames = 50
t_vals = np.linspace(0.0, 2.8, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_tank_truck(ax, x_ref, y_ground, spray_active=True):
    # 바퀴 2개 (후륜, 전륜)
    r_w = 0.36
    x_rear = x_ref + 1.15
    x_front = x_ref + 3.25
    y_wc = y_ground + r_w

    # 섀시 프레임
    ax.add_patch(patches.Rectangle((x_ref + 0.35, y_wc + 0.02), 3.35, 0.20,
                                   facecolor='#424242', edgecolor='#212121', lw=1.4, zorder=2))

    # 물탱크 본체 (하늘색 둥근 실린더)
    tank = patches.FancyBboxPatch((x_ref + 0.35, y_wc + 0.22), 1.95, 1.05,
                                  boxstyle='round,pad=0.08,rounding_size=0.18',
                                  facecolor='#90caf9', edgecolor='#1e3a5f', lw=1.8, zorder=3)
    ax.add_patch(tank)
    # 탱크 상단 해치
    ax.add_patch(patches.Rectangle((x_ref + 1.12, y_wc + 1.35), 0.42, 0.08,
                                   facecolor='#64b5f6', edgecolor='#1e3a5f', lw=1.3, zorder=3))

    # 운전석 캡 (민트 블루 다각형 - 교재 원도 1:1)
    cab_pts = np.array([
        [x_ref + 2.42, y_wc + 0.02],
        [x_ref + 3.72, y_wc + 0.02],
        [x_ref + 3.72, y_wc + 0.56],
        [x_ref + 3.12, y_wc + 0.65],
        [x_ref + 2.92, y_wc + 1.12],
        [x_ref + 2.42, y_wc + 1.12]
    ])
    ax.add_patch(patches.Polygon(cab_pts, facecolor='#80cbc4', edgecolor='#004d40', lw=1.8, zorder=3))
    # 창문
    win_pts = np.array([
        [x_ref + 2.52, y_wc + 0.66],
        [x_ref + 3.04, y_wc + 0.66],
        [x_ref + 2.86, y_wc + 1.03],
        [x_ref + 2.52, y_wc + 1.03]
    ])
    ax.add_patch(patches.Polygon(win_pts, facecolor='#e0f2f1', edgecolor='#004d40', lw=1.2, zorder=4))

    # 타이어 및 림
    for wx in (x_rear, x_front):
        ax.add_patch(patches.Circle((wx, y_wc), r_w, facecolor='#455a64', edgecolor='#212121', lw=2.0, zorder=5))
        ax.add_patch(patches.Circle((wx, y_wc), r_w * 0.52, facecolor='#26c6da', edgecolor='#006064', lw=1.4, zorder=6))
        ax.add_patch(patches.Circle((wx, y_wc), r_w * 0.18, facecolor='#37474f', edgecolor='#212121', lw=1.0, zorder=7))

    # 후방 구리색 살수 배관 및 노즐 (30도 하향 경사)
    nozzle_base = np.array([x_ref + 0.35, y_wc + 0.16])
    nozzle_tip = nozzle_base + np.array([-0.75 * np.cos(theta), -0.75 * np.sin(theta)])
    ax.plot([x_ref + 0.75, nozzle_base[0], nozzle_tip[0]],
            [y_wc + 0.16, nozzle_base[1], nozzle_tip[1]],
            color='#d88c6a', lw=4.5, solid_capstyle='round', zorder=4)
    ax.plot([x_ref + 0.75, nozzle_base[0], nozzle_tip[0]],
            [y_wc + 0.16, nozzle_base[1], nozzle_tip[1]],
            color='#5d4037', lw=5.5, solid_capstyle='round', zorder=3)

    # 수평 점선 및 30도 각도 표시
    ax.plot([nozzle_base[0] - 1.15, nozzle_base[0]], [nozzle_base[1], nozzle_base[1]], color='#616161', ls='--', lw=1.2)
    arc = patches.Arc(nozzle_base, 1.3, 1.3, angle=0, theta1=180, theta2=210, color='#212121', lw=1.4)
    ax.add_patch(arc)
    ax.text(nozzle_base[0] - 0.92, nozzle_base[1] - 0.22, r'$30^\circ$', fontsize=11, fontweight='bold')

    # 살수 물줄기 (작동 시)
    if spray_active:
        jet_end = np.array([nozzle_tip[0] - (nozzle_tip[1] - y_ground) / np.tan(theta), y_ground])
        jet_poly = np.array([
            nozzle_tip + np.array([-0.02, 0.03]),
            nozzle_tip + np.array([0.02, -0.03]),
            jet_end + np.array([0.16, 0.0]),
            jet_end + np.array([-0.22, 0.0])
        ])
        ax.add_patch(patches.Polygon(jet_poly, facecolor='#4fc3f7', edgecolor='none', alpha=0.65, zorder=2))
        ax.annotate('', xy=nozzle_tip + np.array([-0.55 * np.cos(theta), -0.55 * np.sin(theta)]),
                    xytext=nozzle_tip,
                    arrowprops=dict(arrowstyle='->', color='#0277bd', lw=2.2, mutation_scale=14), zorder=6)
        ax.text(nozzle_tip[0] - 0.62, nozzle_tip[1] - 0.56, r'$u = 20\ \mathrm{m/s}\ (\dot{m} = -40\ \mathrm{kg/s})$',
                color='#01579b', fontsize=9.6, fontweight='bold', ha='center', va='center')


def update(frame):
    t = t_vals[frame]
    # 전반부(0~24 프레임): (a) 살수기 작동 (Water ON), 후반부(25~49 프레임): (b) 살수기 미작동 (Water OFF)
    spray_on = (frame < 28)
    t_local = (frame % 28) * 0.08
    s_curr = 0.5 * a * t_local**2
    v_curr = a * t_local
    P_curr = P_on if spray_on else P_off
    m_dot_curr = m_dot_on if spray_on else 0.0

    # ---------------- 1. 메인 뷰 (교재 원도 1:1) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.9, 6.9)
    ax_main.set_ylim(-0.6, 3.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 평탄한 도로 지면
    y_g = 0.2
    ax_main.fill_between([-1.7, 6.7], -0.35, y_g, color='#e0dcd3')
    ax_main.plot([-1.7, 6.7], [y_g, y_g], color='#3e2723', lw=2.2)

    x_truck = 0.05 + s_curr * 0.90
    draw_tank_truck(ax_main, x_truck, y_g, spray_active=spray_on)

    # 우측 가속도 화살표 a = 0.6 m/s^2 (초록색, 트럭 전면과 충분한 여백 확보)
    ax_main.annotate('', xy=(x_truck + 4.88, y_g + 0.72), xytext=(x_truck + 4.02, y_g + 0.72),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=16))
    ax_main.text(x_truck + 4.55, y_g + 0.90, f'$a = {a:.1f}\\ \\mathrm{{m/s^2}}$\n$(v = {v_curr:.2f}\\ \\mathrm{{m/s}})$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='center')

    # 바닥 타이어 견인력 P 화살표 (빨간색)
    ax_main.annotate('', xy=(x_truck + 2.15, y_g - 0.15), xytext=(x_truck + 1.15, y_g - 0.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=16))
    ax_main.text(x_truck + 2.25, y_g - 0.16, f'견인력 $P = {P_curr:.0f}\\ \\mathrm{{N}}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', va='center')

    # 상단 모드 배지
    mode_str = "(a) 살수기 작동 중 (Water ON: P = 5310 N)" if spray_on else "(b) 살수기 미작동 (Water OFF: P = 6000 N)"
    badge_col = '#0277bd' if spray_on else '#455a64'
    ax_main.text(2.5, 3.15, mode_str, fontsize=11, fontweight='bold', color=badge_col, ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=badge_col, lw=1.4))

    ax_main.set_title('문제 4/60: 도로청소 살수 탱크 트럭의 견인력 해석', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. 우측 패널 (자유물체도 & 정량 유도) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단 FBD 박스 (교재 기준 자유물체도)
    fbd_box = patches.FancyBboxPatch((0.3, 6.45), 9.4, 3.25, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[자유물체도 (FBD)] 수평 가변질량 운동방정식 ($+x$ 전진 방향)',
                 fontsize=10.2, fontweight='bold', ha='center', color='#1e3a5f')

    # 간략 트럭 FBD 윤곽
    ax_calc.add_patch(patches.Rectangle((2.8, 7.35), 2.5, 1.15, facecolor='#eceff1', edgecolor='#37474f', lw=1.6))
    ax_calc.add_patch(patches.Circle((3.35, 7.15), 0.22, facecolor='#cfd8dc', edgecolor='#37474f', lw=1.4))
    ax_calc.add_patch(patches.Circle((4.75, 7.15), 0.22, facecolor='#cfd8dc', edgecolor='#37474f', lw=1.4))

    # 중력 10(10^3)(9.81) N
    ax_calc.annotate('', xy=(4.05, 8.10), xytext=(4.05, 9.10),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(4.20, 8.85, r'$mg = 10^4(9.81)\ \mathrm{N}$', color='#d32f2f', fontsize=9.5, fontweight='bold')

    # 분사 상대속도 u = 20 m/s (30도)
    ax_calc.annotate('', xy=(1.75, 6.85), xytext=(2.80, 7.45),
                     arrowprops=dict(arrowstyle='->', color='#0277bd', lw=2.2))
    ax_calc.text(1.55, 7.35, r'$u = 20\ \mathrm{m/s}\ (30^\circ)$' '\n' r'$u_x = 17.32\ \mathrm{m/s}$',
                 color='#0277bd', fontsize=9.2, fontweight='bold', ha='center')

    # 견인력 P 및 가속도 a
    ax_calc.annotate('', xy=(4.35, 6.82), xytext=(3.15, 6.82),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.2))
    ax_calc.text(3.75, 6.56, r'$P$ (견인력)', color='#d32f2f', fontsize=9.5, fontweight='bold', ha='center')
    ax_calc.annotate('', xy=(7.25, 7.90), xytext=(5.85, 7.90),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2))
    ax_calc.text(6.65, 8.20, r'$a = 0.6\ \mathrm{m/s^2}\ (+x)$', color='#2e7d32', fontsize=9.5, fontweight='bold', ha='center')

    # 중앙 카드: 정량 유도
    sol_text = (
        r"■ 가변질량 수평 운동방정식 ($\Sigma F_x = m\dot{v} + \dot{m}u_x$):" "\n"
        r"  $\bullet\ m = 10\ \mathrm{Mg} = 10^4\ \mathrm{kg},\ \dot{v} = a = 0.6\ \mathrm{m/s^2}$" "\n"
        r"  $\bullet\ u_x = u\cos 30^\circ = 20\cos 30^\circ = 17.32\ \mathrm{m/s},\ \dot{m} = -40\ \mathrm{kg/s}$" "\n"
        r"■ (a) 살수기 작동 시 ($\dot{m} = -40\ \mathrm{kg/s}$):" "\n"
        r"  $\bullet\ P = 10^4(0.6) - 40(17.32) = 6000 - 692.8 \Rightarrow \mathbf{P = 5310\ \mathrm{N}}$" "\n"
        r"■ (b) 살수기 미작동 시 ($\dot{m} = 0$):  $\mathbf{P = 10^4(0.6) = 6000\ \mathrm{N}}$"
    )
    ax_calc.text(0.35, 4.25, sol_text, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드: 실시간 비교 모니터
    live_text = (
        f"[실시간 운전 상태 모니터]\n"
        f"• 현재 운전 모드: {'(a) 살수기 작동 (Water ON)' if spray_on else '(b) 살수기 정지 (Water OFF)'}\n"
        f"• 질량 방출률: $\\dot{{m}} = {m_dot_curr:.1f}\\ \\mathrm{{kg/s}}$   |   분사 반작용 추력: ${-m_dot_curr*ux:.1f}\\ \\mathrm{{N}}$\n"
        f"• 필요 바퀴 견인력: $\\mathbf{{P = {P_curr:.0f}\\ \\mathrm{{N}}}}$ (이론 최종값: ON $5310\\ \\mathrm{{N}}$ / OFF $6000\\ \\mathrm{{N}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_60_street_washer_truck.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
