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
예제 4.10 (Sample Problem 4/10) - 수직으로 끌어올리는 개방링크 체인의 가변질량 동역학 및 에너지 손실
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영
- 이론 검증 결과:
  * 견인력 P(x) = rho*(g*x + v^2)
  * 바닥 반력 R(x) = rho*g*(L - x)
  * 비탄성 충돌 에너지 손실 Delta_E = 1/2*rho*L*v^2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 정량 파라미터 (이론식 기호 및 실시간 수치 동시 표기용)
L = 4.0         # 체인 전체 길이 (m)
rho = 2.5       # 단위길이당 질량 (kg/m)
v = 2.0         # 일정 상승 속도 (m/s)
g = 9.81        # 중력가속도 (m/s^2)

n_frames = 50
x_vals = np.linspace(0.3, L - 0.1, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_chain_links(ax, x_pos, y_start, y_end, link_h=0.22):
    n_links = max(1, int((y_end - y_start) / link_h))
    ys = np.linspace(y_start + link_h / 2, y_end - link_h / 2, n_links)
    for idx, yc in enumerate(ys):
        if idx % 2 == 0:
            ell = patches.Ellipse((x_pos, yc), 0.14, link_h * 0.95,
                                  facecolor='#cfd8dc', edgecolor='#37474f', lw=1.6, zorder=4)
        else:
            ell = patches.Ellipse((x_pos, yc), 0.06, link_h * 0.95,
                                  facecolor='#90a4ae', edgecolor='#263238', lw=1.6, zorder=5)
        ax.add_patch(ell)


def update(frame):
    x = x_vals[frame]
    P_curr = rho * (g * x + v**2)
    R_curr = rho * g * (L - x)
    W_air = rho * g * x
    F_dyn = rho * v**2
    U_P = 0.5 * rho * g * x**2 + rho * v**2 * x
    dT = 0.5 * rho * x * v**2
    dVg = 0.5 * rho * g * x**2
    dE = U_P - (dT + dVg)  # 0.5 * rho * x * v^2

    # ---------------- 1. 메인 뷰 (교재 원도 1:1) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.6, 2.8)
    ax_main.set_ylim(-0.7, 5.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 평판(바닥) 그리기
    plat_rect = patches.Rectangle((-1.8, -0.38), 3.6, 0.38, facecolor='#e0dcd5', edgecolor='#424242', lw=1.8)
    ax_main.add_patch(plat_rect)
    ax_main.plot([-1.9, 1.9], [0.0, 0.0], color='#212121', lw=2.4)

    # 바닥에 쌓인 개방링크 체인 더미 (남은 길이 L - x에 비례)
    rem_ratio = (L - x) / L
    np.random.seed(42)
    n_pile = int(4 + 26 * rem_ratio)
    for i in range(n_pile):
        px = (i - n_pile / 2) * 0.038 + np.sin(i * 1.7) * 0.18 * rem_ratio
        py = 0.05 + (i % 3) * 0.045 * rem_ratio
        ang = np.sin(i * 2.3) * 25
        pile_ell = patches.Ellipse((px, py), 0.22, 0.09, angle=ang,
                                   facecolor='#b0bec5', edgecolor='#37474f', lw=1.2, zorder=3)
        ax_main.add_patch(pile_ell)

    # 수직 상승 중인 체인 링크들
    draw_chain_links(ax_main, 0.0, 0.0, x)

    # 상단 견인력 화살표 P (빨간색, 교재 원도 동일)
    ax_main.annotate('', xy=(0.0, x + 0.85), xytext=(0.0, x),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, x + 0.55, f'$P = \\rho(gx + v^2)$\n$({P_curr:.1f}\\ \\mathrm{{N}})$',
                 color='#d32f2f', fontsize=11, fontweight='bold', va='center')

    # 상승 속도 벡터 v (초록색)
    v_y = max(0.5, x * 0.55)
    ax_main.annotate('', xy=(0.55, v_y + 0.65), xytext=(0.55, v_y),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=15))
    ax_main.text(0.72, v_y + 0.32, f'$v = {v:.1f}\\ \\mathrm{{m/s}}$\n(일정 속력)',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', va='center')

    # 좌측 치수선 x (평판 바닥 ~ 체인 상단)
    ax_main.plot([-1.45, -0.15], [x, x], color='#616161', lw=1.0)
    ax_main.plot([-1.45, -0.15], [0.0, 0.0], color='#616161', lw=1.0)
    ax_main.annotate('', xy=(-1.20, x), xytext=(-1.20, 0.0),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.4))
    ax_main.text(-1.35, x / 2.0, f'$x = {x:.2f}\\ \\mathrm{{m}}$',
                 fontsize=11, fontweight='bold', ha='right', va='center', color='#212121')

    # 하단 비탄성 충돌 강조 표시
    ax_main.text(0.65, 0.18, r'하단 링크 비탄성 충돌 ($\dot{m} = \rho v$)',
                 fontsize=9.5, color='#bf360c', fontweight='bold')

    ax_main.set_title('예제 4.10: 수직 상승 개방링크 체인 (가변질량 해석)', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. 우측 패널 (FBD I, II & 이론 유도 및 실시간 모니터) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단 FBD 비교 박스 (풀이 I: 가변질량 m=rho*x vs 풀이 II: 전체 일정질량 m=rho*L)
    fbd_box = patches.FancyBboxPatch((0.3, 6.55), 9.4, 3.15, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[자유물체도 비교] 풀이 I (가변질량) vs 풀이 II (일정질량)',
                 fontsize=10.5, fontweight='bold', ha='center', color='#1e3a5f')

    # 풀이 I FBD (좌측)
    ax_calc.add_patch(patches.Rectangle((2.1, 7.05), 0.22, 1.65, facecolor='#eceff1', edgecolor='#455a64', lw=1.5))
    ax_calc.annotate('', xy=(2.21, 9.25), xytext=(2.21, 8.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.40, 9.02, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(2.21, 7.45), xytext=(2.21, 8.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.42, 7.80, r'$\rho gx$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.text(1.45, 7.90, '풀이 I\n(가변질량)', fontsize=9.5, ha='center', va='center', fontweight='bold')

    # 풀이 II FBD (우측)
    ax_calc.add_patch(patches.Rectangle((6.7, 7.25), 0.22, 1.45, facecolor='#eceff1', edgecolor='#455a64', lw=1.5))
    pile_poly = patches.Polygon([[6.2, 7.05], [7.42, 7.05], [6.92, 7.25], [6.7, 7.25]],
                                facecolor='#cfd8dc', edgecolor='#455a64', lw=1.5)
    ax_calc.add_patch(pile_poly)
    ax_calc.annotate('', xy=(6.81, 9.25), xytext=(6.81, 8.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.00, 9.02, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(6.81, 7.50), xytext=(6.81, 8.20),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.02, 7.85, r'$\rho gL$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.annotate('', xy=(6.81, 7.05), xytext=(6.81, 6.62),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 6.75, r'$\rho g(L-x)$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.text(5.75, 7.90, '풀이 II\n(일정질량)', fontsize=9.5, ha='center', va='center', fontweight='bold')

    # 중앙 카드: 이론 유도 및 정량 공식 전개
    sol_text = (
        r"■ 가변질량 운동방정식 유도 ($\Sigma F_x = m\dot{v} + \dot{m}u$):" "\n"
        r"  $\bullet\ \dot{v}=0,\ \dot{m}=\rho v,\ u=v-0=v \Rightarrow P - \rho gx = 0 + (\rho v)v$" "\n"
        r"  $\bullet\ \mathbf{P(x) = \rho(gx + v^2)} = \rho gx$ (자중) $+ \rho v^2$ (운동량 변화율)" "\n"
        r"■ 체인 인양 중 내부 비탄성 충돌 에너지 손실 ($\Delta E$):" "\n"
        r"  $\bullet\ \int_0^L P\,dx - \Delta E = \Delta T + \Delta V_g \Rightarrow \left(\frac{1}{2}\rho gL^2 + \rho Lv^2\right) - \Delta E = \frac{1}{2}\rho Lv^2 + \frac{1}{2}\rho gL^2$" "\n"
        r"  $\bullet\ $이론 최종값: $\mathbf{\Delta E = \frac{1}{2}\rho Lv^2}$"
    )
    ax_calc.text(0.35, 4.35, sol_text, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드: 실시간 물리량 모니터
    live_text = (
        f"[실시간 정량 모니터: $L={L:.1f}\\ \\mathrm{{m}},\\ \\rho={rho:.1f}\\ \\mathrm{{kg/m}},\\ v={v:.1f}\\ \\mathrm{{m/s}}$]\n"
        f"• 공중 체인 자중: $\\rho gx = {W_air:.1f}\\ \\mathrm{{N}}$   |   동적 추력항: $\\rho v^2 = {F_dyn:.1f}\\ \\mathrm{{N}}$\n"
        f"• 현재 견인력: $P(x) = {P_curr:.1f}\\ \\mathrm{{N}}$   |   바닥 반력: $R = {R_curr:.1f}\\ \\mathrm{{N}}$\n"
        f"• 누적 에너지 손실: $\\Delta E(x) = \\frac{{1}}{{2}}\\rho xv^2 = {dE:.1f}\\ \\mathrm{{J}}$ (완전 인양 시 ${0.5*rho*L*v**2:.1f}\\ \\mathrm{{J}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_10_open_link_chain_lift.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
