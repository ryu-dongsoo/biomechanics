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
연습문제 3/142: 75 g 탄알의 50 kg 카트 수평 충돌 및 역학적 에너지 손실 해석
동역학 9판 (한국어판) - 제3장 3.9절 선형 충격량과 선형 운동량

문제 조건:
- 탄알 질량 m = 75 g = 0.075 kg, 초기 수평 속도 v1 = 600 m/s (오른쪽 방향)
- 바퀴 달린 카트 질량 M = 50 kg (수평면 위 초기 정지 상태, 구름 저항 무시)
- 탄알이 카트에 박혀 함께 이동 (완전 비탄성 충돌)

이론 해석 결과:
- 충돌 직후 공통 속도: vf = 0.075(600) / (50 + 0.075) = 0.899 m/s
- 손실된 역학적 에너지: |ΔE| = T1 - T2 = 13,500 - 20.2 = 13,480 J (손실률 n = 99.9%)
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

m = 0.075
v0 = 600.0
M = 50.0
M_tot = M + m             # 50.075 kg
G_init = m * v0           # 45.0 N·s
vf = G_init / M_tot       # 0.89865 -> 0.899 m/s

T1 = 0.5 * m * (v0 ** 2)        # 13,500 J
T2 = 0.5 * M_tot * (vf ** 2)    # 20.22 J
delta_E = T1 - T2               # 13,479.8 -> 13,480 J
loss_pct = (delta_E / T1) * 100.0  # 99.85% -> 99.9%

n_frames = 72
t_arr = np.linspace(-0.50, 0.55, n_frames)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.22, 1.0], height_ratios=[0.95, 1.05],
              left=0.03, right=0.97, top=0.87, bottom=0.08, wspace=0.18, hspace=0.33)

ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])

fig.suptitle("문제 3/142: 75 g 탄알-50 kg 카트 비탄성 충돌 및 에너지 손실 해석",
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

    # =====================================================
    # [좌측 패널] 교재 원도 1:1 탄알 우향 비행 -> 충돌 -> 일체화 구름 운동
    # =====================================================
    ax1.set_xlim(-1.32, 1.56)
    ax1.set_ylim(-0.30, 1.18)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("교재 그림 1:1 충돌 시뮬레이션 (수평 외력 = 0 → 선형 운동량 보존)",
                  fontsize=12, fontweight='bold', color='#1e293b', pad=6)

    # 지면 및 하부 단면 그라데이션 음영 (교재 원도 재현)
    ax1.fill_between([-1.26, 1.50], -0.16, 0.0, color='#dfd9d2', zorder=1)
    ax1.plot([-1.26, 1.50], [0.0, 0.0], color='#1e293b', lw=2.4, zorder=3)

    cart_w, cart_h = 0.68, 0.36
    cart_y0 = 0.055
    bullet_y = 0.235
    cart_x0 = 0.52

    if t < 0.0:
        # 탄알이 왼쪽(-0.92)에서 카트 왼쪽 면(0.18)으로 매끄럽게 우향 비행!
        prog = (t + 0.50) / 0.50
        cart_x = cart_x0
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = -0.92 + prog * (cart_left - (-0.92))
        phase_str = f"충돌 전: 탄알 우향 접근 ($v_1 = {v0:.0f}\\ \\mathrm{{m/s}}$, 카트 정지)"
        phase_col = '#1d4ed8'
    elif t <= 0.035:
        cart_x = cart_x0 + 0.02 * (t / 0.035)
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = cart_left + 0.14 * (t / 0.035)
        phase_str = "충돌 순간! 탄알 관입 및 마찰열·소성변형 발생"
        phase_col = '#e11d48'
        for r_fl, col_fl, al in [(0.13, '#fde047', 0.55), (0.075, '#f97316', 0.80)]:
            ax1.add_patch(patches.Circle((cart_left, bullet_y), r_fl, facecolor=col_fl, edgecolor='none', alpha=al, zorder=7))
    else:
        prog_post = (t - 0.035) / (0.55 - 0.035)
        cart_x = cart_x0 + 0.02 + prog_post * 0.42
        cart_left = cart_x - cart_w / 2.0
        b_tip_x = cart_left + 0.22
        phase_str = f"충돌 후: 탄알+카트 일체화 우향 구름 운동 ($v_f = {vf:.3f}\\ \\mathrm{{m/s}}$)"
        phase_col = '#0ca678'

    # 주황색 파선 탄도 궤적선 (교재 원도 동일)
    ax1.plot([-1.20, cart_x - cart_w / 2.0], [bullet_y, bullet_y],
             color='#f97316', ls=(0, (7, 5)), lw=2.0, zorder=2)

    # 카트 바퀴 2개 (카트 몸체 뒤쪽에 반원이 보이도록 배치 — 교재 원도 1:1)
    r_w = 0.072
    for wx_off in [-0.20, 0.20]:
        wc = (cart_x + wx_off, r_w)
        ax1.add_patch(patches.Circle(wc, r_w, facecolor='#bae6fd', edgecolor='#1e293b', lw=1.8, zorder=2.5))
        ax1.add_patch(patches.Circle(wc, r_w * 0.65, facecolor='#7dd3fc', edgecolor='none', zorder=2.6))

    # 카트 직사각형 몸체 및 차축 점 2개
    cart_rect = patches.Rectangle((cart_x - cart_w / 2.0, cart_y0), cart_w, cart_h,
                                  facecolor='#b2d4e5', edgecolor='#1e293b', lw=2.0, zorder=4)
    ax1.add_patch(cart_rect)
    for wx_off in [-0.20, 0.20]:
        ax1.add_patch(patches.Circle((cart_x + wx_off, cart_y0 + 0.035), 0.015, facecolor='#111827', zorder=5))

    label_y = cart_y0 + 0.21 if t >= 0.0 else cart_y0 + 0.18
    ax1.text(cart_x + (0.05 if t >= 0.0 else 0.0), label_y, "50 kg",
             fontsize=13, fontweight='bold', color='#111827', ha='center', va='center', zorder=5)

    # 탄알 및 속도 화살표 (교재 원도 배치)
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
        # 카트 내부에 박힌 탄알 투영 표시
        ax1.plot([cart_left, b_tip_x - 0.12], [bullet_y, bullet_y], color='#78350f', lw=3.0, ls=':', zorder=4.5)
        draw_bullet(ax1, b_tip_x, bullet_y, zorder=5.2, alpha=0.88)
        if t > 0.035:
            c_right = cart_x + cart_w / 2.0
            ax1.annotate('', xy=(c_right + 0.36, bullet_y), xytext=(c_right + 0.03, bullet_y),
                         arrowprops=dict(arrowstyle='->', color='#0ca678', lw=2.8, mutation_scale=16), zorder=6)
            ax1.text(c_right + 0.22, bullet_y + 0.085, rf"$v_f = {vf:.3f}\ \mathrm{{m/s}}$",
                     fontsize=10.5, fontweight='bold', color='#0ca678', ha='center', zorder=6)

    # 상태 표시 배지 (하단)
    ax1.text(0.12, -0.24, phase_str, fontsize=10.5, fontweight='bold', color=phase_col, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8fafc', edgecolor=phase_col, lw=1.4))

    # [말풍선 보충 설명] (학생 친화적 핵심 개념 설명 + 말풍선 꼬리)
    bubble_str = (
        "[말풍선 보충 설명] 운동량은 보존되는데 왜 에너지는 99.9% 사라질까요?\n"
        "• [운동량 100% 보존] 탄알과 카트가 주고받는 큰 충격력은 '서로 반대 방향인 내부 힘'이라 합치면 0이에요!\n"
        "  수평 방향 외부 힘이 없으므로 충돌 전후 총 운동량(G = 45 N·s)은 정확히 그대로 유지됩니다.\n"
        "• [에너지 99.9% 손실] 탄알이 카트를 뚫고 멈추는 동안 마찰열·소리·영구 변형으로 13,480 J이 빠져나가요!"
    )
    ax1.text(-1.26, 1.13, bubble_str, fontsize=8.9, color='#78350f', va='top', ha='left', linespacing=1.38,
             bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.8), zorder=8)

    # =====================================================
    # [우측 상단] 선형 운동량 보존 vs 역학적 에너지 손실 비교 그래프
    # =====================================================
    curr_T = T1 if t < 0 else (T1 - (t / 0.035) * delta_E if t <= 0.035 else T2)
    curr_E_pct = (curr_T / T1) * 100.0

    cats = ['수평 선형 운동량 $G$\n(보존율 %)', '역학적 에너지 $T$\n(잔류율 %)']
    init_vals = [100.0, 100.0]
    curr_vals = [100.0, curr_E_pct]

    x_pos = np.arange(len(cats))
    w_bar = 0.30
    ax2.bar(x_pos - w_bar/2, init_vals, width=w_bar, color='#cbd5e1', edgecolor='#64748b', label='충돌 전 초기값 (100%)')
    bars = ax2.bar(x_pos + w_bar/2, curr_vals, width=w_bar, color=['#2563eb', '#e11d48'], edgecolor='#1e293b', label='현재 상태')

    ax2.set_ylim(0, 146)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(cats, fontsize=9.8, fontweight='bold')
    ax2.set_ylabel("비율 (%)", fontsize=9.8, fontweight='bold')
    ax2.set_title("충돌 전후 선형 운동량(100% 보존) vs 운동 에너지(99.9% 손실)",
                  fontsize=10.8, fontweight='bold', color='#1e293b', pad=5)
    ax2.grid(axis='y', ls=':', alpha=0.5)
    ax2.legend(loc='upper left', fontsize=8.2, ncol=2)

    ax2.text(bars[0].get_x() + w_bar/2, 103, "45.0 N·s\n(100% 보존)", ha='center', va='bottom',
             fontsize=8.8, fontweight='bold', color='#1d4ed8')
    ax2.text(bars[1].get_x() + w_bar/2, curr_E_pct + 3,
             f"{curr_T:,.1f} J\n({curr_E_pct:.1f}%)", ha='center', va='bottom',
             fontsize=8.8, fontweight='bold', color='#be123c')

    # =====================================================
    # [우측 하단] 단계별 정량 수식 정리 패널
    # =====================================================
    ax3.axis('off')
    eq_card = (
        "1. 수평 선형 운동량 보존 (" + r"$\Sigma F_x = 0 \Rightarrow G_1 = G_2$" + ")\n"
        + r"$m v_1 + M(0) = (m + M)v_f \Rightarrow 0.075(600) = (0.075 + 50)\,v_f$" + "\n"
        + r"$\therefore\ v_f = \frac{45.0}{50.075} = \mathbf{0.899\ m/s}$" + "  (오른쪽)\n\n"
        + "2. 역학적 에너지 손실량 " + r"$|\Delta E|$" + " 및 손실률 " + r"$n$" + " 계산\n"
        + r"$T_1 = \frac{1}{2}(0.075)(600)^2 = 13,500\ \mathrm{J},\quad T_2 = \frac{1}{2}(50.075)(0.8987)^2 = 20.2\ \mathrm{J}$" + "\n"
        + r"$|\Delta E| = T_1 - T_2 = \mathbf{13,480\ J},\quad n = \frac{13,480}{13,500}\times 100\% = \mathbf{99.9\%}$"
    )
    ax3.text(0.02, 0.96, eq_card, fontsize=9.6, color='#111827', va='top', ha='left', linespacing=1.42,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4))

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "prob3_142_bullet_cart_impact.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=85)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved prob3_142_bullet_cart_impact.gif")
