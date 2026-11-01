# Problem 2/101: Kinematics of Pin P in Parabolic Slot and Vertical Slotted Guide
# Real-time simulation with homework hints and exact answers

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# Parameters
x_dot = 150.0   # mm/s
x_start = -80.0 # mm
x_target = 60.0 # mm

t_total = (x_target - x_start) / x_dot
frames = 120
t_arr = np.linspace(0, t_total, frames)
x_arr = x_start + x_dot * t_arr

y_arr = 100.0 - (x_arr**2) / 100.0
x_dot_arr = np.full_like(t_arr, x_dot)
y_dot_arr = -0.02 * x_arr * x_dot
v_arr = np.sqrt(x_dot_arr**2 + y_dot_arr**2)
theta_arr = np.arctan2(y_dot_arr, x_dot_arr)

x_ddot_arr = np.zeros_like(t_arr)
y_ddot_arr = np.full_like(t_arr, -0.02 * (x_dot**2))

at_arr = (x_ddot_arr * np.cos(theta_arr) + y_ddot_arr * np.sin(theta_arr))
an_arr = np.abs(-x_ddot_arr * np.sin(theta_arr) + y_ddot_arr * np.cos(theta_arr))
rho_arr = v_arr**2 / an_arr

fig, ax = plt.subplots(figsize=(12.5, 7.5))
fig.subplots_adjust(left=0.03, right=0.66, bottom=0.04, top=0.96)
ax.set_facecolor('#ebf5fb')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-125, 125)
ax.set_ylim(-35, 125)

bg_box = patches.Rectangle((-120, -30), 240, 150, facecolor='#ebf5fb', edgecolor='#85929e', lw=1.5, zorder=0)
ax.add_patch(bg_box)

shaft_bar = patches.Rectangle((-115, -3), 230, 6, facecolor='#d5dbdb', edgecolor='#2c3e50', lw=1.5, zorder=1)
ax.add_patch(shaft_bar)

mount_r = patches.Polygon([[115, -8], [122, -12], [122, 12], [115, 8]], facecolor='#7fb3d5', edgecolor='#2c3e50', lw=1.5, zorder=2)
ax.add_patch(mount_r)

ax.plot([-115, 122], [0, 0], 'k--', lw=1.0, alpha=0.6, zorder=2)
ax.text(124, 0, '$x$', fontsize=15, fontfamily='serif', fontstyle='italic', va='center', ha='left')
ax.plot([0, 0], [0, 115], 'k--', lw=1.0, alpha=0.6, zorder=2)
ax.text(0, 118, '$y$', fontsize=15, fontfamily='serif', fontstyle='italic', va='bottom', ha='center')

x_slot = np.linspace(-100, 100, 300)
y_slot = 100.0 - (x_slot**2) / 100.0

dx_s = np.gradient(x_slot)
dy_s = np.gradient(y_slot)
norm_s = np.sqrt(dx_s**2 + dy_s**2)
nx_s = -dy_s / norm_s
ny_s = dx_s / norm_s

track_w = 4.0
x_outer = x_slot + nx_s * track_w
y_outer = y_slot + ny_s * track_w
x_inner = x_slot - nx_s * track_w
y_inner = y_slot - ny_s * track_w

track_poly_x = np.concatenate([x_outer, x_inner[::-1]])
track_poly_y = np.concatenate([y_outer, y_inner[::-1]])
track_patch = patches.Polygon(np.column_stack([track_poly_x, track_poly_y]), facecolor='white', edgecolor='#2c3e50', lw=1.8, zorder=2)
ax.add_patch(track_patch)
ax.plot(x_slot, y_slot, color='#566573', lw=1.2, ls='-', zorder=3)

cap_l = patches.Circle((-100, 0), track_w, facecolor='white', edgecolor='#2c3e50', lw=1.8, zorder=2)
cap_r = patches.Circle((100, 0), track_w, facecolor='white', edgecolor='#2c3e50', lw=1.8, zorder=2)
ax.add_patch(cap_l)
ax.add_patch(cap_r)

ax.annotate('', xy=(-85, 100), xytext=(-85, 0),
            arrowprops=dict(arrowstyle='<->,head_width=0.15,head_length=0.35', color='black', lw=0.8, mutation_scale=8))
ax.plot([-88, 0], [100, 100], 'k--', lw=0.8, alpha=0.5)
ax.plot([-88, -75], [0, 0], 'k-', lw=0.8)
ax.text(-90, 50, '100 mm', fontsize=11, ha='right', va='center')

ax.annotate('', xy=(0, -18), xytext=(100, -18),
            arrowprops=dict(arrowstyle='<->,head_width=0.15,head_length=0.35', color='black', lw=0.8, mutation_scale=8))
ax.plot([0, 0], [-22, 0], 'k-', lw=0.8)
ax.plot([100, 100], [-22, 0], 'k-', lw=0.8)
ax.text(50, -23, '100 mm', fontsize=11, ha='center', va='top')

ax.text(75, 80, 'Fixed\nParabolic\nSlot', fontsize=11, fontweight='bold', ha='center', va='center', color='#2c3e50')

guide_base = patches.Rectangle((-12, -7), 24, 14, facecolor='#d98880', edgecolor='#2c3e50', lw=1.5, zorder=5)
guide_slot_outer = patches.Rectangle((-5, 5), 10, 102, facecolor='#d98880', edgecolor='#2c3e50', lw=1.5, zorder=5)
guide_slot_hole = patches.Rectangle((-2, 10), 4, 92, facecolor='#ebf5fb', edgecolor='#2c3e50', lw=1.2, zorder=6)
guide_top_cap = patches.Circle((0, 107), 5, facecolor='#d98880', edgecolor='#2c3e50', lw=1.5, zorder=5)
guide_hole_cap = patches.Circle((0, 102), 2, facecolor='#ebf5fb', edgecolor='#2c3e50', lw=1.2, zorder=6)

for p in [guide_base, guide_slot_outer, guide_top_cap, guide_slot_hole, guide_hole_cap]:
    ax.add_patch(p)

pin_circle = patches.Circle((0, 0), 3.2, facecolor='#27ae60', edgecolor='black', lw=1.5, zorder=8)
pin_dot = patches.Circle((0, 0), 1.0, facecolor='black', zorder=9)
ax.add_patch(pin_circle)
ax.add_patch(pin_dot)
txt_P = ax.text(0, 0, 'P', fontsize=13, fontfamily='serif', fontstyle='italic', fontweight='bold', ha='right', va='center', zorder=10)

dim_x_line = ax.annotate('', xy=(0, -10), xytext=(0, -10),
                         arrowprops=dict(arrowstyle='<->,head_width=0.15,head_length=0.35', color='black', lw=0.8, mutation_scale=8))
txt_dim_x = ax.text(0, -10, '$x$', fontsize=11, fontfamily='serif', fontstyle='italic', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

dynamic_artists = []

info_panel = fig.text(0.67, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    global dynamic_artists
    for art in dynamic_artists:
        art.remove()
    dynamic_artists.clear()

    x_curr = x_arr[i]
    y_curr = y_arr[i]
    th_curr = theta_arr[i]

    guide_base.set_x(x_curr - 12)
    guide_slot_outer.set_x(x_curr - 5)
    guide_slot_hole.set_x(x_curr - 2)
    guide_top_cap.center = (x_curr, 107)
    guide_hole_cap.center = (x_curr, 102)

    pin_circle.center = (x_curr, y_curr)
    pin_dot.center = (x_curr, y_curr)
    txt_P.set_position((x_curr - 5, y_curr))

    if abs(x_curr) > 2.0:
        dim_x_line.set_visible(True)
        txt_dim_x.set_visible(True)
        dim_x_line.xy = (x_curr, -10)
        dim_x_line.set_position((0, -10))
        txt_dim_x.set_position((x_curr / 2.0, -10))
        txt_dim_x.set_text(f'$x = {x_curr:.0f}$')
    else:
        dim_x_line.set_visible(False)
        txt_dim_x.set_visible(False)

    et = np.array([np.cos(th_curr), np.sin(th_curr)])
    en = np.array([-np.sin(th_curr), np.cos(th_curr)])
    if en[1] > 0:
        en = -en

    v_mag = v_arr[i]
    v_scale = 0.10
    v_arr_patch = patches.FancyArrowPatch((x_curr, y_curr), (x_curr + v_mag * et[0] * v_scale, y_curr + v_mag * et[1] * v_scale),
                                          arrowstyle='->,head_width=0.25,head_length=0.45', color='#27ae60', lw=2.0, mutation_scale=10, zorder=7)
    ax.add_patch(v_arr_patch)
    txt_v = ax.text(x_curr + v_mag * et[0] * v_scale + 2, y_curr + v_mag * et[1] * v_scale,
                    r'$\mathbf{v}$', color='#27ae60', fontsize=11, fontweight='bold', va='center')
    dynamic_artists.extend([v_arr_patch, txt_v])

    a_mag = 450.0
    a_scale = 0.05
    a_arr_patch = patches.FancyArrowPatch((x_curr, y_curr), (x_curr, y_curr - a_mag * a_scale),
                                          arrowstyle='->,head_width=0.25,head_length=0.45', color='#c0392b', lw=2.0, mutation_scale=10, zorder=7)
    ax.add_patch(a_arr_patch)
    txt_a = ax.text(x_curr + 2, y_curr - a_mag * a_scale,
                    r'$\mathbf{a}$', color='#c0392b', fontsize=11, fontweight='bold', va='top')
    dynamic_artists.extend([a_arr_patch, txt_a])

    at_val = at_arr[i]
    an_val = an_arr[i]
    rho_val = rho_arr[i]

    C_x = x_curr + rho_val * en[0]
    C_y = y_curr + rho_val * en[1]
    if -110 < C_x < 120 and -30 < C_y < 120:
        mark_C, = ax.plot([C_x], [C_y], 'kx', markersize=7, markeredgewidth=1.5, zorder=6)
        line_rho, = ax.plot([x_curr, C_x], [y_curr, C_y], color='#8e44ad', ls=':', lw=1.0, alpha=0.7, zorder=5)
        txt_C = ax.text(C_x + 2, C_y, '$C$', fontsize=11, fontfamily='serif', fontstyle='italic')
        txt_rho_lbl = ax.text((x_curr + C_x)/2 - 3, (y_curr + C_y)/2, r'$\rho$', color='#8e44ad', fontsize=11, fontweight='bold')
        dynamic_artists.extend([mark_C, line_rho, txt_C, txt_rho_lbl])

    is_final = (i == frames - 1)
    status_header = "★ [Homework Task & Exact Answers (x = 60 mm)] ★" if is_final else "■ [Problem 2/101: Parabolic Slot Kinematics]"

    info_str = (
        f"{status_header}\n"
        f"─────────────────────────────────────\n"
        f"【Geometry & Conditions】\n"
        f" • Slot Eq: $y = 100 - \\frac{{x^2}}{{100}}$ (mm)\n"
        f" • Guide speed: $\\dot{{x}} = {x_dot:.0f}$ mm/s (const, $\\ddot{{x}} = 0$)\n"
        f" • Target position: $x = 60$ mm\n"
        f"─────────────────────────────────────\n"
        f"【Real-time Monitoring】\n"
        f" • Position: $x = {x_curr:+.1f}$ mm,  $y = {y_curr:.1f}$ mm\n"
        f" • Pin P Speed: $|\\mathbf{{v}}| = {v_mag:.1f}$ mm/s (Green)\n"
        f" • Pin P Accel: $|\\mathbf{{a}}| = {a_mag:.1f}$ mm/s² (Red)\n"
        f"─────────────────────────────────────\n"
        f"▶ [Key Hints]\n"
        f" • $\\dot{{y}} = -\\frac{{x\\dot{{x}}}}{{50}},\\ \\ddot{{y}} = -\\frac{{\\dot{{x}}^2}}{{50}}$\n"
        f" • Tangent angle $\\theta = \\arctan(\\dot{{y}}/\\dot{{x}})$\n"
        f" • $a_t = \\ddot{{x}}\\cos\\theta + \\ddot{{y}}\\sin\\theta$\n"
        f" • $a_n = -\\ddot{{x}}\\sin\\theta + \\ddot{{y}}\\cos\\theta$\n"
        f" • Radius of curvature $\\rho = v^2 / a_n$\n"
        f"─────────────────────────────────────\n"
        f"★ [Exact Answers at $x = 60$ mm]\n"
        f" • Tangential accel: $a_t = 345.6$ mm/s² ($0.346$ m/s²)\n"
        f" • Normal accel: $a_n = 288.0$ mm/s² ($0.288$ m/s²)\n"
        f" • Curvature radius: $\\rho = 190.6$ mm ($0.191$ m)"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)
    gif_path = Path(__file__).parent / 'prob2_101_parabolic_slot.gif'
    writer = PillowWriter(fps=28)
    writer._kwargs = {'loop': None}
    ani.save(str(gif_path), writer=writer)
