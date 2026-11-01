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
동역학 9판 제4장: 질점계의 운동역학
심화문제 1 - 문제 4/11 (Problem 4/11) - 네 개의 10 kg 원통과 도르래 시스템의 질량중심 가속도 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (4개의 10 kg 실린더, 도르래 4개, 500 N 및 250 N)
- 이론 정량 검증 완료:
  * 시스템 경계 상단 외력 합: 500 N + 250 N + 250 N = 1000 N (연직 상방)
  * 시스템 총 중량: 4 * 10 kg * 9.81 m/s^2 = 392.4 N (연직 하방)
  * Sigma F_y = m_tot * a_bar => 500 + 250 + 250 - 40(9.81) = 40 * a_bar
  * 40 * a_bar = 1000 - 392.4 = 607.6 N => a_bar = 15.19 m/s^2 (연직 상방)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 및 수식 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
g = 9.81
m_cyl = 10.0
m_tot = 40.0
W_cyl = m_cyl * g               # 98.1 N
W_tot = m_tot * g               # 392.4 N
F_up_tot = 500.0 + 250.0 + 250.0 # 1000.0 N
a_bar = (F_up_tot - W_tot) / m_tot # 15.19 m/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.22, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_pulley(ax, cx, cy, r_p=0.22):
    p = patches.Circle((cx, cy), r_p, facecolor='#bde0f5', edgecolor='#1d4564', lw=1.8, zorder=5)
    pin = patches.Circle((cx, cy), 0.045, facecolor='#222222', edgecolor='none', zorder=6)
    ax.add_patch(p)
    ax.add_patch(pin)

def draw_cylinder(ax, cx, y_top_cyl, w_c=0.52, h_c=0.92):
    rect = patches.Rectangle((cx - w_c/2, y_top_cyl - h_c), w_c, h_c,
                             facecolor='#d99b82', edgecolor='#59281a', lw=1.8, zorder=5)
    ax.add_patch(rect)
    # 입체 하이라이트 스트라이프
    hl = patches.Rectangle((cx - w_c/2 + 0.06, y_top_cyl - h_c + 0.03), 0.10, h_c - 0.06,
                           facecolor='#f0c9b8', edgecolor='none', zorder=6)
    ax.add_patch(hl)
    # 상단 고리 러그
    lug = patches.Circle((cx, y_top_cyl), 0.038, facecolor='#222222', edgecolor='none', zorder=4)
    ax.add_patch(lug)
    ax.text(cx, y_top_cyl - 0.5*h_c, '10\nkg', fontsize=11, fontweight='bold', color='#222222', ha='center', va='center', zorder=7)

def update(frame):
    t = t_vals[frame]
    dy_G = 0.5 * a_bar * t**2
    v_G = a_bar * t
    
    # 시각적 애니메이션을 위한 스케일 이동량
    s = 1.6 * dy_G
    
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.65, 2.45)
    ax_main.set_ylim(-0.3, 5.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    r_p = 0.22
    # 도르래 X 좌표: 좌측 하단 P_L1, 중앙 상단 P_U1, 중앙 하단 P_L2, 우측 상단 P_U2
    x_PL1 = -0.88
    x_PU1 = -0.44
    x_PL2 = 0.00
    x_PU2 = 0.44
    x_C4  = 0.66
    
    y_PU1 = 4.45
    y_PU2 = 4.45
    y_PL1 = 2.15 + 1.15 * s
    y_PL2 = 2.15 + 0.85 * s
    
    y_cyl1_top = y_PL1 - 0.48
    y_cyl2_top = 3.55 + 0.95 * s
    y_cyl3_top = y_PL2 - 0.48
    y_cyl4_top = 3.55 + 1.05 * s
    
    # 로프 선 그리기 (교재 원도와 1:1 일치하는 로프 및 좌측 천장 지지부 구조)
    x_ceil = x_PL1 - r_p
    y_ceil = 5.22
    ax_main.fill_between([x_ceil - 0.36, x_ceil + 0.28], y_ceil, y_ceil + 0.22, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.plot([x_ceil - 0.36, x_ceil + 0.28], [y_ceil, y_ceil], color='#222222', lw=2.3, zorder=3)
    for hx in np.linspace(x_ceil - 0.30, x_ceil + 0.16, 5):
        ax_main.plot([hx, hx + 0.10], [y_ceil, y_ceil + 0.18], color='#555555', lw=1.0, zorder=2)
    ax_main.plot(x_ceil, y_ceil, 'ko', markersize=4.5, zorder=5)

    # 1) 좌측 하단 도르래 PL1을 감싸는 로프 (좌측 끝은 천장 고정 지지부로 250 N 반력 작용, 우측은 상단 도르래 PU1으로 연결)
    ax_main.plot([x_ceil, x_ceil], [y_PL1, y_ceil], color='#333333', lw=1.8, zorder=3)
    ax_main.plot([x_PL1 + r_p, x_PL1 + r_p], [y_PL1, y_PU1], color='#333333', lw=1.8, zorder=3)
    # PL1 중심에서 원통 1 연결봉
    ax_main.plot([x_PL1, x_PL1], [y_cyl1_top, y_PL1], color='#333333', lw=2.2, zorder=4)
    
    # 2) 상단 좌측 도르래 PU1 우측 줄 -> 중앙 상단 원통 2 연결
    ax_main.plot([x_PU1 + r_p, x_PU1 + r_p], [y_cyl2_top, y_PU1], color='#333333', lw=1.8, zorder=3)
    # PU1 중심 상단 500 N 작용선
    ax_main.annotate('', xy=(x_PU1, y_PU1 + 0.72), xytext=(x_PU1, y_PU1),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14), zorder=8)
    ax_main.text(x_PU1 + 0.10, y_PU1 + 0.68, '500 N', color='#d32f2f', fontsize=11.5, fontweight='bold', ha='left', va='center')
    
    # 3) 원통 2 하단에서 하단 우측 도르래 PL2 좌측 줄로 연결
    ax_main.plot([x_PL2 - r_p, x_PL2 - r_p], [y_PL2, y_cyl2_top - 0.92], color='#333333', lw=1.8, zorder=3)
    lug_bot2 = patches.Circle((x_PL2 - r_p, y_cyl2_top - 0.92), 0.032, facecolor='#222222', edgecolor='none', zorder=4)
    ax_main.add_patch(lug_bot2)
    # PL2 중심에서 원통 3 연결봉
    ax_main.plot([x_PL2, x_PL2], [y_cyl3_top, y_PL2], color='#333333', lw=2.2, zorder=4)
    
    # 4) PL2 우측 줄 -> 상단 우측 도르래 PU2 좌측 줄 -> PU2 우측 줄에서 원통 4 연결
    ax_main.plot([x_PL2 + r_p, x_PL2 + r_p], [y_PL2, y_PU2], color='#333333', lw=1.8, zorder=3)
    ax_main.plot([x_PU2 + r_p, x_PU2 + r_p], [y_cyl4_top, y_PU2], color='#333333', lw=1.8, zorder=3)
    # PU2 중심 상단 지지 로프 (250 N 장력)
    ax_main.annotate('', xy=(x_PU2, y_PU2 + 0.72), xytext=(x_PU2, y_PU2),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14), zorder=8)
    ax_main.text(x_PU2 + 0.12, y_PU2 + 0.68, '250 N', color='#d32f2f', fontsize=11.5, fontweight='bold', ha='left', va='center')
    
    # 좌측 천장 지지 로프의 시스템 경계 상향 장력 (250 N) 표시
    ax_main.annotate('', xy=(x_ceil, 5.10), xytext=(x_ceil, 4.55),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13), zorder=8)
    ax_main.text(x_ceil - 0.12, 4.84, '250 N', color='#d32f2f', fontsize=11, fontweight='bold', ha='right', va='center')
    
    # 도르래 4개 그리기
    draw_pulley(ax_main, x_PU1, y_PU1, r_p)
    draw_pulley(ax_main, x_PU2, y_PU2, r_p)
    draw_pulley(ax_main, x_PL1, y_PL1, r_p)
    draw_pulley(ax_main, x_PL2, y_PL2, r_p)
    
    # 10 kg 원통 4개 그리기
    draw_cylinder(ax_main, x_PL1, y_cyl1_top)
    draw_cylinder(ax_main, x_PU1 + r_p, y_cyl2_top)
    draw_cylinder(ax_main, x_PL2, y_cyl3_top)
    draw_cylinder(ax_main, x_C4, y_cyl4_top)
    
    # 시스템 경계 박스 (점선) 및 질량중심 가속도 a_bar 표시
    sys_box = patches.Rectangle((-1.32, 0.45 + 0.8*s), 2.42, 4.25 - 0.4*s,
                                facecolor='none', edgecolor='#1565c0', ls='--', lw=1.5, zorder=2)
    ax_main.add_patch(sys_box)
    ax_main.text(1.18, 4.45, '시스템 경계\n(System Boundary)', fontsize=9.5, fontweight='bold', color='#1565c0', va='top')
    
    y_G_curr = 0.25 * (y_cyl1_top + y_cyl2_top + y_cyl3_top + y_cyl4_top) - 0.46
    ax_main.plot(-0.12, y_G_curr, marker='D', markersize=8, markerfacecolor='#ffeb3b', markeredgecolor='#1565c0', markeredgewidth=1.8, zorder=9)
    ax_main.annotate('', xy=(-1.98, y_G_curr + 0.75), xytext=(-1.98, y_G_curr - 0.15),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(-1.98, y_G_curr + 0.90, r'$\bar{a} = 15.19\ \mathrm{m/s^2}\ (\uparrow)$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='center')
    
    ax_main.set_title('문제 4/11: 네 개의 10 kg 원통과 복합 도르래 시스템', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. 시스템 자유물체도 및 정량 유도 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "이론 해석 및 정량 유도 (4개 원통 통합 시스템 경계):\n"
        "1) 무질량 도르래 정역학에 의한 상단 외력 규명:\n"
        r"  $\bullet$ 좌측 상단 도르래($500\ \mathrm{N}$) 양측 줄의 장력: 각 $250\ \mathrm{N}$ (동일 로프)" "\n"
        r"  $\bullet$ 좌측 천장 지지부에 연결된 줄도 같은 로프이므로 $250\ \mathrm{N}$ 상향 반력 작용!" "\n"
        r"  $\bullet$ 따라서 시스템 경계 상단을 당기는 총 상향 외력은:" "\n"
        r"     $\sum F_{\mathrm{up}} = 250\ \mathrm{N}$ (좌측 천장 줄) $+ 500\ \mathrm{N}$ (중앙) $+ 250\ \mathrm{N}$ (우측) $= 1000\ \mathrm{N}$" "\n\n"
        "2) 시스템 총 질량 및 총 중량:\n"
        r"  $\bullet\ m_{\mathrm{tot}} = 4 \times 10\ \mathrm{kg} = 40\ \mathrm{kg},\quad W_{\mathrm{tot}} = 40(9.81) = 392.4\ \mathrm{N}\ (\downarrow)$" "\n\n"
        r"3) 일반화된 뉴턴 제2법칙 ($\sum F_y = m_{\mathrm{tot}}\bar{a}_y$, +y: 상방):" "\n"
        r"  $\bullet\ 500 + 250 + 250 - 40(9.81) = 40\bar{a}$" "\n"
        r"  $\bullet\ 40\bar{a} = 1000 - 392.4 = 607.6\ \mathrm{N} \Rightarrow \mathbf{\bar{a} = 15.19\ \mathrm{m/s^2}}\ (\uparrow)$"
    )
    ax_calc.text(0.35, 5.95, sol_box, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"실시간 질량중심 상태 모니터 ($t = {t:.2f}\\ \\mathrm{{s}}$):\n"
        f"상향 외력 합: $+1000.0\\ \\mathrm{{N}}$,  하향 중량 합: $-392.4\\ \\mathrm{{N}}$\n"
        f"알짜 외력: $\\sum F_y = +607.6\\ \\mathrm{{N}}$,  총 질량: $m = 40.0\\ \\mathrm{{kg}}$\n"
        f"질량중심 가속도: $\\bar{{a}} = \\mathbf{{15.19\\ \\mathrm{{m/s^2}}}}\\ (\\uparrow)$,  현재 속도: $\\bar{{v}} = {v_G:.2f}\\ \\mathrm{{m/s}}$"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('시스템 경계 외력 합산 및 질량중심 가속도 검증', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_11_four_cylinders_pulley.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
