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

# Physical parameters (Meriam Dynamics 9th Ed. Sample Problem 2.13)
vA_val = 800.0 # km/h
vB_val = vA_val * np.sin(np.radians(60.0)) / np.sin(np.radians(75.0))   # 717.17 km/h
vBA_val = vA_val * np.sin(np.radians(45.0)) / np.sin(np.radians(75.0)) # 585.64 km/h

vA_ms = vA_val / 3.6
vB_ms = vB_val / 3.6
vBA_ms = vBA_val / 3.6

fps = 30
duration = 3.5
n_frames = int(fps * duration)
t_eval = np.linspace(0, duration, n_frames)

posA0 = np.array([400.0, 300.0])
posB0 = np.array([1200.0, 1100.0])

def draw_airliner_A(ax, x, y, angle_deg=0.0, scale=1.0):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    def rot(dx, dy):
        return x + dx*c - dy*s, y + dx*s + dy*c
    
    fx = np.array([-180, -140, 140, 190, 210, 190, 140, -140, -180, -190, -180]) * scale
    fy = np.array([ -15,  -18, -18, -10,   0,  10,  18,   18,   15,    0,  -15]) * scale
    px, py = rot(fx, fy)
    ax.fill(px, py, color='#fb923c', ec='#c2410c', lw=1.8, zorder=5)
    
    cx = np.array([160, 185, 185, 160]) * scale
    cy = np.array([  5,   3,  -3,  -5]) * scale
    cpx, cpy = rot(cx, cy)
    ax.fill(cpx, cpy, color='#0f172a', zorder=6)
    
    wx = np.array([ 20, -60, -90, -30,  50]) * scale
    wy_top = np.array([ 16, 170, 170,  18,  18]) * scale
    wy_bot = -wy_top
    wpx_t, wpy_t = rot(wx, wy_top)
    wpx_b, wpy_b = rot(wx, wy_bot)
    ax.fill(wpx_t, wpy_t, color='#f97316', ec='#9a3412', lw=1.8, zorder=4)
    ax.fill(wpx_b, wpy_b, color='#f97316', ec='#9a3412', lw=1.8, zorder=4)
    
    for eng_y in [70, -70]:
        ex = np.array([20, -40, -40, 20]) * scale
        ey = np.array([eng_y-10, eng_y-10, eng_y+10, eng_y+10]) * scale
        epx, epy = rot(ex, ey)
        ax.fill(epx, epy, color='#475569', ec='#1e293b', lw=1.2, zorder=6)
    
    tx = np.array([-140, -190, -205, -170]) * scale
    ty_top = np.array([ 10,  70,  70,  10]) * scale
    ty_bot = -ty_top
    tpx_t, tpy_t = rot(tx, ty_top)
    tpx_b, tpy_b = rot(tx, ty_bot)
    ax.fill(tpx_t, tpy_t, color='#f97316', ec='#9a3412', lw=1.5, zorder=4)
    ax.fill(tpx_b, tpy_b, color='#f97316', ec='#9a3412', lw=1.5, zorder=4)

def draw_aircraft_B(ax, x, y, angle_deg=45.0, scale=0.85, is_ghost=False):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    def rot(dx, dy):
        return x + dx*c - dy*s, y + dx*s + dy*c
    
    fill_col = '#e0f2fe' if is_ghost else '#38bdf8'
    edge_col = '#0284c7' if is_ghost else '#0369a1'
    alpha_val = 0.55 if is_ghost else 1.0
    ls = '--' if is_ghost else '-'
    
    fx = np.array([-150, -110, 110, 160, 180, 160, 110, -110, -150, -160, -150]) * scale
    fy = np.array([ -14,  -16, -16,  -8,   0,   8,  16,   16,   14,    0,  -14]) * scale
    px, py = rot(fx, fy)
    ax.fill(px, py, color=fill_col, ec=edge_col, lw=1.6, ls=ls, alpha=alpha_val, zorder=5)
    
    if not is_ghost:
        cx = np.array([130, 155, 155, 130]) * scale
        cy = np.array([  4,   2,  -2,  -4]) * scale
        cpx, cpy = rot(cx, cy)
        ax.fill(cpx, cpy, color='#0f172a', zorder=6)
    
    wx = np.array([ 15, -45, -70, -20,  40]) * scale
    wy_top = np.array([ 14, 135, 135,  16,  16]) * scale
    wy_bot = -wy_top
    wpx_t, wpy_t = rot(wx, wy_top)
    wpx_b, wpy_b = rot(wx, wy_bot)
    ax.fill(wpx_t, wpy_t, color=fill_col, ec=edge_col, lw=1.6, ls=ls, alpha=alpha_val, zorder=4)
    ax.fill(wpx_b, wpy_b, color=fill_col, ec=edge_col, lw=1.6, ls=ls, alpha=alpha_val, zorder=4)
    
    tx = np.array([-115, -155, -170, -140]) * scale
    ty_top = np.array([  8,  55,  55,   8]) * scale
    ty_bot = -ty_top
    tpx_t, tpy_t = rot(tx, ty_top)
    tpx_b, tpy_b = rot(tx, ty_bot)
    ax.fill(tpx_t, tpy_t, color=fill_col, ec=edge_col, lw=1.4, ls=ls, alpha=alpha_val, zorder=4)
    ax.fill(tpx_b, tpy_b, color=fill_col, ec=edge_col, lw=1.4, ls=ls, alpha=alpha_val, zorder=4)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

def update(frame):
    t = t_eval[frame]
    sim_scale = 0.5
    posA = posA0 + np.array([vA_ms * sim_scale * t, 0.0])
    vB_vec = np.array([vB_ms * np.cos(np.radians(45.0)), vB_ms * np.sin(np.radians(45.0))])
    posB = posB0 + vB_vec * sim_scale * t
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-100, 2400)
    ax.set_ylim(-150, 1850)
    ax.axis('off')
    
    ax.plot([posA[0] - 300, posA[0] + 650], [posA[1], posA[1]], color='#64748b', linestyle='--', lw=1.5, zorder=2)
    ax.text(posA[0] + 680, posA[1] - 15, '$x$', fontsize=14, fontweight='bold', color='#334155')
    ax.plot([posA[0], posA[0]], [posA[1] - 150, posA[1] + 650], color='#64748b', linestyle='--', lw=1.5, zorder=2)
    ax.text(posA[0] - 10, posA[1] + 680, '$y$', fontsize=14, fontweight='bold', color='#334155')
    
    arrow_vA_len = 380
    ax.quiver(posA[0], posA[1], arrow_vA_len, 0, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.007, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(posA[0] + arrow_vA_len * 0.5, posA[1] - 55, '$v_A = 800\\text{ km/h}$', fontsize=11.5, fontweight='bold', color='#16a34a')
    
    ax.plot([posA[0], posB[0]], [posA[1], posB[1]], color='#94a3b8', linestyle=':', lw=1.8, zorder=2)
    ax.plot([posB[0] - 550, posB[0] + 250], [posB[1], posB[1]], color='#94a3b8', linestyle='--', lw=1.3, zorder=2)
    
    base_x, base_y = posB[0] - 450, posB[1] - 450
    ax.plot([base_x - 100, posB[0] + 400], [base_y - 100, posB[1] + 400], color='#0284c7', linestyle='--', lw=1.4, zorder=2)
    
    arc_ang45 = np.linspace(0, np.radians(45.0), 25)
    arc_r45 = 140
    ax.plot(base_x + arc_r45 * np.cos(arc_ang45), base_y + arc_r45 * np.sin(arc_ang45), color='#0284c7', lw=1.6, zorder=3)
    ax.text(base_x + arc_r45 * 1.25, base_y + arc_r45 * 0.45, '$45^\\circ$', fontsize=12, fontweight='bold', color='#0284c7')
    
    arrow_vB_len = 340
    ax.quiver(posB[0], posB[1], arrow_vB_len * np.cos(np.radians(45.0)), arrow_vB_len * np.sin(np.radians(45.0)),
              angles='xy', scale_units='xy', scale=1, color='#16a34a', width=0.007, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(posB[0] + arrow_vB_len * 0.45, posB[1] + arrow_vB_len * 0.75 + 15, '$v_B = 717.2\\text{ km/h}$',
            fontsize=11.5, fontweight='bold', color='#16a34a')
    
    ghost_offset = np.array([-220.0 * np.cos(np.radians(60.0)), 220.0 * np.sin(np.radians(60.0))])
    posB_ghost = posB + ghost_offset
    
    ax.plot([posB[0], posB[0] - 400 * np.cos(np.radians(60.0))],
            [posB[1], posB[1] + 400 * np.sin(np.radians(60.0))],
            color='#0ea5e9', linestyle='--', lw=1.6, zorder=2)
    
    arc_ang60 = np.linspace(np.pi - np.radians(60.0), np.pi, 25)
    arc_r60 = 130
    ax.plot(posB[0] + arc_r60 * np.cos(arc_ang60), posB[1] + arc_r60 * np.sin(arc_ang60), color='#0ea5e9', lw=1.6, zorder=3)
    ax.text(posB[0] - arc_r60 * 1.45, posB[1] + arc_r60 * 0.55, '$60^\\circ$', fontsize=12, fontweight='bold', color='#0ea5e9')
    
    arrow_vBA_len = 280
    ax.quiver(posB[0], posB[1], -arrow_vBA_len * np.cos(np.radians(60.0)), arrow_vBA_len * np.sin(np.radians(60.0)),
              angles='xy', scale_units='xy', scale=1, color='#16a34a', width=0.007, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(posB[0] - arrow_vBA_len * 0.85 - 80, posB[1] + arrow_vBA_len * 0.85 + 20, '$v_{B/A} = 585.6\\text{ km/h}$',
            fontsize=11.5, fontweight='bold', color='#16a34a')
    
    draw_aircraft_B(ax, posB_ghost[0], posB_ghost[1], angle_deg=120.0, scale=0.8, is_ghost=True)
    draw_aircraft_B(ax, posB[0], posB[1], angle_deg=45.0, scale=0.85, is_ghost=False)
    ax.scatter([posB[0]], [posB[1]], color='#0f172a', s=35, zorder=7)
    ax.text(posB[0] + 75, posB[1] - 40, '$B$', fontsize=14, fontweight='bold', color='#0369a1')
    
    draw_airliner_A(ax, posA[0], posA[1], angle_deg=0.0, scale=1.0)
    ax.scatter([posA[0]], [posA[1]], color='#0f172a', s=45, zorder=7)
    ax.text(posA[0] + 50, posA[1] + 45, '$A$', fontsize=15, fontweight='bold', color='#c2410c')
    
    # Inset Vector Triangle
    tri_x0, tri_y0 = 1750, 250
    t_scale = 0.55
    vA_dx = vA_val * t_scale
    vBA_dx = -vBA_val * np.cos(np.radians(60.0)) * t_scale
    vBA_dy = vBA_val * np.sin(np.radians(60.0)) * t_scale
    vB_dx = vB_val * np.cos(np.radians(45.0)) * t_scale
    vB_dy = vB_val * np.sin(np.radians(45.0)) * t_scale
    
    tri_box = patches.FancyBboxPatch((tri_x0 - 50, tri_y0 - 80), 620, 520,
                                     boxstyle="round,pad=15", fc="#ffffff", ec="#0284c7", lw=1.5, alpha=0.92, zorder=9)
    ax.add_patch(tri_box)
    box_title = '상대속도 벡터 삼각형' if 'en' == 'ko' else 'Velocity Triangle'
    ax.text(tri_x0 + 130, tri_y0 + 380, f'[{box_title}]\n$\\mathbf{v}_B = \\mathbf{v}_A + \\mathbf{v}_{B/A}$',
            fontsize=10.5, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    ax.annotate('', xy=(tri_x0 + vA_dx, tri_y0), xytext=(tri_x0, tri_y0),
                arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.5, mutation_scale=15), zorder=10)
    ax.text(tri_x0 + vA_dx*0.5, tri_y0 - 35, '$\\mathbf{v}_A$', fontsize=11, fontweight='bold', color='#ea580c', ha='center', zorder=10)
    
    ax.annotate('', xy=(tri_x0 + vA_dx + vBA_dx, tri_y0 + vBA_dy), xytext=(tri_x0 + vA_dx, tri_y0),
                arrowprops=dict(arrowstyle="-|>", color='#0ea5e9', lw=2.5, mutation_scale=15), zorder=10)
    ax.text(tri_x0 + vA_dx + vBA_dx*0.5 + 25, tri_y0 + vBA_dy*0.5 + 15, '$\\mathbf{v}_{B/A}$',
            fontsize=11, fontweight='bold', color='#0ea5e9', zorder=10)
    
    ax.annotate('', xy=(tri_x0 + vB_dx, tri_y0 + vB_dy), xytext=(tri_x0, tri_y0),
                arrowprops=dict(arrowstyle="-|>", color='#16a34a', lw=2.5, mutation_scale=15), zorder=10)
    ax.text(tri_x0 + vB_dx*0.4 - 30, tri_y0 + vB_dy*0.5 + 15, '$\\mathbf{v}_B$', fontsize=11, fontweight='bold', color='#16a34a', zorder=10)
    
    sine_str = '사인법칙 (Law of Sines):\n$\\frac{v_B}{\\sin 60^\\circ} = \\frac{v_A}{\\sin 75^\\circ} = \\frac{v_{B/A}}{\\sin 45^\\circ}$'
    ax.text(tri_x0 + 130, tri_y0 - 45, sine_str, fontsize=9.5, color='#334155', ha='center', zorder=10)
    
    if 'en' == 'ko':
        hud_str = (
            f"[예제 2.13 2차원 상대속도 해석]\n"
            f"시간 t = {t:3.1f} s / {duration:3.1f} s\n"
            f"----------------------------------------\n"
            f"여객기 A:  v_A   = {vA_val:5.1f} km/h (동향, 0°)\n"
            f"항공기 B:  v_B   = {vB_val:5.1f} km/h (북동, 45°)\n"
            f"상대속도: v_B/A = {vBA_val:5.1f} km/h (북서, 60°)\n"
            f"----------------------------------------\n"
            f"▶ 구하는 값: 항공기 B 실제 속도 v_B\n"
            f"  v_B = 800 · sin(60°) / sin(75°) = 717.2 km/h"
        )
        title_text = '[동역학 9판 예제 2.13] 제트여객기-항공기 2차원 상대속도 벡터 해석'
    else:
        hud_str = (
            f"[Sample Prob. 2.13 Relative Velocity]\n"
            f"Time t = {t:3.1f} s / {duration:3.1f} s\n"
            f"----------------------------------------\n"
            f"Airliner A: v_A   = {vA_val:5.1f} km/h (East, 0°)\n"
            f"Aircraft B: v_B   = {vB_val:5.1f} km/h (NE, 45°)\n"
            f"Relative:   v_B/A = {vBA_val:5.1f} km/h (NW, 60°)\n"
            f"----------------------------------------\n"
            f"▶ Target: Actual Speed of Aircraft B\n"
            f"  v_B = 800 · sin(60°) / sin(75°) = 717.2 km/h"
        )
        title_text = '[Meriam Dynamics 9th Ed. Ex 2.13] Relative Velocity of Two Airplanes'
    
    ax.text(0.02, 0.96, hud_str, transform=ax.transAxes, fontsize=10, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.55', facecolor='#ffffff', edgecolor='#ea580c', lw=1.5, alpha=0.94))
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=4, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'ex2_13_plane_crosswind.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
