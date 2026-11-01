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
예제 3.19: 테니스 라켓 임팩트 충격력 및 선형운동량 보존
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 테니스공 질량 m = 60 g = 0.060 kg
- 진입 속도 v1 = 15 m/s (최고점에서 수평 좌향)
- 반발 속도 v2 = 21 m/s (수평 대비 15° 상향 우향)
- 임팩트 접촉 시간 Δt = 0.02 s
- 중력가속도 g = 9.81 m/s^2

교재 원도(1:1) 시각화:
- 코트 바닥면과 서 있는 테니스 선수(타구 자세)
- 바닥에서 튀어 올라 최고점에 도달하는 주황색 점선 포물선 궤적
- 라켓 타구 후 15° 상향으로 뻗어나가는 반발 궤적
- 이론 검증 결과: R = 107.2 N, β = 9.07°
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
m = 0.060          # kg
v1 = 15.0          # m/s (좌향)
v2 = 21.0          # m/s (우상향 15도)
theta_deg = 15.0
theta_rad = np.radians(theta_deg)
dt = 0.02          # s
g = 9.81           # m/s^2
W = m * g          # 0.5886 N

# 선형 충격량-운동량 계산
G1_x = -m * v1                       # -0.900 N*s
G2_x = m * v2 * np.cos(theta_rad)     # +1.217 N*s
G2_y = m * v2 * np.sin(theta_rad)     # +0.326 N*s

Rx = (G2_x - G1_x) / dt              # 105.85 N -> 105.9 N
Ry = ((G2_y) + W * dt) / dt          # 16.89 N
R = np.hypot(Rx, Ry)                 # 107.19 N -> 107.2 N
beta_deg = np.degrees(np.arctan2(Ry, Rx)) # 9.07 deg

# 애니메이션 설정 (60 프레임)
n_frames = 60
t_arr = np.linspace(-0.6, 0.6, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def draw_tennis_player(ax, px, py):
    """교재 원도 1:1 테니스 선수 스탠스 정밀 렌더링"""
    # 머리 및 모자/헤어
    ax.add_patch(patches.Circle((px - 0.22, py + 0.48), 0.045, facecolor='#fcc419', edgecolor='#d9480f', lw=1.2, zorder=4))
    ax.add_patch(patches.Circle((px - 0.20, py + 0.46), 0.038, facecolor='#ffec99', edgecolor='#fcc419', lw=1, zorder=5))

    # 상의 (하늘색 반팔 셔츠)
    shirt_pts = np.array([
        [px - 0.25, py + 0.43], [px - 0.16, py + 0.43],
        [px - 0.13, py + 0.28], [px - 0.25, py + 0.28]
    ])
    ax.add_patch(patches.Polygon(shirt_pts, facecolor='#a5d8ff', edgecolor='#1971c2', lw=1.5, zorder=4))

    # 뻗은 왼팔 (밸런스 유지)
    ax.plot([px - 0.16, px - 0.02], [py + 0.42, py + 0.42], color='#ffec99', lw=4, solid_capstyle='round', zorder=4)

    # 오른팔 (라켓 쥔 팔)
    ax.plot([px - 0.22, px - 0.10, px - 0.02], [py + 0.40, py + 0.32, py + 0.30],
            color='#ffec99', lw=4.5, solid_capstyle='round', zorder=4)

    # 치마 (흰색 테니스 스커트)
    skirt_pts = np.array([
        [px - 0.26, py + 0.28], [px - 0.12, py + 0.28],
        [px - 0.08, py + 0.16], [px - 0.29, py + 0.16]
    ])
    ax.add_patch(patches.Polygon(skirt_pts, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5, zorder=3))

    # 다리 2개 (앞굽이 와이드 스탠스)
    # 뒷다리 (왼쪽)
    ax.plot([px - 0.25, px - 0.32, px - 0.38], [py + 0.16, py + 0.06, py - 0.05],
            color='#ffec99', lw=5, solid_capstyle='round', zorder=2)
    ax.add_patch(patches.Rectangle((px - 0.44, py - 0.08), 0.08, 0.035, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2, zorder=3))

    # 앞다리 (오른쪽)
    ax.plot([px - 0.12, px - 0.08, px - 0.05], [py + 0.16, py + 0.05, py - 0.05],
            color='#ffec99', lw=5, solid_capstyle='round', zorder=2)
    ax.add_patch(patches.Rectangle((px - 0.08, py - 0.08), 0.08, 0.035, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2, zorder=3))

    # 테니스 라켓 (타구면과 손잡이)
    # 손잡이
    ax.plot([px - 0.02, px + 0.02], [py + 0.30, py + 0.26], color='#343a40', lw=5, solid_capstyle='round', zorder=5)
    # 라켓 타원 헤드
    racket_head = patches.Ellipse((px + 0.03, py + 0.31), 0.05, 0.15, angle=-10,
                                  facecolor='none', edgecolor='#e03131', lw=3.5, zorder=5)
    ax.add_patch(racket_head)
    # 스트링 격자망
    for dy in np.linspace(-0.05, 0.05, 5):
        ax.plot([px + 0.01, px + 0.05], [py + 0.31 + dy, py + 0.31 + dy], color='#ced4da', lw=1, zorder=4)

def update(frame):
    t = t_arr[frame]
    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 교재 원도 1:1 시각화 (선수 + 궤적)
    # ==========================================
    ax1.set_xlim(-0.6, 1.4)
    ax1.set_ylim(-0.2, 0.8)
    ax1.set_aspect('equal')
    ax1.set_title("예제 3.19: 테니스 라켓 임팩트 동역학 (교재 원도 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # 코트 바닥면 (갈색/회색 그라데이션 및 실선)
    ax1.fill_between([-0.6, 1.4], -0.2, -0.08, color='#dee2e6', alpha=0.5)
    ax1.plot([-0.6, 1.4], [-0.08, -0.08], color='#495057', lw=2.5)

    # 임팩트 정점 좌표 (라켓 타구면 바로 앞)
    impact_x, impact_y = 0.08, 0.31

    # 테니스 선수 렌더링
    draw_tennis_player(ax1, 0.0, 0.0)

    # 진입 궤적: 바닥에서 튀어 올라 정점에 도달하는 주황색 점선 포물선
    # 바닥 바운드 점: (0.85, -0.08) -> 정점: (0.08, 0.31)
    bx_pts = np.linspace(0.85, impact_x, 50)
    # 포물선 수식: y = 0.31 - a*(x - 0.08)^2  where a = (0.31 - (-0.08))/(0.85-0.08)^2 = 0.39 / 0.5929 = 0.658
    by_pts = impact_y - 0.658 * (bx_pts - impact_x)**2
    ax1.plot(bx_pts, by_pts, color='#f76707', linestyle='--', lw=1.8, label='진입 바운드 궤적')

    # 바닥 이전 궤적 (우상단에서 바운드 점으로 진입)
    bx_pre = np.linspace(1.2, 0.85, 30)
    by_pre = -0.08 + 1.2 * (bx_pre - 0.85)
    ax1.plot(bx_pre, by_pre, color='#f76707', linestyle='--', lw=1.8)

    # 반발 궤적: 정점에서 15도 상향으로 날아가는 주황색 점선
    rx_pts = np.linspace(impact_x, 1.35, 50)
    ry_pts = impact_y + np.tan(theta_rad) * (rx_pts - impact_x) - 0.15 * (rx_pts - impact_x)**2 # 약한 중력 포물선
    ax1.plot(rx_pts, ry_pts, color='#f76707', linestyle='--', lw=1.8, label='타구 후 반발 궤적')

    # 수평 기준선 및 15° 각도 호
    ax1.plot([impact_x, impact_x + 0.6], [impact_y, impact_y], color='#868e96', lw=1.2, linestyle='-')
    arc_ang = np.linspace(0, theta_rad, 25)
    ax1.plot(impact_x + 0.35 * np.cos(arc_ang), impact_y + 0.35 * np.sin(arc_ang), color='#2b8a3e', lw=1.5)
    ax1.text(impact_x + 0.38, impact_y + 0.04, "15°", color='#2b8a3e', fontsize=10, fontweight='bold')

    # 공의 실시간 위치 계산
    if t < 0:
        # 진입 중 (t: -0.6 -> 0)
        curr_x = impact_x + (-t / 0.6) * 0.77
        curr_y = impact_y - 0.658 * (curr_x - impact_x)**2
        ball_state = f"진입 최고점 접근 (v1 = {v1:.0f} m/s ←)"
        state_col = '#1864ab'
    elif t <= 0.05:
        # 충돌 순간
        curr_x = impact_x
        curr_y = impact_y
        ball_state = f"라켓 임팩트 충돌 순간! (Δt = {dt*1000:.0f} ms)"
        state_col = '#e03131'
        # 충격력 벡터 R 표시
        arrow_len = 0.32
        ax1.annotate('', xy=(impact_x + arrow_len * np.cos(np.radians(beta_deg)),
                             impact_y + arrow_len * np.sin(np.radians(beta_deg))),
                     xytext=(impact_x, impact_y),
                     arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.5, mutation_scale=18))
        ax1.text(impact_x + 0.15, impact_y + 0.12, f"R = {R:.1f} N\n(β = {beta_deg:.2f}°)",
                 color='#e03131', fontweight='bold', fontsize=10)
        spark = patches.Circle((impact_x, impact_y), 0.05, facecolor='#ffe066', edgecolor='#f59f00', lw=1.5, alpha=0.8, zorder=6)
        ax1.add_patch(spark)
    else:
        # 반발 비행
        tau = t - 0.05
        curr_x = impact_x + (tau / 0.55) * 0.90
        curr_y = impact_y + np.tan(theta_rad) * (curr_x - impact_x) - 0.15 * (curr_x - impact_x)**2
        ball_state = f"반발 비행 중 (v2 = {v2:.0f} m/s, 15° ↗)"
        state_col = '#2b8a3e'

    # 테니스 공 그리기 (노란색/연두색)
    ball = patches.Circle((curr_x, curr_y), 0.026, facecolor='#ccff00', edgecolor='#5c940d', lw=1.5, zorder=6)
    ax1.add_patch(ball)

    # 속도 벡터 표시
    if t < 0:
        ax1.annotate('', xy=(curr_x - 0.18, curr_y), xytext=(curr_x, curr_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.2, mutation_scale=12))
        ax1.text(curr_x, curr_y - 0.06, f"v1 = {v1:.0f} m/s", color='#2b8a3e', fontsize=9.5, fontweight='bold', ha='center')
    elif t > 0.05:
        ax1.annotate('', xy=(curr_x + 0.18 * np.cos(theta_rad), curr_y + 0.18 * np.sin(theta_rad)), xytext=(curr_x, curr_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.2, mutation_scale=12))
        ax1.text(curr_x, curr_y + 0.06, f"v2 = {v2:.0f} m/s", color='#2b8a3e', fontsize=9.5, fontweight='bold')

    # 상단 상태 배지
    ax1.text(0.40, 0.72, f"상태: {ball_state}", fontsize=11, fontweight='bold',
             color=state_col, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=state_col, lw=1.2))

    # ==========================================
    # [우측 패널] 선형충격량-선형운동량 선도 (교재 풀이 원도)
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("충격량-운동량 선도 및 이론 정량 해석", fontsize=12.5, fontweight='bold', pad=10)

    # 1. 벡터 다이어그램 박스 (교재 풀이의 [초기 운동량] + [충격량] = [최종 운동량] 3단 선도)
    rect_box = patches.Rectangle((-0.12, 0.45), 1.32, 0.55, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ 교재 원도 충격량-운동량 3단계 선도 ]", fontsize=11, fontweight='bold', color='#212529')

    # 1단계: mv1 (좌향)
    ax2.annotate('', xy=(0.02, 0.72), xytext=(0.25, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.8, mutation_scale=14))
    ax2.text(0.13, 0.76, "m v1 = 0.90 N·s", color='#1864ab', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(0.30, 0.70, "+", fontsize=18, fontweight='bold', color='#495057')

    # 2단계: 충격량 [Rx dt + (Ry - W) dt]
    ax2.annotate('', xy=(0.60, 0.72), xytext=(0.42, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=2.8, mutation_scale=14))
    ax2.annotate('', xy=(0.60, 0.86), xytext=(0.60, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=2.5, mutation_scale=12))
    ax2.annotate('', xy=(0.60, 0.65), xytext=(0.60, 0.72),
                 arrowprops=dict(arrowstyle="-|>", color='#868e96', lw=1.8, mutation_scale=10))
    ax2.text(0.51, 0.64, "∫Rx dt", color='#e03131', fontsize=9, fontweight='bold')
    ax2.text(0.63, 0.80, "∫Ry dt", color='#e03131', fontsize=9, fontweight='bold')
    ax2.text(0.63, 0.65, "mg Δt", color='#868e96', fontsize=8)
    ax2.text(0.72, 0.70, "=", fontsize=18, fontweight='bold', color='#495057')

    # 3단계: mv2 (15도 우상향)
    ax2.annotate('', xy=(0.82 + 0.28 * np.cos(theta_rad), 0.70 + 0.28 * np.sin(theta_rad)),
                 xytext=(0.82, 0.70),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.0, mutation_scale=15))
    ax2.text(0.96, 0.82, "m v2 = 1.26 N·s\n(15° ↗)", color='#2b8a3e', fontsize=9, fontweight='bold')

    # 2. 이론 유도 및 해답 카드
    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.50, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.34, "■ 충격량-운동량 방정식 (평균 충격력 R 산출):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.27, f"   x방향: -0.060(15) + Rx(0.02) = 0.060(21 cos 15°)  ==>  Rx = {Rx:.1f} N", fontsize=9.2, color='#212529')
    ax2.text(-0.08, 0.20, f"   y방향: 0 + (Ry - mg)(0.02) = 0.060(21 sin 15°)   ==>  Ry = {Ry:.2f} N", fontsize=9.2, color='#212529')

    ax2.text(-0.08, 0.11, "■ 충격력과 비충격력(자중) 크기 비교:", fontsize=10, fontweight='bold', color='#495057')
    ax2.text(-0.08, 0.05, f"   Ry ({Ry:.2f} N) >> 자중 mg (0.589 N)  ==>  자중 무시 시 Ry = 16.31 N", fontsize=9.0, color='#495057')

    ax2.text(-0.08, -0.04, "■ 최종 검증 결과 (교재 이론 최종값 검증):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.08, f"   R = √(Rx² + Ry²) = {R:.1f} N,   β = tan^(-1)(Ry/Rx) = {beta_deg:.2f}°",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_19_tennis_ball_impulse.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
