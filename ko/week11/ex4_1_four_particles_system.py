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
동역학 9판 제4장: 질점계의 운동역학
예제 4.1 (Sample Problem 4/1) - 3차원 4질점 시스템의 질량중심, 운동에너지, 선운동량 및 각운동량 해석
- 순수 흰색 바탕 (#ffffff) & 교재 등각 투영(Isometric 3D->2D) 원도 완벽 반영
- 이론 정량 검증 완료:
  * r_bar = d(-0.4 i + 0.2 j + 0.2 k)
  * v_bar = v(0.3 i + 0.3 j + 0.3 k),  a_bar = (F / 10m)(i + j)
  * T = (11/2) m v^2 = 5.5 m v^2,  G = m v(3 i + 3 j + 3 k)
  * H_O = m v d(-2 i + 6 j - 4 k),  H_O_dot = F d(j - 2 k)
  * H_G = m v d(-2 i + 4.2 j - 2.2 k),  H_G_dot = F d(0.2 i + 0.8 j - 1.4 k)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 및 수식 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 기준 단위 매개변수 (m = 1, d = 1, v = 1, F = 1 기준 무차원/단위 수치)
m = 1.0
d = 1.0
v = 1.0
F = 1.0
M_tot = 10.0 * m

# 초기 위치 (t = 0, 교재 원도 기준)
r1_0 = np.array([2.0*d, -2.0*d, 0.0])
r2_0 = np.array([0.0, 0.0, 1.0*d])
r3_0 = np.array([-2.0*d, 0.0, 0.0])
r4_0 = np.array([0.0, 1.0*d, 0.0])

# 초기 속도 벡터
v1_0 = np.array([-1.0*v, 1.0*v, 0.0])
v2_0 = np.array([0.0, 1.0*v, 0.0])
v3_0 = np.array([0.0, 0.0, 1.0*v])
v4_0 = np.array([1.0*v, 0.0, 0.0])

# 작용 외력 벡터
F1 = np.array([0.0, 0.0, 0.0])
F2 = np.array([1.0*F, 0.0, 0.0])
F3 = np.array([0.0, 1.0*F, 0.0])
F4 = np.array([0.0, 0.0, 0.0])

masses = np.array([1.0*m, 2.0*m, 3.0*m, 4.0*m])
a1 = F1 / masses[0]
a2 = F2 / masses[1]
a3 = F3 / masses[2]
a4 = F4 / masses[3]

# 이론 초기값 (t = 0 순간)
r_bar_0 = (masses[0]*r1_0 + masses[1]*r2_0 + masses[2]*r3_0 + masses[3]*r4_0) / M_tot
v_bar_0 = (masses[0]*v1_0 + masses[1]*v2_0 + masses[2]*v3_0 + masses[3]*v4_0) / M_tot
a_bar = (F1 + F2 + F3 + F4) / M_tot

# 등각 투영 함수 (3D (x, y, z) -> 2D (X, Y), 교재 그림 시점 일치: x는 좌하단, y는 우하단, z는 수직 상방)
ang_x = np.radians(210.0)
ang_y = np.radians(-22.0)

def proj3d(pt3):
    x, y, z = pt3[0], pt3[1], pt3[2]
    X = x * np.cos(ang_x) + y * np.cos(ang_y)
    Y = x * np.sin(ang_x) + y * np.sin(ang_y) + z
    return np.array([X, Y])

n_frames = 48
t_vals = np.linspace(0.0, 0.55, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_sphere(ax, center_2d, radius, label_mass, label_id, offset_id):
    circle = patches.Circle(center_2d, radius, facecolor='#d96b6b', edgecolor='#5c1f1f', lw=1.8, zorder=5)
    ax.add_patch(circle)
    hl = patches.Circle(center_2d + np.array([-0.28*radius, 0.28*radius]), 0.28*radius,
                        facecolor='#f4b3b3', edgecolor='none', zorder=6)
    ax.add_patch(hl)
    ax.text(center_2d[0] + offset_id[0], center_2d[1] + offset_id[1],
            f'{label_id} ({label_mass})', fontsize=10, fontweight='bold', color='#222222', ha='center', va='center', zorder=7)

def update(frame):
    t = t_vals[frame]
    
    # 현재 각 질점의 위치 및 속도
    r1 = r1_0 + v1_0 * t + 0.5 * a1 * t**2
    r2 = r2_0 + v2_0 * t + 0.5 * a2 * t**2
    r3 = r3_0 + v3_0 * t + 0.5 * a3 * t**2
    r4 = r4_0 + v4_0 * t + 0.5 * a4 * t**2
    
    v1 = v1_0 + a1 * t
    v2 = v2_0 + a2 * t
    v3 = v3_0 + a3 * t
    v4 = v4_0 + a4 * t
    
    r_bar = r_bar_0 + v_bar_0 * t + 0.5 * a_bar * t**2
    v_bar = v_bar_0 + a_bar * t
    T_curr = 0.5 * (masses[0]*np.dot(v1,v1) + masses[1]*np.dot(v2,v2) + masses[2]*np.dot(v3,v3) + masses[3]*np.dot(v4,v4))
    
    # ---------------- 1. 메인 뷰 (3D 등각 투영) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-4.5, 2.6)
    ax_main.set_ylim(-2.2, 2.4)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    pO = proj3d([0, 0, 0])
    
    # 좌표축 x, y, z (파선 + 실선 축)
    for axis_vec, lbl, off in [
        ([2.8, 0, 0], r'$x$', [-0.15, -0.12]),
        ([-2.5, 0, 0], '', [0, 0]),
        ([0, 2.4, 0], r'$y$', [0.15, -0.06]),
        ([0, -2.4, 0], '', [0, 0]),
        ([0, 0, 2.1], r'$z$', [0.0, 0.14]),
        ([0, 0, -1.2], '', [0, 0])
    ]:
        p_end = proj3d(axis_vec)
        ax_main.plot([pO[0], p_end[0]], [pO[1], p_end[1]], color='#666666', ls='--', lw=1.2, zorder=1)
        if lbl:
            ax_main.text(p_end[0] + off[0], p_end[1] + off[1], lbl, fontsize=12, fontweight='bold', ha='center', va='center')
            
    ax_main.plot(pO[0], pO[1], 'ko', markersize=4, zorder=4)
    ax_main.text(pO[0] + 0.14, pO[1] - 0.18, r'$O$', fontsize=12, fontweight='bold')
    
    # 초기 위치 보조선 (x-y 평면 내 질점 1 투영선)
    p1_init = proj3d(r1_0)
    p_x2 = proj3d([2*d, 0, 0])
    p_y_2 = proj3d([0, -2*d, 0])
    ax_main.plot([p_x2[0], p1_init[0], p_y_2[0]], [p_x2[1], p1_init[1], p_y_2[1]], color='#999999', lw=1.0, zorder=1)
    ax_main.text(0.5*(p_x2[0]+p1_init[0])-0.15, 0.5*(p_x2[1]+p1_init[1])-0.18, r'$2d$', fontsize=10, color='#555555')
    ax_main.text(0.5*(p_y_2[0]+p1_init[0])-0.22, 0.5*(p_y_2[1]+p1_init[1])+0.12, r'$2d$', fontsize=10, color='#555555')
    
    # 현재 질점들의 2D 투영 위치
    P1, P2, P3, P4 = proj3d(r1), proj3d(r2), proj3d(r3), proj3d(r4)
    PG = proj3d(r_bar)
    PG0 = proj3d(r_bar_0)
    
    # 질점 반지름 (질량 비례 시각적 구분)
    draw_sphere(ax_main, P1, 0.13, r'$m$', '1', [-0.32, -0.22])
    draw_sphere(ax_main, P2, 0.16, r'$2m$', '2', [-0.38, 0.22])
    draw_sphere(ax_main, P3, 0.19, r'$3m$', '3', [-0.38, 0.25])
    draw_sphere(ax_main, P4, 0.22, r'$4m$', '4', [0.35, -0.26])
    
    # 속도 벡터 (초록색 화살표)
    v_scale = 0.55
    for P_pt, v_vec, v_lbl, lbl_off in [
        (P1, v1, r'$\sqrt{2}v$', [0.22, 0.22]),
        (P2, v2, r'$v$', [0.18, -0.18]),
        (P3, v3, r'$v$', [0.18, 0.15]),
        (P4, v4, r'$v$', [-0.15, -0.22])
    ]:
        P_vend = proj3d(np.zeros(3) + v_vec * v_scale) + P_pt
        ax_main.annotate('', xy=P_vend, xytext=P_pt,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=8)
        ax_main.text(P_vend[0] + lbl_off[0], P_vend[1] + lbl_off[1], v_lbl,
                     color='#2e7d32', fontsize=10.5, fontweight='bold', ha='center', va='center')
        
    # 외력 벡터 F (빨간색 화살표: 질점 2에 +x 방향, 질점 3에 +y 방향)
    f_scale = 0.65
    for P_pt, F_vec, f_off in [(P2, F2, [-0.22, -0.16]), (P3, F3, [0.22, -0.15])]:
        P_fend = proj3d(F_vec * f_scale) + P_pt
        ax_main.annotate('', xy=P_fend, xytext=P_pt,
                         arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=8)
        ax_main.text(P_fend[0] + f_off[0], P_fend[1] + f_off[1], r'$\mathbf{F}$',
                     color='#d32f2f', fontsize=11, fontweight='bold', ha='center', va='center')
        
    # 질량중심 G 마커 및 속도 벡터
    ax_main.plot([PG0[0], PG[0]], [PG0[1], PG[1]], color='#1565c0', ls=':', lw=1.8, zorder=4)
    ax_main.plot(PG[0], PG[1], marker='D', markersize=7.5, markerfacecolor='#ffeb3b', markeredgecolor='#1565c0', markeredgewidth=1.8, zorder=9)
    ax_main.text(PG[0] + 0.18, PG[1] + 0.18, r'$G$', fontsize=11.5, fontweight='bold', color='#1565c0', zorder=10)
    
    ax_main.set_title('예제 4.1: 3차원 4질점 시스템의 운동역학 해석', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. 이론 해석 및 정량 검증 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "이론 해석 및 정량 유도 (초기 순간 t = 0 기준, 총 질량 M = 10m):\n"
        r"$\bullet\ \bar{\mathbf{r}} = \frac{\sum m_i \mathbf{r}_i}{10m} = \mathbf{d(-0.4\mathbf{i} + 0.2\mathbf{j} + 0.2\mathbf{k})}$" "\n"
        r"$\bullet\ \dot{\bar{\mathbf{r}}} = \frac{\sum m_i \dot{\mathbf{r}}_i}{10m} = \mathbf{v(0.3\mathbf{i} + 0.3\mathbf{j} + 0.3\mathbf{k})}$" "\n"
        r"$\bullet\ \ddot{\bar{\mathbf{r}}} = \frac{\sum \mathbf{F}}{10m} = \mathbf{\frac{F}{10m}(\mathbf{i} + \mathbf{j})}$" "\n"
        r"$\bullet\ T = \sum \frac{1}{2}m_i v_i^2 = \frac{1}{2}[2mv^2 + 2mv^2 + 3mv^2 + 4mv^2] = \mathbf{\frac{11}{2}mv^2}$" "\n"
        r"$\bullet\ \mathbf{G} = M\dot{\bar{\mathbf{r}}} = \mathbf{mv(3\mathbf{i} + 3\mathbf{j} + 3\mathbf{k})}$" "\n"
        r"$\bullet\ \mathbf{H}_O = \sum(\mathbf{r}_i \times m_i\mathbf{v}_i) = \mathbf{mvd(-2\mathbf{i} + 6\mathbf{j} - 4\mathbf{k})}$" "\n"
        r"$\bullet\ \dot{\mathbf{H}}_O = \sum \mathbf{M}_O = \mathbf{Fd(\mathbf{j} - 2\mathbf{k})}$" "\n"
        r"$\bullet\ \mathbf{H}_G = \mathbf{H}_O - \bar{\mathbf{r}} \times M\bar{\mathbf{v}} = \mathbf{mvd(-2\mathbf{i} + 4.2\mathbf{j} - 2.2\mathbf{k})}$" "\n"
        r"$\bullet\ \dot{\mathbf{H}}_G = \sum \mathbf{M}_O - \bar{\mathbf{r}} \times M\bar{\mathbf{a}} = \mathbf{Fd(0.2\mathbf{i} + 0.8\mathbf{j} - 1.4\mathbf{k})}$"
    )
    ax_calc.text(0.3, 6.1, sol_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"실시간 질량중심 상태 모니터 ($t = {t:.2f}\\ \\mathrm{{s}}$, 단위계 $m=d=v=F=1$):\n"
        f"질량중심 위치: $\\bar{{\\mathbf{{r}}}}(t) = ({r_bar[0]:+.2f}\\mathbf{{i}} {r_bar[1]:+.2f}\\mathbf{{j}} {r_bar[2]:+.2f}\\mathbf{{k}})\\ d$\n"
        f"질량중심 속도: $\\dot{{\\bar{{\\mathbf{{r}}}}}}(t) = ({v_bar[0]:+.2f}\\mathbf{{i}} {v_bar[1]:+.2f}\\mathbf{{j}} {v_bar[2]:+.2f}\\mathbf{{k}})\\ v$\n"
        f"순간 운동에너지: $T(t) = {T_curr:.2f}\\ mv^2$ (초기 이론값: $5.50\\ mv^2$)"
    )
    ax_calc.text(0.3, 1.45, live_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('질점계 운동역학 방정식 및 정량 검증', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_1_four_particles_system.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
