# -*- coding: utf-8 -*-
"""
[동역학 9판 문제 3/22] 30° 경사면 2체 도르래 마찰계의 정지마찰 극복 및 가속도 해석
- 블록 A (60 kg, 30° 경사면, μs=0.25, μk=0.20)
- 블록 B (20 kg, 2:1 복합 이동도르래 연결)
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

# 물리 파라미터
mA, mB = 60.0, 20.0
th_deg = 30.0
th_rad = np.radians(th_deg)
g = 9.81

WA = mA * g              # 588.6 N
WB = mB * g              # 196.2 N
NA = WA * np.cos(th_rad) # 509.74 N
mu_s, mu_k = 0.25, 0.20

fs_max = mu_s * NA      # 127.44 N
Ts_req = WB / 2.0       # 98.1 N
F_drive = WA * np.sin(th_rad) - Ts_req  # 294.3 - 98.1 = 196.2 N

# F_drive (196.2 N) > fs_max (127.44 N) => 정지마찰 극복 및 하향 미끄러짐 발생!
fk = mu_k * NA          # 101.95 N

# 운동방정식 해석:
# A: WA*sin(30) - T - fk = mA * aA
# B: 2T - WB = mB * aB = mB * (aA / 2) => T = WB/2 + (mB/4)*aA
# WA*sin(30) - fk - WB/2 = (mA + mB/4) * aA
aA_val = (WA * np.sin(th_rad) - fk - WB/2.0) / (mA + mB/4.0)   # 1.450 m/s^2 (경사 하향)
aB_val = aA_val / 2.0                                          # 0.725 m/s^2 (수직 상향)
T_val = WB/2.0 + (mB/4.0) * aA_val                             # 105.35 N

def draw_frame(t):
    sA_disp = 0.5 * aA_val * (t**2) * 0.40   # 경사면 이동 변위 (시각적 스케일)
    sB_disp = 0.5 * sA_disp                 # 블록 B 상승 변위
    vA_curr = aA_val * t
    vB_curr = aB_val * t
    
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
    # [패널 1] 좌측: 이론 요약, 정지마찰 판정 및 실시간 HUD 카드
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.7, 13.4, '[문제 3/22 운동역학 해석]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([-0.1, 7.5], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ 물리 매개변수 (Given)\n"
        f"  • 블록 A: mA = {mA:.1f} kg (30° 경사면)\n"
        f"  • 블록 B: mB = {mB:.1f} kg (가동도르래 2줄)\n"
        f"  • 마찰계수: μs = {mu_s:.2f}, μk = {mu_k:.2f}\n"
        f"  • 구속 조건: sA = 2 yB ⇒ aA = 2 aB\n\n"
        "■ 1단계: 정지마찰 한계 및 운동 개시 판정\n"
        f"  • A 중력 분력: WAx = {mA*g*0.5:.1f} N, NA = {NA:.1f} N\n"
        f"  • 최대 정지마찰력: fs,max = μs NA = {fs_max:.2f} N\n"
        f"  • 정지 시 요구 장력: Ts = mB g / 2 = {Ts_req:.1f} N\n"
        f"  • 하향 알짜 구동력: WAx - Ts = {F_drive:.1f} N\n"
        f"  ▶ {F_drive:.1f} N > fs,max ({fs_max:.2f} N) ⇒ 미끄러짐 발생!\n\n"
        "■ 2단계: 연립 운동방정식 및 해석\n"
        f"  • 운동마찰력: fk = μk NA = {fk:.2f} N\n"
        f"  • A (경사 하향): WA sin 30° - T - fk = mA aA\n"
        f"  • B (수직 상향): 2T - mB g = mB aB = (mB/2) aA\n"
        f"  ▶ 블록 A 가속도: aA = {aA_val:.3f} m/s² (하강)\n"
        f"  ▶ 블록 B 가속도: aB = aA/2 = {aB_val:.3f} m/s² (상승)\n"
        f"  ▶ 케이블 장력:   T  = {T_val:.2f} N"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=7.8, va='top', fontproperties=font_prop, linespacing=1.30, zorder=5)
    
    ax.plot([-0.1, 7.5], [2.6, 2.6], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.7, 2.3, '[실시간 상태 (Live Telemetry)]', fontsize=9.2, fontweight='bold', color='#0284c7', ha='center', fontproperties=font_prop, zorder=5)
    
    status_str = (
        f"• 경과 시간:   t  = {t:4.2f} s / 3.00 s\n"
        f"• 블록 A 변위: sA = {sA_disp:4.2f} m (속도 {vA_curr:4.2f} m/s)\n"
        f"• 블록 B 변위: yB = {sB_disp:4.2f} m (속도 {vB_curr:4.2f} m/s)\n"
        f"• 케이블 장력: T  = {T_val:4.1f} N (2T = {2*T_val:4.1f} N)"
    )
    ax.text(0.0, 1.9, status_str, fontsize=8.0, va='top', family='monospace', fontproperties=font_prop, linespacing=1.32, zorder=5)
    
    # =============================================================
    # [패널 2] 중앙: 실제 물리 시스템 (경사로, 고정도르래, 이동도르래, 블록 A, B)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.2, 0.2), 10.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.3, 13.4, '[실제 물리 시스템 (Physical System)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([8.5, 18.1], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # 지형 파라미터 (교재 원본 100% 동일 구현)
    ground_y = 1.4
    apex_x = 15.2
    apex_y = 9.2
    ramp_start_x = 8.6
    ramp_start_y = apex_y - (apex_x - ramp_start_x) * np.tan(th_rad)
    
    # 1) 경사면 몸체 및 수직 지지대 다각형 (입체적 단면 및 음영)
    poly_ramp = [
        [ramp_start_x, ground_y],
        [ramp_start_x, ramp_start_y],
        [apex_x, apex_y],
        [apex_x, ground_y]
    ]
    ax.add_patch(patches.Polygon(poly_ramp, closed=True, fc='#f1f5f9', ec='#94a3b8', lw=1.3, zorder=3))
    
    # 경사면 선 및 지면
    ax.plot([ramp_start_x - 0.2, apex_x], [ramp_start_y - 0.2*np.tan(th_rad), apex_y],
            color='#1e293b', lw=2.4, zorder=4)
    ax.plot([apex_x, apex_x], [apex_y, ground_y], color='#64748b', lw=1.8, zorder=4)
    ax.plot([ramp_start_x, ramp_start_x], [ramp_start_y, ground_y], color='#94a3b8', lw=1.4, zorder=4)
    ax.plot([ramp_start_x - 0.4, 18.0], [ground_y, ground_y], color='#334155', lw=2.0, zorder=4)
    
    # 수평 기준선 및 30도 각도 호 (경사로 시작 부분)
    ax.plot([ramp_start_x, ramp_start_x + 2.4], [ramp_start_y, ramp_start_y], color='#64748b', lw=1.1, linestyle=':', zorder=4)
    ax.add_patch(patches.Arc((ramp_start_x, ramp_start_y), 3.0, 3.0, angle=0, theta1=0, theta2=30, color='#0f172a', lw=1.3, zorder=5))
    ax.text(ramp_start_x + 2.0, ramp_start_y + 0.38, r'$30^\circ$', fontsize=10.0, fontweight='bold', color='#0f172a', zorder=6)
    
    # 2) 도르래 기하 배치 (교재 완벽 기하 정렬: r1=0.78, r2=0.39, x1=apex_x+0.55, x2=x1+r2)
    r1 = 0.78
    r2 = 0.39
    p1_center = np.array([apex_x + 0.55, apex_y + 0.35])
    
    # 꼭대기 지지 암
    ax.plot([apex_x - 0.1, p1_center[0]], [apex_y, p1_center[1]], color='#475569', lw=5.0, solid_capstyle='round', zorder=4)
    
    # 고정 도르래 1
    ax.add_patch(patches.Circle(p1_center, r1, fc='#e0f2fe', ec='#0284c7', lw=1.6, zorder=6))
    ax.add_patch(patches.Circle(p1_center, r1 * 0.70, fc='#bae6fd', ec='#0284c7', lw=1.0, zorder=7))
    ax.add_patch(patches.Circle(p1_center, 0.16, fc='#0284c7', ec='#0369a1', lw=1.2, zorder=9))
    
    # 3) 블록 A (60 kg)
    u_inc = np.array([np.cos(th_rad), np.sin(th_rad)])
    n_inc = np.array([-np.sin(th_rad), np.cos(th_rad)])
    
    init_dist_A = 2.2
    dist_A = init_dist_A + sA_disp
    boxA_w = 2.4
    boxA_h = 1.35
    center_A = np.array([apex_x, apex_y]) - dist_A * u_inc + (boxA_h/2) * n_inc
    
    bl_A = center_A - (boxA_w/2)*u_inc - (boxA_h/2)*n_inc
    ax.add_patch(patches.Rectangle(bl_A, boxA_w, boxA_h, angle=th_deg,
                                   fc='#ea997b', ec='#802611', lw=1.8, zorder=6))
    
    # 블록 A 라벨
    ax.text(center_A[0] + 0.52*n_inc[0], center_A[1] + 0.52*n_inc[1] + 0.25,
            r'$A$', fontsize=11.0, fontweight='bold', color='#802611', ha='center', va='bottom', zorder=8)
    ax.text(center_A[0], center_A[1],
            r'$60\text{ kg}$', fontsize=9.2, fontweight='bold', color='#802611', ha='center', va='center', zorder=8)
    
    # 마찰계수 화살표
    contact_pt = center_A - (boxA_h/2)*n_inc - 0.4*u_inc
    ax.annotate('', xy=contact_pt, xytext=contact_pt - 0.9*n_inc - 0.5*u_inc,
                arrowprops=dict(arrowstyle='->', color='#334155', lw=1.3), zorder=7)
    ax.text(contact_pt[0] - 1.1*n_inc[0] - 0.7*u_inc[0], contact_pt[1] - 1.1*n_inc[1] - 0.7*u_inc[1],
            r'$\mu_s, \mu_k$', fontsize=9.2, fontweight='bold', color='#0f172a', zorder=8)
    
    anchor_A = center_A + (boxA_w/2)*u_inc
    
    # 4) 이동 도르래 2 및 블록 B (20 kg)
    p2_x = p1_center[0] + r2
    init_p2_y = p1_center[1] - 3.4
    p2_y = init_p2_y + sB_disp
    p2_center = np.array([p2_x, p2_y])
    
    ax.add_patch(patches.Circle(p2_center, r2, fc='#e0f2fe', ec='#0284c7', lw=1.4, zorder=6))
    ax.add_patch(patches.Circle(p2_center, r2 * 0.65, fc='#bae6fd', ec='#0284c7', lw=0.9, zorder=7))
    ax.add_patch(patches.Circle(p2_center, 0.11, fc='#0284c7', ec='#0369a1', lw=1.0, zorder=9))
    
    blockB_w = 1.3
    blockB_h = 2.4
    blockB_center = np.array([p2_x, p2_y - r2 - 0.4 - blockB_h/2])
    
    ax.plot([p2_x, p2_x], [p2_y, blockB_center[1] + blockB_h/2],
            color='#334155', lw=2.2, zorder=5)
    ax.add_patch(patches.Rectangle((blockB_center[0] - blockB_w/2, blockB_center[1] - blockB_h/2),
                                   blockB_w, blockB_h, fc='#ea997b', ec='#802611', lw=1.8, zorder=6))
    
    ax.text(blockB_center[0] + blockB_w/2 + 0.25, blockB_center[1],
            r'$20\text{ kg}$', fontsize=9.5, fontweight='bold', color='#802611', va='center', zorder=8)
    ax.text(blockB_center[0], blockB_center[1] - blockB_h/2 - 0.25,
            r'$B$', fontsize=11.0, fontweight='bold', color='#802611', ha='center', va='top', zorder=8)
    
    # 5) 케이블 결선 (2:1 복합 도르래 100% 동일)
    rope_top1 = p1_center + r1 * n_inc
    ax.plot([anchor_A[0], rope_top1[0]], [anchor_A[1], rope_top1[1]], color='#1e293b', lw=2.0, zorder=5)
    
    rope_r_x = p1_center[0] + r1
    ax.plot([rope_r_x, rope_r_x], [p1_center[1], p2_y], color='#1e293b', lw=2.0, zorder=5)
    
    rope_l_x = p1_center[0]
    ax.plot([rope_l_x, rope_l_x], [p2_y, p1_center[1]], color='#1e293b', lw=2.0, zorder=5)
    
    ax.add_patch(patches.Arc(p1_center, 2*r1, 2*r1, angle=0, theta1=0, theta2=120, color='#1e293b', lw=2.0, zorder=8))
    ax.add_patch(patches.Arc(p2_center, 2*r2, 2*r2, angle=0, theta1=180, theta2=360, color='#1e293b', lw=2.0, zorder=8))
    
    # =============================================================
    # [패널 3] 우측: 블록 A & 블록 B 2체 독립 분리 FBD 카드
    # =============================================================
    card3 = patches.FancyBboxPatch((18.6, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.7, 13.4, '[자유물체도 (FBD: A & B)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([18.9, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # (1) 상단 FBD: 블록 A (60 kg)
    fbdA_cx = 22.4
    fbdA_cy = 9.3
    
    ax.annotate('', xy=(fbdA_cx + 2.7*u_inc[0], fbdA_cy + 2.7*u_inc[1]), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(arrowstyle='->', color='#94a3b8', lw=1.1, linestyle='--'), zorder=6)
    ax.text(fbdA_cx + 2.8*u_inc[0] + 0.1, fbdA_cy + 2.8*u_inc[1], r'$x$', fontsize=9.0, fontweight='bold', color='#64748b')
    ax.annotate('', xy=(fbdA_cx + 2.7*n_inc[0], fbdA_cy + 2.7*n_inc[1]), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(arrowstyle='->', color='#94a3b8', lw=1.1, linestyle='--'), zorder=6)
    ax.text(fbdA_cx + 2.8*n_inc[0] - 0.25, fbdA_cy + 2.8*n_inc[1], r'$y$', fontsize=9.0, fontweight='bold', color='#64748b')
    
    fbdA_w, fbdA_h = 2.4, 1.35
    fbdA_bl = np.array([fbdA_cx, fbdA_cy]) - (fbdA_w/2)*u_inc - (fbdA_h/2)*n_inc
    ax.add_patch(patches.Rectangle(fbdA_bl, fbdA_w, fbdA_h, angle=th_deg,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbdA_cx - 0.35*u_inc[0] + 0.40*n_inc[0], fbdA_cy - 0.35*u_inc[1] + 0.40*n_inc[1],
            r'$A$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbdA_cx], [fbdA_cy], color='#ef4444', s=24, zorder=9)
    
    # 힘 화살표
    ax.annotate('', xy=(fbdA_cx + 2.1*u_inc[0], fbdA_cy + 2.1*u_inc[1]), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdA_cx + 2.2*u_inc[0] + 0.1, fbdA_cy + 2.2*u_inc[1] + 0.1, r'$T = 105.4\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=11)
    
    fk_start = np.array([fbdA_cx, fbdA_cy]) - (fbdA_h/2)*n_inc
    ax.annotate('', xy=fk_start + 1.5*u_inc, xytext=fk_start,
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fk_start[0] + 1.6*u_inc[0] - 0.1, fk_start[1] + 1.6*u_inc[1] - 0.35, r'$f_k = 102.0\text{ N}$',
            fontsize=8.2, fontweight='bold', color='#7e22ce', zorder=11)
    
    ax.annotate('', xy=(fbdA_cx + 2.1*n_inc[0], fbdA_cy + 2.1*n_inc[1]), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdA_cx + 2.2*n_inc[0] - 0.1, fbdA_cy + 2.2*n_inc[1] + 0.25, r'$N_A = 509.7\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#15803d', zorder=11)
    
    ax.annotate('', xy=(fbdA_cx, fbdA_cy - 2.5), xytext=(fbdA_cx, fbdA_cy),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdA_cx + 0.2, fbdA_cy - 2.0, r'$m_A g = 588.6\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#c2410c', zorder=11)
    
    ax.annotate('', xy=(fbdA_cx - 2.1*u_inc[0], fbdA_cy - 2.1*u_inc[1]),
                xytext=(fbdA_cx - 0.3*u_inc[0], fbdA_cy - 0.3*u_inc[1]),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdA_cx - 2.2*u_inc[0] - 0.3, fbdA_cy - 2.2*u_inc[1] - 0.2,
            r'$a_A = 1.450\text{ m/s}^2$', fontsize=8.5, fontweight='bold', color='#2563eb', zorder=11)
    
    ax.plot([18.9, 26.5], [6.2, 6.2], color='#fee2e2', lw=1.0, linestyle='--', zorder=5)
    
    # (2) 하단 FBD: 블록 B + 이동도르래 (20 kg)
    fbdB_cx = 22.5
    fbdB_cy = 3.6
    
    fbdB_w, fbdB_h = 1.6, 2.2
    ax.add_patch(patches.Rectangle((fbdB_cx - fbdB_w/2, fbdB_cy - fbdB_h/2), fbdB_w, fbdB_h,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbdB_cx, fbdB_cy + 0.55, r'$B$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbdB_cx], [fbdB_cy], color='#ef4444', s=24, zorder=9)
    
    ax.annotate('', xy=(fbdB_cx, fbdB_cy + 2.5), xytext=(fbdB_cx, fbdB_cy + fbdB_h/2),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6.0, headlength=7.0), zorder=10)
    ax.text(fbdB_cx + 0.25, fbdB_cy + 2.0, r'$2T = 210.7\text{ N}$',
            fontsize=8.8, fontweight='bold', color='#b91c1c', zorder=11)
    
    ax.annotate('', xy=(fbdB_cx, fbdB_cy - 2.3), xytext=(fbdB_cx, fbdB_cy - fbdB_h/2),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbdB_cx + 0.25, fbdB_cy - 1.8, r'$m_B g = 196.2\text{ N}$',
            fontsize=8.5, fontweight='bold', color='#c2410c', zorder=11)
    
    ax.annotate('', xy=(fbdB_cx - 1.2, fbdB_cy + 1.5), xytext=(fbdB_cx - 1.2, fbdB_cy - 0.5),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=10)
    ax.text(fbdB_cx - 1.4, fbdB_cy + 0.5, r'$a_B = 0.725\text{ m/s}^2$',
            fontsize=8.5, fontweight='bold', color='#2563eb', ha='right', va='center', zorder=11)
    
    # 메인 타이틀
    fig.suptitle('[동역학 9판 문제 3/22] 30° 경사면 2체 도르래 마찰계의 정지마찰 극복 및 가속도 해석',
                 fontsize=12.0, fontweight='bold', y=0.98, fontproperties=font_prop)
    
    # 버퍼로 저장 후 PIL 이미지 반환
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def generate_gif():
    total_time = 3.0
    fps = 30
    total_frames = int(total_time * fps)
    t_vals = np.linspace(0.0, total_time, total_frames)
    
    print(f"문제 3/22 애니메이션 GIF 렌더링 시작 ({total_frames} 프레임, {fps} FPS)...")
    frames = []
    for i, t in enumerate(t_vals):
        img = draw_frame(t)
        frames.append(img)
        if (i + 1) % 15 == 0 or (i + 1) == total_frames:
            print(f"  렌더링 진행률: {i+1}/{total_frames} 프레임 완료")
            
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "prob3_22_pulley_incline.gif")
    
    # GIF 저장 (루프 및 지속 시간)
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
