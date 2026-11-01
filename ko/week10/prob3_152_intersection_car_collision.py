"""
심화 1 (문제 3/152): 교차로 2차원 차량 충돌 일체화 및 사고 조사 동역학
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 자동차 A: 질량 mA = 1600 kg, 북향(+y) 속도 vA = 32 km/h = 8.889 m/s
- 자동차 B: 질량 mB = 1500 kg, 서향(-x) 속도 vB = 48 km/h = 13.333 m/s
- 교차로 중심에서 충돌 후 엉켜 붙어 일체로 활주 (완전 비탄성 충돌)
- 총 합체 질량 M = mA + mB = 3100 kg

교재 원도 1:1 시각화:
- 베이지/탄색 수평 교차로 평면과 십자 점선 기준축 (N 북향, W 서향)
- 남쪽에서 북향으로 주행하는 빨간색 세단 A (32 km/h ↑)
- 동쪽에서 서향으로 주행하는 파란색 세단 B (48 km/h ←)
- 충돌 후 북서쪽 54.6° 방향으로 활주하는 잔해 궤적

교재 이론 검증 결과:
- 잔해 최종 속도 크기: v = 28.5 km/h (7.92 m/s)
- 진행 각도: θ = 54.6° (북향 기준 서쪽, West of North)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

mA = 1600.0        # kg
vA_kmh = 32.0      # km/h (북향)
vA = vA_kmh / 3.6  # 8.889 m/s

mB = 1500.0        # kg
vB_kmh = 48.0      # km/h (서향)
vB = vB_kmh / 3.6  # 13.333 m/s

M = mA + mB        # 3100 kg

vx_kmh = -(mB * vB_kmh) / M   # -23.226 km/h
vy_kmh = (mA * vA_kmh) / M    # +16.516 km/h
v_kmh = np.hypot(vx_kmh, vy_kmh) # 28.5 km/h
v_ms = v_kmh / 3.6            # 7.916 m/s

theta_rad = np.arctan2(abs(vx_kmh), vy_kmh)
theta_deg = np.degrees(theta_rad) # 54.58 deg -> 54.6 deg

T1 = 0.5 * mA * (vA**2) + 0.5 * mB * (vB**2) # 196.5 kJ
T2 = 0.5 * M * (v_ms**2)                     # 97.1 kJ
delta_T = T1 - T2                            # 99.4 kJ

n_frames = 65
t_arr = np.linspace(-0.6, 0.6, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def draw_topview_car(ax, cx, cy, angle_rad, body_color, edge_color, label_text):
    """교재 원도 1:1 자동차 조감도 정밀 렌더링 (후드, 앞유리, 루프, 뒷유리, 트렁크)"""
    w, l = 0.22, 0.48
    c_th, s_th = np.cos(angle_rad), np.sin(angle_rad)
    R_mat = np.array([[c_th, -s_th], [s_th, c_th]])

    # 차체 외곽선 (둥근 모서리 직사각형)
    corners = np.array([
        [-w/2, -l/2], [w/2, -l/2], [w/2, l/2 - 0.05], [w/2 - 0.04, l/2],
        [-w/2 + 0.04, l/2], [-w/2, l/2 - 0.05]
    ])
    body_rot = np.dot(corners, R_mat.T) + np.array([cx, cy])
    ax.add_patch(patches.Polygon(body_rot, facecolor=body_color, edgecolor=edge_color, lw=2, zorder=4))

    # 앞유리창 (곡면 창문)
    fw_pts = np.array([
        [-w/2 + 0.03, l/4 - 0.02], [w/2 - 0.03, l/4 - 0.02],
        [w/2 - 0.04, l/4 + 0.06], [-w/2 + 0.04, l/4 + 0.06]
    ])
    fw_rot = np.dot(fw_pts, R_mat.T) + np.array([cx, cy])
    ax.add_patch(patches.Polygon(fw_rot, facecolor='#d0ebff', edgecolor=edge_color, lw=1.2, zorder=5))

    # 루프 및 뒷유리창
    rw_pts = np.array([
        [-w/2 + 0.03, -l/4 + 0.02], [w/2 - 0.03, -l/4 + 0.02],
        [w/2 - 0.04, -l/4 - 0.05], [-w/2 + 0.04, -l/4 - 0.05]
    ])
    rw_rot = np.dot(rw_pts, R_mat.T) + np.array([cx, cy])
    ax.add_patch(patches.Polygon(rw_rot, facecolor='#d0ebff', edgecolor=edge_color, lw=1.2, zorder=5))

    # 라벨 텍스트
    if label_text:
        ax.text(cx, cy, label_text, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#ffffff', zorder=6)

def update(frame):
    t = t_arr[frame]

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 교재 원도 1:1 시각화 (베이지 평면 + 십자 점선 기준축)
    # ==========================================
    ax1.set_xlim(-1.4, 1.4)
    ax1.set_ylim(-1.3, 1.4)
    ax1.set_aspect('equal')
    ax1.set_title("심화 1 (문제 3/152): 교차로 2D 충돌 (교재 원도 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # 교재 원도 1:1 베이지색/탄색 평면 배경 박스
    ground_rect = patches.Rectangle((-1.3, -1.2), 2.6, 2.5, facecolor='#d8c8b8', edgecolor='#b09880', lw=2, zorder=1)
    ax1.add_patch(ground_rect)

    # 십자 점선 기준축 (W 서향, N 북향)
    ax1.plot([-1.1, 1.1], [0.0, 0.0], color='#495057', linestyle='--', lw=1.5, zorder=2)
    ax1.plot([0.0, 0.0], [-1.0, 1.0], color='#495057', linestyle='--', lw=1.5, zorder=2)
    ax1.text(0.06, 1.0, "N", fontsize=12, fontweight='bold', ha='left', va='center', color='#212529', zorder=3)
    ax1.text(-1.18, 0.0, "W", fontsize=12, fontweight='bold', va='center', ha='right', color='#212529', zorder=3)

    scale_d = 1.3
    if t < 0:
        # A: 남쪽에서 북향 주행 (+y)
        carA_x = 0.0
        carA_y = -0.55 + t * scale_d * (vA / vB)
        # B: 동쪽에서 서향 주행 (-x)
        carB_x = 0.70 - t * scale_d
        carB_y = 0.0

        # 빨간색 세단 A (북향: 각도 0)
        draw_topview_car(ax1, carA_x, carA_y, 0.0, '#ff8787', '#c92a2a', "A")
        # 녹색 속도 화살표 32 km/h (좌측)
        ax1.annotate('', xy=(carA_x - 0.20, carA_y + 0.25), xytext=(carA_x - 0.20, carA_y - 0.15),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        ax1.text(carA_x - 0.25, carA_y + 0.05, "32 km/h", color='#212529', fontsize=9.5, fontweight='bold', ha='right')

        # 파란색 세단 B (서향: 각도 pi/2)
        draw_topview_car(ax1, carB_x, carB_y, np.pi/2, '#74c0fc', '#1864ab', "B")
        # 녹색 속도 화살표 48 km/h (상단)
        ax1.annotate('', xy=(carB_x - 0.25, carB_y + 0.20), xytext=(carB_x + 0.15, carB_y + 0.20),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.5, mutation_scale=14))
        ax1.text(carB_x - 0.05, carB_y + 0.28, "48 km/h", color='#212529', fontsize=9.5, fontweight='bold', ha='center')

        status_text = "교차로 중심 충돌 접근 중"
        status_col = '#1864ab'
    elif abs(t) <= 0.03:
        # 충돌 순간
        spark = patches.Circle((0, 0), 0.20, facecolor='#ffe066', edgecolor='#f59f00', lw=2.5, alpha=0.8, zorder=7)
        ax1.add_patch(spark)
        status_text = "충돌 임팩트 및 엉킴 일체화 순간!"
        status_col = '#e03131'
    else:
        # 충돌 후: 북서 방향 54.6도 활주
        # 북쪽 기준 서쪽 theta_rad ==> +x축 기준 (pi/2 + theta_rad)
        ang_track = np.pi/2 + theta_rad
        wreck_x = t * scale_d * (v_ms / vB) * np.cos(ang_track)
        wreck_y = t * scale_d * (v_ms / vB) * np.sin(ang_track)

        # 엉켜 붙은 두 차량 렌더링
        draw_topview_car(ax1, wreck_x - 0.08, wreck_y, 0.2, '#ff8787', '#c92a2a', "A")
        draw_topview_car(ax1, wreck_x + 0.08, wreck_y, np.pi/2 - 0.2, '#74c0fc', '#1864ab', "B")

        # 스키드 마크 (충돌 중심에서 현재 위치까지)
        ax1.plot([0, wreck_x], [0, wreck_y], color='#495057', lw=3.0, linestyle=':', alpha=0.7, zorder=3)

        # 최종 속도 벡터 화살표 (초록색)
        v_arrow_len = 0.40
        ax1.annotate('', xy=(wreck_x + v_arrow_len * np.cos(ang_track), wreck_y + v_arrow_len * np.sin(ang_track)),
                     xytext=(wreck_x, wreck_y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.5, mutation_scale=18))
        ax1.text(wreck_x - 0.15, wreck_y + 0.30, f"v = {v_kmh:.1f} km/h\n(θ = {theta_deg:.1f}° W of N)",
                 color='#212529', fontweight='bold', fontsize=10.5)

        status_text = f"잔해 북서방향 활주 (v = {v_kmh:.1f} km/h, θ = {theta_deg:.1f}°)"
        status_col = '#2b8a3e'

    # 각도 호 (북쪽 기준 서쪽 54.6°)
    arc_theta = np.linspace(np.pi/2, np.pi/2 + theta_rad, 25)
    ax1.plot(0.50 * np.cos(arc_theta), 0.50 * np.sin(arc_theta), color='#c92a2a', lw=2.2, zorder=5)
    ax1.text(-0.35, 0.58, f"θ = {theta_deg:.1f}°", color='#c92a2a', fontsize=11, fontweight='bold', zorder=6)

    # 상단 상태 배지
    ax1.text(0.0, 1.25, f"현재 상태: {status_text}", fontsize=11, fontweight='bold',
             color=status_col, ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor=status_col, lw=1.2))

    # ==========================================
    # [우측 패널] 2차원 운동량 보존 벡터 직교 합성
    # ==========================================
    ax2.set_xlim(-0.15, 1.25)
    ax2.set_ylim(-0.15, 1.05)
    ax2.axis('off')
    ax2.set_title("선형운동량 2차원 보존 및 사고 조사 해석", fontsize=12.5, fontweight='bold', pad=10)

    rect_box = patches.Rectangle((-0.12, 0.45), 1.32, 0.55, facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.5)
    ax2.add_patch(rect_box)
    ax2.text(-0.08, 0.94, "[ 2차원 선형운동량 보존 벡터 직교 합성 ]", fontsize=11, fontweight='bold', color='#212529')

    v_ox, v_oy = 0.70, 0.48
    scale_v = 0.0065

    # GA 벡터: 북향 (+y)
    ax2.annotate('', xy=(v_ox, v_oy + vy_kmh * scale_v * 3.1), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#c92a2a', lw=2.8, mutation_scale=14))
    ax2.text(v_ox + 0.03, v_oy + 0.16, f"GA = mA·vA = {mA*vA:.0f} N·s\n(북향 ↑)", color='#c92a2a', fontsize=9, fontweight='bold')

    # GB 벡터: 서향 (-x)
    p_top_x = v_ox
    p_top_y = v_oy + vy_kmh * scale_v * 3.1
    ax2.annotate('', xy=(p_top_x + vx_kmh * scale_v * 3.1, p_top_y), xytext=(p_top_x, p_top_y),
                 arrowprops=dict(arrowstyle="-|>", color='#1864ab', lw=2.8, mutation_scale=14))
    ax2.text(p_top_x - 0.25, p_top_y + 0.03, f"GB = mB·vB = {mB*vB:.0f} N·s (서향 ←)", color='#1864ab', fontsize=9, fontweight='bold')

    # G_tot 벡터
    p_end_x = p_top_x + vx_kmh * scale_v * 3.1
    p_end_y = p_top_y
    ax2.annotate('', xy=(p_end_x, p_end_y), xytext=(v_ox, v_oy),
                 arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=3.2, mutation_scale=16))
    ax2.text(p_end_x - 0.25, (v_oy + p_end_y)*0.5 - 0.05,
             f"G_tot = M·v\n= {M*v_ms:.0f} N·s\n(θ = {theta_deg:.1f}° W of N)",
             color='#2b8a3e', fontsize=9.5, fontweight='bold')

    card_box = patches.Rectangle((-0.12, -0.10), 1.32, 0.50, facecolor='#ffffff', edgecolor='#adb5bd', lw=1.2)
    ax2.add_patch(card_box)

    ax2.text(-0.08, 0.34, "■ 운동량 보존 성분별 해석 (수평 외력 = 0):", fontsize=10, fontweight='bold', color='#1864ab')
    ax2.text(-0.08, 0.27, f"   서향(-x): mB·vB = (mA + mB)·vx  ==>  1500(48) = 3100·vx  ==>  vx = {abs(vx_kmh):.2f} km/h", fontsize=9.2, color='#212529')
    ax2.text(-0.08, 0.20, f"   북향(+y): mA·vA = (mA + mB)·vy  ==>  1600(32) = 3100·vy  ==>  vy = {vy_kmh:.2f} km/h", fontsize=9.2, color='#212529')

    ax2.text(-0.08, 0.11, "■ 운동에너지 손실 검토 (차량 파손·소성변형):", fontsize=10, fontweight='bold', color='#495057')
    ax2.text(-0.08, 0.05, f"   T1 = 196.5 kJ  ==>  T2 = 97.1 kJ  (|ΔT| = {delta_T/1000:.1f} kJ, 손실률 {delta_T/T1*100:.1f}%)", fontsize=9.2, color='#495057')

    ax2.text(-0.08, -0.04, "■ 최종 검증 결과 (교재 이론 최종값 검증):", fontsize=10.5, fontweight='bold', color='#c92a2a')
    ax2.text(-0.04, -0.08, f"   v = √(vx^2 + vy^2) = {v_kmh:.1f} km/h,   θ = tan^(-1)(|vx|/vy) = {theta_deg:.1f}° (북 기준 서쪽)",
             fontsize=10.5, fontweight='bold', color='#c92a2a')

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "prob3_152_intersection_car_collision.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
