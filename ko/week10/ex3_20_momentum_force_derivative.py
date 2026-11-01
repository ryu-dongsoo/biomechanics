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
예제 3.20: 시간 가변 선형운동량으로부터 작용력 F(t) 미분 역산
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 질점 질량 m = 0.2 kg
- 운동 평면: y-z 수직 평면 (y: 수평, z: 연직 상향)
- 선형운동량 함수: G(t) = 1.5(t^2 + 3) j - (2/3)(t^3 - 4) k [N*s]
- 중력가속도 g = 9.81 m/s^2, 자중 W = -0.2(9.81) k = -1.962 k [N]
- 계산 목표 시점: t = 2 s

교재 이론 검증 결과:
- 힘 벡터: F = 6 j - 6.04 k N
- 힘 크기: F = 8.51 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
m = 0.200          # kg
g = 9.81           # m/s^2
W_z = -m * g       # -1.962 N

# 해석적 함수들 (0 <= t <= 3 s)
def get_kinetics(t):
    # 선형운동량 G
    G_y = 1.5 * (t**2 + 3.0)
    G_z = -(2.0 / 3.0) * (t**3 - 4.0)

    # 운동량 시간 변화율 G_dot = dG/dt = Sigma F
    Gdot_y = 3.0 * t
    Gdot_z = -2.0 * (t**2)

    # 외력 F = G_dot - W
    F_y = Gdot_y
    F_z = Gdot_z - W_z  # Gdot_z - (-1.962) = -2t^2 + 1.962
    F_mag = np.hypot(F_y, F_z)

    # 속도 v = G / m
    v_y = G_y / m
    v_z = G_z / m

    return G_y, G_z, Gdot_y, Gdot_z, F_y, F_z, F_mag, v_y, v_z

# 애니메이션 시간 설정 (0.0 to 3.0 s, 60 frames)
n_frames = 60
t_arr = np.linspace(0.0, 3.0, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def update(frame):
    t = t_arr[frame]
    G_y, G_z, Gdot_y, Gdot_z, F_y, F_z, F_mag, v_y, v_z = get_kinetics(t)

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 교재 원도 1:1 시각화 (y-z 수직평면)
    # ==========================================
    ax1.set_xlim(-0.2, 1.4)
    ax1.set_ylim(-0.3, 1.3)
    ax1.set_aspect('equal')
    ax1.set_title("예제 3.20: y-z 평면 질점과 작용력 F (교재 원도 1:1)", fontsize=13, fontweight='bold', pad=12)

    # y-z 좌표축 (y: 수평 우향, z: 연직 상향)
    ax1.annotate('', xy=(1.2, 0.0), xytext=(0.0, 0.0),
                 arrowprops=dict(arrowstyle="->", color='#212529', lw=1.8))
    ax1.annotate('', xy=(0.0, 1.15), xytext=(0.0, 0.0),
                 arrowprops=dict(arrowstyle="->", color='#212529', lw=1.8))
    ax1.text(1.25, -0.02, "y", fontsize=12, fontweight='bold', color='#212529')
    ax1.text(-0.02, 1.20, "z", fontsize=12, fontweight='bold', color='#212529')

    # 연직 상향 표시 "Up"
    ax1.annotate('', xy=(-0.10, 0.65), xytext=(-0.10, 0.35),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.text(-0.16, 0.48, "Up", fontsize=10, fontweight='bold', color='#495057', va='center')

    # 질점 현재 위치 (시각적 스케일링: y축 0.2~0.9, z축 0.8~0.2)
    # t=0 -> (0.25, 0.85), t=2 -> (0.65, 0.50), t=3 -> (0.95, 0.25)
    py = 0.25 + (t / 3.0) * 0.70
    pz = 0.85 - (t / 3.0)**1.8 * 0.65

    # 궤적 파선
    t_trace = np.linspace(0.0, 3.0, 50)
    py_trace = 0.25 + (t_trace / 3.0) * 0.70
    pz_trace = 0.85 - (t_trace / 3.0)**1.8 * 0.65
    ax1.plot(py_trace, pz_trace, 'k--', lw=1.2, alpha=0.4, label='운동 궤적')

    # 질점 구 (하늘색 구 + 윤곽선)
    particle = patches.Circle((py, pz), 0.045, facecolor='#74c0fc', edgecolor='#1864ab', lw=2, zorder=5)
    ax1.add_patch(particle)
    ax1.text(py, pz, "m", fontsize=9, fontweight='bold', ha='center', va='center', color='#1864ab')

    # 자중 벡터: -0.2(9.81)k N (빨간색 하향 화살표)
    w_len = 0.25
    ax1.annotate('', xy=(py, pz - w_len), xytext=(py, pz),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(py, pz - w_len - 0.08, "-0.2(9.81)k N\n(-1.962k N)",
             color='#e03131', fontsize=9, fontweight='bold', ha='center')

    # 작용력 F 벡터: F_y j + F_z k (빨간색 화살표)
    f_scale = 0.035
    f_end_y = py + F_y * f_scale
    f_end_z = pz + F_z * f_scale
    ax1.annotate('', xy=(f_end_y, f_end_z), xytext=(py, pz),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=3.5, mutation_scale=18))
    ax1.text(f_end_y + 0.04, f_end_z + 0.02, f"F = {F_mag:.2f} N\n({F_y:+.1f}j {F_z:+.2f}k)",
             color='#c92a2a', fontsize=9.5, fontweight='bold')

    # t = 2 s 특징점 마커
    if abs(t - 2.0) <= 0.08:
        ax1.add_patch(patches.Circle((py, pz), 0.07, facecolor='none', edgecolor='#f59f00', lw=2.5, linestyle=':', zorder=6))
        highlight_text = "★ 목표 시점 t = 2.0 s (목표 시각 정량 확인)"
        highlight_color = '#d9480f'
    else:
        highlight_text = f"경과 시간: t = {t:.2f} s"
        highlight_color = '#212529'

    ax1.text(0.60, 1.15, highlight_text, fontsize=11, fontweight='bold',
             color=highlight_color, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=highlight_color, lw=1.2))

    # ==========================================
    # [우측 패널] 힘-운동량 미분 해석 및 교재 검증
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("힘-선형운동량 변화율 관계 및 이론 정량 해석", fontsize=12.5, fontweight='bold', pad=10)

    # 1. 실시간 모니터 박스 (Top Box)
    rect_box = patches.Rectangle((-0.12, 0.48), 1.32, 0.52, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ 실시간 운동역학 변수 모니터링 ]", fontsize=11, fontweight='bold', color='#212529')

    ax2.text(-0.08, 0.83, f"■ 시간: t = {t:.2f} s", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.74, f"■ 선형운동량 G(t) = {G_y:.2f}j {G_z:+.2f}k N·s", fontsize=9.5, color='#343a40')
    ax2.text(-0.08, 0.65, f"■ 운동량 변화율 dG/dt = {Gdot_y:.2f}j {Gdot_z:+.2f}k N", fontsize=9.5, color='#343a40')
    ax2.text(-0.08, 0.56, f"■ 작용력 F(t) = dG/dt - W = {F_y:.2f}j {F_z:+.2f}k N  (|F| = {F_mag:.2f} N)",
             fontsize=9.5, fontweight='bold', color='#c92a2a')

    # 2. 이론 유도 및 검증 카드 (Bottom Box)
    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.52, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.35, "■ 기본 지배 방정식 (Newton's 2nd Law in Momentum Form):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.28, "   ΣF = dG/dt  ==>  F + W = dG/dt", fontsize=9.5, color='#212529')

    ax2.text(-0.08, 0.19, "■ 벡터 성분별 미분 및 힘 유도:", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.12, "   dG/dt = d/dt [ 1.5(t²+3)j - (2/3)(t³-4)k ] = 3t j - 2t² k", fontsize=9.0, color='#212529')
    ax2.text(-0.08, 0.05, "   F = dG/dt - W = 3t j - 2t² k - (-1.962 k) = 3t j + (1.962 - 2t²) k", fontsize=9.0, color='#212529')

    ax2.text(-0.08, -0.04, "■ t = 2 s 대입 및 최종 교재 이론 최종값 검증:", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.09, "   F = 6 j - 6.04 k N,    |F| = √(6² + 6.038²) = 8.51 N",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_20_momentum_force_derivative.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
