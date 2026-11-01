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
[동역학 9판 예제 3.5] 수직 가이드 봉을 따라 움직이는 칼라의 방향 가변 외력(θ=kt) 하에서의 FBD 및 운동역학
교재 원본 삽화 및 완벽한 분리형 FBD 100% 동일 구현 + 고리 작동 범위(Stroke) 뷰포트 내 완벽 수용
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터
m = 2.0            # 칼라 질량 (kg)
mu_k = 0.25        # 운동마찰계수
g = 9.81           # 중력가속도 (m/s^2)
k_rate = 1.0       # 각속도 k (rad/s)

# θ = π/2 에서 v = 0 이 되는 필요 일정 외력 F
# F = (m * g * π) / [2 * (1 - μ_k)]
F_val = (m * g * np.pi) / (2.0 * (1.0 - mu_k))  # 약 41.09 N
t_final = np.pi / (2.0 * k_rate)                 # 약 1.5708 s

# 애니메이션 설정
fps = 30
duration = t_final
n_sim_frames = int(fps * duration)
n_pause_frames = 20
total_frames = n_sim_frames + n_pause_frames

t_eval = np.linspace(0, duration, n_sim_frames)

fig = plt.figure(figsize=(15.2, 8.4), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.01, 0.02, 0.98, 0.92])
title_text = '[동역학 9판 예제 3.5] 방향이 변하는 외력(θ = kt)을 받는 원통형 칼라(2kg)의 FBD 및 수직 상승 운동'

def get_motion(t):
    t_c = min(t, t_final)
    th = k_rate * t_c
    
    # v(t) = (F / (m*k)) * sin(kt) - g*t + (mu_k * F / (m*k)) * (cos(kt) - 1)
    v = (F_val / (m * k_rate)) * np.sin(th) - g * t_c + (mu_k * F_val / (m * k_rate)) * (np.cos(th) - 1.0)
    if t >= t_final:
        v = 0.0
        
    # y(t) = (F / (m*k^2)) * (1 - cos(kt)) - 0.5*g*t^2 + (mu_k * F / (m*k^2)) * (sin(kt) - kt)
    y = (F_val / (m * k_rate**2)) * (1.0 - np.cos(th)) - 0.5 * g * (t_c**2) + (mu_k * F_val / (m * k_rate**2)) * (np.sin(th) - th)
    
    # N(t) = F * sin(kt)
    N = F_val * np.sin(th)
    # f_k(t) = mu_k * N
    f_k = mu_k * N
    # a_y(t) = (F*cos(kt) - m*g - mu_k*F*sin(kt)) / m
    a_y = (F_val * np.cos(th) - m * g - mu_k * N) / m
    if t >= t_final:
        a_y = 0.0
        
    return th, y, v, N, f_k, a_y

def update(frame):
    if frame < n_sim_frames:
        t = t_eval[frame]
    else:
        t = duration
        
    th, y_val, v, N, f_k, a_y = get_motion(t)
    th_deg = np.degrees(th)
    mid_th = th / 2.0
    
    ax.clear()
    ax.set_xlim(-0.8, 27.2)
    ax.set_ylim(-0.6, 14.8)
    ax.axis('off')
    
    # 전체 배경
    ax.add_patch(patches.Rectangle((-0.8, -0.6), 28.0, 15.4, fc='#f8fafc', ec='none', zorder=1))
    
    # =============================================================
    # [패널 1] 좌측: HUD 이론 / 수식 전개 및 실시간 상태 카드
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.6, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.9, 13.4, '[예제 3.5 운동역학 해석]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([-0.1, 7.9], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ 물리 매개변수 (Given)\n"
        f"  • 칼라 질량: m = {m:.1f} kg\n"
        f"  • 운동마찰계수: μ_k = {mu_k:.2f}\n"
        f"  • 각변화율: k = {k_rate:.1f} rad/s  (θ = kt)\n"
        f"  • 중력가속도: g = {g:.2f} m/s²\n\n"
        "■ 운동방정식 (Equations of Motion)\n"
        "  • 수평 평형 (ΣFx = 0):\n"
        "    N - F sin(kt) = 0 ⇒ N = F sin(kt)\n"
        "  • 운동마찰력 (f_k):\n"
        "    f_k = μ_k N = μ_k F sin(kt)\n"
        "  • 수직 운동방정식 (ΣFy = m a_y):\n"
        "    m(dv/dt) = F cos(kt) - mg - μ_k F sin(kt)\n\n"
        "■ 속도 적분 및 정지 조건\n"
        "  • v(t) = (F/mk)sin(kt) - gt + (μ_k F/mk)[cos(kt)-1]\n"
        "  • θ = π/2 (90°), t = π/(2k) = 1.57 s 에서 v = 0:\n"
        f"    F = (mgπ) / [2(1 - μ_k)] = {F_val:.2f} N (일정)\n"
        f"  • 최대 상승 변위: y_max = 5.51 m"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=8.2, va='top', fontproperties=font_prop, linespacing=1.38, zorder=5)
    
    ax.plot([-0.1, 7.9], [4.1, 4.1], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.9, 3.8, '[실시간 상태 계측 (HUD)]', fontsize=9.8, fontweight='bold', color='#0284c7', ha='center', fontproperties=font_prop, zorder=5)
    
    status_str = (
        f"• 경과 시간:   t = {t:4.2f} s / {t_final:4.2f} s\n"
        f"• 힘의 각도:   θ = {th_deg:4.1f}° / 90.0°\n"
        f"• 상승 변위:   y(t) = {y_val:4.2f} m / 5.51 m\n"
        f"• 현재 속도:   v(t) = {v:4.2f} m/s\n"
        f"• 현재 가속도: a_y  = {a_y:4.2f} m/s²\n"
        f"• 수직항력:   N(t) = {N:4.2f} N\n"
        f"• 마찰력:     f_k  = {f_k:4.2f} N"
    )
    ax.text(0.1, 3.4, status_str, fontsize=8.2, va='top', family='monospace', fontproperties=font_prop, linespacing=1.35, zorder=5)
    
    # =============================================================
    # [패널 2] 중앙: 실제 물리 시스템 (수직 환봉 & 칼라 작동 메커니즘)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.6, 0.2), 9.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.2, 13.4, '[실제 물리 메커니즘 (Physical System)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([8.9, 17.5], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # 가이드 봉 파라미터
    rod_x = 13.2
    ground_y = 1.0
    rod_top_y = 12.6
    rod_w = 0.50
    
    # 1) 베이스 지면
    ax.add_patch(patches.Rectangle((rod_x - 3.4, ground_y - 0.7), 6.8, 0.7,
                                   fc='#e2e8f0', ec='#64748b', lw=1.4, zorder=3))
    ax.plot([rod_x - 3.4, rod_x + 3.4], [ground_y, ground_y], color='#334155', lw=2.2, zorder=4)
    for hx in np.linspace(rod_x - 3.2, rod_x + 3.2, 15):
        ax.plot([hx, hx - 0.25], [ground_y, ground_y - 0.3], color='#94a3b8', lw=1.0, zorder=3)
        
    # 2) 수직 환봉 (하늘색 가이드 샤프트)
    ax.add_patch(patches.Rectangle((rod_x - rod_w/2, ground_y), rod_w, rod_top_y - ground_y,
                                   fc='#bae6fd', ec='#0284c7', lw=1.3, zorder=4))
    ax.add_patch(patches.Ellipse((rod_x, rod_top_y), rod_w, 0.18, fc='#7dd3fc', ec='#0284c7', lw=1.1, zorder=5))
    ax.plot([rod_x, rod_x], [ground_y, rod_top_y + 0.3], color='#64748b', lw=1.0, linestyle='-.', zorder=3)
    ax.text(rod_x + 0.45, ground_y + 0.4, r'$\mu_k = 0.25$', fontsize=9.0, fontweight='bold', color='#0284c7', zorder=6)
    
    # 3) 칼라의 작동 스트로크 스케일링
    y_scale = 1.35
    y_start_y = 2.4
    collar_y = y_start_y + y_val * y_scale
    col_w = 1.6
    col_h = 2.2
    
    # 4) 좌측 변위 눈금자 & 작동 범위 (Ruler / Stroke Guide)
    ruler_x = 9.4
    ax.plot([ruler_x, ruler_x], [y_start_y, y_start_y + 5.51 * y_scale], color='#64748b', lw=1.5, zorder=5)
    
    for y_mark in [0.0, 2.0, 4.0, 5.51]:
        my = y_start_y + y_mark * y_scale
        ax.plot([ruler_x - 0.15, ruler_x + 0.15], [my, my], color='#475569', lw=1.2, zorder=5)
        ax.text(ruler_x - 0.25, my, f"{y_mark:.1f}m", fontsize=7.6, color='#475569', ha='right', va='center', fontproperties=font_prop, zorder=6)
        
    # 초기 위치 기준선 (y=0)
    ax.plot([ruler_x, rod_x + 2.5], [y_start_y, y_start_y], color='#94a3b8', lw=1.1, linestyle=':', zorder=3)
    ax.text(rod_x + 2.6, y_start_y, 'y = 0 (초기 기준)', fontsize=7.8, color='#64748b', va='center', fontproperties=font_prop, zorder=6)
    
    # 최고점 도달 목표선 (y=5.51m)
    y_top_target = y_start_y + 5.51 * y_scale
    ax.plot([ruler_x, rod_x + 2.5], [y_top_target, y_top_target], color='#dc2626', lw=1.1, linestyle='--', alpha=0.7, zorder=3)
    ax.text(ruler_x + 0.3, y_top_target + 0.3, 'y_max = 5.51 m (v = 0)', fontsize=7.8, fontweight='bold', color='#dc2626', va='bottom', fontproperties=font_prop, zorder=6)
    
    # 현재 위치 표시 및 변위 화살표
    if y_val > 0.08:
        ax.annotate('', xy=(ruler_x, collar_y), xytext=(ruler_x, y_start_y),
                    arrowprops=dict(arrowstyle='<->', color='#2563eb', lw=1.5), zorder=6)
        ax.text(ruler_x + 0.2, (y_start_y + collar_y)/2, f"y = {y_val:.2f} m",
                fontsize=8.2, fontweight='bold', color='#2563eb', va='center', fontproperties=font_prop, zorder=7)
    
    # 5) 원통형 칼라 (Collar)
    col_left = rod_x - col_w/2
    col_bot = collar_y - col_h/2
    
    ax.add_patch(patches.Rectangle((col_left, col_bot), col_w, col_h,
                                   fc='#ea997b', ec='#802611', lw=1.5, zorder=6))
    ax.plot([rod_x - rod_w/2, rod_x - rod_w/2], [col_bot, col_bot + col_h], color='#802611', lw=0.9, linestyle='--', zorder=7)
    ax.plot([rod_x + rod_w/2, rod_x + rod_w/2], [col_bot, col_bot + col_h], color='#802611', lw=0.9, linestyle='--', zorder=7)
    
    ax.add_patch(patches.Ellipse((rod_x, col_bot + col_h), col_w, 0.32,
                                 fc='#f2bba7', ec='#802611', lw=1.3, zorder=8))
    ax.add_patch(patches.Arc((rod_x, col_bot), col_w, 0.32, angle=0, theta1=180, theta2=360,
                             color='#802611', lw=1.3, zorder=8))
    
    ax.text(col_left + col_w + 0.25, collar_y - 0.05, r'$m$', fontsize=11.0, fontweight='bold', color='#802611', va='center', zorder=9)
    
    # 6) 중앙 피벗 핀
    ax.add_patch(patches.Circle((rod_x, collar_y), 0.20, fc='#ffffff', ec='#1e293b', lw=1.3, zorder=9))
    ax.add_patch(patches.Circle((rod_x, collar_y), 0.09, fc='#1e293b', ec='none', zorder=10))
    
    # 7) 피벗 핀에서 뻗어나온 링크 바
    link_len = 1.5
    link_end = np.array([rod_x + link_len * np.sin(th), collar_y + link_len * np.cos(th)])
    ax.plot([rod_x, link_end[0]], [collar_y, link_end[1]], color='#334155', lw=2.2, zorder=8)
    ax.add_patch(patches.Circle(link_end, 0.08, fc='#7dd3fc', ec='#0284c7', lw=1.0, zorder=9))
    
    # 8) 외력 F 화살표
    f_arrow_len = 2.0
    f_arrow_end = link_end + f_arrow_len * np.array([np.sin(th), np.cos(th)])
    ax.annotate('', xy=f_arrow_end, xytext=link_end,
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6.0, headlength=7.0), zorder=10)
    ax.text(f_arrow_end[0] + 0.2, f_arrow_end[1] + 0.1, r'$F$',
            fontsize=12.0, fontweight='bold', color='#b91c1c', va='bottom', zorder=11)
    
    # 9) 각도 θ 호 및 지시선
    if th > 0.05:
        arc_r = 2.2
        ax.plot([rod_x, rod_x], [collar_y, collar_y + arc_r + 0.3], color='#64748b', lw=0.9, linestyle=':', zorder=5)
        arc_patch = patches.Arc((rod_x, collar_y), 2*arc_r, 2*arc_r, angle=90,
                                theta1=-th_deg, theta2=0, color='#0f172a', lw=1.2, zorder=7)
        ax.add_patch(arc_patch)
        arc_tip = np.array([rod_x + arc_r * np.sin(th), collar_y + arc_r * np.cos(th)])
        ax.annotate('', xy=arc_tip, xytext=(rod_x + (arc_r-0.01)*np.sin(th-0.05), collar_y + (arc_r-0.01)*np.cos(th-0.05)),
                    arrowprops=dict(arrowstyle='->', color='#0f172a', lw=1.2), zorder=8)
        ax.text(rod_x + (arc_r + 0.3) * np.sin(mid_th), collar_y + (arc_r + 0.3) * np.cos(mid_th),
                r'$\theta$', fontsize=10.0, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=9)
        
    # =============================================================
    # [패널 3] 우측: 교재 원본 100% 동일 자유물체도 (Free-Body Diagram)
    # =============================================================
    card3 = patches.FancyBboxPatch((18.2, 0.2), 8.6, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.5, 13.4, '[자유물체도 (Free-Body Diagram)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([18.5, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # FBD 중심 좌표
    fbd_cx, fbd_cy = 22.2, 6.6
    fbd_w, fbd_h = 2.4, 3.6
    
    # 1) 칼라 직사각형 실루엣
    ax.add_patch(patches.Rectangle((fbd_cx - fbd_w/2, fbd_cy - fbd_h/2), fbd_w, fbd_h,
                                   fc='#ffffff', ec='#1e293b', lw=1.6, zorder=6))
    
    # 2) 수직 중심선 (점선)
    ax.plot([fbd_cx, fbd_cx], [fbd_cy - fbd_h/2 - 2.8, fbd_cy + fbd_h/2 + 2.8],
            color='#64748b', lw=1.2, linestyle='--', zorder=5)
    
    # 3) 질점 작용점 (중앙 빨간 점)
    ax.scatter([fbd_cx], [fbd_cy], color='#ef4444', s=28, zorder=12)
    
    # (A) 외력 F
    f_fbd_len = 3.0
    f_fbd_end = np.array([fbd_cx + f_fbd_len * np.sin(th), fbd_cy + f_fbd_len * np.cos(th)])
    ax.annotate('', xy=f_fbd_end, xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=13)
    ax.text(f_fbd_end[0] + 0.25, f_fbd_end[1] + 0.15, r'$F$',
            fontsize=12.5, fontweight='bold', color='#b91c1c', va='bottom', zorder=14)
    
    # FBD 각도 θ 호
    if th > 0.08:
        fbd_arc_r = 1.7
        fbd_arc = patches.Arc((fbd_cx, fbd_cy), 2*fbd_arc_r, 2*fbd_arc_r, angle=90,
                              theta1=-th_deg, theta2=0, color='#0f172a', lw=1.2, zorder=10)
        ax.add_patch(fbd_arc)
        ax.text(fbd_cx + (fbd_arc_r + 0.32) * np.sin(mid_th), fbd_cy + (fbd_arc_r + 0.32) * np.cos(mid_th),
                r'$\theta$', fontsize=10.0, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=11)
        
    # (B) 마찰력 μ_k N (상단에서 중심을 향해 수직 하향)
    muN_len = 0.8 + (f_k / (mu_k * F_val)) * 1.8
    muN_start = np.array([fbd_cx, fbd_cy + muN_len])
    ax.annotate('', xy=(fbd_cx, fbd_cy), xytext=muN_start,
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=13)
    ax.text(fbd_cx - 0.35, fbd_cy + muN_len/2, r'$\mu_k N$',
            fontsize=11.0, fontweight='bold', color='#b91c1c', ha='right', va='center', zorder=14)
    
    # (C) 자중 mg (중심에서 수직 하향)
    mg_len = 2.6
    ax.annotate('', xy=(fbd_cx, fbd_cy - mg_len), xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=13)
    ax.text(fbd_cx, fbd_cy - mg_len - 0.35, r'$mg$',
            fontsize=12.0, fontweight='bold', color='#b91c1c', ha='center', va='top', zorder=14)
    
    # (D) 수직항력 N (우측에서 중심을 향해 수평 좌향)
    n_len = 0.8 + (N / F_val) * 2.6
    n_start = np.array([fbd_cx + n_len, fbd_cy])
    ax.annotate('', xy=(fbd_cx, fbd_cy), xytext=n_start,
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=13)
    ax.text(n_start[0] + 0.3, fbd_cy, r'$N$',
            fontsize=12.0, fontweight='bold', color='#b91c1c', va='center', zorder=14)
            
    # 하단 힘 크기 요약 박스
    fbd_info = (
        f"• 외력: F = {F_val:.2f} N (일정)\n"
        f"• 항력: N = F sin(kt) = {N:4.2f} N\n"
        f"• 마찰: μ_k N = {f_k:4.2f} N\n"
        f"• 중력: mg = {m*g:4.2f} N\n"
        f"• 합력: ΣFy = {m*a_y:4.2f} N"
    )
    ax.text(18.6, 2.0, fbd_info, fontsize=8.0, va='top', family='monospace', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff1f2', edgecolor='#fca5a5', lw=1.0), zorder=15)

fig.suptitle(title_text, fontsize=12.0, fontweight='bold', y=0.98, fontproperties=font_prop)
anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'ex3_5_collar_rod_force.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
