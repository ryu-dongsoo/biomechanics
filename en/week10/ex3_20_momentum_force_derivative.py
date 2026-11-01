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
Sample Problem 3.20: Force Calculation from Time-Varying Linear Momentum
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Particle mass m = 0.200 kg
- Motion plane: y-z vertical plane (y: horizontal, z: vertical upward)
- Linear momentum function: G(t) = 1.5(t^2 + 3) j - (2/3)(t^3 - 4) k [N s]
- Gravitational acceleration g = 9.81 m/s^2, weight W = -0.2(9.81) k = -1.962 k [N]
- Target evaluation time: t = 2 s

Analytical Result:
- Force vector: F = 6 j - 6.04 k N
- Force magnitude: F = 8.51 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Physical parameters
m = 0.200          # kg
g = 9.81           # m/s^2
W_z = -m * g       # -1.962 N

def get_kinetics(t):
    G_y = 1.5 * (t**2 + 3.0)
    G_z = -(2.0 / 3.0) * (t**3 - 4.0)

    Gdot_y = 3.0 * t
    Gdot_z = -2.0 * (t**2)

    F_y = Gdot_y
    F_z = Gdot_z - W_z
    F_mag = np.hypot(F_y, F_z)

    v_y = G_y / m
    v_z = G_z / m

    return G_y, G_z, Gdot_y, Gdot_z, F_y, F_z, F_mag, v_y, v_z

n_frames = 60
t_arr = np.linspace(0.0, 3.0, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def update(frame):
    t = t_arr[frame]
    G_y, G_z, Gdot_y, Gdot_z, F_y, F_z, F_mag, v_y, v_z = get_kinetics(t)

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [Left Panel] Textbook Schematic & Kinematics
    # ==========================================
    ax1.set_xlim(-0.2, 1.4)
    ax1.set_ylim(-0.3, 1.3)
    ax1.set_aspect('equal')
    ax1.set_title("Sample Problem 3.20: Particle in y-z Plane", fontsize=13, fontweight='bold', pad=12)

    ax1.annotate('', xy=(1.2, 0.0), xytext=(0.0, 0.0),
                 arrowprops=dict(arrowstyle="->", color='#212529', lw=1.8))
    ax1.annotate('', xy=(0.0, 1.15), xytext=(0.0, 0.0),
                 arrowprops=dict(arrowstyle="->", color='#212529', lw=1.8))
    ax1.text(1.25, -0.02, "y", fontsize=12, fontweight='bold', color='#212529')
    ax1.text(-0.02, 1.20, "z", fontsize=12, fontweight='bold', color='#212529')

    ax1.annotate('', xy=(-0.10, 0.65), xytext=(-0.10, 0.35),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.text(-0.16, 0.48, "Up", fontsize=10, fontweight='bold', color='#495057', va='center')

    py = 0.25 + (t / 3.0) * 0.70
    pz = 0.85 - (t / 3.0)**1.8 * 0.65

    t_trace = np.linspace(0.0, 3.0, 50)
    py_trace = 0.25 + (t_trace / 3.0) * 0.70
    pz_trace = 0.85 - (t_trace / 3.0)**1.8 * 0.65
    ax1.plot(py_trace, pz_trace, 'k--', lw=1.2, alpha=0.4, label='Trajectory')

    particle = patches.Circle((py, pz), 0.045, facecolor='#74c0fc', edgecolor='#1864ab', lw=2, zorder=5)
    ax1.add_patch(particle)
    ax1.text(py, pz, "m", fontsize=9, fontweight='bold', ha='center', va='center', color='#1864ab')

    w_len = 0.25
    ax1.annotate('', xy=(py, pz - w_len), xytext=(py, pz),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(py, pz - w_len - 0.08, "-0.2(9.81)k N\n(-1.962k N)",
             color='#e03131', fontsize=9, fontweight='bold', ha='center')

    f_scale = 0.035
    f_end_y = py + F_y * f_scale
    f_end_z = pz + F_z * f_scale
    ax1.annotate('', xy=(f_end_y, f_end_z), xytext=(py, pz),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=3.5, mutation_scale=18))
    ax1.text(f_end_y + 0.04, f_end_z + 0.02, f"F = {F_mag:.2f} N\n({F_y:+.1f}j {F_z:+.2f}k)",
             color='#c92a2a', fontsize=9.5, fontweight='bold')

    if abs(t - 2.0) <= 0.08:
        ax1.add_patch(patches.Circle((py, pz), 0.07, facecolor='none', edgecolor='#f59f00', lw=2.5, linestyle=':', zorder=6))
        highlight_text = "Target Time t = 2.0 s (Textbook Solution)"
        highlight_color = '#d9480f'
    else:
        highlight_text = f"Time: t = {t:.2f} s"
        highlight_color = '#212529'

    ax1.text(0.60, 1.15, highlight_text, fontsize=11, fontweight='bold',
             color=highlight_color, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=highlight_color, lw=1.2))

    # ==========================================
    # [Right Panel] Momentum Derivative & Solution
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("Force-Momentum Rate Relation & Textbook Verification", fontsize=12.5, fontweight='bold', pad=10)

    rect_box = patches.Rectangle((-0.12, 0.48), 1.32, 0.52, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ Real-Time Kinetics Monitor ]", fontsize=11, fontweight='bold', color='#212529')

    ax2.text(-0.08, 0.83, f"Time: t = {t:.2f} s", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.74, f"Linear Momentum G(t) = {G_y:.2f}j {G_z:+.2f}k N s", fontsize=9.5, color='#343a40', fontfamily='monospace')
    ax2.text(-0.08, 0.65, f"Rate of Momentum dG/dt = {Gdot_y:.2f}j {Gdot_z:+.2f}k N", fontsize=9.5, color='#343a40', fontfamily='monospace')
    ax2.text(-0.08, 0.56, f"Applied Force F(t) = dG/dt - W = {F_y:.2f}j {F_z:+.2f}k N  (|F| = {F_mag:.2f} N)",
             fontsize=9.5, fontweight='bold', color='#c92a2a', fontfamily='monospace')

    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.52, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.35, "Governing Equations (Newton's 2nd Law in Momentum Form):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.28, "   Sigma F = dG/dt  ==>  F + W = dG/dt", fontsize=9.5, color='#212529', fontfamily='monospace')

    ax2.text(-0.08, 0.19, "Vector Differentiation:", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.12, "   dG/dt = d/dt [ 1.5(t^2+3)j - (2/3)(t^3-4)k ] = 3t j - 2t^2 k", fontsize=9.0, color='#212529', fontfamily='monospace')
    ax2.text(-0.08, 0.05, "   F = dG/dt - W = 3t j - 2t^2 k - (-1.962 k) = 3t j + (1.962 - 2t^2) k", fontsize=9.0, color='#212529', fontfamily='monospace')

    ax2.text(-0.08, -0.04, "Evaluation at t = 2 s (100% Textbook Parity):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.09, "   F = 6 j - 6.04 k N,    |F| = sqrt(6^2 + 6.038^2) = 8.51 N",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_20_momentum_force_derivative.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[Done] {out_path} successfully generated!")
