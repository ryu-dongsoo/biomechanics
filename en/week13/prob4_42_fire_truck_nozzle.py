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
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.6: Steady Mass Flow
Problem 4/42 - Fire Truck Nozzle Discharge Velocity v and Additional Support Moment M at Joint A
- Pure white background (#ffffff) & 2-panel layout (14 x 6.5)
- Quantitative verification:
  * Spring stiffness k = 15 kN/m = 15000 N/m, spring compression x = 150 mm = 0.150 m
  * Nozzle exit diameter d = 30 mm = 0.030 m -> Area A = (pi/4)*(0.030)^2 = 7.0686e-4 m^2
  * Mass flow rate m' = rho * A * v = 1000 * 7.0686e-4 * v = 0.7069 * v (kg/s)
  * 1) Horizontal momentum equation (kx = m' * Delta v):
       15000 * (0.150) = 0.7069 * v * (v - 0) -> 2250 = 0.7069 * v^2 -> v^2 = 3183 -> v = 56.4 m/s
  * 2) Angular momentum equation about joint A (Sigma M_A = m' * v * d_arm):
       d_arm = 15*sin(75 deg) - 4.8*cos(75 deg) = 14.489 - 1.242 = 13.25 m
       M = (15 * 150) * (15*sin(75 deg) - 4.8*cos(75 deg)) = 2250 * (13.25) = 29,800 N*m = 29.8 kN*m
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

rho = 1000.0
d_noz = 0.030
A_noz = 0.25 * np.pi * d_noz**2   # 7.0686e-4 m^2
k_sp = 15000.0                    # 15 kN/m
x_sp_max = 0.150                  # 150 mm

F_sp_max = k_sp * x_sp_max        # 2250 N
v_final = np.sqrt(F_sp_max / (rho * A_noz))  # 56.419 m/s -> 56.4 m/s
m_dot_final = rho * A_noz * v_final          # 39.88 kg/s

L1 = 15.0                         # Main ladder length (m)
L2 = 4.8                          # Upper boom length (m)
ang1_deg = 75.0
ang1 = np.radians(ang1_deg)

d_arm = L1 * np.sin(ang1) - L2 * np.cos(ang1)  # 13.2466 m (~= 13.25 m)
M_final = F_sp_max * d_arm                     # 29,804.8 N*m -> 29.8 kN*m

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_spring(ax, x0, x1, y_c, n_coils=7, amp=0.18):
    xs = np.linspace(x0, x1, n_coils * 2 + 3)
    ys = np.full_like(xs, y_c)
    for i in range(1, len(xs) - 1):
        ys[i] = y_c + (amp if i % 2 == 1 else -amp)
    ax.plot(xs, ys, color='#37474f', lw=1.8, zorder=4)


def draw_truck_wheel(ax, wx, wy, r=0.26):
    ax.add_patch(patches.Circle((wx, wy), r, facecolor='#455a64', edgecolor='#111111', lw=1.6, zorder=6))
    ax.add_patch(patches.Circle((wx, wy), r * 0.52, facecolor='#cfd8dc', edgecolor='#263238', lw=1.1, zorder=7))


def update(frame):
    prog = min(1.0, frame / 28.0)
    smooth_p = 0.5 - 0.5 * np.cos(np.pi * prog)
    x_sp_curr = x_sp_max * smooth_p
    F_curr = k_sp * x_sp_curr
    v_curr = v_final * np.sqrt(smooth_p)
    M_curr = F_curr * d_arm
    phase_t = (frame * 0.10) % 1.0

    dx_plot = 0.28 * smooth_p

    # ---------------- 1. Left Panel: Fire Ladder Truck Mechanism ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(0.5, 8.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    y_gnd = 1.25
    x_wall = 8.95

    ax_main.fill_between([0.4, x_wall + 0.35], y_gnd - 0.40, y_gnd, color='#e5dfd5', zorder=1)
    ax_main.fill_between([x_wall, x_wall + 0.35], y_gnd - 0.40, 2.35, color='#e5dfd5', zorder=1)
    ax_main.plot([0.4, x_wall], [y_gnd, y_gnd], color='#333333', lw=2.0, zorder=3)
    ax_main.plot([x_wall, x_wall], [y_gnd, 2.35], color='#333333', lw=2.0, zorder=3)

    x_A = 6.75 + dx_plot
    y_A = 2.28

    # 1) Fire truck body and cab
    ax_main.add_patch(patches.Rectangle((3.95 + dx_plot, 1.48), 4.15, 0.22,
                                        facecolor='#78909c', edgecolor='#263238', lw=1.4, zorder=4))
    ax_main.add_patch(patches.Rectangle((4.15 + dx_plot, 1.70), 2.95, 0.48,
                                        facecolor='#e53935', edgecolor='#263238', lw=1.5, zorder=4))
    ax_main.add_patch(patches.Rectangle((4.15 + dx_plot, 1.82), 2.95, 0.12,
                                        facecolor='#fdd835', edgecolor='#263238', lw=0.8, zorder=5))
    cab_poly = np.array([
        [7.15 + dx_plot, 1.70],
        [8.08 + dx_plot, 1.70],
        [8.08 + dx_plot, 2.08],
        [7.92 + dx_plot, 2.38],
        [7.15 + dx_plot, 2.38]
    ])
    ax_main.add_patch(patches.Polygon(cab_poly, facecolor='#e53935', edgecolor='#263238', lw=1.5, zorder=4))
    win_poly = np.array([
        [7.52 + dx_plot, 2.04],
        [7.98 + dx_plot, 2.04],
        [7.86 + dx_plot, 2.30],
        [7.52 + dx_plot, 2.30]
    ])
    ax_main.add_patch(patches.Polygon(win_poly, facecolor='#4fc3f7', edgecolor='#01579b', lw=1.1, zorder=5))
    ax_main.add_patch(patches.Circle((7.45 + dx_plot, 2.43), 0.06, facecolor='#d50000', edgecolor='#263238', lw=1.0, zorder=5))

    for wx_off in [4.75, 5.45, 7.55]:
        draw_truck_wheel(ax_main, wx_off + dx_plot, y_gnd + 0.26, r=0.26)

    draw_spring(ax_main, 8.08 + dx_plot, x_wall, y_c=1.68, n_coils=6, amp=0.17)

    # 2) Turntable & Joint A
    turntable = np.array([
        [x_A - 0.35, 2.18],
        [x_A + 0.35, 2.18],
        [x_A + 0.22, y_A + 0.08],
        [x_A - 0.22, y_A + 0.08]
    ])
    ax_main.add_patch(patches.Polygon(turntable, facecolor='#cfd8dc', edgecolor='#263238', lw=1.5, zorder=5))

    # 3) Articulated ladder geometry
    s_len = 0.32
    L1_p = L1 * s_len
    L2_p = L2 * s_len

    u1 = np.array([-np.cos(ang1), np.sin(ang1)])
    n1 = np.array([np.sin(ang1), np.cos(ang1)])

    p_A = np.array([x_A, y_A])
    p_B = p_A + L1_p * u1

    u2 = np.array([-np.sin(ang1), -np.cos(ang1)])
    n2 = np.array([-np.cos(ang1), np.sin(ang1)])
    p_C = p_B + L2_p * u2

    for seg_i, (f0, f1, w_boom) in enumerate([(0.0, 0.36, 0.24), (0.36, 0.70, 0.19), (0.70, 1.0, 0.14)]):
        pa = p_A + (f0 * L1_p) * u1
        pb = p_A + (f1 * L1_p) * u1
        poly_seg = np.array([
            pa - (w_boom / 2) * n1,
            pb - (w_boom / 2) * n1,
            pb + (w_boom / 2) * n1,
            pa + (w_boom / 2) * n1
        ])
        ax_main.add_patch(patches.Polygon(poly_seg, facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=4))

    w2 = 0.12
    poly_boom2 = np.array([
        p_B - (w2 / 2) * n2,
        p_C - (w2 / 2) * n2,
        p_C + (w2 / 2) * n2,
        p_B + (w2 / 2) * n2
    ])
    ax_main.add_patch(patches.Polygon(poly_boom2, facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=5))

    for pt_j in [p_A, p_B, p_C]:
        ax_main.add_patch(patches.Circle(pt_j, 0.09, facecolor='#ffffff', edgecolor='#263238', lw=1.6, zorder=6))
        ax_main.plot(pt_j[0], pt_j[1], 'ko', markersize=3.2, zorder=7)
    ax_main.text(p_A[0] + 0.24, p_A[1] + 0.18, r'$A$', fontsize=12, fontweight='bold', color='#111111')

    # 4) Nozzle head assembly
    ax_main.add_patch(patches.Rectangle((p_C[0] - 0.32, p_C[1] - 0.13), 0.38, 0.26,
                                        facecolor='#d7a184', edgecolor='#3e2723', lw=1.5, zorder=5))
    ax_main.add_patch(patches.Rectangle((p_C[0] - 0.48, p_C[1] - 0.07), 0.16, 0.14,
                                        facecolor='#bcaaa4', edgecolor='#3e2723', lw=1.4, zorder=5))
    noz_tip = np.array([p_C[0] - 0.48, p_C[1]])

    # 5) Horizontal water stream & velocity vector v
    if smooth_p > 0.02:
        jet_len = 2.35
        s_w = np.linspace(0, jet_len, 30)
        xw = noz_tip[0] - s_w
        yw_up = noz_tip[1] + 0.06 + 0.04 * (s_w / jet_len)
        yw_lo = noz_tip[1] - 0.06 - 0.04 * (s_w / jet_len)
        ax_main.fill_between(xw, yw_lo, yw_up, color='#bbdefb', alpha=0.88, zorder=3)
        ax_main.plot(xw, yw_up, color='#64b5f6', lw=1.1, zorder=4)
        ax_main.plot(xw, yw_lo, color='#64b5f6', lw=1.1, zorder=4)

        for k in range(5):
            frac = ((k / 5.0) + phase_t) % 1.0
            ax_main.plot(noz_tip[0] - frac * jet_len, noz_tip[1], 'o', color='#0277bd', markersize=4.0, zorder=5)

        ax_main.annotate('', xy=(noz_tip[0] - 1.15, noz_tip[1]), xytext=(noz_tip[0] - 0.15, noz_tip[1]),
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13), zorder=6)
        ax_main.text(noz_tip[0] - 0.65, noz_tip[1] + 0.22, f'$v = {v_curr:.1f}\\ \\mathrm{{m/s}}$',
                     fontsize=10.5, fontweight='bold', color='#00695c', ha='center')

    # 6) Dimension lines and angles
    ax_main.plot([p_A[0] - 1.1, p_A[0] - 0.2], [p_A[1], p_A[1]], color='#444444', ls='--', lw=1.1)
    arc_75 = patches.Arc(p_A, 1.35, 1.35, angle=0, theta1=105, theta2=180, color='#222222', lw=1.3)
    ax_main.add_patch(arc_75)
    ax_main.text(p_A[0] - 0.92, p_A[1] + 0.38, r'$75^\circ$', fontsize=10.2, fontweight='bold')

    arc_90 = patches.Arc(p_B, 0.95, 0.95, angle=0, theta1=-75, theta2=-165, color='#222222', lw=1.3)
    ax_main.add_patch(arc_90)
    ax_main.text(p_B[0] - 0.45, p_B[1] - 0.58, r'$90^\circ$', fontsize=10.0, fontweight='bold', ha='center')

    off_15 = 0.72 * n1
    pA_d = p_A + off_15
    pB_d = p_B + off_15
    ax_main.plot([p_A[0] + 0.2*n1[0], pA_d[0] + 0.15*n1[0]], [p_A[1] + 0.2*n1[1], pA_d[1] + 0.15*n1[1]], color='#666666', lw=0.9)
    ax_main.plot([p_B[0] + 0.2*n1[0], pB_d[0] + 0.15*n1[0]], [p_B[1] + 0.2*n1[1], pB_d[1] + 0.15*n1[1]], color='#666666', lw=0.9)
    ax_main.annotate('', xy=pB_d, xytext=pA_d, arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    mid_15 = 0.5 * (pA_d + pB_d)
    ax_main.text(mid_15[0] + 0.12, mid_15[1], '15 m', fontsize=10.2, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.1', facecolor='#ffffff', edgecolor='none'))

    off_48 = 0.52 * n2
    pB_d2 = p_B + off_48
    pC_d2 = p_C + off_48
    ax_main.plot([p_B[0] + 0.12*n2[0], pB_d2[0] + 0.12*n2[0]], [p_B[1] + 0.12*n2[1], pB_d2[1] + 0.12*n2[1]], color='#666666', lw=0.9)
    ax_main.plot([p_C[0] + 0.12*n2[0], pC_d2[0] + 0.12*n2[0]], [p_C[1] + 0.12*n2[1], pC_d2[1] + 0.12*n2[1]], color='#666666', lw=0.9)
    ax_main.annotate('', xy=pC_d2, xytext=pB_d2, arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    mid_48 = 0.5 * (pB_d2 + pC_d2)
    ax_main.text(mid_48[0], mid_48[1] + 0.18, '4.8 m', fontsize=10.0, fontweight='bold', ha='center')

    ax_main.set_title('Problem 4/42: Fire Truck Nozzle Speed $v$ & Support Moment $M$', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. Right Panel: Moment Arm Geometry & Derivation ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.55, 'Ladder Control Volume FBD & Moment Arm ($d$) about Joint $A$',
                 fontsize=10.6, fontweight='bold', ha='center', color='#1d4564')

    A_f = np.array([6.2, 6.65])
    B_f = np.array([5.55, 9.05])
    C_f = np.array([4.25, 8.70])
    ax_calc.plot([A_f[0], B_f[0], C_f[0]], [A_f[1], B_f[1], C_f[1]], color='#8d6e63', lw=3.2, zorder=3)
    ax_calc.plot(A_f[0], A_f[1], 'ko', markersize=5, zorder=5)
    ax_calc.text(A_f[0] + 0.22, A_f[1] - 0.05, r'$A$', fontsize=11, fontweight='bold')

    ax_calc.annotate('', xy=(2.5, C_f[1]), xytext=C_f,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
    ax_calc.text(2.4, C_f[1], r"$m' v = kx = 2250\ \mathrm{N}$",
                 fontsize=9.6, fontweight='bold', color='#2e7d32', ha='right', va='center')

    x_d_line = 7.45
    ax_calc.plot([A_f[0], x_d_line + 0.15], [A_f[1], A_f[1]], color='#777777', ls='--', lw=1.0)
    ax_calc.plot([C_f[0], x_d_line + 0.15], [C_f[1], C_f[1]], color='#777777', ls='--', lw=1.0)
    ax_calc.annotate('', xy=(x_d_line, C_f[1]), xytext=(x_d_line, A_f[1]),
                     arrowprops=dict(arrowstyle='<->', color='#d32f2f', lw=1.6))
    ax_calc.text(x_d_line + 0.18, 0.5 * (A_f[1] + C_f[1]),
                 r'$d = 15\sin 75^\circ - 4.8\cos 75^\circ$' + '\n' + r'$= 13.25\ \mathrm{m}$',
                 fontsize=9.1, fontweight='bold', color='#d32f2f', va='center')

    arc_ma = patches.Arc(A_f, 1.0, 1.0, angle=0, theta1=160, theta2=310, color='#d32f2f', lw=2.2)
    ax_calc.add_patch(arc_ma)
    ax_calc.text(A_f[0] - 0.85, A_f[1] - 0.35, r'$M$', fontsize=11, fontweight='bold', color='#d32f2f')

    sol_text = (
        "[Theoretical Derivation & Analysis (" + r"$\Sigma F_x = m'\Delta v,\ \Sigma M_A = m' v d$" + ")]\n"
        r"1) Nozzle mass flow rate ($d = 30\ \mathrm{mm}$):" + "\n"
        r"   $m' = \rho A v = 1000\left(\frac{\pi}{4}\right)(0.030)^2 v = 0.7069 v\ [\mathrm{kg/s}]$" + "\n"
        r"2) Discharge speed $v$ from spring force balance ($kx = m'\Delta v$):" + "\n"
        r"   $15,000(0.150) = 0.7069 v(v - 0) \Rightarrow v^2 = 3183 \Rightarrow \mathbf{v = 56.4\ \mathrm{m/s}}$" + "\n"
        r"3) Additional moment $M$ supported at joint $A$ ($\Sigma M_A = m' v d$):" + "\n"
        r"   $M = 15(150)(15\sin 75^\circ - 4.8\cos 75^\circ) = 2250(13.25)$" + "\n"
        r"   $\Rightarrow M = 29,800\ \mathrm{N\cdot m} \approx \mathbf{29.8\ \mathrm{kN\cdot m}}$"
    )
    ax_calc.text(5.0, 3.85, sol_text, fontsize=9.1, ha='center', va='center', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_text = (
        f"[Live Monitor ($k = 15\\ \\mathrm{{kN/m}},\\ x = {x_sp_curr*1000:.1f}\\ /\\ 150.0\\ \\mathrm{{mm}}$)]\n"
        f"Spring force: $kx = {F_curr:.0f}\\ \\mathrm{{N}}$  |  Moment arm: $d = {d_arm:.2f}\\ \\mathrm{{m}}$\n"
        f"Current: $v = {v_curr:.1f}\\ \\mathrm{{m/s}},\\ M = {M_curr/1000:.2f}\\ \\mathrm{{kN\\cdot m}}$  |  "
        f"Theoretical Values: $\\mathbf{{v = 56.4\\ \\mathrm{{m/s}},\\ M = 29.8\\ \\mathrm{{kN\\cdot m}}}}$"
    )
    ax_calc.text(5.0, 1.05, live_text, fontsize=9.1, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('Theoretical Derivation & Analysis', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_42_fire_truck_nozzle.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
