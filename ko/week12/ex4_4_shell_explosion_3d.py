# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 유동수 (Dongsoo Ryu). All rights reserved.
#   - 소속 (Affiliation) : 전북대학교 생물산업기계공학과
#                          (Dept. of Bioindustrial Machinery Engineering,
#                           Jeonbuk National University)
#   - 성명 (Author)      : 유동수 (Dongsoo Ryu)
#   - 이메일 (Contact)   : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - 교과목 (Course)    : 생물역학 (Biomechanics)
# =============================================================================

"""
동역학 9판 제4장 4.5절: 에너지와 운동량 보존
예제 4.4 (Sample Problem 4/4) - 궤도 최고점에서 폭발하는 20 kg 파열탄의 3차원 선운동량 보존 해석
- 순수 흰색 바탕 (#ffffff) & 교재 3차원 투영 원도 완벽 구현
- 정량 계산 검증:
  * 최고점 P 도달 시간 t = 24.5 s, 고도 h = 2940 m
  * v_A = 99.0 k m/s, v_B = 163.5(i cos 45° + j sin 45°) m/s
  * v_C = 427 i - 173.4 j - 82.5 k m/s (v_C = 468 m/s)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 상수 및 문제 조건
m_total = 20.0
m_A, m_B, m_C = 5.0, 9.0, 6.0
u = 300.0
g = 9.81
ux = u * (3.0 / 5.0)   # 180.0 m/s
uz = u * (4.0 / 5.0)   # 240.0 m/s

t_apex = uz / g            # 24.465 -> 24.5 s
h_apex = uz**2 / (2 * g)   # 2935.8 -> 2940 m
x_apex = ux * t_apex       # 4403.7 m

h_A = 500.0
vA_mag = np.sqrt(2 * g * h_A)            # 99.0 m/s
s_B = 4000.0
vB_mag = s_B / 24.5                      # 163.5 m/s
vBx = vB_mag * np.cos(np.radians(45.0))  # 115.6 m/s
vBy = vB_mag * np.sin(np.radians(45.0))  # 115.6 m/s

vCx = (20.0 * 180.0 - 9.0 * vBx) / 6.0   # 426.6 -> 427 m/s
vCy = (-9.0 * vBy) / 6.0                 # -173.4 m/s
vCz = (-5.0 * 99.0) / 6.0                # -82.5 m/s
vC_mag = np.sqrt(427.0**2 + 173.4**2 + 82.5**2)  # 468 m/s

def proj3d(x, y, z):
    xs, ys, zs = x / 1000.0, y / 1000.0, z / 1000.0
    px = 0.85 * xs + 0.55 * ys
    py = -0.28 * xs + 0.32 * ys + 1.05 * zs
    return np.array([px, py])

n_frames = 56
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.4, 9.2)
    ax_main.set_ylim(-2.6, 4.3)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    pO = proj3d(0, 0, 0)
    px_end = proj3d(8200, 0, 0)
    py_end = proj3d(0, 3800, 0)
    pz_end = proj3d(0, 0, 3400)

    ax_main.plot([pO[0], px_end[0]], [pO[1], px_end[1]], color='#444444', ls='--', lw=1.3)
    ax_main.plot([pO[0], py_end[0]], [pO[1], py_end[1]], color='#444444', ls='--', lw=1.3)
    ax_main.plot([pO[0], pz_end[0]], [pO[1], pz_end[1]], color='#444444', ls='--', lw=1.3)
    ax_main.text(px_end[0] + 0.15, px_end[1] - 0.08, r'$x$', fontsize=12, fontweight='bold')
    ax_main.text(py_end[0] + 0.12, py_end[1] + 0.08, r'$y$', fontsize=12, fontweight='bold')
    ax_main.text(pz_end[0], pz_end[1] + 0.15, r'$z$', fontsize=12, fontweight='bold', ha='center')
    ax_main.text(pO[0] - 0.25, pO[1] - 0.22, r'$O$', fontsize=12, fontweight='bold')

    pP = proj3d(x_apex, 0, h_apex)
    pP0 = proj3d(x_apex, 0, 0)
    xQ = x_apex + s_B * np.cos(np.radians(45.0))
    yQ = s_B * np.sin(np.radians(45.0))
    pQ = proj3d(xQ, yQ, 0)

    ax_main.plot([pP0[0], pP[0]], [pP0[1], pP[1]], color='#666666', ls='-.', lw=1.2)
    ax_main.text(0.5*(pP0[0]+pP[0]) - 0.28, 0.5*(pP0[1]+pP[1]), r'$h = 2940\ \mathrm{m}$',
                 fontsize=10, fontweight='bold', color='#333333', ha='right')

    ax_main.plot([pP0[0], pQ[0]], [pP0[1], pQ[1]], color='#777777', ls='--', lw=1.2)
    mid_PQ = 0.5 * (pP0 + pQ)
    ax_main.text(mid_PQ[0] + 0.25, mid_PQ[1] - 0.22, '4000 m', fontsize=10.5, fontweight='bold', color='#333333')
    ax_main.text(pP0[0] + 0.95, pP0[1] - 0.15, r'$45^\circ$', fontsize=10, fontweight='bold', color='#333333')
    ax_main.plot(pQ[0], pQ[1], 'kx', markersize=7, mew=1.8)
    ax_main.text(pQ[0] + 0.18, pQ[1] - 0.18, r'$Q$', fontsize=12, fontweight='bold')

    p_u_tip = proj3d(1300, 0, 1733)
    ax_main.annotate('', xy=p_u_tip, xytext=pO,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=14))
    ax_main.text(p_u_tip[0] - 0.65, p_u_tip[1] + 0.28, r'$u = 300\ \mathrm{m/s}$ (3:4:5)',
                 fontsize=10.5, fontweight='bold', color='#1565c0', ha='center',
                 bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.85))

    t_up_all = np.linspace(0, t_apex, 40)
    pts_up_all = np.array([proj3d(ux * t, 0, uz * t - 0.5 * g * t**2) for t in t_up_all])
    ax_main.plot(pts_up_all[:, 0], pts_up_all[:, 1], color='#cccccc', ls=':', lw=1.5)

    if frame < 24:
        t_curr = (frame / 23.0) * t_apex
        pts_up = np.array([proj3d(ux * t, 0, uz * t - 0.5 * g * t**2) for t in np.linspace(0, t_curr, 25)])
        ax_main.plot(pts_up[:, 0], pts_up[:, 1], color='#d84315', lw=2.5)
        shell_pos = pts_up[-1]
        ax_main.plot(shell_pos[0], shell_pos[1], 'o', color='#1d4564', markersize=9)
        ax_main.text(shell_pos[0] - 0.2, shell_pos[1] + 0.25, '20 kg 파열탄', fontsize=10, fontweight='bold', color='#1d4564')
        phase_str = f'최고점 $P$ 향해 비행 중 ($t = {t_curr:.1f}\\ /\\ 24.5\\ \\mathrm{{s}}$)'
    else:
        ax_main.plot(pts_up_all[:, 0], pts_up_all[:, 1], color='#d84315', lw=2.2)
        dt_post = ((frame - 24) / (n_frames - 25)) * 14.0

        ax_main.plot(pP[0], pP[1], '*', color='#ff6f00', markersize=14, zorder=6)
        ax_main.text(pP[0] - 0.28, pP[1] - 0.12, r'$P$', fontsize=12, fontweight='bold', color='#bf360c')

        t_B_all = np.linspace(0, t_apex, 35)
        pts_B_all = np.array([proj3d(x_apex + vBx * t, vBy * t, h_apex - 0.5 * g * t**2) for t in t_B_all])
        ax_main.plot(pts_B_all[:, 0], pts_B_all[:, 1], color='#ef6c00', ls='--', lw=1.4, alpha=0.6)

        t_arr = np.linspace(0, max(0.2, dt_post), 25)
        pts_A = np.array([proj3d(x_apex, 0, h_apex + vA_mag * t - 0.5 * g * t**2) for t in t_arr])
        pts_B = np.array([proj3d(x_apex + vBx * t, vBy * t, h_apex - 0.5 * g * t**2) for t in t_arr])
        pts_C = np.array([proj3d(x_apex + vCx * t, vCy * t, max(0.0, h_apex + vCz * t - 0.5 * g * t**2)) for t in t_arr])
        pts_G = np.array([proj3d(x_apex + ux * t, 0, h_apex - 0.5 * g * t**2) for t in t_arr])

        ax_main.plot(pts_A[:, 0], pts_A[:, 1], color='#1e88e5', lw=2.2)
        ax_main.plot(pts_B[:, 0], pts_B[:, 1], color='#ef6c00', lw=2.2)
        ax_main.plot(pts_C[:, 0], pts_C[:, 1], color='#8e24aa', lw=2.2)
        ax_main.plot(pts_G[:, 0], pts_G[:, 1], color='#2e7d32', ls=':', lw=2.0)

        pA_curr, pB_curr, pC_curr, pG_curr = pts_A[-1], pts_B[-1], pts_C[-1], pts_G[-1]
        ax_main.plot(pA_curr[0], pA_curr[1], 'o', color='#1e88e5', markersize=7.5)
        ax_main.plot(pB_curr[0], pB_curr[1], 'o', color='#ef6c00', markersize=8.5)
        ax_main.plot(pC_curr[0], pC_curr[1], 'o', color='#8e24aa', markersize=8.0)
        ax_main.plot(pG_curr[0], pG_curr[1], 's', color='#2e7d32', markersize=6.0)

        ax_main.annotate('', xy=pP + np.array([0, 0.78]), xytext=pP,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0, mutation_scale=12))
        ax_main.text(pP[0] + 0.12, pP[1] + 0.82, r'$\mathbf{v}_A\ (5\ \mathrm{kg})$', fontsize=9.8, fontweight='bold', color='#1e88e5')

        ax_main.annotate('', xy=pP + np.array([0.85, 0.08]), xytext=pP,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0, mutation_scale=12))
        ax_main.text(pP[0] + 0.90, pP[1] + 0.12, r'$\mathbf{v}_B\ (9\ \mathrm{kg})$', fontsize=9.8, fontweight='bold', color='#ef6c00')

        ax_main.annotate('', xy=pP + np.array([0.75, -0.58]), xytext=pP,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
        ax_main.text(pP[0] + 0.82, pP[1] - 0.65, r'$\mathbf{v}_C = 468\ \mathrm{m/s}\ (6\ \mathrm{kg})$',
                     fontsize=9.8, fontweight='bold', color='#8e24aa')

        ax_main.text(pG_curr[0] - 0.12, pG_curr[1] - 0.30, r'질량중심 $G$ 궤적', fontsize=9.2, fontweight='bold', color='#2e7d32', ha='right',
                     bbox=dict(boxstyle='round,pad=0.12', facecolor='#ffffff', edgecolor='none', alpha=0.85))
        phase_str = f'최고점 $P$ 폭발 후 3파편 분리 (폭발 후 $+{dt_post:.1f}\\ \\mathrm{{s}}$)'

    ax_main.set_title(r'예제 4.4: 궤도 최고점 $P$에서 폭발하는 $20\ \mathrm{kg}$ 파열탄 (3D)', fontsize=13.3, fontweight='bold', pad=12)

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        "1. 최고점 $P$ 도달 시간($t$) 및 파편 $A, B$ 초기 속도:\n"
        r"  $\bullet\ t = \frac{u_z}{g} = \frac{300(4/5)}{9.81} = 24.5\ \mathrm{s},\quad h = \frac{u_z^2}{2g} = 2940\ \mathrm{m}$" "\n"
        r"  $\bullet\ v_A = \sqrt{2gh_A} = \sqrt{2(9.81)(500)} = 99.0\ \mathrm{m/s}\ (+\mathbf{k})$" "\n"
        r"  $\bullet\ v_B = \frac{s}{t} = \frac{4000}{24.5} = 163.5\ \mathrm{m/s}\ (\mathbf{i}\cos 45^\circ + \mathbf{j}\sin 45^\circ)$" "\n\n"
        r"2. 폭발 전후 3차원 선운동량 보존 ($\mathbf{G}_1 = \mathbf{G}_2$):" "\n"
        r"  $m\mathbf{v} = m_A\mathbf{v}_A + m_B\mathbf{v}_B + m_C\mathbf{v}_C$" "\n"
        r"  $20(300)\left(\frac{3}{5}\right)\mathbf{i} = 5(99.0\mathbf{k}) + 9(163.5)(\mathbf{i}\cos 45^\circ + \mathbf{j}\sin 45^\circ) + 6\mathbf{v}_C$" "\n"
        r"  $6\mathbf{v}_C = 2560\mathbf{i} - 1040\mathbf{j} - 495\mathbf{k}$" "\n"
        r"  $\mathbf{v}_C = \mathbf{427\mathbf{i} - 173.4\mathbf{j} - 82.5\mathbf{k}\ \mathrm{m/s}}$" "\n"
        r"  $\mathbf{v_C = \sqrt{(427)^2 + (173.4)^2 + (82.5)^2} = 468\ \mathrm{m/s}}$"
    )
    ax_calc.text(0.35, 6.1, sol_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'현재 상태: {phase_str}\n'
        f'폭발 전 총 선운동량: $\\mathbf{{G}}_1 = 3600\\mathbf{{i}}\\ \\mathrm{{kg\\cdot m/s}}$\n'
        f'폭발 직후 파편 $A, B$ 속력: $v_A = 99.0\\ \\mathrm{{m/s}},\\ v_B = 163.5\\ \\mathrm{{m/s}}$\n'
        f'이론 최종값 (파편 $C$): $\\mathbf{{v}}_C = 427\\mathbf{{i}} - 173.4\\mathbf{{j}} - 82.5\\mathbf{{k}}\\ \\mathrm{{m/s}}\\ (468\\ \\mathrm{{m/s}})$'
    )
    ax_calc.text(0.35, 1.5, live_box, fontsize=9.7, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title(r'이론 해석 및 정량 유도 ($\mathbf{G}_1 = \mathbf{G}_2$ 선운동량 보존)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_4_shell_explosion_3d.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
