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

h = 250.0
L_cable = 1050.0
vA_val = 25.0
sA_snap = 425.0

duration = 3.5
fps = 30
n_frames = int(fps * duration)
t_eval = np.linspace(-1.75, 1.75, n_frames)

def draw_pulley(ax, cx, cy, r, color='#38bdf8', ec='#0284c7', lw=1.6):
    sheave = patches.Circle((cx, cy), r, fc=color, ec=ec, lw=lw, zorder=7)
    ax.add_patch(sheave)
    rim = patches.Circle((cx, cy), r * 0.65, fc='#e0f2fe', ec=ec, lw=1.0, zorder=8)
    ax.add_patch(rim)
    hub = patches.Circle((cx, cy), r * 0.22, fc='#0f172a', ec='#0284c7', lw=1.0, zorder=9)
    ax.add_patch(hub)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

def update(frame):
    t = t_eval[frame]
    sA = sA_snap + vA_val * t
    l1 = np.sqrt(sA**2 + h**2)
    l2 = L_cable - l1
    delta_y = np.sqrt(np.maximum(0, l2**2 - sA**2))
    yB = h + delta_y
    
    cos_th1 = sA / l1
    cos_th2 = sA / l2
    sin_th2 = delta_y / l2
    vB_val = ((cos_th1 + cos_th2) / sin_th2) * vA_val if sin_th2 > 0 else 0
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-850, 220)
    ax.set_ylim(-820, 160)
    ax.axis('off')
    
    bg_rect = patches.Rectangle((-850, -820), 1070, 980, color='#f8fafc', zorder=1)
    ax.add_patch(bg_rect)
    
    ceil_mount = patches.Rectangle((-50, 0), 100, 45, color='#cbd5e1', ec='#64748b', lw=1.5, zorder=2)
    ax.add_patch(ceil_mount)
    ax.plot([-70, 70], [45, 45], color='#475569', lw=2.0, zorder=3)
    for cx in np.linspace(-60, 50, 7):
        ax.plot([cx, cx + 15], [45, 60], color='#94a3b8', lw=1.2, zorder=2)
    
    bracket_C = patches.Polygon([(-25, 0), (25, 0), (0, -18)], fc='#64748b', ec='#334155', lw=1.6, zorder=5)
    ax.add_patch(bracket_C)
    ax.scatter([0], [-10], color='#0f172a', s=30, zorder=7)
    ax.text(28, -12, '$C$', fontsize=14, fontweight='bold', color='#0284c7', va='center')
    
    guide_w, guide_h = 70, 560
    guide_rect = patches.Rectangle((-guide_w/2, -780), guide_w, guide_h, color='#e2e8f0', ec='#94a3b8', lw=1.8, zorder=2)
    ax.add_patch(guide_rect)
    slot_w = 40
    slot_rect = patches.Rectangle((-slot_w/2, -770), slot_w, guide_h - 20, color='#ffffff', ec='#cbd5e1', lw=1.2, zorder=3)
    ax.add_patch(slot_rect)
    ax.plot([0, 0], [0, -780], color='#64748b', linestyle='-.', lw=1.4, zorder=4)
    
    cyl_base_x = -780
    cyl_len = 220
    cyl_h = 60
    mount_A = patches.Rectangle((cyl_base_x - 10, -h - cyl_h/2 - 18), cyl_len + 20, 18, color='#cbd5e1', ec='#64748b', lw=1.5, zorder=2)
    ax.add_patch(mount_A)
    ax.plot([cyl_base_x - 20, cyl_base_x + cyl_len + 30], [-h - cyl_h/2 - 18, -h - cyl_h/2 - 18], color='#475569', lw=2.0, zorder=3)
    
    cyl_body = patches.Rectangle((cyl_base_x, -h - cyl_h/2), cyl_len, cyl_h,
                                 fc='#facc15', ec='#ca8a04', lw=2.0, zorder=5)
    ax.add_patch(cyl_body)
    cap_L = patches.Rectangle((cyl_base_x - 12, -h - cyl_h/2 - 4), 14, cyl_h + 8, fc='#713f12', ec='#451a03', lw=1.5, zorder=6)
    cap_R = patches.Rectangle((cyl_base_x + cyl_len - 2, -h - cyl_h/2 - 4), 14, cyl_h + 8, fc='#713f12', ec='#451a03', lw=1.5, zorder=6)
    ax.add_patch(cap_L)
    ax.add_patch(cap_R)
    
    rod_start_x = cyl_base_x + cyl_len
    rod_end_x = -sA
    piston_rod = patches.Rectangle((rod_start_x, -h - 7), rod_end_x - rod_start_x, 14,
                                  fc='#e2e8f0', ec='#94a3b8', lw=1.4, zorder=4)
    ax.add_patch(piston_rod)
    ax.plot([cyl_base_x - 40, 50], [-h, -h], color='#64748b', linestyle='-.', lw=1.2, zorder=3)
    
    cable_col = '#1e293b'
    cable_lw = 2.4
    ax.plot([0, -sA], [-10, -h], color=cable_col, lw=cable_lw, zorder=5)
    ax.plot([-sA, 0], [-h, -yB], color=cable_col, lw=cable_lw, zorder=5)
    
    r_pulley = 22.0
    draw_pulley(ax, -sA, -h, r_pulley)
    ax.text(-sA, -h - r_pulley - 18, '$A$', fontsize=14, fontweight='bold', color='#0284c7', ha='center', zorder=10)
    
    block_w, block_h = 36, 50
    block_B = patches.Rectangle((-block_w/2, -yB - block_h/2), block_w, block_h,
                                fc='#f87171', ec='#b91c1c', lw=1.8, zorder=6)
    ax.add_patch(block_B)
    ax.scatter([0], [-yB], color='#0f172a', s=25, zorder=8)
    ax.text(block_w/2 + 12, -yB, '$B$', fontsize=14, fontweight='bold', color='#b91c1c', va='center', zorder=10)
    
    dim_h_x = -sA - 120
    ax.plot([dim_h_x, 0], [0, 0], color='#64748b', linestyle='--', lw=1.1)
    ax.plot([dim_h_x, -sA], [-h, -h], color='#64748b', linestyle='--', lw=1.1)
    ax.annotate('', xy=(dim_h_x, 0), xytext=(dim_h_x, -h),
                arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    ax.text(dim_h_x - 12, -h * 0.5, '250 mm', fontsize=11, fontweight='bold', color='#0f172a', ha='right', va='center')
    
    dim_sA_y = 60
    ax.plot([-sA, -sA], [-h, dim_sA_y + 15], color='#64748b', linestyle='--', lw=1.1)
    ax.plot([0, 0], [0, dim_sA_y + 15], color='#64748b', linestyle='--', lw=1.1)
    ax.annotate('', xy=(-sA, dim_sA_y), xytext=(0, dim_sA_y),
                arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.5))
    ax.text(-sA * 0.5, dim_sA_y + 14, '$s_A$', fontsize=13, fontweight='bold', color='#0f172a', ha='center')
    
    arrow_vA_len = 70.0
    ax.quiver(-sA, -h + 26, -arrow_vA_len, 0, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.007, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(-sA - arrow_vA_len * 0.5, -h + 40, '$v_A = 25\\text{ mm/s} \\leftarrow$',
            fontsize=11.0, fontweight='bold', color='#16a34a', ha='center')
    
    arrow_vB_len = vB_val * 1.6
    ax.quiver(block_w/2 + 22, -yB, 0, arrow_vB_len, angles='xy', scale_units='xy', scale=1,
              color='#ea580c', width=0.007, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(block_w/2 + 30, -yB + arrow_vB_len * 0.5, f'$v_B = {vB_val:.1f}\\text{{ mm/s}} \\uparrow$',
            fontsize=11.0, fontweight='bold', color='#ea580c', va='center')
    
    if "en" == "ko":
        hud_str = (
            f"[문제 2/189 유압실린더-슬라이더 구속운동]\n"
            f"시간 t = {t:4.2f} s / 1.75 s\n"
            f"----------------------------------------\n"
            f"케이블 총 길이: L = {L_cable:.0f} mm, h = {h:.0f} mm\n"
            f"피스톤 변위:   s_A = {sA:5.1f} mm (v_A = 25 mm/s)\n"
            f"슬라이더 깊이: y_B = {yB:5.1f} mm\n"
            f"케이블 분지:   l_1 = {l1:5.1f} mm, l_2 = {l2:5.1f} mm\n"
            f"----------------------------------------\n"
            f"▶ s_A = 425 mm 순간 슬라이더 B의 속도:\n"
            f"  v_B = [ (cos θ₁ + cos θ₂) / sin θ₂ ] · v_A\n"
            f"      = 62.9 mm/s (상향 상승)"
        )
        title_text = '[동역학 9판 문제 2/189] 유압실린더-도르래-슬라이더 기하학적 구속운동 해석'
    else:
        hud_str = (
            f"[Problem 2/189 Hydraulic Cylinder & Slider]\n"
            f"Time t = {t:4.2f} s / 1.75 s\n"
            f"----------------------------------------\n"
            f"Cable Length: L = {L_cable:.0f} mm, h = {h:.0f} mm\n"
            f"Piston Disp:  s_A = {sA:5.1f} mm (v_A = 25 mm/s)\n"
            f"Slider Depth: y_B = {yB:5.1f} mm\n"
            f"Cable Legs:   l_1 = {l1:5.1f} mm, l_2 = {l2:5.1f} mm\n"
            f"----------------------------------------\n"
            f"▶ At s_A = 425 mm, Slider B Velocity:\n"
            f"  v_B = [ (cos θ₁ + cos θ₂) / sin θ₂ ] · v_A\n"
            f"      = 62.9 mm/s (Upward)"
        )
        title_text = '[Meriam Dynamics 9th Ed. Prob 2/189] Constrained Motion of Hydraulic Cylinder & Slider'
    
    ax.text(-830, 150, hud_str, fontsize=9.0, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#eab308', lw=1.5, alpha=0.94))
    
    deriv_box = patches.FancyBboxPatch((-835, -805), 440, 360,
                                       boxstyle="round,pad=10", fc="#ffffff", ec='#0284c7', lw=1.5, alpha=0.94, zorder=9)
    ax.add_patch(deriv_box)
    
    d_title = '구속방정식 미분 풀이 (Derivation)' if "en" == "ko" else 'Kinematic Derivation'
    ax.text(-615, -465, f'[{{d_title}}]', fontsize=9.2, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    if "en" == "ko":
        eq1 = '1) 케이블 길이:\n   $L = \\sqrt{s_A^2 + h^2} + \\sqrt{s_A^2 + (y_B - h)^2}$'
        eq2 = '2) 시간에 대한 미분 ($\\dot{L} = 0$):\n   $0 = \\frac{s_A v_A}{l_1} + \\frac{s_A v_A}{l_2} + \\frac{y_B - h}{l_2}\\dot{y}_B$'
        eq3 = '3) $s_A = 425\\text{ mm}$ 수치 대입:\n   $l_1 = 493.1\\text{ mm}, l_2 = 556.9\\text{ mm}, y_B - h = 359.9\\text{ mm}$'
        eq4 = '▶ 슬라이더 B 속도 (Answer):\n   $v_B = -\\dot{y}_B = \\mathbf{62.9\\text{ mm/s}}$ (상향)'
    else:
        eq1 = '1) Cable Length:\n   $L = \\sqrt{s_A^2 + h^2} + \\sqrt{s_A^2 + (y_B - h)^2}$'
        eq2 = '2) Time Derivative ($\\dot{L} = 0$):\n   $0 = \\frac{s_A v_A}{l_1} + \\frac{s_A v_A}{l_2} + \\frac{y_B - h}{l_2}\\dot{y}_B$'
        eq3 = '3) Substitute $s_A = 425\\text{ mm}$:\n   $l_1 = 493.1\\text{ mm}, l_2 = 556.9\\text{ mm}, y_B - h = 359.9\\text{ mm}$'
        eq4 = '▶ Slider B Velocity (Answer):\n   $v_B = -\\dot{y}_B = \\mathbf{62.9\\text{ mm/s (Upward)}}$'
    
    ax.text(-820, -535, eq1, fontsize=8.2, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-820, -615, eq2, fontsize=8.2, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-820, -695, eq3, fontsize=8.0, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-820, -775, eq4, fontsize=8.6, color='#b91c1c', fontweight='bold', fontproperties=font_prop, zorder=10)
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=6, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'prob2_189_cylinder_slider.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
