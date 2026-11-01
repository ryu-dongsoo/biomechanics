"""
Engineering Mechanics: Dynamics 9th Ed. Chapter 4 (4.7 Variable Mass)
Sample Problem 4/10 - Vertical Lifting of an Open-Link Chain & Inelastic Energy Loss
- Pure white background (#ffffff) & 1:1 textbook schematic fidelity
- Theoretical verification:
  * Pulling force P(x) = rho*(g*x + v^2)
  * Platform reaction R(x) = rho*g*(L - x)
  * Energy lost during lift Delta_E = 1/2*rho*L*v^2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Representative numerical parameters for real-time quantitative display
L = 4.0         # Total chain length (m)
rho = 2.5       # Mass per unit length (kg/m)
v = 2.0         # Constant upward speed (m/s)
g = 9.81        # Gravitational acceleration (m/s^2)

n_frames = 50
x_vals = np.linspace(0.3, L - 0.1, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_chain_links(ax, x_pos, y_start, y_end, link_h=0.22):
    n_links = max(1, int((y_end - y_start) / link_h))
    ys = np.linspace(y_start + link_h / 2, y_end - link_h / 2, n_links)
    for idx, yc in enumerate(ys):
        if idx % 2 == 0:
            ell = patches.Ellipse((x_pos, yc), 0.14, link_h * 0.95,
                                  facecolor='#cfd8dc', edgecolor='#37474f', lw=1.6, zorder=4)
        else:
            ell = patches.Ellipse((x_pos, yc), 0.06, link_h * 0.95,
                                  facecolor='#90a4ae', edgecolor='#263238', lw=1.6, zorder=5)
        ax.add_patch(ell)


def update(frame):
    x = x_vals[frame]
    P_curr = rho * (g * x + v**2)
    R_curr = rho * g * (L - x)
    W_air = rho * g * x
    F_dyn = rho * v**2
    U_P = 0.5 * rho * g * x**2 + rho * v**2 * x
    dT = 0.5 * rho * x * v**2
    dVg = 0.5 * rho * g * x**2
    dE = U_P - (dT + dVg)

    # ---------------- 1. Main Physical Mechanism View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.6, 2.8)
    ax_main.set_ylim(-0.7, 5.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # Platform base
    plat_rect = patches.Rectangle((-1.8, -0.38), 3.6, 0.38, facecolor='#e0dcd5', edgecolor='#424242', lw=1.8)
    ax_main.add_patch(plat_rect)
    ax_main.plot([-1.9, 1.9], [0.0, 0.0], color='#212121', lw=2.4)

    # Heap of open links on platform (proportional to remaining length L - x)
    rem_ratio = (L - x) / L
    np.random.seed(42)
    n_pile = int(4 + 26 * rem_ratio)
    for i in range(n_pile):
        px = (i - n_pile / 2) * 0.038 + np.sin(i * 1.7) * 0.18 * rem_ratio
        py = 0.05 + (i % 3) * 0.045 * rem_ratio
        ang = np.sin(i * 2.3) * 25
        pile_ell = patches.Ellipse((px, py), 0.22, 0.09, angle=ang,
                                   facecolor='#b0bec5', edgecolor='#37474f', lw=1.2, zorder=3)
        ax_main.add_patch(pile_ell)

    # Vertically suspended moving chain links
    draw_chain_links(ax_main, 0.0, 0.0, x)

    # Pulling force vector P (Red)
    ax_main.annotate('', xy=(0.0, x + 0.85), xytext=(0.0, x),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, x + 0.55, f'$P = \\rho(gx + v^2)$\n$({P_curr:.1f}\\ \\mathrm{{N}})$',
                 color='#d32f2f', fontsize=11, fontweight='bold', va='center')

    # Upward velocity vector v (Green)
    v_y = max(0.5, x * 0.55)
    ax_main.annotate('', xy=(0.55, v_y + 0.65), xytext=(0.55, v_y),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=15))
    ax_main.text(0.72, v_y + 0.32, f'$v = {v:.1f}\\ \\mathrm{{m/s}}$\n(Constant)',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', va='center')

    # Dimension line x
    ax_main.plot([-1.45, -0.15], [x, x], color='#616161', lw=1.0)
    ax_main.plot([-1.45, -0.15], [0.0, 0.0], color='#616161', lw=1.0)
    ax_main.annotate('', xy=(-1.20, x), xytext=(-1.20, 0.0),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.4))
    ax_main.text(-1.35, x / 2.0, f'$x = {x:.2f}\\ \\mathrm{{m}}$',
                 fontsize=11, fontweight='bold', ha='right', va='center', color='#212121')

    # Bottom link impact note
    ax_main.text(0.65, 0.18, r'Inelastic Link Impact ($\dot{m} = \rho v$)',
                 fontsize=9.5, color='#bf360c', fontweight='bold')

    ax_main.set_title('Sample Problem 4/10: Open-Link Chain Lift', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. Right Panel (FBD I, II & Theoretical Analysis) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # Top FBD comparison box
    fbd_box = patches.FancyBboxPatch((0.3, 6.55), 9.4, 3.15, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[FBD Comparison] Method I (Variable Mass) vs Method II (Constant Mass)',
                 fontsize=10.0, fontweight='bold', ha='center', color='#1e3a5f')

    # Method I FBD (Left)
    ax_calc.add_patch(patches.Rectangle((2.1, 7.05), 0.22, 1.65, facecolor='#eceff1', edgecolor='#455a64', lw=1.5))
    ax_calc.annotate('', xy=(2.21, 9.25), xytext=(2.21, 8.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.40, 9.02, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(2.21, 7.45), xytext=(2.21, 8.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.42, 7.80, r'$\rho gx$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.text(1.30, 7.90, 'Method I\n(Variable m)', fontsize=9.2, ha='center', va='center', fontweight='bold')

    # Method II FBD (Right)
    ax_calc.add_patch(patches.Rectangle((6.7, 7.25), 0.22, 1.45, facecolor='#eceff1', edgecolor='#455a64', lw=1.5))
    pile_poly = patches.Polygon([[6.2, 7.05], [7.42, 7.05], [6.92, 7.25], [6.7, 7.25]],
                                facecolor='#cfd8dc', edgecolor='#455a64', lw=1.5)
    ax_calc.add_patch(pile_poly)
    ax_calc.annotate('', xy=(6.81, 9.25), xytext=(6.81, 8.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.00, 9.02, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(6.81, 7.50), xytext=(6.81, 8.20),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.02, 7.85, r'$\rho gL$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.annotate('', xy=(6.81, 7.05), xytext=(6.81, 6.62),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 6.75, r'$\rho g(L-x)$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.text(5.65, 7.90, 'Method II\n(Constant m)', fontsize=9.2, ha='center', va='center', fontweight='bold')

    # Middle Card: Theoretical Derivation
    sol_text = (
        r"■ Variable-Mass Equation ($\Sigma F_x = m\dot{v} + \dot{m}u$):" "\n"
        r"  $\bullet\ \dot{v}=0,\ \dot{m}=\rho v,\ u=v-0=v \Rightarrow P - \rho gx = 0 + (\rho v)v$" "\n"
        r"  $\bullet\ \mathbf{P(x) = \rho(gx + v^2)} = \rho gx\ (\mathrm{Weight}) + \rho v^2\ (\mathrm{Momentum\ flux})$" "\n"
        r"■ Inelastic Impact Energy Loss ($\Delta E$ over $x = 0 \to L$):" "\n"
        r"  $\bullet\ \int_0^L P\,dx - \Delta E = \Delta T + \Delta V_g \Rightarrow \left(\frac{1}{2}\rho gL^2 + \rho Lv^2\right) - \Delta E = \frac{1}{2}\rho Lv^2 + \frac{1}{2}\rho gL^2$" "\n"
        r"  $\bullet\ $Theoretical Value: $\mathbf{\Delta E = \frac{1}{2}\rho Lv^2}$"
    )
    ax_calc.text(0.35, 4.35, sol_text, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # Bottom Card: Real-Time Monitor
    live_text = (
        f"[Real-Time Monitor: $L={L:.1f}\\ \\mathrm{{m}},\\ \\rho={rho:.1f}\\ \\mathrm{{kg/m}},\\ v={v:.1f}\\ \\mathrm{{m/s}}$]\n"
        f"• Suspended Weight: $\\rho gx = {W_air:.1f}\\ \\mathrm{{N}}$   |   Dynamic Thrust: $\\rho v^2 = {F_dyn:.1f}\\ \\mathrm{{N}}$\n"
        f"• Pulling Force: $P(x) = {P_curr:.1f}\\ \\mathrm{{N}}$   |   Platform Reaction: $R = {R_curr:.1f}\\ \\mathrm{{N}}$\n"
        f"• Cumulative Energy Loss: $\\Delta E(x) = \\frac{{1}}{{2}}\\rho xv^2 = {dE:.1f}\\ \\mathrm{{J}}$ (Total at $L$: ${0.5*rho*L*v**2:.1f}\\ \\mathrm{{J}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_10_open_link_chain_lift.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
