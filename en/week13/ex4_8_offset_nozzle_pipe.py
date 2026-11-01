"""
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.6: Steady Mass Flow
Sample Problem 4/8 - Internal Loads (Tension T, Shear Q, Moment M) in Offset Nozzle Pipe
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Theoretical validation:
  * Continuity: A0*v0 = A*v -> v0 = v*(A/A0), m' = rho*A*v
  * Tension T: p*A0 - T = m'*(v*cos(theta) - v0) -> T = p*A0 + rho*A*v^2*(A/A0 - cos(theta))
  * Shear Q: -Q = m'*(-v*sin(theta) - 0) -> Q = rho*A*v^2*sin(theta)
  * Moment M (CW+ about O): M = m'*(v*cos(theta)*a + v*sin(theta)*b) = rho*A*v^2*(a*cos(theta) + b*sin(theta))
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

rho = 1000.0         # Fluid density (kg/m^3)
A0 = 0.010           # Inlet C area (m^2)
A = 0.0025           # Exit B area (m^2), A/A0 = 0.25
p = 250000.0         # Static gage pressure p = 250 kPa
v_nom = 24.0         # Nominal exit speed (m/s)
theta_deg = 45.0     # Discharge angle (deg)
theta = np.radians(theta_deg)
a_dim = 0.35         # Vertical offset a (m)
b_dim = 0.50         # Horizontal offset b (m)

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_nozzle_geometry():
    x_C, y_C = 3.2, 3.2
    x_B, y_B = 6.7, 5.65

    t_param = np.linspace(0, 1, 50)
    P0 = np.array([x_C, y_C])
    P1 = np.array([x_C + 1.5, y_C + 0.1])
    P2 = np.array([x_B - 0.9, y_B + 0.9])
    P3 = np.array([x_B, y_B])

    s = t_param[:, None]
    center = ((1 - s)**3) * P0 + 3 * ((1 - s)**2) * s * P1 + 3 * (1 - s) * (s**2) * P2 + (s**3) * P3
    dcenter = 3 * ((1 - s)**2) * (P1 - P0) + 6 * (1 - s) * s * (P2 - P1) + 3 * (s**2) * (P3 - P2)
    tang = dcenter / np.linalg.norm(dcenter, axis=1, keepdims=True)
    norm = np.column_stack([-tang[:, 1], tang[:, 0]])

    r_prof = 0.52 * (1 - t_param) + 0.24 * t_param
    upper = center + norm * r_prof[:, None]
    lower = center - norm * r_prof[:, None]
    return center, upper, lower, tang[-1]


center_pts, upper_pts, lower_pts, exit_tang = get_nozzle_geometry()
x_C, y_C = center_pts[0]
x_B, y_B = center_pts[-1]


def update(frame):
    v_curr = 20.0 + 4.0 * np.sin(2 * np.pi * frame / n_frames)
    if frame > n_frames - 8:
        v_curr = v_nom
    phase_t = (frame * 0.08) % 1.0

    # ---------------- 1. Left Panel: Offset Nozzle Mechanism ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(1.2, 7.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 1) Fixed horizontal supply pipe
    pipe_r = 0.52
    ax_main.add_patch(patches.Rectangle((1.1, y_C - pipe_r), x_C - 1.1, 2 * pipe_r,
                                        facecolor='#cfd8dc', edgecolor='#37474f', lw=2.0, zorder=3))
    for bx in [1.65, 2.55]:
        ax_main.add_patch(patches.Rectangle((bx - 0.14, y_C - pipe_r - 0.55), 0.28, 2 * pipe_r + 0.62,
                                            facecolor='#90a4ae', edgecolor='#263238', lw=1.6, zorder=4))
        ax_main.add_patch(patches.Rectangle((bx - 0.26, y_C - pipe_r - 0.68), 0.52, 0.14,
                                            facecolor='#78909c', edgecolor='#263238', lw=1.5, zorder=4))
    ax_main.fill_between([1.15, 3.05], y_C - pipe_r - 0.95, y_C - pipe_r - 0.68, color='#e0dcd5', zorder=2)
    ax_main.plot([1.15, 3.05], [y_C - pipe_r - 0.68, y_C - pipe_r - 0.68], color='#333333', lw=2.0, zorder=4)

    # Flange at C
    ax_main.add_patch(patches.Rectangle((x_C - 0.08, y_C - pipe_r - 0.18), 0.16, 2 * pipe_r + 0.36,
                                        facecolor='#607d8b', edgecolor='#263238', lw=1.8, zorder=5))
    ax_main.text(x_C, y_C + pipe_r + 0.32, r'$C\ (A_0)$', fontsize=11.2, fontweight='bold', ha='center', color='#1d4564')

    # 2) Offset nozzle body
    noz_poly = np.vstack([lower_pts, upper_pts[::-1]])
    ax_main.add_patch(patches.Polygon(noz_poly, facecolor='#a5d6a7', edgecolor='#1b5e20', lw=2.0, zorder=3))

    # 3) Discharging jet at B
    s_jet = np.linspace(0, 1.85, 20)
    jet_dir = np.array([np.cos(theta), -np.sin(theta)])
    jet_norm = np.array([np.sin(theta), np.cos(theta)])
    r_exit = 0.20
    j_center = np.array([x_B, y_B])[None, :] + s_jet[:, None] * jet_dir[None, :]
    j_up = j_center + r_exit * jet_norm[None, :]
    j_lo = j_center - r_exit * jet_norm[None, :]
    jet_poly = np.vstack([j_lo, j_up[::-1]])
    ax_main.add_patch(patches.Polygon(jet_poly, facecolor='#bbdefb', edgecolor='#1976d2', lw=1.2, alpha=0.85, zorder=2))

    for k in range(6):
        frac = ((k / 6.0) + phase_t) % 1.0
        idx = int(frac * (len(center_pts) - 1))
        ax_main.plot(center_pts[idx, 0], center_pts[idx, 1], 'o', color='#1b5e20', markersize=4.5, zorder=4)
    for k in range(4):
        frac = ((k / 4.0) + phase_t * 1.5) % 1.0
        pt = np.array([x_B, y_B]) + frac * 1.65 * jet_dir
        ax_main.plot(pt[0], pt[1], 'o', color='#0d47a1', markersize=4.5, zorder=4)

    for dy in [-0.28, 0.0, 0.28]:
        ax_main.annotate('', xy=(1.05, y_C + dy), xytext=(0.45, y_C + dy),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.8, mutation_scale=11))
    ax_main.text(0.75, y_C + 0.55, r'$p,\ v_0$', fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')

    v_tip = np.array([x_B, y_B]) + 1.35 * jet_dir
    ax_main.annotate('', xy=v_tip, xytext=(x_B, y_B),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15), zorder=6)
    ax_main.text(v_tip[0] - 0.35, v_tip[1] - 0.32, f'$v = {v_curr:.1f}\\ \\mathrm{{m/s}}$',
                 fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')
    ax_main.text(x_B - 0.25, y_B - 0.38, r'$B\ (A)$', fontsize=11.0, fontweight='bold', color='#1b5e20', ha='right')

    ax_main.plot([x_B, x_B + 1.35], [y_B, y_B], color='#555555', ls='--', lw=1.2)
    arc_th = patches.Arc((x_B, y_B), 1.1, 1.1, angle=0, theta1=-theta_deg, theta2=0, color='#222222', lw=1.4)
    ax_main.add_patch(arc_th)
    ax_main.text(x_B + 0.72, y_B - 0.26, r'$\theta$', fontsize=11, fontweight='bold')

    y_dim_b = 6.85
    ax_main.plot([x_C, x_C], [y_C + pipe_r + 0.65, y_dim_b + 0.15], color='#777777', lw=1.0)
    ax_main.plot([x_B, x_B], [y_B + 0.35, y_dim_b + 0.15], color='#777777', lw=1.0)
    ax_main.annotate('', xy=(x_B, y_dim_b), xytext=(x_C, y_dim_b),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.4))
    ax_main.text(0.5 * (x_C + x_B), y_dim_b + 0.15, f'$b = {b_dim:.2f}\\ \\mathrm{{m}}$',
                 fontsize=10.2, fontweight='bold', ha='center')

    x_dim_a = 8.45
    ax_main.plot([x_C + 0.3, x_dim_a + 0.15], [y_C, y_C], color='#777777', ls='--', lw=1.0)
    ax_main.plot([x_B, x_dim_a + 0.15], [y_B, y_B], color='#777777', lw=1.0)
    ax_main.annotate('', xy=(x_dim_a, y_B), xytext=(x_dim_a, y_C),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.4))
    ax_main.text(x_dim_a + 0.18, 0.5 * (y_C + y_B), f'$a = {a_dim:.2f}\\ \\mathrm{{m}}$',
                 fontsize=10.2, fontweight='bold', va='center')

    ax_main.set_title('Sample Problem 4/8: Offset Nozzle with Static Pressure', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: FBD & Internal Loads Analysis ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.55, 'FBD of Nozzle + Internal Fluid (Section $C$ Loads & $pA_0$)',
                 fontsize=10.8, fontweight='bold', ha='center', color='#1d4564')

    scale_fbd = 0.65
    offset_fbd = np.array([2.2, 5.45])
    fbd_poly = (noz_poly - np.array([x_C, y_C])) * scale_fbd + offset_fbd
    ax_calc.add_patch(patches.Polygon(fbd_poly, facecolor='#f1f8e9', edgecolor='#33691e', lw=1.6, zorder=2))

    O_pt = offset_fbd
    ax_calc.plot(O_pt[0], O_pt[1], 'ko', markersize=4.5, zorder=5)
    ax_calc.text(O_pt[0] + 0.22, O_pt[1] + 0.15, r'$O$', fontsize=10.5, fontweight='bold')

    ax_calc.plot([O_pt[0] - 0.5, O_pt[0] + 3.4], [O_pt[1], O_pt[1]], color='#888888', ls='--', lw=1.0)
    ax_calc.plot([O_pt[0], O_pt[0]], [O_pt[1] - 0.8, O_pt[1] + 2.2], color='#888888', ls='--', lw=1.0)
    ax_calc.text(O_pt[0] + 3.5, O_pt[1], r'$x$', fontsize=10, va='center')
    ax_calc.text(O_pt[0], O_pt[1] + 2.3, r'$y$', fontsize=10, ha='center')

    ax_calc.annotate('', xy=(O_pt[0] - 1.35, O_pt[1] + 0.12), xytext=(O_pt[0], O_pt[1] + 0.12),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13), zorder=5)
    ax_calc.text(O_pt[0] - 1.42, O_pt[1] + 0.12, r'$T$', fontsize=11, fontweight='bold', color='#d32f2f', ha='right', va='center')

    ax_calc.annotate('', xy=(O_pt[0], O_pt[1] - 0.18), xytext=(O_pt[0] - 1.25, O_pt[1] - 0.18),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13), zorder=5)
    ax_calc.text(O_pt[0] - 1.32, O_pt[1] - 0.22, r'$p A_0$', fontsize=10.5, fontweight='bold', color='#d32f2f', ha='right', va='center')

    ax_calc.annotate('', xy=(O_pt[0], O_pt[1] - 1.15), xytext=(O_pt[0], O_pt[1]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13), zorder=5)
    ax_calc.text(O_pt[0] + 0.18, O_pt[1] - 1.05, r'$Q$', fontsize=11, fontweight='bold', color='#d32f2f', va='center')

    arc_m = patches.Arc(O_pt, 1.15, 1.15, angle=0, theta1=115, theta2=245, color='#d32f2f', lw=2.2)
    ax_calc.add_patch(arc_m)
    ax_calc.annotate('', xy=(O_pt[0] - 0.20, O_pt[1] + 0.54), xytext=(O_pt[0] - 0.42, O_pt[1] + 0.38),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.2, mutation_scale=12), zorder=5)
    ax_calc.text(O_pt[0] - 0.65, O_pt[1] + 0.58, r'$M$', fontsize=11, fontweight='bold', color='#d32f2f')

    sol_text = (
        "[Theoretical Derivation & Analysis (Eqs. 4.18, 4.19)]\n"
        "• Continuity: " + r"$A_0 v_0 = A v \Rightarrow v_0 = v\frac{A}{A_0},\quad m' = \rho A v$" + "\n"
        "• Tension " + r"$T$" + " (" + r"$\Sigma F_x = m'\Delta v_x$" + "): " + r"$p A_0 - T = \rho A v(v\cos\theta - v_0)$" + "\n"
        r"   $\Rightarrow \mathbf{T = p A_0 + \rho A v^2\left(\frac{A}{A_0} - \cos\theta\right)}$" + "\n"
        "• Shear " + r"$Q$" + " (" + r"$\Sigma F_y = m'\Delta v_y$" + "): " + r"$-Q = \rho A v(-v\sin\theta - 0) \Rightarrow \mathbf{Q = \rho A v^2\sin\theta}$" + "\n"
        "• Moment " + r"$M$" + " (" + r"$\Sigma M_O = m'(v_2 d_2 - v_1 d_1)$" + "): " + r"$\mathbf{M = \rho A v^2(a\cos\theta + b\sin\theta)}$"
    )
    ax_calc.text(5.0, 3.85, sol_text, fontsize=9.3, ha='center', va='center', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    m_dot = rho * A * v_curr
    T_val = p * A0 + rho * A * (v_curr**2) * (A / A0 - np.cos(theta))
    Q_val = rho * A * (v_curr**2) * np.sin(theta)
    M_val = rho * A * (v_curr**2) * (a_dim * np.cos(theta) + b_dim * np.sin(theta))

    live_text = (
        f"[Live Section Loads ($p={p/1000:.0f}\\ \\mathrm{{kPa}},\\ A/A_0={A/A0:.2f},\\ \\theta={theta_deg:.0f}^\\circ$)]\n"
        f"Exit speed: $v = {v_curr:.1f}\\ \\mathrm{{m/s}}$  |  Mass flow: $m' = {m_dot:.1f}\\ \\mathrm{{kg/s}}$  |  Pressure force: $pA_0 = {p*A0:.0f}\\ \\mathrm{{N}}$\n"
        f"Internal Loads: $\\mathbf{{T = {T_val:.0f}\\ \\mathrm{{N}}}}$,  $\\mathbf{{Q = {Q_val:.0f}\\ \\mathrm{{N}}}}$,  "
        f"$\\mathbf{{M = {M_val:.1f}\\ \\mathrm{{N\\cdot m}}}}$"
    )
    ax_calc.text(5.0, 1.05, live_text, fontsize=9.1, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_8_offset_nozzle_pipe.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
