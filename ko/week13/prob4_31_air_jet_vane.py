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
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
문제 4/31 (Problem 4/31) - 수직 대칭 분기 날개(Splitter Vane)에 충돌하는 공기 제트 반력 F
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 정량 검증:
  * 공기 밀도 rho = 1.206 kg/m^3, 유량 Q = 0.2 m^3/s, 분사 속력 v = 100 m/s
  * 질량유량 m' = rho * Q = 1.206 * 0.2 = 0.2412 kg/s (~= 0.241 kg/s)
  * Sigma F_x = m' * Delta v_x -> F = 0.2412 * (0 - (-100)) = 24.12 N -> F = 24.1 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터
rho = 1.206           # 공기 밀도 (kg/m^3)
Q = 0.20              # 체적유량 (m^3/s)
v_jet = 100.0         # 노즐 분사 속력 (m/s)
m_dot = rho * Q       # 0.2412 kg/s
F_val = m_dot * v_jet # 24.12 N -> 24.1 N

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_splitter_geometry(x_back=2.8, y_mid=4.2):
    """교재 문제 4/31의 대칭 분기 날개(Splitter Vane) 외곽 좌표 생성"""
    # 날개 뒷면: x = x_back, y = y_mid - 2.3 ~ y_mid + 2.3
    # 날개 두께 상/하단 끝: 0.42, 중앙 뾰족한 커스프(cusp) 정점: (x_back + 1.35, y_mid)
    R_cusp = 0.93
    ang_up = np.linspace(-np.pi / 2, 0.0, 35)
    cx_u, cy_u = x_back + 0.42 + R_cusp, y_mid + R_cusp
    x_curve_u = cx_u - R_cusp * np.cos(ang_up)
    y_curve_u = cy_u + R_cusp * np.sin(ang_up)

    # 좀 더 정확한 4분원 커스프:
    # (x_tip, y_mid)에서 수평 접선 -> (x_back + 0.42, y_mid + R_cusp)에서 수직 접선
    th = np.linspace(0, np.pi / 2, 35)
    x_tip = x_back + 0.42 + R_cusp
    xu = x_tip - R_cusp * (1.0 - np.cos(th))   # th=0 -> x_tip (오류 방지: th=0에서 x=x_tip, y=y_mid 이어야 함)
    # 원 방정식: 중심 (x_tip, y_mid + R_cusp) -> th=-pi/2 (x_tip, y_mid) ~ th=-pi (x_tip - R_cusp, y_mid + R_cusp)
    ang1 = np.linspace(-np.pi / 2, -np.pi, 35)
    xu = x_tip + R_cusp * np.cos(ang1)
    yu = (y_mid + R_cusp) + R_cusp * np.sin(ang1)

    ang2 = np.linspace(np.pi, np.pi / 2, 35)
    xl = x_tip + R_cusp * np.cos(ang2)
    yl = (y_mid - R_cusp) + R_cusp * np.sin(ang2)

    poly_pts = np.vstack([
        [x_back, y_mid - 2.25],
        [x_back + 0.42, y_mid - 2.25],
        np.column_stack([xl, yl]),
        np.column_stack([xu, yu]),
        [x_back + 0.42, y_mid + 2.25],
        [x_back, y_mid + 2.25]
    ])
    return poly_pts, x_tip, R_cusp


vane_pts, x_tip, R_cusp = get_splitter_geometry(x_back=2.8, y_mid=4.2)


def update(frame):
    phase_t = (frame * 0.08) % 1.0
    x_back, y_mid = 2.8, 4.2

    # ---------------- 1. 좌측 패널: 공기 제트 분기 날개 물리 거동 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.4, 9.6)
    ax_main.set_ylim(0.8, 7.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 좌표축 점선 (x축, y축)
    ax_main.plot([1.2, 9.1], [y_mid, y_mid], color='#777777', ls='--', lw=1.1, zorder=1)
    ax_main.text(9.2, y_mid, r'$x$', fontsize=11.5, fontweight='bold', va='center')
    ax_main.plot([x_back + 0.21, x_back + 0.21], [1.2, 7.1], color='#777777', ls='--', lw=1.1, zorder=1)
    ax_main.text(x_back + 0.21, 7.22, r'$y$', fontsize=11.5, fontweight='bold', ha='center')

    # 우측 황동 노즐 (x: 6.4 -> 8.2, 왼쪽으로 공기 분사)
    noz_x_tip = 6.35
    noz_x_base = 8.25
    noz_body = np.array([
        [noz_x_tip, y_mid - 0.36],
        [noz_x_base, y_mid - 0.50],
        [noz_x_base, y_mid + 0.50],
        [noz_x_tip, y_mid + 0.36]
    ])
    ax_main.add_patch(patches.Polygon(noz_body, facecolor='#ecc94b', edgecolor='#5c4811', lw=1.9, zorder=4))
    # 노즐 립(lip) 림
    ax_main.add_patch(patches.FancyBboxPatch((noz_x_tip - 0.12, y_mid - 0.42), 0.16, 0.84,
                                             boxstyle='round,pad=0.04', facecolor='#f6e05e', edgecolor='#5c4811', lw=1.7, zorder=5))

    # 공기 제트 유동 영역 (연한 하늘색 반투명 가이드)
    ax_main.fill_between([x_tip, noz_x_tip], y_mid - 0.32, y_mid + 0.32, color='#e1f5fe', alpha=0.65, zorder=2)

    # 날개 본체 (연청회색 셰이딩, 교재 원도 완벽 재현)
    ax_main.add_patch(patches.Polygon(vane_pts, facecolor='#b3d4e5', edgecolor='#263238', lw=2.0, zorder=4))

    # 유선 화살표 및 이동 공기 입자 애니메이션 (초록색 화살표: 입구 -x, 출구 +y 및 -y)
    # 1) 수평 입사 화살표들
    for y_off in [-0.22, 0.0, 0.22]:
        for x_st in [5.95, 4.95]:
            if y_off == 0.0 and x_st == 5.95:
                continue
            ax_main.annotate('', xy=(x_st - 0.65, y_mid + y_off), xytext=(x_st, y_mid + y_off),
                             arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)
    ax_main.annotate('', xy=(4.75, y_mid), xytext=(5.55, y_mid),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.9, mutation_scale=12), zorder=5)
    ax_main.text(5.35, y_mid - 0.52, r'$v = 100\ \mathrm{m/s}$', fontsize=11, fontweight='bold', color='#00695c', ha='center')

    # 2) 상/하 곡면 분기 화살표들
    for sign in [+1, -1]:
        # 곡면 구간 화살표
        ang_a1 = np.radians(25)
        ang_a2 = np.radians(65)
        p1 = np.array([x_tip - R_cusp * np.sin(ang_a1), y_mid + sign * R_cusp * (1 - np.cos(ang_a1)) + sign * 0.14])
        p2 = np.array([x_tip - R_cusp * np.sin(ang_a2) + 0.14, y_mid + sign * R_cusp * (1 - np.cos(ang_a2)) + sign * 0.14])
        rad_val = -0.25 * sign
        ax_main.annotate('', xy=p2, xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11,
                                         connectionstyle=f'arc3,rad={rad_val}'), zorder=5)
        # 수직 직선 배출 화살표
        xv_line = x_back + 0.62
        y_st1 = y_mid + sign * 1.25
        y_ed1 = y_mid + sign * 1.85
        ax_main.annotate('', xy=(xv_line + 0.08, y_ed1), xytext=(xv_line + 0.08, y_st1),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)
        y_st2 = y_mid + sign * 2.00
        y_ed2 = y_mid + sign * 2.65
        ax_main.annotate('', xy=(xv_line - 0.04, y_ed2), xytext=(xv_line - 0.04, y_st2),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=5)

    # 3) 실시간 이동하는 공기 유체 입자들 (점 애니메이션)
    for k in range(6):
        s_p = ((k / 6.0) + phase_t) % 1.0
        if s_p < 0.45:
            # 수평 구간 (noz_x_tip -> x_tip)
            u_f = s_p / 0.45
            px = noz_x_tip - u_f * (noz_x_tip - x_tip)
            ax_main.plot(px, y_mid + 0.12, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, y_mid - 0.12, 'o', color='#0277bd', markersize=4.5, zorder=6)
        elif s_p < 0.75:
            # 원호 분기 구간
            u_f = (s_p - 0.45) / 0.30
            ang = u_f * (np.pi / 2)
            r_s = R_cusp - 0.16
            px = x_tip - r_s * np.sin(ang)
            py_u = y_mid + R_cusp - r_s * np.cos(ang)
            py_l = y_mid - R_cusp + r_s * np.cos(ang)
            ax_main.plot(px, py_u, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, py_l, 'o', color='#0277bd', markersize=4.5, zorder=6)
        else:
            # 수직 방출 구간
            u_f = (s_p - 0.75) / 0.25
            px = x_back + 0.58
            py_u = (y_mid + R_cusp) + u_f * 1.65
            py_l = (y_mid - R_cusp) - u_f * 1.65
            ax_main.plot(px, py_u, 'o', color='#0277bd', markersize=4.5, zorder=6)
            ax_main.plot(px, py_l, 'o', color='#0277bd', markersize=4.5, zorder=6)

    # 날개 뒷면에 작용하는 고정 지지력 F (붉은색 굵은 화살표, +x 방향)
    ax_main.annotate('', xy=(x_back, y_mid), xytext=(x_back - 1.45, y_mid),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=3.0, mutation_scale=17), zorder=6)
    ax_main.text(x_back - 1.55, y_mid, r'$F = 24.1\ \mathrm{N}$',
                 fontsize=12, fontweight='bold', color='#d32f2f', ha='right', va='center')

    # 제원 안내 배너
    ax_main.text(5.0, 1.15, r'체적유량 $Q = 0.2\ \mathrm{m^3/s}$,  분사속도 $v = 100\ \mathrm{m/s}$,  공기밀도 $\rho = 1.206\ \mathrm{kg/m^3}$',
                 fontsize=10.2, fontweight='bold', color='#1d4564', ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    ax_main.set_title('문제 4/31: 대칭 분기 날개에 충돌하는 공기 제트 반력', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 검사체적 FBD 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단(y: 6.5 ~ 9.6): 검사체적 FBD 및 선운동량 벡터 변화
    ax_calc.text(5.0, 9.50, '날개+공기류 검사체적 자유물체도 (FBD) 및 운동량 변화',
                 fontsize=11.2, fontweight='bold', ha='center', color='#1d4564')

    # 미니 날개 FBD (중심 x=4.6, y=7.85)
    mini_pts = (vane_pts - np.array([x_back, y_mid])) * 0.48 + np.array([4.2, 7.85])
    ax_calc.add_patch(patches.Polygon(mini_pts, facecolor='#e1f5fe', edgecolor='#37474f', lw=1.6))
    # 해칭 표시 (고정 지지)
    ax_calc.annotate('', xy=(4.2, 7.85), xytext=(2.7, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14))
    ax_calc.text(2.55, 7.85, r'$F$', fontsize=11.5, fontweight='bold', color='#d32f2f', ha='right', va='center')

    # 입구 속도 v1x = -100 m/s
    ax_calc.annotate('', xy=(5.2, 7.85), xytext=(6.6, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
    ax_calc.text(6.75, 7.85, r'$v_{1x} = -100\ \mathrm{m/s}$', fontsize=10.0, fontweight='bold', color='#2e7d32', va='center')

    # 상/하 대칭 출구 속도 (v2x = 0)
    ax_calc.annotate('', xy=(4.45, 9.25), xytext=(4.45, 8.65),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.8, mutation_scale=11))
    ax_calc.annotate('', xy=(4.45, 6.45), xytext=(4.45, 7.05),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.8, mutation_scale=11))
    ax_calc.text(4.75, 9.05, r'$v_{2x} = 0$', fontsize=9.8, fontweight='bold', color='#2e7d32')

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (" + r"$\Sigma F_x = m'\Delta v_x$" + ")]\n"
        r"1) 단위시간당 공기 질량유량 ($m'$):" + "\n"
        r"   $m' = \rho Q = 1.206\ \mathrm{kg/m^3} \times 0.2\ \mathrm{m^3/s} = 0.2412\ \mathrm{kg/s}$" + "\n"
        r"2) $x$ 방향 속도 변화량 ($\Delta v_x = v_{2x} - v_{1x}$, 우측 $+x$):" + "\n"
        r"   입구: $v_{1x} = -100\ \mathrm{m/s}$,  출구(수직 분기): $v_{2x} = 0$" + "\n"
        r"   $\Delta v_x = 0 - (-100) = +100\ \mathrm{m/s}$" + "\n"
        r"3) 수평 방향 힘-운동량 방정식:" + "\n"
        r"   $\Sigma F_x = m'\Delta v_x \Rightarrow F = 0.2412(0 - [-100]) = \mathbf{24.1\ \mathrm{N}}$"
    )
    ax_calc.text(5.0, 4.15, sol_text, fontsize=9.7, ha='center', va='center', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.48', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    live_text = (
        f"[정량 검증 요약 ($Q = {Q:.1f}\\ \\mathrm{{m^3/s}},\\ \\rho = {rho:.3f}\\ \\mathrm{{kg/m^3}}$)]\n"
        f"질량유량: $m' = {m_dot:.4f}\\ \\mathrm{{kg/s}} \\approx 0.241\\ \\mathrm{{kg/s}}$  |  "
        f"상·하 $y$방향 운동량은 대칭 상쇄 ($\\Sigma F_y = 0$)\n"
        f"날개 고정에 필요한 수평 지지력 (이론 최종값): $\\mathbf{{F = {F_val:.1f}\\ \\mathrm{{N}}}}$"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.5, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_31_air_jet_vane.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
