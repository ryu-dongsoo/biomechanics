"""
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.6: Steady Mass Flow
Sample Problem 4/6 - Fluid Stream Deflection by Smooth Vane (Fixed vs. Moving Vane)
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Theoretical validation:
  (a) Fixed vane (u = 0): F = rho*A*v^2*(1 - cos(theta)), R = rho*A*v^2*sin(theta)
  (b) Moving vane (u < v): m' = rho*A*(v - u), F = rho*A*(v - u)^2*(1 - cos(theta)), R = rho*A*(v - u)^2*sin(theta)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Representative physical parameters (rho=1000 kg/m^3, A=0.002 m^2, v=20 m/s, theta=60 deg)
rho = 1000.0
A = 0.002
v = 20.0
theta_deg = 60.0
theta = np.radians(theta_deg)

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_vane_curve(x0, y0, R_arc=2.4, th_max=theta):
    ang = np.linspace(-np.pi / 2, -np.pi / 2 + th_max, 40)
    cx, cy = x0, y0 + R_arc
    xs = cx + R_arc * np.cos(ang)
    ys = cy + R_arc * np.sin(ang)
    nx = -np.cos(ang)
    ny = -np.sin(ang)
    return xs, ys, nx, ny


def draw_vane_and_stream(ax, x_vane, y_vane, u_val, phase_t, label_title, is_moving=False):
    R_arc = 2.2
    xs, ys, nx, ny = get_vane_curve(x_vane, y_vane, R_arc, theta)

    jet_h = 0.34
    vane_thick = 0.22

    # 1) Nozzle
    noz_x0, noz_x1 = 0.6, 1.9
    noz_poly = np.array([
        [noz_x0, y_vane - 0.30],
        [noz_x1, y_vane - jet_h / 2],
        [noz_x1, y_vane + jet_h / 2],
        [noz_x0, y_vane + 0.30]
    ])
    ax.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.8, zorder=4))
    ax.add_patch(patches.Rectangle((noz_x1 - 0.1, y_vane - jet_h / 2 - 0.04), 0.1, jet_h + 0.08,
                                   facecolor='#e6c65a', edgecolor='#5c4811', lw=1.5, zorder=5))

    # 2) Horizontal incoming fluid stream
    ax.fill_between([noz_x1, x_vane], y_vane - jet_h / 2, y_vane + jet_h / 2,
                    color='#bbdefb', alpha=0.85, zorder=2)
    ax.plot([noz_x1, x_vane], [y_vane + jet_h / 2, y_vane + jet_h / 2], color='#1976d2', lw=1.2, zorder=3)
    ax.plot([noz_x1, x_vane], [y_vane - jet_h / 2, y_vane - jet_h / 2], color='#1976d2', lw=1.2, zorder=3)

    # 3) Curved stream along vane + exit jet
    s_ext = np.linspace(0, 0.9, 15)
    tx_end, ty_end = np.cos(theta), np.sin(theta)
    nx_end, ny_end = -np.sin(theta), np.cos(theta)

    xs_ext = xs[-1] + s_ext * tx_end
    ys_ext = ys[-1] + s_ext * ty_end
    nx_ext = np.full_like(s_ext, nx_end)
    ny_ext = np.full_like(s_ext, ny_end)

    x_stream = np.concatenate([xs, xs_ext[1:]])
    y_stream = np.concatenate([ys, ys_ext[1:]])
    nx_stream = np.concatenate([nx, nx_ext[1:]])
    ny_stream = np.concatenate([ny, ny_ext[1:]])

    upper_x = x_stream + (jet_h / 2) * nx_stream
    upper_y = y_stream + (jet_h / 2) * ny_stream
    lower_x = x_stream - (jet_h / 2) * nx_stream
    lower_y = y_stream - (jet_h / 2) * ny_stream

    stream_poly = np.column_stack([
        np.concatenate([lower_x, upper_x[::-1]]),
        np.concatenate([lower_y, upper_y[::-1]])
    ])
    ax.add_patch(patches.Polygon(stream_poly, facecolor='#bbdefb', edgecolor='#1976d2', lw=1.2, alpha=0.85, zorder=2))

    # 4) Fluid particles animation
    n_pts = 7
    for k in range(n_pts):
        frac = ((k / n_pts) + phase_t) % 1.0
        idx = int(frac * (len(x_stream) - 1))
        ax.plot(x_stream[idx], y_stream[idx], 'o', color='#0d47a1', markersize=4.5, zorder=4)
    for k in range(4):
        frac = ((k / 4.0) + phase_t * 1.4) % 1.0
        px = noz_x1 + frac * (x_vane - noz_x1)
        ax.plot(px, y_vane, 'o', color='#0d47a1', markersize=4.5, zorder=4)

    # 5) Vane body
    vane_top_x = xs - (jet_h / 2) * nx
    vane_top_y = ys - (jet_h / 2) * ny
    vane_bot_x = xs - (jet_h / 2 + vane_thick) * nx
    vane_bot_y = ys - (jet_h / 2 + vane_thick) * ny
    vane_poly = np.column_stack([
        np.concatenate([vane_bot_x, vane_top_x[::-1]]),
        np.concatenate([vane_bot_y, vane_top_y[::-1]])
    ])
    ax.add_patch(patches.Polygon(vane_poly, facecolor='#90a4ae', edgecolor='#263238', lw=2.0, zorder=5))

    # 6) Inlet velocity vector v
    ax.annotate('', xy=(noz_x1 + 1.15, y_vane), xytext=(noz_x1 + 0.15, y_vane),
                arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=6)
    ax.text(noz_x1 + 0.65, y_vane + 0.28, r'$v$', fontsize=11.5, fontweight='bold', color='#2e7d32', ha='center')

    # 7) External support forces F and R
    mid_i = len(xs) // 2
    vx_m, vy_m = vane_bot_x[mid_i], vane_bot_y[mid_i]
    ax.annotate('', xy=(vx_m + 0.05, vy_m - 0.05), xytext=(vx_m + 1.25, vy_m - 0.05),
                arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax.text(vx_m + 1.32, vy_m - 0.05, r'$F$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    ax.annotate('', xy=(vx_m - 0.15, vy_m - 0.02), xytext=(vx_m - 0.15, vy_m - 0.95),
                arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax.text(vx_m - 0.02, vy_m - 0.78, r'$R$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    # 8) Exit velocity and angle
    end_x, end_y = x_stream[-1], y_stream[-1]
    ax.plot([end_x - 0.1, end_x + 1.1], [end_y, end_y], color='#666666', ls='--', lw=1.1)
    arc = patches.Arc((end_x, end_y), 0.9, 0.9, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.3)
    ax.add_patch(arc)
    ax.text(end_x + 0.62, end_y + 0.24, r'$\theta=60^\circ$', fontsize=9.8, fontweight='bold', color='#333333')

    if not is_moving:
        v_out_end = (end_x + 0.95 * np.cos(theta), end_y + 0.95 * np.sin(theta))
        ax.annotate('', xy=v_out_end, xytext=(end_x, end_y),
                    arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=6)
        ax.text(v_out_end[0] + 0.1, v_out_end[1] + 0.05, r"$v' = v$", fontsize=11, fontweight='bold', color='#2e7d32')
    else:
        ax.annotate('', xy=(vx_m + 1.45, vy_m - 0.52), xytext=(vx_m + 0.55, vy_m - 0.52),
                    arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=13), zorder=6)
        ax.text(vx_m + 1.52, vy_m - 0.52, r'$u$', fontsize=11, fontweight='bold', color='#1565c0', va='center')

        u_vec = np.array([0.45, 0.0])
        vrel_vec = np.array([0.85 * np.cos(theta), 0.85 * np.sin(theta)])
        vp_vec = u_vec + vrel_vec
        p0 = np.array([end_x, end_y])
        p_u = p0 + u_vec
        p_vp = p0 + vp_vec

        ax.annotate('', xy=p_u, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p_vp, xytext=p_u,
                    arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p_vp, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=7)
        ax.text(p_vp[0] + 0.1, p_vp[1], r"$v'$", fontsize=11, fontweight='bold', color='#2e7d32', va='center')
        ax.text(p0[0] - 0.15, p0[1] + 0.52, r'$v - u$', fontsize=9.8, fontweight='bold', color='#00897b', ha='right')

    ax.text(0.6, y_vane + 1.55, label_title, fontsize=11.0, fontweight='bold', color='#1d4564',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f4f8', edgecolor='#b0bec5'))


def update(frame):
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 9.2)
    ax_main.set_ylim(0.0, 9.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    phase_t = (frame * 0.08) % 1.0

    # Top: (a) Fixed Vane (u = 0)
    draw_vane_and_stream(ax_main, x_vane=3.2, y_vane=6.1, u_val=0.0, phase_t=phase_t,
                         label_title='(a) Fixed Vane ($u = 0$)', is_moving=False)

    ax_main.plot([0.3, 8.9], [4.55, 4.55], color='#cfd8dc', ls='--', lw=1.5)

    # Bottom: (b) Moving Vane (u = 0 -> 8 m/s)
    u_curr = 8.0 * (0.5 - 0.5 * np.cos(2 * np.pi * frame / n_frames))
    x_shift = 2.8 + 0.9 * (u_curr / 8.0)
    draw_vane_and_stream(ax_main, x_vane=x_shift, y_vane=1.55, u_val=u_curr, phase_t=phase_t * 0.75,
                         label_title=f'(b) Moving Vane ($u = {u_curr:.1f}\\ \\mathrm{{m/s}}$)', is_moving=True)

    ax_main.set_title('Sample Problem 4/6: Fluid Stream Deflection by Smooth Vane', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- Right Panel: Velocity Diagram & Theoretical Analysis ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.45, 'Exit Velocity Addition Diagram ($\\mathbf{v}\' = \\mathbf{u} + \\mathbf{v}_{\\mathrm{rel}}$)',
                 fontsize=11.2, fontweight='bold', ha='center', color='#1d4564')

    tri_x0, tri_y0 = 2.2, 6.65
    u_len = 2.2
    vr_len = 2.55
    p_origin = np.array([tri_x0, tri_y0])
    p_u_end = p_origin + np.array([u_len, 0.0])
    p_vp_end = p_u_end + np.array([vr_len * np.cos(theta), vr_len * np.sin(theta)])

    p_vr_top = p_origin + np.array([vr_len * np.cos(theta), vr_len * np.sin(theta)])
    ax_calc.plot([p_origin[0], p_vr_top[0]], [p_origin[1], p_vr_top[1]], color='#90a4ae', ls='--', lw=1.2)
    ax_calc.plot([p_vr_top[0], p_vp_end[0]], [p_vr_top[1], p_vp_end[1]], color='#90a4ae', ls='--', lw=1.2)

    ax_calc.annotate('', xy=p_u_end, xytext=p_origin,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=14))
    ax_calc.text(0.5 * (p_origin[0] + p_u_end[0]), p_origin[1] - 0.35, r'Vane speed $u$',
                 fontsize=10.2, fontweight='bold', color='#1565c0', ha='center')

    ax_calc.annotate('', xy=p_vp_end, xytext=p_u_end,
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=14))
    ax_calc.text(p_u_end[0] + 1.15, p_u_end[1] + 0.78, r'Relative $v - u$',
                 fontsize=10.2, fontweight='bold', color='#00897b', ha='left')

    ax_calc.annotate('', xy=p_vp_end, xytext=p_origin,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(p_origin[0] + 1.35, p_origin[1] + 1.25, r"Absolute $v'$",
                 fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')

    arc_v = patches.Arc(p_u_end, 1.3, 1.3, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.3)
    ax_calc.add_patch(arc_v)
    ax_calc.text(p_u_end[0] + 0.85, p_u_end[1] + 0.25, r'$\theta$', fontsize=11, fontweight='bold')

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$\Sigma\mathbf{F} = m'\Delta\mathbf{v}$" + ")]\n"
        "• (a) Fixed Vane (" + r"$u = 0,\ m' = \rho A v$" + "):\n"
        r"   $\Delta v_x = -v(1 - \cos\theta),\quad \Delta v_y = v\sin\theta$" + "\n"
        r"   $F = \rho A v^2(1 - \cos\theta),\quad R = \rho A v^2\sin\theta$" + "\n"
        "• (b) Moving Vane (" + r"$u < v,\ m' = \rho A(v - u)$" + "):\n"
        r"   $v'_x = u + (v - u)\cos\theta \Rightarrow \Delta v_x = -(v - u)(1 - \cos\theta)$" + "\n"
        r"   $F = \rho A(v - u)^2(1 - \cos\theta),\quad R = \rho A(v - u)^2\sin\theta$"
    )
    ax_calc.text(5.0, 4.35, sol_text, fontsize=9.6, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    m_dot_a = rho * A * v
    F_a = m_dot_a * v * (1 - np.cos(theta))
    R_a = m_dot_a * v * np.sin(theta)

    m_dot_b = rho * A * (v - u_curr)
    F_b = rho * A * (v - u_curr)**2 * (1 - np.cos(theta))
    R_b = rho * A * (v - u_curr)**2 * np.sin(theta)

    live_text = (
        f"[Live Monitor ($v={v:.0f}\\ \\mathrm{{m/s}},\\ \\theta={theta_deg:.0f}^\\circ,\\ \\rho A={rho*A:.1f}\\ \\mathrm{{kg/m}}$)]\n"
        f"(a) Fixed ($u=0.0\\ \\mathrm{{m/s}}$): $m' = {m_dot_a:.1f}\\ \\mathrm{{kg/s}}$  |  "
        f"$F = {F_a:.1f}\\ \\mathrm{{N}},\\ R = {R_a:.1f}\\ \\mathrm{{N}}$\n"
        f"(b) Moving ($u={u_curr:.1f}\\ \\mathrm{{m/s}}$): $m' = {m_dot_b:.1f}\\ \\mathrm{{kg/s}}$  |  "
        f"$F = {F_b:.1f}\\ \\mathrm{{N}},\\ R = {R_b:.1f}\\ \\mathrm{{N}}$"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.4, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_6_fluid_vane_deflection.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
