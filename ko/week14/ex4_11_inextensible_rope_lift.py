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
동역학 9판 제4장 질점계의 운동역학 (4.7 가변질량)
예제 4.11 (Sample Problem 4/11) - 유연하고 신장성 없는 밧줄/자전거 체인의 보존계 인양 동역학
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (회전 구속 가이드 omega = v/r 모델 포함)
- 이론 검증 결과:
  * 보존계 견인력 P(x) = rho*g*x + 1/2*rho*v^2
  * 바닥 반력 R(x) = rho*g*(L - x) + 1/2*rho*v^2
  * 하단 가이드 천이 장력 T_0 = 1/2*rho*v^2, 가이드 반력 F = 1/2*rho*v^2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 정량 파라미터
L = 4.0         # 로프 전체 길이 (m)
rho = 2.5       # 단위길이당 질량 (kg/m)
v = 2.0         # 일정 상승 속도 (m/s)
g = 9.81        # 중력가속도 (m/s^2)

n_frames = 50
x_vals = np.linspace(0.4, L - 0.1, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def update(frame):
    x = x_vals[frame]
    T0 = 0.5 * rho * v**2
    P_curr = rho * g * x + T0
    W_rem = rho * g * (L - x)
    R_curr = W_rem + T0
    U_P = 0.5 * rho * g * x**2 + 0.5 * rho * v**2 * x
    dT = 0.5 * rho * x * v**2
    dVg = 0.5 * rho * g * x**2

    # ---------------- 1. 메인 뷰 (교재 원도 1:1 - 연속 로프 및 하단 구속 가이드) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.8, 2.8)
    ax_main.set_ylim(-0.9, 5.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 바닥 지지 평판
    plat_rect = patches.Rectangle((-1.9, -0.35), 3.8, 0.35, facecolor='#e5d8c8', edgecolor='#5d4037', lw=1.8)
    ax_main.add_patch(plat_rect)
    ax_main.plot([-2.0, 2.0], [0.0, 0.0], color='#3e2723', lw=2.4)

    # 바닥 코일 (남은 로프 L - x 를 양쪽 적층 단면 코일로 표현 - 교재 중앙/우측 원도 반영)
    rem_ratio = (L - x) / L
    n_coils = max(1, int(5 * rem_ratio))
    for i in range(n_coils):
        cy = 0.06 + i * 0.09
        ax_main.add_patch(patches.Circle((-0.38, cy), 0.042, facecolor='#e6c29f', edgecolor='#6d4c41', lw=1.3))
        ax_main.add_patch(patches.Circle((+0.38, cy), 0.042, facecolor='#e6c29f', edgecolor='#6d4c41', lw=1.3))

    # 하단 구속 가이드 하우징 및 회전 롤러 (교재 우하단 원도 omega = v/r 반영)
    guide_housing = patches.Polygon([[-0.32, 0.0], [-0.32, 0.38], [-0.08, 0.38], [-0.08, 0.0]],
                                    facecolor='#cfd8dc', edgecolor='#455a64', lw=1.4, zorder=3)
    guide_housing_r = patches.Polygon([[0.08, 0.0], [0.08, 0.38], [0.32, 0.38], [0.32, 0.0]],
                                      facecolor='#cfd8dc', edgecolor='#455a64', lw=1.4, zorder=3)
    ax_main.add_patch(guide_housing)
    ax_main.add_patch(guide_housing_r)

    # 회전 가이드 캠/원통 (중심 (0, 0.22), 반경 0.16)
    cam = patches.Circle((0.0, 0.22), 0.16, facecolor='#f5d6ba', edgecolor='#5d4037', lw=1.6, zorder=4)
    ax_main.add_patch(cam)
    ang_rot = frame * 18.0
    rad_rot = np.radians(ang_rot)
    ax_main.plot([0.0, 0.12 * np.cos(rad_rot)], [0.22, 0.22 + 0.12 * np.sin(rad_rot)], color='#5d4037', lw=1.8, zorder=5)
    ax_main.text(0.48, 0.22, r'구속 가이드 ($\omega = v/r$)' '\n' r'무손실 연속 천이 ($\Delta E = 0$)',
                 fontsize=9.5, color='#37474f', fontweight='bold', va='center')

    # 수직 상승 중인 유연 비신장 로프 본체 (두께 있는 연속 띠)
    rope_rect = patches.Rectangle((-0.055, 0.22), 0.11, x - 0.22,
                                  facecolor='#e6c29f', edgecolor='#5d4037', lw=1.8, zorder=4)
    ax_main.add_patch(rope_rect)

    # 상단 견인력 P 화살표
    ax_main.annotate('', xy=(0.0, x + 0.85), xytext=(0.0, x),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, x + 0.52, f'$P = \\rho gx + \\frac{{1}}{{2}}\\rho v^2$\n$({P_curr:.1f}\\ \\mathrm{{N}})$',
                 color='#d32f2f', fontsize=11, fontweight='bold', va='center')

    # 바닥 평판 반력 R 화살표 (하단에서 상향 작용)
    ax_main.annotate('', xy=(0.0, 0.0), xytext=(0.0, -0.78),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=18))
    ax_main.text(0.18, -0.62, f'$R = \\rho g(L-x) + \\frac{{1}}{{2}}\\rho v^2 = {R_curr:.1f}\\ \\mathrm{{N}}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold', va='center')

    # 속도 벡터 v (초록색)
    v_y = max(0.75, x * 0.55)
    ax_main.annotate('', xy=(-0.55, v_y + 0.65), xytext=(-0.55, v_y),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=15))
    ax_main.text(-0.70, v_y + 0.32, f'$v = {v:.1f}\\ \\mathrm{{m/s}}$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right', va='center')

    # 치수선 x
    ax_main.plot([-1.55, -0.15], [x, x], color='#616161', lw=1.0)
    ax_main.plot([-1.55, -0.15], [0.0, 0.0], color='#616161', lw=1.0)
    ax_main.annotate('', xy=(-1.35, x), xytext=(-1.35, 0.0),
                     arrowprops=dict(arrowstyle='<->', color='#212121', lw=1.4))
    ax_main.text(-1.48, x / 2.0, f'$x = {x:.2f}\\ \\mathrm{{m}}$',
                 fontsize=11, fontweight='bold', ha='right', va='center', color='#212121')

    ax_main.set_title('예제 4.11: 유연 비신장 로프/체인의 보존계 인양', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. 우측 패널 (분리 자유물체도 & 일-에너지/운동량 유도) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단 FBD 박스 (교재 우측 원도: 상부 수직 로프 T0 vs 하부 코일+가이드 F, R)
    fbd_box = patches.FancyBboxPatch((0.3, 6.45), 9.4, 3.25, boxstyle='round,pad=0.2',
                                     facecolor='#ffffff', edgecolor='#cfd8dc', lw=1.3)
    ax_calc.add_patch(fbd_box)
    ax_calc.text(5.0, 9.42, '[분리 자유물체도] 수직 상승부 (장력 $T_0$) & 하단 구속 가이드부 (반력 $R$)',
                 fontsize=10.0, fontweight='bold', ha='center', color='#1e3a5f')

    # 좌측: 수직 상승부 FBD
    ax_calc.add_patch(patches.Rectangle((2.2, 7.35), 0.20, 1.45, facecolor='#e6c29f', edgecolor='#5d4037', lw=1.5))
    ax_calc.annotate('', xy=(2.30, 9.28), xytext=(2.30, 8.80),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.48, 9.05, r'$P$', color='#d32f2f', fontsize=10.5, fontweight='bold')
    ax_calc.annotate('', xy=(2.30, 7.75), xytext=(2.30, 8.35),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.50, 8.05, r'$\rho gx$', color='#d32f2f', fontsize=10, fontweight='bold')
    ax_calc.annotate('', xy=(2.30, 6.80), xytext=(2.30, 7.35),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(2.50, 6.95, r'$T_0 = \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.text(1.30, 8.05, '상승 구간\n($\dot{v}=0$ 평형)', fontsize=9.2, ha='center', va='center', fontweight='bold')

    # 우측: 하단 가이드 및 코일부 FBD
    ax_calc.add_patch(patches.Rectangle((6.4, 7.15), 0.90, 0.55, facecolor='#cfd8dc', edgecolor='#455a64', lw=1.5))
    ax_calc.annotate('', xy=(6.85, 8.35), xytext=(6.85, 7.70),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 8.10, r'$T_0 = \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.5, fontweight='bold')
    ax_calc.annotate('', xy=(7.30, 7.42), xytext=(8.05, 7.42),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.0))
    ax_calc.text(8.12, 7.42, r'가이드 힘 $F = \frac{1}{2}\rho v^2$', color='#1565c0', fontsize=9.2, fontweight='bold', va='center')
    ax_calc.annotate('', xy=(6.85, 7.15), xytext=(6.85, 6.58),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.0))
    ax_calc.text(7.05, 6.72, r'$R = \rho g(L-x) + \frac{1}{2}\rho v^2$', color='#d32f2f', fontsize=9.2, fontweight='bold')
    ax_calc.text(5.45, 7.45, '하단 코일\n& 가이드', fontsize=9.2, ha='center', va='center', fontweight='bold')

    # 중앙 카드: 보존계 일-에너지 및 운동량 유도
    sol_text = (
        r"■ 보존계 일-에너지 방정식 ($dU' = dT + dV_g,\ \Delta E = 0$):" "\n"
        r"  $\bullet\ P\,dx = d\left(\frac{1}{2}\rho xv^2\right) + d\left(\rho gx\frac{x}{2}\right) \Rightarrow \mathbf{P = \rho gx + \frac{1}{2}\rho v^2}$" "\n"
        r"■ 전체 로프 충격량-운동량 방정식 ($\Sigma F_x = \dot{G}_x$):" "\n"
        r"  $\bullet\ P + R - \rho gL = \frac{d}{dt}(\rho xv) = \rho v^2 \Rightarrow \left(\rho gx + \frac{1}{2}\rho v^2\right) + R - \rho gL = \rho v^2$" "\n"
        r"  $\bullet\ $이론 최종값: $\mathbf{R = \rho g(L - x) + \frac{1}{2}\rho v^2},\quad T_0 = P - \rho gx = \frac{1}{2}\rho v^2$"
    )
    ax_calc.text(0.35, 4.30, sol_text, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드: 실시간 물리량 모니터
    live_text = (
        f"[실시간 정량 모니터: $L={L:.1f}\\ \\mathrm{{m}},\\ \\rho={rho:.1f}\\ \\mathrm{{kg/m}},\\ v={v:.1f}\\ \\mathrm{{m/s}}$]\n"
        f"• 필요 견인력: $P(x) = {P_curr:.1f}\\ \\mathrm{{N}}$ (개방링크 체인 대비 $-\\frac{{1}}{{2}}\\rho v^2 = -{T0:.1f}\\ \\mathrm{{N}}$ 감소)\n"
        f"• 바닥 평판 반력: $R(x) = {R_curr:.1f}\\ \\mathrm{{N}}$ (잔여 자중 ${W_rem:.1f}\\ \\mathrm{{N}} + $ 가이드 반력 ${T0:.1f}\\ \\mathrm{{N}}$)\n"
        f"• 에너지 보존 검증: $U_{{1-2}} = {U_P:.1f}\\ \\mathrm{{J}} = \\Delta T({dT:.1f}\\ \\mathrm{{J}}) + \\Delta V_g({dVg:.1f}\\ \\mathrm{{J}})$ (손실 $0\\ \\mathrm{{J}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('일-에너지 해석 및 정량 검증', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_11_inextensible_rope_lift.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
