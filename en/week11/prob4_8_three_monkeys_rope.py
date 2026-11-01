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
Problem 4/8 - Three Monkeys Climbing Up and Down a Vertical Rope Suspended at D
- Pure white background (#ffffff) & faithful textbook geometry
- Theoretical verification completed:
  * W_A = 10(9.81) = 98.1 N,  W_B = 15(9.81) = 147.2 N,  W_C = 8(9.81) = 78.5 N
  * a_A = -2.0 m/s^2 (down),  a_B = 0 (constant speed 0.8 m/s up),  a_C = +1.5 m/s^2 (up)
  * Sigma F_y = Sigma m_i a_i => T - (98.1 + 147.2 + 78.5) = 10(-2) + 15(0) + 8(1.5)
  * T - 323.7 = -8 => T = 315.7 N ≈ 316 N
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
g = 9.81
mA, mB, mC = 10.0, 15.0, 8.0
WA, WB, WC = mA * g, mB * g, mC * g    # 98.1, 147.15, 78.48 N
W_tot = WA + WB + WC                    # 323.73 N

aA = -2.0   # Downward 2 m/s^2
aB = 0.0    # Constant speed 0.8 m/s upward
aC = +1.5   # Upward 1.5 m/s^2
vB_0 = 0.8

ma_sum = mA * aA + mB * aB + mC * aC    # -20 + 0 + 12 = -8.0 N
T_val = W_tot + ma_sum                  # 315.73 N -> 316 N

# Initial vertical positions (m)
yA_0, yB_0, yC_0 = 4.3, 2.7, 1.1
yG_0 = (mA*yA_0 + mB*yB_0 + mC*yC_0) / (mA + mB + mC)
aG = ma_sum / (mA + mB + mC)

n_frames = 48
t_vals = np.linspace(0.0, 0.55, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_monkey_body(ax, x_rope, y_c, label_name, mass_str, acc_str, arrow_dir, arrow_color):
    body = patches.Ellipse((x_rope + 0.14, y_c), 0.24, 0.44, angle=-8,
                           facecolor='#b8865c', edgecolor='#4d3319', lw=1.6, zorder=5)
    head = patches.Circle((x_rope + 0.12, y_c + 0.26), 0.10,
                          facecolor='#c69468', edgecolor='#4d3319', lw=1.6, zorder=6)
    ax.add_patch(body)
    ax.add_patch(head)
    ax.plot([x_rope + 0.08, x_rope], [y_c + 0.15, y_c + 0.28], color='#4d3319', lw=3.2, solid_capstyle='round', zorder=6)
    ax.plot([x_rope + 0.10, x_rope], [y_c - 0.14, y_c - 0.24], color='#4d3319', lw=3.2, solid_capstyle='round', zorder=6)
    tail_x = np.linspace(x_rope + 0.22, x_rope + 0.42, 12)
    tail_y = y_c - 0.16 - 0.15 * np.sin(np.linspace(0, np.pi, 12))
    ax.plot(tail_x, tail_y, color='#7a5230', lw=2.2, zorder=4)
    
    ax.text(x_rope + 0.52, y_c + 0.08, f'${label_name}$ ({mass_str})', fontsize=11.5, fontweight='bold', color='#222222', va='center')
    ax.text(x_rope + 0.52, y_c - 0.14, acc_str, fontsize=10, fontweight='bold', color=arrow_color, va='center')
    
    y_arr_start = y_c - 0.22 * arrow_dir
    y_arr_end = y_c + 0.22 * arrow_dir
    ax.annotate('', xy=(x_rope - 0.28, y_arr_end), xytext=(x_rope - 0.28, y_arr_start),
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=2.3, mutation_scale=14), zorder=7)

def update(frame):
    t = t_vals[frame]
    
    yA = yA_0 - 0.25 * t + 0.5 * aA * t**2
    yB = yB_0 + vB_0 * t
    yC = yC_0 + 0.20 * t + 0.5 * aC * t**2
    yG = (mA*yA + mB*yB + mC*yC) / (mA + mB + mC)
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.2, 2.6)
    ax_main.set_ylim(-0.2, 5.7)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    x_r = -0.35
    y_top = 5.25
    
    ax_main.fill_between([x_r - 0.65, x_r + 0.65], y_top, y_top + 0.25, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.plot([x_r - 0.65, x_r + 0.65], [y_top, y_top], color='#222222', lw=2.5, zorder=3)
    for hx in np.linspace(x_r - 0.55, x_r + 0.45, 7):
        ax_main.plot([hx, hx + 0.14], [y_top, y_top + 0.22], color='#555555', lw=1.1, zorder=2)
    ax_main.plot(x_r, y_top, 'ko', markersize=5, zorder=5)
    ax_main.text(x_r - 0.22, y_top - 0.24, r'$D$', fontsize=13, fontweight='bold', color='#222222')
    
    ax_main.plot([x_r - 0.025, x_r - 0.025], [0.15, y_top], color='#555555', lw=1.6, zorder=2)
    ax_main.plot([x_r + 0.025, x_r + 0.025], [0.15, y_top], color='#555555', lw=1.6, zorder=2)
    
    ax_main.annotate('', xy=(x_r, y_top + 0.02), xytext=(x_r, y_top - 0.62),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=15), zorder=8)
    ax_main.text(x_r - 0.72, y_top - 0.42, r'$T = 316\ \mathrm{N}$', color='#d32f2f', fontsize=11.5, fontweight='bold', ha='center')
    
    draw_monkey_body(ax_main, x_r, yA, 'A', '10 kg', r'$a_A = 2\ \mathrm{m/s^2}\ (\downarrow)$', -1, '#d32f2f')
    draw_monkey_body(ax_main, x_r, yB, 'B', '15 kg', r'$v_B = 0.8\ \mathrm{m/s}\ (\uparrow,\ a_B=0)$', +1, '#2e7d32')
    draw_monkey_body(ax_main, x_r, yC, 'C', '8 kg', r'$a_C = 1.5\ \mathrm{m/s^2}\ (\uparrow)$', +1, '#1565c0')
    
    ax_main.plot(x_r, yG, marker='D', markersize=7.5, markerfacecolor='#ffeb3b', markeredgecolor='#1565c0', markeredgewidth=1.8, zorder=9)
    ax_main.text(x_r - 0.88, yG, r'$G\ (\mathrm{Mass\ Center})$', fontsize=10, fontweight='bold', color='#1565c0', va='center', ha='center')
    
    ax_main.set_title('Problem 4/8: Three Monkeys Climbing on a Vertical Rope', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. Theoretical Derivation & Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Analysis (Rope + 3 Monkeys System):\n"
        "1) Weights of the Three Monkeys (External Forces):\n"
        r"  $\bullet\ W_A = 10(9.81) = 98.1\ \mathrm{N}$" "\n"
        r"  $\bullet\ W_B = 15(9.81) = 147.2\ \mathrm{N}$" "\n"
        r"  $\bullet\ W_C = 8(9.81) = 78.5\ \mathrm{N} \quad \Rightarrow \sum W = 323.7\ \mathrm{N}\ (\downarrow)$" "\n\n"
        "2) Individual Accelerations (+y: vertically upward):\n"
        r"  $\bullet\ a_A = -2.0\ \mathrm{m/s^2},\quad a_B = 0\ (\text{const } 0.8\ \mathrm{m/s}),\quad a_C = +1.5\ \mathrm{m/s^2}$" "\n\n"
        "3) Generalized Newton's 2nd Law ($\sum F_y = \sum m_i a_i$):\n"
        r"  $\bullet\ T - (98.1 + 147.2 + 78.5) = 10(-2) + 15(0) + 8(1.5)$" "\n"
        r"  $\bullet\ T - 323.7 = -20 + 0 + 12 = -8.0\ \mathrm{N}$" "\n"
        r"  $\Rightarrow\ \mathbf{T = 315.7\ \mathrm{N} \approx 316\ \mathrm{N}}$"
    )
    ax_calc.text(0.35, 5.95, sol_box, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"Live Dynamic Equilibrium Monitor ($t = {t:.2f}\\ \\mathrm{{s}}$):\n"
        f"Total Weight: $\\sum W_i = 323.7\\ \\mathrm{{N}}\\ (\\downarrow)$,  Inertia Sum: $\\sum m_i a_i = -8.0\\ \\mathrm{{N}}$\n"
        f"Mass Center Accel: $\\bar{{a}}_y = \\frac{{-8.0}}{{33\\ \\mathrm{{kg}}}} = {aG:.3f}\\ \\mathrm{{m/s^2}}\\ (\\downarrow)$\n"
        f"Rope Tension at Support D: $T = 323.7 - 8.0 = \\mathbf{{316\\ \\mathrm{{N}}}}$"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('System Equation of Motion & Tension Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_8_three_monkeys_rope.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
