"""
예제 3.21: 수평면 시간 가변 외력 F1, F2와 2차원 선형충격량-운동량 해석
동역학 9판 제3장 C편 (Section 3.9) 선형충격량과 선형운동량

문제 제원:
- 질점 질량 m = 0.5 kg
- 초기 상태 (t = 0): v1 = 10 m/s (+x 방향, v1 = 10i m/s)
- 작용 외력:
  * F1 (-x 방향): 0 <= t <= 1 s에서 4 N, 1 < t <= 3 s에서 2 N
  * F2 (+y 방향): 0 <= t <= 2 s에서 1 N, 2 < t <= 3 s에서 1 N -> 3 N 선형 증가
- 계산 목표: 3초 후 속도 v2 = (v2)x i + (v2)y j

교재 이론 검증 결과:
- (v2)x = -6 m/s, (v2)y = 8 m/s
- 최종 속도 크기: v2 = 10 m/s
- 속도 방향각: θx = 126.9° (+x축 기준)
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
m = 0.500          # kg
v1_x = 10.0        # m/s
v1_y = 0.0         # m/s

# 3초간 충격량 적분
# Imp_x = - ∫ F1 dt = -(4*1 + 2*2) = -8 N*s
# Imp_y = + ∫ F2 dt = (1*2 + (1+3)/2 * 1) = 4 N*s
imp_x = -8.0       # N*s
imp_y = 4.0        # N*s

v2_x = (m * v1_x + imp_x) / m # (5 - 8)/0.5 = -6.0 m/s
v2_y = (m * v1_y + imp_y) / m # 4.0 / 0.5 = +8.0 m/s
v2_mag = np.hypot(v2_x, v2_y) # 10.0 m/s
theta_deg = np.degrees(np.arctan2(v2_y, v2_x)) # 126.87 deg -> 126.9 deg

# 운동학 해석 함수 (0 <= t <= 3 s)
def get_state(t):
    # F1(t), F2(t)
    if t <= 1.0:
        F1 = 4.0
    else:
        F1 = 2.0

    if t <= 2.0:
        F2 = 1.0
    else:
        F2 = 1.0 + 2.0 * (t - 2.0)

    # 속도 및 위치 성분
    if t <= 1.0:
        vx = 10.0 - 8.0 * t
        x = 10.0 * t - 4.0 * (t**2)
        vy = 2.0 * t
        y = t**2
    elif t <= 2.0:
        dt1 = t - 1.0
        vx = 2.0 - 4.0 * dt1
        x = 6.0 + 2.0 * dt1 - 2.0 * (dt1**2)
        vy = 2.0 + 2.0 * dt1
        y = 1.0 + 2.0 * dt1 + (dt1**2)
    else:
        dt2 = t - 2.0
        vx = -2.0 - 4.0 * dt2
        x = 6.0 - 2.0 * dt2 - 2.0 * (dt2**2)
        vy = 4.0 + 2.0 * dt2 + 2.0 * (dt2**2)
        y = 4.0 + 4.0 * dt2 + (dt2**2) + (2.0/3.0)*(dt2**3)

    return F1, F2, vx, vy, x, y

# 애니메이션 설정 (75 프레임)
n_frames = 75
t_arr = np.linspace(0.0, 3.0, n_frames)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.patch.set_facecolor('#ffffff')
fig.subplots_adjust(top=0.91, bottom=0.13, left=0.08, right=0.96, wspace=0.24)

def update(frame):
    t = t_arr[frame]
    F1, F2, vx, vy, x, y = get_state(t)

    ax1.clear()
    ax2.clear()

    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # ==========================================
    # [좌측 패널] 교재 원도 1:1 시각화 (수평 평면 궤적 + 힘-시간 선도)
    # ==========================================
    ax1.set_xlim(-2.0, 8.5)
    ax1.set_ylim(-1.5, 11.5)
    ax1.set_aspect('equal')
    ax1.set_title("예제 3.21: x-y 평면 질점 운동 및 실시간 궤적 (교재 원도 1:1)", fontsize=12.5, fontweight='bold', pad=10)

    # 직교 좌표축 (x, y)
    ax1.axhline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.axvline(0, color='#ced4da', lw=1.2, linestyle='--')
    ax1.text(8.0, -0.6, "x, m", fontsize=11, fontweight='bold', color='#495057')
    ax1.text(-0.8, 10.8, "y, m", fontsize=11, fontweight='bold', color='#495057')

    # 전체 3초간 궤적 곡선 (교재 원도의 주황색 점선)
    t_full = np.linspace(0.0, 3.0, 100)
    traj_x = [get_state(tau)[4] for tau in t_full]
    traj_y = [get_state(tau)[5] for tau in t_full]
    ax1.plot(traj_x, traj_y, color='#f76707', linestyle='--', lw=2.2, label='3초간 운동 궤적')

    # 주요 특징 시간대 위치 마크 (t=1, 2, 3s)
    for t_mark in [1.0, 2.0, 3.0]:
        _, _, _, _, mx, my = get_state(t_mark)
        ax1.plot([mx], [my], 'ko', markersize=4)
        ax1.text(mx + 0.3, my - 0.2, f"t = {t_mark:.0f} s", fontsize=8.5, color='#495057', fontweight='bold')

    # 현재 질점 위치 (하늘색 원)
    particle = patches.Circle((x, y), 0.35, facecolor='#a5d8ff', edgecolor='#1971c2', lw=2, zorder=5)
    ax1.add_patch(particle)
    ax1.text(x, y, "m", fontsize=9, fontweight='bold', ha='center', va='center', color='#1971c2')

    # 작용력 F1 (-x 방향: 빨간색 화살표)
    f1_len = F1 * 0.45
    ax1.annotate('', xy=(x - f1_len, y), xytext=(x, y),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(x - f1_len - 0.2, y + 0.2, f"F1 = {F1:.1f} N", color='#e03131', fontsize=9.5, fontweight='bold', ha='right')

    # 작용력 F2 (+y 방향: 빨간색 화살표)
    f2_len = F2 * 0.45
    ax1.annotate('', xy=(x, y + f2_len), xytext=(x, y),
                 arrowprops=dict(arrowstyle="-|>", color='#e03131', lw=3.0, mutation_scale=15))
    ax1.text(x + 0.2, y + f2_len + 0.2, f"F2 = {F2:.1f} N", color='#e03131', fontsize=9.5, fontweight='bold')

    # 속도 벡터 (초록색 화살표)
    v_mag_curr = np.hypot(vx, vy)
    if v_mag_curr > 0.2:
        v_scale = 0.22
        ax1.annotate('', xy=(x + vx * v_scale, y + vy * v_scale), xytext=(x, y),
                     arrowprops=dict(arrowstyle="-|>", color='#2b8a3e', lw=2.8, mutation_scale=14))
        ax1.text(x + vx * v_scale + 0.2, y + vy * v_scale, f"v = {v_mag_curr:.1f} m/s",
                 color='#2b8a3e', fontsize=9.5, fontweight='bold')

    # t = 3 s 도달 시 최종 속도 분력 직사각형 표시 (교재 하단 원도 반영)
    if t >= 2.95:
        ax1.plot([x, x + vx * 0.35], [y, y], color='#1864ab', lw=2, linestyle=':')
        ax1.plot([x + vx * 0.35, x + vx * 0.35], [y, y + vy * 0.35], color='#2b8a3e', lw=2, linestyle=':')
        ax1.plot([x, x + vx * 0.35], [y + vy * 0.35, y + vy * 0.35], color='#adb5bd', lw=1, linestyle='--')
        ax1.plot([x, x], [y, y + vy * 0.35], color='#adb5bd', lw=1, linestyle='--')
        ax1.text(x - 1.2, y - 0.5, "-6i m/s", color='#1864ab', fontweight='bold', fontsize=10)
        ax1.text(x - 2.8, y + 1.5, "8j m/s", color='#2b8a3e', fontweight='bold', fontsize=10)
        ax1.text(x - 2.5, y + 3.2, f"v2 = 10 m/s\n(θx = {theta_deg:.1f}°)", color='#c92a2a', fontweight='bold', fontsize=10.5)

    # 상단 상태 배지
    ax1.text(3.0, 11.2, f"시간: t = {t:.2f} s | 위치: ({x:.2f}, {y:.2f}) m", fontsize=11, fontweight='bold',
             color='#212529', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

    # ==========================================
    # [우측 패널] 힘-시간 F(t) 선도 및 이론 정량 해석
    # ==========================================
    ax2.set_xlim(-0.3, 3.5)
    ax2.set_ylim(-0.5, 5.0)
    ax2.set_title("힘-시간 F(t) 충격량 선도 및 속도 검증", fontsize=12.5, fontweight='bold', pad=10)

    # F1(t) 곡선 (빨간색 계단선)
    t_f = np.array([0.0, 1.0, 1.0, 3.0])
    f1_f = np.array([4.0, 4.0, 2.0, 2.0])
    ax2.plot(t_f, f1_f, color='#c92a2a', lw=2.5, label='F1 (음의 x방향: 충격량 -8 N·s)')
    ax2.fill_between(t_f, f1_f, color='#ffc9c9', alpha=0.35)

    # F2(t) 곡선 (파란색 꺾은선)
    t_f2 = np.array([0.0, 2.0, 3.0])
    f2_f2 = np.array([1.0, 1.0, 3.0])
    ax2.plot(t_f2, f2_f2, color='#1864ab', lw=2.5, label='F2 (양의 y방향: 충격량 +4 N·s)')
    ax2.fill_between(t_f2, f2_f2, color='#d0ebff', alpha=0.35)

    # 현재 시간 수직선
    ax2.axvline(t, color='#f59f00', linestyle=':', lw=2)

    ax2.set_xlabel("시간 t (s)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("힘 F (N)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', color='#dee2e6')
    ax2.legend(loc='upper right', fontsize=9.0)

    # 이론 유도 카드
    imp_card = (
        "■ 선형충격량-운동량 방정식 (성분별 면적 적분):\n"
        "   m(v1)x + ∫(-F1)dt = m(v2)x\n"
        "   0.5(10) - [4(1) + 2(2)] = 0.5(v2)x  ==>  5 - 8 = -3  ==>  (v2)x = -6 m/s\n\n"
        "   m(v1)y + ∫(F2)dt = m(v2)y\n"
        "   0 + [1(2) + 0.5(1+3)(1)] = 0.5(v2)y  ==>  4 = 0.5(v2)y  ==>  (v2)y = +8 m/s\n\n"
        "■ 최종 이론 계산 결과 (100% 일치):\n"
        "   v2 = -6i + 8j m/s  (|v2| = 10 m/s,  θx = 126.9°)"
    )
    ax2.text(-0.2, -0.35, imp_card, fontsize=8.8,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#ced4da', lw=1.2))

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "ex3_21_variable_force_plane_impulse.gif")
anim = FuncAnimation(fig, update, frames=n_frames, interval=80)
anim.save(out_path, writer='pillow', dpi=100)
plt.close()
print(f"[완료] {out_path} 생성 완료!")
