"""
Dynamics 9th Ed. Chapter 4: Kinetics of Systems of Particles
Sample Problem 4/3 - Three Spheres with Bars Freely Hinged at O
- Pure white background (#ffffff) & faithful textbook geometry
- Theoretical verification completed:
  * Mass center acceleration: a_bar = (F / 3m) i (Identical to Sample Problem 4/2!)
  * However, as angles between bars change, hinge O ceases to be the mass center (a_O != a_bar),
    and the angular accelerations of the individual bars differ.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Normalized parameters (m = 1, r = 1, b = 0.6, F = 3)
m = 1.0
r = 1.0
b = 0.6
F = 3.0

a_G_x = F / (3.0 * m)                   # Mass center accel = 1.00 m/s^2
a_1_x = F / m                           # Top sphere accel = 3.00 m/s^2
a_O_x = F * (r - b) / (m * r)           # Hinge O initial accel = 1.20 m/s^2 (!= a_G_x)
alpha_1_cw = (F * b) / (m * r**2)       # Top bar angular accel = 1.80 rad/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.55, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

p2_fixed = np.array([r * np.cos(np.radians(210.0)), r * np.sin(np.radians(210.0))])
p3_fixed = np.array([r * np.cos(np.radians(330.0)), r * np.sin(np.radians(330.0))])
p1_init = np.array([0.0, r])

def update(frame):
    t = t_vals[frame]
    
    dx_1 = 0.5 * a_1_x * t**2
    dx_G = 0.5 * a_G_x * t**2
    dx_O = 0.5 * a_O_x * t**2
    
    p1 = np.array([dx_1, np.sqrt(max(0.1, r**2 - (dx_1 - dx_O)**2))])
    pO = np.array([dx_O, 0.0])
    pG = (p1 + p2_fixed + p3_fixed) / 3.0
    
    theta1_deg = np.degrees(np.arctan2(p1[0] - pO[0], p1[1] - pO[1]))
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-1.15, 1.45)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    ax_main.plot([-1.2, 1.6], [0, 0], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.plot([0, 0], [-0.95, 1.3], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.text(1.65, 0.0, r'$x$', fontsize=12, fontweight='bold', va='center')
    ax_main.text(0.0, 1.34, r'$y$', fontsize=12, fontweight='bold', ha='center')
    
    if frame > 0:
        for p_init in [p1_init, p2_fixed, p3_fixed]:
            ax_main.plot([0, p_init[0]], [0, p_init[1]], color='#e0e0e0', lw=2.8, ls='--', zorder=1)
        c1_0 = patches.Circle(p1_init, 0.12, facecolor='none', edgecolor='#cccccc', ls='--', lw=1.2, zorder=1)
        ax_main.add_patch(c1_0)
        
    for p_sph, lbl_off in [(p1, [-0.14, 0.0]), (p2_fixed, [-0.1, 0.12]), (p3_fixed, [0.1, 0.12])]:
        ax_main.plot([pO[0], p_sph[0]], [pO[1], p_sph[1]], color='#4a5568', lw=4.0, solid_capstyle='round', zorder=4)
        mid_pt = 0.5 * (pO + p_sph) + np.array(lbl_off)
        ax_main.text(mid_pt[0], mid_pt[1], r'$r$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
        
    hinge_outer = patches.Circle(pO, 0.085, facecolor='#ffffff', edgecolor='#2d3748', lw=2.0, zorder=6)
    hinge_pin = patches.Circle(pO, 0.032, facecolor='#2d3748', edgecolor='none', zorder=7)
    ax_main.add_patch(hinge_outer)
    ax_main.add_patch(hinge_pin)
    ax_main.text(pO[0] + 0.02, pO[1] - 0.15, r'$O$', fontsize=11.5, fontweight='bold', color='#2d3748', ha='center', va='top')
    ax_main.annotate('Freely Hinged', xy=(pO[0]-0.06, pO[1]+0.05), xytext=(pO[0]-0.62, pO[1]+0.24),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.1),
                     fontsize=9.5, fontweight='bold', color='#2d3748', ha='center')
    
    ax_main.plot(pG[0], pG[1], marker='D', markersize=7.5, markerfacecolor='#ffeb3b', markeredgecolor='#d32f2f', markeredgewidth=1.8, zorder=8)
    ax_main.text(pG[0] + 0.08, pG[1] + 0.14, r'$G\ (\bar{\mathbf{a}} = \frac{F}{3m}\mathbf{i})$',
                 fontsize=10, fontweight='bold', color='#c62828', ha='left', va='bottom', zorder=9)
    
    for p_sph, off in [(p1, [0.0, 0.23]), (p2_fixed, [-0.22, -0.14]), (p3_fixed, [0.22, -0.14])]:
        sph = patches.Circle(p_sph, 0.135, facecolor='#7ab8e6', edgecolor='#1d4564', lw=1.8, zorder=7)
        ax_main.add_patch(sph)
        hl = patches.Circle(p_sph + np.array([-0.04, 0.04]), 0.04, facecolor='#d6ecfa', edgecolor='none', zorder=8)
        ax_main.add_patch(hl)
        ax_main.text(p_sph[0] + off[0], p_sph[1] + off[1], r'$m$', fontsize=11.5, fontweight='bold', color='#1d4564', ha='center', va='center')
        
    u_bar1 = (p1 - pO) / np.linalg.norm(p1 - pO)
    p_force = pO + b * u_bar1
    f_start = p_force - np.array([0.52, 0.0])
    ax_main.annotate('', xy=p_force, xytext=f_start,
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(f_start[0] - 0.08, f_start[1], r'$\mathbf{F}$', color='#d32f2f', fontsize=12.5, fontweight='bold', ha='right', va='center')
    
    b_mid = pO + 0.5 * b * u_bar1 + np.array([0.12, -0.02])
    ax_main.text(b_mid[0], b_mid[1], r'$b$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
    
    if frame > 2:
        v1_curr = a_1_x * t
        ax_main.annotate('', xy=(p1[0] + 0.25*v1_curr, p1[1]), xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=9)
        ax_main.text(p1[0] + 0.25*v1_curr + 0.06, p1[1], r'$\mathbf{v}_1$', color='#2e7d32', fontsize=10.5, fontweight='bold', va='center')
        
    ax_main.set_title('Sample Problem 4/3: Spheres with Bars Freely Hinged at O', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. Theoretical Derivation & Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Comparison with Sample Problem 4/2:\n"
        "1) Mass Center G Acceleration (Generalized Newton's 2nd Law, Eq. 4.1):\n"
        r"  $\bullet$ Eq. (4.1) $\sum\mathbf{F} = m\bar{\mathbf{a}}$ holds for ANY system (rigid or nonrigid)!" "\n"
        r"  $\Rightarrow\ \mathbf{\bar{\mathbf{a}} = \frac{F}{3m}\mathbf{i}}$ (Identical to Sample Problem 4/2)" "\n\n"
        r"2) Motion of Hinge Point O ($\mathbf{a}_O \neq \bar{\mathbf{a}}$):" "\n"
        r"  $\bullet$ Although $G$ coincides with $O$ at this instant, $O$ does not" "\n"
        r"     remain the mass center as the angles change ($\mathbf{a}_O \neq \bar{\mathbf{a}}$)" "\n\n"
        "3) Angular Momentum Rate & Individual Bar Motions:\n"
        r"  $\bullet$ While $\sum M_G = \dot{H}_G = F b$ is the same at this instant," "\n"
        r"     the angular motions $\ddot{\theta}_i$ of the hinged bars are different!" "\n"
        r"  $\bullet$ Member dismemberment: $\ddot{\theta}_1 = \frac{Fb}{mr^2},\ \ddot{\theta}_2 = \ddot{\theta}_3 = 0,\ \mathbf{a}_O = \frac{F(r-b)}{mr}\mathbf{i}$"
    )
    ax_calc.text(0.35, 5.95, sol_box, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"Live Nonrigid Hinged Motion Monitor ($t = {t:.2f}\\ \\mathrm{{s}}$):\n"
        f"Mass Center G: $x_G = {pG[0]:.3f}\\ \\mathrm{{m}}$  ($\\bar{{a}}_x = F/3m = {a_G_x:.2f}\\ \\mathrm{{m/s^2}}$)\n"
        f"Hinge Pin O: $x_O = {pO[0]:.3f}\\ \\mathrm{{m}}$  ($a_{{Ox}} = {a_O_x:.2f}\\ \\mathrm{{m/s^2}} \\neq \\bar{{a}}_x$)\n"
        f"Top Bar Rotation: $\\Delta\\theta_1 = {theta1_deg:.1f}^\\circ$ (Lower two bars remain at rest)"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Rigid (Welded) vs Nonrigid (Hinged) Comparison', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_3_hinged_bars_spheres.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
