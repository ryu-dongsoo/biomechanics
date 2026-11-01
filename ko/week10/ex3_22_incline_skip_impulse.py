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
예제 3.22: 30° 경사면 탄차(Mine Skip)와 케이블 힘 P(t)의 선형 충격량-운동량 해석
동역학 9판 (한국어판) - 제3장 3.9절 선형 충격량과 선형 운동량

문제 조건:
- 짐을 실은 탄차 질량 m = 150 kg, 경사각 θ = 30°
- 동도르래 2:1 감기 구조 (경사면 위쪽 방향 케이블 당김력 = 2P)
- 케이블 힘 P(t): 0 <= t <= 4 s 구간 0 -> 600 N 선형 증가, t > 4 s 구간 600 N 일정
- 초기 속도 v1 = 4 m/s (경사면 아래쪽 방향, +x를 경사면 위쪽으로 두면 v1 = -4 m/s)

이론 해석 결과:
- (a) 탄차가 방향을 바꾸며 정지하는 시각: t' = 4 + Δt = 6.46 s (Δt = 2.46 s)
- (b) t = 8 s에서의 속도: v2 = +4.76 m/s (경사면 위쪽 방향)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 상수
m = 150.0
theta_deg = 30.0
theta_rad = np.radians(theta_deg)
g = 9.81
W_x = m * g * np.sin(theta_rad)   # 735.75 N (경사면 아래쪽)
v1 = -4.0                         # m/s (+x: 경사면 위쪽)
t_stop = 6.46                     # (3000 / 464.25 = 6.462 s)

def get_dynamics(t):
    if t <= 4.0:
        P = 150.0 * t
        # m dv/dt = 2(150 t) - 735.75 => a = 2 t - 4.905
        a = 2.0 * t - 4.905
        v = v1 + t**2 - 4.905 * t
        s = (t**3) / 3.0 - 4.905 * (t**2) / 2.0 + v1 * t
    else:
        P = 600.0
        a = (1200.0 - W_x) / m    # +3.095 m/s^2
        dt4 = t - 4.0
        v4 = v1 + 16.0 - 4.905 * 4.0
        s4 = (64.0 / 3.0) - 4.905 * 8.0 + v1 * 4.0
        v = v4 + a * dt4
        s = s4 + v4 * dt4 + 0.5 * a * (dt4**2)
    return P, a, v, s

_, _, _, s_min = get_dynamics(3000.0 / 464.25)  # -43.29 m

n_frames = 81
t_arr = np.linspace(0.0, 8.0, n_frames)
t_dense = np.linspace(0.0, 8.5, 300)
P_dense = np.array([get_dynamics(tt)[0] for tt in t_dense])
v_dense = np.array([get_dynamics(tt)[2] for tt in t_dense])

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.18, 1.0], height_ratios=[1.05, 1.0],
              left=0.03, right=0.97, top=0.87, bottom=0.09, wspace=0.18, hspace=0.35)

ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])

fig.suptitle("예제 3.22: 경사면 탄차와 케이블 힘 $P(t)$의 선형 충격량-운동량 해석",
             fontsize=14.5, fontweight='bold', color='#111827', y=0.965)

c_th, s_th = np.cos(theta_rad), np.sin(theta_rad)
u_vec = np.array([c_th, s_th])
n_vec = np.array([-s_th, c_th])

P0 = np.array([0.12, 0.24])
L_slope = 3.42
P_step_bot = P0 + L_slope * u_vec                 # (3.082, 1.950)
C_fixed = np.array([P_step_bot[0], P_step_bot[1] + 0.165])  # (3.082, 2.115)
R_f = 0.165
R_m = R_f / 2.0

# 고정 도르래 중심의 경사면 법선 좌표 계산 (평행 케이블 정렬용)
rel_cf = C_fixed - P0
u_cf = np.dot(rel_cf, u_vec)
n_cf = np.dot(rel_cf, n_vec)
n_m = n_cf + R_m  # 동도르래 중심 법선 높이

def to_world(u_c, u_loc, n_loc):
    return P0 + (u_c + u_loc) * u_vec + n_loc * n_vec

def update(frame):
    t_curr = t_arr[frame]
    P_curr, a_curr, v_curr, s_curr = get_dynamics(t_curr)

    ax1.clear()
    ax2.clear()
    ax3.clear()
    for ax in (ax1, ax2, ax3):
        ax.set_facecolor('#ffffff')

    # =====================================================
    # [좌측 패널] 교재 원도 1:1 기하 구조 및 안전 범위 애니메이션
    # =====================================================
    ax1.set_xlim(-0.22, 4.28)
    ax1.set_ylim(-0.18, 2.82)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("교재 그림 1:1 기하 모델 및 운동 시뮬레이션 (+x: 경사면 위쪽)",
                  fontsize=12, fontweight='bold', color='#1e293b', pad=6)

    # 1) 고정 상단 도르래 (단차 모서리 뒤쪽에 반쯤 매립된 교재 원도 표현)
    pulley_f = patches.Circle(C_fixed, R_f, facecolor='#bfe3f7', edgecolor='#1e293b', lw=1.8, zorder=2)
    ax1.add_patch(pulley_f)
    for ang in np.linspace(0, 2*np.pi, 9)[:-1]:
        ax1.plot([C_fixed[0], C_fixed[0] + R_f*0.85*np.cos(ang)],
                 [C_fixed[1], C_fixed[1] + R_f*0.85*np.sin(ang)],
                 color='#7cc4ed', lw=1.0, zorder=2.2)

    # 2) 경사면 및 상단 수평 단차 지반 (교재 원도와 동일한 단면 음영)
    ledge_right_x = 3.56
    ground_poly = np.array([
        [P0[0], P0[1]],
        [P_step_bot[0], P_step_bot[1]],
        [C_fixed[0], C_fixed[1]],
        [ledge_right_x, C_fixed[1]],
        [ledge_right_x, C_fixed[1] - 0.26],
        [P_step_bot[0] + 0.08, P_step_bot[1] - 0.22],
        [P0[0], P0[1] - 0.22]
    ])
    ax1.add_patch(patches.Polygon(ground_poly, facecolor='#dfd9d2', edgecolor='none', zorder=3))
    ax1.plot([P0[0], P_step_bot[0], C_fixed[0], ledge_right_x],
             [P0[1], P_step_bot[1], C_fixed[1], C_fixed[1]],
             color='#1e293b', lw=2.2, zorder=4)

    # 30° 경사각 표시선 (교재 하단 수평 보조선 + 30°)
    ang_base = P0 + 0.62 * u_vec - 0.14 * np.array([0.0, 1.0])
    ax1.plot([ang_base[0], ang_base[0] + 0.72], [ang_base[1], ang_base[1]], color='#475569', lw=1.3, zorder=4)
    ax1.text(ang_base[0] + 0.34, ang_base[1] + 0.04, r"$30^\circ$", fontsize=13, fontweight='bold', color='#111827', ha='center')

    # 초기 위치(s=0) 및 정지 반환점(s=-43.29 m) 기준 마커
    u_min_vis, u_max_vis = 1.32, 2.26
    for u_ref, lbl, col in [(u_max_vis, r"$t=0\ (s=0)$", '#64748b'),
                            (u_min_vis, r"$t'=6.46\ \mathrm{s}\ (v=0)$", '#d97706')]:
        p_tick1 = P0 + u_ref * u_vec
        p_tick2 = p_tick1 - 0.13 * n_vec
        ax1.plot([p_tick1[0], p_tick2[0]], [p_tick1[1], p_tick2[1]], color=col, lw=1.4, ls='--', zorder=4.5)
        ax1.text(p_tick2[0] + 0.05, p_tick2[1] - 0.05, lbl, fontsize=8.8, color=col, fontweight='bold', ha='left', va='top')

    # 3) 실제 변위 s_curr (-43.29 ~ 0 m) -> 화면 안전 구간 [1.24, 2.24] 매핑
    u_c = u_min_vis + ((s_curr - s_min) / (0.0 - s_min)) * (u_max_vis - u_min_vis)
    u_c = float(np.clip(u_c, u_min_vis, u_max_vis))

    # 바퀴 2개 및 사다리꼴 브래킷
    r_wheel = 0.055
    for u_w in [-0.25, 0.25]:
        w_center = to_world(u_c, u_w, r_wheel)
        ax1.add_patch(patches.Circle(w_center, r_wheel, facecolor='#ffffff', edgecolor='#1e293b', lw=1.8, zorder=5))
        ax1.add_patch(patches.Circle(w_center, 0.016, facecolor='#ffffff', edgecolor='#1e293b', lw=1.2, zorder=6.5))
        brk = np.array([
            to_world(u_c, u_w - 0.08, 0.125),
            to_world(u_c, u_w + 0.08, 0.125),
            to_world(u_c, u_w + 0.025, r_wheel - 0.01),
            to_world(u_c, u_w - 0.025, r_wheel - 0.01),
        ])
        ax1.add_patch(patches.Polygon(brk, facecolor='#7da7bc', edgecolor='#1e293b', lw=1.4, zorder=6))

    # 하부 프레임 빔
    beam = np.array([
        to_world(u_c, -0.43, 0.125),
        to_world(u_c,  0.43, 0.125),
        to_world(u_c,  0.43, 0.195),
        to_world(u_c, -0.43, 0.195),
    ])
    ax1.add_patch(patches.Polygon(beam, facecolor='#7da7bc', edgecolor='#1e293b', lw=1.8, zorder=6.2))

    # 광석 더미 (교재 원도와 동일한 상부 회색 자갈 더미)
    ore_pts = [to_world(u_c, -0.42, 0.58)]
    for u_o, n_o in [(-0.34, 0.65), (-0.18, 0.71), (0.02, 0.72), (0.22, 0.68), (0.37, 0.60)]:
        ore_pts.append(to_world(u_c, u_o, n_o))
    ore_pts.append(to_world(u_c, 0.40, 0.58))
    ax1.add_patch(patches.Polygon(np.array(ore_pts), facecolor='#adb5bd', edgecolor='#495057', lw=1.3, zorder=5.8))
    for u_d, n_d in [(-0.26, 0.63), (-0.12, 0.66), (0.04, 0.67), (0.18, 0.64), (-0.04, 0.62), (0.27, 0.61)]:
        pt_d = to_world(u_c, u_d, n_d)
        ax1.plot([pt_d[0], pt_d[0] + 0.025], [pt_d[1], pt_d[1] + 0.01], color='#343a40', lw=1.2, zorder=5.9)

    # 탄차 3패널 사다리꼴 몸체 (교재 원도 블루그레이 + 흰색 내부 패널선)
    body = np.array([
        to_world(u_c, -0.38, 0.195),
        to_world(u_c,  0.38, 0.195),
        to_world(u_c,  0.43, 0.60),
        to_world(u_c, -0.45, 0.60),
    ])
    body_color = '#8fb5c9' if v_curr <= 0 else '#74c69d'
    ax1.add_patch(patches.Polygon(body, facecolor=body_color, edgecolor='#1e293b', lw=1.9, zorder=6.3))

    for p_idx, (ub0, ub1, ut0, ut1) in enumerate([
        (-0.34, -0.14, -0.40, -0.16),
        (-0.10,  0.10, -0.11,  0.11),
        ( 0.14,  0.34,  0.16,  0.38)
    ]):
        panel = np.array([
            to_world(u_c, ub0, 0.23),
            to_world(u_c, ub1, 0.23),
            to_world(u_c, ut1, 0.56),
            to_world(u_c, ut0, 0.56),
        ])
        ax1.add_patch(patches.Polygon(panel, facecolor='none', edgecolor='#f8fafc', lw=1.2, zorder=6.4))

    # 동도르래 및 연결 링크 + 평행 2가닥 케이블 (교재 1:1 라우팅)
    u_mp = u_c + 0.58
    C_mov = P0 + u_mp * u_vec + n_m * n_vec
    hitch_pt = to_world(u_c, 0.43, 0.165)
    ax1.plot([hitch_pt[0], C_mov[0]], [hitch_pt[1], C_mov[1]], color='#1e293b', lw=2.0, zorder=5.5)

    ax1.add_patch(patches.Circle(C_mov, R_m, facecolor='#d0ebff', edgecolor='#1e293b', lw=1.7, zorder=6.0))
    ax1.add_patch(patches.Circle(C_mov, 0.022, facecolor='#ffffff', edgecolor='#1e293b', lw=1.3, zorder=6.6))
    ax1.add_patch(patches.Circle(C_fixed, 0.026, facecolor='#ffffff', edgecolor='#1e293b', lw=1.5, zorder=6.6))

    # 아래쪽 줄: 상단 도르래 중심 핀 -> 동도르래 하단 접점 (경사면과 정확히 평행)
    bot_tan_mov = C_mov - R_m * n_vec
    ax1.plot([C_fixed[0], bot_tan_mov[0]], [C_fixed[1], bot_tan_mov[1]], color='#111827', lw=1.7, zorder=5.2)

    # 위쪽 줄: 동도르래 상단 접점 -> 상단 도르래 상단 접점 (경사면과 정확히 평행)
    top_tan_mov = C_mov + R_m * n_vec
    top_tan_fix = C_fixed + R_f * n_vec
    ax1.plot([top_tan_mov[0], top_tan_fix[0]], [top_tan_mov[1], top_tan_fix[1]], color='#111827', lw=1.7, zorder=5.2)

    # 상단 도르래 꼭대기에서 수평 우측 출구 줄 + 빨간색 화살표 P
    top_horiz_pt = np.array([C_fixed[0], C_fixed[1] + R_f])
    ax1.plot([top_horiz_pt[0], C_fixed[0] + 0.28], [top_horiz_pt[1], top_horiz_pt[1]], color='#111827', lw=1.7, zorder=5.2)
    ax1.annotate('', xy=(C_fixed[0] + 0.86, top_horiz_pt[1]),
                 xytext=(C_fixed[0] + 0.32, top_horiz_pt[1]),
                 arrowprops=dict(arrowstyle='->', color='#e11d48', lw=3.2, mutation_scale=18), zorder=7)
    ax1.text(C_fixed[0] + 0.62, top_horiz_pt[1] - 0.16,
             rf"$P = {P_curr:.0f}\ \mathrm{{N}}$", fontsize=12, fontweight='bold', color='#be123c', ha='center')

    # 속도 화살표 (항상 캔버스 안전 범위 내부에 표시)
    if abs(v_curr) > 0.12:
        v_dir = 1.0 if v_curr > 0 else -1.0
        v_len = np.clip(abs(v_curr) * 0.085, 0.22, 0.44)
        if v_dir < 0:
            v_start = to_world(u_c, -0.48, 0.24)
            v_end = v_start - v_len * u_vec
        else:
            v_start = to_world(u_c, -0.46, 0.42)
            v_end = v_start + v_len * u_vec
        v_col = '#0ca678' if v_curr < 0 else '#1d4ed8'
        ax1.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->', color=v_col, lw=2.6, mutation_scale=15), zorder=7)
        lbl_pos = 0.5 * (v_start + v_end) - 0.13 * n_vec
        v_str = r"$v_1 = 4\ \mathrm{m/s}$" if frame == 0 else rf"$v = {v_curr:+.2f}\ \mathrm{{m/s}}$"
        ax1.text(lbl_pos[0], lbl_pos[1], v_str, fontsize=10.5, fontweight='bold',
                 color=v_col, rotation=30, ha='center', va='center')
    else:
        stop_pt = to_world(u_c, -0.10, 0.82)
        ax1.text(stop_pt[0], stop_pt[1], "순간 정지!\n($v = 0$)", fontsize=10.5, fontweight='bold',
                 color='#d97706', ha='center', bbox=dict(boxstyle='round,pad=0.3', fc='#fef3c7', ec='#f59e0b'))

    # [말풍선 보충 설명] (학생 친화적 도르래 원리 & 부호 설명 + 말풍선 꼬리)
    bubble_text = (
        "[말풍선 보충 설명] 왜 당기는 힘이 2P 일까요?\n"
        "• 탄차 앞의 작은 도르래(동도르래)를 줄 2가닥이 감싸서 당기므로\n"
        "  경사면 위쪽(+x)으로 탄차를 당기는 총 힘은 2P(t)가 됩니다!\n"
        "• 경사면 아래쪽(-x)으로는 무게 성분 mg sin30° = 735.8 N이 계속 작용해요."
    )
    ax1.text(0.02, 2.74, bubble_text, fontsize=9.3, color='#78350f', va='top', ha='left', linespacing=1.38,
             bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.8), zorder=8)

    # 실시간 상태 요약 배지 (우측 하단 여백)
    state_str = (
        f"현재 시각: $t = {t_curr:.2f}\\ \\mathrm{{s}}$\n"
        f"속도: $v = {v_curr:+.2f}\\ \\mathrm{{m/s}}$\n"
        f"경사면 변위: $s = {s_curr:.1f}\\ \\mathrm{{m}}$"
    )
    ax1.text(2.45, 0.52, state_str, fontsize=9.8, fontweight='bold', color='#1e293b',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.3), zorder=8)

    # =====================================================
    # [우측 상단] 교재 P(t) 선도 및 2P(t) 면적 적분 그래프
    # =====================================================
    ax2.set_xlim(0, 8.6)
    ax2.set_ylim(0, 1380)
    ax2.set_ylabel("힘 (N)", fontsize=10, fontweight='bold')
    ax2.set_title(r"케이블 힘 $P(t)$ 및 총 견인력 $2P(t)$의 충격량 면적 ($\int_0^t 2P\,dt$)",
                  fontsize=11, fontweight='bold', color='#1e293b', pad=5)
    ax2.grid(True, ls=':', alpha=0.5)

    ax2.plot(t_dense, P_dense, color='#e11d48', lw=2.0, ls='--', label=r'케이블 힘 $P(t)$ (최대 600 N)')
    ax2.plot(t_dense, 2.0 * P_dense, color='#be123c', lw=2.6, label=r'탄차 견인력 $2P(t)$ (최대 1200 N)')
    ax2.axhline(W_x, color='#475569', lw=1.8, ls='-.', label=r'중력 성분 $mg\sin 30^\circ = 735.8\ \mathrm{N}$')

    mask = t_dense <= t_curr
    ax2.fill_between(t_dense[mask], 0, 2.0 * P_dense[mask], color='#fda4af', alpha=0.38)
    ax2.axvline(4.0, color='#64748b', lw=1.1, ls='--')
    ax2.axvline(t_stop, color='#d97706', lw=1.4, ls='--')
    ax2.axvline(8.0, color='#1d4ed8', lw=1.2, ls='--')
    ax2.plot(t_curr, 2.0 * P_curr, 'o', color='#be123c', markersize=7, zorder=6)

    ax2.text(4.0, 60, "4 s", fontsize=8.8, ha='center', fontweight='bold', color='#475569')
    ax2.text(t_stop, 60, r"$t'=6.46\ \mathrm{s}$", fontsize=8.8, ha='center', fontweight='bold', color='#b45309')
    ax2.text(8.0, 60, "8 s", fontsize=8.8, ha='center', fontweight='bold', color='#1d4ed8')
    ax2.legend(loc='upper left', fontsize=8.3, framealpha=0.92)

    # =====================================================
    # [우측 하단] 속도 v(t) 변화 및 정적분 풀이 요약
    # =====================================================
    ax3.set_xlim(0, 8.6)
    ax3.set_ylim(-10.5, 6.8)
    ax3.set_xlabel("시간 $t$ (s)", fontsize=10, fontweight='bold')
    ax3.set_ylabel("속도 $v$ (m/s)", fontsize=10, fontweight='bold')
    ax3.set_title("탄차 속도 $v(t)$ 응답 및 정적분 해법", fontsize=11, fontweight='bold', color='#1e293b', pad=5)
    ax3.grid(True, ls=':', alpha=0.5)

    ax3.axhline(0, color='#111827', lw=1.2)
    ax3.plot(t_dense, v_dense, color='#1d4ed8', lw=2.5)
    ax3.plot(t_stop, 0.0, 'o', color='#d97706', markersize=7, zorder=5)
    ax3.plot(8.0, 4.76, 's', color='#0ca678', markersize=7, zorder=5)
    ax3.plot(t_curr, v_curr, 'o', color='#e11d48', markersize=7.5, zorder=6)

    eq_box = (
        r"$\mathbf{(a)}\ mv_1 + \int_0^{t'} (2P - mg\sin 30^\circ)\,dt = 0$" + "\n"
        r"$150(-4) + 2\left[\frac{1}{2}(4)(600) + 600(t'-4)\right] - 735.8\,t' = 0 \Rightarrow \mathbf{t' = 6.46\ s}$" + "\n"
        r"$\mathbf{(b)}\ 150(-4) + \int_0^8 2P\,dt - 735.8(8) = 150\,v_2 \Rightarrow \mathbf{v_2 = +4.76\ m/s}$"
    )
    ax3.text(0.18, -9.8, eq_box, fontsize=8.6, color='#111827', va='bottom', ha='left',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1.2))

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "ex3_22_incline_skip_impulse.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=90)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved ex3_22_incline_skip_impulse.gif")
