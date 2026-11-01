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

vA_val = 0.30  # m/s (downward)
vB_val = -0.20 # m/s (upward)

fps = 30
duration = 3.5
n_frames = int(fps * duration)
t_eval = np.linspace(0, duration, n_frames)

def draw_pulley(ax, cx, cy, r, color='#38bdf8', ec='#0284c7', lw=1.6):
    sheave = patches.Circle((cx, cy), r, fc=color, ec=ec, lw=lw, zorder=5)
    ax.add_patch(sheave)
    rim = patches.Circle((cx, cy), r * 0.65, fc='#e0f2fe', ec=ec, lw=1.0, zorder=6)
    ax.add_patch(rim)
    hub = patches.Circle((cx, cy), r * 0.22, fc='#0f172a', ec='#0284c7', lw=1.0, zorder=7)
    ax.add_patch(hub)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

xB_pos = 0.4
xA_pos = 1.6
r1, rC, rB = 0.16, 0.12, 0.16
r2, rA = 0.15, 0.09
y_top1, y_C, y_top2 = 0.28, 0.72, 0.28

def update(frame):
    t = t_eval[frame]
    yA = 1.05 + vA_val * t
    yB = 2.45 + vB_val * t
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 2.3)
    ax.set_ylim(3.7, -0.4)
    ax.axis('off')
    
    ceiling_bg = patches.Rectangle((-2.5, -0.4), 4.8, 0.4, color='#cbd5e1', zorder=1)
    ax.add_patch(ceiling_bg)
    ax.plot([-2.5, 2.3], [0, 0], color='#475569', lw=2.5, zorder=3)
    for hx in np.linspace(-2.4, 2.2, 40):
        ax.plot([hx, hx + 0.12], [-0.25, 0.0], color='#94a3b8', lw=1.2, zorder=2)
    
    datum_txt = "고정 기준면 (Datum)" if "en" == "ko" else "Fixed Datum"
    ax.text(-2.4, -0.1, datum_txt, fontsize=10.5, fontweight='bold', color='#1e293b', fontproperties=font_prop)
    
    bracket_left = patches.Rectangle((xB_pos - 0.04, 0.0), 0.08, y_C, color='#94a3b8', ec='#475569', lw=1.2, zorder=4)
    ax.add_patch(bracket_left)
    bracket_right = patches.Rectangle((xA_pos - 0.04, 0.0), 0.08, y_top2, color='#94a3b8', ec='#475569', lw=1.2, zorder=4)
    ax.add_patch(bracket_right)
    ax.scatter([xA_pos - rA], [0.0], color='#0f172a', s=45, zorder=6)
    
    cable_color = '#1e293b'
    cable_lw = 2.2
    
    anchor_C_x, anchor_C_y = xB_pos - rC * 0.6, y_C + 0.08
    ax.scatter([anchor_C_x], [anchor_C_y], color='#0f172a', s=35, zorder=7)
    ax.plot([anchor_C_x, xB_pos - rB], [anchor_C_y, yB], color=cable_color, lw=cable_lw, zorder=4)
    
    th_b1 = np.linspace(np.pi, 2*np.pi, 25)
    ax.plot(xB_pos + rB * np.cos(th_b1), yB + rB * np.sin(th_b1), color=cable_color, lw=cable_lw, zorder=4)
    ax.plot([xB_pos + rB, xB_pos + rC], [yB, y_C], color=cable_color, lw=cable_lw, zorder=4)
    
    th_c = np.linspace(0, np.pi, 25)
    ax.plot(xB_pos + rC * np.cos(th_c), y_C - rC * np.sin(th_c), color=cable_color, lw=cable_lw, zorder=4)
    
    ax.plot([xB_pos - rC, xB_pos - rB * 0.4], [y_C, yB], color=cable_color, lw=cable_lw, zorder=4)
    th_b2 = np.linspace(np.pi, 2*np.pi, 20)
    ax.plot(xB_pos + rB*0.4 * np.cos(th_b2), yB + rB*0.4 * np.sin(th_b2), color=cable_color, lw=cable_lw, zorder=4)
    ax.plot([xB_pos + rB * 0.4, xB_pos - r1], [yB, y_top1], color=cable_color, lw=cable_lw, zorder=4)
    
    th_top1 = np.linspace(np.pi, np.pi/2, 15)
    ax.plot(xB_pos + r1 * np.cos(th_top1), y_top1 - r1 * np.sin(th_top1), color=cable_color, lw=cable_lw, zorder=4)
    ax.plot([xB_pos, xA_pos], [y_top1 - r1, y_top2 - r2], color=cable_color, lw=cable_lw, zorder=4)
    
    th_top2 = np.linspace(np.pi/2, 0, 15)
    ax.plot(xA_pos + r2 * np.cos(th_top2), y_top2 - r2 * np.sin(th_top2), color=cable_color, lw=cable_lw, zorder=4)
    ax.plot([xA_pos + r2, xA_pos + rA], [y_top2, yA], color=cable_color, lw=cable_lw, zorder=4)
    
    th_a = np.linspace(0, np.pi, 25)
    ax.plot(xA_pos + rA * np.cos(th_a), yA + rA * np.sin(th_a), color=cable_color, lw=cable_lw, zorder=4)
    ax.plot([xA_pos - rA, xA_pos - rA], [yA, 0.0], color=cable_color, lw=cable_lw, zorder=4)
    
    draw_pulley(ax, xB_pos, y_top1, r1)
    draw_pulley(ax, xB_pos, y_C, rC)
    ax.text(xB_pos + rC + 0.08, y_C + 0.04, '$C$', fontsize=13, fontweight='bold', color='#0284c7')
    draw_pulley(ax, xA_pos, y_top2, r2)
    
    draw_pulley(ax, xB_pos, yB, rB)
    bracket_B = patches.Rectangle((xB_pos - 0.05, yB), 0.10, 0.32, color='#64748b', ec='#334155', lw=1.2, zorder=4)
    ax.add_patch(bracket_B)
    block_B = patches.Rectangle((xB_pos - 0.32, yB + 0.32), 0.64, 0.32, fc='#f97316', ec='#c2410c', lw=1.8, zorder=6)
    ax.add_patch(block_B)
    ax.text(xB_pos, yB + 0.51, '$B$', fontsize=15, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=7)
    
    draw_pulley(ax, xA_pos, yA, rA)
    bracket_A = patches.Rectangle((xA_pos - 0.03, yA), 0.06, 0.22, color='#64748b', ec='#334155', lw=1.2, zorder=4)
    ax.add_patch(bracket_A)
    cyl_A = patches.Rectangle((xA_pos - 0.16, yA + 0.22), 0.32, 0.72, fc='#ea580c', ec='#9a3412', lw=1.8, zorder=6)
    ax.add_patch(cyl_A)
    ax.text(xA_pos, yA + 0.58, '$A$', fontsize=15, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=7)
    
    dim_xB = -0.12
    ax.plot([dim_xB, xB_pos - rB - 0.05], [0, 0], color='#64748b', linestyle='--', lw=1.2)
    ax.plot([dim_xB, xB_pos - rB - 0.05], [yB, yB], color='#64748b', linestyle='--', lw=1.2)
    ax.annotate('', xy=(dim_xB, yB), xytext=(dim_xB, 0), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    ax.text(dim_xB - 0.08, yB * 0.5, '$y_B$', fontsize=13, fontweight='bold', color='#0f172a', ha='right', va='center')
    
    dim_xA = 1.05
    ax.plot([dim_xA, xA_pos - rA - 0.05], [0, 0], color='#64748b', linestyle='--', lw=1.2)
    ax.plot([dim_xA, xA_pos - rA - 0.05], [yA, yA], color='#64748b', linestyle='--', lw=1.2)
    ax.annotate('', xy=(dim_xA, yA), xytext=(dim_xA, 0), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    ax.text(dim_xA - 0.08, yA * 0.5, '$y_A$', fontsize=13, fontweight='bold', color='#0f172a', ha='right', va='center')
    
    arrow_vA_len = 0.50
    ax.quiver(xA_pos + 0.25, yA + 0.55, 0, arrow_vA_len, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.009, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xA_pos + 0.32, yA + 0.55 + arrow_vA_len * 0.5, '$v_A = 0.3\\text{ m/s} \\downarrow$',
            fontsize=11.5, fontweight='bold', color='#16a34a', va='center')
    
    arrow_vB_len = 0.35
    ax.quiver(xB_pos + 0.42, yB + 0.48, 0, -arrow_vB_len, angles='xy', scale_units='xy', scale=1,
              color='#ea580c', width=0.009, headwidth=4.5, headlength=5.5, zorder=8)
    ax.text(xB_pos + 0.49, yB + 0.48 - arrow_vB_len * 0.5, '$v_B = 0.2\\text{ m/s} \\uparrow$',
            fontsize=11.5, fontweight='bold', color='#ea580c', va='center')
    
    if "en" == "ko":
        hud_str = (
            f"[예제 2.15 복합 풀리 실시간 해석]\n"
            f"시간 t = {t:4.2f} s / {duration:4.2f} s\n"
            f"--------------------------------------\n"
            f"원통 A 속도: v_A = +{vA_val:4.2f} m/s (하향)\n"
            f"원통 A 위치: y_A =  {yA:4.2f} m\n"
            f"블록 B 위치: y_B =  {yB:4.2f} m\n"
            f"--------------------------------------\n"
            f"▶ 블록 B 속도 계산 결과:\n"
            f"  v_B = - (2/3) · v_A = -0.20 m/s\n"
            f"  (상향 0.20 m/s로 상승)"
        )
        title_text = '[동역학 9판 예제 2.15] 복합 풀리 도르래 시스템 구속속도 해석'
    else:
        hud_str = (
            f"[Sample Prob. 2.15 Pulley System]\n"
            f"Time t = {t:4.2f} s / {duration:4.2f} s\n"
            f"--------------------------------------\n"
            f"Cylinder A Vel: v_A = +{vA_val:4.2f} m/s (Down)\n"
            f"Cylinder A Pos: y_A =  {yA:4.2f} m\n"
            f"Block B Pos:    y_B =  {yB:4.2f} m\n"
            f"--------------------------------------\n"
            f"▶ Block B Velocity Result:\n"
            f"  v_B = - (2/3) · v_A = -0.20 m/s\n"
            f"  (Moving UP at 0.20 m/s)"
        )
        title_text = '[Meriam Dynamics 9th Ed. Ex 2.15] Constrained Motion of Pulley System'
    
    ax.text(-2.4, 0.45, hud_str, fontsize=9.2, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#0284c7', lw=1.5, alpha=0.94))
    
    deriv_box = patches.FancyBboxPatch((-2.42, 1.95), 1.95, 1.65,
                                       boxstyle="round,pad=0.08", fc="#ffffff", ec='#16a34a', lw=1.5, alpha=0.94, zorder=9)
    ax.add_patch(deriv_box)
    d_title = '풀이 1: 케이블 길이 미분법' if "en" == "ko" else 'Method 1: Length Differentiation'
    ax.text(-1.45, 2.15, f'[{d_title}]', fontsize=9.5, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    if "en" == "ko":
        eq1 = '1) 케이블 총 길이 방정식:\n   $L = 3y_B + 2y_A + C$'
        eq2 = '2) 시간에 대한 미분 (총 길이 불변):\n   $0 = 3v_B + 2v_A$'
        eq3 = '3) 블록 B의 구속속도 도출:\n   $v_B = -\\frac{2}{3}v_A = -\\frac{2}{3}(0.3) = -0.2\\text{ m/s}$\n   ▶ 0.2 m/s (상향)'
    else:
        eq1 = '1) Total Cable Length Equation:\n   $L = 3y_B + 2y_A + C$'
        eq2 = '2) Time Derivative (Constant Length):\n   $0 = 3v_B + 2v_A$'
        eq3 = '3) Block B Constrained Velocity:\n   $v_B = -\\frac{2}{3}v_A = -\\frac{2}{3}(0.3) = -0.2\\text{ m/s}$\n   ▶ 0.2 m/s (Upward)'
    
    ax.text(-2.35, 2.45, eq1, fontsize=8.5, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-2.35, 2.95, eq2, fontsize=8.5, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-2.35, 3.45, eq3, fontsize=8.5, color='#b91c1c', fontweight='bold', fontproperties=font_prop, zorder=10)
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=6, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'ex2_15_pulley_2d.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
