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
보충 개념 애니메이션 1: 개방링크 체인(예제 4.10) vs 유연한 밧줄(예제 4.11) 인양 시 견인력과 에너지 손실 비교
동역학 9판 (한국어판) - 제4장 4.7절 가변질량 핵심 개념 시각화
- 순수 흰색 바탕 (#ffffff), STIX 수식 폰트, 한글 $...$ 외부 분리 원칙 준수
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 동일 물리 파라미터 설정 (정확한 1:1 정량 대조)
L = 4.0         # 전체 길이 (m)
rho = 2.5       # 단위길이당 질량 (kg/m)
v = 2.0         # 일정 인양 속력 (m/s)
g = 9.81        # 중력가속도 (m/s^2)

rv2 = rho * v**2          # 10.0 N  (체인 동적 항)
half_rv2 = 0.5 * rv2      # 5.0 N   (밧줄 동적 항)

n_frames = 54
x_vals = np.concatenate([
    np.linspace(0.35, L, 44),
    np.full(10, L)
])

fig = plt.figure(figsize=(14, 6.5), dpi=120)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, figure=fig, width_ratios=[1.12, 1.08], height_ratios=[1.08, 0.92],
              left=0.04, right=0.97, top=0.87, bottom=0.09, wspace=0.18, hspace=0.34)

ax_phys = fig.add_subplot(gs[:, 0])
ax_force = fig.add_subplot(gs[0, 1])
ax_energy = fig.add_subplot(gs[1, 1])

fig.suptitle('보충 개념 1: 개방링크 체인(비탄성 충돌 손실) vs 유연한 밧줄(보존계) 인양 비교',
             fontsize=14.5, fontweight='bold', color='#1e3a5f', y=0.96)


def draw_open_chain(ax, xc, y0, y1, link_h=0.21):
    n_links = max(1, int((y1 - y0) / link_h))
    ys = np.linspace(y0 + link_h / 2, y1 - link_h / 2, n_links)
    for i, yc in enumerate(ys):
        w = 0.13 if i % 2 == 0 else 0.055
        col = '#b0bec5' if i % 2 == 0 else '#78909c'
        ax.add_patch(patches.Ellipse((xc, yc), w, link_h * 0.94,
                                     facecolor=col, edgecolor='#263238', lw=1.35, zorder=5))


def update(frame):
    x = x_vals[frame]
    rem = max(0.0, L - x)

    W_x = rho * g * x
    P_chain = W_x + rv2
    P_rope = W_x + half_rv2

    dVg = 0.5 * rho * g * x**2
    dT = 0.5 * rho * x * v**2
    dE_loss = 0.5 * rho * x * v**2
    U_chain = dVg + dT + dE_loss   # int_0^x P_chain dx
    U_rope = dVg + dT              # int_0^x P_rope dx

    # ---------------- 1. 좌측 패널: 물리 메커니즘 1:1 대조 ----------------
    ax_phys.cla()
    ax_phys.set_facecolor('#ffffff')
    ax_phys.set_xlim(-3.05, 3.15)
    ax_phys.set_ylim(-0.85, 6.15)
    ax_phys.set_aspect('equal')
    ax_phys.axis('off')

    # 바닥 플랫폼
    ax_phys.fill_between([-2.85, 2.95], -0.32, 0.0, color='#e5e0d8')
    ax_phys.plot([-2.85, 2.95], [0.0, 0.0], color='#3e2723', lw=2.2)
    ax_phys.plot([0.05, 0.05], [-0.30, 5.90], color='#cfd8dc', ls='--', lw=1.3)

    # === (A) 좌측: 예제 4.10 개방링크 체인 ===
    xc_L = -1.52
    ax_phys.text(xc_L, 5.75, '예제 4.10: 개방링크 체인\n(비탄성 미세충돌 발생)',
                 fontsize=10.0, fontweight='bold', color='#b71c1c', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.28', facecolor='#fff5f5', edgecolor='#ef9a9a', lw=1.2))

    # 잔여 체인 더미
    if rem > 0.03:
        np.random.seed(42)
        n_pile = max(2, int(20 * (rem / L)))
        for i in range(n_pile):
            px = xc_L + 0.05 + (i % 6) * 0.08 * (rem / L + 0.35)
            py = 0.05 + (i // 6) * 0.045
            ax_phys.add_patch(patches.Ellipse((px, py), 0.19, 0.075, angle=(i * 19) % 35 - 15,
                                              facecolor='#90a4ae', edgecolor='#263238', lw=1.0, zorder=3))
        # 고리 이탈 순간 비탄성 충격 스파크 표시
        if frame % 2 == 0 and x < L - 0.02:
            for ang_d in (35, 75, 115, 150):
                ar = np.radians(ang_d)
                ax_phys.plot([xc_L + 0.10 * np.cos(ar), xc_L + 0.25 * np.cos(ar)],
                             [0.08 + 0.10 * np.sin(ar), 0.08 + 0.25 * np.sin(ar)],
                             color='#ff6f00', lw=1.8, zorder=7)
        ax_phys.text(xc_L, -0.56, r'급격 가속 ($0 \to v$): $T_0 = 0$' '\n' r'손실 $\Delta E = \frac{1}{2}\rho x v^2$',
                     fontsize=9.1, fontweight='bold', color='#c62828', ha='center', va='center')
    else:
        ax_phys.text(xc_L, -0.56, r'완전 인양 완료 ($x = L$)' '\n' r'총 손실 $\Delta E = \frac{1}{2}\rho L v^2$',
                     fontsize=9.1, fontweight='bold', color='#c62828', ha='center', va='center')

    draw_open_chain(ax_phys, xc_L, 0.04, x)
    # 상단 견인력 P_chain
    ax_phys.annotate('', xy=(xc_L, x + 0.68), xytext=(xc_L, x),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=17), zorder=7)
    ax_phys.text(xc_L, x + 0.73, f'$P_{{\\mathrm{{chain}}}} = {P_chain:.1f}\\,\\mathrm{{N}}$\n$(\\rho gx + \\rho v^2)$',
                 fontsize=9.4, fontweight='bold', color='#d32f2f', ha='center', va='bottom')

    # === (B) 우측: 예제 4.11 유연한 밧줄 ===
    xc_R = 1.62
    ax_phys.text(xc_R, 5.75, '예제 4.11: 유연한 밧줄\n(매끄러운 가이드 · 보존계)',
                 fontsize=10.0, fontweight='bold', color='#0d47a1', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.28', facecolor='#f0f7ff', edgecolor='#90caf9', lw=1.2))

    # 하단 매끄러운 가이드 블록
    ax_phys.add_patch(patches.FancyBboxPatch((xc_R - 0.55, 0.02), 0.92, 0.30,
                                             boxstyle='round,pad=0.02,rounding_size=0.06',
                                             facecolor='#cfd8dc', edgecolor='#455a64', lw=1.3, zorder=2))
    # 코일 잔여분
    if rem > 0.03:
        w_coil = 0.50 * (rem / L) + 0.15
        ax_phys.plot([xc_R - 0.08 - w_coil, xc_R - 0.04], [0.15, 0.15],
                     color='#c69c6d', lw=5.5, solid_capstyle='round', zorder=4)
    # 수직 상승 연속 밧줄
    ax_phys.plot([xc_R, xc_R], [0.16, x], color='#5d4037', lw=6.5, solid_capstyle='round', zorder=4)
    ax_phys.plot([xc_R, xc_R], [0.16, x], color='#d7b186', lw=4.5, solid_capstyle='round', zorder=5)

    # 하단 장력 T_0 = 1/2 rho v^2 표시
    ax_phys.annotate('', xy=(xc_R + 0.32, 0.12), xytext=(xc_R + 0.32, 0.56),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.0, mutation_scale=13), zorder=7)
    ax_phys.text(xc_R + 0.40, 0.34, r'$T_0 = \frac{1}{2}\rho v^2$', fontsize=9.2, fontweight='bold', color='#1565c0', va='center')

    ax_phys.annotate('', xy=(xc_R, x + 0.65), xytext=(xc_R, x),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.8, mutation_scale=17), zorder=7)
    ax_phys.text(xc_R, x + 0.70, f'$P_{{\\mathrm{{rope}}}} = {P_rope:.1f}\\,\\mathrm{{N}}$\n$(\\rho gx + \\frac{{1}}{{2}}\\rho v^2)$',
                 fontsize=9.4, fontweight='bold', color='#1565c0', ha='center', va='bottom')

    ax_phys.text(xc_R, -0.56, r'연속 방향 전환: $T_0 = \frac{1}{2}\rho v^2$' '\n' r'에너지 손실 $\Delta E = 0$ (보존)',
                 fontsize=9.1, fontweight='bold', color='#0d47a1', ha='center', va='center')

    # 중앙 높이 x 치수 표시
    ax_phys.annotate('', xy=(0.05, x), xytext=(0.05, 0.0),
                     arrowprops=dict(arrowstyle='<->', color='#2e7d32', lw=1.6))
    ax_phys.text(0.05, max(0.45, x * 0.5), f'$x = {x:.2f}\\,\\mathrm{{m}}$\n$(v = {v:.1f}\\,\\mathrm{{m/s}})$',
                 fontsize=9.2, fontweight='bold', color='#2e7d32', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.18', facecolor='#ffffff', edgecolor='#a5d6a7', lw=1.0))

    # ---------------- 2. 우측 상단: 견인력 P(x) 곡선 및 차이 넓이(= 손실 에너지) ----------------
    ax_force.cla()
    ax_force.set_facecolor('#ffffff')
    xs = np.linspace(0, L, 100)
    Pc_line = rho * g * xs + rv2
    Pr_line = rho * g * xs + half_rv2

    ax_force.plot(xs, Pc_line, color='#d32f2f', lw=2.4, label=r'체인 $P_{\mathrm{chain}} = \rho gx + \rho v^2$')
    ax_force.plot(xs, Pr_line, color='#1565c0', lw=2.4, label=r'밧줄 $P_{\mathrm{rope}} = \rho gx + \frac{1}{2}\rho v^2$')
    ax_force.plot(xs, rho * g * xs, color='#78909c', ls=':', lw=1.4, label=r'정적 자중 $\rho gx$')

    xs_sub = np.linspace(0, x, 60)
    ax_force.fill_between(xs_sub, rho * g * xs_sub + half_rv2, rho * g * xs_sub + rv2,
                          color='#ffb74d', alpha=0.55, label=r'차이 넓이 $= \Delta E_{\mathrm{loss}} = \frac{1}{2}\rho x v^2$')
    ax_force.fill_between(xs_sub, 0, rho * g * xs_sub + half_rv2, color='#bbdefb', alpha=0.30)

    ax_force.plot([x, x], [0, P_chain], color='#37474f', ls='--', lw=1.2)
    ax_force.plot(x, P_chain, 'o', color='#d32f2f', markersize=6.5, zorder=5)
    ax_force.plot(x, P_rope, 'o', color='#1565c0', markersize=6.5, zorder=5)

    ax_force.set_xlim(0, L * 1.04)
    ax_force.set_ylim(0, 122)
    ax_force.set_xlabel(r'인양 높이 $x\ (\mathrm{m})$', fontsize=10, fontweight='bold')
    ax_force.set_ylabel(r'견인력 $P\ (\mathrm{N})$', fontsize=10, fontweight='bold')
    ax_force.set_title(r'인양 변위에 따른 견인력 $P(x)$ 및 외력이 한 일 $\int_0^x P\,dx$', fontsize=11, fontweight='bold', color='#1e3a5f')
    ax_force.grid(True, ls=':', alpha=0.45)
    ax_force.legend(loc='upper left', fontsize=8.4, framealpha=0.95)

    # ---------------- 3. 우측 하단: 누적 일-에너지 수지 막대 비교 ----------------
    ax_energy.cla()
    ax_energy.set_facecolor('#ffffff')

    y_pos = [1.0, 0.0]
    bar_h = 0.44

    # 위치에너지 Delta V_g (공통)
    ax_energy.barh(y_pos, [dVg, dVg], height=bar_h, color='#64b5f6', edgecolor='#1e3a5f', lw=1.1,
                   label=r'위치에너지 $\Delta V_g = \frac{1}{2}\rho gx^2$')
    # 운동에너지 Delta T (공통)
    ax_energy.barh(y_pos, [dT, dT], left=[dVg, dVg], height=bar_h, color='#81c784', edgecolor='#1b5e20', lw=1.1,
                   label=r'운동에너지 $\Delta T = \frac{1}{2}\rho xv^2$')
    # 비탄성 충돌 손실 Delta E (체인만 존재!)
    ax_energy.barh([1.0], [dE_loss], left=[dVg + dT], height=bar_h, color='#ff8a65', edgecolor='#bf360c', lw=1.2,
                   hatch='//', label=r'충돌 열·소음 손실 $\Delta E = \frac{1}{2}\rho xv^2$')

    ax_energy.text(U_chain + 5.0, 1.0,
                   f'$\\int_0^x P\\,dx = {U_chain:.1f}\\,\\mathrm{{J}}$ (손실 ${dE_loss:.1f}\\,\\mathrm{{J}}$)',
                   va='center', fontsize=9.0, fontweight='bold', color='#b71c1c')
    ax_energy.text(U_rope + 5.0, 0.0,
                   f'$\\int_0^x P\\,dx = {U_rope:.1f}\\,\\mathrm{{J}}$ (손실 $0\\,\\mathrm{{J}}$)',
                   va='center', fontsize=9.0, fontweight='bold', color='#0d47a1')

    ax_energy.set_yticks(y_pos)
    ax_energy.set_yticklabels(['개방링크 체인\n(예제 4.10)', '유연한 밧줄\n(예제 4.11)'], fontsize=9.5, fontweight='bold')
    ax_energy.set_xlim(0, 425)
    ax_energy.set_ylim(-0.55, 2.15)
    ax_energy.set_xlabel(r'누적 에너지 수지 $(\mathrm{J})$', fontsize=10, fontweight='bold')
    ax_energy.set_title(r'누적 일-에너지 비교: $\int_0^x P\,dx = \Delta V_g + \Delta T + \Delta E_{\mathrm{loss}}$',
                        fontsize=11, fontweight='bold', color='#1e3a5f')
    ax_energy.grid(True, axis='x', ls=':', alpha=0.45)
    ax_energy.legend(loc='upper left', ncol=3, fontsize=7.6, framealpha=0.95, columnspacing=0.9)


anim = FuncAnimation(fig, update, frames=n_frames, interval=75)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_chain_vs_rope_energy.gif')
anim.save(gif_path, writer='pillow', fps=14)
plt.close()
print(f'Saved: {gif_path}')
