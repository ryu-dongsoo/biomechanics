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
기초 3 (문제 3/143): 60 g 총알의 목재 블록 관통 충격량 및 마찰계수 역산
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 총알 질량 m = 60 g = 0.060 kg
- 총알 진입 속도 v1 = 600 m/s (수평 좌향 ←)
- 총알 관통 후 출사 속도 v2 = 400 m/s (수평 좌향 ←)
- 목재 블록 질량 M = 3.0 kg (초기 정지)
- 블록 활주 거리 s = 2.70 m (좌향 활주 후 정지)
- 중력가속도 g = 9.81 m/s^2

교재 원도 1:1 시각화:
- 우측에서 좌향으로 진입하는 60 g 총알 (600 m/s ←)
- 3 kg 목재 블록을 관통하여 좌측으로 출사 (400 m/s ←)
- 피격된 목재 블록이 좌측으로 2.70 m 활주 후 정지

교재 이론 검증 결과:
- 블록 발출 직후 초기 속도: vb = 4.0 m/s (좌향)
- 바닥면과 블록 사이의 동마찰계수: μk = 0.302
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
v1 = 600.0         # m/s (좌향)
v2 = 400.0         # m/s (좌향)
M = 3.000          # kg
s_stop = 2.70      # m (좌향)
g = 9.81           # m/s^2

# 1단계: 선형운동량 보존 (관통 순간, 좌향 기준)
# m*v1 = m*v2 + M*vb
vb0 = (m * (v1 - v2)) / M # 4.0 m/s (좌향)

# 2단계: 일-에너지 원리 및 감속 운동
# μk * M * g * s = 0.5 * M * vb0^2 ==> μk = vb0^2 / (2 * g * s)
mu_k = (vb0**2) / (2.0 * g * s_stop) # 0.3020 -> 0.302
a_dec = mu_k * g                     # 2.963 m/s^2
t_slide = vb0 / a_dec                # 1.350 s

# 애니메이션 설정 (70 프레임)
n_frames = 70
t_arr = np.linspace(-0.25, t_slide + 0.25, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def update(frame):
    t = t_arr[frame]

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 교재 원도 1:1 시각화 (좌향 관통 및 좌향 활주)
    # ==========================================
    ax1.set_xlim(-1.0, 3.8)
    ax1.set_ylim(-0.45, 1.15)
    ax1.set_title("기초 3 (문제 3/143): 총알 관통 및 마찰 감속 활주 (교재 원도 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # 지면 (수평 바닥 + 하단 음영)
    ax1.plot([-0.9, 3.7], [-0.08, -0.08], color='#495057', lw=3.0)
    ax1.fill_between([-0.9, 3.7], -0.08, -0.22, color='#dee2e6', alpha=0.6)
    for hx in np.linspace(-0.85, 3.55, 30):
        ax1.plot([hx, hx + 0.08], [-0.08, -0.16], color='#adb5bd', lw=1.2)

    # 블록 치수
    bk_w, bk_h = 0.65, 0.45

    # 초기 블록 위치 (우측: x = 2.70)
    init_x = 2.70
    # 최종 정지 위치 (좌측: x = 0.0)
    final_x = 0.0

    # 교재 원도의 2.70 m 치수선 및 화살표
    dim_y = -0.25
    ax1.plot([final_x, init_x], [dim_y, dim_y], color='#495057', lw=1.5)
    ax1.plot([final_x, final_x], [-0.08, dim_y - 0.05], color='#868e96', lw=1.2)
    ax1.plot([init_x, init_x], [-0.08, dim_y - 0.05], color='#868e96', lw=1.2)
    ax1.annotate('', xy=(final_x, dim_y), xytext=(final_x + 0.3, dim_y),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.annotate('', xy=(init_x, dim_y), xytext=(init_x - 0.3, dim_y),
                 arrowprops=dict(arrowstyle="->", color='#495057', lw=1.5))
    ax1.text((final_x + init_x)/2, dim_y - 0.12, "2.70 m", fontsize=10.5, fontweight='bold', color='#212529', ha='center')

    # 초기 블록 고스트/기준 윤곽선 (우측)
    init_block_ghost = patches.Rectangle((init_x - bk_w/2, -0.08), bk_w, bk_h,
                                         facecolor='#fff4e6', edgecolor='#ffd8a8', lw=1.5, linestyle='--', zorder=2)
    ax1.add_patch(init_block_ghost)

    # 상태에 따른 블록 및 총알 위치 (좌향 운동!)
    if t < 0:
        # 충돌 전: 블록은 x = 2.70에서 정지
        bk_x = init_x
        bullet_x = init_x + bk_w/2 + 0.8 + (t / 0.25) * 0.8 # 우측에서 좌측으로 접근
        bullet_v = v1
        status_text = f"총알 좌향 진입 (v1 = {v1:.0f} m/s ←)"
        status_col = '#1864ab'
    elif t <= 0.05:
        # 관통 순간
        bk_x = init_x
        bullet_x = init_x - bk_w/2 - 0.15 # 블록 좌측으로 관통 출사
        bullet_v = v2
        status_text = f"블록 관통 출사! (v2 = {v2:.0f} m/s ←, 블록 vb = {vb0:.1f} m/s ←)"
        status_col = '#e03131'
        spark = patches.Circle((init_x, 0.15), 0.10, facecolor='#ffe066', edgecolor='#f59f00', lw=2, alpha=0.8, zorder=6)
        ax1.add_patch(spark)
    else:
        # 충돌 후: 블록 좌측 활주
        dt_slide = min(t, t_slide)
        s_curr = vb0 * dt_slide - 0.5 * a_dec * (dt_slide**2) # 좌향 이동거리
        bk_x = init_x - s_curr
        v_curr = max(0.0, vb0 - a_dec * dt_slide)
        bullet_x = -0.8 # 총알은 화면 좌측 밖으로 비행
        bullet_v = v2
        if v_curr > 0:
            status_text = f"블록 좌측 마찰 활주 중 (v = {v_curr:.2f} m/s ←, s = {s_curr:.2f} m)"
            status_col = '#d9480f'
        else:
            status_text = f"블록 정지 완료 (정지 위치 x = 0.0 m, 정지거리 s = {s_stop:.2f} m)"
            status_col = '#2b8a3e'

    # 목재 블록 그리기 (교재 원도의 tan/wood 색상)
    block = patches.Rectangle((bk_x - bk_w/2, -0.08), bk_w, bk_h,
                              facecolor='#ffd8a8', edgecolor='#d9480f', lw=2.2, zorder=3)
    ax1.add_patch(block)
    ax1.text(bk_x, 0.14, "3 kg", fontsize=10.5, fontweight='bold', color='#d9480f', ha='center', va='center')

    # 총알 관통 구멍 파선
    ax1.plot([bk_x - bk_w/2, bk_x + bk_w/2], [0.14, 0.14], 'k:', lw=1.5, zorder=4)

    # 진입 총알 표시 (우측 총알)
    if t < 0.02:
        # 주황색 점선 진입 궤적
        ax1.plot([bullet_x + 0.6, bullet_x], [0.14, 0.14], color='#f76707', linestyle='--', lw=1.8)
        # 총알 탄두 (좌향 뾰족한 탄두)
        ax1.annotate('', xy=(bullet_x - 0.20, 0.14), xytext=(bullet_x, 0.14),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        b_patch = patches.Rectangle((bullet_x, 0.10), 0.12, 0.08, facecolor='#ff8787', edgecolor='#c92a2a', lw=1.2, zorder=5)
        ax1.add_patch(b_patch)
        ax1.text(bullet_x + 0.06, 0.22, "600 m/s\n(60 g)", color='#212529', fontsize=9, fontweight='bold', ha='center')

    # 출사 총알 표시 (좌측 관통 출사)
    if t >= 0.02 and bullet_x > -0.6:
        ax1.annotate('', xy=(bullet_x - 0.20, 0.14), xytext=(bullet_x, 0.14),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        b_patch = patches.Rectangle((bullet_x, 0.10), 0.12, 0.08, facecolor='#ff8787', edgecolor='#c92a2a', lw=1.2, zorder=5)
        ax1.add_patch(b_patch)
        ax1.text(bullet_x - 0.10, 0.22, "400 m/s", color='#212529', fontsize=9.5, fontweight='bold', ha='center')

    # 마찰력 화살표 (블록 활주 시: 운동 반대방향인 우향)
    if t > 0.05 and t <= t_slide:
        f_fric = mu_k * M * g
        ax1.annotate('', xy=(bk_x + bk_w/2 + 0.35, -0.08), xytext=(bk_x + bk_w/2, -0.08),
                     arrowprops=dict(arrowstyle="-|>", color='#495057', lw=2.8, mutation_scale=14))
        ax1.text(bk_x + bk_w/2 + 0.40, -0.05, f"Ff = μk N\n({f_fric:.1f} N)", color='#495057', fontsize=8.5, fontweight='bold')

    # 상단 상태 배지
    ax1.text(1.4, 0.96, f"상태: {status_text}", fontsize=10.5, fontweight='bold',
             color=status_col, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=status_col, lw=1.2))

    # ==========================================
    # [우측 패널] 충격량 전달 및 일-에너지 감속 곡선
    # ==========================================
    ax2.set_xlim(-0.1, 3.0)
    ax2.set_ylim(-0.3, 4.6)
    ax2.set_title("블록 속도-거리 v(s) 곡선 및 이론 정량 해석", fontsize=12.5, fontweight='bold', pad=10)

    s_plot = np.linspace(0, s_stop, 100)
    v_plot = np.sqrt(np.maximum(0, vb0**2 - 2.0 * a_dec * s_plot))
    ax2.plot(s_plot, v_plot, color='#1864ab', lw=2.8, label='블록 속도 v(s) [m/s]')

    ax2.plot([0.0], [vb0], 'bo', markersize=8)
    ax2.text(0.1, vb0 + 0.15, f"초기 발출 속도: vb = {vb0:.1f} m/s (←)", color='#1864ab', fontweight='bold', fontsize=9.5)

    ax2.plot([s_stop], [0.0], 'ro', markersize=8)
    ax2.text(s_stop, 0.55, f"완전 정지\n(s = {s_stop:.2f} m)", color='#c92a2a', fontweight='bold', fontsize=9.0, ha='center')

    if t > 0.05:
        curr_s_val = min(s_stop, vb0 * min(t, t_slide) - 0.5 * a_dec * (min(t, t_slide)**2))
        curr_v_val = max(0.0, vb0 - a_dec * min(t, t_slide))
        ax2.plot([curr_s_val], [curr_v_val], 'o', color='#f59f00', markersize=10, zorder=5)

    ax2.set_xlabel("블록 좌향 활주 거리 s (m)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("블록 속도 v (m/s)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', color='#dee2e6')
    ax2.legend(loc='upper right', fontsize=10)

    theory_text = (
        "■ 1단계: 관통 충돌 시 선형운동량 보존 (외력 충격량 무시, 좌향 +):\n"
        "   m·v1 = m·v2 + M·vb\n"
        "   0.060(600) = 0.060(400) + 3·vb\n"
        "   36.0 = 24.0 + 3·vb  ==>  vb = 4.0 m/s (좌향 ←)\n\n"
        "■ 2단계: 활주 구간 일-에너지 원리:\n"
        "   -μk·M·g·s = 0 - 0.5·M·(vb)^2  ==>  μk·g·s = 0.5·(vb)^2\n"
        "   μk(9.81)(2.70) = 0.5(4.0)^2 = 8.0\n"
        "   μk = 8.0 / (9.81 × 2.70) = 0.3020\n"
        "■ 최종 이론 계산 결과: vb = 4.0 m/s,  μk = 0.302"
    )
    ax2.text(0.05, 0.40, theory_text, fontsize=9.0,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "prob3_143_bullet_wood_block.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
