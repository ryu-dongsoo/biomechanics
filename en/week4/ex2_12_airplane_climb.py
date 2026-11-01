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
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Font configuration
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters (Meriam Dynamics 9th Ed. Sample Problem 2.12)
v0 = 250.0 / 3.6     # 69.44 m/s (250 km/h)
gamma = np.radians(15.0) # 15 deg
a_tan = 0.8          # m/s^2
xA = 3000.0          # 3000 m (3 km)
t_total = 60.0       # 60 s

fps = 30
duration = 3.5
n_frames = int(fps * duration)
t_eval = np.linspace(0, t_total, n_frames)

def draw_airplane(ax_3d, px, py, pz, scale=140):
    cy, sy = np.cos(gamma), np.sin(gamma)
    ax_3d.plot([px, px], [py - 1.6*scale*cy, py + 1.6*scale*cy], [pz - 1.6*scale*sy, pz + 1.6*scale*sy],
               color='#b91c1c', lw=3.5)
    ax_3d.plot([px - 2.0*scale, px + 2.0*scale], [py + 0.2*scale*cy, py + 0.2*scale*cy], [pz + 0.2*scale*sy, pz + 0.2*scale*sy],
               color='#b91c1c', lw=3.0)
    ax_3d.plot([px - 0.9*scale, px + 0.9*scale], [py - 1.2*scale*cy, py - 1.2*scale*cy], [pz - 1.2*scale*sy, pz - 1.2*scale*sy],
               color='#b91c1c', lw=2.5)
    ax_3d.plot([px, px], [py - 1.3*scale*cy, py - 1.3*scale*cy], [pz - 1.3*scale*sy, pz - 1.3*scale*sy + 0.9*scale],
               color='#b91c1c', lw=2.5)

def draw_radar(ax_3d):
    ax_3d.plot([0, 0], [0, 0], [-250, 0], color='#1e293b', lw=5)
    ax_3d.plot([-150, 150], [0, 0], [-250, -250], color='#1e293b', lw=5)
    ax_3d.plot([0, 0], [-150, 150], [-250, -250], color='#1e293b', lw=5)
    u = np.linspace(0, 2*np.pi, 24)
    v_ang = np.linspace(0, np.pi/2, 12)
    dish_r = 260
    dx = dish_r * np.outer(np.cos(u), np.sin(v_ang)) * 0.45
    dy = dish_r * np.outer(np.sin(u), np.sin(v_ang)) * 0.85
    dz = dish_r * np.outer(np.ones(np.size(u)), np.cos(v_ang)) * 0.85
    ax_3d.plot_wireframe(dx, dy, dz, color='#334155', alpha=0.7, lw=0.9)

fig = plt.figure(figsize=(10.2, 7.6), dpi=120)
ax = fig.add_subplot(111, projection='3d')
ax.set_position([0.01, 0.01, 0.98, 0.95])

def update(frame):
    t = t_eval[frame]
    s = v0 * t + 0.5 * a_tan * t**2
    v = v0 + a_tan * t
    xP, yP, zP = xA, s * np.cos(gamma), s * np.sin(gamma)
    vx, vy, vz = 0.0, v * np.cos(gamma), v * np.sin(gamma)
    
    r = np.hypot(xP, yP)
    theta_rad = np.arctan2(yP, xP)
    theta_deg = np.degrees(theta_rad)
    r_dot = (xP * vx + yP * vy) / r if r > 0 else 0
    theta_dot = (xP * vy - yP * vx) / (r**2) if r > 0 else 0
    z_dot = vz
    
    R = np.sqrt(xP**2 + yP**2 + zP**2)
    phi_rad = np.arcsin(zP / R) if R > 0 else 0
    phi_deg = np.degrees(phi_rad)
    R_dot = (xP * vx + yP * vy + zP * vz) / R if R > 0 else 0
    phi_dot = (R * z_dot - zP * R_dot) / (R * np.sqrt(xP**2 + yP**2)) if (R > 0 and r > 0) else 0
    
    ax.clear()
    ax.view_init(elev=22, azim=-52)
    ax.dist = 8.2
    
    ax.plot([0, 4200], [0, 0], [0, 0], color='#1e293b', linestyle='--', lw=1.5)
    ax.text(4350, 0, 0, 'x', fontsize=13, fontweight='bold', color='#1e293b')
    ax.plot([0, 0], [0, 6500], [0, 0], color='#1e293b', linestyle='--', lw=1.5)
    ax.text(0, 6700, 0, 'y', fontsize=13, fontweight='bold', color='#1e293b')
    ax.plot([0, 0], [0, 0], [0, 2400], color='#1e293b', linestyle='--', lw=1.5)
    ax.text(0, 0, 2550, 'z', fontsize=13, fontweight='bold', color='#1e293b')
    
    ax.plot([xA, xA], [0, 6500], [0, 0], color='#64748b', linestyle='--', lw=1.3)
    ax.text(xA, 6700, 0, "y'", fontsize=13, fontweight='bold', color='#64748b')
    ax.plot([xA, xA], [0, 0], [0, 2000], color='#64748b', linestyle='--', lw=1.3)
    ax.text(xA, 0, 2150, "z'", fontsize=13, fontweight='bold', color='#64748b')
    
    ax.plot([0, xA], [0, 0], [0, 0], color='#0f172a', lw=3.0)
    ax.text(xA * 0.45, -450, 0, '3 km', fontsize=12, fontweight='bold', color='#0f172a', fontproperties=font_prop)
    
    s_full = v0 * 60.0 + 0.5 * a_tan * (60.0**2)
    s_arr = np.linspace(0, s_full, 80)
    ax.plot(xA * np.ones_like(s_arr), s_arr * np.cos(gamma), s_arr * np.sin(gamma),
            color='#ea580c', linestyle='--', lw=2.2)
    
    arc_ang = np.linspace(0, np.radians(15.0), 20)
    arc_rad = 1400
    ax.plot(xA * np.ones_like(arc_ang), arc_rad * np.cos(arc_ang), arc_rad * np.sin(arc_ang),
            color='#ea580c', lw=1.8)
    ax.text(xA, arc_rad * 1.15, arc_rad * 0.16, '15°', fontsize=12, fontweight='bold', color='#ea580c')
    
    ax.quiver(xA, 0, 0, 0, v0*np.cos(gamma)*8.5, v0*np.sin(gamma)*8.5,
              color='#16a34a', lw=2.5, arrow_length_ratio=0.2)
    ax.text(xA, v0*np.cos(gamma)*4.5, v0*np.sin(gamma)*5.5 + 180, '$v_0$', fontsize=13, fontweight='bold', color='#16a34a')
    
    beam_verts = [[(0, 0, 0), (xP, yP, zP), (xP, yP, 0)]]
    beam_poly = Poly3DCollection(beam_verts, color='#fed7aa', alpha=0.38)
    ax.add_collection3d(beam_poly)
    
    lbl_R = '시선거리 $R$' if 'en' == 'ko' else 'Line of Sight $R$'
    lbl_r = '수평거리 $r$' if 'en' == 'ko' else 'Horizontal Proj. $r$'
    lbl_z = '고도 $z$' if 'en' == 'ko' else 'Altitude $z$'
    
    ax.plot([0, xP], [0, yP], [0, zP], color='#d97706', lw=2.5, label=lbl_R)
    ax.plot([0, xP], [0, yP], [0, 0], color='#475569', linestyle='--', lw=2.0, label=lbl_r)
    ax.plot([xP, xP], [yP, yP], [0, zP], color='#64748b', linestyle=':', lw=2.0, label=lbl_z)
    
    ax.text(xP * 0.48, yP * 0.48, zP * 0.48 + 250, '$R$', fontsize=14, fontweight='bold', color='#d97706')
    ax.text(xP * 0.52, yP * 0.52, -220, '$r$', fontsize=14, fontweight='bold', color='#475569')
    ax.text(xP + 180, yP, zP * 0.5, '$z$', fontsize=14, fontweight='bold', color='#64748b')
    
    th_arc = np.linspace(0, theta_rad, 20)
    th_rad = 1600
    ax.plot(th_rad * np.cos(th_arc), th_rad * np.sin(th_arc), np.zeros_like(th_arc), color='#475569', lw=1.6)
    ax.text(th_rad * np.cos(theta_rad*0.5) * 1.2, th_rad * np.sin(theta_rad*0.5) * 1.2, 0, r'$\theta$',
            fontsize=13, fontweight='bold', color='#475569')
    
    phi_arc = np.linspace(0, phi_rad, 20)
    phi_rad_len = 1900
    px_arc = phi_rad_len * np.cos(phi_arc) * np.cos(theta_rad)
    py_arc = phi_rad_len * np.cos(phi_arc) * np.sin(theta_rad)
    pz_arc = phi_rad_len * np.sin(phi_arc)
    ax.plot(px_arc, py_arc, pz_arc, color='#d97706', lw=1.6)
    ax.text(phi_rad_len * np.cos(phi_rad*0.5) * np.cos(theta_rad) * 1.15,
            phi_rad_len * np.cos(phi_rad*0.5) * np.sin(theta_rad) * 1.15,
            phi_rad_len * np.sin(phi_rad*0.5) * 1.15 + 100, r'$\phi$',
            fontsize=13, fontweight='bold', color='#d97706')
    
    draw_radar(ax)
    ax.text(0, -550, 100, 'O', fontsize=14, fontweight='bold', color='#0f172a')
    ax.scatter([xA], [0], [0], color='#16a34a', s=70)
    ax.text(xA + 120, -350, 0, 'A', fontsize=14, fontweight='bold', color='#16a34a')
    
    draw_airplane(ax, xP, yP, zP, scale=140)
    ax.text(xP + 120, yP + 250, zP + 250, 'P', fontsize=15, fontweight='bold', color='#b91c1c')
    
    ax.set_xlim(-200, 3600)
    ax.set_ylim(-300, 6500)
    ax.set_zlim(-300, 2400)
    ax.set_axis_off()
    
    if 'en' == 'ko':
        hud_str = (
            f"[예제 2.12 실시간 해석]\n"
            f"t = {t:4.1f} s / 60.0 s\n"
            f"v = {v:5.1f} m/s ({v*3.6:5.1f} km/h)\n"
            f"s = {s:5.0f} m\n"
            f"r = {r:5.0f} m,  dr/dt = {r_dot:4.1f} m/s\n"
            f"θ = {theta_deg:4.1f}°, dθ/dt = {theta_dot:6.4f} rad/s\n"
            f"z = {zP:5.0f} m,  dz/dt = {z_dot:4.1f} m/s\n"
            f"R = {R:5.0f} m,  dR/dt = {R_dot:4.1f} m/s\n"
            f"φ = {phi_deg:4.1f}°, dφ/dt = {phi_dot:6.4f} rad/s"
        )
        title_text = '[동역학 9판 예제 2.12] 항공기 이륙 3차원 공간곡선운동 및 레이더 추적 기하학'
    else:
        hud_str = (
            f"[Sample Prob. 2.12 Real-Time]\n"
            f"t = {t:4.1f} s / 60.0 s\n"
            f"v = {v:5.1f} m/s ({v*3.6:5.1f} km/h)\n"
            f"s = {s:5.0f} m\n"
            f"r = {r:5.0f} m,  dr/dt = {r_dot:4.1f} m/s\n"
            f"θ = {theta_deg:4.1f}°, dθ/dt = {theta_dot:6.4f} rad/s\n"
            f"z = {zP:5.0f} m,  dz/dt = {z_dot:4.1f} m/s\n"
            f"R = {R:5.0f} m,  dR/dt = {R_dot:4.1f} m/s\n"
            f"φ = {phi_deg:4.1f}°, dφ/dt = {phi_dot:6.4f} rad/s"
        )
        title_text = '[Meriam Dynamics 9th Ed. Ex 2.12] Aircraft Climb 3D Curvilinear Motion & Radar Tracking'
    
    ax.text2D(0.02, 0.96, hud_str, transform=ax.transAxes, fontsize=10, family='monospace',
              verticalalignment='top', fontproperties=font_prop,
              bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#d97706', lw=1.5, alpha=0.94))
    
    ax.legend(loc='lower right', fontsize=10.5, framealpha=0.94, facecolor='#ffffff', edgecolor='#cbd5e1',
              prop=font_prop)
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=2, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'ex2_12_airplane_climb.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
