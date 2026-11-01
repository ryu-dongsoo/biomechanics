# Problem 2/136: Radar Tracking of Jet Aircraft and Velocity Decomposition in Spherical Coordinates (R-θ-φ)
# Real-time 3D simulation with homework hints and exact analytical answers

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

# Parameters
h = 4.0
b = 3.0
u = 0.8 # km/s

t_start = -4.0
t_end = 4.0
frames = 100
t_arr = np.linspace(t_start, t_end, frames)
y_arr = u * t_arr

def get_spherical_state(y):
    r_xy = np.sqrt(b**2 + y**2)
    R = np.sqrt(b**2 + y**2 + h**2)
    theta = np.arctan2(y, b)
    phi = np.arctan2(h, r_xy)

    er = np.array([np.cos(phi)*np.cos(theta), np.cos(phi)*np.sin(theta), np.sin(phi)])
    eth = np.array([-np.sin(theta), np.cos(theta), 0.0])
    ephi = np.array([-np.sin(phi)*np.cos(theta), -np.sin(phi)*np.sin(theta), np.cos(phi)])

    vR = u * np.cos(phi) * np.sin(theta)
    vth = u * np.cos(theta)
    vphi = -u * np.sin(phi) * np.sin(theta)

    return R, theta, phi, r_xy, er, eth, ephi, vR, vth, vphi

fig = plt.figure(figsize=(12.8, 7.5))
ax = fig.add_axes([0.0, 0.02, 0.65, 0.96], projection='3d')
ax.set_facecolor('#ebf5fb')
ax.axis('off')

ax.set_xlim(-1, 5)
ax.set_ylim(-4.5, 4.5)
ax.set_zlim(-0.5, 5.5)
ax.set_box_aspect((1.2, 1.6, 1.1))
ax.view_init(elev=24, azim=-55)

ax.plot([0, 4.5], [0, 0], [0, 0], 'k--', lw=1.2, alpha=0.7)
ax.text(4.7, 0, 0, '$x$', fontsize=13, fontfamily='serif', fontstyle='italic', va='center')
ax.plot([0, 0], [-4.2, 4.2], [0, 0], 'k--', lw=1.2, alpha=0.7)
ax.text(0, 4.4, 0, '$y$', fontsize=13, fontfamily='serif', fontstyle='italic', va='center')
ax.plot([0, 0], [0, 0], [0, 5.0], 'k--', lw=1.2, alpha=0.7)
ax.text(0, 0, 5.2, '$z$', fontsize=13, fontfamily='serif', fontstyle='italic', ha='center')

ax.plot(np.full_like(y_arr, b), y_arr, np.full_like(y_arr, h), color='#e67e22', ls='--', lw=2.0, alpha=0.8, zorder=3)
ax.plot([0, b], [0, 0], [0, 0], color='#7f8c8d', ls='-', lw=1.2)
ax.plot([b, b], [-4.0, 4.0], [0, 0], color='#bdc3c7', ls=':', lw=1.0)

ax.plot([0], [0], [0], 'ko', markersize=6, zorder=10)
ax.text(-0.3, -0.3, 0.2, '$P$', fontsize=15, fontfamily='serif', fontweight='bold', color='#1a5276')

def draw_jet(ax, pos, heading=1):
    x, y, z = pos
    pts = np.array([
        [0, 0.7*heading, 0],
        [-0.15, -0.6*heading, 0],
        [0.15, -0.6*heading, 0],
        [0, 0.7*heading, 0.1],
        [-0.9, -0.2*heading, 0],
        [0.9, -0.2*heading, 0],
        [0, -0.6*heading, 0.35]
    ])
    pts[:, 0] += x
    pts[:, 1] += y
    pts[:, 2] += z

    lines = []
    l1, = ax.plot([pts[0,0], pts[1,0], pts[2,0], pts[0,0]],
                  [pts[0,1], pts[1,1], pts[2,1], pts[0,1]],
                  [pts[0,2], pts[1,2], pts[2,2], pts[0,2]], color='#c0392b', lw=2.0)
    l2, = ax.plot([pts[4,0], pts[5,0]], [pts[4,1], pts[5,1]], [pts[4,2], pts[5,2]], color='#c0392b', lw=2.2)
    l3, = ax.plot([pts[2,0], pts[6,0], pts[1,0]], [pts[2,1], pts[6,1], pts[1,1]], [pts[2,2], pts[6,2], pts[1,2]], color='#c0392b', lw=1.8)
    lines.extend([l1, l2, l3])
    return lines

dynamic_artists = []
dynamic_tri_surf = []

info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    global dynamic_artists, dynamic_tri_surf
    for art in dynamic_artists:
        if isinstance(art, list):
            for sub in art: sub.remove()
        else:
            art.remove()
    for surf in dynamic_tri_surf: surf.remove()
    dynamic_artists.clear()
    dynamic_tri_surf.clear()

    y_c = y_arr[i]
    x_c = b
    z_c = h

    R, theta, phi, r_xy, er, eth, ephi, vR, vth, vphi = get_spherical_state(y_c)

    tri_pts = np.array([[0, 0, 0], [x_c, y_c, 0], [x_c, y_c, z_c]])
    tri_poly = Poly3DCollection([tri_pts], facecolors='#f9e79f', edgecolors='#d4ac0d', alpha=0.35, lw=1.0)
    ax.add_collection3d(tri_poly)
    dynamic_tri_surf.append(tri_poly)

    line_R, = ax.plot([0, x_c], [0, y_c], [0, z_c], color='#e67e22', lw=2.2, ls='-', zorder=5)
    line_hproj, = ax.plot([0, x_c], [0, y_c], [0, 0], color='#7f8c8d', lw=1.2, ls=':', zorder=4)
    line_hvert, = ax.plot([x_c, x_c], [y_c, y_c], [0, z_c], color='#7f8c8d', lw=1.2, ls='--', zorder=4)
    txt_h_dim = ax.text(x_c + 0.15, y_c, z_c * 0.5, '$h$', fontsize=12, color='#2c3e50', fontstyle='italic')
    txt_b_dim = ax.text(b * 0.5, -0.4, 0, '$b$', fontsize=12, color='#2c3e50', fontstyle='italic')
    dynamic_artists.extend([line_R, line_hproj, line_hvert, txt_h_dim, txt_b_dim])

    if abs(theta) > 0.05:
        th_samples = np.linspace(0, theta, 20)
        arc_th_x = 2.0 * np.cos(th_samples)
        arc_th_y = 2.0 * np.sin(th_samples)
        arc_th_z = np.zeros_like(th_samples)
        arc_th, = ax.plot(arc_th_x, arc_th_y, arc_th_z, color='#2980b9', lw=1.5, zorder=4)
        txt_th = ax.text(2.3*np.cos(theta/2), 2.3*np.sin(theta/2), 0, r'$\theta$', color='#2980b9', fontsize=12, fontweight='bold')
        dynamic_artists.extend([arc_th, txt_th])

    phi_samples = np.linspace(0, phi, 20)
    arc_phi_x = 2.5 * np.cos(phi_samples) * np.cos(theta)
    arc_phi_y = 2.5 * np.cos(phi_samples) * np.sin(theta)
    arc_phi_z = 2.5 * np.sin(phi_samples)
    arc_phi, = ax.plot(arc_phi_x, arc_phi_y, arc_phi_z, color='#8e44ad', lw=1.5, zorder=4)
    txt_phi = ax.text(2.8*np.cos(phi/2)*np.cos(theta), 2.8*np.cos(phi/2)*np.sin(theta), 2.8*np.sin(phi/2),
                      r'$\phi$', color='#8e44ad', fontsize=12, fontweight='bold')
    dynamic_artists.extend([arc_phi, txt_phi])

    jet_parts = draw_jet(ax, (x_c, y_c, z_c), heading=1)
    txt_A = ax.text(x_c, y_c, z_c + 0.4, '$A$', fontsize=14, fontfamily='serif', fontweight='bold', color='#1a5276')
    dynamic_artists.append(jet_parts)
    dynamic_artists.append(txt_A)

    v_scale = 2.2
    q_v = ax.quiver(x_c, y_c, z_c, 0, u*v_scale, 0, color='#27ae60', arrow_length_ratio=0.25, lw=2.4, zorder=12)
    txt_v = ax.text(x_c, y_c + u*v_scale + 0.3, z_c, r'$\mathbf{v} = u\mathbf{j}$', color='#27ae60', fontsize=11, fontweight='bold')
    dynamic_artists.extend([q_v, txt_v])

    is_final = (i == frames - 1)
    status_hdr = "★ [Homework Task & Exact Velocity Formulas] ★" if is_final else "■ [Problem 2/136: Radar Jet Tracking]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【Geometry & Conditions】\n"
        f" • Jet altitude: $h = {h:.1f}$ km,  Offset: $b = {b:.1f}$ km\n"
        f" • Horizontal velocity: $\\mathbf{{v}} = u\\,\\hat{{\\mathbf{{j}}}}$ ($u = {u*1000:.0f}$ m/s)\n"
        f"─────────────────────────────────────\n"
        f"【Real-time Spherical Monitoring】\n"
        f" • Coord: $y = {y_c:+.2f}$ km $\\rightarrow R = {R:.2f}$ km\n"
        f" • Azimuth $\\theta = {np.degrees(theta):+.1f}^\\circ$,  Elevation $\\phi = {np.degrees(phi):.1f}^\\circ$\n"
        f" • Real-time components:\n"
        f"   - $v_R = {vR*1000:+.1f}$ m/s, $v_\\theta = {vth*1000:+.1f}$ m/s, $v_\\phi = {vphi*1000:+.1f}$ m/s\n"
        f"─────────────────────────────────────\n"
        f"▶ [Key Hints]\n"
        f" • Spherical coordinates:\n"
        f"   $x = R\\cos\\phi\\cos\\theta = b,\\ y = R\\cos\\phi\\sin\\theta,\\ z = R\\sin\\phi = h$\n"
        f" • Dot product with $\\mathbf{{v}} = u\\,\\hat{{\\mathbf{{j}}}}$:\n"
        f"   - $v_R = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_R$\n"
        f"   - $v_\\theta = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_\\theta$\n"
        f"   - $v_\\phi = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_\\phi$\n"
        f"─────────────────────────────────────\n"
        f"★ [Exact Velocity Formulas]\n"
        f" (1) $v_R = u\\cos\\phi\\sin\\theta$\n"
        f" (2) $v_\\theta = u\\cos\\theta$\n"
        f" (3) $v_\\phi = -u\\sin\\phi\\sin\\theta$\n"
        f" ★ Speed check: $\\sqrt{{v_R^2 + v_\\theta^2 + v_\\phi^2}} = u$ (matches)"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)
    gif_path = Path(__file__).parent / 'prob2_136_radar_jet.gif'
    writer = PillowWriter(fps=25)
    writer._kwargs = {'loop': None}
    ani.save(str(gif_path), writer=writer)
