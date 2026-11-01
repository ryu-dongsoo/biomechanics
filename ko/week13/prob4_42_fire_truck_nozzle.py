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
문제 4/42 (Problem 4/42) - 소방 사다리 트럭의 방수 노즐 분출 속도 v 및 조인트 A의 추가 지지 모멘트 M
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 정량 검증:
  * 스프링 상수 k = 15 kN/m = 15000 N/m, 스프링 압축 변형량 x = 150 mm = 0.150 m
  * 노즐 출구 지름 d = 30 mm = 0.030 m -> 단면적 A = (pi/4)*(0.030)^2 = 7.0686e-4 m^2
  * 질량유량 m' = rho * A * v = 1000 * 7.0686e-4 * v = 0.7069 * v (kg/s)
  * 1) 수평 운동량 방정식 (kx = m' * Delta v):
       15000 * (0.150) = 0.7069 * v * (v - 0) -> 2250 = 0.7069 * v^2 -> v^2 = 3183 -> v = 56.4 m/s
  * 2) 조인트 A의 각운동량 방정식 (Sigma M_A = m' * v * d_arm):
       d_arm = 15*sin(75 deg) - 4.8*cos(75 deg) = 14.489 - 1.242 = 13.25 m
       M = (15 * 150) * (15*sin(75 deg) - 4.8*cos(75 deg)) = 2250 * (13.25) = 29,800 N*m = 29.8 kN*m
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
rho = 1000.0
d_noz = 0.030
A_noz = 0.25 * np.pi * d_noz**2   # 7.0686e-4 m^2
k_sp = 15000.0                    # 15 kN/m
x_sp_max = 0.150                  # 150 mm

F_sp_max = k_sp * x_sp_max        # 2250 N
v_final = np.sqrt(F_sp_max / (rho * A_noz))  # 56.419 m/s -> 56.4 m/s
m_dot_final = rho * A_noz * v_final          # 39.88 kg/s

L1 = 15.0                         # 주 사다리 길이 (m)
L2 = 4.8                          # 상단 보조 붐 길이 (m)
ang1_deg = 75.0
ang1 = np.radians(ang1_deg)

# 조인트 A로부터 수평 노즐 분출선까지의 수직 모멘트 팔 길이 d_arm
d_arm = L1 * np.sin(ang1) - L2 * np.cos(ang1)  # 13.2466 m (~= 13.25 m)
M_final = F_sp_max * d_arm                     # 29,804.8 N*m -> 29.8 kN*m

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_spring(ax, x0, x1, y_c, n_coils=7, amp=0.18):
    xs = np.linspace(x0, x1, n_coils * 2 + 3)
    ys = np.full_like(xs, y_c)
    for i in range(1, len(xs) - 1):
        ys[i] = y_c + (amp if i % 2 == 1 else -amp)
    ax.plot(xs, ys, color='#37474f', lw=1.8, zorder=4)


def draw_truck_wheel(ax, wx, wy, r=0.26):
    ax.add_patch(patches.Circle((wx, wy), r, facecolor='#455a64', edgecolor='#111111', lw=1.6, zorder=6))
    ax.add_patch(patches.Circle((wx, wy), r * 0.52, facecolor='#cfd8dc', edgecolor='#263238', lw=1.1, zorder=7))


def update(frame):
    # 펌프 가동으로 수류가 차오르며 트럭이 우측 스프링을 150 mm까지 압축해 평형에 도달하는 과정
    prog = min(1.0, frame / 28.0)
    smooth_p = 0.5 - 0.5 * np.cos(np.pi * prog)
    x_sp_curr = x_sp_max * smooth_p
    F_curr = k_sp * x_sp_curr
    v_curr = v_final * np.sqrt(smooth_p)
    M_curr = F_curr * d_arm
    phase_t = (frame * 0.10) % 1.0

    # 시각적 트럭 우측 이동 오프셋 (최대 0.28 유닛)
    dx_plot = 0.28 * smooth_p

    # ---------------- 1. 좌측 패널: 소방 사다리 트럭 및 굴절 사다리 물리 거동 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(0.5, 8.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    y_gnd = 1.25
    x_wall = 8.95

    # 지면 및 우측 수직 벽체 (해칭 배경)
    ax_main.fill_between([0.4, x_wall + 0.35], y_gnd - 0.40, y_gnd, color='#e5dfd5', zorder=1)
    ax_main.fill_between([x_wall, x_wall + 0.35], y_gnd - 0.40, 2.35, color='#e5dfd5', zorder=1)
    ax_main.plot([0.4, x_wall], [y_gnd, y_gnd], color='#333333', lw=2.0, zorder=3)
    ax_main.plot([x_wall, x_wall], [y_gnd, 2.35], color='#333333', lw=2.0, zorder=3)

    # 트럭 기준 위치 (조인트 A 좌표)
    x_A = 6.75 + dx_plot
    y_A = 2.28

    # 1) 소방차 차체 및 캡 (교재 그림 스타일: 빨강/노랑/하늘색 소방 트럭)
    # 하부 샤시
    ax_main.add_patch(patches.Rectangle((3.95 + dx_plot, 1.48), 4.15, 0.22,
                                        facecolor='#78909c', edgecolor='#263238', lw=1.4, zorder=4))
    # 후방 화물/펌프 바디 (빨강 + 노랑 스트라이프)
    ax_main.add_patch(patches.Rectangle((4.15 + dx_plot, 1.70), 2.95, 0.48,
                                        facecolor='#e53935', edgecolor='#263238', lw=1.5, zorder=4))
    ax_main.add_patch(patches.Rectangle((4.15 + dx_plot, 1.82), 2.95, 0.12,
                                        facecolor='#fdd835', edgecolor='#263238', lw=0.8, zorder=5))
    # 운전석 캡 (우측 전방)
    cab_poly = np.array([
        [7.15 + dx_plot, 1.70],
        [8.08 + dx_plot, 1.70],
        [8.08 + dx_plot, 2.08],
        [7.92 + dx_plot, 2.38],
        [7.15 + dx_plot, 2.38]
    ])
    ax_main.add_patch(patches.Polygon(cab_poly, facecolor='#e53935', edgecolor='#263238', lw=1.5, zorder=4))
    # 운전석 창문
    win_poly = np.array([
        [7.52 + dx_plot, 2.04],
        [7.98 + dx_plot, 2.04],
        [7.86 + dx_plot, 2.30],
        [7.52 + dx_plot, 2.30]
    ])
    ax_main.add_patch(patches.Polygon(win_poly, facecolor='#4fc3f7', edgecolor='#01579b', lw=1.1, zorder=5))
    # 경광등
    ax_main.add_patch(patches.Circle((7.45 + dx_plot, 2.43), 0.06, facecolor='#d50000', edgecolor='#263238', lw=1.0, zorder=5))

    # 바퀴 3개 (후방 복륜 2축 + 전방 조향축 1개)
    for wx_off in [4.75, 5.45, 7.55]:
        draw_truck_wheel(ax_main, wx_off + dx_plot, y_gnd + 0.26, r=0.26)

    # 우측 범퍼와 벽체 사이 완충 스프링 (k = 15 kN/m)
    draw_spring(ax_main, 8.08 + dx_plot, x_wall, y_c=1.68, n_coils=6, amp=0.17)

    # 2) 사다리 회전 포탑(Turntable) 및 조인트 A
    turntable = np.array([
        [x_A - 0.35, 2.18],
        [x_A + 0.35, 2.18],
        [x_A + 0.22, y_A + 0.08],
        [x_A - 0.22, y_A + 0.08]
    ])
    ax_main.add_patch(patches.Polygon(turntable, facecolor='#cfd8dc', edgecolor='#263238', lw=1.5, zorder=5))

    # 3) 굴절 사다리 기하학 (스케일 s_len = 0.32 units/m: 15 m -> 4.80 units, 4.8 m -> 1.536 units)
    s_len = 0.32
    L1_p = L1 * s_len   # 4.80
    L2_p = L2 * s_len   # 1.536

    # 주 사다리 방향 (좌상향 75도: 벡터 (-cos 75, +sin 75))
    u1 = np.array([-np.cos(ang1), np.sin(ang1)])
    n1 = np.array([np.sin(ang1), np.cos(ang1)])

    p_A = np.array([x_A, y_A])
    p_B = p_A + L1_p * u1   # 상단 굴절 조인트 B

    # 상단 보조 붐 방향 (주 사다리와 90도 직각, 좌하향 15도: 벡터 (-sin 75, -cos 75))
    u2 = np.array([-np.sin(ang1), -np.cos(ang1)])
    n2 = np.array([-np.cos(ang1), np.sin(ang1)])
    p_C = p_B + L2_p * u2   # 노즐 조인트 C

    # 주 사다리 3단 텔레스코픽 붐 그리기 (황갈색, 교재 원도 동일)
    for seg_i, (f0, f1, w_boom) in enumerate([(0.0, 0.36, 0.24), (0.36, 0.70, 0.19), (0.70, 1.0, 0.14)]):
        pa = p_A + (f0 * L1_p) * u1
        pb = p_A + (f1 * L1_p) * u1
        poly_seg = np.array([
            pa - (w_boom / 2) * n1,
            pb - (w_boom / 2) * n1,
            pb + (w_boom / 2) * n1,
            pa + (w_boom / 2) * n1
        ])
        ax_main.add_patch(patches.Polygon(poly_seg, facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=4))

    # 상단 보조 붐 (4.8 m)
    w2 = 0.12
    poly_boom2 = np.array([
        p_B - (w2 / 2) * n2,
        p_C - (w2 / 2) * n2,
        p_C + (w2 / 2) * n2,
        p_B + (w2 / 2) * n2
    ])
    ax_main.add_patch(patches.Polygon(poly_boom2, facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=5))

    # 조인트 A, B, C 원형 핀 마커
    for pt_j in [p_A, p_B, p_C]:
        ax_main.add_patch(patches.Circle(pt_j, 0.09, facecolor='#ffffff', edgecolor='#263238', lw=1.6, zorder=6))
        ax_main.plot(pt_j[0], pt_j[1], 'ko', markersize=3.2, zorder=7)
    ax_main.text(p_A[0] + 0.24, p_A[1] + 0.18, r'$A$', fontsize=12, fontweight='bold', color='#111111')

    # 4) 노즐 헤드 어셈블리 (p_C에서 수평 좌측으로 방수)
    ax_main.add_patch(patches.Rectangle((p_C[0] - 0.32, p_C[1] - 0.13), 0.38, 0.26,
                                        facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=5))
    ax_main.add_patch(patches.Rectangle((p_C[0] - 0.48, p_C[1] - 0.07), 0.16, 0.14,
                                        facecolor='#bcaaa4', edgecolor='#3e2723', lw=1.4, zorder=5))
    noz_tip = np.array([p_C[0] - 0.48, p_C[1]])

    # 5) 수평 분출 수류 (Water Stream) 및 속도 벡터 v
    if smooth_p > 0.02:
        jet_len = 2.35
        s_w = np.linspace(0, jet_len, 30)
        xw = noz_tip[0] - s_w
        yw_up = noz_tip[1] + 0.06 + 0.04 * (s_w / jet_len)
        yw_lo = noz_tip[1] - 0.06 - 0.04 * (s_w / jet_len)
        ax_main.fill_between(xw, yw_lo, yw_up, color='#bbdefb', alpha=0.88, zorder=3)
        ax_main.plot(xw, yw_up, color='#64b5f6', lw=1.1, zorder=4)
        ax_main.plot(xw, yw_lo, color='#64b5f6', lw=1.1, zorder=4)

        # 물 입자 이동 마커
        for k in range(5):
            frac = ((k / 5.0) + phase_t) % 1.0
            ax_main.plot(noz_tip[0] - frac * jet_len, noz_tip[1], 'o', color='#0277bd', markersize=4.0, zorder=5)

        # 속도 화살표 v (초록색, 좌향)
        ax_main.annotate('', xy=(noz_tip[0] - 1.15, noz_tip[1]), xytext=(noz_tip[0] - 0.15, noz_tip[1]),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13), zorder=6)
        ax_main.text(noz_tip[0] - 0.65, noz_tip[1] + 0.22, f'$v = {v_curr:.1f}\\ \\mathrm{{m/s}}$',
                     fontsize=10.8, fontweight='bold', color='#00695c', ha='center')

    # 6) 치수선 및 각도 표시 (75 deg, 90 deg, 15 m, 4.8 m — 교재 원도 1:1 배치)
    # 75도 각도 (p_A 좌측 수평선 기준)
    ax_main.plot([p_A[0] - 1.1, p_A[0] - 0.2], [p_A[1], p_A[1]], color='#444444', ls='--', lw=1.1)
    arc_75 = patches.Arc(p_A, 1.35, 1.35, angle=0, theta1=105, theta2=180, color='#222222', lw=1.3)
    ax_main.add_patch(arc_75)
    ax_main.text(p_A[0] - 0.92, p_A[1] + 0.38, r'$75^\circ$', fontsize=10.5, fontweight='bold')

    # 90도 직각 표시 (상단 굴절 조인트 p_B 하단 내측)
    arc_90 = patches.Arc(p_B, 0.95, 0.95, angle=0, theta1=-75, theta2=-165, color='#222222', lw=1.3)
    ax_main.add_patch(arc_90)
    ax_main.text(p_B[0] - 0.45, p_B[1] - 0.58, r'$90^\circ$', fontsize=10.2, fontweight='bold', ha='center')

    # 15 m 치수선 (주 사다리 우측 평행 오프셋)
    off_15 = 0.72 * n1
    pA_d = p_A + off_15
    pB_d = p_B + off_15
    ax_main.plot([p_A[0] + 0.2*n1[0], pA_d[0] + 0.15*n1[0]], [p_A[1] + 0.2*n1[1], pA_d[1] + 0.15*n1[1]], color='#666666', lw=0.9)
    ax_main.plot([p_B[0] + 0.2*n1[0], pB_d[0] + 0.15*n1[0]], [p_B[1] + 0.2*n1[1], pB_d[1] + 0.15*n1[1]], color='#666666', lw=0.9)
    ax_main.annotate('', xy=pB_d, xytext=pA_d, arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    mid_15 = 0.5 * (pA_d + pB_d)
    ax_main.text(mid_15[0] + 0.12, mid_15[1], '15 m', fontsize=10.5, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.1', facecolor='#ffffff', edgecolor='none'))

    # 4.8 m 치수선 (상단 보조 붐 상단 평행 오프셋)
    off_48 = 0.52 * n2
    pB_d2 = p_B + off_48
    pC_d2 = p_C + off_48
    ax_main.plot([p_B[0] + 0.12*n2[0], pB_d2[0] + 0.12*n2[0]], [p_B[1] + 0.12*n2[1], pB_d2[1] + 0.12*n2[1]], color='#666666', lw=0.9)
    ax_main.plot([p_C[0] + 0.12*n2[0], pC_d2[0] + 0.12*n2[0]], [p_C[1] + 0.12*n2[1], pC_d2[1] + 0.12*n2[1]], color='#666666', lw=0.9)
    ax_main.annotate('', xy=pC_d2, xytext=pB_d2, arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    mid_48 = 0.5 * (pB_d2 + pC_d2)
    ax_main.text(mid_48[0], mid_48[1] + 0.18, '4.8 m', fontsize=10.2, fontweight='bold', ha='center')

    ax_main.set_title('문제 4/42: 소방 사다리 트럭의 방수 노즐 속도 $v$ 및 모멘트 $M$', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 모멘트 팔 기하학 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단(y: 6.5 ~ 9.6): 사다리 구조물 FBD 및 수직 모멘트 팔 길이 d = 13.25 m 도해
    ax_calc.text(5.0, 9.55, '사다리 검사체적 FBD 및 조인트 $A$에 대한 모멘트 팔($d$) 기하학',
                 fontsize=10.8, fontweight='bold', ha='center', color='#1d4564')

    # 간략화된 사다리 골격 도해 (A: (6.2, 6.65) -> B: (5.6, 8.95) -> C: (4.3, 8.60))
    A_f = np.array([6.2, 6.65])
    B_f = np.array([5.55, 9.05])
    C_f = np.array([4.25, 8.70])
    ax_calc.plot([A_f[0], B_f[0], C_f[0]], [A_f[1], B_f[1], C_f[1]], color='#8d6e63', lw=3.2, zorder=3)
    ax_calc.plot(A_f[0], A_f[1], 'ko', markersize=5, zorder=5)
    ax_calc.text(A_f[0] + 0.22, A_f[1] - 0.05, r'$A$', fontsize=11, fontweight='bold')

    # C에서 좌측으로 나가는 수류 운동량 m'v 화살표
    ax_calc.annotate('', xy=(2.5, C_f[1]), xytext=C_f,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
    ax_calc.text(2.4, C_f[1], r"$m' v = kx = 2250\ \mathrm{N}$",
                 fontsize=9.8, fontweight='bold', color='#2e7d32', ha='right', va='center')

    # 수직 모멘트 팔 d = 15 sin 75 - 4.8 cos 75 = 13.25 m 치수선
    x_d_line = 7.45
    ax_calc.plot([A_f[0], x_d_line + 0.15], [A_f[1], A_f[1]], color='#777777', ls='--', lw=1.0)
    ax_calc.plot([C_f[0], x_d_line + 0.15], [C_f[1], C_f[1]], color='#777777', ls='--', lw=1.0)
    ax_calc.annotate('', xy=(x_d_line, C_f[1]), xytext=(x_d_line, A_f[1]),
                     arrowprops=dict(arrowstyle='<->', color='#d32f2f', lw=1.6))
    ax_calc.text(x_d_line + 0.18, 0.5 * (A_f[1] + C_f[1]),
                 r'$d = 15\sin 75^\circ - 4.8\cos 75^\circ$' + '\n' + r'$= 13.25\ \mathrm{m}$',
                 fontsize=9.3, fontweight='bold', color='#d32f2f', va='center')

    # 조인트 A에 작용하는 반력 모멘트 M
    arc_ma = patches.Arc(A_f, 1.0, 1.0, angle=0, theta1=160, theta2=310, color='#d32f2f', lw=2.2)
    ax_calc.add_patch(arc_ma)
    ax_calc.text(A_f[0] - 0.85, A_f[1] - 0.35, r'$M$', fontsize=11, fontweight='bold', color='#d32f2f')

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (" + r"$\Sigma F_x = m'\Delta v,\ \Sigma M_A = m' v d$" + ")]\n"
        r"1) 노즐 질량유량 ($d = 30\ \mathrm{mm}$):" + "\n"
        r"   $m' = \rho A v = 1000\left(\frac{\pi}{4}\right)(0.030)^2 v = 0.7069 v\ [\mathrm{kg/s}]$" + "\n"
        r"2) 스프링 압축 평형($kx = m'\Delta v$)을 통한 분출 속도 $v$ 계산:" + "\n"
        r"   $15,000(0.150) = 0.7069 v(v - 0) \Rightarrow v^2 = 3183 \Rightarrow \mathbf{v = 56.4\ \mathrm{m/s}}$" + "\n"
        r"3) 조인트 $A$에서 추가로 지지해야 하는 모멘트 $M$ ($\Sigma M_A = m' v d$):" + "\n"
        r"   $M = 15(150)(15\sin 75^\circ - 4.8\cos 75^\circ) = 2250(13.25)$" + "\n"
        r"   $\Rightarrow M = 29,800\ \mathrm{N\cdot m} \approx \mathbf{29.8\ \mathrm{kN\cdot m}}$"
    )
    ax_calc.text(5.0, 3.85, sol_text, fontsize=9.3, ha='center', va='center', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    live_text = (
        f"[실시간 물리량 모니터 ($k = 15\\ \\mathrm{{kN/m}},\\ x = {x_sp_curr*1000:.1f}\\ /\\ 150.0\\ \\mathrm{{mm}}$)]\n"
        f"스프링 반력: $kx = {F_curr:.0f}\\ \\mathrm{{N}}$  |  모멘트 팔: $d = {d_arm:.2f}\\ \\mathrm{{m}}$\n"
        f"현재: $v = {v_curr:.1f}\\ \\mathrm{{m/s}},\\ M = {M_curr/1000:.2f}\\ \\mathrm{{kN\\cdot m}}$  |  "
        f"이론 최종값: $\\mathbf{{v = 56.4\\ \\mathrm{{m/s}},\\ M = 29.8\\ \\mathrm{{kN\\cdot m}}}}$"
    )
    ax_calc.text(5.0, 1.05, live_text, fontsize=9.3, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_42_fire_truck_nozzle.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
