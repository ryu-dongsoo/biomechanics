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

RA = 75.0
RB = 105.0
vA_kmh = 40.0
vB_kmh = 80.0
vA_ms = vA_kmh / 3.6
vB_ms = vB_kmh / 3.6

fps = 30
duration = 3.5
n_frames = int(fps * duration)
t_eval = np.linspace(-1.5, 1.5, n_frames)

def draw_car(ax, x, y, angle_deg, color='#38bdf8', edge_col='#0284c7', scale=1.0):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    def rot(dx, dy):
        return x + dx*c - dy*s, y + dx*s + dy*c
    
    L, W = 11.0 * scale, 5.5 * scale
    bx = np.array([-L/2, L/2 - 1.5, L/2, L/2 - 1.5, -L/2, -L/2])
    by = np.array([-W/2, -W/2, 0, W/2, W/2, -W/2])
    px, py = rot(bx, by)
    ax.fill(px, py, color=color, ec=edge_col, lw=1.6, zorder=7)
    
    rx = np.array([-L/4, L/4, L/4 - 0.8, -L/4 + 0.8])
    ry = np.array([-W/2.6, -W/2.6, W/2.6, W/2.6])
    rpx, rpy = rot(rx, ry)
    ax.fill(rpx, rpy, color='#1e293b', alpha=0.7, zorder=8)
    
    wx = np.array([L/4, L/4 + 1.5, L/4 + 1.5, L/4])
    wy = np.array([-W/3, -W/3.5, W/3.5, W/3])
    wpx, wpy = rot(wx, wy)
    ax.fill(wpx, wpy, color='#bae6fd', zorder=9)
    
    for hy in [-W/2.6, W/2.6]:
        hpx, hpy = rot(L/2 - 0.5, hy)
        ax.plot([hpx], [hpy], 'o', color='#fef08a', markersize=3.0, zorder=9)

fig = plt.figure(figsize=(10.5, 7.5), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.95])

def update(frame):
    t = t_eval[frame]
    ang_A_rad = np.radians(45.0) - (vA_ms * t) / RA
    ang_A_deg = np.degrees(ang_A_rad)
    xA = RA * np.cos(ang_A_rad)
    yA = RA * np.sin(ang_A_rad)
    head_A_deg = ang_A_deg - 90.0
    
    ang_B_rad = np.radians(-30.0) + (vB_ms * t) / RB
    ang_B_deg = np.degrees(ang_B_rad)
    xB = RB * np.cos(ang_B_rad)
    yB = RB * np.sin(ang_B_rad)
    head_B_deg = ang_B_deg + 90.0
    
    dx = xA - xB
    dy = yA - yB
    r_val = np.hypot(dx, dy)
    phi_r_rad = np.arctan2(dy, dx)
    theta_rad = phi_r_rad - np.radians(head_B_deg)
    theta_deg = np.degrees(theta_rad)
    
    vAx = vA_ms * np.sin(ang_A_rad)
    vAy = -vA_ms * np.cos(ang_A_rad)
    vBx = -vB_ms * np.sin(ang_B_rad)
    vBy = vB_ms * np.cos(ang_B_rad)
    v_rel_x = vAx - vBx
    v_rel_y = vAy - vBy
    
    er_x, er_y = dx / r_val, dy / r_val
    et_x, et_y = -er_y, er_x
    r_dot = v_rel_x * er_x + v_rel_y * er_y
    v_trans = v_rel_x * et_x + v_rel_y * et_y
    phi_r_dot = v_trans / r_val
    omega_B = vB_ms / RB
    theta_dot = phi_r_dot - omega_B
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-75, 135)
    ax.set_ylim(-85, 95)
    ax.axis('off')
    
    bg_rect = patches.Rectangle((-75, -85), 210, 180, color='#dcfce7', zorder=1)
    ax.add_patch(bg_rect)
    
    th_road = np.linspace(-np.pi/2, np.pi/2, 100)
    out_inner_x, out_inner_y = 98 * np.cos(th_road), 98 * np.sin(th_road)
    out_outer_x, out_outer_y = 112 * np.cos(th_road), 112 * np.sin(th_road)
    out_road_poly = patches.Polygon(np.column_stack([
        np.concatenate([out_inner_x, out_outer_x[::-1]]),
        np.concatenate([out_inner_y, out_outer_y[::-1]])
    ]), color='#cbd5e1', ec='#94a3b8', lw=1.5, zorder=2)
    ax.add_patch(out_road_poly)
    ax.plot(105 * np.cos(th_road), 105 * np.sin(th_road), color='#ffffff', linestyle='--', lw=1.5, zorder=3)
    
    in_inner_x, in_inner_y = 68 * np.cos(th_road), 68 * np.sin(th_road)
    in_outer_x, in_outer_y = 82 * np.cos(th_road), 82 * np.sin(th_road)
    in_road_poly = patches.Polygon(np.column_stack([
        np.concatenate([in_inner_x, in_outer_x[::-1]]),
        np.concatenate([in_inner_y, in_outer_y[::-1]])
    ]), color='#cbd5e1', ec='#94a3b8', lw=1.5, zorder=2)
    ax.add_patch(in_road_poly)
    ax.plot(75 * np.cos(th_road), 75 * np.sin(th_road), color='#ffffff', linestyle='--', lw=1.5, zorder=3)
    
    ax.plot([0, 125], [0, 0], color='#64748b', linestyle='--', lw=1.5, zorder=4)
    ax.text(128, -2, '$x$', fontsize=13, fontweight='bold', color='#1e293b')
    ax.plot([0, 0], [-70, 85], color='#64748b', linestyle='--', lw=1.5, zorder=4)
    ax.text(-2, 88, '$y$', fontsize=13, fontweight='bold', color='#1e293b')
    ax.scatter([0], [0], color='#0f172a', s=45, zorder=6)
    ax.text(-8, -8, '$O$', fontsize=13, fontweight='bold', color='#0f172a')
    
    ax.plot([0, 75 * np.cos(np.radians(45.0))], [0, 75 * np.sin(np.radians(45.0))], color='#0f172a', lw=1.4, zorder=4)
    ax.plot([0, 105 * np.cos(np.radians(-30.0))], [0, 105 * np.sin(np.radians(-30.0))], color='#0f172a', lw=1.4, zorder=4)
    
    arc_45 = np.linspace(0, np.radians(45.0), 20)
    ax.plot(35 * np.cos(arc_45), 35 * np.sin(arc_45), color='#0f172a', lw=1.4, zorder=5)
    ax.text(38 * np.cos(np.radians(22.5)), 38 * np.sin(np.radians(22.5)), '$45^\\circ$',
            fontsize=11.5, fontweight='bold', color='#0f172a')
    
    arc_30 = np.linspace(np.radians(-30.0), 0, 20)
    ax.plot(35 * np.cos(arc_30), 35 * np.sin(arc_30), color='#0f172a', lw=1.4, zorder=5)
    ax.text(38 * np.cos(np.radians(-15.0)), 38 * np.sin(np.radians(-15.0)), '$30^\\circ$',
            fontsize=11.5, fontweight='bold', color='#0f172a')
    
    ax.text(48 * np.cos(np.radians(-42.0)), 48 * np.sin(np.radians(-42.0)), '75 m', fontsize=11.0, fontweight='bold', color='#0f172a')
    ax.text(78 * np.cos(np.radians(-38.0)), 78 * np.sin(np.radians(-38.0)), '105 m', fontsize=11.0, fontweight='bold', color='#0f172a')
    
    for arr_ang in [65, 30, -5]:
        rad_arr = np.radians(arr_ang)
        ax_x, ax_y = 75 * np.cos(rad_arr), 75 * np.sin(rad_arr)
        tang_x, tang_y = np.sin(rad_arr) * 8, -np.cos(rad_arr) * 8
        ax.annotate('', xy=(ax_x + tang_x, ax_y + tang_y), xytext=(ax_x - tang_x, ax_y - tang_y),
                    arrowprops=dict(arrowstyle="-|>", color='#f97316', lw=2.0, mutation_scale=12), zorder=4)
    
    for arr_ang in [-50, -15, 20]:
        rad_arr = np.radians(arr_ang)
        ax_x, ax_y = 105 * np.cos(rad_arr), 105 * np.sin(rad_arr)
        tang_x, tang_y = -np.sin(rad_arr) * 8, np.cos(rad_arr) * 8
        ax.annotate('', xy=(ax_x + tang_x, ax_y + tang_y), xytext=(ax_x - tang_x, ax_y - tang_y),
                    arrowprops=dict(arrowstyle="-|>", color='#f97316', lw=2.0, mutation_scale=12), zorder=4)
    
    ax.plot([xB, xA], [yB, yA], color='#0f172a', linestyle='-', lw=1.8, zorder=5)
    ax.text((xB + xA)*0.5 + 4, (yB + yA)*0.5, '$r$', fontsize=13, fontweight='bold', color='#0f172a')
    
    tan_B_rad = np.radians(head_B_deg)
    ax.plot([xB, xB + 35 * np.cos(tan_B_rad)], [yB, yB + 35 * np.sin(tan_B_rad)],
            color='#16a34a', linestyle='--', lw=1.5, zorder=5)
    
    th_start = np.radians(head_B_deg)
    th_end = phi_r_rad
    arc_th = np.linspace(min(th_start, th_end), max(th_start, th_end), 20)
    ax.plot(xB + 22 * np.cos(arc_th), yB + 22 * np.sin(arc_th), color='#b91c1c', lw=1.6, zorder=6)
    mid_th = (th_start + th_end) * 0.5
    ax.text(xB + 26 * np.cos(mid_th), yB + 26 * np.sin(mid_th), '$\\theta$',
            fontsize=12.5, fontweight='bold', color='#b91c1c')
    
    draw_car(ax, xA, yA, angle_deg=head_A_deg, color='#38bdf8', edge_col='#0284c7', scale=1.1)
    ax.text(xA + 12 * np.cos(np.radians(head_A_deg + 90)), yA + 12 * np.sin(np.radians(head_A_deg + 90)),
            '$A$', fontsize=14, fontweight='bold', color='#0284c7', ha='center', va='center', zorder=10)
    
    ax.quiver(xA, yA, vAx * 1.5, vAy * 1.5, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.008, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(xA + vAx * 1.7 + 3, yA + vAy * 1.7 - 2, '$v_A = 40\\text{ km/h}$',
            fontsize=10.5, fontweight='bold', color='#16a34a')
    
    draw_car(ax, xB, yB, angle_deg=head_B_deg, color='#ef4444', edge_col='#991b1b', scale=1.1)
    ax.text(xB + 12 * np.cos(np.radians(head_B_deg - 90)), yB + 12 * np.sin(np.radians(head_B_deg - 90)),
            '$B$', fontsize=14, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=10)
    
    ax.quiver(xB, yB, vBx * 1.2, vBy * 1.2, angles='xy', scale_units='xy', scale=1,
              color='#16a34a', width=0.008, headwidth=4.5, headlength=5.5, zorder=10)
    ax.text(xB + vBx * 1.3 + 3, yB + vBy * 1.3, '$v_B = 80\\text{ km/h}$',
            fontsize=10.5, fontweight='bold', color='#16a34a')
    
    if "ko" == "ko":
        hud_str = (
            f"[문제 2/160 극좌표 상대운동 해석]\n"
            f"시간 t = {t:4.2f} s / 1.50 s\n"
            f"----------------------------------------\n"
            f"자동차 A (R=75m):  v_A = 40.0 km/h (11.1 m/s)\n"
            f"자동차 B (R=105m): v_B = 80.0 km/h (22.2 m/s)\n"
            f"상대거리 r:        {r_val:5.1f} m\n"
            f"상대각도 θ:        {theta_deg:5.1f}° (B 장축 기준)\n"
            f"----------------------------------------\n"
            f"▶ 순간 거리변화율 dr/dt: {r_dot:5.2f} m/s\n"
            f"▶ 순간 각속도   dθ/dt: {theta_dot:6.4f} rad/s"
        )
        title_text = '[동역학 9판 문제 2/160] 2차원 원형 트랙 자동차 상대속도 및 각속도 해석'
    else:
        hud_str = (
            f"[Problem 2/160 Relative Motion]\n"
            f"Time t = {t:4.2f} s / 1.50 s\n"
            f"----------------------------------------\n"
            f"Car A (R=75m):  v_A = 40.0 km/h (11.1 m/s)\n"
            f"Car B (R=105m): v_B = 80.0 km/h (22.2 m/s)\n"
            f"Distance r:     {r_val:5.1f} m\n"
            f"Relative Angle: {theta_deg:5.1f}° (re: B axis)\n"
            f"----------------------------------------\n"
            f"▶ Radial Rate   dr/dt: {r_dot:5.2f} m/s\n"
            f"▶ Angular Rate dθ/dt: {theta_dot:6.4f} rad/s"
        )
        title_text = '[Meriam Dynamics 9th Ed. Prob 2/160] Relative Velocity & Angular Rate of Cars'
    
    ax.text(-72, 90, hud_str, fontsize=9.0, family='monospace',
            verticalalignment='top', fontproperties=font_prop, zorder=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#0284c7', lw=1.5, alpha=0.94))
    
    deriv_box = patches.FancyBboxPatch((-72.5, -82), 68, 48,
                                       boxstyle="round,pad=1.5", fc="#ffffff", ec='#ea580c', lw=1.5, alpha=0.94, zorder=9)
    ax.add_patch(deriv_box)
    
    d_title = '극좌표 상대속도 풀이 (Solution)' if "ko" == "ko" else 'Polar Relative Kinematics'
    ax.text(-38.5, -38, f'[{{d_title}}]', fontsize=9.2, fontweight='bold', color='#0f172a', ha='center', fontproperties=font_prop, zorder=10)
    
    if "ko" == "ko":
        eq1 = '1) 상대속도: $\\mathbf{v}_{A/B} = \\mathbf{v}_A - \\mathbf{v}_B = -3.25\\mathbf{i} - 27.10\\mathbf{j}$'
        eq2 = '2) 지선거리 변화율: $\\dot{r} = \\mathbf{v}_{A/B} \\cdot \\mathbf{e}_r = \\mathbf{-24.41\\text{ m/s}}$'
        eq3 = '3) 회전각속도: $\\dot{\\theta} = \\frac{v_\\phi}{r} - \\omega_B = \\mathbf{-0.1026\\text{ rad/s}}$'
    else:
        eq1 = '1) Rel. Vel: $\\mathbf{v}_{A/B} = \\mathbf{v}_A - \\mathbf{v}_B = -3.25\\mathbf{i} - 27.10\\mathbf{j}$'
        eq2 = '2) Radial Rate: $\\dot{r} = \\mathbf{v}_{A/B} \\cdot \\mathbf{e}_r = \\mathbf{-24.41\\text{ m/s}}$'
        eq3 = '3) Angular Rate: $\\dot{\\theta} = \\frac{v_\\phi}{r} - \\omega_B = \\mathbf{-0.1026\\text{ rad/s}}$'
    
    ax.text(-71, -47, eq1, fontsize=8.2, color='#1e293b', fontproperties=font_prop, zorder=10)
    ax.text(-71, -59, eq2, fontsize=8.5, color='#b91c1c', fontweight='bold', fontproperties=font_prop, zorder=10)
    ax.text(-71, -71, eq3, fontsize=8.5, color='#16a34a', fontweight='bold', fontproperties=font_prop, zorder=10)
    
    plt.title(title_text, fontsize=12.5, fontweight='bold', pad=6, fontproperties=font_prop)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps)
    writer = PillowWriter(fps=fps)
    out_gif = os.path.join(os.path.dirname(__file__), 'prob2_160_cars_intersection.gif')
    anim.save(out_gif, writer=writer)
    plt.close()
