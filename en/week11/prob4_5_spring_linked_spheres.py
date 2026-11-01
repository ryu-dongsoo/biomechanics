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
Dynamics 9th Ed. Chapter 4: Kinetics of Systems of Particles
Problem 4/5 - Two Smooth Spheres Linked by a Spring in a Horizontal Guide with Hinged Bars
- Pure white background (#ffffff) & faithful textbook geometry
- Theoretical verification completed:
  * Spring center C is the mass center G of the two 2-kg spheres
  * Sigma F_x = m_tot * a_C => 50 N = 2(2 kg) * a_C => a_C = 12.5 m/s^2 (->)
  * Dimension b influences normal forces R_1, R_2 but has no influence on Sigma F_x or a_C
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m_sphere = 2.0      # Mass of each sphere (kg)
m_tot = 4.0         # Total system mass (kg)
F_ext = 50.0        # Horizontal external force (N)
L_bar = 0.30        # Bar length 300 mm = 0.30 m
a_C = F_ext / m_tot # 12.5 m/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.16, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_coil_spring(ax, x_left, x_right, y_c, n_coils=10, amp=0.032):
    L = x_right - x_left
    pad = 0.045
    xs = [x_left, x_left + pad]
    ys = [y_c, y_c]
    coil_len = L - 2 * pad
    for i in range(2 * n_coils):
        frac = (i + 0.5) / (2 * n_coils)
        xs.append(x_left + pad + frac * coil_len)
        ys.append(y_c + (amp if i % 2 == 0 else -amp))
    xs.extend([x_right - pad, x_right])
    ys.extend([y_c, y_c])
    ax.plot(xs, ys, color='#2b2b2b', lw=2.0, zorder=5)

def update(frame):
    t = t_vals[frame]
    x_C = 0.5 * a_C * t**2
    v_C = a_C * t
    
    delta_half = 0.018 * np.sin(18.0 * t)
    d_half = 0.15 + delta_half
    
    x1 = x_C - d_half
    x2 = x_C + d_half
    y_guide = 0.32
    r_sph = 0.072
    
    h_drop = np.sqrt(max(0.02, L_bar**2 - d_half**2))
    x_bot = x_C
    y_bot = y_guide - h_drop
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.34, 0.56)
    ax_main.set_ylim(-0.14, 0.50)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    y_top_wall = y_guide + r_sph + 0.003
    y_bot_wall = y_guide - r_sph - 0.003
    ax_main.fill_between([-0.30, 0.52], y_top_wall, y_top_wall + 0.045, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.fill_between([-0.30, 0.52], y_bot_wall - 0.045, y_bot_wall, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.plot([-0.30, 0.52], [y_top_wall, y_top_wall], color='#333333', lw=2.2, zorder=2)
    ax_main.plot([-0.30, 0.52], [y_bot_wall, y_bot_wall], color='#333333', lw=2.2, zorder=2)
    
    for x_s, lbl_x in [(x1, x1 - 0.115), (x2, x2 + 0.115)]:
        sph = patches.Circle((x_s, y_guide), r_sph, facecolor='#d48872', edgecolor='#59281a', lw=1.8, zorder=4)
        ax_main.add_patch(sph)
        hl = patches.Circle((x_s - 0.022, y_guide + 0.022), 0.022, facecolor='#f2cbbd', edgecolor='none', zorder=5)
        ax_main.add_patch(hl)
        ax_main.text(lbl_x, y_guide, '2 kg', fontsize=11.5, fontweight='bold', color='#222222', ha='center', va='center')
        
    draw_coil_spring(ax_main, x1, x2, y_guide, n_coils=9, amp=0.024)
    ax_main.plot(x_C, y_guide, 'ko', markersize=5.5, zorder=8)
    ax_main.text(x_C, y_guide - 0.048, r'$C\ (G)$', fontsize=11.5, fontweight='bold', color='#1565c0', ha='center', va='top', zorder=8)
    
    ax_main.annotate('', xy=(x_C + 0.09, y_guide + 0.048), xytext=(x_C, y_guide + 0.048),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=9)
    ax_main.text(x_C + 0.045, y_guide + 0.088, f'$a_C = 12.5\\ \\mathrm{{m/s^2}}$',
                 fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')
    
    for x_s in [x1, x2]:
        ax_main.plot([x_s, x_bot], [y_guide, y_bot], color='#3a5a78', lw=6.5, solid_capstyle='round', zorder=6)
        ax_main.plot([x_s, x_bot], [y_guide, y_bot], color='#a7c7e7', lw=3.8, solid_capstyle='round', zorder=6)
        p_pin = patches.Circle((x_s, y_guide), 0.015, facecolor='#ffffff', edgecolor='#222222', lw=1.5, zorder=7)
        ax_main.add_patch(p_pin)
        p_dot = patches.Circle((x_s, y_guide), 0.005, facecolor='#222222', edgecolor='none', zorder=8)
        ax_main.add_patch(p_dot)
        
    b_pin = patches.Circle((x_bot, y_bot), 0.016, facecolor='#ffffff', edgecolor='#222222', lw=1.5, zorder=7)
    ax_main.add_patch(b_pin)
    b_dot = patches.Circle((x_bot, y_bot), 0.006, facecolor='#222222', edgecolor='none', zorder=8)
    ax_main.add_patch(b_dot)
    
    ax_main.text(0.5*(x1 + x_bot) - 0.085, 0.5*(y_guide + y_bot) - 0.01, '300 mm', fontsize=10.5, fontweight='bold', ha='center')
    ax_main.text(0.5*(x2 + x_bot) - 0.055, 0.5*(y_guide + y_bot) + 0.01, '300 mm', fontsize=10.5, fontweight='bold', ha='center')
    
    frac_b = 0.36
    px_F = x_bot + frac_b * (x2 - x_bot)
    py_F = y_bot + frac_b * (y_guide - y_bot)
    ax_main.annotate('', xy=(px_F + 0.13, py_F), xytext=(px_F + 0.008, py_F),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(px_F + 0.14, py_F, '50 N', color='#d32f2f', fontsize=12, fontweight='bold', va='center')
    ax_main.text(0.5*(x_bot + px_F) + 0.032, 0.5*(y_bot + py_F) - 0.018, r'$b$', fontsize=11.5, fontweight='bold', color='#222222')
    
    ax_main.set_title('Problem 4/5: Spring-Linked Spheres & Hinged Bars', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. Theoretical Derivation & Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Analysis (System Boundary):\n"
        "1) Mass Center Identification:\n"
        r"  $\bullet$ Since both spheres have equal mass ($2\ \mathrm{kg}$) and the spring/bars" "\n"
        r"     have negligible mass, spring midpoint $C$ is the mass center $G$!" "\n\n"
        "2) Generalized Newton's 2nd Law (Eq. 4.1, Horizontal x-axis):\n"
        r"  $\bullet$ Internal forces (spring force, pin forces) cancel out ($\sum f_x = 0$)" "\n"
        r"  $\bullet\ [\sum F_x = m\bar{a}_x] \quad 50\ \mathrm{N} = 2(2\ \mathrm{kg})\, a_C$" "\n"
        r"  $\Rightarrow\ \mathbf{a_C = 12.5\ \mathrm{m/s^2}}\ (\rightarrow)$" "\n\n"
        r"3) Why Dimension b Has No Influence on $a_C$:" "\n"
        r"  $\bullet$ Dimension $b$ affects the vertical guide normal forces $R_1$ and $R_2$" "\n"
        r"     via moment equilibrium, but has no influence on $\sum F_x$ and $a_C$!"
    )
    ax_calc.text(0.35, 6.0, sol_box, fontsize=9.3, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"Live Mass Center C Monitor ($t = {t:.3f}\\ \\mathrm{{s}}$):\n"
        f"Net Horizontal Force: $\\sum F_x = 50.0\\ \\mathrm{{N}}$,  Total Mass: $m = 4.0\\ \\mathrm{{kg}}$\n"
        f"Center C Acceleration: $a_C = 12.50\\ \\mathrm{{m/s^2}}$,  Speed: $v_C = {v_C:.2f}\\ \\mathrm{{m/s}}$\n"
        f"Center C Displacement: $x_C = {x_C*1000:.1f}\\ \\mathrm{{mm}}$"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('System FBD & Acceleration Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_5_spring_linked_spheres.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
