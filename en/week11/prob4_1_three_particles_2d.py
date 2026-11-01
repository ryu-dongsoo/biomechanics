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
Problem 4/1 - 2D Three-Particle System: Mass Center, Kinetic Energy, and Angular Momentum
- Pure white background (#ffffff) & faithful textbook geometry
- Theoretical verification completed:
  * r_bar = (d / 6)(8 i + 5 j)
  * r_dot_bar = (v / 6)(4 i + 3 j),  r_ddot_bar = (F i) / (6 m)
  * T = (11 / 2) m v^2 = 5.5 m v^2
  * H_O = 2 m v d k,  H_O_dot = -F d k
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Normalized parameters (m = 1, d = 1, v = 1, F = 1)
m = 1.0
d = 1.0
v = 1.0
F = 1.0
M_tot = 6.0 * m

# Initial positions (t = 0)
r1_0 = np.array([0.0, 1.0*d])         # Mass 2m
r2_0 = np.array([2.0*d, 1.0*d])       # Mass 3m
r3_0 = np.array([2.0*d, 0.0])         # Mass m (at rest)

# Initial velocities
v1_0 = np.array([2.0*v, 0.0])
v2_0 = np.array([0.0, 1.0*v])
v3_0 = np.array([0.0, 0.0])

# External force and accelerations
F2 = np.array([1.0*F, 0.0])
a1 = np.array([0.0, 0.0])
a2 = F2 / (3.0*m)
a3 = np.array([0.0, 0.0])

r_bar_0 = (2*m*r1_0 + 3*m*r2_0 + 1*m*r3_0) / M_tot  # (8/6, 5/6) d
v_bar_0 = (2*m*v1_0 + 3*m*v2_0 + 1*m*v3_0) / M_tot  # (4/6, 3/6) v
a_bar = F2 / M_tot                                  # (1/6, 0) F/m

n_frames = 48
t_vals = np.linspace(0.0, 0.45, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_particle(ax, pt, radius, lbl_top, lbl_bot=''):
    c = patches.Circle(pt, radius, facecolor='#cc6666', edgecolor='#4a1c1c', lw=1.8, zorder=6)
    ax.add_patch(c)
    hl = patches.Circle(pt + np.array([-0.28*radius, 0.28*radius]), 0.28*radius, facecolor='#f0b8b8', edgecolor='none', zorder=7)
    ax.add_patch(hl)
    ax.text(pt[0] - 0.16, pt[1] + radius + 0.11, lbl_top, fontsize=11.5, fontweight='bold', color='#222222', ha='center')
    if lbl_bot:
        ax.text(pt[0], pt[1] - radius - 0.18, lbl_bot, fontsize=10, fontweight='bold', color='#444444', ha='center')

def update(frame):
    t = t_vals[frame]
    
    r1 = r1_0 + v1_0 * t
    r2 = r2_0 + v2_0 * t + 0.5 * a2 * t**2
    r3 = r3_0.copy()
    
    v1 = v1_0.copy()
    v2 = v2_0 + a2 * t
    v3 = v3_0.copy()
    
    r_bar = r_bar_0 + v_bar_0 * t + 0.5 * a_bar * t**2
    v_bar = v_bar_0 + a_bar * t
    T_curr = 0.5 * (2*m*np.dot(v1,v1) + 3*m*np.dot(v2,v2))
    HO_z = (r1[0]*2*m*v1[1] - r1[1]*2*m*v1[0]) + (r2[0]*3*m*v2[1] - r2[1]*3*m*v2[0])
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.55, 3.25)
    ax_main.set_ylim(-0.45, 2.05)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    ax_main.plot([0, 2.95], [0, 0], color='#555555', ls='--', lw=1.4, zorder=1)
    ax_main.plot([0, 0], [0, 1.85], color='#555555', ls='--', lw=1.4, zorder=1)
    ax_main.text(3.03, 0.0, r'$x$', fontsize=13, fontweight='bold', va='center')
    ax_main.text(0.0, 1.92, r'$y$', fontsize=13, fontweight='bold', ha='center')
    ax_main.text(-0.12, -0.12, r'$O$', fontsize=13, fontweight='bold', ha='center', va='center')
    
    ax_main.plot([0, 2*d], [d, d], color='#777777', lw=1.1, zorder=1)
    ax_main.plot([2*d, 2*d], [0, d], color='#777777', lw=1.1, zorder=1)
    ax_main.text(-0.14, 0.5*d, r'$d$', fontsize=12, fontweight='bold', ha='center', va='center')
    ax_main.text(1.0*d, -0.15, r'$2d$', fontsize=12, fontweight='bold', ha='center', va='center')
    
    draw_particle(ax_main, r1, 0.11, r'$2m$')
    draw_particle(ax_main, r2, 0.135, r'$3m$')
    draw_particle(ax_main, r3, 0.085, r'$m$', '(at rest)')
    
    ax_main.annotate('', xy=(r1[0] + 0.55, r1[1]), xytext=(r1[0] + 0.12, r1[1]),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=8)
    ax_main.text(r1[0] + 0.36, r1[1] + 0.13, r'$2v$', color='#2e7d32', fontsize=11.5, fontweight='bold', ha='center')
    
    ax_main.annotate('', xy=(r2[0], r2[1] + 0.52), xytext=(r2[0], r2[1] + 0.15),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=8)
    ax_main.text(r2[0] + 0.14, r2[1] + 0.45, r'$v$', color='#2e7d32', fontsize=11.5, fontweight='bold', va='center')
    
    ax_main.annotate('', xy=(r2[0] + 0.62, r2[1]), xytext=(r2[0] + 0.15, r2[1]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=8)
    ax_main.text(r2[0] + 0.68, r2[1], r'$\mathbf{F}$', color='#d32f2f', fontsize=12.5, fontweight='bold', va='center')
    
    ax_main.plot([r_bar_0[0], r_bar[0]], [r_bar_0[1], r_bar[1]], color='#1565c0', ls=':', lw=1.8, zorder=4)
    ax_main.plot(r_bar[0], r_bar[1], marker='D', markersize=7.5, markerfacecolor='#ffeb3b', markeredgecolor='#1565c0', markeredgewidth=1.8, zorder=9)
    ax_main.text(r_bar[0] - 0.08, r_bar[1] - 0.18, r'$G\ (\frac{8}{6}d,\ \frac{5}{6}d)$',
                 fontsize=10.5, fontweight='bold', color='#1565c0', ha='center')
    ax_main.annotate('', xy=(r_bar[0] + 0.35*v_bar[0], r_bar[1] + 0.35*v_bar[1]), xytext=r_bar,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.0, mutation_scale=12), zorder=9)
    
    ax_main.set_title('Problem 4/1: 2D Three-Particle System Kinetics', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. Theoretical Derivation & Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Analysis (Total Mass M = 2m + 3m + m = 6m):\n"
        r"1) Mass Center Position $\bar{\mathbf{r}}$:" "\n"
        r"  $\bullet\ \bar{\mathbf{r}} = \frac{2m(d\mathbf{j}) + 3m(2d\mathbf{i} + d\mathbf{j}) + m(2d\mathbf{i})}{6m} = \mathbf{\frac{d}{6}(8\mathbf{i} + 5\mathbf{j})}$" "\n\n"
        r"2) Mass Center Velocity $\dot{\bar{\mathbf{r}}}$ & Acceleration $\ddot{\bar{\mathbf{r}}}$:" "\n"
        r"  $\bullet\ \dot{\bar{\mathbf{r}}} = \frac{2m(2v\mathbf{i}) + 3m(v\mathbf{j})}{6m} = \mathbf{\frac{v}{6}(4\mathbf{i} + 3\mathbf{j})},\quad \ddot{\bar{\mathbf{r}}} = \frac{\sum\mathbf{F}}{6m} = \mathbf{\frac{F\mathbf{i}}{6m}}$" "\n\n"
        r"3) System Kinetic Energy $T$:" "\n"
        r"  $\bullet\ T = \sum\frac{1}{2}m_i v_i^2 = \frac{1}{2}[2m(2v)^2 + 3m(v^2)] = \mathbf{\frac{11}{2}mv^2}$" "\n\n"
        r"4) Angular Momentum $\mathbf{H}_O$ & Rate $\dot{\mathbf{H}}_O$ about Point $O$:" "\n"
        r"  $\bullet\ \mathbf{H}_O = \sum(\mathbf{r}_i \times m_i\mathbf{v}_i) = -4mvd\mathbf{k} + 6mvd\mathbf{k} = \mathbf{2mvd\mathbf{k}}$" "\n"
        r"  $\bullet\ \dot{\mathbf{H}}_O = \sum\mathbf{M}_O = (2d\mathbf{i} + d\mathbf{j}) \times (F\mathbf{i}) = \mathbf{-Fd\mathbf{k}}$"
    )
    ax_calc.text(0.35, 5.95, sol_box, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"Live State Monitor ($t = {t:.2f}\\ \\mathrm{{s}}$, normalized $m=d=v=F=1$):\n"
        f"Mass Center: $\\bar{{\\mathbf{{r}}}}(t) = ({r_bar[0]:.2f}\\mathbf{{i}} + {r_bar[1]:.2f}\\mathbf{{j}})\\ d$ (Initial: $1.33\\mathbf{{i}} + 0.83\\mathbf{{j}}$)\n"
        f"Kinetic Energy: $T(t) = {T_curr:.2f}\\ mv^2$ (Initial Theoretical Value: $11/2 = 5.50\\ mv^2$)\n"
        f"Angular Momentum: $H_{{Oz}}(t) = {HO_z:+.2f}\\ mvd\\mathbf{{k}}$ ($\\dot{{H}}_O = -1.00\\ Fd\\mathbf{{k}}$)"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('2D System State Derivation & Validation', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_1_three_particles_2d.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
