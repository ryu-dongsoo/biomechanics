# Problem 2/135: Helical Motion of Corkscrew Roller Coaster
# Exact 100% reproduction of textbook illustration geometry, cylinder orientation, rail start/endpoint A, vehicle trajectory, and acceleration vectors

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# Parameters
r_cyl = 5.0
gamma_deg = 40.0
gamma_rad = np.radians(gamma_deg)
v_A = 15.0
g = 9.81

rho_A = r_cyl / (np.cos(gamma_rad)**2)
at_A = g * np.cos(gamma_rad)
an_A = (v_A**2) / rho_A
a_mag_A = np.sqrt(at_A**2 + an_A**2)

fig, ax = plt.subplots(figsize=(12.8, 7.5))
fig.subplots_adjust(left=0.02, right=0.65, bottom=0.04, top=0.96)
ax.set_facecolor('#ebf5fb')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-12, 28)
ax.set_ylim(-14, 15)

ang_ax = np.radians(20.0)
e_X = np.array([np.cos(ang_ax), np.sin(ang_ax)])
ang_Y = np.radians(-35.0)
e_Y = np.array([np.cos(ang_Y), np.sin(ang_Y)])
e_Z = np.array([0.0, 1.0])

xA = 16.0
L_cyl = 23.0

def to_2d(X, Y, Z):
    return X * e_X[0] + Y * e_Y[0] + Z * e_Z[0], X * e_X[1] + Y * e_Y[1] + Z * e_Z[1]

th_sample = np.linspace(0, 2*np.pi, 100)
xl_rim, yl_rim = to_2d(0, r_cyl*np.cos(th_sample), r_cyl*np.sin(th_sample))
xr_rim, yr_rim = to_2d(L_cyl, r_cyl*np.cos(th_sample), r_cyl*np.sin(th_sample))

xt_l, yt_l = to_2d(0, 0, r_cyl)
xt_r, yt_r = to_2d(L_cyl, 0, r_cyl)
xb_l, yb_l = to_2d(0, 0, -r_cyl)
xb_r, yb_r = to_2d(L_cyl, 0, -r_cyl)

cyl_poly = patches.Polygon([[xt_l, yt_l], [xt_r, yt_r], [xb_r, yb_r], [xb_l, yb_l]],
                           facecolor='#e1f1fa', edgecolor='#aed6f1', lw=1.2, alpha=0.55, zorder=1)
ax.add_patch(cyl_poly)

cap_poly = patches.Polygon(np.column_stack([xl_rim, yl_rim]),
                           facecolor='#c7e4f7', edgecolor='#7fb3d5', lw=1.6, alpha=0.75, zorder=2)
ax.add_patch(cap_poly)

ax.plot(xr_rim, yr_rim, color='#aed6f1', lw=1.2, zorder=2)
ax.plot([xt_l, xt_r], [yt_l, yt_r], color='#aed6f1', lw=1.2, zorder=2)
ax.plot([xb_l, xb_r], [yb_l, yb_r], color='#aed6f1', lw=1.2, zorder=2)

ax_s_x, ax_s_y = to_2d(-4, 0, 0)
ax_e_x, ax_e_y = to_2d(L_cyl + 4, 0, 0)
ax.plot([ax_s_x, ax_e_x], [ax_s_y, ax_e_y], 'k--', lw=1.2, alpha=0.75, zorder=3)

t1_x, t1_y = to_2d(7.0, 0, 0)
t2_x, t2_y = to_2d(12.5, 0, 0)
ax.text(t1_x, t1_y + 0.6, 'Horizontal', fontsize=10, color='#2c3e50', ha='center', va='bottom')
ax.text(t2_x, t2_y + 0.6, 'Horizontal', fontsize=10, color='#2c3e50', ha='center', va='bottom')

zv_top_x, zv_top_y = to_2d(0, 0, r_cyl + 2.5)
zv_bot_x, zv_bot_y = to_2d(0, 0, -r_cyl - 2.5)
ax.plot([zv_top_x, zv_bot_x], [zv_top_y, zv_bot_y], 'k-.', lw=1.0, alpha=0.7, zorder=3)

yh_x, yh_y = to_2d(0, r_cyl, 0)
ax.plot([0, yh_x], [0, yh_y], 'k--', lw=1.0, alpha=0.7, zorder=3)

d_s_x, d_s_y = to_2d(0, 0, 0)
d_e_x, d_e_y = to_2d(0, 0, -r_cyl)
ax.annotate('', xy=(d_e_x + 0.6, d_e_y), xytext=(d_s_x + 0.6, d_s_y),
            arrowprops=dict(arrowstyle='<->,head_width=0.15,head_length=0.35', color='black', lw=0.8, mutation_scale=8), zorder=4)
ax.plot([d_s_x + 0.2, d_s_x + 1.0], [d_s_y, d_s_y], 'k-', lw=0.8, zorder=4)
ax.plot([d_e_x + 0.2, d_e_x + 1.0], [d_e_y, d_e_y], 'k-', lw=0.8, zorder=4)
ax.text(d_s_x + 1.3, (d_s_y + d_e_y)*0.5, '5 m', fontsize=11, va='center', color='#2c3e50')

pA_x, pA_y = to_2d(xA, r_cyl, 0)
pAc_x, pAc_y = to_2d(xA, 0, 0)
ax.plot([pAc_x, pA_x], [pAc_y, pA_y], 'k--', lw=1.0, alpha=0.7, zorder=3)
ax.plot([pA_x], [pA_y], 'ko', markersize=6.5, zorder=10)
ax.text(pA_x + 0.4, pA_y + 0.6, '$A$', fontsize=15, fontfamily='serif', fontweight='bold', color='#1a5276', zorder=10)

v_top_x, v_top_y = to_2d(xA, r_cyl, 1.8)
v_bot_x, v_bot_y = to_2d(xA, r_cyl, -5.2)
ax.plot([v_top_x, v_bot_x], [v_top_y, v_bot_y], 'k-', lw=1.0, alpha=0.75, zorder=4)
ax.text(v_bot_x - 0.2, v_bot_y - 0.5, 'Vertical', fontsize=10, ha='right', va='top', color='#2c3e50')

u_tang_2d = np.sin(gamma_rad) * e_X - np.cos(gamma_rad) * e_Z
tang_s = np.array([pA_x, pA_y]) - 2.5 * u_tang_2d
tang_e = np.array([pA_x, pA_y]) + 4.8 * u_tang_2d
ax.plot([tang_s[0], tang_e[0]], [tang_s[1], tang_e[1]], 'k:', lw=1.0, zorder=4)

arc_x = pA_x + 3.4 * np.sin(np.linspace(0, gamma_rad, 20)) * e_X[0]
arc_y = pA_y + 3.4 * np.sin(np.linspace(0, gamma_rad, 20)) * e_X[1] - 3.4 * np.cos(np.linspace(0, gamma_rad, 20))
ax.plot(arc_x, arc_y, 'k-', lw=1.0, zorder=4)
ax.text(pA_x + 1.8, pA_y - 4.0, r'$\gamma = 40^\circ$', fontsize=11, fontweight='bold', color='#2c3e50')

th_rail = np.linspace(1.18 * np.pi, -0.45 * np.pi, 300)
X_rail = xA - r_cyl * np.tan(gamma_rad) * th_rail
Y_rail = r_cyl * np.cos(th_rail)
Z_rail = r_cyl * np.sin(th_rail)

r_2d_x, r_2d_y = to_2d(X_rail, Y_rail, Z_rail)
ax.plot(r_2d_x, r_2d_y, color='#7f8c8d', lw=2.8, alpha=0.9, zorder=5)
ax.plot([r_2d_x[0]], [r_2d_y[0]], 'o', color='#7f8c8d', markersize=3.5, zorder=6)

idx_arr = 160
p_arr_tail = np.array([r_2d_x[idx_arr], r_2d_y[idx_arr]]) + np.array([0.9, 0.9])
p_arr_head = p_arr_tail + 2.8 * u_tang_2d
ax.annotate('', xy=(p_arr_head[0], p_arr_head[1]), xytext=(p_arr_tail[0], p_arr_tail[1]),
            arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.45', color='#27ae60', lw=2.0, mutation_scale=10), zorder=6)

info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

dynamic_artists = []

frames = 110
th_cars = np.linspace(1.10 * np.pi, 0.0, frames)

def animate(i):
    global dynamic_artists
    for art in dynamic_artists: art.remove()
    dynamic_artists.clear()

    th_c = th_cars[i]
    for k in range(5):
        d_th = (k - 2) * 0.08
        th_k = th_c + d_th
        X_k = xA - r_cyl * np.tan(gamma_rad) * th_k
        Y_k = r_cyl * np.cos(th_k)
        Z_k = r_cyl * np.sin(th_k)
        cx, cy = to_2d(X_k, Y_k, Z_k)
        
        tang_k_2d = np.sin(gamma_rad)*e_X - np.cos(gamma_rad)*np.sin(th_k)*e_Y - np.cos(gamma_rad)*np.cos(th_k)*e_Z
        ang_k_deg = np.degrees(np.arctan2(tang_k_2d[1], tang_k_2d[0]))

        box = patches.Rectangle((cx - 0.45, cy - 0.35), 0.9, 0.7, angle=ang_k_deg,
                                facecolor='#e74c3c', edgecolor='#78281f', lw=1.2, zorder=8)
        ax.add_patch(box)
        dynamic_artists.append(box)

    X_head = xA - r_cyl * np.tan(gamma_rad) * th_c
    Y_head = r_cyl * np.cos(th_c)
    Z_head = r_cyl * np.sin(th_c)
    p_head_x, p_head_y = to_2d(X_head, Y_head, Z_head)

    tang_head = np.sin(gamma_rad)*e_X - np.cos(gamma_rad)*np.sin(th_c)*e_Y - np.cos(gamma_rad)*np.cos(th_c)*e_Z
    norm_head = -np.cos(th_c)*e_Y - np.sin(th_c)*e_Z

    v_scale = 0.22
    v_patch = patches.FancyArrowPatch((p_head_x, p_head_y),
                                      (p_head_x + v_A * tang_head[0] * v_scale, p_head_y + v_A * tang_head[1] * v_scale),
                                      arrowstyle='->,head_width=0.25,head_length=0.45', color='#27ae60', lw=2.4, mutation_scale=10, zorder=12)
    ax.add_patch(v_patch)
    txt_v = ax.text(p_head_x + v_A * tang_head[0] * v_scale + 0.4, p_head_y + v_A * tang_head[1] * v_scale,
                    r'$\mathbf{v}$', color='#27ae60', fontsize=12, fontweight='bold', va='center')
    dynamic_artists.extend([v_patch, txt_v])

    a_scale = 0.12
    a_tot_2d = at_A * tang_head + an_A * norm_head
    a_patch = patches.FancyArrowPatch((p_head_x, p_head_y),
                                      (p_head_x + a_tot_2d[0] * a_scale, p_head_y + a_tot_2d[1] * a_scale),
                                      arrowstyle='->,head_width=0.25,head_length=0.45', color='#c0392b', lw=2.4, mutation_scale=10, zorder=12)
    ax.add_patch(a_patch)
    txt_a = ax.text(p_head_x + a_tot_2d[0] * a_scale + 0.4, p_head_y + a_tot_2d[1] * a_scale,
                    r'$\mathbf{a}$', color='#c0392b', fontsize=12, fontweight='bold', va='center')
    dynamic_artists.extend([a_patch, txt_a])

    is_final = (i == frames - 1)
    status_hdr = "★ [Homework Task & Exact Answers (Point A)] ★" if is_final else "■ [Problem 2/135: Corkscrew Coaster Kinematics]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【Geometry & Conditions】\n"
        f" • Cylinder radius: $r = {r_cyl:.1f}$ m\n"
        f" • Helix angle: $\\gamma = {gamma_deg:.1f}^\\circ$\n"
        f" • Speed at A: $v = {v_A:.1f}$ m/s\n"
        f" • Tangential component: $a_t = g\\cos\\gamma$\n"
        f"─────────────────────────────────────\n"
        f"【Real-time Monitoring】\n"
        f" • Position: $\\theta = {np.degrees(th_c):.1f}^\\circ$ ($\\rightarrow$ Target Point A: $0^\\circ$)\n"
        f" • Speed: $|\\mathbf{{v}}| = {v_A:.1f}$ m/s (Green)\n"
        f" • Accel: $|\\mathbf{{a}}| = {a_mag_A:.2f}$ m/s² ({a_mag_A/g:.2f} G, Red)\n"
        f"─────────────────────────────────────\n"
        f"▶ [Key Hints]\n"
        f" • Helical curvature radius: $\\rho = \\frac{{r}}{{\\cos^2\\gamma}}$\n"
        f" • Tangential accel: $a_t = g\\cos\\gamma$\n"
        f" • Normal accel: $a_n = \\frac{{v^2}}{{\\rho}}$\n"
        f" • Total accel magnitude: $|a| = \\sqrt{{a_t^2 + a_n^2}}$\n"
        f"─────────────────────────────────────\n"
        f"★ [Exact Answers at Point A]\n"
        f" • Curvature radius: $\\rho = 8.520$ m\n"
        f" • Tangential accel: $a_t = 7.515$ m/s²\n"
        f" • Normal accel: $a_n = 26.407$ m/s²\n"
        f" • Total accel magnitude: $|a| = 27.46$ m/s² ($2.80$ G)"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)
    gif_path = Path(__file__).parent / 'prob2_135_corkscrew.gif'
    writer = PillowWriter(fps=28)
    writer._kwargs = {'loop': None}
    ani.save(str(gif_path), writer=writer)
