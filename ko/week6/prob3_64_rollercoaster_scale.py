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
문제 3/64: 롤러코스터 곡률반경과 체중계 수직항력 F=ma 해석 (n-t 자연좌표계 심화문제)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영:
  * 오목 저점 A (곡률반경 40 m) 및 상단 곡률중심 십자선 (+), 40 m 치수선 화살표
  * 볼록 정상 B (곡률반경 20 m) 및 하단 곡률중심 십자선 (+), 20 m 치수선 화살표
  * 교재 원도 동일 4칸 연결 롤러코스터 열차 (저점 A 실선 열차 v_A, 정상 B 점선 열차 v_B)
  * 다이내믹 주행 시뮬레이션 및 우측 패널 저점 A / 정상 B 비교 FBD
- 공식 솔루션 매뉴얼(Wiley) 검증:
  * 저점 A (v_A = 22 m/s, ρ_A = 40 m): N_A = m(g + v_A^2/ρ_A) = 75(9.81 + 12.10) = 1643 N (2.23 W)
  * 정상 B (v_B = 12 m/s, ρ_B = 20 m): N_B = m(g - v_B^2/ρ_B) = 75(9.81 - 7.20) = 195.8 N (0.27 W)
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
m = 75.0                # 승객 질량 (kg)
g = 9.81                # 중력가속도 (m/s^2)
W = m * g               # 체중 735.8 N
RA = 40.0               # 저점 A 곡률반경 (m)
vA = 22.0               # 저점 A 속력 (m/s)
RB = 20.0               # 정상 B 곡률반경 (m)
vB = 12.0               # 정상 B 속력 (m/s)

# 공식 솔루션 매뉴얼 검증값
NA_val = m * (g + (vA**2) / RA)    # 1643.25 N -> 1643 N (2.23 W)
NB_val = m * (g - (vB**2) / RB)    # 195.75 N -> 195.8 N (0.27 W)

# 2. 롤러코스터 S자 레일 형상 모델링 (교재 원도 1:1)
# 곡선 파라미터: 저점 A at x = -0.5, y = -0.4; 정상 B at x = 0.9, y = 0.35
# 부드러운 5차 다항식 또는 코사인 합성 곡선
s_eval = np.linspace(-1.4, 1.8, 200)
def get_track_profile(x):
    # 저점 x=-0.5, 정상 x=0.9
    # S-curve transition
    # y = y0 + A * sin(k * (x - x_mid)) with transitions
    # Let's use a composite curve:
    # A trough: concave arc with radius R_A_vis ~ 1.6 near x = -0.5
    # B crest: convex arc with radius R_B_vis ~ 0.8 near x = +0.9
    return -0.40 + 0.75 / (1.0 + np.exp(-3.5 * (x - 0.20))) - 0.12 * (x - 0.20)

# Smooth track coordinates
x_track = np.linspace(-1.35, 1.75, 180)
y_track = get_track_profile(x_track)

# 저점 A 위치 (x ~ -0.52)
idx_A = np.argmin(y_track[:100])
xA_pos, yA_pos = x_track[idx_A], y_track[idx_A]

# 정상 B 위치 (x ~ 0.88)
idx_B = 80 + np.argmax(y_track[80:])
xB_pos, yB_pos = x_track[idx_B], y_track[idx_B]

# 3. 주행 시계열: 4칸 열차가 x = -1.2에서 x = +1.5까지 주행 (총 64 프레임)
n_frames = 64
x_train_series = np.linspace(-1.15, 1.45, n_frames)

# 캔버스 초기화 (14 x 6.5, 순수 흰색 바탕)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    xc = x_train_series[frame]
    yc = get_track_profile(xc)
    
    # 국소 기울기
    eps = 0.01
    dy_dx = (get_track_profile(xc + eps) - get_track_profile(xc - eps)) / (2 * eps)
    th_slope = np.arctan(dy_dx)
    
    # 위치에 따른 속도 및 상태
    if xc < 0.20:
        # A점 인근
        factor = (xc - (-1.15)) / (0.20 - (-1.15))
        v_curr = 24.0 - factor * 7.0
        rho_curr = RA
        N_curr = NA_val
        zone_name = "저점 A 통과 구간"
    else:
        # B점 인근
        factor = (xc - 0.20) / (1.45 - 0.20)
        v_curr = 17.0 - factor * 5.0
        rho_curr = RB
        N_curr = NB_val
        zone_name = "정상 B 통과 구간"
    
    # ---------------- 1. 메인 물리 뷰 (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-0.85, 1.25)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/64: 롤러코스터 곡률반경과 체중계 수직항력 해석', fontsize=13, fontweight='bold', pad=12)
    
    # (1) 트랙 레일 및 하부 음영
    ax_main.plot(x_track, y_track, color='#263238', lw=2.4, zorder=3)
    # 하부 베이지색 두께 음영
    poly_ground = np.vstack([
        np.column_stack([x_track, y_track]),
        np.column_stack([x_track[::-1], y_track[::-1] - 0.12])
    ])
    ax_main.add_patch(patches.Polygon(poly_ground, closed=True, facecolor='#ede7df', edgecolor='#b0bec5', lw=0.8, zorder=1))
    
    # (2) 저점 A 곡률중심 (+) 및 40 m 치수선 (교재 원도 1:1)
    cA_x, cA_y = xA_pos + 0.12, yA_pos + 1.15
    ax_main.plot(cA_x, cA_y, 'k+', ms=12, mew=1.8, zorder=4)
    # 곡률반경 40 m 치수선 화살표
    ax_main.annotate('', xy=(xA_pos + 0.02, yA_pos), xytext=(cA_x, cA_y),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(cA_x + 0.05, (cA_y + yA_pos)/2 + 0.08, r'$40\ \mathrm{m}$',
                 fontsize=11.5, fontweight='bold', color='#263238', zorder=5)
    
    # 저점 A 라벨
    ax_main.text(xA_pos, yA_pos - 0.22, r'$A$', fontsize=16, fontweight='bold', color='#1565c0', ha='center', zorder=5)
    
    # (3) 정상 B 곡률중심 (+) 및 20 m 치수선 (교재 원도 1:1)
    cB_x, cB_y = xB_pos + 0.08, yB_pos - 0.70
    ax_main.plot(cB_x, cB_y, 'k+', ms=12, mew=1.8, zorder=4)
    # 곡률반경 20 m 치수선 화살표
    ax_main.annotate('', xy=(xB_pos, yB_pos), xytext=(cB_x, cB_y),
                     arrowprops=dict(arrowstyle='<->', color='#37474f', lw=1.1), zorder=4)
    ax_main.text(cB_x - 0.18, (cB_y + yB_pos)/2 - 0.02, r'$20\ \mathrm{m}$',
                 fontsize=11.5, fontweight='bold', color='#263238', zorder=5)
    
    # 정상 B 라벨
    ax_main.text(xB_pos, yB_pos - 0.22, r'$B$', fontsize=16, fontweight='bold', color='#1565c0', ha='center', zorder=5)
    
    # (4) 교재 원도 동일: 저점 A 및 정상 B 고정 속도 벡터 표시
    # v_A 화살표 at 저점
    ax_main.annotate('', xy=(xA_pos + 0.28, yA_pos + 0.18), xytext=(xA_pos - 0.08, yA_pos + 0.18),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.0), zorder=6)
    ax_main.text(xA_pos + 0.08, yA_pos + 0.24, r'$v_A$', fontsize=13, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=6)
    
    # v_B 화살표 at 정상
    ax_main.annotate('', xy=(xB_pos + 0.26, yB_pos + 0.18), xytext=(xB_pos - 0.08, yB_pos + 0.18),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=2.0), zorder=6)
    ax_main.text(xB_pos + 0.08, yB_pos + 0.24, r'$v_B$', fontsize=13, fontstyle='italic', fontweight='bold', color='#2e7d32', zorder=6)
    
    # (5) 정상 B 점선 고정 열차 (교재 원도의 B점 점선 차량 4칸)
    b_offsets = [-0.18, -0.06, +0.06, +0.18]
    for b_off in b_offsets:
        bx_car = xB_pos + b_off
        by_car = get_track_profile(bx_car)
        car_box_b = patches.Rectangle((-0.045, 0.015), 0.09, 0.06, ls='--',
                                      facecolor='none', edgecolor='#546e7a', lw=1.2, zorder=4)
        t_b = plt.matplotlib.transforms.Affine2D().translate(bx_car, by_car) + ax_main.transData
        car_box_b.set_transform(t_b)
        ax_main.add_patch(car_box_b)
        # 작은 바퀴 2개 (점선)
        ax_main.plot(bx_car - 0.03, by_car + 0.015, 'o', ms=2.5, mfc='none', mec='#546e7a', zorder=4)
        ax_main.plot(bx_car + 0.03, by_car + 0.015, 'o', ms=2.5, mfc='none', mec='#546e7a', zorder=4)
    
    # (6) 동적 주행 4칸 열차 (실선, 노란색 차체 + 바퀴)
    train_car_spacing = 0.12
    car_w, car_h = 0.095, 0.065
    for c_idx in range(4):
        # 4칸의 상대 위치 (맨 앞칸이 xc, 뒤로 갈수록 x 감소)
        x_ci = xc - (3 - c_idx) * train_car_spacing
        y_ci = get_track_profile(x_ci)
        d_ci = (get_track_profile(x_ci + eps) - get_track_profile(x_ci - eps)) / (2 * eps)
        th_ci = np.arctan(d_ci)
        
        # 차체 박스 (노란색)
        car_rect = patches.Rectangle((-car_w/2, 0.02), car_w, car_h,
                                     facecolor='#fff59d', edgecolor='#f57f17', lw=1.3, zorder=7)
        t_c = plt.matplotlib.transforms.Affine2D().rotate(th_ci).translate(x_ci, y_ci) + ax_main.transData
        car_rect.set_transform(t_c)
        ax_main.add_patch(car_rect)
        
        # 바퀴 2개
        w_r = 0.018
        u_t = np.array([np.cos(th_ci), np.sin(th_ci)])
        u_n = np.array([-np.sin(th_ci), np.cos(th_ci)])
        w1_pos = np.array([x_ci, y_ci]) - 0.032 * u_t + 0.018 * u_n
        w2_pos = np.array([x_ci, y_ci]) + 0.032 * u_t + 0.018 * u_n
        ax_main.add_patch(patches.Circle(w1_pos, w_r, facecolor='#37474f', zorder=8))
        ax_main.add_patch(patches.Circle(w2_pos, w_r, facecolor='#37474f', zorder=8))
        
        # 승객/헤드레스트 (2개 점)
        p1_pos = np.array([x_ci, y_ci]) - 0.022 * u_t + 0.095 * u_n
        p2_pos = np.array([x_ci, y_ci]) + 0.022 * u_t + 0.095 * u_n
        ax_main.plot(p1_pos[0], p1_pos[1], 'o', ms=3.5, color='#e65100', zorder=8)
        ax_main.plot(p2_pos[0], p2_pos[1], 'o', ms=3.5, color='#e65100', zorder=8)
    
    # 상단 상태 배너
    if abs(xc - xA_pos) < 0.15:
        banner_txt = '저점 A 통과: 과부하 2.23G (1643 N, 167.5 kgf)'
        banner_bg, banner_edge, banner_col = '#e3f2fd', '#90caf9', '#0d47a1'
    elif abs(xc - xB_pos) < 0.15:
        banner_txt = '정상 B 통과: 무중력 부유감 0.27G (195.8 N, 20.0 kgf)'
        banner_bg, banner_edge, banner_col = '#fff3e0', '#ffb74d', '#e65100'
    else:
        banner_txt = f'롤러코스터 주행 중 ({zone_name})'
        banner_bg, banner_edge, banner_col = '#f5f5f5', '#e0e0e0', '#424242'
    ax_main.text(-1.40, 1.12, banner_txt, fontsize=10.5, fontweight='bold', color=banner_col,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # ---------------- 2. 해석 및 FBD 비교 뷰 (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD 비교 (좌측: 저점 A, 우측: 정상 B)
    ax_calc.text(0.2, 9.7, '[승객 FBD 비교 - 저점 A vs 정상 B]', fontsize=11, fontweight='bold', color='#1565c0')
    
    # 저점 A FBD (x = 2.6, y = 7.7)
    fbd_ax, fbd_ay = 2.6, 7.7
    ax_calc.text(fbd_ax, fbd_ay + 1.6, r'저점 $A$ FBD', fontsize=11, fontweight='bold', ha='center', color='#1565c0')
    ax_calc.add_patch(patches.Circle((fbd_ax, fbd_ay), 0.50, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5))
    ax_calc.text(fbd_ax, fbd_ay, r'$75\ \mathrm{kg}$', fontsize=9.5, fontweight='bold', ha='center', va='center', color='#4a2800', zorder=6)
    
    # 저점 중력 mg (하향)
    ax_calc.annotate('', xy=(fbd_ax, fbd_ay - 1.1), xytext=(fbd_ax, fbd_ay - 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_ax + 0.12, fbd_ay - 0.9, r'$mg$', fontsize=11, fontweight='bold', color='#d32f2f')
    
    # 저점 수직항력 N_A = 1643 N (상향, 2.23배 긴 화살표)
    ax_calc.annotate('', xy=(fbd_ax, fbd_ay + 1.4), xytext=(fbd_ax, fbd_ay + 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#1565c0', lw=2.6), zorder=6)
    ax_calc.text(fbd_ax + 0.12, fbd_ay + 1.05, r'$N_A = 1643\ \mathrm{N}$' + '\n' + r'($2.23\ W$, 압박감)',
                 fontsize=9.2, fontweight='bold', color='#1565c0')
    
    # 정상 B FBD (x = 7.2, y = 7.7)
    fbd_bx, fbd_by = 7.2, 7.7
    ax_calc.text(fbd_bx, fbd_by + 1.6, r'정상 $B$ FBD', fontsize=11, fontweight='bold', ha='center', color='#e65100')
    ax_calc.add_patch(patches.Circle((fbd_bx, fbd_by), 0.50, facecolor='#d7a15c', edgecolor='#8d5b24', lw=1.4, zorder=5))
    ax_calc.text(fbd_bx, fbd_by, r'$75\ \mathrm{kg}$', fontsize=9.5, fontweight='bold', ha='center', va='center', color='#4a2800', zorder=6)
    
    # 정상 중력 mg (하향)
    ax_calc.annotate('', xy=(fbd_bx, fbd_by - 1.1), xytext=(fbd_bx, fbd_by - 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#d32f2f', lw=2.0), zorder=6)
    ax_calc.text(fbd_bx + 0.12, fbd_by - 0.9, r'$mg$', fontsize=11, fontweight='bold', color='#d32f2f')
    
    # 정상 수직항력 N_B = 196 N (상향, 0.27배 짧은 화살표)
    ax_calc.annotate('', xy=(fbd_bx, fbd_by + 0.8), xytext=(fbd_bx, fbd_by + 0.5),
                     arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.35', color='#e65100', lw=1.8), zorder=6)
    ax_calc.text(fbd_bx + 0.12, fbd_by + 0.65, r'$N_B = 196\ \mathrm{N}$' + '\n' + r'($0.27\ W$, 부유감)',
                 fontsize=9.2, fontweight='bold', color='#e65100')
    
    # (2) 이론 해석 카드 (sol_box at y = 4.65)
    sol_text = (
        "[이론 해석 및 정량 유도 (자연좌표계 n-t)]\n"
        r"• 파라미터: $m = 75.0\ \mathrm{kg},\ W = mg = 75(9.81) = 735.8\ \mathrm{N}$" + "\n"
        r"  저점 $A$: $\rho_A = 40.0\ \mathrm{m},\ v_A = 22.0\ \mathrm{m/s}$ | 정상 $B$: $\rho_B = 20.0\ \mathrm{m},\ v_B = 12.0\ \mathrm{m/s}$" + "\n"
        r"• (1) 저점 $A$ (오목 곡면, 곡률중심 상향 $\Rightarrow +n$ 상향):" + "\n"
        r"  $\sum F_n = N_A - mg = m \frac{v_A^2}{\rho_A} \Rightarrow \mathbf{N_A = m\left(g + \frac{v_A^2}{\rho_A}\right)}$" + "\n"
        r"  $N_A = 75\left(9.81 + \frac{22.0^2}{40.0}\right) = 75(9.81 + 12.10) = \mathbf{1643\ \mathrm{N}}\ (\mathbf{2.23\ W}, 167.5\ \mathrm{kgf})$" + "\n"
        r"• (2) 정상 $B$ (볼록 곡면, 곡률중심 하향 $\Rightarrow +n$ 하향):" + "\n"
        r"  $\sum F_n = mg - N_B = m \frac{v_B^2}{\rho_B} \Rightarrow \mathbf{N_B = m\left(g - \frac{v_B^2}{\rho_B}\right)}$" + "\n"
        r"  $N_B = 75\left(9.81 - \frac{12.0^2}{20.0}\right) = 75(9.81 - 7.20) = \mathbf{195.8\ \mathrm{N}}\ (\mathbf{0.27\ W}, 20.0\ \mathrm{kgf})$"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) 실시간 동적 모니터링 카드 (live_box at y = 1.05)
    live_text = (
        "[실시간 동적 모니터링]\n"
        f"• 열차 주행 위치: {zone_name} (x = {xc:+.2f} m)\n"
        f"• 추정 속력: v = {v_curr:.1f} m/s | 곡률반경: ρ = {rho_curr:.1f} m\n"
        f"• 체중계 수직항력: N = {N_curr:.1f} N (정규 체중 W = 735.8 N 대비 {N_curr/W:.2f}배)\n"
        f"• 체중계 지침 환산: {N_curr/g:.1f} kgf ({'강한 중력가속도 압박감' if N_curr > W else '무중력 부유감'})\n"
        f"• 공식 매뉴얼 검증값: N_A = 1643 N (저점), N_B = 195.8 N (정상)"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF 애니메이션 생성 및 저장
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'prob3_64_rollercoaster_scale.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[완료] 문제 3/64 한국어 애니메이션 생성 완료: {gif_path}")
