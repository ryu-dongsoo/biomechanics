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
[동역학 9판 문제 3/28] 강체봉 연결 2차원 슬라이더 메커니즘의 가속도 및 봉 장력 해석
- 슬라이더 A (2 kg, 수평 홈, 외력 P = 40 N)
- 슬라이더 B (3 kg, 수직 홈)
- 강체봉 (길이 l = 0.5 m, 무시할 수 있는 질량)
- 교재 원본 삽화 100% 동일 구현 + 3단 분리형 FBD 시뮬레이션
"""
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from PIL import Image

# 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터 (순간 기준 조건)
mA = 2.0        # kg
mB = 3.0        # kg
l_rod = 0.5     # m
P_ext = 40.0    # N

# 기준 순간 값 (xA = 0.4 m)
xA_0 = 0.4      # m
yB_0 = np.sqrt(l_rod**2 - xA_0**2)  # 0.3 m
vA_0 = 0.9      # m/s (우측)
vB_0 = - (xA_0 * vA_0) / yB_0       # -1.2 m/s (하향)

# 기하 삼각비
cos_th = xA_0 / l_rod   # 0.8
sin_th = yB_0 / l_rod   # 0.6

# 가속도 구속 및 운동방정식 해석
T_val = 10.25 / 0.22            # 46.591 N (인장 상태)
aA_val = 20.0 - 0.4 * T_val     # +1.364 m/s^2 (우측 가속)
aB_val = -0.2 * T_val           # -9.318 m/s^2 (하향 가속)
NA_val = T_val * sin_th         # 27.95 N (상부 벽면 하향 수직 반력)
NB_val = T_val * cos_th         # 37.27 N (좌측 벽면 우향 수직 반력)

def draw_frame(t_offset):
    # 시간 t_offset (기준 순간 t=0 전후 [-0.07 s, +0.07 s])
    xA_curr = np.clip(xA_0 + vA_0 * t_offset + 0.5 * aA_val * (t_offset**2), 0.24, 0.48)
    yB_curr = np.sqrt(l_rod**2 - xA_curr**2)
    vA_curr = vA_0 + aA_val * t_offset
    vB_curr = -(xA_curr * vA_curr) / yB_curr
    
    fig = plt.figure(figsize=(15.6, 8.4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_position([0.01, 0.02, 0.98, 0.92])
    
    ax.clear()
    ax.set_xlim(-0.8, 27.2)
    ax.set_ylim(-0.6, 14.8)
    ax.axis('off')
    
    # 전체 배경
    ax.add_patch(patches.Rectangle((-0.8, -0.6), 28.0, 15.4, fc='#f8fafc', ec='none', zorder=1))
    
    # =============================================================
    # [패널 1] 좌측: 이론 요약, 구속식 및 연립방정식 해석 카드
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.7, 13.4, '[문제 3/28 운동역학 해석]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([-0.1, 7.5], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ 물리 매개변수 (Given)\n"
        f"  • 슬라이더 A: mA = {mA:.1f} kg (수평 홈)\n"
        f"  • 슬라이더 B: mB = {mB:.1f} kg (수직 홈)\n"
        f"  • 강체봉 길이: l = {l_rod:.2f} m (무시할 질량)\n"
        f"  • 작용 외력:   P = {P_ext:.1f} N (A에 우측 작용)\n"
        f"  • 순간 조건:   xA = {xA_0:.2f} m, vA = {vA_0:.2f} m/s (→)\n\n"
        "■ 1단계: 위치·속도·가속도 구속조건 (Kinematics)\n"
        f"  • 위치 구속: xA² + yB² = l²\n"
        f"    ⇒ yB = √(0.5² - 0.4²) = {yB_0:.2f} m (cosθ=0.8, sinθ=0.6)\n"
        f"  • 속도 구속: xA vA + yB vB = 0\n"
        f"    ⇒ 0.4(0.9) + 0.3 vB = 0 ⇒ vB = {vB_0:.2f} m/s (↓)\n"
        f"  • 가속도 구속: xA aA + yB aB = -(vA² + vB²)\n"
        f"    ⇒ 0.4 aA + 0.3 aB = -(0.81 + 1.44) = -2.25\n"
        f"    ⇒ 4 aA + 3 aB = -22.5  --- [식 1]\n\n"
        "■ 2단계: 운동방정식 및 연립해 (Kinetics)\n"
        f"  • A: P - T cos θ = mA aA ⇒ aA = 20 - 0.4 T --- [식 2]\n"
        f"  • B: -T sin θ = mB aB    ⇒ aB = -0.2 T    --- [식 3]\n"
        f"  • 대입 연립해 (봉 장력 및 각 가속도):\n"
        f"  ▶ 봉 작용 장력:   T  = {T_val:.2f} N (인장 상태)\n"
        f"  ▶ 슬라이더 A 가속도: aA = {aA_val:+.3f} m/s² (우측)\n"
        f"  ▶ 슬라이더 B 가속도: aB = {aB_val:.3f} m/s² (하향)"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=7.7, va='top', fontproperties=font_prop, linespacing=1.28, zorder=5)
    
    ax.plot([-0.1, 7.5], [2.6, 2.6], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.7, 2.3, '[실시간 상태 (Live Telemetry)]', fontsize=9.2, fontweight='bold', color='#0284c7', ha='center', fontproperties=font_prop, zorder=5)
    
    status_str = (
        f"• 시간 오프셋: Δt = {t_offset:+5.3f} s (순간 t=0)\n"
        f"• A 위치/속도: xA = {xA_curr:5.3f} m (vA = {vA_curr:+4.2f} m/s)\n"
        f"• B 위치/속도: yB = {yB_curr:5.3f} m (vB = {vB_curr:+4.2f} m/s)\n"
        f"• 봉 장력/가속: T = {T_val:4.1f} N, aA = {aA_val:+.2f} m/s²"
    )
    ax.text(0.0, 1.9, status_str, fontsize=8.0, va='top', family='monospace', fontproperties=font_prop, linespacing=1.32, zorder=5)
    
    # =============================================================
    # [패널 2] 중앙: 실제 물리 시스템 (교재 원본 100% 동일 L자형 홈 & 슬라이더)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.2, 0.2), 10.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.3, 13.4, '[실제 물리 시스템 (Physical System)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([8.5, 18.1], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # 물리 시스템 스케일 및 원점
    ox, oy = 9.4, 3.2
    scale = 14.0  # 1 m = 14.0 단위
    gw = 1.40     # 가이드 홈 폭
    
    # 1) L자 가이드 채널 벽면 렌더링
    outer_wall = [
        [ox - gw/2 - 0.7, oy - gw/2 - 0.7],
        [ox + 7.4, oy - gw/2 - 0.7],
        [ox + 7.4, oy - gw/2],
        [ox - gw/2, oy - gw/2],
        [ox - gw/2, oy + 8.8],
        [ox - gw/2 - 0.7, oy + 8.8]
    ]
    ax.add_patch(patches.Polygon(outer_wall, closed=True, fc='#e2e8f0', ec='#64748b', lw=1.4, zorder=3))
    
    inner_wall = [
        [ox + gw/2, oy + gw/2],
        [ox + 7.4, oy + gw/2],
        [ox + 7.4, oy + gw/2 + 0.7],
        [ox + gw/2 + 0.7, oy + gw/2 + 0.7],
        [ox + gw/2 + 0.7, oy + 8.8],
        [ox + gw/2, oy + 8.8]
    ]
    ax.add_patch(patches.Polygon(inner_wall, closed=True, fc='#e2e8f0', ec='#64748b', lw=1.4, zorder=3))
    
    poly_slot = [
        [ox - gw/2, oy - gw/2],
        [ox + 7.4, oy - gw/2],
        [ox + 7.4, oy + gw/2],
        [ox + gw/2, oy + gw/2],
        [ox + gw/2, oy + 8.8],
        [ox - gw/2, oy + 8.8]
    ]
    ax.add_patch(patches.Polygon(poly_slot, closed=True, fc='#f8fafc', ec='none', zorder=2))
    
    ax.plot([ox - gw/2, ox - gw/2], [oy - gw/2, oy + 8.8], color='#334155', lw=2.0, zorder=4)
    ax.plot([ox - gw/2, ox + 7.4], [oy - gw/2, oy - gw/2], color='#334155', lw=2.0, zorder=4)
    ax.plot([ox + gw/2, ox + gw/2], [oy + gw/2, oy + 8.8], color='#334155', lw=2.0, zorder=4)
    ax.plot([ox + gw/2, ox + 7.4], [oy + gw/2, oy + gw/2], color='#334155', lw=2.0, zorder=4)
    
    # 2) 슬라이더 A, B 위치 좌표
    pos_Ax = ox + xA_curr * scale
    pos_Ay = oy
    pos_Bx = ox
    pos_By = oy + yB_curr * scale
    
    # 3) 슬라이더 본체 (Rectangle)
    b_w, b_h = 1.05, 1.55
    ax.add_patch(patches.Rectangle((pos_Bx - b_w/2, pos_By - b_h/2), b_w, b_h,
                                   fc='#ea997b', ec='#802611', lw=1.6, zorder=6))
    
    rw, rh = 0.16, 0.28
    for rx_sign in [-1, 1]:
        for ry_offset in [-0.45, 0.45]:
            rcx = pos_Bx + rx_sign * (b_w/2)
            rcy = pos_By + ry_offset
            ax.add_patch(patches.Rectangle((rcx - rw/2, rcy - rh/2), rw, rh,
                                           fc='#ffffff', ec='#802611', lw=1.1, zorder=7))
    
    a_w, a_h = 1.55, 1.05
    ax.add_patch(patches.Rectangle((pos_Ax - a_w/2, pos_Ay - a_h/2), a_w, a_h,
                                   fc='#ea997b', ec='#802611', lw=1.6, zorder=6))
    
    for ry_sign in [-1, 1]:
        for rx_offset in [-0.45, 0.45]:
            rcx = pos_Ax + rx_offset
            rcy = pos_Ay + ry_sign * (a_h/2)
            ax.add_patch(patches.Rectangle((rcx - rh/2, rcy - rw/2), rh, rw,
                                           fc='#ffffff', ec='#802611', lw=1.1, zorder=7))
    
    # 4) 강체봉 (Rigid Rod, 0.5 m) - 슬라이더 본체 위에 얹어 핀에 완벽 도킹
    ax.plot([pos_Bx, pos_Ax], [pos_By, pos_Ay], color='#7dd3fc', lw=5.5, solid_capstyle='round', zorder=8)
    ax.plot([pos_Bx, pos_Ax], [pos_By, pos_Ay], color='#0284c7', lw=2.0, solid_capstyle='round', zorder=9)
    
    rod_cx = (pos_Ax + pos_Bx) / 2.0
    rod_cy = (pos_Ay + pos_By) / 2.0
    ax.text(rod_cx + 0.15, rod_cy + 0.45, r'$0.5\text{ m}$', fontsize=9.5, fontweight='bold', color='#0369a1', ha='center', va='bottom', zorder=10)
    
    # 5) 중심 핀 & 링 (최상단 zorder)
    ax.add_patch(patches.Circle((pos_Bx, pos_By), 0.28, fc='#e0f2fe', ec='#0284c7', lw=1.4, zorder=11))
    ax.add_patch(patches.Circle((pos_Bx, pos_By), 0.08, fc='#0f172a', ec='none', zorder=12))
    
    ax.add_patch(patches.Circle((pos_Ax, pos_Ay), 0.28, fc='#e0f2fe', ec='#0284c7', lw=1.4, zorder=11))
    ax.add_patch(patches.Circle((pos_Ax, pos_Ay), 0.08, fc='#0f172a', ec='none', zorder=12))
    
    # 6) 텍스트 라벨
    ax.text(pos_Bx + b_w/2 + 0.35, pos_By, r'$3\text{ kg}$', fontsize=9.2, fontweight='bold', color='#802611', va='center', zorder=13)
    ax.text(pos_Bx, pos_By - b_h/2 - 0.28, r'$B$', fontsize=11.0, fontweight='bold', color='#802611', ha='center', va='top', zorder=13)
    
    ax.text(pos_Ax, pos_Ay + a_h/2 + 0.25, r'$2\text{ kg}$', fontsize=9.2, fontweight='bold', color='#802611', ha='center', va='bottom', zorder=13)
    ax.text(pos_Ax - a_w/2 - 0.25, pos_Ay - a_h/2 - 0.22, r'$A$', fontsize=11.0, fontweight='bold', color='#802611', ha='right', va='top', zorder=13)
    
    # 7) 외력 P = 40 N
    p_len = 2.0
    ax.annotate('', xy=(pos_Ax + a_w/2 + p_len, pos_Ay), xytext=(pos_Ax + a_w/2, pos_Ay),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6.0, headlength=7.0), zorder=14)
    ax.text(pos_Ax + a_w/2 + p_len + 0.15, pos_Ay, r'$P = 40\text{ N}$',
            fontsize=9.5, fontweight='bold', color='#b91c1c', va='center', zorder=15)
    
    # 8) 치수선 x_A
    dim_y = oy - gw/2 - 1.4
    ax.plot([ox, ox], [oy - gw/2 - 0.2, dim_y - 0.4], color='#64748b', lw=1.1, linestyle='-', zorder=4)
    ax.plot([pos_Ax, pos_Ax], [pos_Ay - a_h/2 - 0.2, dim_y - 0.4], color='#64748b', lw=1.1, linestyle='-', zorder=4)
    ax.annotate('', xy=(pos_Ax, dim_y), xytext=(ox, dim_y),
                arrowprops=dict(arrowstyle='<->', color='#0f172a', lw=1.3), zorder=5)
    ax.text((ox + pos_Ax)/2.0, dim_y - 0.1, r'$x_A$', fontsize=10.0, fontweight='bold', color='#0f172a', ha='center', va='top', zorder=6)
    
    # =============================================================
    # [패널 3] 우측: 슬라이더 A & 슬라이더 B 2체 독립 분리 FBD 카드
    # =============================================================
    card3 = patches.FancyBboxPatch((18.6, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.7, 13.4, '[자유물체도 (FBD: A & B)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([18.9, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # (1) 상단 FBD: 슬라이더 B (3 kg, 수직 홈)
    fbdB_cx = 22.5
    fbdB_cy = 9.5
    
    fbdB_w, fbdB_h = 1.3, 1.9
    ax.add_patch(patches.Rectangle((fbdB_cx - fbdB_w/2, fbdB_cy - fbdB_h/2), fbdB_w, fbdB_h,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbdB_cx - 0.40, fbdB_cy + 0.45, r'$B$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbdB_cx], [fbdB_cy], color='#ef4444', s=24, zorder=9)
    
    # 힘 1: 봉 작용력 T (우하향)
    rod_vec = np.array([cos_th, -sin_th])
    ax.annotate('', xy=(fbdB_cx + 2.2*rod_vec[0], fbdB_cy + 2.2*rod_vec[1]), xytext=(fbdB_cx, fbdB_cy),
                arrowprops=dict(facecolor='#0284c7', edgecolor='#0369a1', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdB_cx + 2.3*rod_vec[0] + 0.1, fbdB_cy + 2.3*rod_vec[1] - 0.1, r'$T = 46.6\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#0284c7', zorder=11)
    
    # 힘 2: 벽면 수직항력 NB (우측)
    ax.annotate('', xy=(fbdB_cx - 0.1, fbdB_cy), xytext=(fbdB_cx - 2.1, fbdB_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdB_cx - 2.2, fbdB_cy + 0.25, r'$N_B = 37.3\text{ N}$',
            fontsize=8.2, fontweight='bold', color='#15803d', ha='right', zorder=11)
    
    # 가속도 aB 벡터 (수직 하향)
    ax.annotate('', xy=(fbdB_cx + 1.6, fbdB_cy - 1.8), xytext=(fbdB_cx + 1.6, fbdB_cy + 0.2),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdB_cx + 1.8, fbdB_cy - 0.8, r'$a_B = 9.318\text{ m/s}^2$ (↓)',
            fontsize=8.5, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    ax.plot([18.9, 26.5], [6.5, 6.5], color='#fee2e2', lw=1.0, linestyle='--', zorder=5)
    
    # (2) 하단 FBD: 슬라이더 A (2 kg, 수평 홈)
    fbdA_cx = 22.5
    fbdA_cy = 3.6
    
    fbdA_w, fbdA_h = 1.9, 1.3
    ax.add_patch(patches.Rectangle((fbdA_cx - fbdA_w/2, fbdA_cy - fbdA_h/2), fbdA_w, fbdA_h,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbdA_cx - 0.45, fbdA_cy - 0.35, r'$A$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbdA_cx], [fbdA_cy], color='#ef4444', s=24, zorder=9)
    
    # 힘 1: 외력 P = 40 N (우측)
    ax.annotate('', xy=(fbdA_cx + 2.3, fbdA_cy), xytext=(fbdA_cx + fbdA_w/2, fbdA_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdA_cx + 2.4, fbdA_cy + 0.1, r'$P = 40\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=11)
    
    # 힘 2: 봉 작용력 T (좌상향)
    rod_vec_A = np.array([-cos_th, sin_th])
    ax.annotate('', xy=(fbdA_cx + 2.2*rod_vec_A[0], fbdA_cy + 2.2*rod_vec_A[1]), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(facecolor='#0284c7', edgecolor='#0369a1', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdA_cx + 2.3*rod_vec_A[0] - 0.2, fbdA_cy + 2.3*rod_vec_A[1] + 0.1, r'$T = 46.6\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#0284c7', ha='right', zorder=11)
    
    # 힘 3: 상부 벽면 수직항력 NA (하향)
    ax.annotate('', xy=(fbdA_cx, fbdA_cy - 2.0), xytext=(fbdA_cx, fbdA_cy - fbdA_h/2),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdA_cx + 0.2, fbdA_cy - 1.6, r'$N_A = 28.0\text{ N}$',
            fontsize=8.2, fontweight='bold', color='#15803d', zorder=11)
    
    # 가속도 aA 벡터 (우측)
    ax.annotate('', xy=(fbdA_cx + 1.8, fbdA_cy + 1.4), xytext=(fbdA_cx - 0.2, fbdA_cy + 1.4),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdA_cx + 2.0, fbdA_cy + 1.4, r'$a_A = +1.364\text{ m/s}^2$ (→)',
            fontsize=8.5, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    # 메인 타이틀
    fig.suptitle('[동역학 9판 문제 3/28] 강체봉 연결 2차원 슬라이더 메커니즘의 가속도 및 봉 장력 해석',
                 fontsize=12.0, fontweight='bold', y=0.98, fontproperties=font_prop)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def generate_gif():
    total_time = 0.14
    fps = 30
    total_frames = int(3.0 * fps)  # 90 프레임
    t_vals = np.linspace(-0.07, 0.07, total_frames)
    
    print(f"문제 3/28 애니메이션 GIF 렌더링 시작 ({total_frames} 프레임, {fps} FPS)...")
    frames = []
    for i, t in enumerate(t_vals):
        img = draw_frame(t)
        frames.append(img)
        if (i + 1) % 15 == 0 or (i + 1) == total_frames:
            print(f"  렌더링 진행률: {i+1}/{total_frames} 프레임 완료")
            
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "prob3_28_rigid_rod_sliders.gif")
    
    duration_ms = int(1000 / fps)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True
    )
    print(f"성공적으로 GIF 생성 완료: {gif_path}")

if __name__ == '__main__':
    generate_gif()
