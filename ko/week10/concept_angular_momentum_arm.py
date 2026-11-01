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
보충 개념 애니메이션 1 (3.10절): 각운동량 H_O = m v d = m r v sin(theta) 와 수직 모멘트 팔 d 의 불변성
동역학 9판 (한국어판) - 제3장 3.10절 각충격량과 각운동량 기초 개념 시각화
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

# 예제 수치: m = 2.0 kg, 직선 경로 y = d = 3.0 m 위를 왼쪽(-x)으로 등속 v = 5.0 m/s 이동
# 원점 O(0,0) 기준 반시계방향(CCW, +k): H_O = m * v * d = 2 * 5 * 3 = +30.0 kg·m^2/s (항상 일정!)
m = 2.0
v_mag = 5.0
d_arm = 3.0
H_O = m * v_mag * d_arm  # 30.0 kg·m^2/s

n_frames = 60
x_vals = np.linspace(4.5, -4.5, n_frames)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.15, 1.05], height_ratios=[0.92, 1.08],
              left=0.05, right=0.97, top=0.87, bottom=0.08, wspace=0.14, hspace=0.28)

ax_geom = fig.add_subplot(gs[:, 0])
ax_bars = fig.add_subplot(gs[0, 1])
ax_note = fig.add_subplot(gs[1, 1])

fig.suptitle(r"보충 개념 애니메이션 ①: 직선 운동에서도 각운동량 $H_O = m v d = m r v\sin\theta$ 는 왜 일정할까요?",
             fontsize=13.8, fontweight='bold', color='#111827', y=0.96)


def update(frame):
    xc = float(x_vals[frame])
    yc = d_arm
    r_curr = np.hypot(xc, yc)
    theta_rad = np.arccos(np.clip(-xc / r_curr, -1.0, 1.0))
    theta_deg = np.degrees(theta_rad)
    v_theta = v_mag * np.sin(theta_rad)

    ax_geom.clear()
    ax_bars.clear()
    ax_note.clear()
    for ax in (ax_geom, ax_bars, ax_note):
        ax.set_facecolor('#ffffff')

    # 1) 좌측 패널: x-y 평면 기하학 (r, v, theta 변화 vs 수직 모멘트 팔 d = 3 m 불변!)
    ax_geom.set_xlim(-5.8, 5.8)
    ax_geom.set_ylim(-1.9, 5.3)
    ax_geom.set_aspect('equal')
    ax_geom.axis('off')
    ax_geom.set_title(r"① 위치벡터 $\mathbf{r}$ 과 사잇각 $\theta$ 가 변해도 수직 팔 길이 $d = r\sin\theta$ 는 일정!",
                      fontsize=11.3, fontweight='bold', color='#1e293b', pad=6)

    # 좌상단 고정 HUD 수치 배지 (움직이는 화살표와 절대 겹치지 않는 안전 구역!)
    ax_geom.text(-5.45, 4.65,
                 rf"실시간 측정:  $r = {r_curr:.2f}\ \mathrm{{m}}$,   $\theta = {theta_deg:.0f}^\circ$,   $r\sin\theta = {d_arm:.2f}\ \mathrm{{m}}$",
                 fontsize=9.6, fontweight='bold', color='#1e40af', ha='left', va='center',
                 bbox=dict(boxstyle='round,pad=0.30', fc='#eff6ff', ec='#93c5fd', lw=1.3))

    # 좌표축
    ax_geom.plot([-5.3, 5.3], [0, 0], color='#64748b', lw=1.3, ls='--')
    ax_geom.plot([0, 0], [-0.8, 4.15], color='#64748b', lw=1.3, ls='--')
    ax_geom.text(5.45, -0.08, '$x$', fontsize=12, fontweight='bold', color='#334155')
    ax_geom.text(0.14, 4.12, '$y$', fontsize=12, fontweight='bold', color='#334155')

    # 속도 작용선 (직선 y = d = 3.0 m)
    ax_geom.plot([-5.3, 5.3], [d_arm, d_arm], color='#94a3b8', lw=1.8, ls=':', zorder=2)
    ax_geom.text(5.25, d_arm - 0.34, "속도 작용선 (Line of Action)", fontsize=9.0, color='#475569', ha='right', fontweight='bold')

    # 수직 모멘트 팔 d = 3.0 m (원점 O -> (0, d)) 보라색 강조 + 직각 표시
    ax_geom.plot([0, 0], [0, d_arm], color='#7c3aed', lw=3.0, zorder=3)
    sq = 0.28
    ax_geom.plot([0, sq, sq], [d_arm - sq, d_arm - sq, d_arm], color='#7c3aed', lw=1.5, zorder=3)
    # 위치벡터 r이 오른쪽에 있을 때는 왼쪽에, 왼쪽에 있을 때는 오른쪽에 배치하여 겹침 원천 차단!
    if xc >= 0.0:
        ax_geom.text(-0.25, 1.45, r"$d = r\sin\theta = 3.0\ \mathrm{m}$" + "\n(항상 일정!)",
                     fontsize=9.5, fontweight='bold', color='#6d28d9', ha='right', va='center',
                     bbox=dict(boxstyle='round,pad=0.22', fc='#f5f3ff', ec='#c4b5fd', lw=1.1))
    else:
        ax_geom.text(0.25, 1.45, r"$d = r\sin\theta = 3.0\ \mathrm{m}$" + "\n(항상 일정!)",
                     fontsize=9.5, fontweight='bold', color='#6d28d9', ha='left', va='center',
                     bbox=dict(boxstyle='round,pad=0.22', fc='#f5f3ff', ec='#c4b5fd', lw=1.1))

    # 원점 O 및 반시계(+k, 엄지 위) 회전 부호 배지
    ax_geom.plot(0, 0, 'o', color='#0f172a', markersize=6.5, zorder=6)
    ax_geom.text(0.18, -0.42, '$O$', fontsize=12, fontweight='bold', color='#0f172a')
    arc_ccw = np.linspace(-0.25, 1.30, 30)
    ax_geom.plot(0.55 * np.cos(arc_ccw), 0.55 * np.sin(arc_ccw), color='#0284c7', lw=2.0)
    ax_geom.annotate('', xy=(0.55 * np.cos(1.36), 0.55 * np.sin(1.36)),
                     xytext=(0.55 * np.cos(1.12), 0.55 * np.sin(1.12)),
                     arrowprops=dict(arrowstyle='-|>', color='#0284c7', lw=2.0, mutation_scale=12))
    ax_geom.text(-0.68, -0.45, r"$+\mathbf{k}$ (CCW)", fontsize=9.3, fontweight='bold', color='#0369a1', ha='right')

    # 현재 위치벡터 r 화살표 (O -> P)
    ax_geom.annotate('', xy=(xc, yc), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='-|>', color='#1d4ed8', lw=2.3, mutation_scale=14), zorder=4)
    if abs(xc) > 0.65:
        off_x = 0.28 if xc > 0 else -0.28
        ax_geom.text(xc * 0.52 + off_x, yc * 0.52 - 0.18, r"$\mathbf{r}$",
                     fontsize=11.5, fontweight='bold', color='#1d4ed8', ha='center', va='center')

    # r 연장선 점선 및 사잇각 theta 호 표시
    u_r = np.array([xc, yc]) / r_curr
    ax_geom.plot([xc, xc + 0.95 * u_r[0]], [yc, yc + 0.95 * u_r[1]], color='#1d4ed8', lw=1.2, ls='--', zorder=3)
    ang_r_dir = np.arctan2(yc, xc)
    ang_v_dir = np.pi
    a1, a2 = min(ang_r_dir, ang_v_dir), max(ang_r_dir, ang_v_dir)
    arc_th = np.linspace(a1, a2, 24)
    ax_geom.plot(xc + 0.68 * np.cos(arc_th), yc + 0.68 * np.sin(arc_th), color='#d97706', lw=1.8, zorder=5)
    mid_a = 0.5 * (a1 + a2)
    ax_geom.text(xc + 0.92 * np.cos(mid_a), yc + 0.92 * np.sin(mid_a), r"$\theta$",
                 fontsize=10.5, fontweight='bold', color='#b45309', ha='center', va='center')

    # 질점 구 (m = 2 kg) 및 선형운동량 벡터 mv (왼쪽)
    ball = patches.Circle((xc, yc), 0.25, facecolor='#bae6fd', edgecolor='#0f172a', lw=1.8, zorder=6)
    ax_geom.add_patch(ball)
    ax_geom.text(xc + 0.35, yc - 0.38, r"$m = 2\ \mathrm{kg}$", fontsize=9.6, fontweight='bold', ha='left', color='#0f172a')

    v_len = 1.60
    ax_geom.annotate('', xy=(xc - v_len, yc), xytext=(xc, yc),
                     arrowprops=dict(arrowstyle='-|>', color='#059669', lw=2.8, mutation_scale=16), zorder=7)
    ax_geom.text(xc - 0.85, yc + 0.34, r"$m\mathbf{v}\ (5\ \mathrm{m/s})$",
                 fontsize=9.6, fontweight='bold', color='#047857', ha='center')

    # 하단 오른손 법칙 비교 미니 배지 (CCW +k vs CW -k)
    ax_geom.text(0.0, -1.35,
                 r"오른손 법칙: 네 손가락을 $\mathbf{r} \to m\mathbf{v}$ 로 감아쥘 때  "
                 r"반시계(CCW) $= +\mathbf{k}$ (엄지 $\odot$)  |  시계(CW) $= -\mathbf{k}$ (엄지 $\otimes$)",
                 fontsize=9.3, fontweight='bold', color='#1e293b', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.35', fc='#f8fafc', ec='#cbd5e1', lw=1.3))

    # 2) 우상단: 변하는 값(r, v_theta) vs 불변량(d = r sin theta, H_O) 실시간 막대 비교 (xlim 0..48 로 텍스트 잘림 원천 차단!)
    ax_bars.set_xlim(0, 48)
    ax_bars.set_ylim(-0.6, 2.7)
    ax_bars.set_yticks([0.0, 1.0, 2.0])
    ax_bars.set_yticklabels([r'각운동량 $H_O$', r'모멘트 팔 $d \times 5$', r'거리 $r(t) \times 5$'],
                            fontsize=9.5, fontweight='bold')
    ax_bars.set_title(r"② 실시간 비교: $r(t)$ 는 계속 변해도 $d = r\sin\theta$ 와 $H_O$ 는 100% 불변!",
                      fontsize=10.5, fontweight='bold', color='#1e293b', pad=6)
    ax_bars.grid(axis='x', ls=':', alpha=0.5)

    ax_bars.barh(2.0, r_curr * 5.0, height=0.52, color='#93c5fd', edgecolor='#1d4ed8', lw=1.4)
    ax_bars.text(r_curr * 5.0 + 0.7, 2.0, rf"$r = {r_curr:.2f}\ \mathrm{{m}},\ v_\theta = {v_theta:.2f}\ \mathrm{{m/s}}$",
                 va='center', fontsize=8.9, fontweight='bold', color='#1e40af')

    ax_bars.barh(1.0, d_arm * 5.0, height=0.52, color='#ddd6fe', edgecolor='#6d28d9', lw=1.4)
    ax_bars.text(d_arm * 5.0 + 0.7, 1.0, rf"$d = r\sin\theta = {d_arm:.2f}\ \mathrm{{m}}$ (일정!)",
                 va='center', fontsize=8.9, fontweight='bold', color='#5b21b6')

    ax_bars.barh(0.0, H_O, height=0.52, color='#6ee7b7', edgecolor='#047857', lw=1.5)
    ax_bars.text(H_O + 0.7, 0.0, r"$H_O = +30.0\ \mathrm{kg\cdot m^2/s}$",
                 va='center', fontsize=9.0, fontweight='bold', color='#065f46')

    # 3) 우하단: 말풍선 보충 설명 + 3가지 등가 계산식
    ax_note.set_xlim(0, 10)
    ax_note.set_ylim(0, 10)
    ax_note.axis('off')

    bubble = (
        "[말풍선 보충 설명] 직선으로 날아가는데 왜 '각운동량'이 있을까요?\n"
        "• 각운동량 " + r"$\mathbf{H}_O = \mathbf{r} \times m\mathbf{v}$" + " 는 쉽게 말해 '선형운동량(" + r"$m\mathbf{v}$" + ")의 점 " + r"$O$" + "에 대한 모멘트'예요!\n"
        "• 물체가 꼭 원운동을 하지 않더라도, 속도 작용선이 점 " + r"$O$" + "를 비껴 지나가면(" + r"$d > 0$" + ")\n"
        "  점 " + r"$O$" + "에서 볼 때는 반시계 방향으로 돌아가는 회전 효과(" + r"$H_O = m v d$" + ")를 가집니다."
    )
    ax_note.text(0.15, 9.75, bubble, fontsize=9.1, color='#78350f', va='top', ha='left', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_card = (
        "교재 3.10절 평면 각운동량의 3가지 똑같은 계산법:\n"
        + r"$\mathbf{H}_O = \mathbf{r} \times m\mathbf{v} \quad\Longrightarrow\quad "
        + r"H_O = m v d = m r v\sin\theta = m r v_\theta = m r^2\dot{\theta}$" + "\n"
        + "• 수직 팔 길이 " + r"$d$" + " 를 바로 알면 " + r"$mvd$" + " 로 계산하고, 3차원 좌표가 주어지면 외적 행렬식 사용!"
    )
    ax_note.text(0.15, 3.85, eq_card, fontsize=9.1, color='#0f172a', va='top', ha='left', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4))


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_angular_momentum_arm.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=85)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved concept_angular_momentum_arm.gif")
