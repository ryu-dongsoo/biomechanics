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
동역학 9판 제3장 질점의 운동역학 (Kinetics of Particles)
문제 3/69: 회전 슬롯 암과 슬라이더 r-θ 코리올리 가속도 및 장력 해석 (r-θ 극좌표계 심화문제)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영:
  * 고정 피벗 지지대 브래킷 및 피벗 O 허브
  * 중심 구멍을 통해 하단으로 길게 늘어진 끈 S
  * 내부 슬롯 홈과 둥근 끝단을 갖춘 완벽한 슬롯 암 (Slotted Arm)
  * 슬롯 상부 레일 B 및 하부 레일 A 라벨
  * 슬롯 내부를 미끄러지는 슬라이더 C, 장력 케이블, 치수선 r, 각속도 omega 화살표
- 공식 솔루션 매뉴얼(Wiley) 검증:
  * 반경방향 운동방정식: T = -m(0 - r*omega^2) = 2.0(0.225 * 6^2) = 16.20 N
  * 횡방향 운동방정식: a_θ = r*alpha + 2*r_dot*omega = 0.225(-2.0) + 2(-0.055)(6.0) = -1.110 m/s^2
  * 접촉력: N = m*a_θ = 2.0(-1.110) = -2.22 N (|N| = 2.22 N, 음수 부호로 [Side B] 접촉)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 물리 파라미터 및 공식 솔루션 정량값
m = 2.0                 # 슬라이더 질량 (kg)
r0 = 0.225              # 기준 반경 (m = 225 mm)
rdot = -0.055           # 케이블 당김 속도 (m/s = -55 mm/s)
omega = 6.0             # 각속도 (rad/s, 반시계방향)
alpha = -2.0            # 각가속도 (rad/s^2, 감속)

# 공식 솔루션 매뉴얼 검증값
ar_val = -r0 * (omega**2)                       # -8.10 m/s^2
T_val = -m * ar_val                             # 16.20 N
atheta_val = r0 * alpha + 2.0 * rdot * omega    # -0.450 - 0.660 = -1.110 m/s^2
N_val = m * atheta_val                          # -2.22 N (Side B 접촉)

# 2. 기하 보조 함수 (매끄러운 장공 슬롯 및 회전 변환)
def make_racetrack(u1, u2, width, n_arc=30):
    R = width / 2.0
    u_pts = [u1, u2]
    v_pts = [-R, -R]
    phi_right = np.linspace(-np.pi/2, np.pi/2, n_arc)
    u_pts.extend(u2 + R * np.cos(phi_right))
    v_pts.extend(R * np.sin(phi_right))
    u_pts.extend([u2, u1])
    v_pts.extend([R, R])
    phi_left = np.linspace(np.pi/2, 3*np.pi/2, n_arc)
    u_pts.extend(u1 + R * np.cos(phi_left))
    v_pts.extend(R * np.sin(phi_left))
    return np.array(u_pts), np.array(v_pts)

def rotate_pts(u_pts, v_pts, th):
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    return np.outer(u_pts, u_r) + np.outer(v_pts, u_th)

# 3. 애니메이션 시계열 (각도 16° -> 44° 회전 동안 슬라이더가 r: 0.285 m -> 0.165 m로 O를 향해 이동)
n_frames = 64
thetas = np.radians(np.linspace(16.0, 44.0, n_frames))
r_series = np.linspace(0.285, 0.165, n_frames)

# 캔버스 초기화 (14 x 6.5, 순수 흰색 바탕)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = thetas[frame]
    th_deg = np.degrees(th)
    r_curr = r_series[frame]
    
    # 동적 가속도 및 힘 계산
    cur_ar = -r_curr * (omega**2)
    cur_T = -m * cur_ar
    cur_atheta = r_curr * alpha + 2.0 * rdot * omega
    cur_N = m * cur_atheta
    
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    
    # ---------------- 1. 메인 물리 뷰 (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.16, 0.44)
    ax_main.set_ylim(-0.16, 0.40)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/69: 회전 슬롯 암과 슬라이더 r-θ 코리올리 해석', fontsize=13, fontweight='bold', pad=12)
    
    # (1) 바닥 지반선 및 해칭
    ground_y = -0.09
    ax_main.plot([-0.14, 0.12], [ground_y, ground_y], color='#37474f', lw=2.2, zorder=1)
    for hx in np.linspace(-0.13, 0.11, 16):
        ax_main.plot([hx, hx - 0.015], [ground_y, ground_y - 0.015], color='#78909c', lw=1.2, zorder=1)
    
    # (2) 피벗 지지대 브래킷
    bracket_pts = np.array([
        [-0.075, ground_y],
        [0.055, ground_y],
        [0.032, -0.015],
        [0.022, 0.0],
        [-0.040, 0.0],
        [-0.055, -0.015]
    ])
    ax_main.add_patch(patches.Polygon(bracket_pts, closed=True, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=2))
    
    # (3) 슬롯 암 외곽 윤곽선 (일체형 둥근 끝단)
    L_arm = 0.36
    w_out = 0.046
    R_out = w_out / 2.0
    u_pts = [0.0, L_arm]
    v_pts = [-R_out, -R_out]
    phi_right = np.linspace(-np.pi/2, np.pi/2, 30)
    u_pts.extend(L_arm + R_out * np.cos(phi_right))
    v_pts.extend(R_out * np.sin(phi_right))
    u_pts.extend([L_arm, 0.0])
    v_pts.extend([R_out, R_out])
    pts_out = rotate_pts(np.array(u_pts), np.array(v_pts), th)
    ax_main.add_patch(patches.Polygon(pts_out, closed=True, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=3))
    
    # (4) 피벗 허브 링 및 중심 핀 O
    hub_R = 0.044
    ax_main.add_patch(patches.Circle((0, 0), hub_R, facecolor='#b0cddb', edgecolor='#37474f', lw=1.5, zorder=4))
    pin_R = 0.013
    ax_main.add_patch(patches.Circle((0, 0), pin_R, facecolor='#455a64', edgecolor='#263238', lw=1.0, zorder=7))
    
    # (5) 내부 관통 슬롯 홈 (흰색 장공)
    w_in = 0.021
    s_start = 0.075
    s_end = 0.34
    u_in, v_in = make_racetrack(s_start, s_end, w_in)
    pts_in = rotate_pts(u_in, v_in, th)
    ax_main.add_patch(patches.Polygon(pts_in, closed=True, facecolor='#ffffff', edgecolor='#37474f', lw=1.3, zorder=5))
    
    # (6) 암 중심 점선 (Centerline)
    ax_main.plot([0, (L_arm + R_out)*u_r[0]], [0, (L_arm + R_out)*u_r[1]], color='#78909c', ls=':', lw=1.0, zorder=6)
    
    # (7) 슬라이더 C 및 인장 끈
    pos_c = r_curr * u_r
    c_len = 0.036
    c_w = w_in
    cord_end = pos_c - (c_len/2) * u_r
    # 피벗 O 중심에서 슬라이더 내부 연결 끈
    ax_main.plot([0, cord_end[0]], [0, cord_end[1]], color='#212121', lw=1.8, zorder=7)
    
    # 피벗 O 하단으로 늘어진 끈 S
    t_hang = np.linspace(0, 1, 35)
    y_hang = -0.14 * t_hang
    x_hang = -0.015 * np.sin(t_hang * 1.2 * np.pi) + 0.012 * (t_hang**2)
    ax_main.plot(x_hang, y_hang, color='#212121', lw=1.8, zorder=8)
    ax_main.text(x_hang[-1] - 0.025, y_hang[-1], r'$S$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # 슬라이더 블록 C (정밀 4정점 다각형)
    p1 = pos_c - (c_len/2) * u_r - (c_w/2) * u_th
    p2 = pos_c + (c_len/2) * u_r - (c_w/2) * u_th
    p3 = pos_c + (c_len/2) * u_r + (c_w/2) * u_th
    p4 = pos_c - (c_len/2) * u_r + (c_w/2) * u_th
    poly_c = patches.Polygon([p1, p2, p3, p4], closed=True, facecolor='#cf8a78', edgecolor='#5d4037', lw=1.3, zorder=7)
    ax_main.add_patch(poly_c)
    
    # (8) 라벨 (교재 원도 1:1 배치)
    ax_main.text(-0.068, -0.012, r'$O$', fontsize=16, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    c_lbl_pos = pos_c + (c_len/2 + 0.008) * u_r + 0.006 * u_th
    ax_main.text(c_lbl_pos[0], c_lbl_pos[1], r'$C$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    pos_B = 0.27 * u_r + (R_out + 0.016) * u_th
    pos_A = 0.27 * u_r - (R_out + 0.024) * u_th
    ax_main.text(pos_B[0], pos_B[1], r'$B$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    ax_main.text(pos_A[0], pos_A[1], r'$A$', fontsize=15, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # (9) 치수선 r (피벗 O -> 슬라이더 C)
    dim_h = R_out + 0.034
    p0_dim = dim_h * u_th
    pC_dim = pos_c + dim_h * u_th
    ax_main.plot([0, 1.15 * p0_dim[0]], [0, 1.15 * p0_dim[1]], color='#90a4ae', lw=0.9, zorder=6)
    ax_main.plot([pos_c[0], pos_c[0] + 1.15 * dim_h * u_th[0]], [pos_c[1], pos_c[1] + 1.15 * dim_h * u_th[1]], color='#90a4ae', lw=0.9, zorder=6)
    ax_main.annotate('', xy=pC_dim, xytext=p0_dim,
                     arrowprops=dict(arrowstyle='<->', color='#263238', lw=1.1), zorder=8)
    mid_dim = 0.5 * (p0_dim + pC_dim) + 0.012 * u_th
    ax_main.text(mid_dim[0], mid_dim[1], r'$r$', fontsize=14, fontstyle='italic', fontweight='bold', color='#263238', zorder=9)
    
    # (10) 각속도 회전 화살표 omega (피벗 허브 외곽 반시계 방향)
    om_r = 0.065
    phi_om = np.linspace(np.radians(75), np.radians(160), 30)
    ax_main.plot(om_r * np.cos(phi_om), om_r * np.sin(phi_om), color='#00897b', lw=1.8, zorder=8)
    tip_x = om_r * np.cos(np.radians(160))
    tip_y = om_r * np.sin(np.radians(160))
    prev_x = om_r * np.cos(np.radians(150))
    prev_y = om_r * np.sin(np.radians(150))
    ax_main.annotate('', xy=(tip_x, tip_y), xytext=(prev_x, prev_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.45', color='#00897b', lw=1.8), zorder=9)
    ax_main.text(tip_x - 0.030, tip_y + 0.015, r'$\omega$', fontsize=15, fontstyle='italic', fontweight='bold', color='#00897b', zorder=9)
    
    # (11) 상대속도 벡터 r_dot (녹색 화살표)
    v_len = 0.040
    v_start = pos_c
    v_end = pos_c - v_len * u_r
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#2e7d32', lw=2.0), zorder=8)
    ax_main.text(v_end[0] - 0.015*u_r[0], v_end[1] + 0.018, r'$\dot{r}$',
                 fontsize=12, fontweight='bold', color='#2e7d32', zorder=9)
    
    # 상단 상태 배너
    if abs(r_curr - r0) < 0.008:
        banner_txt = '문제 조건 순간: r = 225 mm 통과!'
        banner_bg, banner_edge, banner_col = '#e8f5e9', '#81c784', '#1b5e20'
    else:
        banner_txt = f'슬라이더 이동 중 (r = {r_curr*1e3:.0f} mm)'
        banner_bg, banner_edge, banner_col = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-0.14, 0.35, banner_txt, fontsize=10.5, fontweight='bold', color=banner_col,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # ---------------- 2. 해석 및 FBD 뷰 (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD 상단 렌더링 (슬라이더 C)
    ax_calc.text(0.2, 9.7, '[자유물체도 (Free Body Diagram) - 극좌표계 (r-θ)]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_cx, fbd_cy = 4.0, 8.2
    fbd_w, fbd_h = 1.4, 0.9
    fbd_sq = patches.Rectangle((fbd_cx - fbd_w/2, fbd_cy - fbd_h/2), fbd_w, fbd_h,
                               facecolor='#cf8a78', edgecolor='#5d4037', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_cx, fbd_cy, r'$m = 2.0\ \mathrm{kg}$' + '\n' + r'(슬라이더 $C$)',
                 fontsize=9.5, fontweight='bold', ha='center', va='center', color='#3e2723', zorder=6)
    
    # 극좌표계 (+r, +theta) 기준축
    axis_x, axis_y = 7.5, 8.2
    ax_calc.plot([axis_x, axis_x + 1.2], [axis_y, axis_y], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(axis_x + 1.2, axis_y), xytext=(axis_x, axis_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(axis_x + 1.3, axis_y - 0.12, r'$+r$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([axis_x, axis_x], [axis_y, axis_y + 1.1], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(axis_x, axis_y + 1.1), xytext=(axis_x, axis_y),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(axis_x - 0.12, axis_y + 1.22, r'$+\theta$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # 케이블 장력 T (-r 방향, 중심 O를 향함)
    ax_calc.annotate('', xy=(fbd_cx - fbd_w/2 - 1.4, fbd_cy), xytext=(fbd_cx - fbd_w/2, fbd_cy),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.50', color='#d32f2f', lw=2.4), zorder=6)
    ax_calc.text(fbd_cx - fbd_w/2 - 0.7, fbd_cy + 0.22, r'$T = 16.20\ \mathrm{N}$',
                 fontsize=10.5, fontweight='bold', color='#d32f2f', ha='center')
    
    # 횡접촉력 N (음수이므로 -theta 방향: [Side B]가 아래로 밈)
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - fbd_h/2 - 0.9), xytext=(fbd_cx, fbd_cy - fbd_h/2),
                     arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.45', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_cx + 0.15, fbd_cy - fbd_h/2 - 0.70, r'$N = 2.22\ \mathrm{N}$ ([Side B] 접촉)',
                 fontsize=10.5, fontweight='bold', color='#1565c0')
    
    # (2) 이론 해석 카드
    sol_text = (
        "[이론 해석 및 정량 유도 (r-θ 극좌표계)]\n"
        r"• 파라미터: $m = 2.0\ \mathrm{kg},\ r = 0.225\ \mathrm{m},\ \dot{r} = -0.055\ \mathrm{m/s}\ (\ddot{r} = 0)$" + "\n"
        r"  각속도 $\omega = 6.0\ \mathrm{rad/s}$, 각가속도 $\alpha = -2.0\ \mathrm{rad/s^2}$ (감속)" + "\n"
        r"• (1) 반경방향 운동방정식 ($\sum F_r = m a_r$):" + "\n"
        r"  $a_r = \ddot{r} - r\omega^2 = 0 - (0.225)(6.0^2) = -8.10\ \mathrm{m/s^2}$" + "\n"
        r"  $\sum F_r = -T = m a_r = 2.0(-8.10) = -16.20\ \mathrm{N} \Rightarrow \mathbf{T = 16.20\ \mathrm{N}}$" + "\n"
        r"• (2) 횡방향 운동방정식 ($\sum F_\theta = m a_\theta$):" + "\n"
        r"  $a_\theta = r\alpha + 2\dot{r}\omega = (0.225)(-2.0) + 2(-0.055)(6.0) = -0.450 - 0.660 = \mathbf{-1.110\ \mathrm{m/s^2}}$" + "\n"
        r"  $\sum F_\theta = N = m a_\theta = 2.0(-1.110) = \mathbf{-2.22\ \mathrm{N}}$" + "\n"
        r"• 접촉면 판정: $N$의 부호가 음수($-$)이므로 횡방향($+\theta$) 반대 방향인" + "\n"
        r"  회전 진행방향 앞쪽 가이드 면인 $\mathbf{[Side\ B]}$와 접촉!"
    )
    ax_calc.text(0.2, 4.55, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) 실시간 동적 모니터링 카드
    live_text = (
        "[실시간 동적 모니터링]\n"
        f"• 반경 위치: r = {r_curr*1e3:.1f} mm | 암 회전각: θ = {th_deg:.1f}°\n"
        f"• 반경 가속도: a_r = {cur_ar:.2f} m/s² | 케이블 장력: T = {cur_T:.2f} N\n"
        f"• 횡방향 가속도: a_θ = {cur_atheta:.3f} m/s²\n"
        f"• 가이드 접촉력: N = {cur_N:+.2f} N (r = 225 mm 이론값: -2.22 N)\n"
        f"• 접촉 가이드 판정: [Side B] (회전 앞쪽 면) 접촉!"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF 애니메이션 생성 및 저장
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_69_rotating_arm_slider.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[완료] 문제 3/69 한국어 애니메이션 생성 완료: {gif_path}")
