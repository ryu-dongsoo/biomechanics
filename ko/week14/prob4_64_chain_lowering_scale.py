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
기초문제 3 - 문제 4/64 (Problem 4/64) - 바닥 저울 위로 일정 속력으로 내려지는 개방링크 체인
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (원형 다이얼 저울 + 하강하는 개방링크 체인)
- 이론 검증 결과:
  * 상단 지지력 P = 하강 중인 링크 무게 = rho*g*(L - x)
  * Sigma F_x = dG_x / dt => rho*g*L - R - rho*g*(L - x) = d/dt [rho*(L - x)*v] = -rho*v^2
  * 바닥 저울 눈금 R(x) = rho*g*x + rho*v^2 = rho*(g*x + v^2)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 정량 시뮬레이션 파라미터 (기호식과 병기)
L = 4.0         # 체인 전체 길이 (m)
rho = 2.0       # 단위길이당 질량 (kg/m)
v = 2.5         # 일정 하강 속력 (m/s)
g = 9.81        # 중력가속도 (m/s^2)

n_frames = 50
x_vals = np.linspace(0.25, L - 0.25, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_dial_scale(ax, R_curr, R_max):
    # 교재 p.275 문제 4/64의 황금색 스탠드형 원형 다이얼 저울 1:1 재현
    # 바닥 받침대
    ax.fill_between([-2.1, 2.1], -0.45, -0.15, color='#e0dcd3')
    ax.plot([-2.1, 2.1], [-0.15, -0.15], color='#3e2723', lw=2.2)

    base1 = patches.Rectangle((-1.05, -0.15), 2.10, 0.22, facecolor='#dfc16d', edgecolor='#4e342e', lw=1.6, zorder=1)
    base2 = patches.Rectangle((-0.90, 0.07), 1.80, 0.11, facecolor='#e6ce8a', edgecolor='#4e342e', lw=1.4, zorder=1)
    ax.add_patch(base1)
    ax.add_patch(base2)

    # 사다리꼴 기둥 (Pillar)
    pillar = patches.Polygon([
        [-0.36, 0.18], [0.36, 0.18], [0.24, 1.95], [-0.24, 1.95]
    ], facecolor='#dfc16d', edgecolor='#4e342e', lw=1.6, zorder=1)
    ax.add_patch(pillar)

    # 원형 다이얼 외곽 및 내판 (중심 (0.0, 2.45), 반경 0.72)
    dc_y = 2.45
    ax.add_patch(patches.Circle((0.0, dc_y), 0.72, facecolor='#dfc16d', edgecolor='#4e342e', lw=1.8, zorder=1))
    ax.add_patch(patches.Circle((0.0, dc_y), 0.62, facecolor='#f9f3df', edgecolor='#6d4c41', lw=1.3, zorder=1))

    # 다이얼 눈금선
    for deg in np.linspace(-45, 225, 28):
        rad = np.radians(deg)
        r_in = 0.52 if int(deg) % 45 == 0 else 0.56
        ax.plot([r_in * np.cos(rad), 0.61 * np.cos(rad)],
                [dc_y + r_in * np.sin(rad), dc_y + 0.61 * np.sin(rad)],
                color='#5d4037', lw=1.0, zorder=2)

    # 저울 바늘 (R_curr 값에 따라 회전: 140 deg -> 20 deg)
    frac = np.clip(R_curr / R_max, 0.0, 1.0)
    ang_needle = np.radians(145.0 - frac * 115.0)
    ax.plot([0.0, 0.46 * np.cos(ang_needle)],
            [dc_y, dc_y + 0.46 * np.sin(ang_needle)],
            color='#212121', lw=3.0, solid_capstyle='round', zorder=2)
    ax.add_patch(patches.Circle((0.0, dc_y), 0.045, facecolor='#212121', zorder=3))


def draw_chain_links(ax, x_pos, y_start, y_end, link_h=0.22):
    n_links = max(1, int((y_end - y_start) / link_h))
    ys = np.linspace(y_start + link_h / 2, y_end - link_h / 2, n_links)
    for idx, yc in enumerate(ys):
        if idx % 2 == 0:
            ell = patches.Ellipse((x_pos, yc), 0.13, link_h * 0.95,
                                  facecolor='#b0bec5', edgecolor='#263238', lw=1.5, zorder=5)
        else:
            ell = patches.Ellipse((x_pos, yc), 0.055, link_h * 0.95,
                                  facecolor='#78909c', edgecolor='#263238', lw=1.5, zorder=6)
        ax.add_patch(ell)


def update(frame):
    x = x_vals[frame]
    y_pan = 0.18
    y_top = y_pan + (L - x)

    P_curr = rho * g * (L - x)
    W_pile = rho * g * x
    F_imp = rho * v**2
    R_curr = W_pile + F_imp
    R_max = rho * (g * L + v**2)

    # ---------------- 1. 메인 뷰 (교재 원도 1:1) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.6, 2.8)
    ax_main.set_ylim(-0.6, 5.5)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 황금색 다이얼 저울 렌더링 (배경)
    draw_dial_scale(ax_main, R_curr, R_max)

    # 저울 접시 위 쌓인 체인 더미 (길이 x에 비례)
    pile_ratio = x / L
    np.random.seed(17)
    n_pile = int(4 + 26 * pile_ratio)
    for i in range(n_pile):
        px = -0.10 + (i - n_pile / 2) * 0.032 + np.sin(i * 1.9) * 0.14 * pile_ratio
        py = y_pan + 0.04 + (i % 3) * 0.042 * pile_ratio
        ang = np.cos(i * 2.1) * 22
        ax_main.add_patch(patches.Ellipse((px, py), 0.20, 0.08, angle=ang,
                                          facecolor='#90a4ae', edgecolor='#263238', lw=1.1, zorder=4))

    # 하강 중인 수직 체인 (길이 L - x, 중심 x = -0.10: 다이얼 바늘 중심을 살짝 비켜 내려감 - 교재 원도 동일)
    x_chain = -0.12
    draw_chain_links(ax_main, x_chain, y_pan, y_top)

    # 상단 지지력 P 화살표 (빨간색 상향)
    ax_main.annotate('', xy=(x_chain, y_top + 0.75), xytext=(x_chain, y_top),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18), zorder=7)
    ax_main.plot([-0.68, x_chain - 0.05], [y_top + 0.45, y_top + 0.45], color='#d32f2f', lw=0.9, ls=':')
    ax_main.text(-0.72, y_top + 0.45, f'$P = \\rho g(L-x)$\n$({P_curr:.1f}\\ \\mathrm{{N}})$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', ha='right', va='center')

    # 하강 속도 벡터 v (초록색 하향 화살표 - 다이얼 좌측 외곽)
    ax_main.annotate('', xy=(-0.74, y_top - 0.55), xytext=(-0.74, y_top + 0.15),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=15), zorder=7)
    ax_main.text(-0.86, y_top - 0.20, f'$v = {v:.1f}\\ \\mathrm{{m/s}}$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right', va='center')

    # 치수선 L (전체 높이) 및 x (상단 하강 변위) - 교재 원도 우측 치수선 1:1 재현
    y_datum_top = y_pan + L
    ax_main.plot([x_chain + 0.15, 1.88], [y_datum_top, y_datum_top], color='#616161', lw=1.0)
    ax_main.plot([x_chain + 0.15, 0.88], [y_top, y_top], color='#616161', lw=1.0)
    ax_main.plot([0.92, 1.88], [y_pan, y_pan], color='#616161', lw=1.0)

    # x 치수선 (다이얼 우측 반경 0.62 바깥 x=0.72에 배치)
    ax_main.annotate('', xy=(0.72, y_top), xytext=(0.72, y_datum_top),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.3))
    ax_main.text(0.78, 0.5 * (y_top + y_datum_top), f'$x = {x:.2f}\\ \\mathrm{{m}}$',
                 fontsize=10.5, fontweight='bold', va='center', color='#212121')

    # L 치수선
    ax_main.annotate('', xy=(1.75, y_pan), xytext=(1.75, y_datum_top),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.3))
    ax_main.text(1.83, 0.5 * (y_pan + y_datum_top), f'$L = {L:.1f}\\ \\mathrm{{m}}$',
                 fontsize=11, fontweight='bold', va='center', color='#212121')

    # 하단 저울 반력 R 표시
    ax_main.text(0.0, -0.36, f'저울 눈금(반력) $R = \\rho(gx + v^2) = {R_curr:.1f}\\ \\mathrm{{N}}$',
                 fontsize=10.5, fontweight='bold', color='#b71c1c', ha='center')

    ax_main.set_title('문제 4/64: 바닥 저울 위로 일정 속력 하강하는 체인', fontsize=13.5, fontweight='bold', pad=12)

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
    ax_calc.text(5.0, 9.42, '[자유물체도 (FBD)] 전체 체인 시스템 ($+x$ 연직 하향 좌표축)',
                 fontsize=10.2, fontweight='bold', ha='center', color='#1e3a5f')

    # FBD 체인 수직부 + 하단 더미
    ax_calc.add_patch(patches.Rectangle((3.1, 7.20), 0.22, 1.55, facecolor='#eceff1', edgecolor='#455a64', lw=1.5))
    ax_calc.add_patch(patches.Polygon([[2.75, 6.95], [3.67, 6.95], [3.32, 7.20], [3.10, 7.20]],
                                      facecolor='#cfd8dc', edgecolor='#455a64', lw=1.5))
    # +x 좌표 화살표
    ax_calc.annotate('', xy=(1.35, 7.45), xytext=(1.35, 8.35),
                     arrowprops=dict(arrowstyle='->', color='#212121', lw=1.6))
    ax_calc.text(1.35, 7.15, r'$+x$ (하향)', fontsize=9.5, fontweight='bold', ha='center')

    # P 화살표 (상향)
    ax_calc.annotate('', xy=(3.21, 9.30), xytext=(3.21, 8.75),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(3.42, 9.05, r'$P = \rho g(L-x)$', color='#d32f2f', fontsize=9.5, fontweight='bold')

    # 전체 무게 rho*g*L (하향)
    ax_calc.annotate('', xy=(3.21, 7.50), xytext=(3.21, 8.20),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(3.45, 7.85, r'$\rho gL$ (총중량)', color='#d32f2f', fontsize=9.5, fontweight='bold')

    # 바닥 반력 R (상향)
    ax_calc.annotate('', xy=(3.21, 6.95), xytext=(3.21, 6.52),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.2))
    ax_calc.text(3.45, 6.68, r'$R$ (저울 반력)', color='#d32f2f', fontsize=9.5, fontweight='bold')

    # 우측 설명 텍스트
    ax_calc.text(7.2, 8.05, r'하강 중인 링크 길이: $L - x$' '\n'
                            r'하강 속도: $\dot{x} = v = \mathrm{const}$' '\n'
                            r'전체 하향 운동량:' '\n'
                            r'$G_x = \rho(L - x)v$',
                 fontsize=9.5, ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8f9fa', edgecolor='#cfd8dc'))

    # 중앙 카드: 정량 유도
    sol_text = (
        r"■ 상단 지지력($P$) 및 전체 체인 운동량 방정식 ($\Sigma F_x = \frac{dG_x}{dt}$):" "\n"
        r"  $\bullet\ \dot{x} = v = \mathrm{const}$ 이므로 상단 지지력은 하강 링크 무게와 평형: $P = \rho g(L - x)$" "\n"
        r"  $\bullet\ \Sigma F_x = \frac{dG_x}{dt} \Rightarrow \rho gL - R - \rho g(L - x) = \frac{d}{dt}\left(\rho[L - x]v\right)$" "\n"
        r"  $\bullet\ \rho gx - R = -\rho v\dot{x} = -\rho v^2$" "\n"
        r"■ 바닥 저울 눈금 (이론 최종값):  $\mathbf{R(x) = \rho gx + \rho v^2 = \rho(gx + v^2)}$"
    )
    ax_calc.text(0.35, 4.30, sol_text, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드: 실시간 물리량 모니터
    live_text = (
        f"[실시간 저울 계측 모니터: $L={L:.1f}\\ \\mathrm{{m}},\\ \\rho={rho:.1f}\\ \\mathrm{{kg/m}},\\ v={v:.1f}\\ \\mathrm{{m/s}}$]\n"
        f"• 상단 지지력: $P(x) = \\rho g(L-x) = {P_curr:.1f}\\ \\mathrm{{N}}$\n"
        f"• 저울 위 쌓인 자중: $\\rho gx = {W_pile:.1f}\\ \\mathrm{{N}}$   |   낙하 충격력: $\\rho v^2 = {F_imp:.1f}\\ \\mathrm{{N}}$\n"
        f"• 현재 저울 눈금: $\\mathbf{{R(x) = {R_curr:.1f}\\ \\mathrm{{N}}}}$ (완전 하강 직전 최대 ${R_max:.1f}\\ \\mathrm{{N}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_64_chain_lowering_scale.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
