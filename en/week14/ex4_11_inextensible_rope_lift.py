# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

"""
Engineering Mechanics: Dynamics 9th Ed. Chapter 4 (4.7 Variable Mass)
Sample Problem 4/11 - Conservative Vertical Lifting of an Inextensible Flexible Rope / Bicycle Chain
- Pure white background (#ffffff) & 1:1 textbook schematic fidelity (including rotating guide omega = v/r)
- Theoretical verification:
  * Pulling force P(x) = rho*g*x + 1/2*rho*v^2
  * Platform reaction R(x) = rho*g*(L - x) + 1/2*rho*v^2
  * Bottom tension T_0 = 1/2*rho*v^2, guide force F = 1/2*rho*v^2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Representative numerical parameters
L = 4.0         # Total rope length (m)
rho = 2.5       # Mass per unit length (kg/m)
v = 2.0         # Constant upward speed (m/s)
g = 9.81        # Gravitational acceleration (m/s^2)

n_frames = 50
x_vals = np.linspace(0.4, L - 0.1, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def update(frame):
    x = x_vals[frame]
    T0 = 0.5 * rho * v**2
    P_curr = rho * g * x + T0
    W_rem = rho * g * (L - x)
    R_curr = W_rem + T0
    U_P = 0.5 * rho * g * x**2 + 0.5 * rho * v**2 * x
    dT = 0.5 * rho * x * v**2
    dVg = 0.5 * rho * g * x**2

    # ---------------- 1. Main Physical Mechanism View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.8, 2.8)
    ax_main.set_ylim(-0.9, 5.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # Platform base
    plat_rect = patches.Rectangle((-1.9, -0.35), 3.8, 0.35, facecolor='#e5d8c8', edgecolor='#5d4037', lw=1.8)
    ax_main.add_patch(plat_rect)
    ax_main.plot([-2.0, 2.0], [0.0, 0.0], color='#3e2723', lw=2.4)

    # Coiled rope cross-sections on platform
    rem_ratio = (L - x) / L
    n_coils = max(1, int(5 * rem_ratio))
    for i in range(n_coils):
        cy = 0.06 + i * 0.09
        ax_main.add_patch(patches.Circle((-0.38, cy), 0.042, facecolor='#e6c29f', edgecolor='#6d4c41', lw=1.3))
        ax_main.add_patch(patches.Circle((+0.38, cy), 0.042, facecolor='#e6c29f', edgecolor='#6d4c41', lw=1.3))

    # Bottom smooth transition guide housing & rotating cylinder (omega = v/r)
    guide_housing = patches.Polygon([[-0.32, 0.0], [-0.32, 0.38], [-0.08, 0.38], [-0.08, 0.0]],
                                    facecolor='#cfd8dc', edgecolor='#455a64', lw=1.4, zorder=3)
    guide_housing_r = patches.Polygon([[0.08, 0.0], [0.08, 0.38], [0.32, 0.38], [0.32, 0.0]],
                                      facecolor='#cfd8dc', edgecolor='#455a64', lw=1.4, zorder=3)
    ax_main.add_patch(guide_housing)
    ax_main.add_patch(guide_housing_r)

    cam = patches.Circle((0.0, 0.22), 0.16, facecolor='#f5d6ba', edgecolor='#5d4037', lw=1.6, zorder=4)
    ax_main.add_patch(cam)
    ang_rot = frame * 18.0
    rad_rot = np.radians(ang_rot)
    ax_main.plot([0.0, 0.12 * np.cos(rad_rot)], [0.22, 0.22 + 0.12 * np.sin(rad_rot)], color='#5d4037', lw=1.8, zorder=5)
    ax_main.text(0.48, 0.22, r'Smooth Guide ($\omega = v/r$)' '\n' r'Lossless Transition ($\Delta E = 0$)',
                 fontsize=9.2, color='#37474f', fontweight='bold', va='center')

    # Vertically moving inextensible rope
    rope_rect = patches.Rectangle((-0.055, 0.22), 0.11, x - 0.22,
                                  facecolor='#e6c29f', edgecolor='#5d4037', lw=1.8, zorder=4)
    ax_main.add_patch(rope_rect)

    # Pulling force P arrow
    ax_main.annotate('', xy=(0.0, x + 0.85), xytext=(0.0, x),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, x + 0.52, f'$P = \\rho gx + \\frac{{1}}{{2}}\\rho v^2$\n$({P_curr:.1f}\\ \\mathrm{{N}})$',
                 color='#d32f2f', fontsize=11, fontweight='bold', va='center')

    # Platform reaction R arrow
    ax_main.annotate('', xy=(0.0, 0.0), xytext=(0.0, -0.78),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, -0.62, f'$R = \\rho g(L-x) + \\frac{{1}}{{2}}\\rho v^2 = {R_curr:.1f}\\ \\mathrm{{N}}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', va='center')

    # Velocity vector v (Green)
    v_y = max(0.75, x * 0.55)
    ax_main.annotate('', xy=(-0.55, v_y + 0.65), xytext=(-0.55, v_y),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=15))
    ax_main.text(-0.70, v_y + 0.32, f'$v = {v:.1f}\\ \\mathrm{{m/s}}$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right', va='center')

    # Dimension line x
    ax_main.plot([-1.55, -0.15], [x, x], color='#616161', lw=1.0)
    ax_main.plot([-1.55, -0.15], [0.0, 0.0], color='#616161', lw=1.0)
    ax_main.annotate('', xy=(-1.35, x), xytext=(-1.35, 0.0),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.4))
    ax_main.text(-1.48, x / 2.0, f'$x = {x:.2f}\\ \\mathrm{{m}}$',
                 fontsize=11, fontweight='bold', ha='right', va='center', color='#212121')

    ax_main.set_title('Sample Problem 4/11: Inextensible Flexible Rope Lift', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. Right Panel (Split FBD & Work-Energy / Momentum Analysis) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # Top FBD Box
    fbd_box = patches.FancyBboxPatch((0.3, 6.45), 9.4, 3.25, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[Split FBDs] Moving Vertical Section ($T_0$) & Bottom Guide/Coil ($R$)',
                 fontsize=10.0, fontweight='bold', ha='center', color='#1e3a5f')

    # Left: Moving Vertical Rope FBD
    ax_calc.add_patch(patches.Rectangle((2.2, 7.35), 0.20, 1.45, facecolor='#e6c29f', edgecolor='#5d4037', lw=1.5))
    ax_calc.annotate('', xy=(2.30, 9.28), xytext=(2.30, 8.80),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.48, 9.05, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(2.30, 7.75), xytext=(2.30, 8.35),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.50, 8.05, r'$\rho gx$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.annotate('', xy=(2.30, 6.80), xytext=(2.30, 7.35),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.50, 6.95, r'$T_0 = \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.text(1.25, 8.05, 'Vertical Part\n($\dot{v}=0$ Equil.)', fontsize=9.0, ha='center', va='center', fontweight='bold')

    # Right: Bottom Guide & Coil FBD
    ax_calc.add_patch(patches.Rectangle((6.4, 7.15), 0.90, 0.55, facecolor='#cfd8dc', edgecolor='#455a64', lw=1.5))
    ax_calc.annotate('', xy=(6.85, 8.35), xytext=(6.85, 7.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 8.10, r'$T_0 = \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.annotate('', xy=(7.30, 7.42), xytext=(8.05, 7.42),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.0))
    ax_calc.text(8.12, 7.42, r'Guide $F = \frac{1}{2}\rho v^2$', color='#1565c0', fontsize=9.2, fontweight='bold', va='center')
    ax_calc.annotate('', xy=(6.85, 7.15), xytext=(6.85, 6.58),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 6.72, r'$R = \rho g(L-x) + \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.2, fontweight='bold')
    ax_calc.text(5.40, 7.45, 'Bottom Coil\n& Guide', fontsize=9.0, ha='center', va='center', fontweight='bold')

    # Middle Card: Work-Energy & Momentum Derivation
    sol_text = (
        r"■ Conservative Work-Energy Equation ($dU' = dT + dV_g,\ \Delta E = 0$):" "\n"
        r"  $\bullet\ P\,dx = d\left(\frac{1}{2}\rho xv^2\right) + d\left(\rho gx\frac{x}{2}\right) \Rightarrow \mathbf{P = \rho gx + \frac{1}{2}\rho v^2}$" "\n"
        r"■ Total Rope Impulse-Momentum ($\Sigma F_x = \dot{G}_x$):" "\n"
        r"  $\bullet\ P + R - \rho gL = \frac{d}{dt}(\rho xv) = \rho v^2 \Rightarrow \left(\rho gx + \frac{1}{2}\rho v^2\right) + R - \rho gL = \rho v^2$" "\n"
        r"  $\bullet\ $Theoretical Value: $\mathbf{R = \rho g(L - x) + \frac{1}{2}\rho v^2},\quad T_0 = P - \rho gx = \frac{1}{2}\rho v^2$"
    )
    ax_calc.text(0.35, 4.30, sol_text, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # Bottom Card: Real-Time Monitor
    live_text = (
        f"[Real-Time Monitor: $L={L:.1f}\\ \\mathrm{{m}},\\ \\rho={rho:.1f}\\ \\mathrm{{kg/m}},\\ v={v:.1f}\\ \\mathrm{{m/s}}$]\n"
        f"• Pulling Force: $P(x) = {P_curr:.1f}\\ \\mathrm{{N}}$ ($-\\frac{{1}}{{2}}\\rho v^2 = -{T0:.1f}\\ \\mathrm{{N}}$ less than Open-Link Chain)\n"
        f"• Platform Reaction: $R(x) = {R_curr:.1f}\\ \\mathrm{{N}}$ (Resting Weight ${W_rem:.1f}\\ \\mathrm{{N}} + $ Guide Force ${T0:.1f}\\ \\mathrm{{N}}$)\n"
        f"• Energy Conservation: $U_{{1-2}} = {U_P:.1f}\\ \\mathrm{{J}} = \\Delta T({dT:.1f}\\ \\mathrm{{J}}) + \\Delta V_g({dVg:.1f}\\ \\mathrm{{J}})$ (Loss $0\\ \\mathrm{{J}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Work-Energy Analysis & Validation', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_11_inextensible_rope_lift.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
