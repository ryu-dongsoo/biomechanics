"""
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.6: Steady Mass Flow
Sample Problem 4/9 - Air-Breathing Jet Aircraft Equation of Motion and Thrust T
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Theoretical validation:
  * Moving reference frame (+x forward with aircraft):
    - Air flow m'_a: Delta v_a = -u - (-v) = -(u - v)
    - Fuel flow m'_f: Delta v_f = -u - 0 = -u
    - Exhaust gas flow: m'_g = m'_a + m'_f
  * Force-momentum equation: -m*g*sin(theta) - D = -m'_a*(u - v) - m'_f*u = -m'_g*u + m'_a*v
  * Effective Thrust: T = m'_g*u - m'_a*v  (Approximation: T ~= m'_g*(u - v) when m'_f << m'_a)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

m = 8000.0            # Aircraft mass (8 Mg)
g = 9.81
v = 250.0             # Flight speed (250 m/s = 900 km/h)
u = 750.0             # Relative exhaust speed (750 m/s)
m_dot_a = 80.0        # Air intake rate (80 kg/s)
m_dot_f = 1.6         # Fuel burn rate (1.6 kg/s, 2% of m'_a)
m_dot_g = m_dot_a + m_dot_f  # 81.6 kg/s
theta_deg = 12.0      # Climb angle (deg)
theta = np.radians(theta_deg)

T_exact = m_dot_g * u - m_dot_a * v          # 41,200 N (41.2 kN)
T_approx = m_dot_g * (u - v)                 # 40,800 N (40.8 kN)
D_eq = T_exact - m * g * np.sin(theta)

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_jet_polygon(cx, cy, scale=1.0, ang_deg=theta_deg):
    body = np.array([
        [2.6, 0.0],
        [1.5, 0.25],
        [0.8, 0.42],
        [0.1, 0.30],
        [-1.6, 0.28],
        [-2.3, 0.95],
        [-2.65, 0.95],
        [-2.45, 0.25],
        [-2.55, 0.14],
        [-2.55, -0.14],
        [-1.8, -0.22],
        [0.4, -0.26],
        [0.7, -0.12],
        [1.6, -0.15],
    ]) * scale

    wing = np.array([
        [0.3, -0.05],
        [-0.9, -0.18],
        [-1.3, -0.05],
        [0.1, 0.05]
    ]) * scale

    canopy = np.array([
        [1.45, 0.22],
        [0.8, 0.39],
        [0.18, 0.28],
        [0.8, 0.18]
    ]) * scale

    rad = np.radians(ang_deg)
    R_mat = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])

    body_rot = body @ R_mat.T + np.array([cx, cy])
    wing_rot = wing @ R_mat.T + np.array([cx, cy])
    canopy_rot = canopy @ R_mat.T + np.array([cx, cy])
    return body_rot, wing_rot, canopy_rot, R_mat


def update(frame):
    phase_t = (frame * 0.08) % 1.0
    s_flight = -0.45 + 0.90 * (frame / (n_frames - 1))
    tx, ty = np.cos(theta), np.sin(theta)
    nx, ny = -np.sin(theta), np.cos(theta)

    cx = 4.9 + s_flight * tx
    cy = 4.6 + s_flight * ty

    # ---------------- 1. Left Panel: Jet Aircraft Steady Mass Flow ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(1.2, 8.0)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    p_base = np.array([cx, cy]) - 3.6 * np.array([tx, ty])
    p_front = np.array([cx, cy]) + 3.8 * np.array([tx, ty])
    ax_main.plot([p_base[0], p_front[0]], [p_base[1], p_front[1]], color='#90a4ae', ls='--', lw=1.2, zorder=1)
    ax_main.text(p_front[0] + 0.15, p_front[1] + 0.05, r'$x$', fontsize=11, fontweight='bold', color='#546e7a')

    ang_pivot = np.array([cx, cy]) + 1.8 * np.array([tx, ty])
    ax_main.plot([ang_pivot[0], ang_pivot[0] + 1.6], [ang_pivot[1], ang_pivot[1]], color='#777777', ls=':', lw=1.2)
    arc_th = patches.Arc(ang_pivot, 1.3, 1.3, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.4)
    ax_main.add_patch(arc_th)
    ax_main.text(ang_pivot[0] + 0.92, ang_pivot[1] + 0.14, r'$\theta = 12^\circ$', fontsize=9.8, fontweight='bold')

    body_pts, wing_pts, canopy_pts, R_mat = get_jet_polygon(cx, cy, scale=1.05, ang_deg=theta_deg)
    ax_main.add_patch(patches.Polygon(body_pts, facecolor='#cfd8dc', edgecolor='#263238', lw=1.9, zorder=4))
    ax_main.add_patch(patches.Polygon(wing_pts, facecolor='#90a4ae', edgecolor='#263238', lw=1.5, zorder=5))
    ax_main.add_patch(patches.Polygon(canopy_pts, facecolor='#81d4fa', edgecolor='#0277bd', lw=1.4, zorder=5))

    noz_pos = np.array([cx, cy]) + R_mat @ np.array([-2.68, 0.0])
    for dy_off in [-0.12, 0.0, 0.12]:
        p_start = noz_pos + dy_off * np.array([nx, ny])
        p_end = p_start - 1.35 * np.array([tx, ty])
        ax_main.annotate('', xy=p_end, xytext=p_start,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=3)
    ax_main.text(noz_pos[0] - 0.95 * tx + 0.35 * nx, noz_pos[1] - 0.95 * ty + 0.35 * ny,
                 r"Exhaust $m'_g,\ u$", fontsize=9.6, fontweight='bold', color='#00695c', ha='center')

    intake_pos = np.array([cx, cy]) + R_mat @ np.array([0.85, -0.18])
    for k in range(3):
        frac = ((k / 3.0) + phase_t) % 1.0
        pt_air = intake_pos + (1.2 - frac * 1.0) * np.array([tx, ty])
        ax_main.plot(pt_air[0], pt_air[1], 'o', color='#0288d1', markersize=4.0, zorder=5)

    v_orig = np.array([cx, cy]) + 0.55 * np.array([nx, ny]) + 0.4 * np.array([tx, ty])
    v_end = v_orig + 1.45 * np.array([tx, ty])
    ax_main.annotate('', xy=v_end, xytext=v_orig,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(0.5 * (v_orig[0] + v_end[0]) - 0.1, 0.5 * (v_orig[1] + v_end[1]) + 0.25,
                 f'$v = {v:.0f}\\ \\mathrm{{m/s}}$', fontsize=10.2, fontweight='bold', color='#2e7d32', ha='center')

    cg = np.array([cx, cy])
    ax_main.annotate('', xy=cg + np.array([0, 0.32]), xytext=cg + np.array([0, 1.85]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(cg[0] + 0.15, cg[1] + 1.75, r'$mg$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    ax_main.annotate('', xy=cg - 0.25 * np.array([nx, ny]), xytext=cg - 1.85 * np.array([nx, ny]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(cg[0] - 1.75 * nx + 0.22, cg[1] - 1.75 * ny, r'$L$', fontsize=11.5, fontweight='bold', color='#d32f2f')

    d_pt = cg + 1.25 * np.array([tx, ty]) - 0.38 * np.array([nx, ny])
    ax_main.annotate('', xy=d_pt, xytext=d_pt + 1.25 * np.array([tx, ty]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(d_pt[0] + 0.75 * tx, d_pt[1] + 0.75 * ty - 0.32, r'$D$', fontsize=11.5, fontweight='bold', color='#d32f2f')

    banner_text = (
        "Effective Thrust Model: Gross Thrust (" + r"$+m'_g u$" + ") - Ram Drag (" + r"$-m'_a v$" + ")  "
        + r"$\Rightarrow\ \mathbf{T = m'_g u - m'_a v}$"
    )
    ax_main.text(4.9, 1.75, banner_text, fontsize=9.8, fontweight='bold', color='#1d4564', ha='center',
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    ax_main.set_title('Sample Problem 4/9: Air-Breathing Jet Aircraft Thrust $T$', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Equivalent Thrust Models & Derivation ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.50, 'Internal Duct Forces vs. Equivalent External Thrust ($T$) Model',
                 fontsize=10.8, fontweight='bold', ha='center', color='#1d4564')

    ax_calc.add_patch(patches.FancyBboxPatch((0.4, 6.85), 4.2, 2.2, boxstyle='round,pad=0.15',
                                             facecolor='#fff8e1', edgecolor='#ffb300', lw=1.4))
    ax_calc.text(2.5, 8.75, '① Exposed Internal Boundary', fontsize=9.6, fontweight='bold', ha='center', color='#e65100')
    ax_calc.annotate('', xy=(2.3, 7.95), xytext=(0.8, 7.95),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13))
    ax_calc.text(1.55, 8.22, r"$m'_g u$ (Exhaust)", fontsize=9.1, fontweight='bold', color='#d32f2f', ha='center')
    ax_calc.annotate('', xy=(2.7, 7.35), xytext=(4.2, 7.35),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=13))
    ax_calc.text(3.45, 7.62, r"$m'_a v$ (Ram Drag)", fontsize=9.1, fontweight='bold', color='#1565c0', ha='center')

    ax_calc.add_patch(patches.FancyBboxPatch((5.4, 6.85), 4.2, 2.2, boxstyle='round,pad=0.15',
                                             facecolor='#e8f5e9', edgecolor='#43a047', lw=1.4))
    ax_calc.text(7.5, 8.75, '② Equivalent Thrust ($T$) Model', fontsize=9.6, fontweight='bold', ha='center', color='#1b5e20')
    ax_calc.annotate('', xy=(8.6, 7.85), xytext=(6.2, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(7.4, 8.18, r"$T = m'_g u - m'_a v$", fontsize=9.8, fontweight='bold', color='#2e7d32', ha='center')
    ax_calc.text(7.5, 7.20, r"$T - mg\sin\theta - D = m\dot{v}$", fontsize=9.3, fontweight='bold', color='#263238', ha='center')

    sol_text = (
        "[Theoretical Derivation & Analysis (Moving Axes " + r"$\Sigma F_x = m'\Delta v_x$" + ")]\n"
        "• Air Flow (" + r"$m'_a$" + "): " + r"$\Delta v_a = (-u) - (-v) = -(u - v)$" + "\n"
        "• Fuel Flow (" + r"$m'_f$" + "): " + r"$\Delta v_f = (-u) - 0 = -u \quad (m'_g = m'_a + m'_f)$" + "\n"
        "• Flight-Path Momentum Equation:\n"
        r"   $-mg\sin\theta - D = -m'_a(u - v) - m'_f u = -m'_g u + m'_a v$" + "\n"
        "• Exact & Approximate Thrust (" + r"$m'_f \ll m'_a \Rightarrow m'_g \cong m'_a$" + "):\n"
        "   " + r"$\mathbf{T = m'_g u - m'_a v}$" + "     and     " + r"$\mathbf{T \cong m'_g(u - v)}$"
    )
    ax_calc.text(5.0, 4.30, sol_text, fontsize=9.3, ha='center', va='center', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.48', facecolor='#fbfbfb', edgecolor='#cccccc'))

    gross_thrust = m_dot_g * u
    ram_drag = m_dot_a * v
    err_pct = abs(T_exact - T_approx) / T_exact * 100.0

    live_text = (
        f"[Quantitative Verification ($m'_a={m_dot_a:.0f}\\ \\mathrm{{kg/s}},\\ m'_f={m_dot_f:.1f}\\ \\mathrm{{kg/s}},\\ "
        f"v={v:.0f}\\ \\mathrm{{m/s}},\\ u={u:.0f}\\ \\mathrm{{m/s}}$)]\n"
        f"Gross thrust: $m'_g u = {gross_thrust/1000:.2f}\\ \\mathrm{{kN}}$  |  Ram drag: $m'_a v = {ram_drag/1000:.2f}\\ \\mathrm{{kN}}$\n"
        f"Exact Thrust: $\\mathbf{{T = {T_exact/1000:.2f}\\ \\mathrm{{kN}}}}$  |  "
        f"Approx: $T \\cong m'_g(u-v) = {T_approx/1000:.2f}\\ \\mathrm{{kN}}$ (Diff {err_pct:.2f}%)"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.1, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_9_jet_aircraft_thrust.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
