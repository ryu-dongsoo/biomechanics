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
예제 3.18 (Sample Problem 3/18) - 비틀림 스프링 막대와 연성 실린더 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 (회전 봉 OA, 비틀림 스프링, 줄 S, 실린더 B)
- 교재 공식 해답 및 수치 검증 완료:
  * (a) theta = 90°일 때 v_A = 0.794 m/s
  * (b) 0° <= theta <= 90° 속도 곡선: 최대 속도 (v_A)_max = 1.400 m/s (theta = 56.4°에서 발생)
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
mA = 2.0            # 질점 A 질량 (kg)
mB = 4.0            # 실린더 B 질량 (kg)
L = 0.5             # 막대 OA 길이 (m)
kT = 13.0           # 비틀림 스프링 상수 (N·m/rad)
g = 9.81            # 중력가속도 (m/s^2)

# 기하 좌표계 (O점 = (0, 0))
# C점은 막대 중앙 (길이 L/2 = 0.25 m)
# 지지대 구멍 C'' 위치: (-L/2, 0) = (-0.25, 0.0)
xC_prime = -L / 2.0
yC_prime = 0.0

# 속도 함수 정의
def get_kinematics(th):
    # th: 반시계방향 각도 (rad)
    alpha = (np.pi / 2.0 - th) / 2.0
    chord = 2.0 * (L / 2.0) * np.sin(alpha)
    initial_chord = (L / 2.0) * np.sqrt(2.0)
    delta_s = initial_chord - chord
    delta_yB = 0.5 * delta_s
    
    # 위치에너지
    Delta_VgA = -mA * g * L * (1.0 - np.cos(th))
    Delta_VgB = -mB * g * delta_yB
    Delta_Ve = 0.5 * kT * th**2
    Delta_V = Delta_VgA + Delta_VgB + Delta_Ve
    
    # 운동에너지 계수
    coeff = mA + (mB / 16.0) * (np.cos(alpha))**2
    T = max(-Delta_V, 0.0)
    vA = np.sqrt(2.0 * T / coeff) if coeff > 0 else 0.0
    vB = (vA / 4.0) * np.cos(alpha)
    return vA, vB, delta_yB, Delta_VgA, Delta_VgB, Delta_Ve

# 곡선 데이터 사전 생성 (0 to 90 deg)
theta_plot_deg = np.linspace(0.01, 90.0, 200)
theta_plot_rad = np.radians(theta_plot_deg)
vA_plot = np.array([get_kinematics(th)[0] for th in theta_plot_rad])

# 애니메이션 설정 (0도 -> 90도)
n_frames = 50
theta_vals = np.linspace(0.001, np.radians(90.0), n_frames)

fig, (ax_main, ax_graph) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.1, 1.1]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def update(frame):
    th = theta_vals[frame]
    th_deg = np.degrees(th)
    vA, vB, delta_yB, VgA, VgB, Ve = get_kinematics(th)
    
    # 질점 A 및 점 C 좌표 (수직에서 반시계방향 회전)
    # x = -L * sin(th), y = L * cos(th)
    xA_curr = -L * np.sin(th)
    yA_curr = L * np.cos(th)
    xC_curr = -(L / 2.0) * np.sin(th)
    yC_curr = (L / 2.0) * np.cos(th)
    
    # ---------------- 1. 메인 기구도 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.65, 0.45)
    ax_main.set_ylim(-0.85, 0.65)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 수평 지지 테이블 (Hatching)
    table_poly = np.array([
        [-0.45, 0.0], [0.35, 0.0], [0.35, -0.12], [-0.45, -0.12]
    ])
    ax_main.fill(table_poly[:, 0], table_poly[:, 1], color='#e4ded4', edgecolor='#2b2b2b', lw=1.5)
    
    # 수직 안내 구멍 (C'' 위치: x = -0.25)
    ax_main.plot([-0.25, -0.25], [0.0, -0.12], color='#ffffff', lw=4.0)
    ax_main.plot([-0.27, -0.27], [0.0, -0.12], color='#2b2b2b', lw=1.5)
    ax_main.plot([-0.23, -0.23], [0.0, -0.12], color='#2b2b2b', lw=1.5)
    
    # 지지대 O 피벗 (Torsion spring 마운트)
    mount_O = patches.Polygon([[-0.08, -0.08], [0.08, -0.08], [0.0, 0.0]],
                              facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5, zorder=3)
    ax_main.add_patch(mount_O)
    ax_main.plot(0.0, 0.0, 'o', color='#2b2b2b', markersize=5, zorder=6)
    ax_main.text(0.03, -0.05, r'$O$', fontsize=12, fontweight='bold')
    
    # 비틀림 스프링 기호 (나선형 호)
    arc_spring = patches.Arc((0, 0), 0.12, 0.12, angle=0, theta1=0, theta2=220, color='#888888', lw=1.8, zorder=4)
    ax_main.add_patch(arc_spring)
    ax_main.text(0.07, 0.06, r'$k_T$', fontsize=10.5, color='#1a5276', fontweight='bold')
    
    # 회전 궤적 (주황 점선)
    th_arc = np.linspace(0, np.pi/2, 50)
    ax_main.plot(-L * np.sin(th_arc), L * np.cos(th_arc), ls='--', color='#e67e22', lw=1.2)
    ax_main.plot(-(L/2) * np.sin(th_arc), (L/2) * np.cos(th_arc), ls=':', color='#e67e22', lw=1.0)
    
    # 막대 OA (가느다란 봉)
    ax_main.plot([0.0, xA_curr], [0.0, yA_curr], color='#2b2b2b', lw=3.0, zorder=4)
    
    # 점 C 핀
    ax_main.plot(xC_curr, yC_curr, 'o', color='#d32f2f', markersize=4, zorder=6)
    ax_main.text(xC_curr + 0.03, yC_curr + 0.02, r'$C$', fontsize=11, fontweight='bold', color='#d32f2f')
    
    # 질점 A (구체)
    ball_A = patches.Circle((xA_curr, yA_curr), 0.045, facecolor='#e67e22', edgecolor='#78341a', lw=1.8, zorder=5)
    ax_main.add_patch(ball_A)
    ax_main.text(xA_curr - 0.08, yA_curr + 0.03, r'$m_A$', fontsize=11, fontweight='bold')
    
    # 줄 S: 점 C -> 구멍 (-0.25, 0.0) -> 도르래 B -> 고정점
    # 도르래 B 위치: y는 delta_yB만큼 하강
    y_pulley = -0.32 - delta_yB
    ax_main.plot([xC_curr, -0.25], [yC_curr, 0.0], color='#2b2b2b', lw=1.8, zorder=3)
    ax_main.text((xC_curr - 0.25)/2 - 0.04, yC_curr/2 + 0.04, r'$S$', fontsize=11, fontweight='bold')
    
    # 도르래로 내려가는 줄
    ax_main.plot([-0.25, -0.25], [0.0, y_pulley], color='#2b2b2b', lw=1.8, zorder=3)
    ax_main.plot([-0.17, -0.17], [-0.12, y_pulley], color='#2b2b2b', lw=1.8, zorder=3)
    
    # 매달린 도르래 (Pulley B)
    r_pulley = 0.04
    pulley_B = patches.Circle((-0.21, y_pulley), r_pulley, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5, zorder=4)
    ax_main.add_patch(pulley_B)
    
    # 실린더 B (질량 4 kg)
    cyl_w, cyl_h = 0.12, 0.22
    cyl_top = y_pulley - r_pulley - 0.04
    ax_main.plot([-0.21, -0.21], [y_pulley, cyl_top], color='#2b2b2b', lw=2.0)
    cyl_B = patches.Rectangle((-0.21 - cyl_w/2, cyl_top - cyl_h), cyl_w, cyl_h,
                              facecolor='#b87333', edgecolor='#5a2d0c', lw=1.8, zorder=5)
    ax_main.add_patch(cyl_B)
    ax_main.text(-0.21, cyl_top - cyl_h/2, r'$m_B$', color='#ffffff', ha='center', va='center', fontsize=10, fontweight='bold')
    ax_main.text(-0.35, cyl_top - cyl_h/2, r'$B$', fontsize=12, fontweight='bold', color='#2b2b2b')
    
    # 속도 벡터 A
    if vA > 0.1:
        v_scale = 0.12 * (vA / 1.40)
        # vA는 막대에 수직인 방향 (접선 방향)
        vx = -np.cos(th) * v_scale
        vy = -np.sin(th) * v_scale
        ax_main.annotate('', xy=(xA_curr + vx, yA_curr + vy), xytext=(xA_curr, yA_curr),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(xA_curr + vx - 0.05, yA_curr + vy + 0.02, r'$v_A$', color='#27ae60', fontsize=11, fontweight='bold')
    
    # 각도 theta 호 표시
    arc_th = patches.Arc((0, 0), 0.25, 0.25, angle=90, theta1=0, theta2=th_deg, color='#2b2b2b', lw=1.5)
    ax_main.add_patch(arc_th)
    ax_main.text(-0.06, 0.18, r'$\theta$', fontsize=11, fontweight='bold')
    
    ax_main.set_title('예제 3.18 기구도 (막대-도르래 연성 시스템)', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. 교재 vA(theta) 특성 곡선 & 검증 패널 ----------------
    ax_graph.cla()
    ax_graph.set_facecolor('#ffffff')
    
    # 교재와 동일한 vA - theta 그래프 플롯
    ax_graph.plot(theta_plot_deg, vA_plot, color='#d32f2f', lw=2.5, label=r'$v_A(\theta)$ 특성 곡선')
    ax_graph.plot(56.4, 1.400, 'ko', markersize=6)
    ax_graph.text(56.4, 1.44, r'$(v_A)_{\max} = 1.400\ \mathrm{m/s}\ (\theta = 56.4^\circ)$',
                  ha='center', fontsize=9.5, fontweight='bold', color='#111111')
    
    # 90도 값 표시
    ax_graph.plot(90.0, 0.794, 'bs', markersize=5)
    ax_graph.text(90.0, 0.73, r'$v_A(90^\circ) = 0.794\ \mathrm{m/s}$', ha='right', fontsize=9.5, color='#2980b9')
    
    # 현재 애니메이션 위치 트래커 (초록 큰 점)
    ax_graph.plot(th_deg, vA, 'o', color='#27ae60', markersize=8, zorder=8)
    
    ax_graph.set_xlim(0, 95)
    ax_graph.set_ylim(0, 1.65)
    ax_graph.set_xlabel(r'$\theta\ (\mathrm{deg})$', fontsize=11)
    ax_graph.set_ylabel(r'$v_A\ (\mathrm{m/s})$', fontsize=11)
    ax_graph.grid(True, ls=':', color='#cccccc')
    ax_graph.legend(loc='lower left', frameon=True, facecolor='#ffffff')
    
    # 하단 이론 검증 카드
    summary_box = (
        f"【교재 공식 일-에너지 해석 (Section 3.7)】\n"
        f"• (a) $\\theta = 90^\\circ$ 일 때:\n"
        f"  $v_B = \\frac{{1}}{{4}} v_A,\\quad \\Delta y_B = \\frac{{L\\sqrt{{2}}}}{{4}} = \\frac{{0.5\\sqrt{{2}}}}{{4}} = 0.1768\\ \\mathrm{{m}}$\n"
        f"  $0 = \\frac{{1}}{{2}}(2)v_A^2 + \\frac{{1}}{{2}}(4)\\left(\\frac{{v_A}}{{4}}\\right)^2 - 2(9.81)(0.5) - 4(9.81)(0.1768) + \\frac{{1}}{{2}}(13)\\left(\\frac{{\\pi}}{{2}}\\right)^2$\n"
        f"  $\\rightarrow\\ v_A = \\mathbf{{0.794\\ \\mathrm{{m/s}}}}$\n"
        f"• (b) 최대 속도: $\\mathbf{{(v_A)_{{\\max}} = 1.400\\ \\mathrm{{m/s}}}}$ at $\\theta = 56.4^\\circ$\n"
        f"─────────────────────────────\n"
        f"• 현재 각도: $\\theta = {th_deg:.1f}^\\circ,\\quad v_A = {vA:.3f}\\ \\mathrm{{m/s}},\\quad v_B = {vB:.3f}\\ \\mathrm{{m/s}}$"
    )
    ax_graph.text(0.02, 0.05, summary_box, transform=ax_graph.transAxes, fontsize=8.8,
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.2))
    
    ax_graph.set_title('속도-각도 특성 곡선 및 수치 검증', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_18_torsion_rod_cylinder.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
