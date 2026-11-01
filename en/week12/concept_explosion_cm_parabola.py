"""
Meriam & Kraige Dynamics 9th Ed. Chapter 4 Section 4.5: Conservation of Energy and Momentum
Supplementary Concept Animation 1 - Parabolic Center-of-Mass Trajectory vs. Energy Jump in Midair Explosion
- Pure white background (#ffffff) & STIX math typography
- Compares momentum conservation / CM parabolic path (Σf_i = 0) vs. discontinuous mechanical energy jump (ΔE > 0)
- Highlights termination of the free-flight CM parabola rule once the first fragment strikes the ground (t > t_hit)
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

# Physical parameters (20-kg shell launched -> explodes at apex t = 4.0 s)
g = 9.81
m_tot = 20.0
ux0, uz0 = 40.0, 39.24          # m/s (apex at t_exp = uz0/g = 4.00 s)
t_exp = uz0 / g                 # 4.00 s
x_exp = ux0 * t_exp             # 160.0 m
z_exp = uz0 * t_exp - 0.5 * g * t_exp**2  # 78.48 m

# 3 fragments & post-explosion velocities (exact Σ m_i v_ix = 800 N·s, Σ m_i v_iz = 0 N·s)
m1, m2, m3 = 5.0, 9.0, 6.0
v1x, v1z = 10.0, -18.0          # m/s (strikes ground first)
v2x, v2z = 42.0, 4.0            # m/s
v3x, v3z = 62.0, 9.0            # m/s

def calc_dt_hit(vz):
    return (vz + np.sqrt(vz**2 + 2.0 * g * z_exp)) / g

dt_hit1 = calc_dt_hit(v1z)      # 2.566 s -> t_hit1 = 6.566 s
dt_hit2 = calc_dt_hit(v2z)      # 4.432 s
dt_hit3 = calc_dt_hit(v3z)      # 5.025 s
t_hit1 = t_exp + dt_hit1        # 6.566 s

t_para = np.linspace(0, 8.0, 200)
x_para = ux0 * t_para
z_para = uz0 * t_para - 0.5 * g * t_para**2

def frag_state(t, vx, vz, dt_hit):
    dt = t - t_exp
    if dt <= dt_hit:
        x = x_exp + vx * dt
        z = z_exp + vz * dt - 0.5 * g * dt**2
        vx_c, vz_c = vx, vz - g * dt
    else:
        x = x_exp + vx * dt_hit
        z = 0.0
        vx_c, vz_c = 0.0, 0.0
    return x, z, vx_c, vz_c

def system_histories(t_arr):
    Gx_list, E_list, xG_list, zG_list = [], [], [], []
    for t in t_arr:
        if t < t_exp:
            x = ux0 * t
            z = uz0 * t - 0.5 * g * t**2
            vz = uz0 - g * t
            Gx = m_tot * ux0
            T = 0.5 * m_tot * (ux0**2 + vz**2)
            V = m_tot * g * z
            xG, zG = x, z
        else:
            x1, z1, vx1, vz1 = frag_state(t, v1x, v1z, dt_hit1)
            x2, z2, vx2, vz2 = frag_state(t, v2x, v2z, dt_hit2)
            x3, z3, vx3, vz3 = frag_state(t, v3x, v3z, dt_hit3)
            xG = (m1 * x1 + m2 * x2 + m3 * x3) / m_tot
            zG = (m1 * z1 + m2 * z2 + m3 * z3) / m_tot
            Gx = m1 * vx1 + m2 * vx2 + m3 * vx3
            T = 0.5 * (m1 * (vx1**2 + vz1**2) + m2 * (vx2**2 + vz2**2) + m3 * (vx3**2 + vz3**2))
            V = g * (m1 * z1 + m2 * z2 + m3 * z3)
        Gx_list.append(Gx)
        E_list.append((T + V) / 1000.0)
        xG_list.append(xG)
        zG_list.append(zG)
    return np.array(Gx_list), np.array(E_list), np.array(xG_list), np.array(zG_list)

n_frames = 58
t_vals = np.linspace(0.0, 7.6, n_frames)
t_dense = np.linspace(0.0, 7.6, 300)
Gx_dense, E_dense, xG_dense, zG_dense = system_histories(t_dense)

fig = plt.figure(figsize=(14, 6.5))
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.25, 1.0], height_ratios=[1.0, 1.0, 1.05],
              left=0.055, right=0.965, top=0.89, bottom=0.09, wspace=0.18, hspace=0.38)

ax_traj = fig.add_subplot(gs[:, 0])
ax_mom = fig.add_subplot(gs[0, 1])
ax_erg = fig.add_subplot(gs[1, 1])
ax_note = fig.add_subplot(gs[2, 1])

def update(frame):
    t = t_vals[frame]

    ax_traj.cla()
    ax_traj.set_facecolor('#ffffff')
    ax_traj.set_xlim(-15, 395)
    ax_traj.set_ylim(-14, 108)
    ax_traj.grid(True, linestyle=':', color='#dcdcdc', lw=0.9)
    ax_traj.spines['top'].set_visible(False)
    ax_traj.spines['right'].set_visible(False)
    ax_traj.set_xlabel(r'Horizontal Distance $x\ (\mathrm{m})$', fontsize=10.5, fontweight='bold')
    ax_traj.set_ylabel(r'Altitude $z\ (\mathrm{m})$', fontsize=10.5, fontweight='bold')
    ax_traj.set_title(r'Fragment Trajectories & Parabolic Motion of Mass Center $G$', fontsize=13, fontweight='bold', pad=10)

    ground = patches.Rectangle((-15, -14), 410, 14, facecolor='#ece4db', edgecolor='none', zorder=1)
    ax_traj.add_patch(ground)
    ax_traj.plot([-15, 395], [0, 0], color='#4e342e', lw=2.0, zorder=2)

    ax_traj.plot(x_para, z_para, ls='--', lw=1.8, color='#9e9e9e', label=r'Unexploded Reference Parabola ($\mathbf{a}_G = \mathbf{g}$)', zorder=2)

    if t < t_exp:
        t_sub = np.linspace(0, t, 60)
        xs = ux0 * t_sub
        zs = uz0 * t_sub - 0.5 * g * t_sub**2
        ax_traj.plot(xs, zs, color='#c62828', lw=2.8, zorder=4, label=r'Shell / Mass Center $G$ Path')
        ax_traj.plot(xs[-1], zs[-1], 'o', color='#263238', markersize=10, zorder=6)
        ax_traj.text(xs[-1] + 8, zs[-1] + 5, r'$m = 20\ \mathrm{kg}$', fontsize=10, fontweight='bold', color='#263238')
        phase_txt = f'Pre-Explosion Flight ($t = {t:.2f}\\ \\mathrm{{s}}$)'
        phase_col = '#1565c0'
    else:
        t_pre = np.linspace(0, t_exp, 60)
        ax_traj.plot(ux0 * t_pre, uz0 * t_pre - 0.5 * g * t_pre**2, color='#c62828', lw=2.6, zorder=4)

        ax_traj.plot(x_exp, z_exp, '*', color='#ff8f00', markeredgecolor='#bf360c', markersize=16, zorder=7)
        ax_traj.text(x_exp - 6, z_exp + 7.5, r'Internal Explosion ($\sum \mathbf{f}_i = \mathbf{0}$)',
                     fontsize=9.6, fontweight='bold', color='#bf360c', ha='center',
                     bbox=dict(boxstyle='round,pad=0.16', facecolor='#fff8e1', edgecolor='#ffb74d', alpha=0.92), zorder=8)

        t_post = np.linspace(t_exp, t, 65)
        frags = [
            (m1, v1x, v1z, dt_hit1, '#1565c0', r'$m_1=5\ \mathrm{kg}$'),
            (m2, v2x, v2z, dt_hit2, '#2e7d32', r'$m_2=9\ \mathrm{kg}$'),
            (m3, v3x, v3z, dt_hit3, '#6a1b9a', r'$m_3=6\ \mathrm{kg}$'),
        ]
        xG_post, zG_post = np.zeros_like(t_post), np.zeros_like(t_post)
        for mi, vxi, vzi, dth, col, lbl in frags:
            xf_arr, zf_arr = [], []
            for tp in t_post:
                xx, zz, _, _ = frag_state(tp, vxi, vzi, dth)
                xf_arr.append(xx)
                zf_arr.append(zz)
            xf_arr, zf_arr = np.array(xf_arr), np.array(zf_arr)
            xG_post += (mi / m_tot) * xf_arr
            zG_post += (mi / m_tot) * zf_arr
            ax_traj.plot(xf_arr, zf_arr, color=col, lw=1.9, ls='-', label=lbl, zorder=4)
            ax_traj.plot(xf_arr[-1], zf_arr[-1], 'o', color=col, markersize=7.5, markeredgecolor='#ffffff', markeredgewidth=0.8, zorder=6)

        ax_traj.plot(xG_post, zG_post, color='#c62828', lw=3.0, zorder=5, label=r'Actual Mass Center $G$ ($\sum m_i \mathbf{r}_i / m$)')
        ax_traj.plot(xG_post[-1], zG_post[-1], 'D', color='#c62828', markersize=8.5, markeredgecolor='#ffffff', markeredgewidth=1.0, zorder=7)
        ax_traj.text(xG_post[-1] + 6, zG_post[-1] - 7, r'$G$', fontsize=11, fontweight='bold', color='#c62828', zorder=8)

        if t < t_hit1:
            phase_txt = f'All Fragments Airborne ($t = {t:.2f}\\ \\mathrm{{s}}$): $G$ Follows Exact Parabola!'
            phase_col = '#2e7d32'
        else:
            x1_hit = x_exp + v1x * dt_hit1
            ax_traj.axvline(x1_hit, ymin=0.12, ymax=0.52, color='#d32f2f', ls='-.', lw=1.4, zorder=3)
            ax_traj.text(x1_hit - 6, 36, r'$m_1$ Hits Ground (Ext. Force!)', fontsize=9.0, fontweight='bold',
                         color='#c62828', ha='right',
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffebee', edgecolor='#ef9a9a'), zorder=8)
            phase_txt = f'After Ground Impact ($t = {t:.2f}\\ \\mathrm{{s}} > t_{{\\mathrm{{hit}}}}$): Ground Force Deviates $G$'
            phase_col = '#c62828'

    ax_traj.text(0.02, 0.95, phase_txt, transform=ax_traj.transAxes, fontsize=9.5, fontweight='bold',
                 color=phase_col, va='top',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor=phase_col, lw=1.2, alpha=0.94), zorder=9)
    ax_traj.legend(loc='lower left', bbox_to_anchor=(0.01, 0.14), fontsize=8.4, framealpha=0.92, edgecolor='#cccccc')

    ax_mom.cla()
    ax_mom.set_facecolor('#ffffff')
    mask = t_dense <= t
    ax_mom.plot(t_dense, Gx_dense, color='#e0e0e0', lw=1.5)
    ax_mom.plot(t_dense[mask], Gx_dense[mask], color='#1565c0', lw=2.5)
    ax_mom.axvline(t_exp, color='#ff8f00', ls='--', lw=1.3)
    ax_mom.axvline(t_hit1, color='#d32f2f', ls=':', lw=1.3)
    Gx_now = np.interp(t, t_dense, Gx_dense)
    ax_mom.plot(t, Gx_now, 'o', color='#1565c0', markersize=6.5)
    ax_mom.set_xlim(0, 7.6)
    ax_mom.set_ylim(680, 860)
    ax_mom.grid(True, ls=':', color='#e0e0e0')
    ax_mom.spines['top'].set_visible(False)
    ax_mom.spines['right'].set_visible(False)
    ax_mom.set_ylabel(r'$G_x\ (\mathrm{N\cdot s})$', fontsize=9.5, fontweight='bold')
    ax_mom.set_title(r'Horizontal Momentum $G_x(t)$: Conserved Across Explosion ($\Delta G_x = 0$)', fontsize=10.4, fontweight='bold', pad=5)
    ax_mom.text(2.0, 815, r'$G_x = 800\ \mathrm{N\cdot s}$ (Const.)', fontsize=9.0, color='#1565c0', fontweight='bold', ha='center')
    ax_mom.text(t_exp + 0.08, 700, r'Explosion ($4\ \mathrm{s}$)', fontsize=8.4, color='#e65100', fontweight='bold')
    ax_mom.text(t_hit1 - 0.10, 700, r'$m_1$ Lands', fontsize=8.4, color='#c62828', fontweight='bold', ha='right')

    ax_erg.cla()
    ax_erg.set_facecolor('#ffffff')
    ax_erg.plot(t_dense, E_dense, color='#e0e0e0', lw=1.5)
    ax_erg.plot(t_dense[mask], E_dense[mask], color='#2e7d32', lw=2.5)
    ax_erg.axvline(t_exp, color='#ff8f00', ls='--', lw=1.3)
    ax_erg.axvline(t_hit1, color='#d32f2f', ls=':', lw=1.3)
    E_now = np.interp(t, t_dense, E_dense)
    ax_erg.plot(t, E_now, 'o', color='#2e7d32', markersize=6.5)
    ax_erg.set_xlim(0, 7.6)
    ax_erg.set_ylim(28, 40.5)
    ax_erg.grid(True, ls=':', color='#e0e0e0')
    ax_erg.spines['top'].set_visible(False)
    ax_erg.spines['right'].set_visible(False)
    ax_erg.set_xlabel(r'Time $t\ (\mathrm{s})$', fontsize=9.5, fontweight='bold')
    ax_erg.set_ylabel(r'$E_{\mathrm{mech}}\ (\mathrm{kJ})$', fontsize=9.5, fontweight='bold')
    ax_erg.set_title(r'Mechanical Energy $T + V_g$: Jumps Upward via Chemical Work ($\Delta E > 0$)', fontsize=10.3, fontweight='bold', pad=5)
    ax_erg.annotate(r'$\Delta E = +4.85\ \mathrm{kJ}\uparrow$', xy=(t_exp, 36.24), xytext=(t_exp + 0.55, 37.2),
                    fontsize=8.8, fontweight='bold', color='#bf360c',
                    arrowprops=dict(arrowstyle='->', color='#bf360c', lw=1.3))

    ax_note.cla()
    ax_note.set_facecolor('#ffffff')
    ax_note.set_xlim(0, 10)
    ax_note.set_ylim(0, 10)
    ax_note.axis('off')

    summary_txt = (
        r"[Key Principle Summary: Why Momentum Holds While Energy Jumps]" "\n"
        r"$\bullet$ Internal Force Cancellation ($\sum \mathbf{f}_i = \mathbf{0}$): While all fragments are airborne," "\n"
        r"   only gravity acts externally, so $\Delta G_x = 0$ and $G$ tracks the exact original parabola." "\n"
        r"$\bullet$ Positive Internal Work ($U'_{1-2,\mathrm{int}} > 0$): Chemical explosion converts internal energy" "\n"
        r"   into kinetic energy, so $\Delta T + \Delta V = 0$ does NOT apply across the explosion!" "\n"
        r"$\bullet$ Caution: Once any fragment hits the ground ($t > 6.57\ \mathrm{s}$), ground reaction ends free flight."
    )
    ax_note.text(0.15, 5.0, summary_txt, fontsize=8.7, va='center', linespacing=1.33,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fff8e1', edgecolor='#ffb300', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_explosion_cm_parabola.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
