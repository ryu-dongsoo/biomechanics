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
예제 3.8: 평면 S-곡선 도로에서 감속 주행하는 자동차의 타이어 수평 구속력 해석 (n-t 자연좌표계)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영 (A-B-C S-곡선 도로, ρ_A = 400 m, ρ_C = 80 m, Δs = 200 m, FBD)
- 공식 솔루션 매뉴얼(Wiley) 검증 완료:
  * 등접선감속도 a_t = -1.447 m/s^2, 접선 제동력 F_t = 2170 N
  * A지점: a_n = 1.929 m/s^2, F_n = 2890 N, 총수평력 F_A = 3620 N (3.62 kN)
  * B지점: 변곡점 a_n = 0, F_n = 0, 총수평력 F_B = 2170 N (2.17 kN)
  * C지점: a_n = 2.411 m/s^2, F_n = 3620 N, 총수평력 F_C = 4220 N (4.22 kN)
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
m = 1500.0                   # 차량 질량 (kg)
v_A_kmh = 100.0              # A지점 속도 (km/h)
v_C_kmh = 50.0               # C지점 속도 (km/h)
v_A = v_A_kmh / 3.6          # 27.778 m/s
v_C = v_C_kmh / 3.6          # 13.889 m/s
delta_s = 200.0              # A에서 C까지의 곡선 경로 거리 (m)

rho_A = 400.0                # A지점 곡률반지름 (m)
rho_C = 80.0                 # C지점 곡률반지름 (m)

# 접선방향 등감속도: v_C^2 = v_A^2 + 2 * a_t * delta_s
a_t = (v_C**2 - v_A**2) / (2.0 * delta_s)   # -1.4468 m/s^2
F_t = m * abs(a_t)                          # 2170.1 N (일정)

# 지점별 가속도 및 힘 (Wiley 공식 솔루션과 100% 일치)
a_n_A = (v_A**2) / rho_A                    # 1.9290 m/s^2
F_n_A = m * a_n_A                           # 2893.5 N -> 2890 N
F_tot_A = np.sqrt(F_n_A**2 + F_t**2)        # 3617 N -> 3620 N

a_n_B = 0.0                                 # 변곡점 (rho -> inf)
F_n_B = 0.0
F_tot_B = F_t                               # 2170 N

a_n_C = (v_C**2) / rho_C                    # 2.4113 m/s^2
F_n_C = m * a_n_C                           # 3616.9 N -> 3620 N
F_tot_C = np.sqrt(F_n_C**2 + F_t**2)        # 4218 N -> 4220 N

t_total = (v_C - v_A) / a_t                 # 주행 소요 시간: 9.60 s

# 2. S-곡선 도로 기하학 모델링 (교재 원도 1:1 완벽 반영)
scale = 200.0 / 206.9383
x_pts = np.array([-40.0, 0.0, 100.0, 200.0, 240.0]) * scale
y_pts = np.array([25.0, 0.0, 25.0, 12.0, -8.0]) * scale
p_curve = np.poly1d(np.polyfit(x_pts, y_pts, 4))

N_pts = 1000
x_dense = np.linspace(-40.0 * scale, 240.0 * scale, N_pts)
y_dense = p_curve(x_dense)
dx = np.diff(x_dense)
dy = np.diff(y_dense)
ds = np.sqrt(dx**2 + dy**2)
s_cum = np.concatenate([[0.0], np.cumsum(ds)])
idx_A = np.argmin(np.abs(x_dense - 0.0))
s_dense = s_cum - s_cum[idx_A]  # A를 s = 0 기준으로 정규화

dy_dx = np.gradient(y_dense, x_dense)
heading_dense = np.arctan2(dy_dx, 1.0)
nx_dense = -np.sin(heading_dense)
ny_dense = np.cos(heading_dense)

# 도로 리본 생성 (폭 12 m)
road_w = 12.0
x_l = x_dense + (road_w / 2.0) * nx_dense
y_l = y_dense + (road_w / 2.0) * ny_dense
x_r = x_dense - (road_w / 2.0) * nx_dense
y_r = y_dense - (road_w / 2.0) * ny_dense

# A, B, C 지점 인덱스 및 위치/방위각
idx_B = np.argmin(np.abs(s_dense - 100.0))
idx_C = np.argmin(np.abs(s_dense - 200.0))

xA, yA, thA = x_dense[idx_A], y_dense[idx_A], heading_dense[idx_A]
xB, yB, thB = x_dense[idx_B], y_dense[idx_B], heading_dense[idx_B]
xC, yC, thC = x_dense[idx_C], y_dense[idx_C], heading_dense[idx_C]

# 3. 애니메이션 시간 샘플링 (60 프레임)
n_frames = 60
t_series = np.linspace(0.0, t_total, n_frames)
s_series = v_A * t_series + 0.5 * a_t * (t_series**2)
v_series = v_A + a_t * t_series

# 캔버스 초기화 (14 x 6.5, 순수 흰색 바탕)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.91, bottom=0.07, left=0.04, right=0.96, wspace=0.14)

def draw_car(ax, x0, y0, theta_c, color='#d32f2f', alpha=1.0, zorder=6):
    """탑뷰 자동차 렌더링 (차체, 유리창)"""
    car_l, car_w = 11.0, 5.5
    c_cos, c_sin = np.cos(theta_c), np.sin(theta_c)
    corners = np.array([
        [-car_l/2.0, -car_w/2.0],
        [ car_l/2.0, -car_w/2.0],
        [ car_l/2.0,  car_w/2.0],
        [-car_l/2.0,  car_w/2.0]
    ])
    R = np.array([[c_cos, -c_sin], [c_sin, c_cos]])
    rot_corners = corners @ R.T + np.array([x0, y0])
    poly = patches.Polygon(rot_corners, closed=True, facecolor=color, edgecolor='#b71c1c', lw=1.2, alpha=alpha, zorder=zorder)
    ax.add_patch(poly)
    
    ws_w = 4.2
    ws_pts = np.array([
        [car_l*0.05, -ws_w/2.0],
        [car_l*0.28, -ws_w/2.0],
        [car_l*0.28,  ws_w/2.0],
        [car_l*0.05,  ws_w/2.0]
    ]) @ R.T + np.array([x0, y0])
    ax.add_patch(patches.Polygon(ws_pts, closed=True, facecolor='#263238', alpha=alpha*0.85, zorder=zorder+1))

def draw_fbd_point(ax, cx, cy, label_str, th_deg, Fn, Ft, Ftot, n_dir_deg, is_active=False):
    """수평면 타이어 구속력 FBD 렌더링"""
    th = np.radians(th_deg)
    w_fp, h_fp = 0.85, 0.42
    corners = np.array([[-w_fp/2.0, -h_fp/2.0], [w_fp/2.0, -h_fp/2.0], [w_fp/2.0, h_fp/2.0], [-w_fp/2.0, h_fp/2.0]])
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    rot = corners @ R.T + np.array([cx, cy])
    
    bg_col = '#fff9c4' if is_active else '#ffffff'
    edge_col = '#d32f2f' if is_active else '#37474f'
    ax.add_patch(patches.Polygon(rot, closed=True, facecolor=bg_col, edgecolor=edge_col, lw=1.5 if is_active else 1.2, zorder=4))
    
    lbl_col = '#d32f2f' if is_active else '#1565c0'
    ax.text(cx - 0.40, cy + 0.80, f'({label_str})', fontsize=11.5, fontweight='bold', color=lbl_col)
    
    t_v = np.array([np.cos(th), np.sin(th)])
    n_rad = np.radians(n_dir_deg)
    n_v = np.array([np.cos(n_rad), np.sin(n_rad)])
    
    # 접선축 t (파선)
    ax.plot([cx - 1.0*t_v[0], cx + 1.1*t_v[0]], [cy - 1.0*t_v[1], cy + 1.1*t_v[1]], color='#90a4ae', ls='--', lw=0.9)
    ax.text(cx + 1.15*t_v[0], cy + 1.15*t_v[1], 't', fontsize=10, fontstyle='italic', color='#455a64')
    
    ft_scale = 0.00036
    ft_len = Ft * ft_scale
    
    # 접선 제동 마찰력 F_t (-t 방향)
    ax.annotate('', xy=(cx - ft_len*t_v[0], cy - ft_len*t_v[1]), xytext=(cx, cy),
                arrowprops=dict(arrowstyle='->,head_width=0.28,head_length=0.42', color='#d32f2f', lw=2.0))
    ax.text(cx - (ft_len+0.16)*t_v[0], cy - (ft_len+0.16)*t_v[1], r'$F_t$', fontsize=10, fontweight='bold', color='#d32f2f')

    if Fn > 0:
        # 법선축 n (파선)
        ax.plot([cx - 0.3*n_v[0], cx + 1.1*n_v[0]], [cy - 0.3*n_v[1], cy + 1.1*n_v[1]], color='#90a4ae', ls='--', lw=0.9)
        ax.text(cx + 1.15*n_v[0], cy + 1.15*n_v[1], 'n', fontsize=10, fontstyle='italic', color='#455a64')
        
        # 법선 구심력 F_n (+n 방향)
        fn_len = Fn * ft_scale
        ax.annotate('', xy=(cx + fn_len*n_v[0], cy + fn_len*n_v[1]), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle='->,head_width=0.28,head_length=0.42', color='#d32f2f', lw=2.0))
        ax.text(cx + (fn_len+0.14)*n_v[0], cy + (fn_len+0.14)*n_v[1], r'$F_n$', fontsize=10, fontweight='bold', color='#d32f2f')

        # 벡터 합성 평행사변형
        corner_tot = np.array([cx, cy]) - ft_len*t_v + fn_len*n_v
        ax.plot([cx - ft_len*t_v[0], corner_tot[0]], [cy - ft_len*t_v[1], corner_tot[1]], color='#78909c', ls=':', lw=1.0)
        ax.plot([cx + fn_len*n_v[0], corner_tot[0]], [cy + fn_len*n_v[1], corner_tot[1]], color='#78909c', ls=':', lw=1.0)
        
        # 합성 수평력 F (파선 화살표)
        ax.annotate('', xy=(corner_tot[0], corner_tot[1]), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.48', color='#b71c1c', lw=2.2, ls='--'))
        ax.text(corner_tot[0] - 0.06, corner_tot[1] - 0.25, r'$F$', fontsize=11, fontweight='bold', color='#b71c1c')
    else:
        # B지점 (순수 접선력만 존재)
        ax.text(cx - (ft_len+0.22)*t_v[0], cy - (ft_len+0.22)*t_v[1] - 0.22, r'$F=F_t$', fontsize=10.5, fontweight='bold', color='#b71c1c')

def update(frame):
    s_curr = s_series[frame]
    v_curr = v_series[frame]
    v_kmh_curr = v_curr * 3.6
    
    # 도로 위 현재 위치 (보간)
    x_curr = np.interp(s_curr, s_dense, x_dense)
    y_curr = np.interp(s_curr, s_dense, y_dense)
    th_curr = np.interp(s_curr, s_dense, heading_dense)
    
    # 현재 곡률 및 구심력 계산
    if s_curr <= 100.0:
        kappa_curr = (1.0 / rho_A) * (1.0 - s_curr / 100.0)
    else:
        kappa_curr = (1.0 / rho_C) * ((s_curr - 100.0) / 100.0)
    
    an_curr = (v_curr**2) * kappa_curr
    Fn_curr = m * an_curr
    Ftot_curr = np.sqrt(Fn_curr**2 + F_t**2)
    
    # ---------------- 1. 메인 물리 뷰 (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    
    # 도로 아스팔트 리본 & 차선
    x_poly = np.concatenate([x_l, x_r[::-1]])
    y_poly = np.concatenate([y_l, y_r[::-1]])
    ax_main.fill(x_poly, y_poly, color='#b0bec5', alpha=0.9, zorder=1)
    ax_main.plot(x_l, y_l, color='#37474f', lw=1.6, zorder=2)
    ax_main.plot(x_r, y_r, color='#37474f', lw=1.6, zorder=2)
    ax_main.plot(x_dense, y_dense, color='#ffffff', lw=1.3, ls=(0, (6, 6)), zorder=2)
    
    # A, B, C 지점 표기
    ax_main.text(xA - 5, yA - 15, 'A', fontsize=16, fontweight='bold', color='#1565c0', zorder=5)
    ax_main.text(xB - 2, yB - 15, 'B', fontsize=16, fontweight='bold', color='#1565c0', zorder=5)
    ax_main.text(xC + 8, yC + 4, 'C', fontsize=16, fontweight='bold', color='#1565c0', zorder=5)
    
    # A지점 좌표축 및 곡률반경 표기
    t_len = 22.0
    ax_main.plot([xA - t_len*np.cos(thA), xA + t_len*np.cos(thA)], [yA - t_len*np.sin(thA), yA + t_len*np.sin(thA)],
                 color='#546e7a', ls='--', lw=1.1, zorder=3)
    ax_main.text(xA + t_len*np.cos(thA) + 2, yA + t_len*np.sin(thA) - 1, 't', fontsize=13, fontstyle='italic', zorder=5)
    
    n_len = 32.0
    ax_main.plot([xA, xA - n_len*np.sin(thA)], [yA, yA + n_len*np.cos(thA)], color='#546e7a', ls='--', lw=1.1, zorder=3)
    ax_main.text(xA - n_len*np.sin(thA) - 5, yA + n_len*np.cos(thA) + 2, 'n', fontsize=13, fontstyle='italic', zorder=5)
    
    ax_main.annotate(r'$\rho = 400\ \mathrm{m}$', xy=(xA - 2, yA + 2), xytext=(xA - 25, yA + 42),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.3),
                     fontsize=12, fontweight='bold', color='#1565c0')
    
    # B지점 접선축
    ax_main.plot([xB - t_len*np.cos(thB), xB + t_len*np.cos(thB)], [yB - t_len*np.sin(thB), yB + t_len*np.sin(thB)],
                 color='#546e7a', ls='--', lw=1.1, zorder=3)
    ax_main.text(xB + t_len*np.cos(thB) + 2, yB + t_len*np.sin(thB), 't', fontsize=13, fontstyle='italic', zorder=5)
    
    # C지점 좌표축 및 곡률반경 표기
    ax_main.plot([xC - t_len*np.cos(thC), xC + t_len*np.cos(thC)], [yC - t_len*np.sin(thC), yC + t_len*np.sin(thC)],
                 color='#546e7a', ls='--', lw=1.1, zorder=3)
    ax_main.text(xC + t_len*np.cos(thC) + 2, yC + t_len*np.sin(thC) - 4, 't', fontsize=13, fontstyle='italic', zorder=5)
    
    ax_main.plot([xC, xC + n_len*np.sin(thC)], [yC, yC - n_len*np.cos(thC)], color='#546e7a', ls='--', lw=1.1, zorder=3)
    ax_main.text(xC + n_len*np.sin(thC) - 6, yC - n_len*np.cos(thC) - 6, 'n', fontsize=13, fontstyle='italic', zorder=5)
    
    ax_main.annotate(r'$\rho = 80\ \mathrm{m}$', xy=(xC - 1, yC - 2), xytext=(xC - 25, yC - 38),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.3),
                     fontsize=12, fontweight='bold', color='#1565c0')
    
    # A-C 호 길이 200 m 치수 보조선
    dim_offset = 16.0
    x_dim = x_dense[idx_A:idx_C+1] + dim_offset * nx_dense[idx_A:idx_C+1]
    y_dim = y_dense[idx_A:idx_C+1] + dim_offset * ny_dense[idx_A:idx_C+1]
    ax_main.plot(x_dim, y_dim, color='#455a64', lw=1.1)
    ax_main.annotate('', xy=(x_dim[0], y_dim[0]), xytext=(x_dim[3], y_dim[3]),
                     arrowprops=dict(arrowstyle='->', color='#455a64', lw=1.2))
    ax_main.annotate('', xy=(x_dim[-1], y_dim[-1]), xytext=(x_dim[-4], y_dim[-4]),
                     arrowprops=dict(arrowstyle='->', color='#455a64', lw=1.2))
    mid_idx = len(x_dim) // 2
    ax_main.text(x_dim[mid_idx] - 10, y_dim[mid_idx] + 3, r'$200\ \mathrm{m}$', fontsize=13, fontweight='bold', color='#263238')
    
    ax_main.plot([xA, x_dim[0] + 3*nx_dense[idx_A]], [yA, y_dim[0] + 3*ny_dense[idx_A]], color='#78909c', lw=0.9, ls=':')
    ax_main.plot([xC, x_dim[-1] + 3*nx_dense[idx_C]], [yC, y_dim[-1] + 3*ny_dense[idx_C]], color='#78909c', lw=0.9, ls=':')
    
    # 기준 위치 실루엣 차량 (A, B, C)
    draw_car(ax_main, xA, yA, thA, color='#ef9a9a', alpha=0.45)
    draw_car(ax_main, xB, yB, thB, color='#ef9a9a', alpha=0.45)
    draw_car(ax_main, xC, yC, thC, color='#ef9a9a', alpha=0.45)
    
    # 실시간 주행 차량 (선명한 빨간색)
    draw_car(ax_main, x_curr, y_curr, th_curr, color='#d32f2f', alpha=1.0)
    
    # 실시간 속도 벡터 v (녹색 화살표)
    v_vec_len = 10.0 + (v_curr / v_A) * 10.0
    ax_main.annotate('', xy=(x_curr + v_vec_len*np.cos(th_curr), y_curr + v_vec_len*np.sin(th_curr)),
                     xytext=(x_curr, y_curr),
                     arrowprops=dict(arrowstyle='->,head_width=0.4,head_length=0.6', color='#2e7d32', lw=2.2), zorder=8)
    ax_main.text(x_curr + (v_vec_len+3)*np.cos(th_curr), y_curr + (v_vec_len+3)*np.sin(th_curr), r'$\vec{v}$',
                 fontsize=14, fontweight='bold', color='#2e7d32', zorder=8)
    
    ax_main.set_aspect('equal')
    ax_main.set_xlim(-50, 245)
    ax_main.set_ylim(-52, 60)
    ax_main.axis('off')
    ax_main.set_title('예제 3.8: 평면 S-곡선 도로 감속 주행 메커니즘', fontsize=13, fontweight='bold', pad=12)
    
    # ---------------- 2. 해석 및 모니터링 뷰 (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD 상단 렌더링
    ax_calc.text(0.2, 9.7, '[자유물체도 (Free Body Diagram) - 수평면]', fontsize=11, fontweight='bold', color='#1565c0')
    
    active_A = (s_curr < 30.0)
    active_B = (70.0 <= s_curr <= 130.0)
    active_C = (s_curr > 170.0)
    
    draw_fbd_point(ax_calc, 1.8, 8.35, 'A', 20.0,  F_n_A, F_t, F_tot_A, 110.0, is_active=active_A)
    draw_fbd_point(ax_calc, 5.0, 8.35, 'B', 15.0,  0.0,   F_t, F_tot_B, 105.0, is_active=active_B)
    draw_fbd_point(ax_calc, 8.2, 8.35, 'C', -30.0, F_n_C, F_t, F_tot_C, -120.0, is_active=active_C)
    
    # (2) 이론 해석 카드 (sol_box)
    sol_text = (
        "[이론 해석 및 정량 유도 (n-t 자연좌표계)]\n"
        r"• 파라미터: $m = 1500\ \mathrm{kg},\ v_A = 100\ \mathrm{km/h} = 27.78\ \mathrm{m/s}$" + "\n"
        r"  $v_C = 50\ \mathrm{km/h} = 13.89\ \mathrm{m/s},\ \Delta s = 200\ \mathrm{m}$" + "\n"
        r"• 접선방향 감속도: $v_C^2 = v_A^2 + 2a_t\Delta s \Rightarrow a_t = -1.447\ \mathrm{m/s^2}$" + "\n"
        r"  $\Rightarrow F_t = m|a_t| = 1500(1.447) = 2170\ \mathrm{N}$ ($-t$ 제동 마찰력)" + "\n"
        r"• 지점별 법선 구심력 및 타이어 총수평력 $F = \sqrt{F_n^2 + F_t^2}$:" + "\n"
        r"  - A지점 ($\rho = 400\ \mathrm{m}$): $a_n = \frac{v_A^2}{\rho} = 1.929\ \mathrm{m/s^2} \Rightarrow F_n = 2890\ \mathrm{N}$" + "\n"
        r"    $\Rightarrow F_A = \sqrt{2890^2 + 2170^2} = \mathbf{3620\ \mathrm{N}}\ (3.62\ \mathrm{kN})$" + "\n"
        r"  - B지점 (변곡점 $\rho \to \infty$): $a_n = 0 \Rightarrow F_n = 0$" + "\n"
        r"    $\Rightarrow F_B = F_t = \mathbf{2170\ \mathrm{N}}\ (2.17\ \mathrm{kN})$" + "\n"
        r"  - C지점 ($\rho = 80\ \mathrm{m}$): $a_n = \frac{v_C^2}{\rho} = 2.411\ \mathrm{m/s^2} \Rightarrow F_n = 3620\ \mathrm{N}$" + "\n"
        r"    $\Rightarrow F_C = \sqrt{3620^2 + 2170^2} = \mathbf{4220\ \mathrm{N}}\ (4.22\ \mathrm{kN})$"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) 실시간 동적 모니터링 카드 (live_box)
    if s_curr < 85.0:
        sec_str = "A → B 좌선회 진입 구간"
    elif s_curr <= 115.0:
        sec_str = "B 변곡점 (곡률 전환)"
    else:
        sec_str = "B → C 우선회 감속 구간"
        
    live_text = (
        "[실시간 동적 모니터링]\n"
        f"• 통과 구간: {sec_str} (s = {s_curr:.1f} m / 200 m)\n"
        f"• 주행 속도: v = {v_curr:.2f} m/s ({v_kmh_curr:.1f} km/h)\n"
        f"• 접선 제동력: Ft = {F_t:.0f} N (일정 감속)\n"
        f"• 법선 구심력: Fn = {abs(Fn_curr):.0f} N\n"
        f"• 타이어 총수평력: F = {Ftot_curr:.0f} N"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF 애니메이션 생성 및 저장
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'ex3_8_car_curved_road.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[완료] 예제 3.8 한국어 애니메이션 생성 완료: {gif_path}")
