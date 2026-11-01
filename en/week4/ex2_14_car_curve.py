# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

# Font configuration
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

R_curve = 150.0
vA0 = 20.0
aA_val = 1.2
vB_val = 15.0
anB_val = (vB_val**2) / R_curve

fps = 30
duration = 3.5
n_frames = int(fps * duration)
t_eval = np.linspace(-1.5, 1.5, n_frames)

def draw_car(ax, x, y, angle_deg, color='#ef4444', edge_col='#991b1b', scale=1.0, is_car_A=True):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    def rot(dx, dy):
        return x + dx*c - dy*s, y + dx*s + dy*c
    
    L, W = 18.0 * scale, 9.0 * scale
    bx = np.array([-L/2, L/2 - 2, L/2, L/2 - 2, -L/2, -L/2])
    by = np.array([-W/2, -W/2, 0, W/2, W/2, -W/2])
    px, py = rot(bx, by)
    ax.fill(px, py, color=color, ec=edge_col, lw=1.8, zorder=6)
    
    rx = np.array([-L/4, L/4, L/4 - 1, -L/4 + 1])
    ry = np.array([-W/2.8, -W/2.8, W/2.8, W/2.8])
    rpx, rpy = rot(rx, ry)
    ax.fill(rpx, rpy, color='#1e293b', alpha=0.7, zorder=7)
    
    wx = np.array([L/4, L/4 + 2, L/4 + 2, L/4])
    wy = np.array([-W/3, -W/3.5, W/3.5, W/3])
    wpx, wpy = rot(wx, wy)
    ax.fill(wpx, wpy, color='#94a3b8', zorder=8)
    
    hx = np.array([L/2 - 1, L/2 - 1])
    for hy in [-W/2.5, W/2.5]:
        hpx, hpy = rot(hx[0], hy)
        ax.plot([hpx], [hpy], 'o', color='#fef08a', markersize=3.5, zorder=8)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])
y_road_A = 70.0

def update(frame):
    t = t_eval[frame]
    xA = 0.0 - (vA0 * t + 0.5 * aA_val * t**2)
    yA = y_road_A
    vA_t = vA0 + aA_val * t
    
    theta_B_rad = np.radians(-30.0) - (vB_val * t) / R_curve
    theta_B_deg = np.degrees(theta_B_rad)
    xB = R_curve * np.cos(theta_B_rad)
    yB = R_curve * np.sin(theta_B_rad)
    heading_B_deg = theta_B_deg - 90.0
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-140, 240)
    ax.set_ylim(-165, 115)
    ax.axis('off')
    
    bg_rect = patches.Rectangle((-140, -165), 380, 280, color='#e2e8f0', zorder=1)
    ax.add_patch(bg_rect)
    
    road_A = patches.Rectangle((-140, 52), 380, 36, color='#cbd5e1', zorder=2)
    ax.add_patch(road_A)
    ax.plot([-140, 240], [70, 70], color='#ffffff', linestyle='--', lw=1.6, zorder=3)
    ax.plot([-140, 240], [52, 52], color='#94a3b8', lw=2.0, zorder=3)
    ax.plot([-140, 240], [88, 88], color='#94a3b8', lw=2.0, zorder=3)
    
    road_V = patches.Rectangle((132, -165), 36, 280, color='#cbd5e1', zorder=2)
    ax.add_patch(road_V)
    ax.plot([150, 150], [-165, 115], color='#ffffff', linestyle='--', lw=1.6, zorder=3)
    ax.plot([132, 132], [-165, 52], color='#94a3b8', lw=2.0, zorder=3)
    ax.plot([168, 168], [-165, 52], color='#94a3b8', lw=2.0, zorder=3)
    
    th_arc = np.linspace(-np.pi/2, 0, 80)
    inner_arc_x, inner_arc_y = 132 * np.cos(th_arc), 132 * np.sin(th_arc)
    outer_arc_x, outer_arc_y = 168 * np.cos(th_arc), 168 * np.sin(th_arc)
    curve_poly = patches.Polygon(np.column_stack([
        np.concatenate([inner_arc_x, outer_arc_x[::-1]]),
        np.concatenate([inner_arc_y, outer_arc_y[::-1]])
    ]), color='#cbd5e1', ec='#94a3b8', lw=2.0, zorder=2)
    ax.add_patch(curve_poly)
    mid_arc_x, mid_arc_y = 150 * np.cos(th_arc), 150 * np.sin(th_arc)
    ax.plot(mid_arc_x, mid_arc_y, color='#ffffff', linestyle='--', lw=1.6, zorder=3)
    
    for arrow_x in [-70, 40, 110]:
        ax.annotate('', xy=(arrow_x - 18, 70), xytext=(arrow_x + 18, 70),
                    arrowprops=dict(arrowstyle="-|>", color='#f97316', lw=2.2, mutation_scale=14), zorder=4)
    for ang_arr in [-15, -45, -75]:
        rad_arr = np.radians(ang_arr)
        ax_x, ax_y = 150 * np.cos(rad_arr), 150 * np.sin(rad_arr)
        tang_x, tang_y = -np.sin(rad_arr) * 18, -np.cos(rad_arr) * 18
        ax.annotate('', xy=(ax_x + tang_x, ax_y + tang_y), xytext=(ax_x - tang_x, ax_y - tang_y),
                    arrowprops=dict(arrowstyle="-|>", color='#f97316', lw=2.2, mutation_scale=14), zorder=4)
    
    ax.plot([0, 0], [-6, 6], color='#0f172a', lw=2.0, zorder=5)
    ax.plot([-6, 6], [0, 0], color='#0f172a', lw=2.0, zorder=5)
    ax.text(-14, -14, '$C$', fontsize=13, fontweight='bold', color='#0f172a')
    ax.plot([-30, 150], [0, 0], color='#64748b', linestyle='-.', lw=1.5, zorder=4)
    ax.plot([0, xB], [0, yB], color='#0f172a', linestyle='-', lw=1.8, zorder=4)
    ax.text(xB * 0.45 + 5, yB * 0.45 + 6, '150 m', fontsize=11, fontweight='bold', color='#0f172a')
    
    norm_extend_x = [xB - 40 * np.cos(theta_B_rad), xB + 40 * np.cos(theta_B_rad)]
    norm_extend_y = [yB - 40 * np.sin(theta_B_rad), yB + 40 * np.sin(theta_B_rad)]
    ax.plot(norm_extend_x, norm_extend_y, color='#0284c7', linestyle='--', lw=1.4, zorder=4)
    ax.text(xB + 42 * np.cos(theta_B_rad), yB + 42 * np.sin(theta_B_rad) - 5, '$n$',
            fontsize=13, fontweight='bold', color='#0284c7')
    
    arc_ang30 = np.linspace(np.radians(-30.0), 0, 20)
    ax.plot(40 * np.cos(arc_ang30), 40 * np.sin(arc_ang30), color='#0f172a', lw=1.5, zorder=5)
    ax.text(48, -12, '$30^\\circ$', fontsize=11.5, fontweight='bold', color='#0f172a')
    
    ax.plot([xA - 65, xA + 55], [yA, yA], color='#b91c1c', linestyle='--', lw=1.5, zorder=5)
    ax.text(xA - 75, yA - 4, '$x$', fontsize=13, fontweight='bold', color='#b91c1c')
    ax.plot([xA, xA], [yA - 20, yA + 35], color='#b91c1c', linestyle='--', lw=1.5, zorder=5)
    ax.text(xA - 3, yA + 38, '$y$', fontsize=13, fontweight='bold', color='#b91c1c')
    
    ax.quiver(xA, yA, -35, 0, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.008, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xA - 42, yA + 8, '$\\mathbf{v}_A$', fontsize=11, fontweight='bold', color='#16a34a')
    
    ax.quiver(xA, yA - 6, -28, 0, angles='xy', scale_units='xy', scale=1,
              color='#ea580c', width=0.008, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xA - 36, yA - 18, '$\\mathbf{a}_A$', fontsize=11, fontweight='bold', color='#ea580c')
    
    tan_bx, tan_by = np.cos(np.radians(heading_B_deg)), np.sin(np.radians(heading_B_deg))
    ax.quiver(xB, yB, tan_bx * 32, tan_by * 32, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.008, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xB + tan_bx * 35 - 5, yB + tan_by * 35 - 8, '$\\mathbf{v}_B$', fontsize=11, fontweight='bold', color='#16a34a')
    
    an_bx, an_by = -np.cos(theta_B_rad), -np.sin(theta_B_rad)
    ax.quiver(xB, yB, an_bx * 26, an_by * 26, angles='xy', scale_units='xy', scale=1,
              color='#ea580c', width=0.008, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xB + an_bx * 30 - 15, yB + an_by * 30 + 5, '$\\mathbf{a}_n$', fontsize=11, fontweight='bold', color='#ea580c')
    
    ax.plot([xA, xB], [yA, yB], color='#94a3b8', linestyle=':', lw=1.8, zorder=4)
    
    draw_car(ax, xA, yA, angle_deg=180.0, color='#ef4444', edge_col='#991b1b', scale=1.0, is_car_A=True)
    ax.text(xA, yA - 16, '$A$', fontsize=13, fontweight='bold', color='#991b1b', ha='center', zorder=9)
    draw_car(ax, xB, yB, angle_deg=heading_B_deg, color='#38bdf8', edge_col='#0284c7', scale=1.0, is_car_A=False)
    ax.text(xB + 16, yB - 6, '$B$', fontsize=13, fontweight='bold', color='#0284c7', zorder=9)
    
    if 'en' == 'ko':
        hud_str = (
            f"[예제 2.14 커브길 상대운동 해석]\n"
            f"시간 t = {t:4.2f} s / 1.50 s\n"
            f"자동차 A (직선): v_A = {vA_t:4.1f} m/s, a_A = {aA_val:4.1f} m/s²\n"
            f"자동차 B (곡선): v_B = {vB_val:4.1f} m/s, a_n = {anB_val:4.2f} m/s²"
        )
        title_text = '[동역학 9판 예제 2.14] 직선 가속 자동차-커브길 자동차 상대속도 및 상대가속도'
    else:
        hud_str = (
            f"[Sample Prob. 2.14 Relative Motion]\n"
            f"Time t = {t:4.2f} s / 1.50 s\n"
            f"Car A (Straight): v_A = {vA_t:4.1f} m/s, a_A = {aA_val:4.1f} m/s²\n"
            f"Car B (Curve):    v_B = {vB_val:4.1f} m/s, a_n = {anB_val:4.2f} m/s²"
        )
        title_text = '[Meriam Dynamics 9th Ed. Ex 2.14] Relative Velocity & Acceleration of Cars'
    
    ax.text(0.02, 0.74, hud_str, transform=ax.transAxes, fontsize=9.0, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.45', facecolor='#ffffff', edgecolor='#ef4444', lw=1.4, alpha=0.94))
    
    tri_x0, tri_y0 = -136, -105
    box_w, box_h = 126, 92
    tri_box = patches.FancyBboxPatch((tri_x0, tri_y0), box_w, box_h,
                                     boxstyle="round,pad=4", fc="#ffffff", ec="#0284c7", lw=1.4, alpha=0.94, zorder=9)
    ax.add_patch(tri_box)
    inset_title = '상대속도/가속도 벡터 풀이' if 'en' == 'ko' else 'Relative Vectors Solution'
    ax.text(tri_x0 + box_w*0.5, tri_y0 + box_h - 9, f'[{inset_title}]',
            fontsize=9.0, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    v_eq = '$\\mathbf{v}_{B/A} = \\mathbf{v}_B - \\mathbf{v}_A = -12.5\\mathbf{i} - 13.0\\mathbf{j}$'
    v_ans = '$|\\mathbf{v}_{B/A}| = 18.03\\text{ m/s } (64.9\\text{ km/h})$'
    a_eq = '$\\mathbf{a}_{B/A} = \\mathbf{a}_B - \\mathbf{a}_A = 0.10\\mathbf{i} + 0.75\\mathbf{j}$'
    a_ans = '$|\\mathbf{a}_{B/A}| = 0.756\\text{ m/s}^2$'
    
    ax.text(tri_x0 + 6, tri_y0 + box_h - 25, v_eq, fontsize=8.0, color='#1e293b', zorder=10)
    ax.text(tri_x0 + 6, tri_y0 + box_h - 41, f'▶ {v_ans}', fontsize=8.2, fontweight='bold', color='#16a34a', zorder=10)
    ax.text(tri_x0 + 6, tri_y0 + box_h - 60, a_eq, fontsize=8.0, color='#1e293b', zorder=10)
    ax.text(tri_x0 + 6, tri_y0 + box_h - 76, f'▶ {a_ans}', fontsize=8.2, fontweight='bold', color='#ea580c', zorder=10)
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=4, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'ex2_14_car_curve.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
