"""
Supplementary Concept Animation 1: Pairwise Internal Force Cancellation & Smooth Mass-Center Trajectory
Dynamics 9th Ed. - Chapter 4, Sections 4.1-4.2 Generalized Newton's Second Law (Eq. 4.1)
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

masses = np.array([1.0, 2.0, 1.0])
M_tot = float(np.sum(masses))
k_sp = 32.0
L0 = 0.72

F_ext_i = np.array([
    [1.5, -1.2],
    [3.0, -2.4],
    [1.5, -1.2],
])
F_ext_tot = np.sum(F_ext_i, axis=0)
a_bar_exact = F_ext_tot / M_tot  # [1.50, -1.20] m/s^2

r_bar0 = np.array([0.0, 0.45])
v_bar0 = np.array([1.45, 2.15])

rho0 = np.array([
    [-0.58,  0.42],
    [ 0.05, -0.35],
    [ 0.48,  0.28],
])
vrel0 = np.array([
    [ 1.30,  1.10],
    [-0.25, -0.85],
    [-0.80,  0.60],
])

r0 = r_bar0 + rho0
v0 = v_bar0 + vrel0

def internal_forces(r):
    f = np.zeros((3, 2))
    pairs = [(0, 1), (1, 2), (2, 0)]
    pair_vecs = {}
    for i, j in pairs:
        diff = r[j] - r[i]
        dist = max(1e-6, np.linalg.norm(diff))
        u = diff / dist
        f_ij = k_sp * (dist - L0) * u
        f[i] += f_ij
        f[j] -= f_ij
        pair_vecs[(i, j)] = f_ij
    return f, pair_vecs

dt = 0.002
n_steps = 1400
t_sim = np.linspace(0.0, dt * n_steps, n_steps + 1)
r_hist = np.zeros((n_steps + 1, 3, 2))
v_hist = np.zeros((n_steps + 1, 3, 2))
fint_hist = np.zeros((n_steps + 1, 3, 2))

r_curr = r0.copy()
v_curr = v0.copy()
for s in range(n_steps + 1):
    r_hist[s] = r_curr
    v_hist[s] = v_curr
    f_int, _ = internal_forces(r_curr)
    fint_hist[s] = f_int
    if s < n_steps:
        def acc(rr):
            fi, _ = internal_forces(rr)
            return (F_ext_i + fi) / masses[:, None]
        k1_r, k1_v = v_curr, acc(r_curr)
        k2_r, k2_v = v_curr + 0.5*dt*k1_v, acc(r_curr + 0.5*dt*k1_r)
        k3_r, k3_v = v_curr + 0.5*dt*k2_v, acc(r_curr + 0.5*dt*k2_r)
        k4_r, k4_v = v_curr + dt*k3_v, acc(r_curr + dt*k3_r)
        r_curr = r_curr + (dt / 6.0) * (k1_r + 2*k2_r + 2*k3_r + k4_r)
        v_curr = v_curr + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)

r_bar_hist = np.sum(masses[None, :, None] * r_hist, axis=1) / M_tot
v_bar_hist = np.sum(masses[None, :, None] * v_hist, axis=1) / M_tot
f_sum_hist = np.sum(fint_hist, axis=1)

n_frames = 56
frame_idx = np.linspace(0, n_steps, n_frames, dtype=int)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.18, 1.0], height_ratios=[1.0, 1.0],
              left=0.04, right=0.97, top=0.89, bottom=0.09, wspace=0.19, hspace=0.35)

ax_2d = fig.add_subplot(gs[:, 0])
ax_f  = fig.add_subplot(gs[0, 1])
ax_v  = fig.add_subplot(gs[1, 1])

fig.suptitle("Concept Animation 1: Why Does Mass Center G Move Smoothly Despite Wild Internal Vibrations?",
             fontsize=13.5, fontweight='bold', color='#0f172a', y=0.965)

def draw_spring_line(ax, pA, pB, n_coils=7, amp=0.045):
    vec = pB - pA
    L = np.linalg.norm(vec)
    if L < 1e-4:
        return
    u = vec / L
    n = np.array([-u[1], u[0]])
    pts = [pA, pA + 0.12 * vec]
    for k in range(2 * n_coils):
        frac = 0.12 + 0.76 * (k + 0.5) / (2 * n_coils)
        pts.append(pA + frac * vec + (amp if k % 2 == 0 else -amp) * n)
    pts.extend([pA + 0.88 * vec, pB])
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color='#64748b', lw=1.6, zorder=3)

colors_p = ['#2563eb', '#16a34a', '#9333ea']

def update(frame):
    idx = frame_idx[frame]
    t = t_sim[idx]
    r_now = r_hist[idx]
    rG_now = r_bar_hist[idx]
    vG_now = v_bar_hist[idx]
    _, pair_vecs = internal_forces(r_now)

    ax_2d.clear()
    ax_f.clear()
    ax_v.clear()
    for ax in (ax_2d, ax_f, ax_v):
        ax.set_facecolor('#ffffff')

    ax_2d.set_xlim(-1.05, 11.2)
    ax_2d.set_ylim(-1.55, 5.85)
    ax_2d.set_aspect('equal')
    ax_2d.axis('off')
    ax_2d.set_title(r"1) Pairwise Cancellation ($\mathbf{f}_{ij} = -\mathbf{f}_{ji}$) & Parabolic Path of $G$",
                    fontsize=11.5, fontweight='bold', color='#1e293b', pad=6)

    ax_2d.plot([-0.8, 10.9], [-1.25, -1.25], color='#cbd5e1', lw=1.5)
    ax_2d.plot(r_bar_hist[:, 0], r_bar_hist[:, 1], color='#fda4af', ls='--', lw=1.6, zorder=1)

    for i in range(3):
        ax_2d.plot(r_hist[:idx+1, i, 0], r_hist[:idx+1, i, 1],
                   color=colors_p[i], lw=1.3, alpha=0.55, zorder=2)
    ax_2d.plot(r_bar_hist[:idx+1, 0], r_bar_hist[:idx+1, 1],
               color='#e11d48', lw=3.2, zorder=6)

    for (i, j), fij in pair_vecs.items():
        draw_spring_line(ax_2d, r_now[i], r_now[j], n_coils=6, amp=0.05)
        fmag = np.linalg.norm(fij)
        if fmag > 1.2:
            u_f = fij / fmag
            flen = min(0.42, 0.032 * fmag)
            ax_2d.annotate('', xy=r_now[i] + flen * u_f, xytext=r_now[i],
                           arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.8, mutation_scale=11), zorder=7)
            ax_2d.annotate('', xy=r_now[j] - flen * u_f, xytext=r_now[j],
                           arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.8, mutation_scale=11), zorder=7)

    radii = [0.19, 0.25, 0.19]
    lbls = [r'$m_1$', r'$m_2$', r'$m_3$']
    for i in range(3):
        c = patches.Circle(r_now[i], radii[i], facecolor=colors_p[i], edgecolor='#0f172a', lw=1.6, alpha=0.88, zorder=5)
        ax_2d.add_patch(c)
        ax_2d.text(r_now[i, 0], r_now[i, 1], lbls[i], color='white', fontsize=8.8, fontweight='bold',
                   ha='center', va='center', zorder=8)

    ax_2d.plot(rG_now[0], rG_now[1], marker='D', markersize=8.5,
               markerfacecolor='#facc15', markeredgecolor='#be123c', markeredgewidth=2.0, zorder=9)
    ax_2d.annotate('', xy=rG_now + 0.14 * F_ext_tot, xytext=rG_now,
                   arrowprops=dict(arrowstyle='->', color='#be123c', lw=2.6, mutation_scale=14), zorder=9)
    ax_2d.text(rG_now[0] + 0.15, rG_now[1] + 0.34, r'$G\ (\Sigma\mathbf{F}_{\mathrm{ext}} = m\bar{\mathbf{a}})$',
               fontsize=9.8, fontweight='bold', color='#be123c', zorder=10)

    bubble = (
        "[Student Tip] Why Doesn't G Wobble Under Strong Spring Forces?\n"
        "• Every internal spring pull ($+\\mathbf{f}_{12}$) has an equal and opposite partner ($-\\mathbf{f}_{12}$).\n"
        "• Summing over the whole system cancels all internal pairs: $(+\\mathbf{f}_{12}) + (-\\mathbf{f}_{12}) = \\mathbf{0}$!\n"
        "• Thus $G$ moves as a single mass $m$ driven ONLY by net external force: $\\Sigma\\mathbf{F}_{\\mathrm{ext}} = m\\bar{\\mathbf{a}}$!"
    )
    ax_2d.text(-0.92, 5.72, bubble, fontsize=8.7, color='#78350f', va='top', ha='left', linespacing=1.36,
               bbox=dict(boxstyle='round,pad=0.42', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_bot = (
        "Internal Sum "
        + r"$\sum \mathbf{f}_i = \mathbf{0} \;\Longrightarrow\; \sum \mathbf{F}_{\mathrm{ext}} = m\bar{\mathbf{a}}"
        + rf"\quad (m={M_tot:.0f}\ \mathrm{{kg}},\ \bar{{\mathbf{{a}}}} = +1.5\mathbf{{i}} - 1.2\mathbf{{j}}\ \mathrm{{m/s^2}})$"
    )
    ax_2d.text(5.05, -0.92, eq_bot, fontsize=9.5, color='#0f172a', ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.35', facecolor='#eff6ff', edgecolor='#60a5fa', lw=1.4))

    ax_f.set_xlim(0.0, t_sim[-1])
    ax_f.set_ylim(-16.0, 16.0)
    ax_f.set_ylabel("Internal Force x (N)", fontsize=9.5, fontweight='bold')
    ax_f.set_title(r"2) Wild Individual $f_{ix}(t)$ vs Exact Zero Sum $\sum f_{ix}(t) = 0\ \mathrm{N}$",
                   fontsize=10.2, fontweight='bold', color='#1e293b', pad=5)
    ax_f.grid(True, ls=':', alpha=0.5)
    for i in range(3):
        ax_f.plot(t_sim[:idx+1], fint_hist[:idx+1, i, 0], color=colors_p[i], lw=1.5, ls='--', alpha=0.8,
                  label=rf'$f_{{{i+1}x}}$')
    ax_f.plot(t_sim[:idx+1], f_sum_hist[:idx+1, 0], color='#e11d48', lw=2.8,
              label=r'$\sum f_{ix} = 0.00\ \mathrm{N}$')
    ax_f.plot(t, f_sum_hist[idx, 0], 'o', color='#e11d48', markersize=6)
    ax_f.legend(loc='upper right', ncol=2, fontsize=8.0)

    ax_v.set_xlim(0.0, t_sim[-1])
    ax_v.set_ylim(-0.5, 7.2)
    ax_v.set_xlabel("Time $t$ (s)", fontsize=9.5, fontweight='bold')
    ax_v.set_ylabel("Velocity x (m/s)", fontsize=9.5, fontweight='bold')
    ax_v.set_title(r"3) Smooth Linear Mass-Center Velocity $\bar{v}_x(t) = \bar{v}_{x0} + (\Sigma F_x / m)t$",
                   fontsize=10.2, fontweight='bold', color='#1e293b', pad=5)
    ax_v.grid(True, ls=':', alpha=0.5)
    for i in range(3):
        ax_v.plot(t_sim[:idx+1], v_hist[:idx+1, i, 0], color=colors_p[i], lw=1.4, ls='--', alpha=0.75,
                  label=rf'$v_{{{i+1}x}}$')
    ax_v.plot(t_sim, v_bar0[0] + a_bar_exact[0] * t_sim, color='#fda4af', lw=1.5, ls=':')
    ax_v.plot(t_sim[:idx+1], v_bar_hist[:idx+1, 0], color='#e11d48', lw=2.9,
              label=rf'$\bar{{v}}_x(t) = {vG_now[0]:.2f}\ \mathrm{{m/s}}$')
    ax_v.plot(t, vG_now[0], 'o', color='#e11d48', markersize=6)
    ax_v.legend(loc='upper left', ncol=2, fontsize=8.0)

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_cm_internal_cancel.gif")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
    anim.save(gif_path, writer='pillow', fps=13)
    plt.close(fig)
    print(f"Saved: {gif_path}")
