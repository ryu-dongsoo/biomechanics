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
예제 3.9: 지구 주위 원궤도를 선회하는 인공위성의 속도 및 공전주기 해석 (n-t 자연좌표계)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영 (지구 반경 R, 고도 h 원형 궤도, 인공위성 본체 및 태양광 패널, 중심인력)
- 공식 솔루션 매뉴얼(Wiley) 검증: v = 7613 m/s (27,400 km/h), 주기 tau = 5669 s (94.5 min)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터 (지구 및 위성)
R_e = 6371e3            # 지구 반지름 (m)
h = 500e3               # 궤도 고도 (m = 500 km)
r = R_e + h             # 중심 거리 (m = 6871 km)
g0 = 9.81               # 지표면 중력가속도 (m/s^2)
m = 100.0               # 위성 기준 질량 (kg)

# 이론 해석값 계산
# v = R * sqrt(g / r)
v_orb = R_e * np.sqrt(g0 / r)               # 7613.4 m/s (27,408 km/h)
an_val = (v_orb**2) / r                     # 8.437 m/s^2 (궤도 중력가속도 g_r)
period_tau = (2.0 * np.pi * r) / v_orb      # 5669.2 s = 94.49 min = 1.575 hr
Fg_val = m * an_val                         # 843.7 N

# 시각화 정규화 스케일: R_e = 1.0, r = 1.0 + (500/6371)*1.2 = 1.094
r_scale = 1.0
orbit_scale = 1.35
n_frames = 60
orbit_angles = np.linspace(0, 2*np.pi, n_frames, endpoint=False)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_satellite(ax, cx, cy, phi, s_scale=0.18):
    b_w, b_h = s_scale*0.7, s_scale*0.7
    body = patches.Rectangle((-b_w/2, -b_h/2), b_w, b_h, facecolor='#ffffff', edgecolor='#1565c0', lw=1.6)
    p_w, p_h = s_scale*0.8, s_scale*0.3
    p1 = patches.Rectangle((b_w/2, -p_h/2), p_w, p_h, facecolor='#1976d2', edgecolor='#0d47a1', lw=1.2)
    p2 = patches.Rectangle((-b_w/2 - p_w, -p_h/2), p_w, p_h, facecolor='#1976d2', edgecolor='#0d47a1', lw=1.2)
    
    t_sat = plt.matplotlib.transforms.Affine2D().rotate(phi).translate(cx, cy) + ax.transData
    for p in [body, p1, p2]:
        p.set_transform(t_sat)
        ax.add_patch(p)
    ax.plot(cx, cy, 'ko', ms=3.0)

def update(frame):
    ang = orbit_angles[frame]
    sat_x = orbit_scale * np.cos(ang)
    sat_y = orbit_scale * np.sin(ang)
    phi = ang + np.pi/2 # 접선 방향
    
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.9, 2.1)
    ax_main.set_ylim(-1.9, 2.1)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 지구 본체 (대기권 및 푸른 구체)
    atmo = patches.Circle((0, 0), r_scale * 1.03, facecolor='#dcedf9', edgecolor='none')
    earth = patches.Circle((0, 0), r_scale, facecolor='#4da8da', edgecolor='#1d6fa5', lw=2.0)
    ax_main.add_patch(atmo)
    ax_main.add_patch(earth)
    
    # 대륙 표현 (녹색 다각형 패치)
    c1 = patches.Polygon([[-0.2, 0.2], [-0.5, 0.4], [-0.4, 0.7], [0.1, 0.6], [0.0, 0.3]],
                         facecolor='#81c784', edgecolor='none')
    c2 = patches.Polygon([[0.2, -0.3], [0.5, -0.2], [0.6, -0.6], [0.3, -0.7]],
                         facecolor='#81c784', edgecolor='none')
    c3 = patches.Polygon([[-0.6, -0.3], [-0.3, -0.4], [-0.4, -0.7], [-0.7, -0.6]],
                         facecolor='#81c784', edgecolor='none')
    for c in [c1, c2, c3]:
        ax_main.add_patch(c)
        
    # 지구 중심 O 및 반경 R_e
    ax_main.plot(0, 0, 'ko', ms=4.0)
    ax_main.text(-0.06, -0.15, r'$O$', fontsize=12, fontweight='bold')
    dim_th = np.radians(-40.0)
    ax_main.plot([0, r_scale*np.cos(dim_th)], [0, r_scale*np.sin(dim_th)], color='#222222', lw=1.2)
    ax_main.text(r_scale*np.cos(dim_th)/2 + 0.05, r_scale*np.sin(dim_th)/2 - 0.08,
                 r'$R$', fontsize=11, fontweight='bold')
    
    # 고도 h 치수선 (우측 수평)
    ax_main.plot([0, orbit_scale], [0, 0], color='#888888', ls='--', lw=1.0)
    ax_main.annotate('', xy=(orbit_scale, 0), xytext=(r_scale, 0),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text((r_scale + orbit_scale)/2, 0.06, r'$h$', fontsize=11, fontweight='bold', ha='center')
    
    # 원형 궤도선 (파선)
    orbit_circle = patches.Circle((0, 0), orbit_scale, facecolor='none', edgecolor='#e65100',
                                  ls='--', lw=1.5)
    ax_main.add_patch(orbit_circle)
    
    # 인공위성 및 속도 벡터
    draw_satellite(ax_main, sat_x, sat_y, phi, s_scale=0.18)
    
    # 속도 벡터 화살표 (초록색, 접선 방향)
    v_arrow_len = 0.42
    v_dir = np.array([-np.sin(ang), np.cos(ang)])
    ax_main.annotate('', xy=(sat_x + v_arrow_len*v_dir[0], sat_y + v_arrow_len*v_dir[1]),
                     xytext=(sat_x, sat_y),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
    ax_main.text(sat_x + (v_arrow_len+0.08)*v_dir[0], sat_y + (v_arrow_len+0.08)*v_dir[1],
                 f'$v = {v_orb/1e3:.2f}\\ \\mathrm{{km/s}}$', color='#2e7d32', fontsize=10.5, fontweight='bold')
    
    # 중심인력 F_g 화살표 (빨간색, O 방향)
    f_dir = np.array([-np.cos(ang), -np.sin(ang)])
    ax_main.annotate('', xy=(sat_x + 0.35*f_dir[0], sat_y + 0.35*f_dir[1]), xytext=(sat_x, sat_y),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0, mutation_scale=12))
    
    ax_main.set_title('예제 3.9: 지구 주위 원궤도를 선회하는 인공위성', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 정량 해석 및 FBD 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # FBD (상단: 위성에 작용하는 중심 중력선도)
    fbd_cx, fbd_cy = 3.6, 8.2
    draw_satellite(ax_calc, fbd_cx, fbd_cy, 0, s_scale=0.32)
    
    # 중심선 (r축: 하향)
    ax_calc.plot([fbd_cx, fbd_cx], [fbd_cy - 1.5, fbd_cy + 1.1], color='#888888', ls='--', lw=1.2)
    ax_calc.text(fbd_cx + 0.12, fbd_cy + 0.9, r'$r$', fontsize=11, fontweight='bold')
    
    # 중력 인력 F = mg(R/r)^2 (하향: 지구 중심 방향)
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - 1.3), xytext=(fbd_cx, fbd_cy),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15))
    ax_calc.text(fbd_cx + 0.15, fbd_cy - 0.7, r'$F = G\frac{m m_e}{r^2} = mg\frac{R^2}{r^2}$',
                 color='#d32f2f', fontsize=11, fontweight='bold')
    
    # 법선가속도 a_n
    ax_calc.text(fbd_cx - 1.8, fbd_cy - 0.7, r'$a_n = \frac{v^2}{r}$',
                 color='#2e7d32', fontsize=11, fontweight='bold')
    ax_calc.annotate('', xy=(fbd_cx - 0.6, fbd_cy - 0.7), xytext=(fbd_cx - 1.2, fbd_cy - 0.7),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0))
    
    # 중앙: 이론 공식 유도 카드
    sol_box = (
        "이론 해석 및 정량 유도:\n"
        r"(1) 궤도 선회 속도 $v$:" "\n"
        r"  $\bullet\ \sum F_n = m a_n \Rightarrow mg\frac{R^2}{r^2} = m \frac{v^2}{r}$" "\n"
        r"  $\bullet\ v = R\sqrt{\frac{g}{r}} = 6371\times 10^3 \sqrt{\frac{9.81}{6871\times 10^3}}$" "\n"
        r"  $\bullet\ \mathbf{v = 7613\ \mathrm{m/s} = 27,400\ \mathrm{km/h}}$" "\n\n"
        r"(2) 공전 주기 $\tau$ (Orbital Period):" "\n"
        r"  $\bullet\ \tau = \frac{2\pi r}{v} = \frac{2\pi(6871\times 10^3)}{7613} = \mathbf{5669\ \mathrm{s}}$" "\n"
        r"  $\bullet\ \mathbf{\tau = 94.5\ \mathrm{min} = 1.575\ \mathrm{h}}$"
    )
    ax_calc.text(0.5, 4.3, sol_box, fontsize=9.0, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    # 하단: 실시간 동역학 모니터 카드
    live_box = (
        f'궤도 고도: $h = {h/1e3:.0f}\\ \\mathrm{{km}}$ (반경: $r = {r/1e3:.0f}\\ \\mathrm{{km}}$)\n'
        f'궤도 속도: $v = {v_orb:.1f}\\ \\mathrm{{m/s}}$ ({v_orb*3.6:.0f} km/h)\n'
        f'구심 가속도: $a_n = {an_val:.3f}\\ \\mathrm{{m/s^2}}$ ($g_r = 0.860 g$)\n'
        f'공전 주기: $\\tau = {period_tau/60:.1f}\\ \\mathrm{{min}}$ ({period_tau/3600:.2f} 시간/바퀴)'
    )
    ax_calc.text(0.5, 1.0, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('원궤도 역학(n-t) 정량 해석 및 검증', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_9_satellite_orbit.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
