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
동역학 9판 제3장 B편: 일과 에너지 (Section 3.7 위치에너지 및 에너지 보존)
예제 3.16 (Sample Problem 3/16) - 곡선 봉을 따라 미끄러지는 고리와 스프링 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 원도 완벽 반영 2분할 레이아웃
- 교재 공식 해답 검증 완료:
  * 위치 1: V_1 = 63.0 J (탄성 위치에너지, x_1 = 0.6 m)
  * 위치 2: V_g2 = -17.66 J, V_e2 = 10.81 J (x_2 = 0.2485 m)
  * 에너지 보존: T_1 + V_1 = T_2 + V_2  =>  v_2 = 6.82 m/s
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
m = 3.0             # 고리 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
k = 350.0           # 스프링 강성계수 (N/m)
L0 = 0.6            # 스프링 자유(무변형) 길이 (m)
R = 0.6             # 원형 안내봉 곡률 반경 (m)

# 기하 좌표계 설정:
# 안내 곡선 중심: (R, 0) = (0.6, 0.0)
# 스프링 고정 지지점 (Anchor): (2*R, 0) = (1.2, 0.0)
# 위치 1 (초기): (0.0, 0.0) -> 수직 접선
# 위치 2 (최종): (0.6, -0.6) -> 수평 접선
x_center, y_center = 0.6, 0.0
x_anchor, y_anchor = 1.2, 0.0

# 위치 1에서의 에너지
L1 = 1.2
x1 = L1 - L0        # 0.6 m
Ve1 = 0.5 * k * x1**2 # 63.0 J
Vg1 = 0.0
E_total = Ve1       # 63.0 J

# 위치 2에서의 에너지
L2 = np.sqrt(0.6**2 + 0.6**2) # 0.6 * sqrt(2) = 0.8485 m
x2 = L2 - L0        # 0.2485 m
Ve2 = 0.5 * k * x2**2 # 10.81 J
Vg2 = -m * g * R    # -17.658 J
T2 = E_total - (Ve2 + Vg2) # 69.85 J
v2 = np.sqrt(2 * T2 / m)   # 6.82 m/s

# 애니메이션 매개변수 (원형 경로 매개변수 phi: 180도 -> 270도)
n_frames = 50
phi_vals = np.linspace(np.pi, 1.5 * np.pi, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.05, color='#444444', lw=1.8):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-6:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    
    lead_len = 0.06
    active_len = max(length - 2 * lead_len, 0.05)
    
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
    phi = phi_vals[frame]
    
    # 칼라 현재 좌표
    x_c = x_center + R * np.cos(phi)
    y_c = y_center + R * np.sin(phi)
    
    # 스프링 길이 및 변형량
    L_curr = np.sqrt((x_anchor - x_c)**2 + (y_anchor - y_c)**2)
    x_curr = L_curr - L0
    
    # 에너지 계산
    Ve_curr = 0.5 * k * x_curr**2
    Vg_curr = m * g * y_c  # y_c <= 0 이므로 음수
    T_curr = max(E_total - (Ve_curr + Vg_curr), 0.0)
    v_curr = np.sqrt(2 * T_curr / m)
    
    # ---------------- 1. 메인 물리 시스템 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.25, 1.45)
    ax_main.set_ylim(-0.85, 0.35)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 천장/지지대 해칭 (상단 지지벽)
    ax_main.plot([-0.15, 0.15], [0.08, 0.08], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.15, 0.12, 6):
        ax_main.plot([hx, hx + 0.04], [0.08, 0.14], color='#666666', lw=1.2)
    mount_top = patches.Rectangle((-0.06, 0.0), 0.12, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_top)
    
    # 우측 스프링 고정 앵커 (Wall Mount)
    ax_main.plot([x_anchor + 0.06, x_anchor + 0.06], [-0.15, 0.15], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.14, 0.11, 6):
        ax_main.plot([x_anchor + 0.06, x_anchor + 0.12], [hy, hy + 0.04], color='#666666', lw=1.2)
    anchor_mount = patches.Polygon([[x_anchor, 0.0], [x_anchor + 0.06, 0.08], [x_anchor + 0.06, -0.08]],
                                   facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(anchor_mount)
    ax_main.plot(x_anchor, y_anchor, 'o', color='#2b2b2b', markersize=5)
    
    # 하단 2번 위치 고정 지지대
    ax_main.plot([0.72, 0.72], [-0.75, -0.45], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.73, -0.48, 6):
        ax_main.plot([0.72, 0.78], [hy, hy + 0.04], color='#666666', lw=1.2)
    mount_bot = patches.Rectangle((0.64, -0.64), 0.08, 0.08, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_bot)
    
    # 원형 안내봉 (Curved Rod) - 교재와 동일한 튜브 질감
    theta_rod = np.linspace(np.pi, 1.5 * np.pi, 100)
    rx = x_center + R * np.cos(theta_rod)
    ry = y_center + R * np.sin(theta_rod)
    ax_main.plot(rx, ry, color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot(rx, ry, color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    # 연장선
    ax_main.plot([0.6, 0.65], [-0.6, -0.6], color='#4682b4', lw=8.0, zorder=2)
    ax_main.plot([0.6, 0.65], [-0.6, -0.6], color='#d0e4f7', lw=3.0, zorder=2)
    
    # 초기 위치 1 스프링 및 최종 위치 2 가상선 (점선)
    draw_spring(ax_main, (0.0, 0.0), (x_anchor, y_anchor), nodes=16, width=0.04, color='#bbbbbb', lw=1.2)
    draw_spring(ax_main, (0.6, -0.6), (x_anchor, y_anchor), nodes=12, width=0.04, color='#bbbbbb', lw=1.2)
    
    # 현재 작동 스프링 (동적)
    draw_spring(ax_main, (x_c, y_c), (x_anchor, y_anchor), nodes=14, width=0.045, color='#2b2b2b', lw=2.0)
    ax_main.text(0.70, -0.15, r'$k = 350\ \mathrm{N/m}$', fontsize=10.5, fontweight='bold', color='#1a5276', rotation=22)
    
    # 미끄럼고리 (Collar) 렌더링 (진행 각도에 맞춘 회전 칼라)
    tang_angle = phi + np.pi / 2
    collar_w, collar_h = 0.12, 0.07
    c_poly = patches.Polygon([
        [-collar_w/2, -collar_h/2], [collar_w/2, -collar_h/2],
        [collar_w/2, collar_h/2], [-collar_w/2, collar_h/2]
    ], facecolor='#e67e22', edgecolor='#78341a', lw=1.8, zorder=5)
    t = patches.transforms.Affine2D().rotate(tang_angle).translate(x_c, y_c) + ax_main.transData
    c_poly.set_transform(t)
    ax_main.add_patch(c_poly)
    ax_main.plot(x_c, y_c, 'o', color='#2b2b2b', markersize=4, zorder=6)
    
    # 속도 벡터 표시
    if v_curr > 0.3:
        v_scale = 0.035 * (v_curr / v2)
        vx = -np.sin(phi) * v_scale
        vy = np.cos(phi) * v_scale
        ax_main.annotate('', xy=(x_c + vx, y_c + vy), xytext=(x_c, y_c),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(x_c + vx * 1.1, y_c + vy * 1.1 - 0.05, f'$v$', color='#27ae60', fontsize=11, fontweight='bold')
    
    # 치수선 및 레이블 (교재 1:1 완벽 반영)
    # 상단 수평 0.6 m 치수선
    ax_main.plot([0.6, 1.2], [0.18, 0.18], color='#333333', lw=1.2)
    ax_main.plot([0.6, 0.6], [-0.6, 0.22], color='#777777', ls='--', lw=1.0)
    ax_main.plot([1.2, 1.2], [0.0, 0.22], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(0.6, 0.18), xytext=(0.85, 0.18), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(1.2, 0.18), xytext=(0.95, 0.18), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(0.90, 0.21, r'$0.6\ \mathrm{m}$', ha='center', fontsize=10)
    
    # 곡률 반경 0.6 m 화살표
    ax_main.annotate('', xy=(0.3, -0.3*np.sqrt(3)/1), xytext=(0.6, 0.0),
                     arrowprops=dict(arrowstyle='->', color='#777777', ls=':', lw=1.2))
    ax_main.text(0.28, -0.15, r'$0.6\ \mathrm{m}$', fontsize=10, color='#555555')
    
    # 위치 1, 2 표시
    ax_main.text(-0.12, 0.0, r'$\mathbf{1}$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(0.55, -0.73, r'$\mathbf{2}$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(-0.06, -0.22, r'$3\ \mathrm{kg}$', fontsize=10.5, color='#333333')
    
    ax_main.set_title('예제 3.16 기구도 (원형 레일 칼라 시스템)', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. 실시간 에너지 보존 & FBD 패널 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    # 에너지 막대 그래프 (Energy Monitor)
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, T_curr + Ve_curr + Vg_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e74c3c', '#8e44ad']
    bar_labels = [r'$T$', r'$V_e$', r'$V_g$', r'$E_{\mathrm{tot}}$']
    
    # 상단 에너지 바 표시
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        # 60 J 기준 정규화
        h_norm = (val / 70.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + (0.06 if h_norm >= 0 else -0.12), f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    # 수치 검증 및 이론 카드 (교재 공식 솔루션과 100% 동일)
    summary_box = (
        f"【교재 공식 일-에너지 해석 (Section 3.7)】\n"
        f"• 상태 1: $x_1 = 1.2 - 0.6 = 0.6\\ \\mathrm{{m}},\\ V_1 = \\frac{{1}}{{2}}(350)(0.6)^2 = 63.0\\ \\mathrm{{J}}$\n"
        f"• 상태 2: $x_2 = 0.6\\sqrt{{2}} - 0.6 = 0.2485\\ \\mathrm{{m}},\\ V_{{e2}} = 10.81\\ \\mathrm{{J}}$\n"
        f"  중력 위치에너지: $V_{{g2}} = -mgh = -3(9.81)(0.6) = -17.66\\ \\mathrm{{J}}$\n"
        f"• 에너지 보존: $T_1 + V_1 = T_2 + V_2$\n"
        f"  $0 + 63.0 = \\frac{{1}}{{2}}(3)v_2^2 - 17.66 + 10.81$\n"
        f"  $\\rightarrow\\ v_2 = \\mathbf{{6.82\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• 현재 진행률: {(frame+1)/n_frames*100:3.0f}%\n"
        f"• 현재 속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (최종: $6.82\\ \\mathrm{{m/s}}$)"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.5, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('에너지 보존 모니터 및 이론적 검증', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_16_curved_rod_collar.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
