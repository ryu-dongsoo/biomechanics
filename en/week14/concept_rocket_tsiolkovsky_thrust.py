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
Supplementary Concept Animation 2: Variable-Mass Rocket Propulsion & Tsiolkovsky Velocity Integration
Engineering Mechanics: Dynamics 9th Ed. - Chapter 4, Sec. 4.7 Variable Mass
- Pure white background (#ffffff), STIX math font, strict visual clarity
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Representative rocket parameters (mass ratio m0/mb = 4.0)
m0 = 1000.0        # Initial total mass (kg)
mb = 250.0         # Structural dry mass at burnout (kg)
m_prime = 15.0     # Positive fuel burn rate m' = -dm/dt (kg/s)
m_dot = -m_prime   # Signed mass rate dm/dt = -15.0 kg/s
u = 2000.0         # Relative exhaust speed (m/s)
g = 9.81           # Gravitational acceleration (m/s^2)

tb = (m0 - mb) / m_prime                      # 50.0 s
T_thrust = m_prime * u                        # 30,000 N = 30.0 kN (constant)
v_max = u * np.log(m0 / mb) - g * tb          # 2772.6 - 490.5 = 2282.1 m/s
a_init = T_thrust / m0 - g                    # 20.19 m/s^2
a_final = T_thrust / mb - g                   # 110.19 m/s^2

n_frames = 54
t_vals = np.concatenate([
    np.linspace(0.0, tb, 45),
    np.full(9, tb)
])

fig = plt.figure(figsize=(14, 6.5), dpi=120)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.02, 1.18], height_ratios=[1.0, 1.0, 1.15],
              left=0.04, right=0.97, top=0.87, bottom=0.09, wspace=0.18, hspace=0.38)

ax_phys = fig.add_subplot(gs[:, 0])
ax_m = fig.add_subplot(gs[0, 1])
ax_a = fig.add_subplot(gs[1, 1])
ax_v = fig.add_subplot(gs[2, 1])

fig.suptitle('Concept 2: Variable-Mass Rocket Nonlinear Acceleration & Tsiolkovsky Velocity Equation',
             fontsize=14.0, fontweight='bold', color='#1e3a5f', y=0.96)


def draw_rocket_cutaway(ax, xc, yc, fuel_frac):
    bw, bh = 0.56, 1.95
    ax.add_patch(patches.Rectangle((xc - bw / 2, yc), bw, bh,
                                   facecolor='#eceff1', edgecolor='#263238', lw=2.0, zorder=3))
    tw, th = 0.38, 1.32
    ty0 = yc + 0.30
    ax.add_patch(patches.Rectangle((xc - tw / 2, ty0), tw, th,
                                   facecolor='#ffffff', edgecolor='#78909c', lw=1.3, zorder=4))
    if fuel_frac > 0.005:
        ax.add_patch(patches.Rectangle((xc - tw / 2, ty0), tw, th * fuel_frac,
                                       facecolor='#ffb74d', edgecolor='none', zorder=5))
        ax.plot([xc - tw / 2, xc + tw / 2], [ty0 + th * fuel_frac, ty0 + th * fuel_frac],
                color='#e65100', lw=1.6, zorder=6)

    nose = patches.Polygon([[xc - bw / 2, yc + bh], [xc + bw / 2, yc + bh], [xc, yc + bh + 0.62]],
                           facecolor='#90caf9', edgecolor='#1e3a5f', lw=2.0, zorder=3)
    ax.add_patch(nose)

    fin_l = patches.Polygon([[xc - bw / 2, yc + 0.45], [xc - bw / 2 - 0.30, yc - 0.08], [xc - bw / 2, yc + 0.05]],
                            facecolor='#78909c', edgecolor='#263238', lw=1.6, zorder=2)
    fin_r = patches.Polygon([[xc + bw / 2, yc + 0.45], [xc + bw / 2 + 0.30, yc - 0.08], [xc + bw / 2, yc + 0.05]],
                            facecolor='#78909c', edgecolor='#263238', lw=1.6, zorder=2)
    ax.add_patch(fin_l)
    ax.add_patch(fin_r)

    noz = patches.Polygon([[xc - 0.14, yc], [xc + 0.14, yc], [xc + 0.22, yc - 0.22], [xc - 0.22, yc - 0.22]],
                          facecolor='#455a64', edgecolor='#263238', lw=1.5, zorder=3)
    ax.add_patch(noz)

    if fuel_frac > 0.001:
        ax.add_patch(patches.Polygon([[xc - 0.18, yc - 0.22], [xc + 0.18, yc - 0.22], [xc, yc - 1.08]],
                                     facecolor='#ff7043', alpha=0.85, zorder=2))
        ax.add_patch(patches.Polygon([[xc - 0.09, yc - 0.22], [xc + 0.09, yc - 0.22], [xc, yc - 0.72]],
                                     facecolor='#fff176', alpha=0.95, zorder=3))


t_dense = np.linspace(0, tb, 150)
m_dense = m0 - m_prime * t_dense
a_dense = T_thrust / m_dense - g
a_const_m = np.full_like(t_dense, a_init)
v_ideal_dense = u * np.log(m0 / m_dense)
v_act_dense = v_ideal_dense - g * t_dense


def update(frame):
    t = t_vals[frame]
    m_curr = m0 - m_prime * t
    fuel_frac = max(0.0, (m_curr - mb) / (m0 - mb))
    W_curr = m_curr * g
    a_curr = T_thrust / m_curr - g
    v_curr = u * np.log(m0 / m_curr) - g * t

    # ---------------- 1. Left: Cutaway Variable-Mass Rocket & Force Vectors ----------------
    ax_phys.cla()
    ax_phys.set_facecolor('#ffffff')
    ax_phys.set_xlim(-2.6, 2.7)
    ax_phys.set_ylim(-1.35, 5.15)
    ax_phys.set_aspect('equal')
    ax_phys.axis('off')

    yc = 1.15 + 0.55 * (t / tb)
    draw_rocket_cutaway(ax_phys, 0.0, yc, fuel_frac)

    ax_phys.annotate('', xy=(0.55, yc + 0.95), xytext=(0.55, yc - 0.20),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=3.0, mutation_scale=18), zorder=7)
    ax_phys.text(0.68, yc + 0.35,
                 f'Constant Thrust\n$T = m\'u = -\\dot{{m}}u$\n$= {T_thrust/1000:.1f}\\,\\mathrm{{kN}}$',
                 fontsize=9.4, fontweight='bold', color='#d32f2f', va='center')

    ax_phys.annotate('', xy=(-0.52, yc - 1.00), xytext=(-0.52, yc - 0.22),
                     arrowprops=dict(arrowstyle='->', color='#0277bd', lw=2.3, mutation_scale=15), zorder=7)
    ax_phys.text(-0.64, yc - 0.62, f'Exhaust speed\n$u = {u:.0f}\\,\\mathrm{{m/s}}$',
                 fontsize=9.0, fontweight='bold', color='#01579b', ha='right', va='center')

    w_len = 0.28 + 0.65 * (m_curr / m0)
    ax_phys.annotate('', xy=(0.55, yc + 1.85 - w_len), xytext=(0.55, yc + 1.85),
                     arrowprops=dict(arrowstyle='->', color='#6a1b9a', lw=2.3, mutation_scale=15), zorder=7)
    ax_phys.text(0.68, yc + 1.62,
                 f'Shrinking Weight\n$m(t)g = {W_curr/1000:.2f}\\,\\mathrm{{kN}}$\n$(m = {m_curr:.0f}\\,\\mathrm{{kg}})$',
                 fontsize=9.1, fontweight='bold', color='#6a1b9a', va='center')

    a_len = 0.35 + 1.25 * (a_curr / a_final)
    ax_phys.annotate('', xy=(-0.62, yc + 0.55 + a_len), xytext=(-0.62, yc + 0.55),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=3.0, mutation_scale=18), zorder=7)
    ax_phys.text(-0.76, yc + 0.55 + a_len * 0.55,
                 f'Surging Accel!\n$a(t) = {a_curr:.1f}\\,\\mathrm{{m/s^2}}$\n$({a_curr/g:.1f}g)$\n$v = {v_curr:.0f}\\,\\mathrm{{m/s}}$',
                 fontsize=9.4, fontweight='bold', color='#1b5e20', ha='right', va='center')

    eq_str = (
        r'EOM: $T - mg = m\frac{dv}{dt} \quad (T = m^\prime u = -\dot{m}u)$' '\n'
        r'Integration: $\int_0^v dv = -u\int_{m_0}^m \frac{dm}{m} - g\int_0^t dt \;\Rightarrow\; v = u\ln\frac{m_0}{m} - gt$'
    )
    ax_phys.text(0.05, -0.92, eq_str, fontsize=9.1, ha='center', va='center', color='#1e3a5f',
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f4f8fb', edgecolor='#90caf9', lw=1.3))

    # ---------------- 2. Right Top: Linear Mass Decrease m(t) ----------------
    ax_m.cla()
    ax_m.set_facecolor('#ffffff')
    ax_m.plot(t_dense, m_dense, color='#e65100', lw=2.3, label=r'$m(t) = m_0 - m^\prime t$')
    ax_m.axhline(mb, color='#78909c', ls='--', lw=1.2, label=r'Dry mass $m_b = 250\,\mathrm{kg}$')
    ax_m.fill_between(t_dense[t_dense <= t], mb, m_dense[t_dense <= t], color='#ffe0b2', alpha=0.55)
    ax_m.plot(t, m_curr, 'o', color='#e65100', markersize=6.5, zorder=5)
    ax_m.set_xlim(0, tb * 1.03)
    ax_m.set_ylim(0, 1120)
    ax_m.set_ylabel(r'$m(t)\ (\mathrm{kg})$', fontsize=9.8, fontweight='bold')
    ax_m.set_title(f'1. Linear Mass Decrease: $m(t) = {m_curr:.0f}\\,\\mathrm{{kg}}$  (Fuel left {fuel_frac*100:.0f}%, Ratio $m_0/m_b = 4$)',
                   fontsize=10.1, fontweight='bold', color='#1e3a5f')
    ax_m.grid(True, ls=':', alpha=0.45)
    ax_m.legend(loc='upper right', fontsize=8.2, framealpha=0.95)

    # ---------------- 3. Right Middle: Nonlinearly Increasing Acceleration a(t) ----------------
    ax_a.cla()
    ax_a.set_facecolor('#ffffff')
    ax_a.plot(t_dense, a_dense, color='#2e7d32', lw=2.4, label=r'Actual $a(t) = \frac{m^\prime u}{m(t)} - g$')
    ax_a.plot(t_dense, a_const_m, color='#90a4ae', ls='--', lw=1.5, label=r'If mass were constant: $a_0 = 20.2\,\mathrm{m/s^2}$')
    ax_a.plot(t, a_curr, 'o', color='#2e7d32', markersize=6.5, zorder=5)
    ax_a.set_xlim(0, tb * 1.03)
    ax_a.set_ylim(0, 125)
    ax_a.set_ylabel(r'$a(t)\ (\mathrm{m/s^2})$', fontsize=9.8, fontweight='bold')
    ax_a.set_title(f'2. Nonlinear Acceleration Surge ($5.5\\times$ increase): $a(t) = {a_curr:.1f}\\,\\mathrm{{m/s^2}}$',
                   fontsize=10.1, fontweight='bold', color='#1e3a5f')
    ax_a.grid(True, ls=':', alpha=0.45)
    ax_a.legend(loc='upper left', fontsize=8.2, framealpha=0.95)

    # ---------------- 4. Right Bottom: Tsiolkovsky Velocity v(t) ----------------
    ax_v.cla()
    ax_v.set_facecolor('#ffffff')
    ax_v.plot(t_dense, v_ideal_dense, color='#00897b', ls='--', lw=1.7, label=r'Gravity-free $u\ln(m_0/m)$')
    ax_v.plot(t_dense, v_act_dense, color='#1565c0', lw=2.5, label=r'Actual $v(t) = u\ln(m_0/m) - gt$')

    mask = t_dense <= t
    ax_v.fill_between(t_dense[mask], v_act_dense[mask], v_ideal_dense[mask],
                      color='#ffcdd2', alpha=0.45, label=r'Gravity loss $-gt$')
    ax_v.plot(t, v_curr, 'o', color='#d32f2f', markersize=6.8, zorder=6)

    ax_v.set_xlim(0, tb * 1.03)
    ax_v.set_ylim(0, 3050)
    ax_v.set_xlabel(r'Burn Time $t\ (\mathrm{s})$', fontsize=10, fontweight='bold')
    ax_v.set_ylabel(r'$v(t)\ (\mathrm{m/s})$', fontsize=9.8, fontweight='bold')
    ax_v.set_title(f'3. Tsiolkovsky Velocity: $v(t) = {v_curr:.0f}\\,\\mathrm{{m/s}}$  (Burnout $t_b=50\\,\\mathrm{{s}}$ Max $v_{{\\max}} = {v_max:.0f}\\,\\mathrm{{m/s}}$)',
                   fontsize=10.1, fontweight='bold', color='#1e3a5f')
    ax_v.grid(True, ls=':', alpha=0.45)
    ax_v.legend(loc='upper left', fontsize=8.1, framealpha=0.95)


anim = FuncAnimation(fig, update, frames=n_frames, interval=75)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_rocket_tsiolkovsky_thrust.gif')
anim.save(gif_path, writer='pillow', fps=14)
plt.close()
print(f'Saved: {gif_path}')
