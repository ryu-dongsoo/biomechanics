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
Problem 3/142: 75 g Bullet Horizontal Impact on 50 kg Cart & Energy Loss Analysis
Engineering Mechanics: Dynamics 9th Edition - Section 3.9 Linear Impulse and Linear Momentum

Problem Specifications:
- Bullet mass m = 75 g = 0.075 kg, horizontal velocity v1 = 600 m/s (rightward)
- Wheeled cart mass M = 50 kg (initially at rest on horizontal rail, negligible rolling resistance)
- Bullet embeds in cart (plastic collision)

Analytical Results:
- Post-impact common velocity: vf = 0.075(600) / (50 + 0.075) = 0.899 m/s
- Mechanical energy lost: |ΔE| = T1 - T2 = 13,500 - 20.2 = 13,480 J (99.9% lost)
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

m = 0.075
v0 = 600.0
M = 50.0
M_tot = M + m
G_init = m * v0
vf = G_init / M_tot

T1 = 0.5 * m * (v0 ** 2)
T2 = 0.5 * M_tot * (vf ** 2)
delta_E = T1 - T2

n_frames = 72
t_arr = np.linspace(-0.50, 0.55, n_frames)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.22, 1.0], height_ratios=[0.95, 1.05],
              left=0.03, right=0.97, top=0.87, bottom=0.08, wspace=0.18, hspace=0.33)

ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])

fig.suptitle("Problem 3/142: 75 g Bullet–50 kg Cart Impact & Energy Loss Analysis",
             fontsize=14.5, fontweight='bold', color='#111827', y=0.965)

def draw_bullet(ax, tip_x, cy, zorder=6, alpha=1.0):
    L_b = 0.14
    H_b = 0.032
    xs_nose = np.linspace(tip_x - 0.055, tip_x, 12)
    u = (xs_nose - (tip_x - 0.055)) / 0.055
    ys_top = cy + H_b * np.sqrt(np.maximum(0.0, 1.0 - u**2))
    ys_bot = cy - H_b * np.sqrt(np.maximum(0.0, 1.0 - u**2))
    pts = ([[tip_x - L_b, cy - H_b], [tip_x - 0.055, cy - H_b]] +
           list(zip(xs_nose, ys_bot)) +
           list(zip(xs_nose[::-1], ys_top[::-1])) +
           [[tip_x - 0.055, cy + H_b], [tip_x - L_b, cy + H_b]])
    poly = patches.Polygon(pts, facecolor='#e5a387', edgecolor='#3b1f14', lw=1.4, zorder=zorder, alpha=alpha)
    ax.add_patch(poly)

def update(frame):
    t = t_arr[frame]

    ax1.clear()
    ax2.clear()
    ax3.clear()
    for ax in (ax1, ax2, ax3):
        ax.set_facecolor('#ffffff')

    ax1.set_xlim(-1.32, 1.56)
    ax1.set_ylim(-0.30, 1.18)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("Textbook 1:1 Impact Simulation (Zero External Horizontal Force → Momentum Conserved)",
                  fontsize=11.5, fontweight='bold', color='#1e293b', pad=6)

    ax1.fill_between([-1.26, 1.50], -0.16, 0.0, color='#dfd9d2', zorder=1)
    ax1.plot([-1.26, 1.50], [0.0, 0.0], color='#1e293b', lw=2.4, zorder=3)

    cart_w, cart_h = 0.68, 0.36
    cart_y0 = 0.055
    bullet_y = 0.235
    cart_x0 = 0.52

    if t < 0.0:
        prog = (t + 0.50) / 0.50
        cart_x = cart_x0
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = -0.92 + prog * (cart_left - (-0.92))
        phase_str = f"Before Impact: Bullet Approaching Rightward ($v_1 = {v0:.0f}\\ \\mathrm{{m/s}}$, Cart at Rest)"
        phase_col = '#1d4ed8'
    elif t <= 0.035:
        cart_x = cart_x0 + 0.02 * (t / 0.035)
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = cart_left + 0.14 * (t / 0.035)
        phase_str = "Impact Instant! Bullet Embeds with Heat & Plastic Deformation"
        phase_col = '#e11d48'
        for r_fl, col_fl, al in [(0.13, '#fde047', 0.55), (0.075, '#f97316', 0.80)]:
            ax1.add_patch(patches.Circle((cart_left, bullet_y), r_fl, facecolor=col_fl, edgecolor='none', alpha=al, zorder=7))
    else:
        prog_post = (t - 0.035) / (0.55 - 0.035)
        cart_x = cart_x0 + 0.02 + prog_post * 0.42
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = cart_left + 0.22
        phase_str = f"After Impact: Combined Cart + Bullet Rolls Right ($v_f = {vf:.3f}\\ \\mathrm{{m/s}}$)"
        phase_col = '#0ca678'

    ax1.plot([-1.20, cart_x - cart_w / 2.0], [bullet_y, bullet_y],
             color='#f97316', ls=(0, (7, 5)), lw=2.0, zorder=2)

    r_w = 0.072
    for wx_off in [-0.20, 0.20]:
        wc = (cart_x + wx_off, r_w)
        ax1.add_patch(patches.Circle(wc, r_w, facecolor='#bae6fd', edgecolor='#1e293b', lw=1.8, zorder=2.5))
        ax1.add_patch(patches.Circle(wc, r_w * 0.65, facecolor='#7dd3fc', edgecolor='none', zorder=2.6))

    cart_rect = patches.Rectangle((cart_x - cart_w / 2.0, cart_y0), cart_w, cart_h,
                                  facecolor='#b2d4e5', edgecolor='#1e293b', lw=2.0, zorder=4)
    ax1.add_patch(cart_rect)
    for wx_off in [-0.20, 0.20]:
        ax1.add_patch(patches.Circle((cart_x + wx_off, cart_y0 + 0.035), 0.015, facecolor='#111827', zorder=5))

    label_y = cart_y0 + 0.21 if t >= 0.0 else cart_y0 + 0.18
    ax1.text(cart_x + (0.05 if t >= 0.0 else 0.0), label_y, "50 kg",
             fontsize=13, fontweight='bold', color='#111827', ha='center', va='center', zorder=5)

    if t < 0.0:
        draw_bullet(ax1, b_tip_x, bullet_y, zorder=6, alpha=1.0)
        ax1.text(b_tip_x - 0.06, bullet_y + 0.075, "75 g",
                 fontsize=11.5, fontweight='bold', color='#111827', ha='center', zorder=6)
        arr_end = min(b_tip_x + 0.34, cart_x - cart_w / 2.0 - 0.02)
        if arr_end - b_tip_x > 0.08:
            ax1.annotate('', xy=(arr_end, bullet_y), xytext=(b_tip_x + 0.01, bullet_y),
                         arrowprops=dict(arrowstyle='->', color='#0ca678', lw=2.4, mutation_scale=15), zorder=6)
            ax1.text(0.5 * (b_tip_x + arr_end), bullet_y + 0.065, "600 m/s",
                     fontsize=11, fontweight='bold', color='#111827', ha='center', zorder=6)
    else:
        ax1.plot([cart_left, b_tip_x - 0.12], [bullet_y, bullet_y], color='#78350f', lw=3.0, ls=':', zorder=4.5)
        draw_bullet(ax1, b_tip_x, bullet_y, zorder=5.2, alpha=0.88)
        if t > 0.035:
            c_right = cart_x + cart_w / 2.0
            ax1.annotate('', xy=(c_right + 0.34, bullet_y), xytext=(c_right + 0.02, bullet_y),
                         arrowprops=dict(arrowstyle='->', color='#0ca678', lw=2.8, mutation_scale=16), zorder=6)
            ax1.text(c_right + 0.18, bullet_y + 0.075, rf"$v_f = {vf:.3f}\ \mathrm{{m/s}}$",
                     fontsize=10.8, fontweight='bold', color='#0ca678', ha='center', zorder=6)

    ax1.text(0.12, -0.24, phase_str, fontsize=10.0, fontweight='bold', color=phase_col, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8fafc', edgecolor=phase_col, lw=1.4))

    bubble_str = (
        "Key Concept: Why is Momentum Conserved while 99.9% of Energy is Lost?\n"
        "• [100% Momentum Conserved] Contact impulses between bullet & cart are equal and opposite\n"
        "  internal forces that cancel out! With no external horizontal force, G = 45 N·s stays constant.\n"
        "• [99.9% Energy Lost] Friction & deformation during penetration convert 13,480 J into heat!"
    )
    ax1.text(-1.26, 1.13, bubble_str, fontsize=8.8, color='#78350f', va='top', ha='left', linespacing=1.35,
             bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6), zorder=8)

    curr_T = T1 if t < 0 else (T1 - (t / 0.035) * delta_E if t <= 0.035 else T2)
    curr_E_pct = (curr_T / T1) * 100.0

    cats = ['Linear Momentum $G$\n(% Retained)', 'Kinetic Energy $T$\n(% Retained)']
    init_vals = [100.0, 100.0]
    curr_vals = [100.0, curr_E_pct]

    x_pos = np.arange(len(cats))
    w_bar = 0.30
    ax2.bar(x_pos - w_bar/2, init_vals, width=w_bar, color='#cbd5e1', edgecolor='#64748b', label='Before Impact (100%)')
    bars = ax2.bar(x_pos + w_bar/2, curr_vals, width=w_bar, color=['#2563eb', '#e11d48'], edgecolor='#1e293b', label='Current State')

    ax2.set_ylim(0, 146)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(cats, fontsize=9.5, fontweight='bold')
    ax2.set_ylabel("Percentage (%)", fontsize=9.8, fontweight='bold')
    ax2.set_title("Linear Momentum (100% Conserved) vs Kinetic Energy (99.9% Lost)",
                  fontsize=10.5, fontweight='bold', color='#1e293b', pad=5)
    ax2.grid(axis='y', ls=':', alpha=0.5)
    ax2.legend(loc='upper left', fontsize=8.1, ncol=2)

    ax2.text(bars[0].get_x() + w_bar/2, 103, "45.0 N·s\n(100%)", ha='center', va='bottom',
             fontsize=8.8, fontweight='bold', color='#1d4ed8')
    ax2.text(bars[1].get_x() + w_bar/2, curr_E_pct + 3,
             f"{curr_T:,.1f} J\n({curr_E_pct:.1f}%)", ha='center', va='bottom',
             fontsize=8.8, fontweight='bold', color='#be123c')

    ax3.axis('off')
    eq_card = (
        r"$\mathbf{1.\ Conservation\ of\ Linear\ Momentum\ (\Sigma F_x = 0 \Rightarrow G_1 = G_2)}$" + "\n"
        r"$m v_1 + M(0) = (m + M)v_f \Rightarrow 0.075(600) = (0.075 + 50)\,v_f$" + "\n"
        r"$\therefore\ v_f = \frac{45.0}{50.075} = \mathbf{0.899\ m/s}\ \ (\mathrm{rightward})$" + "\n\n"
        r"$\mathbf{2.\ Mechanical\ Energy\ Loss\ |\Delta E|\ &\ Percent\ Loss\ n}$" + "\n"
        r"$T_1 = \frac{1}{2}(0.075)(600)^2 = 13,500\ \mathrm{J},\quad T_2 = \frac{1}{2}(50.075)(0.8987)^2 = 20.2\ \mathrm{J}$" + "\n"
        r"$|\Delta E| = T_1 - T_2 = \mathbf{13,480\ J},\quad n = \frac{13,480}{13,500}\times 100\% = \mathbf{99.9\%}$"
    )
    ax3.text(0.02, 0.96, eq_card, fontsize=9.4, color='#111827', va='top', ha='left', linespacing=1.40,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4))

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "prob3_142_bullet_cart_impact.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=85)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved prob3_142_bullet_cart_impact.gif")
