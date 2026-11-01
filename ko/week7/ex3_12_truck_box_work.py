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
동역학 9판 제3장 B편: 일과 에너지
예제 3.12 (Sample Problem 3/12) - 가속하는 트럭 적재함 위 상자의 마찰력 일
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (단일 정밀 트럭 모델)
- 솔루션 매뉴얼 검증 완료:
  * 트럭 가속도: a = 2.667 m/s^2, 이동거리: s = 75 m, 주행시간: t = 7.5 s
  * (a) μ_s=0.30, μ_k=0.28: 미끄러지지 않음, F = 213 N, U = +16.00 kJ
  * (b) μ_s=0.25, μ_k=0.20: 미끄러짐 발생, F = 157.0 N, s_box = 55.2 m, U = +8.66 kJ
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
m = 80.0            # 상자 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
s_truck_end = 75.0  # 트럭 총 주행거리 (m)
v_end = 72.0 / 3.6  # 최종 속도: 72 km/h = 20 m/s

# 트럭 등가속도 운동
a_truck = v_end**2 / (2 * s_truck_end)  # 2.667 m/s^2
t_total = v_end / a_truck               # 7.5 s

# 수직항력 및 요구 가속력
N = m * g           # 784.8 N
F_req = m * a_truck # 213.3 N

# (a) 경우
mu_s_a = 0.30
mu_k_a = 0.28
F_max_a = mu_s_a * N # 235.4 N > 213.3 N (미끄러짐 없음)
s_a = s_truck_end    # 75.0 m
U_a = F_req * s_a    # 16000 J = 16.00 kJ

# (b) 경우
mu_s_b = 0.25
mu_k_b = 0.20
F_max_b = mu_s_b * N # 196.2 N < 213.3 N (미끄러짐 발생)
F_b = mu_k_b * N     # 157.0 N
a_box_b = F_b / m    # 1.962 m/s^2
s_b = 0.5 * a_box_b * t_total**2 # 55.18 m (~55.2 m)
U_b = F_b * s_b      # 8663 J = 8.66 kJ
slip_rel = s_truck_end - s_b     # 19.8 m (상대 미끄러짐)

# 애니메이션 설정 (0~24: Case a, 25~49: Case b)
n_frames = 50
t_sub = np.linspace(0, t_total, 25)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_truck(ax, x_pos, y_pos, crate_shift, is_slip):
    # 트럭 치수 (교재 fig_ex3_12 비율)
    wheel_r = 0.65
    bed_len = 5.2
    bed_h = 0.45
    cab_w = 2.2
    cab_h = 2.0
    
    # 지면 및 도로
    ax.plot([-3, 24], [y_pos, y_pos], color='#555555', lw=2.0)
    ax.fill_between([-3, 24], y_pos - 0.6, y_pos, color='#f0eeea', edgecolor='none')
    
    # 섀시 / 평판 베드 (청록색)
    chassis_y = y_pos + wheel_r + 0.15
    ax.add_patch(patches.Rectangle((x_pos, chassis_y), bed_len, bed_h,
                                   facecolor='#1b5e73', edgecolor='#0e3a47', lw=1.8))
    # 운전석 뒤 하부 프레임
    ax.add_patch(patches.Rectangle((x_pos + bed_len, chassis_y), cab_w + 0.2, bed_h*0.7,
                                   facecolor='#1b5e73', edgecolor='#0e3a47', lw=1.5))
    
    # 연료 탱크 (원통형 은색)
    ax.add_patch(patches.Rectangle((x_pos + 1.8, y_pos + 0.25), 1.5, 0.5,
                                   facecolor='#e0e0e0', edgecolor='#757575', lw=1.2))
    
    # 운전석 캡 (베이지/황갈색)
    cab_x = x_pos + bed_len + 0.2
    cab_y = chassis_y + bed_h
    cab_poly = np.array([
        [cab_x, cab_y],
        [cab_x + cab_w, cab_y],
        [cab_x + cab_w - 0.35, cab_y + cab_h],
        [cab_x, cab_y + cab_h]
    ])
    ax.add_patch(patches.Polygon(cab_poly, facecolor='#d8a473', edgecolor='#7d471b', lw=1.8))
    
    # 운전석 창문 (연청색)
    win1 = np.array([
        [cab_x + 0.2, cab_y + 0.9],
        [cab_x + 1.0, cab_y + 0.9],
        [cab_x + 1.0, cab_y + 1.8],
        [cab_x + 0.2, cab_y + 1.8]
    ])
    win2 = np.array([
        [cab_x + 1.15, cab_y + 0.9],
        [cab_x + cab_w - 0.35, cab_y + 0.9],
        [cab_x + cab_w - 0.55, cab_y + 1.8],
        [cab_x + 1.15, cab_y + 1.8]
    ])
    ax.add_patch(patches.Polygon(win1, facecolor='#e0f2fe', edgecolor='#38bdf8', lw=1.2))
    ax.add_patch(patches.Polygon(win2, facecolor='#e0f2fe', edgecolor='#38bdf8', lw=1.2))
    
    # 바퀴 휠 및 타이어 (뒷바퀴 x_pos + 1.1, 앞바퀴 cab_x + 1.2)
    wheel_xs = [x_pos + 1.1, cab_x + 1.2]
    for wx in wheel_xs:
        # 타이어
        ax.add_patch(patches.Circle((wx, y_pos + wheel_r), wheel_r,
                                    facecolor='#333333', edgecolor='#111111', lw=1.8))
        # 림
        ax.add_patch(patches.Circle((wx, y_pos + wheel_r), wheel_r*0.55,
                                    facecolor='#b0bec5', edgecolor='#455a64', lw=1.2))
        # 휠 허브
        ax.add_patch(patches.Circle((wx, y_pos + wheel_r), wheel_r*0.2,
                                    facecolor='#eceff1', edgecolor='#37474f', lw=1.0))
        
    # 적재함 위 상자 (80 kg)
    # 기본 위치: bed 중앙 약간 앞쪽
    crate_w, crate_h = 1.7, 1.15
    crate_base_x = x_pos + 2.3 - crate_shift
    crate_base_y = chassis_y + bed_h
    ax.add_patch(patches.Rectangle((crate_base_x, crate_base_y), crate_w, crate_h,
                                   facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8))
    # 상자 띠 / 텍스처
    ax.plot([crate_base_x, crate_base_x + crate_w], [crate_base_y + crate_h/2, crate_base_y + crate_h/2],
            color='#7a4d25', lw=1)
    ax.plot([crate_base_x + crate_w/2, crate_base_x + crate_w/2], [crate_base_y, crate_base_y + crate_h],
            color='#7a4d25', lw=1)
    ax.text(crate_base_x + crate_w/2, crate_base_y + crate_h/2, '80 kg',
            fontsize=10, fontweight='bold', ha='center', va='center', color='#4a2800')
    
    # 상대 미끄러짐 표시 화살표 (미끄러짐 발생 시)
    if is_slip and crate_shift > 0.05:
        slip_arr_start = crate_base_x + crate_w + 0.1
        ax.annotate('', xy=(slip_arr_start - 0.5, crate_base_y + crate_h*0.3),
                    xytext=(slip_arr_start, crate_base_y + crate_h*0.3),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0, mutation_scale=12))
        ax.text(slip_arr_start - 0.25, crate_base_y + crate_h*0.3 + 0.2,
                '뒤로 미끄러짐', fontsize=9, fontweight='bold', color='#d32f2f', ha='center')

def update(frame):
    is_case_b = (frame >= 25)
    f_sub = frame % 25
    t = t_sub[f_sub]
    
    # 트럭 주행 물리값
    s_trk = 0.5 * a_truck * t**2
    v_trk = a_truck * t
    
    # 화면 좌표 매핑 (트럭 위치: x_min = 0 -> x_max = 10)
    truck_screen_x = (s_trk / s_truck_end) * 10.0
    
    if not is_case_b:
        # Case (a): 미끄러짐 없음 (crate_shift = 0)
        crate_shift = 0.0
        is_slip = False
        F_curr = F_req
        U_curr = F_req * s_trk
        status_title = '경우 (a): 미끄러짐 없음 (정지마찰)'
        status_sub = r'$\mu_s=0.30,\ \mu_k=0.28\ \Rightarrow\ F_{\mathrm{req}} = 213\ \mathrm{N} \leq F_{\max} = 235\ \mathrm{N}$'
        badge_bg = '#e8f5e9'
        badge_border = '#66bb6a'
    else:
        # Case (b): 미끄러짐 발생
        s_box_b_curr = 0.5 * a_box_b * t**2
        # 화면상 상자 후퇴량
        crate_shift = ((s_trk - s_box_b_curr) / slip_rel) * 1.5 if slip_rel > 0 else 0
        is_slip = (t > 0.1)
        F_curr = F_b
        U_curr = F_b * s_box_b_curr
        status_title = '경우 (b): 뒤로 미끄러짐 발생 (운동마찰)'
        status_sub = r'$\mu_s=0.25,\ \mu_k=0.20\ \Rightarrow\ F_{\mathrm{req}} = 213\ \mathrm{N} > F_{\max} = 196\ \mathrm{N}$'
        badge_bg = '#ffebee'
        badge_border = '#ef5350'
        
    # ---------------- 1. 메인 트럭 주행 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.0, 22.0)
    ax_main.set_ylim(-0.4, 6.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 트럭 그리기
    draw_truck(ax_main, truck_screen_x, 1.0, crate_shift, is_slip)
    
    # 트럭 가속도 화살표 (녹색)
    acc_x = truck_screen_x + 8.2
    ax_main.annotate('', xy=(acc_x + 1.8, 4.5), xytext=(acc_x, 4.5),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
    ax_main.text(acc_x + 0.9, 4.8, r'$a = 2.67\ \mathrm{m/s^2}$', color='#2e7d32', fontsize=11, fontweight='bold', ha='center')
    
    # 상태 알림 배너
    banner_text = f'{status_title}\n{status_sub}'
    ax_main.text(10.0, 5.8, banner_text, ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor=badge_bg, edgecolor=badge_border))
    
    # 실시간 주행 정보
    info_str = f'트럭 주행거리: $s = {s_trk:.1f}\\ /\\ 75.0\\ \\mathrm{{m}}$, 속도: $v = {v_trk*3.6:.1f}\\ /\\ 72.0\\ \\mathrm{{km/h}}$ ($t = {t:.2f}\\ \\mathrm{{s}}$)'
    ax_main.text(10.0, 0.2, info_str, ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#f5f5f5', edgecolor='#dddddd'))
    
    ax_main.set_title('예제 3.12: 가속하는 트럭 적재함 위 상자', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 자유물체도(FBD) 및 해석 뷰 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-2.8, 2.8)
    ax_fbd.set_ylim(-3.5, 3.2)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    # 상자 FBD 본체 (교재 fig_ex3_12 완벽 일치)
    fbd_w, fbd_h = 1.8, 1.1
    crate_fbd = patches.Rectangle((-fbd_w/2, 1.2 - fbd_h/2), fbd_w, fbd_h,
                                  facecolor='#e8b88a', edgecolor='#7a4d25', lw=2.0)
    ax_fbd.add_patch(crate_fbd)
    ax_fbd.text(0, 1.2, '80 kg', fontsize=10.5, fontweight='bold', ha='center', va='center', color='#4a2800')
    
    # 힘 벡터들:
    # 1) 중력: 위에서 상자 윗면으로 수직 하향 80(9.81) N
    ax_fbd.annotate('', xy=(0, 1.2 + fbd_h/2), xytext=(0, 1.2 + fbd_h/2 + 1.2),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(0, 1.2 + fbd_h/2 + 1.35, r'$80(9.81)\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center')
    
    # 2) 수직항력: 아래에서 상자 밑면으로 수직 상향 80(9.81) N
    ax_fbd.annotate('', xy=(0, 1.2 - fbd_h/2), xytext=(0, 1.2 - fbd_h/2 - 1.2),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(0, 1.2 - fbd_h/2 - 1.35, r'$80(9.81)\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center', va='top')
    
    # 3) 마찰력 F: 바닥면 좌측에서 우측으로 작용
    ax_fbd.annotate('', xy=(-fbd_w/2, 1.2 - fbd_h/2), xytext=(-fbd_w/2 - 1.3, 1.2 - fbd_h/2),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(-fbd_w/2 - 1.4, 1.2 - fbd_h/2, r'$F$', color='#d32f2f', fontsize=12, fontweight='bold', ha='right', va='center')
    
    # 4) 가속도 a 벡터 (녹색)
    ax_fbd.annotate('', xy=(fbd_w/2 + 1.3, 1.2), xytext=(fbd_w/2 + 0.2, 1.2),
                    arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=14))
    ax_fbd.text(fbd_w/2 + 1.45, 1.2, r'$a$', color='#2e7d32', fontsize=12, fontweight='bold', va='center')
    
    # 하부 비교 요약 카드
    calc_summary = (
        r"$\mathbf{해석\ 결과\ 비교\ (솔루션\ 검증):}$" "\n"
        r"(a) $\mu_s=0.30,\ \mu_k=0.28$ (미끄러짐 없음):" "\n"
        r"  $\bullet\ F = m a = 80(2.67) = \mathbf{213\ \mathrm{N}}$" "\n"
        r"  $\bullet\ U = F \cdot s = 213(75) = \mathbf{16.00\ \mathrm{kJ}}$" "\n\n"
        r"(b) $\mu_s=0.25,\ \mu_k=0.20$ (미끄러짐 발생):" "\n"
        r"  $\bullet\ F = \mu_k N = 0.20(785) = \mathbf{157.0\ \mathrm{N}}$" "\n"
        r"  $\bullet\ s_{\mathrm{box}} = \frac{1}{2}(1.962)(7.5)^2 = \mathbf{55.2\ \mathrm{m}}$" "\n"
        r"  $\bullet\ U = F \cdot s_{\mathrm{box}} = \mathbf{8.66\ \mathrm{kJ}}$"
    )
    # 한글 텍스트 분리
    calc_box_text = (
        "해석 결과 비교:\n"
        r"(a) $\mu_s=0.30,\ \mu_k=0.28$ (미끄러짐 없음):" "\n"
        r"  $\bullet\ F = m a = 80(2.67) = \mathbf{213\ \mathrm{N}}$" "\n"
        r"  $\bullet\ U = F \cdot s = 213(75) = \mathbf{16.00\ \mathrm{kJ}}$" "\n\n"
        r"(b) $\mu_s=0.25,\ \mu_k=0.20$ (미끄러짐 발생):" "\n"
        r"  $\bullet\ F = \mu_k N = 0.20(785) = \mathbf{157.0\ \mathrm{N}}$" "\n"
        r"  $\bullet\ s_{\mathrm{box}} = \frac{1}{2}(1.962)(7.5)^2 = \mathbf{55.2\ \mathrm{m}}$" "\n"
        r"  $\bullet\ U = F \cdot s_{\mathrm{box}} = \mathbf{8.66\ \mathrm{kJ}}$"
    )
    ax_fbd.text(0, -2.1, calc_box_text, fontsize=9.8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('자유물체도 (FBD) 및 마찰력 일', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_12_truck_box_work.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
