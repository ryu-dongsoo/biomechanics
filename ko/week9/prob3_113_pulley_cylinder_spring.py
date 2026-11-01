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
동역학 9판 제3장 B편: 일과 에너지 (Section 3.7 위치에너지 및 기계적 에너지 보존)
연습문제 기초 3 (Problem 3/113) - 도르래-스프링 현수 실린더의 일-에너지 해석
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 (상단 천장 마운트, 수직 스프링, 동도르래 및 실린더)
- 교재 공식 솔루션 매뉴얼 검증 완료:
  * 도르래 기구학: 실린더 낙하 h = 12 mm => 스프링 신장 Delta x = 2 * h = 24 mm
  * 초기 신장: x_1 = 0.075 m, 최종 신장: x_2 = 0.075 + 0.024 = 0.099 m
  * 중력 위치에너지: Delta V_g = -45 * 9.81 * 0.012 = -5.297 J
  * 탄성 위치에너지: Delta V_e = 0.5 * 1050 * (0.099^2 - 0.075^2) = 2.192 J
  * 에너지 보존: Delta T + Delta V_g + Delta V_e = 0  =>  v = 0.371 m/s
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
m = 45.0            # 실린더 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
k = 1050.0          # 스프링 상수 (N/m)
x1 = 0.075          # 초기 인장 변위 (m = 75 mm)
h_drop = 0.012      # 실린더 낙하 거리 (m = 12 mm)
x2 = x1 + 2.0 * h_drop # 최종 스프링 인장 변위 = 0.099 m (99 mm)

# 에너지 및 최종 속도 계산
Delta_Vg = -m * g * h_drop                     # -5.2974 J
Delta_Ve = 0.5 * k * (x2**2 - x1**2)           # +2.1924 J
T_final = - (Delta_Vg + Delta_Ve)              # 3.1050 J
v_final = np.sqrt(2.0 * T_final / m)           # 0.371 m/s

# 애니메이션 설정 (실린더 낙하 0 -> h_drop)
n_frames = 50
tau_vals = np.linspace(0, 1.0, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.1, 1.1]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.06, color='#2b2b2b', lw=2.0):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-5:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.06
    active_len = max(length - 2 * lead_len, 0.04)
    pts = [start, start + lead_len * u_par]
    step = active_len / nodes
    for i in range(1, nodes):
        sgn = 1 if i % 2 == 1 else -1
        p = start + lead_len * u_par + i * step * u_par + sgn * width * u_perp
        pts.append(p)
    pts.append(end - lead_len * u_par)
    pts.append(end)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle='round')

def update(frame):
    tau = tau_vals[frame]
    
    # 시각적 강조를 위한 수치 스케일링:
    # 실제 12 mm는 화면에서 매우 작으므로 시각적 스케일 factor 20 적용 (표기 수치는 엄밀한 실제 값)
    h_curr = h_drop * (tau**1.2)
    s_curr_disp = h_curr * 18.0   # 시각적 변위
    sp_ext_disp = 2.0 * s_curr_disp
    
    # 실제 물리값
    x_curr = x1 + 2.0 * h_curr
    Vg_curr = -m * g * h_curr
    Ve_curr = 0.5 * k * (x_curr**2 - x1**2)
    T_curr = max(- (Vg_curr + Ve_curr), 0.0)
    v_curr = np.sqrt(2.0 * T_curr / m)
    
    # ---------------- 1. 메인 시스템 기구도 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.6, 0.9)
    ax_main.set_ylim(-1.8, 0.5)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 상단 천장 해칭 (Ceiling)
    ax_main.plot([-0.4, 0.4], [0.35, 0.35], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.38, 0.34, 10):
        ax_main.plot([hx, hx + 0.04], [0.35, 0.42], color='#666666', lw=1.2)
    
    # 좌측 로프 고정 앵커: x = -0.15
    ax_main.plot([-0.15, -0.15], [0.35, 0.28], color='#2b2b2b', lw=2.0)
    ax_main.plot(-0.15, 0.28, 'o', color='#2b2b2b', markersize=4)
    
    # 스프링 상단 앵커: x = 0.08
    ax_main.plot([0.08, 0.08], [0.35, 0.25], color='#2b2b2b', lw=2.0)
    ax_main.plot(0.08, 0.25, 'o', color='#2b2b2b', markersize=4)
    
    # 스프링 하단 연결점: y = -0.55 - sp_ext_disp
    y_sp_bottom = -0.55 - sp_ext_disp
    draw_spring(ax_main, (0.08, 0.25), (0.08, y_sp_bottom), nodes=14, width=0.065, color='#2b2b2b', lw=2.0)
    ax_main.plot(0.08, y_sp_bottom, 'o', color='#2b2b2b', markersize=4)
    ax_main.text(0.18, -0.15 - sp_ext_disp * 0.5, r'$k = 1050\ \mathrm{N/m}$', fontsize=10.5, fontweight='bold', color='#1a5276')
    
    # 동도르래 중심 위치: y = -0.80 - s_curr_disp
    # 로프는 좌측 (-0.15, 0.28)에서 내려와 도르래를 감고 스프링 하단 (0.08, y_sp_bottom)으로 연결
    r_p = 0.115
    xc_p = (-0.15 + 0.08) / 2.0 # -0.035
    yc_p = -0.75 - s_curr_disp
    
    # 로프 좌측 수직선
    ax_main.plot([-0.15, -0.15], [0.28, yc_p], color='#2b2b2b', lw=2.0, zorder=3)
    # 도르래 호
    rope_arc = patches.Arc((xc_p, yc_p), 2*r_p, 2*r_p, angle=180, theta1=0, theta2=180, color='#2b2b2b', lw=2.0, zorder=3)
    ax_main.add_patch(rope_arc)
    # 로프 우측 상승선: (0.08, yc_p) -> (0.08, y_sp_bottom)
    ax_main.plot([0.08, 0.08], [yc_p, y_sp_bottom], color='#2b2b2b', lw=2.0, zorder=3)
    
    # 동도르래 휠
    pulley = patches.Circle((xc_p, yc_p), r_p, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.8, zorder=4)
    ax_main.add_patch(pulley)
    ax_main.plot(xc_p, yc_p, 'o', color='#2b2b2b', markersize=4, zorder=5)
    
    # 도르래와 실린더를 연결하는 링크
    y_cyl_top = yc_p - r_p - 0.10
    ax_main.plot([xc_p, xc_p], [yc_p, y_cyl_top], color='#2b2b2b', lw=2.5, zorder=4)
    
    # 45 kg 실린더
    cyl_w, cyl_h = 0.38, 0.42
    cyl = patches.Rectangle((xc_p - cyl_w/2, y_cyl_top - cyl_h), cyl_w, cyl_h,
                            facecolor='#b87333', edgecolor='#5a2d0c', lw=1.8, zorder=5)
    ax_main.add_patch(cyl)
    ax_main.text(xc_p, y_cyl_top - cyl_h/2, r'$45\ \mathrm{kg}$', color='#ffffff',
                 ha='center', va='center', fontsize=11, fontweight='bold', zorder=6)
    
    # 속도 화살표
    if v_curr > 0.05:
        v_scale = 0.25 * (v_curr / v_final)
        ax_main.annotate('', xy=(xc_p, y_cyl_top - cyl_h - v_scale), xytext=(xc_p, y_cyl_top - cyl_h),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(xc_p + 0.10, y_cyl_top - cyl_h - v_scale/2, f'$v$', color='#27ae60', fontsize=11, fontweight='bold')
    
    # 초기 기준선 및 변위 표시
    ax_main.plot([-0.4, 0.3], [-0.75 - r_p - 0.10, -0.75 - r_p - 0.10], color='#999999', ls=':', lw=1.0)
    ax_main.text(-0.45, -0.85, r'$h = 12\ \mathrm{mm}$', fontsize=9.5, color='#444444')
    
    ax_main.set_title('문제 3/113 기구도 (도르래-스프링 현수 시스템)', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. 실시간 에너지 보존 & 이론 검증 패널 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    # 에너지 막대 그래프 (T, Ve, Vg, Etot)
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, T_curr + Ve_curr + Vg_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$\Delta V_e$', r'$\Delta V_g$', r'$\Delta E_{\mathrm{tot}}$']
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 6.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.2f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"【교재 공식 일-에너지 해석 (Problem 3/113)】\n"
        f"• 시스템 일-에너지 방정식: $T_1 + V_1 + U'_{{1-2}} = T_2 + V_2$\n"
        f"  $\\frac{{1}}{{2}}mv_1^2 + \\frac{{1}}{{2}}kx_1^2 + 0 = \\frac{{1}}{{2}}mv^2 + \\frac{{1}}{{2}}kx_2^2 - mgh$\n"
        f"• 도르래 기구학 관계: 스프링 신장량은 실린더 낙하량의 2배!\n"
        f"  $h = 12\\ \\mathrm{{mm}} = 0.012\\ \\mathrm{{m}}$\n"
        f"  $x_2 = 0.075 + 2(0.012) = 0.099\\ \\mathrm{{m}}$\n"
        f"• 수치 대입:\n"
        f"  $\\frac{{1}}{{2}}(1050)(0.075)^2 = \\frac{{1}}{{2}}(45)v^2 + \\frac{{1}}{{2}}(1050)(0.099)^2$\n"
        f"                                        $- 45(9.81)(0.012)$\n"
        f"  $2.953 = 22.5 v^2 + 5.146 - 5.297$\n"
        f"  $22.5 v^2 = 3.105\\ \\rightarrow\\ v = \\mathbf{{0.371\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• 실린더 낙하: $h = {h_curr*1000:.1f}\\ \\mathrm{{mm}},\\quad$ 속도: $v = {v_curr:.3f}\\ \\mathrm{{m/s}}$"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.0, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('기계적 에너지 보존 모니터 및 검증', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_113_pulley_cylinder_spring.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
