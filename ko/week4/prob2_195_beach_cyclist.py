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

# Physical parameters (Meriam Dynamics 9th Ed. Problem 2/195)
vB_mag = 25.0       # km/h
th_B_deg = 15.0     # deg
th_B = np.radians(th_B_deg)

vw_mag = 32.0       # km/h
th_w_deg = 35.0     # deg
th_w = np.radians(th_w_deg)

vBx = vB_mag * np.sin(th_B)     # +6.4705 km/h
vBy = -vB_mag * np.cos(th_B)    # -24.1481 km/h

vwx = -vw_mag * np.sin(th_w)    # -18.3544 km/h
vwy = -vw_mag * np.cos(th_w)    # -26.2132 km/h

# (a) Relative velocity v_(w/B) = v_w - v_B
vwBx = vwx - vBx                # -24.8250 km/h
vwBy = vwy - vBy                # -2.0651 km/h
vwB_mag = np.hypot(vwBx, vwBy)  # 24.9108 km/h
rel_angle_deg = np.degrees(np.arctan2(np.abs(vwBy), np.abs(vwBx))) # 4.76 deg south of west

# (b) Perpendicular component from cyclist's left
un_x = -np.cos(th_B)
un_y = -np.sin(th_B)
v_cross = vwBx * un_x + vwBy * un_y # 24.5124 km/h

# Animation duration & trajectory
duration = 3.6
fps = 30
n_frames = int(fps * duration)
t_eval = np.linspace(0, duration, n_frames)

vBx_ms = vBx / 3.6
vBy_ms = vBy / 3.6

xB_traj = -2.0 + vBx_ms * t_eval
yB_traj = 34.0 + vBy_ms * t_eval

bushes = [
    (-28, 28), (-24, 12), (-29, -8), (-23, -24), (-27, -38),
    (-20, 38), (-18, -2), (-19, -32)
]

def draw_bush(ax, cx, cy, r=2.2):
    b1 = patches.Circle((cx, cy), r, fc='#84cc16', ec='#4d7c0f', lw=1.2, zorder=3)
    b2 = patches.Circle((cx - r*0.35, cy + r*0.2), r*0.7, fc='#65a30d', ec='none', zorder=4)
    b3 = patches.Circle((cx + r*0.3, cy - r*0.15), r*0.65, fc='#a3e635', ec='none', zorder=4)
    b4 = patches.Circle((cx, cy), r*0.4, fc='#4d7c0f', ec='none', zorder=5)
    ax.add_patch(b1)
    ax.add_patch(b2)
    ax.add_patch(b3)
    ax.add_patch(b4)

def draw_topdown_cyclist(ax, bx, by, angle_deg=15.0):
    tx, ty = np.sin(th_B), -np.cos(th_B)
    nx, ny = -np.cos(th_B), -np.sin(th_B)
    
    shadow = patches.Ellipse((bx + 0.4, by - 0.5), 3.2, 1.8, angle=-angle_deg,
                             fc='#000000', alpha=0.16, zorder=5)
    ax.add_patch(shadow)
    
    wb = 2.6
    rw_x, rw_y = bx - tx * (wb*0.5), by - ty * (wb*0.5)
    fw_x, fw_y = bx + tx * (wb*0.5), by + ty * (wb*0.5)
    
    tire_w, tire_l = 0.35, 1.3
    rw_patch = patches.Rectangle((rw_x - tire_w*0.5, rw_y - tire_l*0.5), tire_w, tire_l,
                                 angle=-angle_deg, fc='#1e293b', ec='#0f172a', lw=1.0, zorder=6)
    fw_patch = patches.Rectangle((fw_x - tire_w*0.5, fw_y - tire_l*0.5), tire_w, tire_l,
                                 angle=-angle_deg, fc='#1e293b', ec='#0f172a', lw=1.0, zorder=6)
    ax.plot([rw_x, fw_x], [rw_y, fw_y], color='#334155', lw=2.4, zorder=7)
    
    hb_len = 1.8
    hb_x1, hb_y1 = fw_x - nx * (hb_len*0.5), fw_y - ny * (hb_len*0.5)
    hb_x2, hb_y2 = fw_x + nx * (hb_len*0.5), fw_y + ny * (hb_len*0.5)
    ax.plot([hb_x1, hb_x2], [hb_y1, hb_y2], color='#0f172a', lw=2.2, zorder=8)
    
    torso_w, torso_l = 1.4, 1.9
    torso = patches.Ellipse((bx - tx*0.2, by - ty*0.2), torso_w, torso_l, angle=-angle_deg,
                            fc='#0284c7', ec='#0369a1', lw=1.4, zorder=9)
    ax.add_patch(torso)
    
    helmet = patches.Ellipse((bx + tx*0.35, by + ty*0.35), 0.95, 1.25, angle=-angle_deg,
                             fc='#ffffff', ec='#b91c1c', lw=1.3, zorder=10)
    ax.add_patch(helmet)
    ax.plot([bx + tx*0.1, bx + tx*0.6], [by + ty*0.1, by + ty*0.6], color='#ef4444', lw=2.0, zorder=11)
    
    ax.plot([bx - nx*0.5, hb_x1], [by - ny*0.5, hb_y1], color='#fed7aa', lw=1.8, zorder=9)
    ax.plot([bx + nx*0.5, hb_x2], [by + ny*0.5, hb_y2], color='#fed7aa', lw=1.8, zorder=9)
    
    ax.text(bx + nx*2.6, by + ny*2.6, r'$B$', fontsize=14, fontweight='bold',
            fontstyle='italic', color='#0f172a', ha='center', va='center', zorder=12)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

def update(frame):
    t = t_eval[frame]
    bx = -2.0 + vBx_ms * t
    by = 34.0 + vBy_ms * t
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-36, 48)
    ax.set_ylim(-44, 46)
    ax.axis('off')
    
    beach_bg = patches.Rectangle((-36, -44), 84, 90, fc='#fef3c7', ec='none', zorder=1)
    ax.add_patch(beach_bg)
    
    coast_y = np.linspace(-44, 46, 120)
    coast_x = 14.0 - 0.14 * coast_y + 2.4 * np.sin(coast_y * 0.07 + 0.3)
    sea_poly = np.vstack([np.column_stack([coast_x, coast_y]), [[55, 46], [55, -44]]])
    sea_patch = patches.Polygon(sea_poly, closed=True, fc='#bae6fd', ec='#38bdf8', lw=2.2, zorder=2)
    ax.add_patch(sea_patch)
    
    wave_x1 = coast_x - 1.2 + 0.6 * np.sin(coast_y * 0.25 + t * 3.2)
    ax.plot(wave_x1, coast_y, color='#ffffff', lw=2.8, alpha=0.9, zorder=3)
    wave_x2 = coast_x + 3.2 + 0.8 * np.sin(coast_y * 0.18 + t * 2.5)
    ax.plot(wave_x2, coast_y, color='#e0f2fe', lw=1.8, alpha=0.6, zorder=3)
    
    for bush_x, bush_y in bushes:
        draw_bush(ax, bush_x, bush_y, r=2.2)
    
    orig_x, orig_y = -28, -34
    ax.plot([orig_x, orig_x + 7.5], [orig_y, orig_y], color='#475569', linestyle='--', lw=1.6, zorder=5)
    ax.plot([orig_x, orig_x], [orig_y, orig_y + 7.5], color='#475569', linestyle='--', lw=1.6, zorder=5)
    ax.text(orig_x + 8.2, orig_y, '$x$', fontsize=12, fontweight='bold', color='#475569', va='center', zorder=6)
    ax.text(orig_x, orig_y + 8.4, '$y$', fontsize=12, fontweight='bold', color='#475569', ha='center', zorder=6)
    
    comp_x, comp_y = 32, 28
    ax.annotate('', xy=(comp_x, comp_y + 11.0), xytext=(comp_x, comp_y),
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=1.4, headwidth=5.5, headlength=7.5), zorder=6)
    ax.scatter([comp_x], [comp_y + 3.0], color='#ffffff', edgecolors='#0f172a', s=45, lw=1.5, zorder=7)
    ax.text(comp_x, comp_y + 12.5, '$N$', fontsize=13, fontweight='bold', fontstyle='italic', color='#0f172a', ha='center', va='bottom', zorder=7)
    
    w_dx, w_dy = -np.sin(th_w), -np.cos(th_w)
    wind_cluster = [
        (22, 18), (25, 14), (28, 10), (31, 6), (34, 2), (37, -2)
    ]
    w_shift = (t * 10.0) % 15.0
    w_arrow_len = 15.0
    for wx0, wy0 in wind_cluster:
        wx_start = wx0 + w_dx * w_shift
        wy_start = wy0 + w_dy * w_shift
        ax.annotate('', xy=(wx_start + w_dx * w_arrow_len, wy_start + w_dy * w_arrow_len),
                    xytext=(wx_start, wy_start),
                    arrowprops=dict(facecolor='#10b981', edgecolor='#059669', width=1.6, headwidth=5.5, headlength=6.5), zorder=5)
    
    ref_w_x, ref_w_y = 38, 2
    ax.plot([ref_w_x, ref_w_x], [ref_w_y, ref_w_y - 18], color='#0f172a', linestyle='-', lw=1.3, zorder=5)
    arc_w = patches.Arc((ref_w_x, ref_w_y), 24, 24, angle=270, theta1=0, theta2=35, color='#0f172a', lw=1.4, zorder=5)
    ax.add_patch(arc_w)
    ax.text(ref_w_x + 3.2, ref_w_y - 12.0, r'$35^\circ$', fontsize=11, fontweight='bold', color='#0f172a', zorder=6)
    ax.text(23, -6, r'$v_w$', fontsize=13, fontweight='bold', fontstyle='italic', color='#059669', zorder=6)
    
    past_idx = frame + 1
    ax.plot(xB_traj[:past_idx], yB_traj[:past_idx], color='#cbd5e1', linestyle='--', lw=2.0, zorder=4)
    
    ax.plot([bx, bx], [by, by - 16], color='#0f172a', linestyle='-', lw=1.2, zorder=6)
    arc_b = patches.Arc((bx, by), 20, 20, angle=270, theta1=-15, theta2=0, color='#0f172a', lw=1.4, zorder=6)
    ax.add_patch(arc_b)
    ax.text(bx + 1.6, by - 11.5, r'$15^\circ$', fontsize=10.5, fontweight='bold', color='#0f172a', zorder=7)
    
    draw_topdown_cyclist(ax, bx, by, th_B_deg)
    
    s_v = 0.52
    vBx_p, vBy_p = vBx * s_v, vBy * s_v
    ax.annotate('', xy=(bx + vBx_p, by + vBy_p), xytext=(bx, by),
                arrowprops=dict(facecolor='#10b981', edgecolor='#047857', width=2.0, headwidth=6.0, headlength=7.0), zorder=14)
    ax.text(bx + vBx_p + 1.2, by + vBy_p + 1.0, r'$v_B$', fontsize=13, fontweight='bold', fontstyle='italic', color='#047857', zorder=15)
    
    vwBx_p, vwBy_p = vwBx * s_v, vwBy * s_v
    ax.annotate('', xy=(bx + vwBx_p, by + vwBy_p), xytext=(bx, by),
                arrowprops=dict(facecolor='#f97316', edgecolor='#c2410c', width=2.2, headwidth=6.5, headlength=7.5), zorder=16)
    ax.text(bx + vwBx_p - 1.5, by + vwBy_p - 2.5, r'$\mathbf{v}_{w/B} = 24.9\text{ km/h}$',
            fontsize=10.5, fontweight='bold', color='#c2410c', ha='right', zorder=17)
    
    vcx_p = un_x * v_cross * s_v
    vcy_p = un_y * v_cross * s_v
    ax.annotate('', xy=(bx + vcx_p, by + vcy_p), xytext=(bx, by),
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=2.0, headwidth=6.0, headlength=7.0), zorder=15)
    ax.text(bx + vcx_p - 2.0, by + vcy_p + 2.2, r'$\mathbf{v}_{\mathrm{cross}} = 24.5\text{ km/h}$',
            fontsize=10.0, fontweight='bold', color='#7e22ce', ha='right', zorder=16)
    
    ax.plot([bx + vwBx_p, bx + vcx_p], [by + vwBy_p, by + vcy_p], color='#7e22ce', linestyle=':', lw=1.5, zorder=13)
    
    if "ko" == "ko":
        hud_str = (
            f"[문제 2/195 해변 자전거-풍속 상대운동]\n"
            f"시간 t = {t:4.2f} s / {duration:.1f} s\n"
            f"-----------------------------------------\n"
            f"자전거 속도:  v_B = {vB_mag:.1f} km/h (남동 15°)\n"
            f"바람 속도:    v_w = {vw_mag:.1f} km/h (남서 35°)\n"
            f"-----------------------------------------\n"
            f"▶ (a) 상대풍속: v_(w/B) = v_w - v_B\n"
            f"      = 24.9 km/h (서남서 4.8°)\n"
            f"▶ (b) 좌측 직각 측풍 성분: v_cross\n"
            f"      = v_(w/B) · e_n = 24.5 km/h"
        )
        title_text = '[동역학 9판 문제 2/195] 해변 자전거 탑승자와 바람의 2차원 상대속도 및 측풍 해석'
    else:
        hud_str = (
            f"[Problem 2/195 Beach Cyclist Relative Velocity]\n"
            f"Time t = {t:4.2f} s / {duration:.1f} s\n"
            f"-----------------------------------------\n"
            f"Cyclist Speed: v_B = {vB_mag:.1f} km/h (15° E of S)\n"
            f"Wind Speed:    v_w = {vw_mag:.1f} km/h (35° W of S)\n"
            f"-----------------------------------------\n"
            f"▶ (a) Rel Wind: v_(w/B) = v_w - v_B\n"
            f"      = 24.9 km/h (4.8° S of W)\n"
            f"▶ (b) Left Crosswind Component: v_cross\n"
            f"      = v_(w/B) · e_n = 24.5 km/h"
        )
        title_text = '[Meriam Dynamics 9th Ed. Prob 2/195] 2D Relative Velocity Analysis of Beach Cyclist & Wind'
    
    ax.text(-34, 44, hud_str, fontsize=8.8, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=20,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#eab308', lw=1.5, alpha=0.95))
    
    deriv_box = patches.FancyBboxPatch((-34, -42), 43, 34,
                                       boxstyle="round,pad=0.8", fc="#ffffff", ec='#0284c7', lw=1.5, alpha=0.95, zorder=19)
    ax.add_patch(deriv_box)
    
    d_title = '상대속도 및 벡터 분해 해석 (Derivation)' if "ko" == "ko" else 'Vector Resolution & Derivation'
    ax.text(-12.5, -10.0, f'[{{d_title}}]', fontsize=9.2, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=20)
    
    if "ko" == "ko":
        eq1 = r'1) 직교 성분 분해 (+x 동쪽, +y 북쪽):\n   $\mathbf{v}_B = 25(\sin 15^\circ\mathbf{i} - \cos 15^\circ\mathbf{j}) = 6.47\mathbf{i} - 24.15\mathbf{j}$\n   $\mathbf{v}_w = 32(-\sin 35^\circ\mathbf{i} - \cos 35^\circ\mathbf{j}) = -18.35\mathbf{i} - 26.21\mathbf{j}$'
        eq2 = r'2) (a) 상대속도 벡터 ($\mathbf{v}_{w/B} = \mathbf{v}_w - \mathbf{v}_B$):\n   $\mathbf{v}_{w/B} = -24.83\mathbf{i} - 2.07\mathbf{j}\text{ km/h}$\n   ▶ $|\mathbf{v}_{w/B}| = \mathbf{24.9\text{ km/h}}$' + ' (서쪽 기준 남향 4.8°)'
        eq3 = r'3) (b) 좌측 법선 단위벡터 $\mathbf{e}_n$:\n   $\mathbf{e}_n = -\cos 15^\circ\mathbf{i} - \sin 15^\circ\mathbf{j}$\n   ▶ $v_{\text{cross}} = \mathbf{v}_{w/B} \cdot \mathbf{e}_n = \mathbf{24.5\text{ km/h}}$'
    else:
        eq1 = r'1) Coordinate Components (+x East, +y North):\n   $\mathbf{v}_B = 25(\sin 15^\circ\mathbf{i} - \cos 15^\circ\mathbf{j}) = 6.47\mathbf{i} - 24.15\mathbf{j}$\n   $\mathbf{v}_w = 32(-\sin 35^\circ\mathbf{i} - \cos 35^\circ\mathbf{j}) = -18.35\mathbf{i} - 26.21\mathbf{j}$'
        eq2 = r'2) (a) Relative Velocity ($\mathbf{v}_{w/B} = \mathbf{v}_w - \mathbf{v}_B$):\n   $\mathbf{v}_{w/B} = -24.83\mathbf{i} - 2.07\mathbf{j}\text{ km/h}$\n   ▶ $|\mathbf{v}_{w/B}| = \mathbf{24.9\text{ km/h}}$' + ' (4.8° S of W)'
        eq3 = r'3) (b) Left Normal Unit Vector $\mathbf{e}_n$:\n   $\mathbf{e}_n = -\cos 15^\circ\mathbf{i} - \sin 15^\circ\mathbf{j}$\n   ▶ $v_{\text{cross}} = \mathbf{v}_{w/B} \cdot \mathbf{e}_n = \mathbf{24.5\text{ km/h}}$'
    
    ax.text(-32.5, -17.0, eq1, fontsize=7.6, color='#1e293b', fontproperties=font_prop, zorder=20)
    ax.text(-32.5, -26.5, eq2, fontsize=7.6, color='#1e293b', fontproperties=font_prop, zorder=20)
    ax.text(-32.5, -36.0, eq3, fontsize=7.6, color='#b91c1c', fontweight='bold', fontproperties=font_prop, zorder=20)
    
    tri_box = patches.FancyBboxPatch((18, -38), 28, 22,
                                     boxstyle="round,pad=0.6", fc="#ffffff", ec='#64748b', lw=1.2, alpha=0.92, zorder=18)
    ax.add_patch(tri_box)
    vtri_title = '[벡터 삼각형 다이어그램]' if "ko" == "ko" else '[Vector Triangle]'
    ax.text(32, -18.5, vtri_title,
            fontsize=8.4, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=19)
    
    tri_ox, tri_oy = 28, -22
    sc_tri = 0.38
    ax.annotate('', xy=(tri_ox + vBx*sc_tri, tri_oy + vBy*sc_tri), xytext=(tri_ox, tri_oy),
                arrowprops=dict(facecolor='#10b981', edgecolor='#047857', width=1.5, headwidth=4.5, headlength=5.5), zorder=20)
    ax.text(tri_ox + vBx*sc_tri*0.5 + 1.2, tri_oy + vBy*sc_tri*0.5, r'$\mathbf{v}_B$', fontsize=9, fontweight='bold', color='#047857', zorder=21)
    
    ax.annotate('', xy=(tri_ox + vwx*sc_tri, tri_oy + vwy*sc_tri), xytext=(tri_ox, tri_oy),
                arrowprops=dict(facecolor='#0284c7', edgecolor='#0369a1', width=1.5, headwidth=4.5, headlength=5.5), zorder=20)
    ax.text(tri_ox + vwx*sc_tri*0.5 - 1.2, tri_oy + vwy*sc_tri*0.5 - 1.2, r'$\mathbf{v}_w$', fontsize=9, fontweight='bold', color='#0369a1', zorder=21)
    
    ax.annotate('', xy=(tri_ox + vwx*sc_tri, tri_oy + vwy*sc_tri), xytext=(tri_ox + vBx*sc_tri, tri_oy + vBy*sc_tri),
                arrowprops=dict(facecolor='#f97316', edgecolor='#c2410c', width=1.8, headwidth=5.0, headlength=6.0), zorder=20)
    ax.text(tri_ox + (vBx + vwx)*sc_tri*0.5, tri_oy + (vBy + vwy)*sc_tri*0.5 - 2.2, r'$\mathbf{v}_{w/B}$',
            fontsize=9.5, fontweight='bold', color='#c2410c', ha='center', zorder=21)
    
    plt.title(title_text, fontsize=12.2, fontweight='bold', pad=6, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'prob2_195_beach_cyclist.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
