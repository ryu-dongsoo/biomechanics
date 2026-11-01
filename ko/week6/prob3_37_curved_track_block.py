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
문제 3/37: 수직 원형 곡선 레일 블록 수직항력 해석 (n-t 자연좌표계 기초문제)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영:
  * 최상단 곡률중심 십자선 (+) 및 수직 1점쇄선
  * 최하점 A (0°) 및 좌측 경사 위치 B (30°)
  * 중심에서 곡면으로 이어지는 3 m 치수선 화살표
  * 우측에서 A로 진입하는 속도 v 방향 및 오목 곡선 레일
- 공식 솔루션 매뉴얼(Wiley) 검증:
  * A점 (θ = 0°, v_A = 5 m/s): N_A = m(g + v_A^2/R) = 0.6(9.81 + 25/3) = 10.89 N
  * B점 (θ = 30°, v_B = 4 m/s): N_B = m(g*cos 30° + v_B^2/R) = 0.6(9.81*cos 30° + 16/3) = 8.30 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 물리 파라미터 및 솔루션 정량값
m = 0.6               # 블록 질량 (kg)
g = 9.81              # 중력가속도 (m/s^2)
R = 3.0               # 곡률반경 (m)
vA = 5.0              # A점 속력 (m/s)
vB = 4.0              # B점 속력 (m/s)
th_B = np.radians(30.0) # 좌측 30도 위치

# Wiley 공식 해석값
NA_val = m * (g + (vA**2) / R)                    # 10.886 N -> 10.89 N
NB_val = m * (g * np.cos(th_B) + (vB**2) / R)     # 8.298 N -> 8.30 N

# 2. 애니메이션 시계열: 우측(+35도) -> A(0도) -> B(-30도) -> -35도 왕복
n_frames = 64
t_eval = np.linspace(0, 1.0, n_frames)
# 부드러운 단진동 슬라이딩 (우측에서 출발하여 좌측으로 이동 후 복귀)
theta_deg_series = 34.0 * np.cos(2 * np.pi * t_eval)
theta_series = np.radians(theta_deg_series)

# 캔버스 초기화 (14 x 6.5, 순수 흰색 바탕)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = theta_series[frame]
    th_deg = theta_deg_series[frame]
    
    # 궤도 상의 블록 중심 좌표 (O=(0,0) 중심, 최하점 A=(0, -R))
    # th > 0 이면 우측, th < 0 이면 좌측 (B는 th = -30도)
    px = R * np.sin(th)
    py = -R * np.cos(th)
    
    # 이동 속도 (에너지 보존형 보간: A에서 5.0 m/s, B에서 4.0 m/s)
    # v^2 = v_A^2 - 2 * g_eff * R * (1 - cos th), g_eff 산출
    g_eff = (vA**2 - vB**2) / (2 * R * (1 - np.cos(th_B))) # (25 - 16)/(6 * 0.13397) ~ 11.19
    v_sq = max(1.0, vA**2 - 2 * g_eff * R * (1 - np.cos(th)))
    v_curr = np.sqrt(v_sq)
    
    # 진행 방향 판별 (d_theta / dt)
    # th_deg = 34 * cos(2pi*t) -> 속도 부호: -sin(2pi*t)
    vel_sign = -np.sign(np.sin(2 * np.pi * t_eval[frame])) if abs(np.sin(2 * np.pi * t_eval[frame])) > 1e-3 else -1.0
    # 접선 단위벡터 (반시계방향: e_t = [cos th, sin th])
    # vel_sign < 0 이면 왼쪽(시계방향, A 및 B로 향함)
    an_curr = (v_curr**2) / R
    N_curr = m * (g * np.cos(th) + an_curr)
    
    # ---------------- 1. 메인 물리 뷰 (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.5, 2.5)
    ax_main.set_ylim(-3.5, 0.4)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/37: 수직 원형 곡선 레일 블록 수직항력 해석', fontsize=13, fontweight='bold', pad=12)
    
    # (1) 곡률 중심 + 및 기준 축선
    ax_main.plot(0, 0, 'k+', ms=12, mew=1.8, zorder=5)
    # 수직 1점 쇄선 (중심 -> A)
    ax_main.plot([0, 0], [0, -R], color='#546e7a', ls='-.', lw=1.2, zorder=2)
    
    # (2) 좌측 B점 기준선 (교재 원도 1:1: A에서 좌측 30도)
    bx_ref = -R * np.sin(th_B)
    by_ref = -R * np.cos(th_B)
    ax_main.plot([0, bx_ref], [0, by_ref], color='#78909c', ls='--', lw=1.2, zorder=2)
    
    # 각도 30도 호 표시 (중심선과 좌측 30도 선 사이)
    arc_patch = patches.Arc((0, 0), 1.8, 1.8, angle=-90, theta1=-30, theta2=0, color='#37474f', lw=1.2)
    ax_main.add_patch(arc_patch)
    ax_main.text(-0.38, -1.05, r'$30^\circ$', fontsize=11, fontweight='bold', color='#263238')
    
    # (3) 원형 가이드 레일 (교재 원도 스타일: 오목 곡면 + 부드러운 음영)
    arc_span = np.linspace(-np.radians(46), np.radians(46), 120)
    rx_rail = R * np.sin(arc_span)
    ry_rail = -R * np.cos(arc_span)
    ax_main.plot(rx_rail, ry_rail, color='#37474f', lw=2.2, zorder=3)
    
    # 레일 하부 두께 및 베이지/회색 음영
    thick = 0.20
    poly_rail = np.vstack([
        np.column_stack([rx_rail, ry_rail]),
        np.column_stack([(R + thick) * np.sin(arc_span[::-1]), -(R + thick) * np.cos(arc_span[::-1])])
    ])
    ax_main.add_patch(patches.Polygon(poly_rail, closed=True, facecolor='#ede7df', edgecolor='#b0bec5', lw=0.8, zorder=1))
    
    # (4) 곡률반경 치수선 R = 3 m (중심에서 레일 우측으로 향하는 화살표)
    dim_th = np.radians(12.0)
    dim_target = np.array([R * np.sin(dim_th), -R * np.cos(dim_th)])
    ax_main.annotate('', xy=dim_target, xytext=(0, 0),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(dim_target[0]/2 + 0.12, dim_target[1]/2, r'$3\ \mathrm{m}$',
                 fontsize=12, fontweight='bold', color='#263238', zorder=5)
    
    # (5) A점 및 B점 레이블
    ax_main.plot(0, -R, 'ko', ms=4, zorder=4)
    ax_main.text(0.0, -R - 0.32, r'$A$', fontsize=15, fontweight='bold', color='#1565c0', ha='center', zorder=6)
    
    ax_main.plot(bx_ref, by_ref, 'ko', ms=4, zorder=4)
    ax_main.text(bx_ref - 0.12, by_ref - 0.25, r'$B$', fontsize=15, fontweight='bold', color='#1565c0', ha='center', zorder=6)
    
    # (6) 블록 패치 (교재 원도: 갈색/살구색 직사각형 블록)
    bw, bh = 0.36, 0.20
    rot_deg = np.degrees(th)
    blk_patch = patches.Rectangle((-bw/2, 0), bw, bh, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(rot_deg).translate(px, py) + ax_main.transData
    blk_patch.set_transform(t_blk)
    ax_main.add_patch(blk_patch)
    
    # 블록 중심
    blk_cx = px - np.sin(th) * bh / 2
    blk_cy = py + np.cos(th) * bh / 2
    
    # (7) 속도 벡터 v (녹색 화살표)
    # 접선 단위벡터: t_hat = [cos th, sin th]
    t_hat = np.array([np.cos(th), np.sin(th)])
    v_vec = t_hat * vel_sign
    v_arrow_len = 0.55
    v_start = np.array([blk_cx, blk_cy + 0.15])
    v_end = v_start + v_arrow_len * v_vec
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.45', color='#2e7d32', lw=2.2), zorder=8)
    ax_main.text(v_end[0] + 0.05 * v_vec[0], v_end[1] + 0.08, r'$v$',
                 fontsize=14, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=9)
    
    # 상단 상태 배너
    if abs(th_deg) < 4.0:
        pos_str = '최저점 A 통과 중 (θ ≈ 0°)'
        b_col, b_edge, b_txt = '#e8f5e9', '#81c784', '#1b5e20'
    elif abs(th_deg - (-30.0)) < 4.0:
        pos_str = '경사점 B 통과 중 (θ ≈ -30°)'
        b_col, b_edge, b_txt = '#e3f2fd', '#90caf9', '#0d47a1'
    else:
        pos_str = f'곡면 이동 중 (θ = {th_deg:+.1f}°)'
        b_col, b_edge, b_txt = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-2.4, 0.25, f'상태: {pos_str}', fontsize=10.5, fontweight='bold', color=b_txt,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=b_col, edgecolor=b_edge, lw=1.2))
    
    # ---------------- 2. 해석 및 모니터링 뷰 (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD 상단 렌더링 (자연좌표계 n-t)
    ax_calc.text(0.2, 9.7, '[자유물체도 (Free Body Diagram) - 자연좌표계 (n-t)]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_bx, fbd_by = 4.5, 8.1
    # 블록 사각형
    fbd_sq = patches.Rectangle((fbd_bx - 0.7, fbd_by - 0.4), 1.4, 0.8,
                               facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_bx, fbd_by, r'$m = 0.6\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800', zorder=6)
    
    # 수직항력 N (곡률중심 +n 방향, 상향)
    n_arrow_len = 0.5 + (N_curr / 12.0) * 0.9
    ax_calc.annotate('', xy=(fbd_bx, fbd_by + 0.4 + n_arrow_len), xytext=(fbd_bx, fbd_by + 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by + 0.4 + n_arrow_len, r'$N$', fontsize=14, fontweight='bold', color='#1565c0')
    
    # 중력 mg (연직 하향)
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 0.4 - 1.0), xytext=(fbd_bx, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#d32f2f', lw=2.2), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by - 0.4 - 0.8, r'$mg$', fontsize=13, fontweight='bold', color='#d32f2f')
    
    # 자연좌표계 축 (n, t)
    ax_calc.plot([fbd_bx + 2.0, fbd_bx + 2.0], [fbd_by, fbd_by + 1.2], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 2.0, fbd_by + 1.2), xytext=(fbd_bx + 2.0, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 2.15, fbd_by + 1.15, r'$+n$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([fbd_bx + 2.0, fbd_bx + 3.2], [fbd_by, fbd_by], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 3.2, fbd_by), xytext=(fbd_bx + 2.0, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 3.25, fbd_by - 0.10, r'$+t$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # (2) 이론 해석 카드 (sol_box at y = 4.65)
    sol_text = (
        "[이론 해석 및 정량 유도 (자연좌표계 n-t)]\n"
        r"• 파라미터: $m = 0.6\ \mathrm{kg},\ R = 3.0\ \mathrm{m},\ g = 9.81\ \mathrm{m/s^2}$" + "\n"
        r"  $A$점 속력 $v_A = 5.0\ \mathrm{m/s}\ (\theta = 0^\circ),\ B$점 속력 $v_B = 4.0\ \mathrm{m/s}\ (\theta = 30^\circ)$" + "\n"
        r"• 법선방향 운동방정식 ($\sum F_n = m a_n = m \frac{v^2}{R}$):" + "\n"
        r"  $\sum F_n = N - mg\cos\theta = m \frac{v^2}{R} \Rightarrow \mathbf{N = m\left(g\cos\theta + \frac{v^2}{R}\right)}$" + "\n"
        r"• (1) 최저점 $A$ 통과 시 ($\theta = 0^\circ,\ v_A = 5.0\ \mathrm{m/s}$):" + "\n"
        r"  $\mathbf{N_A = 0.6\left(9.81 + \frac{5.0^2}{3.0}\right) = 0.6(9.81 + 8.333) = 10.89\ \mathrm{N}}$" + "\n"
        r"• (2) 경사점 $B$ 통과 시 ($\theta = 30^\circ,\ v_B = 4.0\ \mathrm{m/s}$):" + "\n"
        r"  $\mathbf{N_B = 0.6\left(9.81\cos 30^\circ + \frac{4.0^2}{3.0}\right) = 0.6(8.496 + 5.333) = 8.30\ \mathrm{N}}$"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) 실시간 동적 모니터링 카드 (live_box at y = 1.05)
    live_text = (
        "[실시간 동적 모니터링]\n"
        f"• 현재 위치 각도: θ = {th_deg:+.1f}° (최저점 기준)\n"
        f"• 블록 이동 속력: v = {v_curr:.2f} m/s (진행 방향: {'← 좌향 (A·B 방면)' if vel_sign < 0 else '→ 우향'})\n"
        f"• 법선 가속도: a_n = v²/R = {an_curr:.2f} m/s²\n"
        f"• 곡면 수직항력: N = {N_curr:.2f} N (중력 성분 {m*g*np.cos(th):.2f} N + 구심력 {m*an_curr:.2f} N)\n"
        f"• 공식 매뉴얼 검증: N_A = {NA_val:.2f} N (A점), N_B = {NB_val:.2f} N (B점)"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF 애니메이션 생성 및 저장
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_37_curved_track_block.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[완료] 문제 3/37 한국어 애니메이션 생성 완료: {gif_path}")
