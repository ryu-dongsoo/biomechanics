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

L_cable = 1.30
vA_val = 0.25
x_start = 0.25
x_end = 0.95
duration = 3.5
fps = 30
n_frames = int(fps * duration)
t_eval = np.linspace(0, duration, n_frames)

def draw_collar(ax, center_x, center_y, angle_deg=0.0, label='A', scale=1.0):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    def rot(dx, dy):
        return center_x + dx*c - dy*s, center_y + dx*s + dy*c
    
    L_c, W_c = 0.16 * scale, 0.09 * scale
    bx = np.array([-L_c/2, L_c/2, L_c/2, -L_c/2])
    by = np.array([-W_c/2, -W_c/2, W_c/2, W_c/2])
    px, py = rot(bx, by)
    ax.fill(px, py, fc='#fdba74', ec='#c2410c', lw=1.8, zorder=6)
    
    bx_in = np.array([-L_c/2, L_c/2])
    for by_in in [-W_c/4, W_c/4]:
        ipx, ipy = rot(bx_in, by_in)
        ax.plot(ipx, ipy, color='#c2410c', linestyle='--', lw=1.0, zorder=7)
    
    pin_px, pin_py = rot(0, 0)
    ax.scatter([pin_px], [pin_py], color='#0f172a', s=35, zorder=8)
    
    lbl_off_x, lbl_off_y = rot(0, W_c * 0.85)
    ax.text(lbl_off_x, lbl_off_y, f'${label}$', fontsize=13, fontweight='bold', color='#c2410c',
            ha='center', va='center', zorder=9)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

def update(frame):
    t = t_eval[frame]
    x_val = x_start + ((x_end - x_start) / duration) * t
    s_val = - (np.sqrt(2.0) / 2.0) * x_val + np.sqrt(L_cable**2 - 0.5 * (x_val**2))
    
    posA = np.array([x_val, 0.0])
    posB = np.array([-s_val * np.cos(np.radians(45.0)), s_val * np.sin(np.radians(45.0))])
    vB_val = ((2.0 * x_val + np.sqrt(2.0) * s_val) / (2.0 * s_val + np.sqrt(2.0) * x_val)) * vA_val
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-1.15, 1.45)
    ax.set_ylim(-0.35, 1.35)
    ax.axis('off')
    
    bg_rect = patches.Rectangle((-1.15, -0.35), 2.60, 1.70, color='#f8fafc', zorder=1)
    ax.add_patch(bg_rect)
    
    base_mount = patches.Rectangle((-0.12, -0.16), 0.28, 0.16, color='#cbd5e1', ec='#64748b', lw=1.5, zorder=2)
    ax.add_patch(base_mount)
    ax.plot([-0.18, 0.20], [-0.16, -0.16], color='#475569', lw=2.0, zorder=3)
    for hx in np.linspace(-0.16, 0.16, 8):
        ax.plot([hx, hx + 0.05], [-0.23, -0.16], color='#94a3b8', lw=1.2, zorder=2)
    
    wall_h = patches.Rectangle((1.25, -0.12), 0.12, 0.24, color='#cbd5e1', ec='#64748b', lw=1.5, zorder=2)
    ax.add_patch(wall_h)
    for wy in np.linspace(-0.10, 0.10, 5):
        ax.plot([1.37, 1.42], [wy, wy + 0.04], color='#94a3b8', lw=1.2, zorder=2)
    
    wx_c, wy_c = -0.92, 0.92
    wall_inc = patches.Polygon([
        (wx_c - 0.08*np.cos(np.pi/4) - 0.08*np.sin(np.pi/4), wy_c + 0.08*np.sin(np.pi/4) - 0.08*np.cos(np.pi/4)),
        (wx_c + 0.08*np.cos(np.pi/4) - 0.08*np.sin(np.pi/4), wy_c - 0.08*np.sin(np.pi/4) - 0.08*np.cos(np.pi/4)),
        (wx_c + 0.08*np.cos(np.pi/4) + 0.08*np.sin(np.pi/4), wy_c - 0.08*np.sin(np.pi/4) + 0.08*np.cos(np.pi/4)),
        (wx_c - 0.08*np.cos(np.pi/4) + 0.08*np.sin(np.pi/4), wy_c + 0.08*np.sin(np.pi/4) + 0.08*np.cos(np.pi/4))
    ], color='#cbd5e1', ec='#64748b', lw=1.5, zorder=2)
    ax.add_patch(wall_inc)
    
    rod_H = patches.Rectangle((0.0, -0.022), 1.25, 0.044, color='#94a3b8', ec='#475569', lw=1.4, zorder=4)
    ax.add_patch(rod_H)
    ax.plot([0.0, 1.25], [0, 0], color='#cbd5e1', lw=1.0, zorder=5)
    
    inc_len = 1.30
    inc_poly = patches.Polygon([
        (0.022*np.sin(np.pi/4), 0.022*np.cos(np.pi/4)),
        (-inc_len*np.cos(np.pi/4) + 0.022*np.sin(np.pi/4), inc_len*np.sin(np.pi/4) + 0.022*np.cos(np.pi/4)),
        (-inc_len*np.cos(np.pi/4) - 0.022*np.sin(np.pi/4), inc_len*np.sin(np.pi/4) - 0.022*np.cos(np.pi/4)),
        (-0.022*np.sin(np.pi/4), -0.022*np.cos(np.pi/4))
    ], color='#94a3b8', ec='#475569', lw=1.4, zorder=4)
    ax.add_patch(inc_poly)
    
    junction_box = patches.Polygon([
        (-0.08, -0.08), (0.12, -0.08), (0.12, 0.05), (0.02, 0.05),
        (-0.05, 0.12), (-0.12, 0.05), (-0.08, -0.08)
    ], fc='#64748b', ec='#334155', lw=1.6, zorder=5)
    ax.add_patch(junction_box)
    ax.scatter([0], [0], color='#0f172a', s=25, zorder=6)
    
    cable_color = '#1e293b'
    ax.plot([posB[0], posA[0]], [posB[1], posA[1]], color=cable_color, lw=2.4, zorder=6)
    
    mid_cab_x = (posA[0] + posB[0]) * 0.5
    mid_cab_y = (posA[1] + posB[1]) * 0.5 + 0.04
    ax.text(mid_cab_x, mid_cab_y, '$L$', fontsize=13, fontweight='bold', color='#1e293b', ha='center', zorder=8)
    
    draw_collar(ax, posA[0], posA[1], angle_deg=0.0, label='A', scale=1.0)
    draw_collar(ax, posB[0], posB[1], angle_deg=135.0, label='B', scale=1.0)
    
    dim_y = -0.11
    ax.plot([0, 0], [0, dim_y - 0.04], color='#64748b', linestyle='--', lw=1.2)
    ax.plot([posA[0], posA[0]], [0, dim_y - 0.04], color='#64748b', linestyle='--', lw=1.2)
    ax.annotate('', xy=(posA[0], dim_y), xytext=(0, dim_y), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    ax.text(posA[0] * 0.5, dim_y - 0.06, '$x$', fontsize=13, fontweight='bold', color='#0f172a', ha='center')
    
    s_off_dist = 0.11
    s_off_x = s_off_dist * np.sin(np.pi/4)
    s_off_y = s_off_dist * np.cos(np.pi/4)
    ax.plot([0, -s_off_x], [0, -s_off_y], color='#64748b', linestyle='--', lw=1.2)
    ax.plot([posB[0], posB[0] - s_off_x], [posB[1], posB[1] - s_off_y], color='#64748b', linestyle='--', lw=1.2)
    ax.annotate('', xy=(posB[0] - s_off_x, posB[1] - s_off_y), xytext=(-s_off_x, -s_off_y), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    mid_s_x = (posB[0] - 2 * s_off_x) * 0.5
    mid_s_y = (posB[1] - 2 * s_off_y) * 0.5
    ax.text(mid_s_x - 0.04, mid_s_y - 0.04, '$s$', fontsize=13, fontweight='bold', color='#0f172a', ha='right', va='top')
    
    arc_ang = np.linspace(np.pi, np.pi * 0.75, 20)
    ax.plot(0.24 * np.cos(arc_ang), 0.24 * np.sin(arc_ang), color='#0f172a', lw=1.4, zorder=5)
    ax.text(0.28 * np.cos(np.radians(157.5)), 0.28 * np.sin(np.radians(157.5)), '$45^\\circ$',
            fontsize=11.5, fontweight='bold', color='#0f172a')
    
    arrow_vA_len = 0.22
    ax.quiver(posA[0] + 0.08, posA[1], arrow_vA_len, 0, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.008, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(posA[0] + 0.08 + arrow_vA_len * 0.5, posA[1] + 0.06, f'$v_A = \\dot{{x}}$',
            fontsize=11.0, fontweight='bold', color='#16a34a', ha='center')
    
    arrow_vB_len = vB_val * 0.8
    tan_bx, tan_by = np.cos(np.radians(315.0)), np.sin(np.radians(315.0))
    ax.quiver(posB[0] + 0.06*tan_bx, posB[1] + 0.06*tan_by, arrow_vB_len*tan_bx, arrow_vB_len*tan_by,
              angles='xy', scale_units='xy', scale=1, color='#ea580c', width=0.008, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(posB[0] + (0.06 + arrow_vB_len*0.5)*tan_bx + 0.08, posB[1] + (0.06 + arrow_vB_len*0.5)*tan_by + 0.06,
            f'$v_B = -\\dot{{s}}$', fontsize=11.0, fontweight='bold', color='#ea580c')
    
    if "en" == "ko":
        hud_str = (
            f"[문제 2/184 고리-끈 구속속도 해석]\n"
            f"시간 t = {t:4.2f} s / {duration:4.2f} s\n"
            f"----------------------------------------\n"
            f"끈의 길이:   L = {L_cable:4.2f} m\n"
            f"고리 A 위치: x = {x_val:4.2f} m, v_A = {vA_val:4.2f} m/s\n"
            f"고리 B 위치: s = {s_val:4.2f} m\n"
            f"----------------------------------------\n"
            f"▶ 고리 B의 실시간 구속속도 v_B:\n"
            f"  v_B = [ (2x + √2·s) / (2s + √2·x) ] · v_A\n"
            f"      = {vB_val:4.3f} m/s (하향 슬라이딩)"
        )
        title_text = '[동역학 9판 문제 2/184] 경사 가이드 고리-끈 2차원 기하학적 구속운동'
    else:
        hud_str = (
            f"[Problem 2/184 Sliders-Cable Constraint]\n"
            f"Time t = {t:4.2f} s / {duration:4.2f} s\n"
            f"----------------------------------------\n"
            f"Cable Length: L = {L_cable:4.2f} m\n"
            f"Collar A Pos: x = {x_val:4.2f} m, v_A = {vA_val:4.2f} m/s\n"
            f"Collar B Pos: s = {s_val:4.2f} m\n"
            f"----------------------------------------\n"
            f"▶ Collar B Instantaneous Velocity v_B:\n"
            f"  v_B = [ (2x + √2·s) / (2s + √2·x) ] · v_A\n"
            f"      = {vB_val:4.3f} m/s"
        )
        title_text = '[Meriam Dynamics 9th Ed. Prob 2/184] Constrained Motion of Sliders and Cable'
    
    ax.text(-1.12, 1.32, hud_str, fontsize=9.0, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#ea580c', lw=1.5, alpha=0.94))
    
    deriv_box = patches.FancyBboxPatch((0.25, 0.45), 1.15, 0.85,
                                       boxstyle="round,pad=0.04", fc="#ffffff", ec='#0284c7', lw=1.5, alpha=0.94, zorder=9)
    ax.add_patch(deriv_box)
    
    d_title = '구속방정식 유도 (Derivation)' if "en" == "ko" else 'Kinematic Derivation'
    ax.text(0.825, 1.22, f'[{{d_title}}]', fontsize=9.2, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    if "en" == "ko":
        eq1 = '1) 코사인 법칙 ($\\angle AOB = 135^\\circ$):\n   $L^2 = x^2 + s^2 + 2xs\\cos 45^\\circ$'
        eq2 = '2) 시간에 대한 미분 ($\\dot{L} = 0$):\n   $0 = 2(x + s\\cos 45^\\circ)\\dot{x} + 2(s + x\\cos 45^\\circ)\\dot{s}$'
        eq3 = '3) $v_A = \\dot{x}, v_B = -\\dot{s}$ 대입:\n   $v_B = \\mathbf{\\frac{x + s\\cos 45^\\circ}{s + x\\cos 45^\\circ} v_A} = \\mathbf{\\frac{2x + \\sqrt{2}s}{2s + \\sqrt{2}x} v_A}$'
    else:
        eq1 = '1) Law of Cosines ($\\angle AOB = 135^\\circ$):\n   $L^2 = x^2 + s^2 + 2xs\\cos 45^\\circ$'
        eq2 = '2) Time Derivative ($\\dot{L} = 0$):\n   $0 = 2(x + s\\cos 45^\\circ)\\dot{x} + 2(s + x\\cos 45^\\circ)\\dot{s}$'
        eq3 = '3) Substitute $v_A = \\dot{x}, v_B = -\\dot{s}$:\n   $v_B = \\mathbf{\\frac{x + s\\cos 45^\\circ}{s + x\\cos 45^\\circ} v_A} = \\mathbf{\\frac{2x + \\sqrt{2}s}{2s + \\sqrt{2}x} v_A}$'
    
    ax.text(0.28, 1.05, eq1, fontsize=8.0, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(0.28, 0.82, eq2, fontsize=8.0, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(0.28, 0.55, eq3, fontsize=8.3, color='#b91c1c', fontweight='bold', fontproperties=font_prop, zorder=10)
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=6, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'prob2_184_sliders_cable.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
