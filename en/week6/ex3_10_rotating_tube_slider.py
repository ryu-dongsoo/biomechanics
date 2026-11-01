# -*- coding: utf-8 -*-
"""
Dynamics 9th Edition - Chapter 3 Kinetics of Particles
Example 3.10: Slider in Rotating Tube (r-theta Polar Coordinates)
- Pure white background (#ffffff) & 2-panel (14x6.8) standard layout (biomechanics-diagram-standard compliant)
- 1:1 textbook accurate mechanism (Meriam Dynamics 9th Ed.) & exact physical formulation:
  * Tube A rotates about vertical axis O with constant counter-clockwise (CCW) angular velocity dot_theta = omega = 4.0 rad/s
  * Slider plug B moves precisely along the centerline of tube A
  * Cable winding drum b rotates in opposite directions between (a) and (b):
    - Case (a): Drum unwinding -> dr/dt = +0.15 m/s (outward motion), trailing wall pushes plug (F_theta = +0.60 N)
    - Case (b): Drum winding up -> dr/dt = -0.15 m/s (inward motion), leading wall pushes plug (F_theta = -0.60 N)
  * Light sky-blue 3D conical stand, neck, upper rotating hub, and vertical axis O CCW rotation display
  * 3D cable winding drum mechanism b mounted directly below axis O (coils, radius b, (a)/(b) arrows)
  * Exact textbook 1:1 FBD (axis O, r-axis, square block B, +r/+θ dashed axes, tension T, transverse force F_θ)
- 100% verified against Wiley official solution manual:
  * Cable tension: T = m r omega^2 = 8r N
  * Case (a) Unwinding: F_theta = +2mb(omega_0)(omega) = +0.60 N (trailing wall pushes plug)
  * Case (b) Winding: F_theta = -2mb(omega_0)(omega) = -0.60 N (leading wall pushes plug)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Matplotlib configuration
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 1. Physical Parameters and Official Solutions
m = 0.50             # Plug B mass (kg)
omega = 4.0          # Tube A angular velocity (always CCW, +4.0 rad/s)
b = 0.05             # Drum radius (m = 50 mm)
omega_0 = 3.0        # Drum angular velocity (rad/s)
r_dot_mag = b * omega_0 # 0.150 m/s

r_min = 0.25         # Min radius (m)
r_max = 0.70         # Max radius (m)

# 2. Time series: Tube A rotates CCW (increasing theta) in both cases
n_half = 32
th_sweep = np.linspace(np.radians(-32.0), np.radians(14.0), n_half)

# Case (a): Tube A CCW rotation + B outward (0.25 -> 0.70 m, drum unwinding)
r_out = np.linspace(r_min, r_max, n_half)
th_out = th_sweep.copy()

# Case (b): Tube A CCW rotation + B inward (0.70 -> 0.25 m, drum winding up)
r_in = np.linspace(r_max, r_min, n_half)
th_in = th_sweep.copy()

r_series = np.concatenate([r_out, r_in])
th_series = np.concatenate([th_out, th_in])
rdot_series = np.concatenate([np.full(n_half, +r_dot_mag), np.full(n_half, -r_dot_mag)])
mode_series = ['a'] * n_half + ['b'] * n_half
n_frames = len(r_series)

# 3. 3D Projection Parameters
phi = np.radians(24.0) # Elevation angle
cos_phi = np.cos(phi)
sin_phi = np.sin(phi)

hub_bcy = 0.04
hub_rx, hub_ry = 0.125, 0.042
hub_h = 0.32
hub_tcy = hub_bcy + hub_h # 0.36
y0 = hub_bcy + 0.18 # Tube A centerline height

R_hub = hub_rx
tube_len = 0.86
R_t = 0.045
plug_len = 0.082
plug_r = R_t * 0.90

th_full = np.linspace(0, 2*np.pi, 100)

def project_pt(s, z_val, th):
    """3D polar coordinates (s, th, z_val) -> 2D screen coordinates (u, v)"""
    u = s * np.cos(th)
    v = s * np.sin(th) * sin_phi + z_val * cos_phi
    return u, v

def get_tube_geometry(th, r_curr):
    """Compute 3D vector geometry of tube A and slider B at rotation angle th"""
    ua = np.cos(th)
    va = np.sin(th) * sin_phi
    La = np.sqrt(ua**2 + va**2)
    t_hat = np.array([ua / La, va / La])
    n_hat = np.array([-va / La, ua / La])
    
    s_start = R_hub * 0.96
    s_end = tube_len
    
    p_start = np.array(project_pt(s_start, y0, th))
    p_end = np.array(project_pt(s_end, y0, th))
    
    poly_tube = np.array([
        p_start + R_t * n_hat,
        p_end + R_t * n_hat,
        p_end - R_t * n_hat,
        p_start - R_t * n_hat
    ])
    
    poly_hl = np.array([
        p_start + R_t * 0.3 * n_hat,
        p_end + R_t * 0.3 * n_hat,
        p_end + R_t * 0.55 * n_hat,
        p_start + R_t * 0.55 * n_hat
    ])
    
    def get_rim(s_val, rad):
        u_c, v_c = project_pt(s_val, y0, th)
        u_rim = u_c - rad * np.sin(th) * np.cos(th_full)
        v_rim = v_c + rad * np.cos(th) * sin_phi * np.cos(th_full) + rad * cos_phi * np.sin(th_full)
        return np.column_stack([u_rim, v_rim])
    
    rim_start = get_rim(s_start, R_t)
    rim_end = get_rim(s_end, R_t)
    rim_hole = get_rim(s_end, R_t * 0.75)
    
    sb_c = r_curr
    pb_center = np.array(project_pt(sb_c, y0, th))
    sb_in = sb_c - plug_len / 2
    sb_out = sb_c + plug_len / 2
    pb_in = np.array(project_pt(sb_in, y0, th))
    pb_out = np.array(project_pt(sb_out, y0, th))
    
    poly_plug = np.array([
        pb_in + plug_r * n_hat,
        pb_out + plug_r * n_hat,
        pb_out - plug_r * n_hat,
        pb_in - plug_r * n_hat
    ])
    plug_rim_out = get_rim(sb_out, plug_r)
    
    return {
        'p_start': p_start, 'p_end': p_end, 'poly_tube': poly_tube, 'poly_hl': poly_hl,
        'rim_start': rim_start, 'rim_end': rim_end, 'rim_hole': rim_hole,
        'pb_center': pb_center, 'pb_in': pb_in, 'pb_out': pb_out,
        'poly_plug': poly_plug, 'plug_rim_out': plug_rim_out,
        'n_hat': n_hat, 't_hat': t_hat
    }

# Canvas initialization (14 x 6.8, pure white background)
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.8), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.92, bottom=0.06, left=0.04, right=0.96, wspace=0.14)

def update(frame):
    r_curr = r_series[frame]
    th_curr = th_series[frame]
    rdot_curr = rdot_series[frame]
    mode_curr = mode_series[frame]
    
    T_curr = m * r_curr * (omega**2)            # 8 * r (N)
    F_theta_curr = 2.0 * m * rdot_curr * omega  # +0.60 N or -0.60 N
    
    # ---------------- 1. Main Physical View (ax_main) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.55, 1.15)
    ax_main.set_ylim(-0.95, 0.95)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Example 3.10: Slider in Rotating Tube (r-θ Polar Coordinates)', fontsize=13, fontweight='bold', pad=14)
    
    # (1) Base Plate
    base_corners = np.array([
        [-0.30, -0.38],
        [ 0.12, -0.49],
        [ 0.32, -0.37],
        [-0.10, -0.26]
    ])
    ax_main.add_patch(patches.Polygon(base_corners, closed=True, facecolor='#d7d2cb', edgecolor='#aba59d', lw=1.2, zorder=1))
    
    # (2) Conical Stand
    bot_cx, bot_cy, bot_rx, bot_ry = 0.0, -0.36, 0.165, 0.048
    top_cx, top_cy, top_rx, top_ry = 0.0, -0.11, 0.090, 0.026
    th_arc = np.linspace(np.pi, 2*np.pi, 60)
    
    cone_pts = np.array([
        [-bot_rx, bot_cy],
        [ bot_rx, bot_cy],
        [ top_rx, top_cy],
        [-top_rx, top_cy]
    ])
    ax_main.add_patch(patches.Polygon(cone_pts, closed=True, facecolor='#a3d3ea', edgecolor='#457b9d', lw=1.3, zorder=2))
    
    hl_cone = np.array([
        [-0.04*bot_rx/0.165, bot_cy],
        [ 0.04*bot_rx/0.165, bot_cy],
        [ 0.025*top_rx/0.09, top_cy],
        [-0.025*top_rx/0.09, top_cy]
    ])
    ax_main.add_patch(patches.Polygon(hl_cone, closed=True, facecolor='#cbe7f5', edgecolor='none', zorder=2))
    ax_main.plot(bot_rx * np.cos(th_arc), bot_cy + bot_ry * np.sin(th_arc), color='#35627f', lw=1.3, zorder=3)
    ax_main.add_patch(patches.Polygon(np.column_stack([top_rx*np.cos(th_full), top_cy + top_ry*np.sin(th_full)]),
                                      closed=True, facecolor='#bfe1f1', edgecolor='#457b9d', lw=1.2, zorder=3))
    
    # (3) Vertical Neck
    neck_rx = 0.052
    neck_h = 0.13
    ax_main.add_patch(patches.Rectangle((-neck_rx, top_cy), 2*neck_rx, neck_h, facecolor='#e1f0f7', edgecolor='#457b9d', lw=1.2, zorder=4))
    ax_main.add_patch(patches.Rectangle((-0.015, top_cy), 0.03, neck_h, facecolor='#f4fafd', edgecolor='none', zorder=4))
    
    # (4) Upper Rotating Hub
    ax_main.add_patch(patches.Rectangle((-hub_rx, hub_bcy), 2*hub_rx, hub_h, facecolor='#a3d3ea', edgecolor='#2c5d79', lw=1.4, zorder=5))
    ax_main.add_patch(patches.Rectangle((-0.03, hub_bcy), 0.06, hub_h, facecolor='#d6edfa', edgecolor='none', zorder=5))
    ax_main.plot(hub_rx * np.cos(th_arc), hub_bcy + hub_ry * np.sin(th_arc), color='#2c5d79', lw=1.3, zorder=6)
    ax_main.add_patch(patches.Polygon(np.column_stack([hub_rx*np.cos(th_full), hub_tcy + hub_ry*np.sin(th_full)]),
                                      closed=True, facecolor='#daf0fa', edgecolor='#2c5d79', lw=1.4, zorder=6))
    
    # (5) Vertical Axis of Rotation O and CCW rotation arrow
    ax_main.plot([0, 0], [hub_tcy, hub_tcy + 0.35], color='#263238', ls='--', lw=1.2, zorder=7)
    ax_main.text(-0.04, hub_tcy + 0.38, r'$O$', fontsize=16, fontweight='bold', fontstyle='italic', color='#263238', zorder=8)
    
    rx_a, ry_a = 0.13, 0.042
    y_a = hub_tcy + 0.20
    arc_th = np.linspace(-0.2*np.pi, 1.2*np.pi, 40)
    ax_main.plot(rx_a * np.cos(arc_th), y_a + ry_a * np.sin(arc_th), color='#2e7d32', lw=2.0, zorder=8)
    ax_main.annotate('', xy=(rx_a*np.cos(arc_th[-1]), y_a + ry_a*np.sin(arc_th[-1])),
                     xytext=(rx_a*np.cos(arc_th[-3]), y_a + ry_a*np.sin(arc_th[-3])),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.5', color='#2e7d32', lw=2.0), zorder=9)
    ax_main.text(rx_a + 0.04, y_a + 0.01, r'$\dot{\theta} = \omega$', fontsize=13, fontweight='bold', color='#2e7d32', zorder=9)
    
    # (6) Rotating Tube A and Slider B Geometry
    geom = get_tube_geometry(th_curr, r_curr)
    
    ax_main.add_patch(patches.Polygon(geom['poly_tube'], closed=True, facecolor='#bfe3f2', edgecolor='#2c5d79', lw=1.4, alpha=0.92, zorder=7))
    ax_main.add_patch(patches.Polygon(geom['poly_hl'], closed=True, facecolor='#ffffff', edgecolor='none', alpha=0.5, zorder=8))
    ax_main.add_patch(patches.Polygon(geom['rim_start'], closed=True, facecolor='#7ec0df', edgecolor='#2c5d79', lw=1.2, zorder=8))
    ax_main.add_patch(patches.Polygon(geom['rim_end'], closed=True, facecolor='#7ec0df', edgecolor='#2c5d79', lw=1.4, zorder=8))
    ax_main.add_patch(patches.Polygon(geom['rim_hole'], closed=True, facecolor='#263238', edgecolor='#102027', lw=1.0, zorder=9))
    
    p_axis_end = geom['p_start'] + (tube_len + 0.16) * geom['t_hat']
    ax_main.plot([geom['p_start'][0], p_axis_end[0]], [geom['p_start'][1], p_axis_end[1]], color='#263238', ls='--', lw=1.1, zorder=9)
    ax_main.text(p_axis_end[0] + 0.02, p_axis_end[1] - 0.01, r'$r$', fontsize=14, fontstyle='italic', color='#263238')
    
    # (7) Slider Plug B (Centered along axis of tube A)
    ax_main.plot([geom['p_start'][0], geom['pb_in'][0]], [geom['p_start'][1], geom['pb_in'][1]], color='#212121', lw=1.8, zorder=9)
    ax_main.add_patch(patches.Polygon(geom['poly_plug'], closed=True, facecolor='#cf7d45', edgecolor='#8c4314', lw=1.3, zorder=10))
    ax_main.add_patch(patches.Polygon(geom['plug_rim_out'], closed=True, facecolor='#e99b66', edgecolor='#8c4314', lw=1.2, zorder=11))
    
    # Labels B and A
    p_lbl_B = geom['pb_center'] - R_t * geom['n_hat'] - 0.08 * geom['n_hat']
    ax_main.text(p_lbl_B[0] - 0.02, p_lbl_B[1], r'$B$', fontsize=15, fontweight='bold', color='#1565c0', zorder=12)
    p_lbl_A = geom['p_end'] - R_t * geom['n_hat'] - 0.08 * geom['n_hat'] - 0.10 * geom['t_hat']
    ax_main.text(p_lbl_A[0], p_lbl_A[1], r'$A$', fontsize=15, fontweight='bold', color='#1565c0', zorder=12)
    
    # Dimension r
    dim_dist = 0.18
    p0_dim = np.array(project_pt(0, y0, th_curr)) + dim_dist * geom['n_hat']
    pb_dim = geom['pb_center'] + dim_dist * geom['n_hat']
    ax_main.plot([0, p0_dim[0] + 0.03*geom['n_hat'][0]], [y0, p0_dim[1] + 0.03*geom['n_hat'][1]], color='#78909c', lw=0.9, ls=':')
    ax_main.plot([geom['pb_center'][0], pb_dim[0] + 0.03*geom['n_hat'][0]], [geom['pb_center'][1], pb_dim[1] + 0.03*geom['n_hat'][1]], color='#78909c', lw=0.9, ls=':')
    ax_main.annotate('', xy=(pb_dim[0], pb_dim[1]), xytext=(p0_dim[0], p0_dim[1]),
                     arrowprops=dict(arrowstyle='<->', color='#263238', lw=1.1), zorder=12)
    mid_dim = (p0_dim + pb_dim) / 2
    ax_main.text(mid_dim[0] - 0.04, mid_dim[1] + 0.03, f'r = {r_curr:.2f} m', fontsize=11, fontweight='bold', color='#263238')
    
    # Real-time velocity vector dr/dt
    v_sign = 1.0 if rdot_curr > 0 else -1.0
    v_vec = 0.13 * v_sign
    v_start = geom['pb_out'] if v_sign > 0 else geom['pb_in']
    v_end = v_start + v_vec * geom['t_hat']
    ax_main.annotate('', xy=(v_end[0], v_end[1]), xytext=(v_start[0], v_start[1]),
                     arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.48', color='#2e7d32', lw=2.2), zorder=13)
    ax_main.text(v_end[0] + 0.02, v_end[1] + 0.03, r'$\dot{r}$', fontsize=13, fontweight='bold', color='#2e7d32', zorder=13)
    
    # (8) Winding Drum Mechanism b
    ax_main.plot([0, 0], [-0.36, -0.84], color='#263238', ls='--', lw=1.1, zorder=2)
    
    drum_cx, drum_cy = 0.0, -0.68
    drum_th = np.radians(35.0)
    cos_d, sin_d = np.cos(drum_th), np.sin(drum_th)
    shaft_len = 0.44
    drum_L, drum_R = 0.18, 0.075
    drum_rx, drum_ry = drum_R * 0.45, drum_R
    
    p_sh1 = np.array([drum_cx - (shaft_len/2)*cos_d, drum_cy - (shaft_len/2)*sin_d])
    p_sh2 = np.array([drum_cx + (shaft_len/2)*cos_d, drum_cy + (shaft_len/2)*sin_d])
    ax_main.plot([p_sh1[0], p_sh2[0]], [p_sh1[1], p_sh2[1]], color='#546e7a', lw=4.5, solid_capstyle='round', zorder=3)
    ax_main.plot([p_sh1[0], p_sh2[0]], [p_sh1[1], p_sh2[1]], color='#90a4ae', lw=2.0, solid_capstyle='round', zorder=3)
    
    p_d1 = np.array([drum_cx - (drum_L/2)*cos_d, drum_cy - (drum_L/2)*sin_d])
    p_d2 = np.array([drum_cx + (drum_L/2)*cos_d, drum_cy + (drum_L/2)*sin_d])
    drum_corners = np.array([
        [p_d1[0] - drum_R*sin_d, p_d1[1] + drum_R*cos_d],
        [p_d2[0] - drum_R*sin_d, p_d2[1] + drum_R*cos_d],
        [p_d2[0] + drum_R*sin_d, p_d2[1] - drum_R*cos_d],
        [p_d1[0] + drum_R*sin_d, p_d1[1] - drum_R*cos_d]
    ])
    ax_main.add_patch(patches.Polygon(drum_corners, closed=True, facecolor='#529778', edgecolor='#1e4634', lw=1.3, zorder=4))
    
    n_coils = 4
    for i in range(1, n_coils):
        s_frac = i / n_coils
        pc = p_d1 + s_frac * (p_d2 - p_d1)
        ax_main.plot([pc[0] - drum_R*sin_d, pc[0] + drum_R*sin_d],
                     [pc[1] + drum_R*cos_d, pc[1] - drum_R*cos_d],
                     color='#1b4332', lw=1.3, zorder=5)
    
    rot_mat = np.array([[cos_d, -sin_d], [sin_d, cos_d]])
    cap_coords = np.column_stack([drum_rx * np.cos(th_full), drum_ry * np.sin(th_full)]) @ rot_mat.T
    ax_main.add_patch(patches.Polygon(p_d1 + cap_coords, closed=True, facecolor='#74af94', edgecolor='#1e4634', lw=1.3, zorder=6))
    ax_main.plot(p_d2[0] + cap_coords[:, 0], p_d2[1] + cap_coords[:, 1], color='#1e4634', lw=1.3, zorder=6)
    
    b_pt = p_d1 + np.array([-drum_R*0.7*sin_d, drum_R*0.7*cos_d])
    ax_main.plot([p_d1[0], b_pt[0]], [p_d1[1], b_pt[1]], color='#1b4332', lw=1.1, zorder=7)
    ax_main.text(b_pt[0] - 0.08, b_pt[1] + 0.01, r'$b$', fontsize=13, fontstyle='italic', fontweight='bold', color='#1b4332', zorder=8)
    ax_main.annotate('', xy=(b_pt[0], b_pt[1]), xytext=(b_pt[0] - 0.05, b_pt[1] + 0.015),
                     arrowprops=dict(arrowstyle='->', color='#1b4332', lw=1.1), zorder=8)
    
    # Drum arrows: (a) unwinding vs (b) winding in opposite directions
    col_a = '#2e7d32' if mode_curr == 'a' else '#9e9e9e'
    col_b = '#2e7d32' if mode_curr == 'b' else '#9e9e9e'
    lw_a = 2.2 if mode_curr == 'a' else 1.3
    lw_b = 2.2 if mode_curr == 'b' else 1.3
    
    arc_sh1 = np.linspace(0.1*np.pi, 1.4*np.pi, 30)
    arc1_coords = np.column_stack([0.045 * np.cos(arc_sh1), 0.045 * np.sin(arc_sh1)]) @ rot_mat.T + p_sh1
    ax_main.plot(arc1_coords[:, 0], arc1_coords[:, 1], color=col_a, lw=lw_a, zorder=8)
    ax_main.annotate('', xy=(arc1_coords[-1, 0], arc1_coords[-1, 1]), xytext=(arc1_coords[-3, 0], arc1_coords[-3, 1]),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color=col_a, lw=lw_a), zorder=9)
    ax_main.text(p_sh1[0] - 0.14, p_sh1[1] - 0.12, 'Case (a)', fontsize=11, fontweight='bold',
                 color='#1b5e20' if mode_curr == 'a' else '#757575', zorder=9)
    
    arc_sh2 = np.linspace(-0.9*np.pi, 0.4*np.pi, 30)
    arc2_coords = np.column_stack([0.045 * np.cos(arc_sh2), 0.045 * np.sin(arc_sh2)]) @ rot_mat.T + p_sh2
    ax_main.plot(arc2_coords[:, 0], arc2_coords[:, 1], color=col_b, lw=lw_b, zorder=8)
    ax_main.annotate('', xy=(arc2_coords[-1, 0], arc2_coords[-1, 1]), xytext=(arc2_coords[-3, 0], arc2_coords[-3, 1]),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color=col_b, lw=lw_b), zorder=9)
    ax_main.text(p_sh2[0] + 0.05, p_sh2[1] + 0.01, r'$\omega_0$', fontsize=13, fontweight='bold', color=col_b, zorder=9)
    ax_main.text(p_sh2[0] + 0.02, p_sh2[1] - 0.08, 'Case (b)', fontsize=11, fontweight='bold',
                 color='#1b5e20' if mode_curr == 'b' else '#757575', zorder=9)
    
    # Top Status Banner: Tube A always rotates CCW
    if mode_curr == 'a':
        banner_txt = f'Case (a): Unwinding(dr/dt > 0, Outward) | Tube A CCW Rotation | Drum Unwinding'
        banner_bg, banner_edge, banner_col = '#e3f2fd', '#90caf9', '#0d47a1'
    else:
        banner_txt = f'Case (b): Winding(dr/dt < 0, Inward) | Tube A CCW Rotation | Drum Reversed Winding'
        banner_bg, banner_edge, banner_col = '#fbe9e7', '#ffab91', '#b71c1c'
    ax_main.text(-0.52, 0.84, banner_txt, fontsize=10.0, fontweight='bold', color=banner_col,
                 bbox=dict(boxstyle='round,pad=0.38', facecolor=banner_bg, edgecolor=banner_edge, lw=1.2))
    
    # ---------------- 2. Analysis & Monitoring View (ax_calc) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # (1) FBD Top View
    ax_calc.text(0.2, 9.75, '[Free Body Diagram (FBD) - Top View]', fontsize=11, fontweight='bold', color='#1565c0')
    
    fbd_ox, fbd_oy = 2.0, 8.35
    fbd_bx, fbd_by = 5.3, 8.35
    
    # Axis O with constant CCW rotation arrow (dot_theta = omega)
    ax_calc.plot([fbd_ox, fbd_ox], [fbd_oy - 0.28, fbd_oy + 0.28], color='#263238', lw=1.2)
    ax_calc.plot([fbd_ox - 0.28, fbd_ox + 0.28], [fbd_oy, fbd_oy], color='#263238', lw=1.2)
    ax_calc.text(fbd_ox - 0.20, fbd_oy - 0.42, r'$O$', fontsize=14, fontweight='bold', color='#263238')
    
    fbd_arc = np.linspace(-0.3*np.pi, 0.9*np.pi, 40)
    ax_calc.plot(fbd_ox + 0.42*np.cos(fbd_arc), fbd_oy + 0.42*np.sin(fbd_arc), color='#2e7d32', lw=1.8)
    ax_calc.annotate('', xy=(fbd_ox + 0.42*np.cos(fbd_arc[-1]), fbd_oy + 0.42*np.sin(fbd_arc[-1])),
                     xytext=(fbd_ox + 0.42*np.cos(fbd_arc[-3]), fbd_oy + 0.42*np.sin(fbd_arc[-3])),
                     arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.45', color='#2e7d32', lw=1.8))
    ax_calc.text(fbd_ox - 0.45, fbd_oy + 0.58, r'$\dot{\theta} = \omega$', fontsize=12, fontweight='bold', color='#2e7d32')
    
    ax_calc.plot([fbd_ox, fbd_bx], [fbd_oy, fbd_oy], color='#455a64', lw=1.2)
    ax_calc.text((fbd_ox + fbd_bx)/2 - 0.08, fbd_oy - 0.32, r'$r$', fontsize=13, fontstyle='italic', fontweight='bold', color='#455a64')
    
    sq_w = 0.65
    ax_calc.add_patch(patches.Rectangle((fbd_bx - sq_w/2, fbd_by - sq_w/2), sq_w, sq_w,
                                        facecolor='#ffffff', edgecolor='#263238', lw=1.5, zorder=5))
    ax_calc.text(fbd_bx + sq_w/2 + 0.12, fbd_by + sq_w/2 + 0.08, r'$B$', fontsize=14, fontweight='bold', color='#1565c0')
    
    ax_calc.plot([fbd_bx + sq_w/2, fbd_bx + 2.1], [fbd_by, fbd_by], color='#78909c', ls='--', lw=1.1)
    ax_calc.text(fbd_bx + 2.2, fbd_by - 0.10, r'$+r$', fontsize=12, fontweight='bold', color='#37474f')
    
    ax_calc.plot([fbd_bx, fbd_bx], [fbd_by + sq_w/2, fbd_by + 1.05], color='#78909c', ls='--', lw=1.1)
    ax_calc.text(fbd_bx - 0.18, fbd_by + 1.15, r'$+\theta$', fontsize=12, fontweight='bold', color='#37474f')
    
    # Tension T
    t_arrow_len = 0.4 + (T_curr / 6.0) * 1.0
    ax_calc.annotate('', xy=(fbd_bx - sq_w/2 - t_arrow_len, fbd_by), xytext=(fbd_bx - sq_w/2, fbd_by),
                     arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#d32f2f', lw=2.4), zorder=6)
    ax_calc.text(fbd_bx - sq_w/2 - t_arrow_len - 0.35, fbd_by + 0.16, r'$T$', fontsize=14, fontweight='bold', color='#d32f2f')
    
    # Transverse Force F_theta
    if mode_curr == 'a':
        ax_calc.annotate('', xy=(fbd_bx, fbd_by - sq_w/2), xytext=(fbd_bx, fbd_by - sq_w/2 - 1.10),
                         arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#d32f2f', lw=2.4), zorder=6)
        ax_calc.text(fbd_bx + 0.18, fbd_by - sq_w/2 - 0.90, r'$F_\theta\ (+)$', fontsize=12, fontweight='bold', color='#d32f2f')
    else:
        ax_calc.annotate('', xy=(fbd_bx, fbd_by + sq_w/2), xytext=(fbd_bx, fbd_by + sq_w/2 + 0.95),
                         arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#d32f2f', lw=2.4), zorder=6)
        ax_calc.text(fbd_bx + 0.18, fbd_by + sq_w/2 + 0.65, r'$F_\theta\ (-)$', fontsize=12, fontweight='bold', color='#d32f2f')
    
    # (2) Theoretical Derivation Card
    sol_text = (
        "[Theoretical Derivation & Analysis (r-θ Polar Coordinates)]\n"
        r"• Parameters: $m = 0.50\ \mathrm{kg},\ \dot{\theta} = \omega = 4.0\ \mathrm{rad/s}\ (\text{always CCW}),\ \ddot{\theta} = 0$" + "\n"
        r"  Drum $b = 50\ \mathrm{mm} = 0.05\ \mathrm{m},\ \omega_0 = 3.0\ \mathrm{rad/s}\ (\dot{r} = \pm b\omega_0 = \pm 0.15\ \mathrm{m/s})$" + "\n"
        r"• Equations of Motion ($\sum F_r = m a_r,\ \sum F_\theta = m a_\theta$):" + "\n"
        r"  - Radial: $-T = m(\ddot{r} - r\dot{\theta}^2) = -m r \omega^2\ (\because \ddot{r} = 0)$" + "\n"
        r"    $\Rightarrow \mathbf{T = m r \omega^2 = 0.50(4.0)^2 r = 8r\ \mathrm{N}}$" + "\n"
        r"  - Transverse (Coriolis): $F_\theta = m(r\ddot{\theta} + 2\dot{r}\dot{\theta}) = 2m\dot{r}\omega\ (\because \ddot{\theta} = 0)$" + "\n"
        r"    * Case (a) (Drum unwinding, $\dot{r} = +b\omega_0 = +0.15\ \mathrm{m/s}$):" + "\n"
        r"      $\mathbf{F_\theta = 2(0.50)(+0.15)(4.0) = +0.60\ \mathrm{N}}$ (Trailing wall pushes plug)" + "\n"
        r"    * Case (b) (Drum winding up, $\dot{r} = -b\omega_0 = -0.15\ \mathrm{m/s}$):" + "\n"
        r"      $\mathbf{F_\theta = 2(0.50)(-0.15)(4.0) = -0.60\ \mathrm{N}}$ (Leading wall pushes plug)"
    )
    ax_calc.text(0.2, 4.65, sol_text, fontsize=8.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.2))
    
    # (3) Real-Time Dynamic Monitoring Card
    live_text = (
        "[Real-Time Dynamic Monitoring]\n"
        f"• Operating Mode: {'Case (a) Cable Unwinding (Drum Unwinding)' if mode_curr == 'a' else 'Case (b) Cable Winding (Drum Reversed)'}\n"
        f"• Tube Rotation: θ = {np.degrees(th_curr):+.1f}° (CCW Rotation about Axis O, ω = 4.0 rad/s)\n"
        f"• Radial Position: r = {r_curr:.3f} m (Moving along Centerline of Tube A)\n"
        f"• Cable Tension: T = 8r = {T_curr:.2f} N (Centripetal demand mrω²)\n"
        f"• Transverse Force: Fθ = {F_theta_curr:+.2f} N ({'Trailing wall contact' if mode_curr == 'a' else 'Leading wall contact'})\n"
        f"• Coriolis Acceleration: 2·r_dot·ω = {2.0 * rdot_curr * omega:+.2f} m/s²"
    )
    ax_calc.text(0.2, 1.05, live_text, fontsize=9.1, va='center',
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.2))

# GIF generation and save
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
out_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(out_dir, 'ex3_10_rotating_tube_slider.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()

print(f"[Done] Example 3.10 English animation generated successfully: {gif_path}")
