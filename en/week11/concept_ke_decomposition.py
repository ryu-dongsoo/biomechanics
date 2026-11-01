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
Supplementary Concept Animation 2: Kinetic Energy Decomposition (Eq. 4.4) & Work of Internal Forces
Dynamics 9th Ed. - Chapter 4, Section 4.3 Work-Energy and Kinetic Energy of a System
T = (1/2) m v_bar^2 + sum (1/2) m_i |rho_dot_i|^2
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

m_i = 2.0
masses = np.array([m_i, m_i, m_i])
M_tot = 6.0

v_bar = np.array([1.80, 0.0])
T_trans_const = 0.5 * M_tot * np.dot(v_bar, v_bar)  # 9.72 J

omega_rot = 2.2
Omega_rad = 2.6
r_mean = 0.72
r_amp = 0.22
base_ang = np.radians([90.0, 210.0, 330.0])

def state_at(t):
    rG = np.array([-1.6 + v_bar[0] * t, 0.15])
    rad = r_mean + r_amp * np.sin(Omega_rad * t)
    drad = r_amp * Omega_rad * np.cos(Omega_rad * t)
    ang = base_ang + omega_rot * t

    rho = np.stack([rad * np.cos(ang), rad * np.sin(ang)], axis=1)
    er = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    eth = np.stack([-np.sin(ang), np.cos(ang)], axis=1)
    rho_dot = drad * er + (rad * omega_rot) * eth

    pos = rG[None, :] + rho
    vel = v_bar[None, :] + rho_dot

    T_direct = 0.5 * np.sum(masses * np.sum(vel**2, axis=1))
    T_trans = 0.5 * M_tot * np.dot(v_bar, v_bar)
    T_rel = 0.5 * np.sum(masses * np.sum(rho_dot**2, axis=1))
    cross_term = np.dot(v_bar, np.sum(masses[:, None] * rho_dot, axis=0))
    return rG, pos, rho, rho_dot, vel, T_direct, T_trans, T_rel, cross_term, drad

n_frames = 56
t_max = 2.4
t_arr = np.linspace(0.0, t_max, n_frames)
t_dense = np.linspace(0.0, t_max, 300)

T_tr_curve, T_rl_curve, T_tot_curve = [], [], []
for tt in t_dense:
    _, _, _, _, _, td, ttr, trl, _, _ = state_at(tt)
    T_tr_curve.append(ttr)
    T_rl_curve.append(trl)
    T_tot_curve.append(td)
T_tr_curve = np.array(T_tr_curve)
T_rl_curve = np.array(T_rl_curve)
T_tot_curve = np.array(T_tot_curve)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.18, 1.0], height_ratios=[0.95, 1.05],
              left=0.04, right=0.97, top=0.89, bottom=0.09, wspace=0.19, hspace=0.36)

ax_2d  = fig.add_subplot(gs[:, 0])
ax_bar = fig.add_subplot(gs[0, 1])
ax_t   = fig.add_subplot(gs[1, 1])

fig.suptitle("Concept Animation 2: Kinetic Energy Decomposition (Eq. 4.4) — CM Translation + Relative Motion",
             fontsize=13.4, fontweight='bold', color='#0f172a', y=0.965)

def update(frame):
    t = float(t_arr[frame])
    rG, pos, rho, rho_dot, vel, T_direct, T_trans, T_rel, cross_term, drad = state_at(t)

    ax_2d.clear()
    ax_bar.clear()
    ax_t.clear()
    for ax in (ax_2d, ax_bar, ax_t):
        ax.set_facecolor('#ffffff')

    ax_2d.set_xlim(-2.65, 3.85)
    ax_2d.set_ylim(-1.55, 3.25)
    ax_2d.set_aspect('equal')
    ax_2d.axis('off')
    ax_2d.set_title(r"1) Velocity Decomposition ($\mathbf{v}_i = \bar{\mathbf{v}} + \dot{\boldsymbol{\rho}}_i$) & Internal Work",
                    fontsize=11.4, fontweight='bold', color='#1e293b', pad=6)

    ax_2d.plot([-2.3, 3.5], [0.15, 0.15], color='#cbd5e1', ls='--', lw=1.4, zorder=1)
    ax_2d.plot([-1.6, rG[0]], [0.15, 0.15], color='#2563eb', lw=2.6, zorder=2)

    for i in range(3):
        ax_2d.plot([rG[0], pos[i, 0]], [rG[1], pos[i, 1]], color='#64748b', lw=2.6, ls='-', zorder=3)
        c = patches.Circle(pos[i], 0.17, facecolor='#38bdf8', edgecolor='#0369a1', lw=1.8, zorder=5)
        ax_2d.add_patch(c)
        ax_2d.text(pos[i, 0], pos[i, 1], r'$2\mathrm{kg}$', fontsize=8.0, fontweight='bold',
                   color='#0f172a', ha='center', va='center', zorder=6)

        ax_2d.annotate('', xy=pos[i] + 0.24 * rho_dot[i], xytext=pos[i],
                       arrowprops=dict(arrowstyle='->', color='#16a34a', lw=2.1, mutation_scale=12), zorder=7)
        ax_2d.annotate('', xy=pos[i] + 0.24 * vel[i], xytext=pos[i],
                       arrowprops=dict(arrowstyle='->', color='#1e3a8a', lw=1.8, ls='--', mutation_scale=11), zorder=6)

    ax_2d.plot(rG[0], rG[1], marker='D', markersize=8.5,
               markerfacecolor='#facc15', markeredgecolor='#1d4ed8', markeredgewidth=2.0, zorder=8)
    ax_2d.annotate('', xy=rG + 0.34 * v_bar, xytext=rG,
                   arrowprops=dict(arrowstyle='->', color='#2563eb', lw=2.8, mutation_scale=14), zorder=8)
    ax_2d.text(rG[0] + 0.28, rG[1] - 0.24, r'$G\ (\bar{\mathbf{v}})$', fontsize=9.8, fontweight='bold', color='#1d4ed8')

    ax_2d.text(-2.50, -0.98, "Blue solid: $\\bar{\\mathbf{v}}$ (CM)   |   Green solid: $\\dot{\\boldsymbol{\\rho}}_i$ (Rel)   |   Navy dashed: $\\mathbf{v}_i$ (Total)",
               fontsize=8.6, fontweight='bold', color='#334155')

    bubble = (
        "[Student Tip] Two Key Insights on System Kinetic Energy!\n"
        "1) Why does the cross term vanish? Because relative momentum about $G$ is always zero ($\\Sigma m_i\\dot{\\boldsymbol{\\rho}}_i = \\mathbf{0}$)!\n"
        "2) Why does total KE change even with zero external force? Internal forces sum to zero ($\\Sigma\\mathbf{f}_i = \\mathbf{0}$),\n"
        "   yet when parts move apart/together, internal work ($U_{\\mathrm{int}} \\neq 0$) changes $T_{\\mathrm{rel}}$!"
    )
    ax_2d.text(-2.55, 3.16, bubble, fontsize=8.5, color='#78350f', va='top', ha='left', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.40', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_bot = (
        r"$T = \frac{1}{2}m\bar{v}^2 + \sum \frac{1}{2}m_i|\dot{\boldsymbol{\rho}}_i|^2"
        + rf" = {T_trans:.2f}\ \mathrm{{J}} + {T_rel:.2f}\ \mathrm{{J}} = \mathbf{{{T_direct:.2f}\ \mathrm{{J}}}}$"
        + f"   (Cross $= {abs(cross_term):.2f}\\ \\mathrm{{J}}$)"
    )
    ax_2d.text(0.60, -1.35, eq_bot, fontsize=9.4, color='#0f172a', ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.35', facecolor='#eff6ff', edgecolor='#60a5fa', lw=1.4))

    cats = ["CM $T_{\\mathrm{trans}}$\n$(\\frac{1}{2}m\\bar{v}^2)$",
            "Rel $T_{\\mathrm{rel}}$\n$(\\Sigma\\frac{1}{2}m_i\\dot{\\rho}_i^2)$",
            "Cross Term\n$(0)$",
            "Total $T$\n$(\\Sigma\\frac{1}{2}m_i v_i^2)$"]
    vals = [T_trans, T_rel, abs(cross_term), T_direct]
    bcols = ['#2563eb', '#16a34a', '#94a3b8', '#e11d48']
    bars = ax_bar.bar(range(4), vals, color=bcols, width=0.52, edgecolor='#1e293b', lw=1.2)
    ax_bar.set_xticks(range(4))
    ax_bar.set_xticklabels(cats, fontsize=8.6, fontweight='bold')
    ax_bar.set_ylim(0, 26.0)
    ax_bar.set_ylabel("Energy (J)", fontsize=9.5, fontweight='bold')
    ax_bar.set_title(r"2) Live Check: $\sum \frac{1}{2}m_i v_i^2 = T_{\mathrm{trans}} + T_{\mathrm{rel}}$ Exact Match!",
                     fontsize=10.2, fontweight='bold', color='#1e293b', pad=5)
    ax_bar.grid(True, axis='y', ls=':', alpha=0.5)
    for b_rect, v_num in zip(bars, vals):
        ax_bar.text(b_rect.get_x() + b_rect.get_width()/2, v_num + 0.7, f"{v_num:.2f} J",
                    ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#0f172a')

    ax_t.set_xlim(0.0, t_max)
    ax_t.set_ylim(0.0, 25.5)
    ax_t.set_xlabel("Time $t$ (s)", fontsize=9.5, fontweight='bold')
    ax_t.set_ylabel("Kinetic Energy (J)", fontsize=9.5, fontweight='bold')
    ax_t.set_title(r"3) With $\Sigma\mathbf{F}_{\mathrm{ext}}=\mathbf{0}$, $T_{\mathrm{trans}}$ Is Constant While Internal Work Varies $T_{\mathrm{rel}}$",
                   fontsize=9.9, fontweight='bold', color='#1e293b', pad=5)
    ax_t.grid(True, ls=':', alpha=0.5)
    mask = t_dense <= t + 1e-6
    ax_t.plot(t_dense, T_tot_curve, color='#fda4af', lw=1.2, ls=':')
    ax_t.plot(t_dense[mask], T_tr_curve[mask], color='#2563eb', lw=2.4, label=r'$T_{\mathrm{trans}} = \frac{1}{2}m\bar{v}^2$ (const)')
    ax_t.plot(t_dense[mask], T_rl_curve[mask], color='#16a34a', lw=2.2, ls='--', label=r'$T_{\mathrm{rel}} = \sum\frac{1}{2}m_i\dot{\rho}_i^2$')
    ax_t.plot(t_dense[mask], T_tot_curve[mask], color='#e11d48', lw=2.8, label=r'Total $T = T_{\mathrm{trans}} + T_{\mathrm{rel}}$')
    ax_t.plot([t, t, t], [T_trans, T_rel, T_direct], 'o', color='#0f172a', markersize=5.5)
    ax_t.legend(loc='upper right', fontsize=7.9)

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_ke_decomposition.gif")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
    anim.save(gif_path, writer='pillow', fps=13)
    plt.close(fig)
    print(f"Saved: {gif_path}")
