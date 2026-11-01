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
[동역학 9판 문제 3/15] 경사면 위 카트의 케이블 견인각(15°)과 장력별 가속도(F=ma) 해석
교재 원본 삽화(인부, 도르래 브래킷, 카트, 20° 경사 지형) 100% 동일 구현 + 3패널 분리형 FBD
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
m = 50.0               # 카트 질량 (kg)
th_inc_deg = 20.0      # 경사각 (deg)
th_cab_deg = 15.0      # 케이블 견인각 (deg, 경사면 기준)
th_inc = np.radians(th_inc_deg)
th_cab = np.radians(th_cab_deg)
g = 9.81               # 중력가속도 (m/s^2)

# 중력 분력
W = m * g
Wx = W * np.sin(th_inc)  # 167.76 N (경사 하향)
Wy = W * np.cos(th_inc)  # 460.92 N (경사 수직 하향)

# 케이스 (b) T = 200 N 기준 (애니메이션 구동)
T_b = 200.0
a_b = (T_b * np.cos(th_cab) - Wx) / m    # +0.5086 m/s^2 (경사 상향)
N_b = Wy - T_b * np.sin(th_cab)          # 409.14 N

# 애니메이션 설정
fps = 30
duration = 3.0
n_sim_frames = int(fps * duration)
n_pause_frames = 20
total_frames = n_sim_frames + n_pause_frames

t_eval = np.linspace(0, duration, n_sim_frames)

fig = plt.figure(figsize=(15.6, 8.4), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.01, 0.02, 0.98, 0.92])
title_text = '[동역학 9판 문제 3/15] 경사면 위 카트의 케이블 견인각(15°)과 장력별 가속도(F=ma) 해석'

def draw_worker(ax, x_base, y_base, hands_pos):
    """교재 원본 삽화와 100% 동일한 고품질 작업자 일러스트 렌더링"""
    # 1) 안전화 (갈색)
    ax.add_patch(patches.Polygon([
        [x_base + 0.85, y_base],
        [x_base + 1.45, y_base],
        [x_base + 1.40, y_base + 0.28],
        [x_base + 0.95, y_base + 0.32],
        [x_base + 0.85, y_base + 0.15]
    ], closed=True, fc='#78350f', ec='#451a03', lw=1.1, zorder=6))
    
    ax.add_patch(patches.Polygon([
        [x_base - 0.25, y_base],
        [x_base + 0.35, y_base],
        [x_base + 0.30, y_base + 0.28],
        [x_base - 0.15, y_base + 0.32],
        [x_base - 0.25, y_base + 0.15]
    ], closed=True, fc='#78350f', ec='#451a03', lw=1.1, zorder=7))
    
    # 2) 바지 다리 (하늘색/청바지)
    # 뒷다리 (오른다리 - 뒤로 곧게 뻗음)
    leg_r_pts = [
        [x_base + 0.90, y_base + 0.25],
        [x_base + 1.25, y_base + 0.25],
        [x_base + 0.85, y_base + 1.5],
        [x_base + 0.65, y_base + 2.1],
        [x_base + 0.35, y_base + 2.1],
        [x_base + 0.65, y_base + 1.4]
    ]
    ax.add_patch(patches.Polygon(leg_r_pts, closed=True, fc='#0284c7', ec='#0369a1', lw=1.2, zorder=6))
    
    # 앞다리 (왼다리 - 앞으로 굽혀서 힘차게 지탱)
    leg_l_pts = [
        [x_base - 0.20, y_base + 0.25],
        [x_base + 0.15, y_base + 0.25],
        [x_base - 0.45, y_base + 1.3],
        [x_base + 0.35, y_base + 2.2],
        [x_base + 0.10, y_base + 2.2],
        [x_base - 0.65, y_base + 1.35]
    ]
    ax.add_patch(patches.Polygon(leg_l_pts, closed=True, fc='#38bdf8', ec='#0284c7', lw=1.2, zorder=7))
    
    # 3) 상체 (살구주황/분홍빛 반팔 셔츠)
    hip_pt = [x_base + 0.35, y_base + 2.1]
    shoulder_pt = [x_base + 0.65, y_base + 3.45]
    chest_pt = [x_base + 0.15, y_base + 3.4]
    waist_pt = [x_base + 0.10, y_base + 2.2]
    
    torso_pts = [hip_pt, shoulder_pt, chest_pt, waist_pt]
    ax.add_patch(patches.Polygon(torso_pts, closed=True, fc='#fed7aa', ec='#ea580c', lw=1.3, zorder=8))
    
    # 4) 머리 & 얼굴 & 안전모
    face_pts = [
        [x_base + 0.30, y_base + 3.55],
        [x_base + 0.55, y_base + 3.55],
        [x_base + 0.60, y_base + 3.9],
        [x_base + 0.15, y_base + 3.9],
        [x_base + 0.15, y_base + 3.75],
        [x_base + 0.25, y_base + 3.7]
    ]
    ax.add_patch(patches.Polygon(face_pts, closed=True, fc='#ffedd5', ec='#ea580c', lw=0.9, zorder=9))
    
    # 노란색 안전모 (Hard hat)
    brim_pts = [
        [x_base + 0.05, y_base + 3.9],
        [x_base + 0.70, y_base + 3.9],
        [x_base + 0.68, y_base + 4.0],
        [x_base + 0.08, y_base + 4.0]
    ]
    ax.add_patch(patches.Polygon(brim_pts, closed=True, fc='#facc15', ec='#ca8a04', lw=1.1, zorder=10))
    
    cap_pts = [
        [x_base + 0.15, y_base + 4.0],
        [x_base + 0.65, y_base + 4.0],
        [x_base + 0.58, y_base + 4.35],
        [x_base + 0.25, y_base + 4.35]
    ]
    ax.add_patch(patches.Polygon(cap_pts, closed=True, fc='#facc15', ec='#ca8a04', lw=1.1, zorder=10))
    
    # 5) 양팔 및 손
    sleeve_pts = [
        [x_base + 0.40, y_base + 3.45],
        [x_base + 0.10, y_base + 3.4],
        [x_base - 0.10, y_base + 3.15],
        [x_base + 0.20, y_base + 3.15]
    ]
    ax.add_patch(patches.Polygon(sleeve_pts, closed=True, fc='#fdba74', ec='#ea580c', lw=1.1, zorder=9))
    
    arm_pts = [
        [x_base + 0.05, y_base + 3.2],
        [hands_pos[0] + 0.1, hands_pos[1] + 0.12],
        [hands_pos[0] + 0.05, hands_pos[1] - 0.12],
        [x_base - 0.05, y_base + 3.1]
    ]
    ax.add_patch(patches.Polygon(arm_pts, closed=True, fc='#ffedd5', ec='#ea580c', lw=1.1, zorder=10))
    
    # 양손
    ax.add_patch(patches.Ellipse(hands_pos, 0.32, 0.22, fc='#ffedd5', ec='#ea580c', lw=1.1, zorder=11))

def update(frame):
    if frame < n_sim_frames:
        t = t_eval[frame]
    else:
        t = duration
        
    s_disp = 0.5 * a_b * (t**2) * 1.5
    v_curr = a_b * t
    
    ax.clear()
    ax.set_xlim(-0.8, 27.2)
    ax.set_ylim(-0.6, 14.8)
    ax.axis('off')
    
    # 전체 배경
    ax.add_patch(patches.Rectangle((-0.8, -0.6), 28.0, 15.4, fc='#f8fafc', ec='none', zorder=1))
    
    # =============================================================
    # [패널 1] 좌측: 문제 요약 및 이론 수식 / 실시간 HUD 카드
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.0, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.6, 13.4, '[문제 3/15 운동역학 해석]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([-0.1, 7.3], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ 물리 매개변수 (Given)\n"
        f"  • 카트 질량: m = {m:.1f} kg\n"
        f"  • 경사면 각도: θ = {th_inc_deg:.0f}°\n"
        f"  • 케이블 견인각: α = {th_cab_deg:.0f}° (경사면 기준)\n"
        f"  • 중력가속도: g = {g:.2f} m/s²\n"
        f"  • 자중: W = mg = {W:.1f} N\n\n"
        "■ 경사 좌표계 운동방정식 (F = ma)\n"
        "  • 경사 하향 중력 분력:\n"
        "    Wx = mg sin 20° = 167.76 N\n"
        "  • 경사 수직 중력 분력:\n"
        "    Wy = mg cos 20° = 460.92 N\n"
        "  • x축 (경사 상향) 운동방정식:\n"
        "    ΣFx = T cos 15° - mg sin 20° = m ax\n"
        "  • y축 (경사 수직) 평형방정식:\n"
        "    ΣFy = N + T sin 15° - mg cos 20° = 0\n"
        "    ⇒ N = mg cos 20° - T sin 15°\n\n"
        "■ 장력 조건별 가속도 해석\n"
        "  ▶ (a) T = 150 N 일 때:\n"
        "    ΣFx = 150 cos 15° - 167.76 = -22.87 N\n"
        "    ⇒ ax = -0.457 m/s² (경사 아래로 하강)\n"
        "    ⇒ N = 422.09 N\n"
        "  ▶ (b) T = 200 N 일 때 (현재 시뮬레이션):\n"
        "    ΣFx = 200 cos 15° - 167.76 = +25.43 N\n"
        "    ⇒ ax = +0.509 m/s² (경사 위로 상승)\n"
        "    ⇒ N = 409.14 N"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=7.9, va='top', fontproperties=font_prop, linespacing=1.32, zorder=5)
    
    ax.plot([-0.1, 7.3], [2.8, 2.8], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.6, 2.5, '[실시간 상태 (Live Telemetry)]', fontsize=9.5, fontweight='bold', color='#0284c7', ha='center', fontproperties=font_prop, zorder=5)
    
    status_str = (
        f"• 경과 시간:   t = {t:4.2f} s / {duration:.2f} s\n"
        f"• 케이블 장력: T = {T_b:.0f} N (상승 모드)\n"
        f"• 가속도:     ax = {a_b:+5.3f} m/s²\n"
        f"• 현재 속도:   vx = {v_curr:+5.2f} m/s\n"
        f"• 경사 변위:   s  = {s_disp:+5.2f} m"
    )
    ax.text(0.0, 2.1, status_str, fontsize=8.2, va='top', family='monospace', fontproperties=font_prop, linespacing=1.35, zorder=5)
    
    # =============================================================
    # [패널 2] 중앙: 실제 물리 시스템 (경사로, 카트, 도르래, 작업자)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.0, 0.2), 10.4, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.2, 13.4, '[실제 물리 시스템 (Physical System)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([8.3, 18.1], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # 지형 지오메트리
    junc_x = 13.0
    junc_y = 6.4
    inc_len = 5.0
    ramp_start_x = junc_x - inc_len * np.cos(th_inc)
    ramp_start_y = junc_y - inc_len * np.sin(th_inc)
    
    # 1) 지반 다각형
    poly_pts = [
        [ramp_start_x - 0.5, ramp_start_y - 0.5 * np.tan(th_inc)],
        [junc_x, junc_y],
        [18.1, junc_y],
        [18.1, 2.0],
        [ramp_start_x - 0.5, 2.0]
    ]
    ax.add_patch(patches.Polygon(poly_pts, closed=True, fc='#f1f5f9', ec='#94a3b8', lw=1.2, zorder=3))
    
    # 경사면 및 수평면 표면 선
    ax.plot([ramp_start_x - 0.5, junc_x], [ramp_start_y - 0.5*np.tan(th_inc), junc_y], color='#334155', lw=2.4, zorder=4)
    ax.plot([junc_x, 18.1], [junc_y, junc_y], color='#334155', lw=2.4, zorder=4)
    
    # 도로 표면 빗금 (Hatching)
    for hx in np.linspace(ramp_start_x - 0.2, junc_x - 0.2, 8):
        hy = ramp_start_y + (hx - ramp_start_x) * np.tan(th_inc)
        ax.plot([hx, hx - 0.25], [hy, hy - 0.35], color='#cbd5e1', lw=1.0, zorder=3)
    for hx in np.linspace(junc_x + 0.3, 17.8, 8):
        ax.plot([hx, hx - 0.25], [junc_y, junc_y - 0.35], color='#cbd5e1', lw=1.0, zorder=3)
        
    # 경사각 20도 호 및 라벨
    ramp_base_y = ramp_start_y + 0.3
    ax.plot([ramp_start_x + 0.6, ramp_start_x + 2.6], [ramp_base_y, ramp_base_y], color='#64748b', lw=1.1, linestyle=':', zorder=4)
    ax.add_patch(patches.Arc((ramp_start_x + 0.6, ramp_base_y), 2.8, 2.8, angle=0, theta1=0, theta2=20, color='#0f172a', lw=1.2, zorder=5))
    ax.text(ramp_start_x + 2.3, ramp_base_y + 0.32, r'$20^\circ$', fontsize=9.0, fontweight='bold', color='#0f172a', zorder=6)
    
    # 2) 도르래 및 천장 브래킷 지지대
    pulley_x = 13.4
    pulley_y = junc_y + 3.4
    pulley_r = 0.60
    
    # 천장 구조물 (회색 블록)
    ax.add_patch(patches.Rectangle((pulley_x - 1.2, pulley_y + 1.2), 2.4, 0.9,
                                   fc='#e2e8f0', ec='#64748b', lw=1.4, zorder=5))
    for cx in np.linspace(pulley_x - 1.0, pulley_x + 1.0, 6):
        ax.plot([cx, cx + 0.2], [pulley_y + 2.1, pulley_y + 2.35], color='#94a3b8', lw=1.0, zorder=5)
        
    # 사다리꼴 행거 브래킷 (하늘색)
    bracket_pts = [
        [pulley_x - 0.9, pulley_y + 1.2],
        [pulley_x + 0.9, pulley_y + 1.2],
        [pulley_x + 0.5, pulley_y],
        [pulley_x - 0.5, pulley_y]
    ]
    ax.add_patch(patches.Polygon(bracket_pts, closed=True, fc='#bae6fd', ec='#0284c7', lw=1.4, zorder=6))
    
    # 풀리 휠 (도르래)
    ax.add_patch(patches.Circle((pulley_x, pulley_y), pulley_r, fc='#e0f2fe', ec='#0284c7', lw=1.6, zorder=7))
    ax.add_patch(patches.Circle((pulley_x, pulley_y), pulley_r * 0.7, fc='#bae6fd', ec='#0284c7', lw=1.0, zorder=8))
    ax.add_patch(patches.Circle((pulley_x, pulley_y), 0.14, fc='#0284c7', ec='#0369a1', lw=1.0, zorder=9))
    
    # 3) 카트 (Cart)
    u_inc = np.array([np.cos(th_inc), np.sin(th_inc)])
    n_inc = np.array([-np.sin(th_inc), np.cos(th_inc)])
    
    cart_pos_s = 1.0 + s_disp * 0.4
    cart_center = np.array([ramp_start_x, ramp_start_y]) + cart_pos_s * u_inc + 0.95 * n_inc
    
    cart_w = 2.4
    cart_h = 1.4
    wheel_r = 0.20
    wheel_base = 1.6
    
    # 바퀴 2개
    w_front = cart_center + (wheel_base/2) * u_inc - (cart_h/2 - wheel_r) * n_inc - wheel_r * n_inc
    w_rear  = cart_center - (wheel_base/2) * u_inc - (cart_h/2 - wheel_r) * n_inc - wheel_r * n_inc
    
    ax.add_patch(patches.Circle(w_front + wheel_r*n_inc, wheel_r, fc='#475569', ec='#0f172a', lw=1.2, zorder=6))
    ax.add_patch(patches.Circle(w_front + wheel_r*n_inc, 0.07, fc='#e2e8f0', ec='#0f172a', lw=0.8, zorder=7))
    ax.add_patch(patches.Circle(w_rear + wheel_r*n_inc, wheel_r, fc='#475569', ec='#0f172a', lw=1.2, zorder=6))
    ax.add_patch(patches.Circle(w_rear + wheel_r*n_inc, 0.07, fc='#e2e8f0', ec='#0f172a', lw=0.8, zorder=7))
    
    # 카트 본체
    cart_bl = cart_center - (cart_w/2) * u_inc - (cart_h/2) * n_inc + wheel_r * n_inc
    cart_box = patches.Rectangle(cart_bl, cart_w, cart_h, angle=th_inc_deg,
                                 fc='#bae6fd', ec='#0284c7', lw=1.6, zorder=7)
    ax.add_patch(cart_box)
    
    # 카트 라벨 "50 kg"
    ax.text(cart_center[0] - 0.45*np.sin(th_inc), cart_center[1] + 0.45*np.cos(th_inc) + 0.3,
            r'$50\text{ kg}$', fontsize=9.2, fontweight='bold', color='#0369a1', ha='center', va='bottom', zorder=9)
    
    # 카트 중앙 황동색 러그
    lug_pos = cart_center + wheel_r * n_inc
    ax.add_patch(patches.Circle(lug_pos, 0.26, fc='#fed7aa', ec='#c2410c', lw=1.3, zorder=8))
    ax.add_patch(patches.Circle(lug_pos, 0.10, fc='#ffffff', ec='#c2410c', lw=1.0, zorder=9))
    
    # 4) 작업자 위치 및 손 위치
    worker_x = 16.8
    worker_ground = junc_y
    hands_pos = np.array([worker_x - 1.1, pulley_y + pulley_r])
    
    # 5) 로프 (Rope) - 도르래 접선 및 원호
    rope_cart_start = lug_pos
    rope_pulley_top = np.array([pulley_x, pulley_y + pulley_r])
    
    # 카트 -> 도르래 상단 접선
    ax.plot([rope_cart_start[0], rope_pulley_top[0]], [rope_cart_start[1], rope_pulley_top[1]],
            color='#334155', lw=2.0, zorder=8)
    # 도르래 상단 -> 작업자 손 (수평선)
    ax.plot([rope_pulley_top[0], hands_pos[0]], [rope_pulley_top[1], hands_pos[1]],
            color='#334155', lw=2.0, zorder=8)
    # 늘어진 여분 로프
    tail_pts_x = [hands_pos[0], hands_pos[0] + 0.08, hands_pos[0] - 0.05, hands_pos[0] + 0.06]
    tail_pts_y = [hands_pos[1], hands_pos[1] - 0.5, hands_pos[1] - 1.1, hands_pos[1] - 1.7]
    ax.plot(tail_pts_x, tail_pts_y, color='#334155', lw=1.8, zorder=8)
    
    # 15도 각도 점선 & 각도 호
    ref_line_len = 2.2
    ref_end = rope_cart_start + ref_line_len * u_inc
    ax.plot([rope_cart_start[0], ref_end[0]], [rope_cart_start[1], ref_end[1]],
            color='#64748b', lw=1.1, linestyle='--', zorder=8)
    
    rope_angle_deg = np.degrees(np.arctan2(rope_pulley_top[1] - rope_cart_start[1], rope_pulley_top[0] - rope_cart_start[0]))
    ax.add_patch(patches.Arc(rope_cart_start, 2.4, 2.4, angle=0,
                             theta1=th_inc_deg, theta2=rope_angle_deg, color='#0f172a', lw=1.2, zorder=9))
    mid_cab_th = np.radians((th_inc_deg + rope_angle_deg) / 2.0)
    ax.text(rope_cart_start[0] + 1.5 * np.cos(mid_cab_th), rope_cart_start[1] + 1.5 * np.sin(mid_cab_th),
            r'$15^\circ$', fontsize=8.8, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=10)
    
    # 6) 작업자 드로잉 (교재 원본 100% 동일)
    draw_worker(ax, worker_x, worker_ground, hands_pos)
    
    # 당김 힘 벡터 T 화살표
    t_arrow_len = 2.2
    ax.annotate('', xy=(hands_pos[0] + t_arrow_len, hands_pos[1]), xytext=hands_pos,
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=12)
    ax.text(hands_pos[0] + t_arrow_len + 0.15, hands_pos[1], r'$T$',
            fontsize=13.0, fontweight='bold', color='#b91c1c', va='center', zorder=13)
    
    # =============================================================
    # [패널 3] 우측: 교재 원본 100% 동일 자유물체도 (Free-Body Diagram)
    # =============================================================
    card3 = patches.FancyBboxPatch((18.6, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.7, 13.4, '[카트 자유물체도 (FBD)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([18.9, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # FBD 중심 좌표
    fbd_cx = 22.5
    fbd_cy = 6.6
    
    # 1) 경사면 좌표축 (x: 경사 상향, y: 경사 수직)
    axis_len_x = 3.6
    axis_len_y = 3.6
    ax.annotate('', xy=(fbd_cx + axis_len_x * u_inc[0], fbd_cy + axis_len_x * u_inc[1]), xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.3, linestyle='--'), zorder=6)
    ax.text(fbd_cx + (axis_len_x + 0.25) * u_inc[0], fbd_cy + (axis_len_x + 0.25) * u_inc[1],
            r'$x$', fontsize=11.0, fontweight='bold', color='#64748b', va='center', zorder=7)
    
    ax.annotate('', xy=(fbd_cx + axis_len_y * n_inc[0], fbd_cy + axis_len_y * n_inc[1]), xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.3, linestyle='--'), zorder=6)
    ax.text(fbd_cx + (axis_len_y + 0.25) * n_inc[0], fbd_cy + (axis_len_y + 0.25) * n_inc[1],
            r'$y$', fontsize=11.0, fontweight='bold', color='#64748b', va='center', zorder=7)
    
    # 2) 카트 실루엣 (20도 기울어진 직사각형)
    fbd_w = 3.2
    fbd_h = 1.8
    fbd_bl = np.array([fbd_cx, fbd_cy]) - (fbd_w/2) * u_inc - (fbd_h/2) * n_inc
    ax.add_patch(patches.Rectangle(fbd_bl, fbd_w, fbd_h, angle=th_inc_deg,
                                   fc='#f8fafc', ec='#1e293b', lw=1.6, linestyle='-', zorder=7))
    
    # 3) 질점 작용점 (중앙 빨간 점)
    ax.scatter([fbd_cx], [fbd_cy], color='#ef4444', s=32, zorder=15)
    
    # (A) 로프 장력 T (경사 x축에서 +15도 상향)
    th_t_rad = th_inc + th_cab
    u_t = np.array([np.cos(th_t_rad), np.sin(th_t_rad)])
    t_fbd_len = 3.2
    t_end = np.array([fbd_cx, fbd_cy]) + t_fbd_len * u_t
    ax.annotate('', xy=t_end, xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=16)
    ax.text(t_end[0] + 0.2, t_end[1] + 0.1, r'$T$',
            fontsize=12.0, fontweight='bold', color='#b91c1c', va='bottom', zorder=17)
    
    # 15도 각도 호
    ax.add_patch(patches.Arc((fbd_cx, fbd_cy), 2.2, 2.2, angle=0,
                             theta1=th_inc_deg, theta2=th_inc_deg + th_cab_deg, color='#0f172a', lw=1.2, zorder=14))
    fbd_mid_th = np.radians(th_inc_deg + th_cab_deg/2.0)
    ax.text(fbd_cx + 1.4 * np.cos(fbd_mid_th), fbd_cy + 1.4 * np.sin(fbd_mid_th),
            r'$15^\circ$', fontsize=8.8, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=15)
    
    # (B) 수직항력 N (경사면에 수직인 +y 방향)
    n_fbd_len = 2.8
    n_end = np.array([fbd_cx, fbd_cy]) + n_fbd_len * n_inc
    ax.annotate('', xy=n_end, xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.4, headwidth=6.5, headlength=7.5), zorder=16)
    ax.text(n_end[0] - 0.2, n_end[1] + 0.2, r'$N$',
            fontsize=12.0, fontweight='bold', color='#16a34a', va='bottom', zorder=17)
    
    # (C) 자중 mg (연직 하향)
    mg_fbd_len = 3.0
    mg_end = np.array([fbd_cx, fbd_cy - mg_fbd_len])
    ax.annotate('', xy=mg_end, xytext=(fbd_cx, fbd_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=16)
    ax.text(mg_end[0], mg_end[1] - 0.35, r'$mg = 490.5\text{ N}$',
            fontsize=10.5, fontweight='bold', color='#b91c1c', ha='center', va='top', zorder=17)
    
    # 자중과 -y축 사이의 20도 각도 표기
    neg_n_inc = -n_inc
    ax.plot([fbd_cx, fbd_cx + 2.2 * neg_n_inc[0]], [fbd_cy, fbd_cy + 2.2 * neg_n_inc[1]],
            color='#94a3b8', lw=1.1, linestyle=':', zorder=10)
    ax.add_patch(patches.Arc((fbd_cx, fbd_cy), 2.4, 2.4, angle=-90,
                             theta1=0, theta2=20, color='#64748b', lw=1.1, zorder=12))
    ax.text(fbd_cx - 0.35, fbd_cy - 1.5, r'$20^\circ$', fontsize=8.5, color='#64748b', zorder=13)
    
    # (D) 가속도 ax 벡터
    ax_len = 2.2
    ax_start = np.array([fbd_cx, fbd_cy]) + 1.2 * n_inc
    ax_end = ax_start + ax_len * u_inc
    ax.annotate('', xy=ax_end, xytext=ax_start,
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=2.0, headwidth=5.5, headlength=6.5), zorder=16)
    ax.text(ax_end[0] + 0.1, ax_end[1] + 0.1, r'$a_x$',
            fontsize=11.0, fontweight='bold', color='#2563eb', va='bottom', zorder=17)
    
    # 하단 상태 박스
    fbd_box_str = (
        f"• ΣFx = T cos 15° - mg sin 20° = m ax\n"
        f"  = 193.19 - 167.76 = +25.43 N\n"
        f"  ⇒ ax = +0.509 m/s²\n"
        f"• ΣFy = N + T sin 15° - mg cos 20° = 0\n"
        f"  ⇒ N = 409.14 N"
    )
    ax.text(19.0, 2.1, fbd_box_str, fontsize=7.8, va='top', family='monospace', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff1f2', edgecolor='#fca5a5', lw=1.0), zorder=15)

fig.suptitle(title_text, fontsize=12.0, fontweight='bold', y=0.98, fontproperties=font_prop)
anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'prob3_15_cart_incline.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
