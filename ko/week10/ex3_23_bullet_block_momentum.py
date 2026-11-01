"""
예제 3.23: 2차원 탄환 충돌 및 선형운동량 보존
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 탄알 질량 m1 = 50 g = 0.050 kg, 속도 v1 = 600 m/s (+y 방향)
- 목재 블록 질량 m2 = 4.0 kg, 속도 v2 = 12 m/s (수평 x축 대비 30° 상향)
- 마찰 없는 수평면 상에서의 완전 비탄성 충돌 (탄알이 블록에 박힘)
- 합체 질량 M = m1 + m2 = 4.050 kg

교재 이론 검증 결과:
- 합체 속도 크기: v = 16.83 m/s
- 합체 진행 각도: θ = 52.4° (x축 기준)
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
m1 = 0.050          # kg (탄알)
v1 = 600.0          # m/s (+y)
m2 = 4.000          # kg (블록)
v2 = 12.0           # m/s (30 deg)
ang2_deg = 30.0
ang2_rad = np.radians(ang2_deg)

# 운동량 벡터 성분
G1_x = 0.0
G1_y = m1 * v1                     # 30.00 kg*m/s
G2_x = m2 * v2 * np.cos(ang2_rad)  # 41.57 kg*m/s
G2_y = m2 * v2 * np.sin(ang2_rad)  # 24.00 kg*m/s

G_tot_x = G1_x + G2_x              # 41.57 kg*m/s
G_tot_y = G1_y + G2_y              # 54.00 kg*m/s
G_mag = np.hypot(G_tot_x, G_tot_y) # 68.15 kg*m/s

M_tot = m1 + m2                    # 4.050 kg
v_final = G_mag / M_tot            # 16.83 m/s
theta_rad = np.arctan2(G_tot_y, G_tot_x) # 0.9149 rad
theta_deg = np.degrees(theta_rad)        # 52.41 deg -> 52.4 deg

# 에너지 계산
T_init = 0.5 * m1 * (v1**2) + 0.5 * m2 * (v2**2) # 9000 + 288 = 9288 J
T_final = 0.5 * M_tot * (v_final**2)             # 573.3 J
delta_T = T_init - T_final                       # 8714.7 J (손실)

# 애니메이션 설정 (60 프레임, 충돌 전 30프레임, 충돌 후 30프레임)
n_frames = 60
t_arr = np.linspace(-0.6, 0.6, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.12, left=0.07, right=0.95, wspace=0.22)

def update(frame):
    t = t_arr[frame]
    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 2D 충돌 기하학 및 실시간 궤적
    # ==========================================
    ax1.set_xlim(-0.8, 0.8)
    ax1.set_ylim(-0.6, 0.8)
    ax1.set_aspect('equal')
    ax1.set_title("예제 3.23: 수평면 2차원 탄환 충돌 (교재 원도 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # 직교 좌표축 (x, y)
    ax1.axhline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.axvline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.text(0.72, -0.07, "x", fontsize=11, fontweight='bold', color='#495057')
    ax1.text(0.04, 0.72, "y", fontsize=11, fontweight='bold', color='#495057')

    # 충돌 궤적 파선
    ax1.plot([0, 0], [-0.6, 0], 'r--', lw=1.2, alpha=0.5)
    ax1.plot([-0.6 * np.cos(ang2_rad), 0], [-0.6 * np.sin(ang2_rad), 0], 'b--', lw=1.2, alpha=0.5)
    ax1.plot([0, 0.7 * np.cos(theta_rad)], [0, 0.7 * np.sin(theta_rad)], 'g--', lw=1.5, alpha=0.6)

    # 30도 및 52.4도 각도 호
    arc_30 = np.linspace(0, ang2_rad, 20)
    ax1.plot(0.25 * np.cos(arc_30), 0.25 * np.sin(arc_30), color='#1864ab', lw=1.2)
    ax1.text(0.28, 0.05, "30°", color='#1864ab', fontsize=9.5, fontweight='bold')

    arc_52 = np.linspace(0, theta_rad, 25)
    ax1.plot(0.40 * np.cos(arc_52), 0.40 * np.sin(arc_52), color='#2b8a3e', lw=1.5)
    ax1.text(0.42 * np.cos(theta_rad/2), 0.42 * np.sin(theta_rad/2), f"θ = {theta_deg:.1f}°",
             color='#2b8a3e', fontsize=10, fontweight='bold')

    # 물체 위치 계산
    scale_pos = 0.8
    if t < 0:
        # 충돌 전
        # 탄알: 아래에서 위로
        b_x = 0.0
        b_y = t * scale_pos
        # 블록: 3차 사분면에서 30도로
        bk_x = t * scale_pos * np.cos(ang2_rad)
        bk_y = t * scale_pos * np.sin(ang2_rad)

        # 블록 직사각형
        rect = patches.Rectangle((bk_x - 0.08, bk_y - 0.06), 0.16, 0.12, angle=30,
                                 facecolor='#ffd8a8', edgecolor='#e8590c', lw=2, zorder=3)
        ax1.add_patch(rect)
        ax1.text(bk_x - 0.05, bk_y + 0.08, "블록 (4 kg)", color='#e8590c', fontsize=9, fontweight='bold')

        # 탄알 원
        bullet = patches.Circle((b_x, b_y), 0.025, facecolor='#ff6b6b', edgecolor='#c92a2a', lw=1.5, zorder=4)
        ax1.add_patch(bullet)
        ax1.text(b_x + 0.04, b_y, "탄알\n(50 g)", color='#c92a2a', fontsize=8.5, fontweight='bold')

        # 속도 벡터
        ax1.annotate('', xy=(b_x, b_y + 0.12), xytext=(b_x, b_y),
                     arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=2.2, mutation_scale=12))
        ax1.annotate('', xy=(bk_x + 0.12 * np.cos(ang2_rad), bk_y + 0.12 * np.sin(ang2_rad)), xytext=(bk_x, bk_y),
                     arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.2, mutation_scale=12))

        status_text = "충돌 접근 중 (완전 비탄성 충돌 대기)"
        status_color = '#1864ab'
    elif abs(t) <= 0.02:
        # 충돌 순간
        spark = patches.Circle((0, 0), 0.08, facecolor='#ffe066', edgecolor='#f59f00', lw=2, alpha=0.8, zorder=5)
        ax1.add_patch(spark)
        status_text = "충돌 임팩트 순간! (내력 상쇄, 외력 합 0)"
        status_color = '#e03131'
    else:
        # 충돌 후 합체 이동
        c_x = t * scale_pos * np.cos(theta_rad)
        c_y = t * scale_pos * np.sin(theta_rad)

        rect = patches.Rectangle((c_x - 0.08, c_y - 0.06), 0.16, 0.12, angle=np.degrees(theta_rad),
                                 facecolor='#b2f2bb', edgecolor='#2b8a3e', lw=2, zorder=3)
        ax1.add_patch(rect)
        bullet_embedded = patches.Circle((c_x, c_y), 0.02, facecolor='#ff6b6b', edgecolor='#c92a2a', lw=1, zorder=4)
        ax1.add_patch(bullet_embedded)

        # 최종 속도 벡터
        v_arrow_len = 0.22
        ax1.annotate('', xy=(c_x + v_arrow_len * np.cos(theta_rad), c_y + v_arrow_len * np.sin(theta_rad)), xytext=(c_x, c_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.0, mutation_scale=15))
        ax1.text(c_x + 0.05, c_y + 0.15, f"v = {v_final:.2f} m/s\n(θ = {theta_deg:.1f}°)",
                 color='#2b8a3e', fontweight='bold', fontsize=10)

        status_text = f"합체 비행 중 (v = {v_final:.2f} m/s, θ = {theta_deg:.1f}°)"
        status_color = '#2b8a3e'

    ax1.text(0.0, -0.52, f"상태: {status_text}", fontsize=11, fontweight='bold',
             color=status_color, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor=status_color, lw=1.2))

    # ==========================================
    # [우측 패널] 선형운동량 벡터합 삼각형 & 교재 검증
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("선형운동량 벡터 다이어그램 & 이론 정량 해석", fontsize=12.5, fontweight='bold', pad=10)

    # 1. 벡터 삼각형 박스
    rect_box = patches.Rectangle((-0.12, 0.45), 1.32, 0.55, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ 선형운동량 보존 벡터 다이어그램: G1 + G2 = G_total ]", fontsize=10.5, fontweight='bold', color='#212529')

    # 벡터 원점 및 스케일
    v_ox, v_oy = 0.10, 0.55
    v_scale = 0.009

    # G2 벡터 (블록 운동량: 30도)
    ax2.annotate('', xy=(v_ox + G2_x * v_scale, v_oy + G2_y * v_scale), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.5, mutation_scale=14))
    ax2.text(v_ox + G2_x * v_scale * 0.4, v_oy + G2_y * v_scale * 0.4 - 0.05,
             f"G2 = m2·v2\n({G2_x:.1f}i + {G2_y:.1f}j)", color='#1864ab', fontsize=9, fontweight='bold')

    # G1 벡터 (탄알 운동량: +y축)
    p_mid_x = v_ox + G2_x * v_scale
    p_mid_y = v_oy + G2_y * v_scale
    ax2.annotate('', xy=(p_mid_x, p_mid_y + G1_y * v_scale), xytext=(p_mid_x, p_mid_y),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=2.5, mutation_scale=14))
    ax2.text(p_mid_x + 0.03, p_mid_y + G1_y * v_scale * 0.5,
             f"G1 = m1·v1\n({G1_y:.1f}j)", color='#c92a2a', fontsize=9, fontweight='bold')

    # G_total 벡터 (합체 운동량)
    p_final_x = p_mid_x
    p_final_y = p_mid_y + G1_y * v_scale
    ax2.annotate('', xy=(p_final_x, p_final_y), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.2, mutation_scale=16))
    ax2.text(v_ox + 0.12, v_oy + 0.25, f"G_tot = (m1+m2)v\n= {G_mag:.1f} kg·m/s\n(θ = {theta_deg:.1f}°)",
             color='#2b8a3e', fontsize=9.5, fontweight='bold')

    # 2. 이론 계산 및 검증 카드
    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.50, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.34, "■ 운동량 보존 성분별 해석 (수평 외력 = 0):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.27, f"   x성분: 4(12 cos 30°) = (4.050) vx  ==>  vx = {G_tot_x/M_tot:.2f} m/s", fontsize=9.2, color='#212529')
    ax2.text(-0.08, 0.20, f"   y성분: 0.050(600) + 4(12 sin 30°) = (4.050) vy  ==>  vy = {G_tot_y/M_tot:.2f} m/s", fontsize=9.2, color='#212529')

    ax2.text(-0.08, 0.11, "■ 운동에너지 손실 검토:", fontsize=10, fontweight='bold', color='#495057')
    ax2.text(-0.08, 0.05, f"   T_초기 = 9288 J  ==>  T_최종 = 573 J  (소실율: {delta_T/T_init*100:.1f}%)", fontsize=9.2, color='#495057')

    ax2.text(-0.08, -0.04, "■ 최종 검증 결과 (교재 이론 최종값 검증):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.08, f"   v = √(vx² + vy²) = {v_final:.2f} m/s,   θ = tan^(-1)(vy/vx) = {theta_deg:.1f}°",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_23_bullet_block_momentum.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
