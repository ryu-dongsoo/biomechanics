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
문제 3/44: 수직 회전관 내 질점의 극좌표계 코리올리 가속도 및 수직접촉력 해석 (r-θ 극좌표계 기초문제)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영:
  * 바닥 지지대 브래킷 및 피벗 O 원형 베어링 림
  * 피벗 O 림에서 우상향으로 뻗은 빈 관(Hollow tube) 및 열린 끝단
  * 수평 기준선과 관 축선 사이의 각도 θ 호 및 라벨
  * 관 내부에서 O 방향으로 미끄러지는 질점 (m = 0.1 kg)과 상대속도 r_dot = -2 m/s
  * 반시계방향 일정 각속도 theta_dot = 3 rad/s
- 공식 솔루션 매뉴얼(Wiley) 검증:
  * 코리올리 가속도: a_θ = 2*r_dot*omega = 2(-2.0)(3.0) = -12.0 m/s^2
  * 수직접촉력: N = m(g*cos 30° + a_θ) = 0.1(9.81*cos 30° - 12.0) = -0.350 N (|N| = 0.350 N, 회전 앞쪽 내벽 접촉)
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
m = 0.1             # 질점 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
omega = 3.0         # 일정한 각속도 (rad/s)
rdot = -2.0         # 상대속도 (m/s, O 방향)
th_target_deg = 30.0
th_target = np.radians(th_target_deg)

# 공식 솔루션 매뉴얼 검증값
a_theta_cor = 2.0 * rdot * omega            # -12.0 m/s^2
mg_theta = m * g * np.cos(th_target)        # +0.8496 N
N_theory = mg_theta + m * a_theta_cor       # -0.3504 N -> -0.350 N
N_mag = abs(N_theory)                       # 0.350 N

# 2. 애니메이션 시계열 (각도 12° -> 48° 회전 동안 질점이 r: 0.78 m -> 0.32 m로 내향 슬라이딩)
n_frames = 64
thetas = np.radians(np.linspace(12.0, 48.0, n_frames))
r_series = np.linspace(0.78, 0.32, n_frames)

# 캔버스 초기화 (14 x 6.5, 순수 흰색 바탕)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    th = thetas[frame]
    th_deg = np.degrees(th)
    r_curr = r_series[frame]
    
    cur_mg_th = m * g * np.cos(th)
    cur_N = cur_mg_th + m * a_theta_cor
    
    # 단위벡터: e_r (반경), e_theta (횡방향)
    u_r = np.array([np.cos(th), np.sin(th)])
    u_th = np.array([-np.sin(th), np.cos(th)])
    
    # ---------------- 1. 메인 물리 뷰 (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.25, 1.15)
    ax_main.set_ylim(-0.25, 0.95)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/44: 수직 회전관 내 질점의 코리올리 가속도 및 수직력', fontsize=13, fontweight='bold', pad=12)
    
    # (1) 바닥면 및 지지대 그림자
    ax_main.plot([-0.18, 0.18], [-0.12, -0.12], color='#37474f', lw=2.2, zorder=1)
    # 바닥 음영
    ax_main.add_patch(patches.Rectangle((-0.18, -0.16), 0.36, 0.04, facecolor='#ede7df', edgecolor='none', zorder=0))
    
    # (2) 삼각형 피벗 지지대 브래킷
    tri_pts = np.array([[-0.10, -0.12], [0.10, -0.12], [0.0, 0.0]])
    ax_main.add_patch(patches.Polygon(tri_pts, closed=True, facecolor='#cfd8dc', edgecolor='#455a64', lw=1.3, zorder=2))
    
    # (3) 원형 베어링 림 및 중심 핀 O (교재 원도 1:1)
    hub_r = 0.055
    ax_main.add_patch(patches.Circle((0, 0), hub_r, facecolor='#eceff1', edgecolor='#37474f', lw=1.4, zorder=3))
    ax_main.add_patch(patches.Circle((0, 0), 0.022, facecolor='#263238', edgecolor='#263238', lw=1.0, zorder=4))
    ax_main.text(-0.11, 0.01, r'$O$', fontsize=16, fontweight='bold', color='#263238', zorder=5)
    
    # (4) 수평 기준선 (가느다란 실선)
    ax_main.plot([0, 0.85], [0, 0], color='#78909c', lw=1.1, zorder=1)
    
    # (5) 각도 θ 호 표시 (피벗 근처)
    arc_th = patches.Arc((0, 0), 0.40, 0.40, angle=0, theta1=0, theta2=th_deg, color='#263238', lw=1.2, zorder=4)
    ax_main.add_patch(arc_th)
    ax_main.text(0.24, 0.06, r'$\theta$', fontsize=13, fontweight='bold', color='#263238', zorder=5)
    
    # (6) 회전하는 빈 관 (Hollow Tube) - 피벗 허브 림에서 시작
    tube_len = 0.95
    tube_w = 0.075
    
    # 관의 4개 코너: 허브 림(s = hub_r)에서 시작
    p1 = hub_r * u_r + (tube_w/2) * u_th
    p2 = tube_len * u_r + (tube_w/2) * u_th
    p3 = tube_len * u_r - (tube_w/2) * u_th
    p4 = hub_r * u_r - (tube_w/2) * u_th
    
    tube_poly = np.array([p1, p2, p3, p4])
    ax_main.add_patch(patches.Polygon(tube_poly, closed=True, facecolor='#e0f2f1', edgecolor='#37474f', lw=1.5, zorder=2))
    
    # 관 중심선 (일점쇄선)
    ax_main.plot([0, (tube_len + 0.08)*u_r[0]], [0, (tube_len + 0.08)*u_r[1]],
                 color='#546e7a', ls='-.', lw=1.1, zorder=3)
    
    # (7) 관 내부 슬라이더 질점 m (교재 원도: 갈색 직사각형)
    pos_p = r_curr * u_r
    b_w, b_h = 0.09, tube_w * 0.88
    block = patches.Rectangle((-b_w/2, -b_h/2), b_w, b_h, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate(th).translate(pos_p[0], pos_p[1]) + ax_main.transData
    block.set_transform(t_blk)
    ax_main.add_patch(block)
    
    # 질점 라벨 m
    ax_main.text(pos_p[0], pos_p[1], r'$m$', fontsize=10, fontweight='bold', color='#4a2800',
                 ha='center', va='center', rotation=th_deg, zorder=6)
    
    # (8) 상대속도 벡터 r_dot (녹색 화살표, O를 향함)
    v_arrow_len = 0.15
    v_start = pos_p
    v_end = pos_p - v_arrow_len * u_r
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.2), zorder=7)
    ax_main.text(v_end[0] - 0.06*u_r[0], v_end[1] + 0.04, r'$\dot{r} = -2\ \mathrm{m/s}$',
                 fontsize=10.5, fontweight='bold', color='#2e7d32', zorder=8)
    
    # (9) 각속도 회전 표시 omega = 3 rad/s (피벗 상단 원호 화살표)
    om_r = 0.22
    arc_om = patches.Arc((0, 0), 2*om_r, 2*om_r, angle=0, theta1=th_deg + 15, theta2=th_deg + 45, color='#e65100', lw=1.8, zorder=5)
    ax_main.add_patch(arc_om)
    tip_th = np.radians(th_deg + 45)
    ax_main.annotate('', xy=(om_r*np.cos(tip_th), om_r*np.sin(tip_th)),
                     xytext=(om_r*np.cos(tip_th - 0.1), om_r*np.sin(tip_th - 0.1)),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.4', color='#e65100', lw=1.8), zorder=6)
    ax_main.text(om_r*np.cos(tip_th) - 0.04, om_r*np.sin(tip_th) + 0.04, r'$\dot{\theta} = 3\ \mathrm{rad/s}$',
                 fontsize=11, fontweight='bold', color='#e65100', zorder=7)
    
    # 상단 상태 배너
    if abs(th_deg - 30.0) < 2.0:
        pos_str = '문제 조건 θ = 30.0° 통과 순간!'
        b_col, b_edge, b_txt = '#e8f5e9', '#81c784', '#1b5e20'
    else:
        pos_str = f'수직면 회전 중 (θ = {th_deg:.1f}°)'
        b_col, b_edge, b_txt = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-0.20, 0.84, f'상태: {pos_str}', fontsize=10.5, fontweight='bold', color=b_txt,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=b_col, edgecolor=b_edge, lw=1.2))
    
    # ---------------- 2. 해석 및 모니터링 뷰 (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD 상단 렌더링 (극좌표계 r-theta)
    ax_calc.text(0.2, 9.7, '[자유물체도 (Free Body Diagram) - 극좌표계 (r-θ)]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_bx, fbd_by = 4.5, 7.8
    # 질점 사각형
    fbd_sq = patches.Rectangle((fbd_bx - 0.7, fbd_by - 0.4), 1.4, 0.8,
                               facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5)
    ax_calc.add_patch(fbd_sq)
    ax_calc.text(fbd_bx, fbd_by, r'$m = 0.1\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800', zorder=6)
    
    # 좌표축 표시 (+r, +theta)
    ax_calc.plot([fbd_bx + 1.8, fbd_bx + 3.0], [fbd_by, fbd_by], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 3.0, fbd_by), xytext=(fbd_bx + 1.8, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 3.1, fbd_by - 0.10, r'$+r$', fontsize=11, fontweight='bold', color='#546e7a')
    
    ax_calc.plot([fbd_bx + 1.8, fbd_bx + 1.8], [fbd_by, fbd_by + 1.2], color='#546e7a', lw=1.3)
    ax_calc.annotate('', xy=(fbd_bx + 1.8, fbd_by + 1.2), xytext=(fbd_bx + 1.8, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#546e7a', lw=1.3))
    ax_calc.text(fbd_bx + 1.95, fbd_by + 1.15, r'$+\theta$', fontsize=11, fontweight='bold', color='#546e7a')
    
    # 수직접촉력 N: 회전 앞벽이 질점을 미는 힘 (-theta 방향)
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 0.4 - 1.1), xytext=(fbd_bx, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.4), zorder=6)
    ax_calc.text(fbd_bx + 0.15, fbd_by - 0.4 - 0.9, r'$N = 0.350\ \mathrm{N}$ (앞쪽 내벽 접촉)',
                 fontsize=10.5, fontweight='bold', color='#1565c0')
    
    # 중력 mg (연직 하향)
    ax_calc.annotate('', xy=(fbd_bx - 0.6, fbd_by - 0.4 - 1.0), xytext=(fbd_bx - 0.6, fbd_by - 0.4),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_bx - 1.45, fbd_by - 0.4 - 0.8, r'$mg$', fontsize=12, fontweight='bold', color='#d32f2f')
    
    # (2) 이론 해석 카드 (sol_box at y = 4.65)
    sol_text = (
        "[이론 해석 및 정량 유도 (r-θ 극좌표계)]\n"
        r"• 파라미터: $m = 0.1\ \mathrm{kg},\ \dot{\theta} = \omega = 3.0\ \mathrm{rad/s}\ (\ddot{\theta} = 0),\ \dot{r} = -2.0\ \mathrm{m/s}$" + "\n"
        r"• 횡방향 가속도 (코리올리 가속도):" + "\n"
        r"  $a_\theta = r\ddot{\theta} + 2\dot{r}\dot{\theta} = 0 + 2(-2.0)(3.0) = \mathbf{-12.0\ \mathrm{m/s^2}}$" + "\n"
        r"• 횡방향 운동방정식 ($\sum F_\theta = m a_\theta,\ \theta = 30^\circ$):" + "\n"
        r"  $\sum F_\theta = N - mg\cos 30^\circ = m a_\theta$" + "\n"
        r"  $\Rightarrow N = mg\cos 30^\circ + m a_\theta = 0.1(9.81)\cos 30^\circ + 0.1(-12.0)$" + "\n"
        r"  $\Rightarrow N = 0.8496 - 1.200 = \mathbf{-0.350\ \mathrm{N}}$" + "\n"
        r"• 결론: 수직력의 크기는 $\mathbf{|N| = 0.350\ \mathrm{N}}$이며, 부호가 음수($-$)이므로" + "\n"
        r"  회전 진행방향 앞쪽 내벽(Leading Wall)이 질점을 밀고 있음!"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) 실시간 동적 모니터링 카드 (live_box at y = 1.05)
    live_text = (
        "[실시간 동적 모니터링]\n"
        f"• 관 회전 각도: θ = {th_deg:.1f}° (각속도 ω = 3.0 rad/s)\n"
        f"• 질점 반경 위치: r = {r_curr:.3f} m (상대속도 r_dot = -2.0 m/s, O 방향)\n"
        f"• 코리올리 가속도: 2·r_dot·ω = {a_theta_cor:.1f} m/s² (일정값)\n"
        f"• 중력 횡방향 성분: mg cos θ = {cur_mg_th:.3f} N\n"
        f"• 벽면 수직접촉력: N = {cur_N:+.3f} N (θ = 30° 이론값: {N_theory:.3f} N)\n"
        f"• 접촉 판정: 회전 앞쪽 내벽(Leading Wall) 접촉 중"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF 애니메이션 생성 및 저장
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_44_rotating_tube_particle.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[완료] 문제 3/44 한국어 애니메이션 생성 완료: {gif_path}")
