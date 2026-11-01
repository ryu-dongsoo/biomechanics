"""
동역학 9판 제4장 4.5절: 에너지와 운동량 보존
기초문제 2 - 문제 4/18 (Problem 4/18) - 수평 궤도 위 화차 3대의 충돌·결합 후 속도 및 에너지 손실 백분율
- 순수 흰색 바탕 (#ffffff) & 교재 그림(박스카 A, 목재 평판차 B, 탱크차 C) 완벽 반영
- 정량 계산 검증:
  * [65(2) + 50(1) + 75(-1.5)] = [65 + 50 + 75] v => v = 0.355 km/h (->)
  * T_1 = 18,470 J, T_2 = 925.2 J
  * 에너지 손실 백분율 n = 100(1 - 925.2 / 18470) = 95.0 %
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
mA, mB, mC = 65.0, 50.0, 75.0       # Mg
vA0, vB0, vC0 = 2.0, 1.0, -1.5      # km/h
m_tot = mA + mB + mC                # 190.0 Mg

# 선운동량 보존: 1단계 B와 C 먼저 충돌 -> 2단계 A와 (B+C) 충돌 -> 최종 3대 일체 거동
v_final = (mA * vA0 + mB * vB0 + mC * vC0) / m_tot  # 67.5 / 190 = 0.35526 km/h
v_BC = (mB * vB0 + mC * vC0) / (mB + mC)            # -0.50 km/h (중간 단계)

T1 = 0.5 * (mA * vA0**2 + mB * vB0**2 + mC * vC0**2) * 1e3 / (3.6**2)  # 18470.3 J
T2 = 0.5 * m_tot * (v_final**2) * 1e3 / (3.6**2)                       # 925.2 J
loss_pct = 100.0 * (1.0 - T2 / T1)                                     # 95.0 %

# 차량 폭 및 초기 중심 위치 (시각화 좌표계)
car_w = 2.1
gap_init = 1.05
xB0 = 0.0
xA0 = xB0 - car_w - gap_init
xC0 = xB0 + car_w + gap_init

# 시간 스케일 (시각적 이동 시간 t in [0, 1.5])
# B(1.0)와 C(-1.5)의 상대 접근 속도는 2.5 -> t1 = gap_init / 2.5 = 0.42 에서 B-C 결합
t1 = gap_init / (vB0 - vC0)  # 0.42
# t1 시점에서 A와 B의 간격: gap_init - (vA0 - vB0)*t1 = 1.05 - 1.0*0.42 = 0.63
# 이후 A(2.0)와 BC(-0.5)의 상대 접근 속도는 2.5 -> dt2 = 0.63 / 2.5 = 0.252 -> t2 = 0.672 에서 3대 완전 결합
t2 = t1 + (gap_init - (vA0 - vB0) * t1) / (vA0 - v_BC)  # 0.672

n_frames = 56
t_vals = np.linspace(0, 1.35, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_wheels(ax, xc, y_rail):
    for dx in [-0.65, -0.38, 0.38, 0.65]:
        w = patches.Circle((xc + dx, y_rail + 0.14), 0.14, facecolor='#90a4ae', edgecolor='#263238', lw=1.5, zorder=4)
        ax.add_patch(w)
        hub = patches.Circle((xc + dx, y_rail + 0.14), 0.05, facecolor='#263238', edgecolor='none', zorder=5)
        ax.add_patch(hub)
    # 대차 프레임
    for bx in [-0.515, 0.515]:
        bogie = patches.Rectangle((xc + bx - 0.22, y_rail + 0.11), 0.44, 0.09,
                                  facecolor='#546e7a', edgecolor='#263238', lw=1.0, zorder=4)
        ax.add_patch(bogie)

def update(frame):
    t = t_vals[frame]
    if t <= t1:
        xA = xA0 + vA0 * t
        xB = xB0 + vB0 * t
        xC = xC0 + vC0 * t
        vA, vB, vC = vA0, vB0, vC0
        state_str = "충돌 전 개별 주행 중"
    elif t <= t2:
        dt = t - t1
        xA = (xA0 + vA0 * t1) + vA0 * dt
        xB = (xB0 + vB0 * t1) + v_BC * dt
        xC = xB + car_w
        vA, vB, vC = vA0, v_BC, v_BC
        state_str = r"1차 충돌 ($B$-$C$ 연결 완료)"
    else:
        dt = t - t2
        xB_t2 = (xB0 + vB0 * t1) + v_BC * (t2 - t1)
        xB = xB_t2 + v_final * dt
        xA = xB - car_w
        xC = xB + car_w
        vA = vB = vC = v_final
        state_str = r"3대 완전 연결 후 일체 주행 ($v = 0.355\ \mathrm{km/h}$)"

    T_curr = 0.5 * (mA * vA**2 + mB * vB**2 + mC * vC**2) * 1e3 / (3.6**2)

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-4.8, 4.8)
    ax_main.set_ylim(-1.2, 3.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 철도 레일 및 침목
    y_rail = -0.25
    ground = patches.Rectangle((-4.6, y_rail - 0.38), 9.2, 0.38, facecolor='#e8dfd5', edgecolor='none', zorder=1)
    ax_main.add_patch(ground)
    ax_main.plot([-4.6, 4.6], [y_rail, y_rail], color='#37474f', lw=2.5, zorder=2)
    for tx in np.linspace(-4.4, 4.4, 28):
        ax_main.plot([tx, tx], [y_rail - 0.06, y_rail], color='#4e342e', lw=2.5, zorder=2)

    # 1) 화차 A (65 Mg 박스카 - 적갈색)
    draw_wheels(ax_main, xA, y_rail)
    baseA = patches.Rectangle((xA - 0.98, y_rail + 0.28), 1.96, 1.15,
                              facecolor='#d99b96', edgecolor='#5c231e', lw=1.8, zorder=3)
    ax_main.add_patch(baseA)
    doorA = patches.Rectangle((xA - 0.28, y_rail + 0.32), 0.56, 1.05,
                              facecolor='#c57b75', edgecolor='#5c231e', lw=1.2, zorder=4)
    ax_main.add_patch(doorA)
    ax_main.text(xA, y_rail + 0.85, '65 Mg', fontsize=10, fontweight='bold', ha='center', va='center', color='#3e120e', zorder=5)
    ax_main.text(xA, y_rail - 0.62, r'$A$', fontsize=13, fontweight='bold', ha='center')

    # 2) 화차 B (50 Mg 목재 적재 평판차 - 황토색)
    draw_wheels(ax_main, xB, y_rail)
    deckB = patches.Rectangle((xB - 0.98, y_rail + 0.28), 1.96, 0.14,
                              facecolor='#b8736d', edgecolor='#4a1c17', lw=1.6, zorder=3)
    ax_main.add_patch(deckB)
    for ly in [0.42, 0.58, 0.74]:
        log_rect = patches.Rectangle((xB - 0.78, y_rail + ly), 1.56, 0.15,
                                     facecolor='#e0a98b', edgecolor='#6d4c41', lw=1.2, zorder=3)
        ax_main.add_patch(log_rect)
    for sx in [-0.45, 0.45]:
        ax_main.plot([xB + sx, xB + sx], [y_rail + 0.28, y_rail + 0.92], color='#37474f', lw=2.2, zorder=4)
    ax_main.text(xB, y_rail + 1.10, '50 Mg', fontsize=10, fontweight='bold', ha='center', va='center', color='#4e342e', zorder=5)
    ax_main.text(xB, y_rail - 0.62, r'$B$', fontsize=13, fontweight='bold', ha='center')

    # 3) 화차 C (75 Mg 탱크차 - 짙은 녹색)
    draw_wheels(ax_main, xC, y_rail)
    deckC = patches.Rectangle((xC - 0.98, y_rail + 0.28), 1.96, 0.12,
                              facecolor='#546e7a', edgecolor='#263238', lw=1.5, zorder=3)
    ax_main.add_patch(deckC)
    tankC = patches.FancyBboxPatch((xC - 0.82, y_rail + 0.42), 1.64, 0.72,
                                   boxstyle='round,pad=0.08,rounding_size=0.32',
                                   facecolor='#4b725f', edgecolor='#1b3629', lw=1.8, zorder=3)
    ax_main.add_patch(tankC)
    domeC = patches.Rectangle((xC - 0.14, y_rail + 1.20), 0.28, 0.12,
                              facecolor='#4b725f', edgecolor='#1b3629', lw=1.5, zorder=3)
    ax_main.add_patch(domeC)
    ax_main.text(xC, y_rail + 0.78, '75 Mg', fontsize=10, fontweight='bold', ha='center', va='center', color='#ffffff', zorder=5)
    ax_main.text(xC, y_rail - 0.62, r'$C$', fontsize=13, fontweight='bold', ha='center')

    # 커플러(연결기) 표현
    for cx in [xA + 0.98, xB - 0.98, xB + 0.98, xC - 0.98]:
        ax_main.plot([cx - 0.06, cx + 0.06], [y_rail + 0.34, y_rail + 0.34], color='#222222', lw=3.0, zorder=4)

    # 상단 속도 화살표 표시 (초록색 표준)
    y_arr = 1.72
    if t <= t2:
        # 개별 속도 표시
        ax_main.annotate('', xy=(xA + 0.55, y_arr), xytext=(xA - 0.55, y_arr),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14))
        ax_main.text(xA, y_arr + 0.22, f'{vA:.1f} km/h', fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')

        if t <= t1:
            ax_main.annotate('', xy=(xB + 0.48, y_arr), xytext=(xB - 0.48, y_arr),
                             arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14))
            ax_main.text(xB, y_arr + 0.22, '1 km/h', fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')

            ax_main.annotate('', xy=(xC - 0.52, y_arr), xytext=(xC + 0.52, y_arr),
                             arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14))
            ax_main.text(xC, y_arr + 0.22, '1.5 km/h', fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')
        else:
            mid_BC = 0.5 * (xB + xC)
            ax_main.annotate('', xy=(mid_BC - 0.48, y_arr), xytext=(mid_BC + 0.48, y_arr),
                             arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14))
            ax_main.text(mid_BC, y_arr + 0.22, '0.50 km/h (B+C)', fontsize=10.2, fontweight='bold', color='#2e7d32', ha='center')
    else:
        # 3대 완전 결합 후 공통 속도 v = 0.355 km/h (->)
        ax_main.annotate('', xy=(xB + 0.85, y_arr + 0.05), xytext=(xB - 0.85, y_arr + 0.05),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.8, mutation_scale=16))
        ax_main.text(xB, y_arr + 0.30, r'공통 속도 $v = 0.355\ \mathrm{km/h}\ (\rightarrow)$',
                     fontsize=11.5, fontweight='bold', color='#2e7d32', ha='center')

    ax_main.set_title('문제 4/18: 수평 궤도 위 화차 3대의 충돌·결합 및 에너지 손실', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 우측 패널: 이론 해석 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        r"1. 수평 방향 선운동량 보존 ($\sum F_x = 0 \Rightarrow G_{x1} = G_{x2}$):" "\n"
        r"  $[65(2) + 50(1) + 75(-1.5)] = [65 + 50 + 75]\,v$" "\n"
        r"  $67.5 = 190\,v \Rightarrow \mathbf{v = 0.355\ \mathrm{km/h}}\ (\rightarrow)$" "\n\n"
        r"2. 충돌 전후 운동에너지 및 백분율 에너지 손실 ($\Delta E_{\mathrm{mech}} < 0$):" "\n"
        r"  $\bullet\ T_1 = \frac{1}{2}[65(2^2) + 50(1^2) + 75(1.5^2)]\times 10^3 \left(\frac{1}{3.6}\right)^2 = 18,470\ \mathrm{J}$" "\n"
        r"  $\bullet\ T_2 = \frac{1}{2}[65 + 50 + 75]\times 10^3 \left(\frac{0.355}{3.6}\right)^2 = 925.2\ \mathrm{J}$" "\n"
        r"  $\bullet\ \eta_{\mathrm{loss}} = \frac{T_1 - T_2}{T_1}\times 100 = 100\left(1 - \frac{925.2}{18,470}\right)$" "\n"
        r"  $\quad\quad\ \ = \mathbf{95.0\%}$"
    )
    ax_calc.text(0.35, 6.0, sol_box, fontsize=9.7, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'현재 상태: {state_str}\n'
        f'계 전체 선운동량 (일정): $G_x = +67.5\\ \\mathrm{{Mg\\cdot km/h}} = +18.75\\ \\mathrm{{kN\\cdot s}}$\n'
        f'현재 총 운동에너지: $T = {T_curr:,.1f}\\ \\mathrm{{J}}$  (초기: $18,470\\ \\mathrm{{J}}$)\n'
        f'이론 최종값: $v = 0.355\\ \\mathrm{{km/h}}$,  에너지 손실률 $= 95.0\\%$'
    )
    ax_calc.text(0.35, 1.45, live_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title(r'이론 해석 및 정량 유도 ($\Delta G_x = 0$ 선운동량 보존)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_18_three_freight_cars.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
