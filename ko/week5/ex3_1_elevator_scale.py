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
[동역학 9판 예제 3.1] 엘리베이터 승객과 스프링 저울의 뉴턴 제2법칙(F=ma) 해석
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

m_p = 75.0
M_tot = 750.0
T_val = 8300.0
g = 9.81

W_tot = M_tot * g
W_p = m_p * g
a_y = (T_val - W_tot) / M_tot
R_val = m_p * (g + a_y)

duration = 3.0
fps = 30
n_frames = int(fps * duration)
t_eval = np.linspace(0, duration, n_frames)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.04, 0.04, 0.92, 0.88])
title_text = '[동역학 9판 예제 3.1] 엘리베이터 승객과 스프링 저울의 뉴턴 제2법칙(F=ma) 해석'

def update(frame):
    t = t_eval[frame]
    y_disp = 0.5 * a_y * (t**2) * 2.2
    v_curr = a_y * t
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-16, 24)
    ax.set_ylim(-6, 22)
    ax.axis('off')
    
    ax.add_patch(patches.Rectangle((-16, -6), 40, 28, fc='#f8fafc', ec='none', zorder=1))
    ax.plot([-8, -8], [-6, 22], color='#cbd5e1', lw=2.0, linestyle='--', zorder=2)
    ax.plot([4, 4], [-6, 22], color='#cbd5e1', lw=2.0, linestyle='--', zorder=2)
    
    cab_w, cab_h = 9.0, 10.0
    cab_x, cab_y = -6.5, -4.0 + y_disp
    ax.add_patch(patches.Rectangle((cab_x, cab_y), cab_w, cab_h, fc='#e0f2fe', ec='#0284c7', lw=2.5, zorder=3))
    ax.add_patch(patches.Rectangle((cab_x + 0.8, cab_y + 0.8), cab_w - 1.6, cab_h - 1.6, fc='#ffffff', ec='#bae6fd', lw=1.5, zorder=4))
    
    # Cable
    ax.plot([cab_x + cab_w/2, cab_x + cab_w/2], [cab_y + cab_h, 22], color='#334155', lw=3.0, zorder=5)
    ax.annotate('', xy=(cab_x + cab_w/2, cab_y + cab_h + 3.8), xytext=(cab_x + cab_w/2, cab_y + cab_h),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6, headlength=7), zorder=6)
    ax.text(cab_x + cab_w/2 + 0.8, cab_y + cab_h + 2.0, r'$T = 8300\text{ N}$', fontsize=9.5, fontweight='bold', color='#ef4444', zorder=7)
    
    # Weight
    ax.annotate('', xy=(cab_x + cab_w/2, cab_y - 3.2), xytext=(cab_x + cab_w/2, cab_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6, headlength=7), zorder=6)
    ax.text(cab_x + cab_w/2, cab_y - 4.2, r'$750(9.81) = 7360\text{ N}$', fontsize=9.0, fontweight='bold', color='#ef4444', ha='center', zorder=7)
    
    # Accel arrow
    ax.annotate('', xy=(cab_x - 1.2, cab_y + cab_h/2 + 2.0), xytext=(cab_x - 1.2, cab_y + cab_h/2 - 2.0),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=1.8, headwidth=5, headlength=6), zorder=6)
    ax.text(cab_x - 1.6, cab_y + cab_h/2, r'$a_y = 1.257\text{ m/s}^2$', fontsize=8.5, fontweight='bold', color='#16a34a', ha='right', va='center', zorder=7)
    
    # Scale
    sc_x, sc_y = cab_x + 2.0, cab_y + 0.8
    ax.add_patch(patches.Rectangle((sc_x, sc_y), 3.0, 0.6, fc='#facc15', ec='#ca8a04', lw=1.5, zorder=5))
    ax.plot([sc_x + 2.5, sc_x + 2.5], [sc_y + 0.6, sc_y + 4.0], color='#475569', lw=2.0, zorder=5)
    ax.add_patch(patches.Circle((sc_x + 2.5, sc_y + 4.3), 0.65, fc='#f1f5f9', ec='#334155', lw=1.2, zorder=6))
    ax.text(sc_x + 2.5, sc_y + 4.3, '830N', fontsize=6.5, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=7)
    
    # Person
    px, py = sc_x + 1.0, sc_y + 0.6
    ax.plot([px - 0.3, px - 0.2], [py, py + 2.0], color='#0f172a', lw=2.2, zorder=5)
    ax.plot([px + 0.3, px + 0.2], [py, py + 2.0], color='#0f172a', lw=2.2, zorder=5)
    ax.add_patch(patches.Rectangle((px - 0.6, py + 2.0), 1.2, 2.4, fc='#38bdf8', ec='#0284c7', lw=1.4, zorder=5))
    ax.add_patch(patches.Circle((px, py + 5.0), 0.6, fc='#fed7aa', ec='#ea580c', lw=1.2, zorder=5))
    
    # Person FBD on right
    fbd_x = 14.0
    fbd_y = -1.5 + y_disp
    ax.plot([fbd_x, fbd_x], [fbd_y - 4.0, fbd_y + 8.5], color='#64748b', linestyle='-.', lw=1.4, zorder=2)
    ax.text(fbd_x, fbd_y + 9.0, r'$y$', fontsize=10.5, fontweight='bold', color='#0f172a', ha='center')
    
    ax.plot([fbd_x - 0.3, fbd_x - 0.2], [fbd_y, fbd_y + 2.0], color='#475569', lw=2.2, zorder=5)
    ax.plot([fbd_x + 0.3, fbd_x + 0.2], [fbd_y, fbd_y + 2.0], color='#475569', lw=2.2, zorder=5)
    ax.add_patch(patches.Rectangle((fbd_x - 0.6, fbd_y + 2.0), 1.2, 2.4, fc='#cbd5e1', ec='#475569', lw=1.4, zorder=5))
    ax.add_patch(patches.Circle((fbd_x, fbd_y + 5.0), 0.6, fc='#e2e8f0', ec='#475569', lw=1.2, zorder=5))
    
    # Normal Force R
    ax.annotate('', xy=(fbd_x, fbd_y), xytext=(fbd_x, fbd_y - 2.8),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6, headlength=7), zorder=6)
    ax.text(fbd_x, fbd_y - 3.6, r'$R = 830\text{ N}$', fontsize=9.5, fontweight='bold', color='#ef4444', ha='center', zorder=7)
    
    # Gravity Wp
    cm_y = fbd_y + 2.8
    ax.annotate('', xy=(fbd_x, cm_y - 2.8), xytext=(fbd_x, cm_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6, headlength=7), zorder=6)
    ax.text(fbd_x + 0.8, cm_y - 1.5, r'$75(9.81) = 736\text{ N}$', fontsize=9.0, fontweight='bold', color='#ef4444', zorder=7)
    
    # ay arrow
    ax.annotate('', xy=(fbd_x + 1.8, cm_y + 1.8), xytext=(fbd_x + 1.8, cm_y - 1.8),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=1.6, headwidth=4.5, headlength=5.5), zorder=6)
    ax.text(fbd_x + 2.2, cm_y, r'$a_y$', fontsize=9.5, fontweight='bold', color='#16a34a', va='center', zorder=7)
    
    # HUD Box
    hud_str = (
                f"[동역학 9판 예제 3.1: 엘리베이터 & 저울 F=ma]\n"
                f"시간 t = {t:4.2f} s / {duration:.1f} s\n"
                f"--------------------------------------------------\n"
                f"전체 계: ΣF_y = M a_y\n"
                f"  8300 - 750(9.81) = 750 a_y  ⇒ a_y = 1.257 m/s²\n"
                f"사람 FBD: ΣF_y = m a_y\n"
                f"  R - 75(9.81) = 75(1.257)     ⇒ R = 830 N (저울 눈금)\n"
                f"--------------------------------------------------\n"
                f"▶ 저울 지시 수직항력: R = 830 N\n"
                f"▶ 3초 후 상승 속도:   v = a_y·t = {v_curr:4.2f} m/s (최종 3.77 m/s)"
    )
    ax.text(-15.0, 21.0, hud_str, fontsize=7.8, va='top', family='monospace', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor='#0284c7', lw=1.4, alpha=0.95), zorder=20)

fig.suptitle(title_text, fontsize=12.0, fontweight='bold', y=0.965, fontproperties=font_prop)
anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'ex3_1_elevator_scale.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
