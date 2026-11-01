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
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
예제 3.25 (Sample Problem 3/25) - 장타원 궤도 혜성의 각운동량 보존
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * 원일점 A: r_A = 6000 x 10^6 km, v_A = 740 m/s
  * 근일점 B: r_B = 75 x 10^6 km
  * 중심력장 각운동량 보존 (H_O)_A = (H_O)_B => m r_A v_A = m r_B v_B
  * v_B = (6000 / 75) * 740 = 80 * 740 = 59,200 m/s (59.2 km/s)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
r_A = 6000.0   # 10^6 km
r_B = 75.0     # 10^6 km
v_A = 740.0    # m/s
v_B = (r_A / r_B) * v_A  # 59,200 m/s

a_vis = 4.2
b_vis = 1.65
c_vis = 3.1
sun_x, sun_y = -c_vis, 0.0

n_frames = 55
u_lin = np.linspace(0, 2 * np.pi, n_frames)
theta_orbit = u_lin + 0.55 * np.sin(u_lin)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    ang = theta_orbit[frame]
    cx = a_vis * np.cos(ang)
    cy = b_vis * np.sin(ang)

    w_factor = 0.5 * (1.0 + np.cos(ang))
    r_curr = r_B + (r_A - r_B) * (w_factor**1.8)
    v_curr = (r_A * v_A) / r_curr

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-5.5, 5.5)
    ax_main.set_ylim(-3.3, 3.0)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('예제 3.25: 장타원 궤도 혜성의 각운동량 보존 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    space_box = patches.FancyBboxPatch((-4.85, -1.95), 9.7, 4.1, boxstyle='round,pad=0.1',
                                       facecolor='#eef6fb', edgecolor='#7fb3d5', lw=1.8, zorder=1)
    ax_main.add_patch(space_box)

    t_curve = np.linspace(0, 2 * np.pi, 200)
    ax_main.plot(a_vis * np.cos(t_curve), b_vis * np.sin(t_curve), color='#e67e22', ls='--', lw=2.0, zorder=2)

    for arr_ang in [0.55, 2.4, 3.8, 5.5]:
        ax_x = a_vis * np.cos(arr_ang)
        ax_y = b_vis * np.sin(arr_ang)
        dx = -a_vis * np.sin(arr_ang) * 0.08
        dy = b_vis * np.cos(arr_ang) * 0.08
        ax_main.annotate('', xy=(ax_x + dx, ax_y + dy), xytext=(ax_x - dx, ax_y - dy),
                         arrowprops=dict(arrowstyle='->', color='#d35400', lw=1.8, mutation_scale=13), zorder=3)

    sun_glow = patches.Circle((sun_x, sun_y), 0.42, facecolor='#fff3bf', edgecolor='none', alpha=0.8, zorder=3)
    sun_core = patches.Circle((sun_x, sun_y), 0.26, facecolor='#fcc419', edgecolor='#e67700', lw=1.5, zorder=4)
    ax_main.add_patch(sun_glow)
    ax_main.add_patch(sun_core)
    ax_main.text(sun_x + 0.35, sun_y + 0.35, r'$O$', fontsize=12, fontweight='bold', color='#1a5276', zorder=5)

    ax_main.plot(a_vis, 0, 'o', color='#111111', markersize=6, zorder=5)
    ax_main.text(a_vis + 0.22, 0.18, r'$A$', fontsize=12, fontweight='bold', color='#111111', zorder=5)
    ax_main.plot(-a_vis, 0, 'o', color='#111111', markersize=6, zorder=5)
    ax_main.text(-a_vis - 0.35, 0.18, r'$B$', fontsize=12, fontweight='bold', color='#111111', zorder=5)

    ax_main.plot([sun_x, cx], [sun_y, cy], color='#5d6d7e', ls=':', lw=1.4, zorder=3)
    vec_to_sun = np.array([sun_x - cx, sun_y - cy])
    dist_vis = np.linalg.norm(vec_to_sun)
    if dist_vis > 0.3:
        u_sun = vec_to_sun / dist_vis
        ax_main.annotate('', xy=(cx + u_sun[0]*0.65, cy + u_sun[1]*0.65), xytext=(cx, cy),
                         arrowprops=dict(arrowstyle='-|>', color='#d32f2f', lw=2.0, mutation_scale=12), zorder=6)

    u_away = -vec_to_sun / max(dist_vis, 0.1)
    u_perp = np.array([-u_away[1], u_away[0]])
    tail_len = 0.55
    tail_poly = patches.Polygon([
        [cx, cy],
        [cx + u_away[0]*tail_len + u_perp[0]*0.12, cy + u_away[1]*tail_len + u_perp[1]*0.12],
        [cx + u_away[0]*tail_len*0.85, cy + u_away[1]*tail_len*0.85],
        [cx + u_away[0]*tail_len - u_perp[0]*0.12, cy + u_away[1]*tail_len - u_perp[1]*0.12]
    ], facecolor='#ffffff', edgecolor='#74c0fc', lw=1.0, alpha=0.9, zorder=5)
    ax_main.add_patch(tail_poly)
    comet_head = patches.Circle((cx, cy), 0.11, facecolor='#1971c2', edgecolor='#ffffff', lw=1.5, zorder=6)
    ax_main.add_patch(comet_head)

    tx = -a_vis * np.sin(ang)
    ty = b_vis * np.cos(ang)
    t_norm = np.hypot(tx, ty)
    v_scale = 0.45 + 0.55 * (1.0 - w_factor)
    vx_draw = (tx / t_norm) * v_scale
    vy_draw = (ty / t_norm) * v_scale
    ax_main.annotate('', xy=(cx + vx_draw, cy + vy_draw), xytext=(cx, cy),
                     arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.4, mutation_scale=14), zorder=7)
    lbl_x = np.clip(cx + vx_draw*1.05, -3.9, 3.9)
    lbl_y = cy + vy_draw*1.05 + (0.24 if cy >= 0 else -0.34)
    ax_main.text(lbl_x, lbl_y, rf'$v = {v_curr:,.0f}\ \mathrm{{m/s}}$',
                 color='#2e7d32', fontsize=9.8, fontweight='bold', ha='center', zorder=8)

    y_dim = -2.45
    ax_main.plot([-a_vis, -a_vis], [0, y_dim - 0.15], color='#444444', lw=1.0)
    ax_main.plot([sun_x, sun_x], [0, y_dim - 0.15], color='#444444', lw=1.0)
    ax_main.plot([a_vis, a_vis], [0, y_dim - 0.15], color='#444444', lw=1.0)

    ax_main.annotate('', xy=(sun_x, y_dim), xytext=(a_vis, y_dim),
                     arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.3))
    ax_main.text((sun_x + a_vis)/2, y_dim, r'$6000(10^6)\ \mathrm{km}$', ha='center', va='center',
                 fontsize=10, fontweight='bold', bbox=dict(boxstyle='square,pad=0.15', facecolor='#ffffff', edgecolor='none'))

    ax_main.annotate('', xy=(-a_vis, y_dim), xytext=(sun_x, y_dim),
                     arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.3))
    ax_main.text(-3.65, -2.95, r'$75(10^6)\ \mathrm{km}$', ha='center', fontsize=10, fontweight='bold')
    ax_main.text(2.8, -2.95, '(일정한 비율이 아님)', ha='center', fontsize=9.5, color='#555555')

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('중심력장 각운동량 보존 및 정량 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_card = (
        "【중심력장(Central Force) 각운동량 보존 원리】\n"
        r"• 태양 만유인력 $\mathbf{F}_g$는 항상 중심점 $O$를 향함 ($\mathbf{r} \parallel \mathbf{F}_g$)" + "\n"
        r"• 원점 $O$에 대한 모멘트: $\Sigma\mathbf{M}_O = \mathbf{r} \times \mathbf{F}_g = \mathbf{0}$" + "\n"
        r"• 따라서 궤도 전 구간에서 $(H_O)_A = (H_O)_B = \mathrm{const}$"
    )
    ax_calc.text(0.35, 8.45, top_card, fontsize=9.8, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (Section 3.10)】\n"
        r"1) 원일점 $A$와 근일점 $B$에서의 각운동량 보존:" + "\n"
        r"   $(H_O)_A = (H_O)_B \;\Rightarrow\; m r_A v_A = m r_B v_B$" + "\n\n"
        r"2) 근일점(최근접점) $B$에서의 혜성 속력 $v_B$:" + "\n"
        r"   $v_B = \frac{r_A v_A}{r_B} = \frac{6000(10^6)\ \mathrm{km} \times 740\ \mathrm{m/s}}{75(10^6)\ \mathrm{km}}$" + "\n"
        r"   $v_B = 80 \times 740 = \mathbf{59,200\ \mathrm{m/s}\ (59.2\ \mathrm{km/s})}$"
    )
    ax_calc.text(0.35, 4.95, sol_text, fontsize=9.8, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        "【실시간 궤도 위치 및 비각운동량 모니터】\n"
        rf"• 태양 중심 거리: $r = {r_curr:,.1f} \times 10^6\ \mathrm{{km}}$" + "\n"
        rf"• 현재 혜성 속력: $v = {v_curr:,.0f}\ \mathrm{{m/s}}\ ({v_curr/1000:.2f}\ \mathrm{{km/s}})$" + "\n"
        r"• 비각운동량 보존: $H_O / m = r_A v_A = 4.44 \times 10^{15}\ \mathrm{m^2/s}$ (일정)" + "\n"
        r"• 이론 최종값: 원일점 $v_A = 740\ \mathrm{m/s} \;\Rightarrow\;$ 근일점 $v_B = 59,200\ \mathrm{m/s}$"
    )
    ax_calc.text(0.35, 1.45, live_text, fontsize=9.4, va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_25_comet_elliptical_orbit.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
