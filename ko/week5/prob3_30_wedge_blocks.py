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
[동역학 9판 문제 3/30] 20° 쐐기 위 블록의 미끄럼 방지 한계 작용력(P) 범위 해석
- 쐐기 카트 m1 (20° 빗면, 바퀴 마찰 무시)
- 블록 m2 (μs = 0.30, μk = 0.25)
- 교재 원본 삽화 100% 동일 구현 + 3단 분리형 FBD (Case 1: P_min, Case 2: P_max)
"""
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from PIL import Image

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------------------------------------
# 1. 물리 파라미터 및 엄밀한 수치해석
# -------------------------------------------------------------
th_deg = 20.0
th_rad = np.radians(th_deg)
mu_s = 0.30
mu_k = 0.25
g = 9.81

sin_th = np.sin(th_rad)  # 0.34202
cos_th = np.cos(th_rad)  # 0.93969

# (1) 하향 미끄럼 임계 가속도 (a_min, fs = +mu_s N 경사 상향 작용)
a_min = g * (sin_th - mu_s * cos_th) / (cos_th + mu_s * sin_th)   # 0.5657 m/s^2

# (2) 상향 미끄럼 임계 가속도 (a_max, fs = -mu_s N 경사 하향 작용)
a_max = g * (sin_th + mu_s * cos_th) / (cos_th - mu_s * sin_th)   # 7.3118 m/s^2

# 공칭 주행 가속도 (안전 범위 중간값 a_nom = 3.5 m/s^2)
a_nom = 3.5

# -------------------------------------------------------------
# 2. 단일 프레임 렌더링 함수
# -------------------------------------------------------------
def render_frame(t, total_time=3.0):
    # 시간 t에 따른 수평 주행 변위
    x_disp = 0.5 * a_nom * (t**2) * 0.12  # 시각적 스케일 계수
    v_curr = a_nom * t
    
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
    # [패널 1] 좌측: 이론 요약, 미끄럼 한계 유도식 및 실시간 HUD 카드
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.7, 13.4, '[문제 3/30 운동역학 해석]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([-0.1, 7.5], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ 물리 매개변수 (Given)\n"
        f"  • 쐐기 카트 질량: m1 (20° 빗면, 바퀴 마찰 무시)\n"
        f"  • 상단 블록 질량: m2 (경사면 거치)\n"
        f"  • 마찰계수: μs = {mu_s:.2f}, μk = {mu_k:.2f}\n"
        f"  • 전체 계 수평 가속도: a = P / (m1 + m2)\n\n"
        "■ 1단계: 하향 미끄럼 방지 최소 작용력 (P_min)\n"
        "  • 마찰력 fs = μs N 이 경사 상향(좌상향)으로 최대로 작용\n"
        "  • ΣFx = N sin 20° - μs N cos 20° = m2 a_min\n"
        "  • ΣFy = N cos 20° + μs N sin 20° - m2 g = 0\n"
        f"  ▶ a_min = g(sin 20° - μs cos 20°)/(cos 20° + μs sin 20°)\n"
        f"          = {a_min:.3f} m/s² [0.0577 g]\n"
        f"  ▶ P_min = {a_min:.3f} (m1 + m2) N\n\n"
        "■ 2단계: 상향 미끄럼 방지 최대 작용력 (P_max)\n"
        "  • 마찰력 fs = μs N 이 경사 하향(우하향)으로 최대로 작용\n"
        "  • ΣFx = N sin 20° + μs N cos 20° = m2 a_max\n"
        "  • ΣFy = N cos 20° - μs N sin 20° - m2 g = 0\n"
        f"  ▶ a_max = g(sin 20° + μs cos 20°)/(cos 20° - μs sin 20°)\n"
        f"          = {a_max:.3f} m/s² [0.745 g]\n"
        f"  ▶ P_max = {a_max:.3f} (m1 + m2) N\n\n"
        "■ 최종 안전 비미끄럼 작용력 허용 범위:\n"
        f"  ▶ {a_min:.3f}(m1+m2) ≤ P ≤ {a_max:.3f}(m1+m2) N"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=7.6, va='top', fontproperties=font_prop, linespacing=1.26, zorder=5)
    
    ax.plot([-0.1, 7.5], [2.6, 2.6], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.7, 2.3, '[실시간 상태 (Live Telemetry)]', fontsize=9.2, fontweight='bold', color='#0284c7', ha='center', fontproperties=font_prop, zorder=5)
    
    status_str = (
        f"• 경과 시간:     t = {t:4.2f} s / {total_time:.2f} s\n"
        f"• 현재 가속도:   a = {a_nom:4.2f} m/s² (안전 대역 주행)\n"
        f"• 수평 이동변위: x = {x_disp:4.2f} m (속도 {v_curr:4.2f} m/s)\n"
        f"• 비미끄럼 상태: Safe (a_min ≤ {a_nom:.1f} ≤ a_max)"
    )
    ax.text(0.0, 1.9, status_str, fontsize=8.0, va='top', family='monospace', fontproperties=font_prop, linespacing=1.32, zorder=5)
    
    # =============================================================
    # [패널 2] 중앙: 실제 물리 시스템 (교재 원본 100% 동일 쐐기 카트 & 블록)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.2, 0.2), 10.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.3, 13.4, '[실제 물리 시스템 (Physical System)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([8.5, 18.1], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # 바닥면 및 지면 렌더링
    ground_y = 3.6
    ax.plot([8.5, 18.1], [ground_y, ground_y], color='#334155', lw=2.2, zorder=3)
    for hx in np.linspace(8.6, 18.0, 24):
        ax.plot([hx, hx - 0.25], [ground_y, ground_y - 0.35], color='#94a3b8', lw=1.1, zorder=2)
    
    # 쐐기 카트 기하 파라미터 (교재 원본 동일 비례)
    w_len = 6.4
    w_h = w_len * np.tan(th_rad)
    
    wheel_r = 0.26
    wheel_y = ground_y + wheel_r
    wedge_base_y = ground_y + 2 * wheel_r
    
    # 쐐기 좌측 하단 x 위치
    init_wx = 9.4
    wx = init_wx + x_disp
    
    # 1) 쐐기 다각형 (m1, 하늘색)
    poly_wedge = [
        [wx, wedge_base_y],
        [wx + w_len, wedge_base_y],
        [wx, wedge_base_y + w_h]
    ]
    ax.add_patch(patches.Polygon(poly_wedge, closed=True, fc='#c7e9fb', ec='#0284c7', lw=1.8, zorder=4))
    
    # 쐐기 라벨 "m1"
    ax.text(wx + 1.2, wedge_base_y + 0.48*w_h, r'$m_1$', fontsize=11.5, fontweight='bold', color='#0369a1', ha='center', va='center', zorder=7)
    
    # 2) 쐐기 바퀴 2개
    wh1_x = wx + 1.4
    wh2_x = wx + w_len - 1.5
    ax.add_patch(patches.Circle((wh1_x, wheel_y), wheel_r, fc='#e2e8f0', ec='#334155', lw=1.3, zorder=5))
    ax.add_patch(patches.Circle((wh1_x, wheel_y), 0.07, fc='#0f172a', ec='none', zorder=6))
    ax.add_patch(patches.Circle((wh2_x, wheel_y), wheel_r, fc='#e2e8f0', ec='#334155', lw=1.3, zorder=5))
    ax.add_patch(patches.Circle((wh2_x, wheel_y), 0.07, fc='#0f172a', ec='none', zorder=6))
    
    # 3) 20도 각도 호 및 라벨
    arc_cx = wx + w_len
    arc_cy = wedge_base_y
    ax.plot([arc_cx - 2.2, arc_cx], [arc_cy, arc_cy], color='#334155', lw=1.0, linestyle=':', zorder=6)
    ax.add_patch(patches.Arc((arc_cx, arc_cy), 3.2, 3.2, angle=180, theta1=0, theta2=20, color='#0f172a', lw=1.3, zorder=7))
    ax.text(arc_cx - 1.8, arc_cy + 0.35, r'$20^\circ$', fontsize=9.5, fontweight='bold', color='#0f172a', zorder=8)
    
    # 4) 블록 m2 (직사각형, 살구색)
    u_down = np.array([cos_th, -sin_th])
    n_out = np.array([sin_th, cos_th])
    
    dist_along_wedge = 2.8
    b_center_on_incline = np.array([wx, wedge_base_y + w_h]) + dist_along_wedge * u_down
    
    box2_w = 2.4
    box2_h = 1.35
    b_center = b_center_on_incline + (box2_h/2) * n_out
    
    bl2 = b_center - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(bl2, box2_w, box2_h, angle=-th_deg,
                                   fc='#ea997b', ec='#802611', lw=1.8, zorder=6))
    
    ax.text(b_center[0], b_center[1], r'$m_2$', fontsize=11.5, fontweight='bold', color='#802611', ha='center', va='center', zorder=8)
    
    # 5) 외력 P (쐐기 좌측 수직면에 작용하는 빨간색 화살표)
    p_len = 1.8
    p_start_x = wx - p_len - 0.2
    p_y = wedge_base_y + 0.50 * w_h
    ax.annotate('', xy=(wx, p_y), xytext=(p_start_x, p_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=8)
    ax.text(p_start_x - 0.2, p_y, r'$P$', fontsize=11.5, fontweight='bold', color='#ef4444', ha='right', va='center', zorder=9)
    
    # 6) 마찰계수 지시선 및 수치
    contact_pt = b_center_on_incline + (box2_w/2)*u_down
    label_pt = contact_pt + np.array([0.9, 0.4])
    ax.annotate('', xy=contact_pt, xytext=label_pt,
                arrowprops=dict(arrowstyle='->', color='#334155', lw=1.2, connectionstyle="arc3,rad=-0.15"), zorder=9)
    
    ax.text(label_pt[0] + 0.1, label_pt[1] + 0.22, r'$\mu_s = 0.30$', fontsize=9.2, fontweight='bold', color='#0f172a', va='center', zorder=10)
    ax.text(label_pt[0] + 0.1, label_pt[1] - 0.22, r'$\mu_k = 0.25$', fontsize=9.2, fontweight='bold', color='#0f172a', va='center', zorder=10)
    
    # =============================================================
    # [패널 3] 우측: 블록 m2 2가지 한계 상태 FBD 분리 카드
    # =============================================================
    card3 = patches.FancyBboxPatch((18.6, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.7, 13.4, '[자유물체도 (FBD: 2가지 한계상태)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=5)
    ax.plot([18.9, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # -------------------------------------------------------------
    # (1) 상단 FBD: Case 1: P_min 임계 상태 (하향 미끄럼 방지)
    # -------------------------------------------------------------
    fbd1_cx = 22.4
    fbd1_cy = 9.8
    
    ax.text(19.2, 12.5, '▶ Case 1: P_min (하향 미끄럼 임계, fs = μs N 경사 상향)',
            fontsize=7.6, fontweight='bold', color='#991b1b', fontproperties=font_prop, zorder=6)
    
    fbd1_bl = np.array([fbd1_cx, fbd1_cy]) - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(fbd1_bl, box2_w, box2_h, angle=-th_deg,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbd1_cx - 0.35*u_down[0] + 0.35*n_out[0], fbd1_cy - 0.35*u_down[1] + 0.35*n_out[1],
            r'$m_2$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbd1_cx], [fbd1_cy], color='#ef4444', s=24, zorder=9)
    
    # N
    ax.annotate('', xy=(fbd1_cx + 2.2*n_out[0], fbd1_cy + 2.2*n_out[1]), xytext=(fbd1_cx, fbd1_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd1_cx + 2.3*n_out[0] + 0.1, fbd1_cy + 2.3*n_out[1] + 0.1, r'$N$',
            fontsize=9.0, fontweight='bold', color='#15803d', zorder=11)
    
    # fs (경사 상향)
    fs1_start = np.array([fbd1_cx, fbd1_cy]) - (box2_h/2)*n_out
    ax.annotate('', xy=fs1_start - 1.8*u_down, xytext=fs1_start,
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fs1_start[0] - 1.9*u_down[0] - 0.1, fs1_start[1] - 1.9*u_down[1] + 0.25, r'$f_s = \mu_s N$',
            fontsize=8.5, fontweight='bold', color='#7e22ce', ha='right', zorder=11)
    
    # m2 g
    ax.annotate('', xy=(fbd1_cx, fbd1_cy - 2.2), xytext=(fbd1_cx, fbd1_cy),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd1_cx + 0.2, fbd1_cy - 1.8, r'$m_2 g$',
            fontsize=9.0, fontweight='bold', color='#c2410c', zorder=11)
    
    # a_min
    ax.annotate('', xy=(fbd1_cx + 2.2, fbd1_cy - 1.2), xytext=(fbd1_cx + 0.2, fbd1_cy - 1.2),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.6, headwidth=4.5, headlength=5.5), zorder=10)
    ax.text(fbd1_cx + 2.3, fbd1_cy - 1.2, r'$a_{\min} = 0.566\text{ m/s}^2$',
            fontsize=8.0, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    # 구분선
    ax.plot([18.9, 26.5], [6.6, 6.6], color='#fee2e2', lw=1.0, linestyle='--', zorder=5)
    
    # -------------------------------------------------------------
    # (2) 하단 FBD: Case 2: P_max 임계 상태 (상향 미끄럼 방지)
    # -------------------------------------------------------------
    fbd2_cx = 22.4
    fbd2_cy = 3.8
    
    ax.text(19.2, 6.2, '▶ Case 2: P_max (상향 미끄럼 임계, fs = μs N 경사 하향)',
            fontsize=7.6, fontweight='bold', color='#991b1b', fontproperties=font_prop, zorder=6)
    
    fbd2_bl = np.array([fbd2_cx, fbd2_cy]) - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(fbd2_bl, box2_w, box2_h, angle=-th_deg,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbd2_cx - 0.35*u_down[0] + 0.35*n_out[0], fbd2_cy - 0.35*u_down[1] + 0.35*n_out[1],
            r'$m_2$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbd2_cx], [fbd2_cy], color='#ef4444', s=24, zorder=9)
    
    # N
    ax.annotate('', xy=(fbd2_cx + 2.2*n_out[0], fbd2_cy + 2.2*n_out[1]), xytext=(fbd2_cx, fbd2_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd2_cx + 2.3*n_out[0] + 0.1, fbd2_cy + 2.3*n_out[1] + 0.1, r'$N$',
            fontsize=9.0, fontweight='bold', color='#15803d', zorder=11)
    
    # fs (경사 하향)
    fs2_start = np.array([fbd2_cx, fbd2_cy]) - (box2_h/2)*n_out
    ax.annotate('', xy=fs2_start + 1.8*u_down, xytext=fs2_start,
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fs2_start[0] + 1.9*u_down[0] + 0.1, fs2_start[1] + 1.9*u_down[1] - 0.25, r'$f_s = \mu_s N$',
            fontsize=8.5, fontweight='bold', color='#7e22ce', ha='left', zorder=11)
    
    # m2 g
    ax.annotate('', xy=(fbd2_cx, fbd2_cy - 2.2), xytext=(fbd2_cx, fbd2_cy),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd2_cx - 0.2, fbd2_cy - 1.8, r'$m_2 g$',
            fontsize=9.0, fontweight='bold', color='#c2410c', ha='right', zorder=11)
    
    # a_max
    ax.annotate('', xy=(fbd2_cx + 2.2, fbd2_cy - 1.2), xytext=(fbd2_cx + 0.2, fbd2_cy - 1.2),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.6, headwidth=4.5, headlength=5.5), zorder=10)
    ax.text(fbd2_cx + 2.3, fbd2_cy - 1.2, r'$a_{\max} = 7.311\text{ m/s}^2$',
            fontsize=8.0, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    # 메인 타이틀
    fig.suptitle('[동역학 9판 문제 3/30] 20° 쐐기 위 블록의 미끄럼 방지 한계 작용력(P) 범위 해석',
                 fontsize=12.0, fontweight='bold', y=0.98, fontproperties=font_prop)
    
    # Pillow Image로 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    return img

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, 'prob3_30_wedge_blocks.gif')
    
    fps = 30
    duration = 3.0
    total_frames = int(fps * duration)
    
    print(f"Rendering {total_frames} frames (30 FPS, {duration:.1f}s) for Problem 3/30...")
    frames = []
    
    times = np.linspace(0.0, duration, total_frames)
    for idx, t in enumerate(times):
        img = render_frame(t, duration)
        frames.append(img)
        if (idx + 1) % 15 == 0 or idx == total_frames - 1:
            print(f"  Frame {idx + 1}/{total_frames} (t = {t:.2f}s) rendered.")
            
    print(f"Saving GIF to: {gif_path}")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True
    )
    print("GIF generation complete successfully!")

if __name__ == '__main__':
    main()
