"""
동역학 9판 제4장 4.5절: 에너지와 운동량 보존
심화문제 1 - 문제 4/25 (Problem 4/25) - 25 Mg 편평 화차(Flatcar) 위 5° 경사로를 12 m 굴러 내려오는 7.5 Mg 차량
- 순수 흰색 바탕 (#ffffff) & 교재 그림(트러스 경사로가 설치된 편평 화차와 활강 차량) 완벽 반영
- 정량 계산 검증:
  * ΔV_g = -7500(9.81)(12 sin 5°) = -76.95 × 10^3 J
  * ΣF_x = 0 => ΔG_x = 0: 7.5(10^3)(ṡ cos 5° - v) - 25(10^3) v = 0 => ṡ cos 5° = 4.333 v
  * ΔT + ΔV_g = 0: 54,706 v^2 = 76,950 => v^2 = 1.4066 => v = 1.186 m/s (ṡ = 5.159 m/s)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수 (정확한 수치 검증용 5도, 시각화 기하학은 가독성을 위해 8.5도로 미세 강조하되 경사면 완전 밀착)
M_flat = 25000.0    # 25 Mg = 25,000 kg
m_car = 7500.0      # 7.5 Mg = 7,500 kg
g = 9.81
theta_deg = 5.0
theta = np.radians(theta_deg)
s_max = 12.0        # m

# 이론 연립해:
# s_dot * cos(5°) = (32.5 / 7.5) * v = 4.3333 * v
ratio_s_v = (M_flat + m_car) / (m_car * np.cos(theta))  # s_dot / v = 4.350
# 54706 * v^2 = m_car * g * s * sin(5°)
v_final = 1.186     # m/s (화차 우측 속도)
s_dot_final = 5.159 # m/s (차량 경사면 상대속력)
t_total = 2.0 * s_max / s_dot_final  # 등가속도 운동 시간 = 4.652 s

n_frames = 54
t_vals = np.linspace(0, t_total, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

# 시각화용 경사각 (5도를 화면에서 선명한 트러스 구조로 표현하기 위해 8도 적용, 차량 바퀴/본체 모두 정확히 동일 각도로 회전 밀착)
vis_deg = 8.0
vis_rad = np.radians(vis_deg)

def update(frame):
    t = t_vals[frame]
    frac = (t / t_total)**2          # s / s_max (0 ~ 1)
    v_frac = t / t_total             # v / v_final (0 ~ 1)

    s_curr = s_max * frac
    v_curr = v_final * v_frac
    s_dot_curr = s_dot_final * v_frac

    # 화차의 수평 이동 변위 x_flat = (m_car * cos5° / (M_flat + m_car)) * s_curr
    x_flat = (m_car * np.cos(theta) / (M_flat + m_car)) * s_curr  # 최대 약 2.76 m

    # 에너지 계산
    dVg_curr = -m_car * g * s_curr * np.sin(theta)
    T_flat_curr = 0.5 * M_flat * v_curr**2
    T_car_curr = 0.5 * m_car * (v_curr**2 + s_dot_curr**2 - 2 * v_curr * s_dot_curr * np.cos(theta))

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-5.5, 6.5)
    ax_main.set_ylim(-1.2, 3.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 지면 및 철도 레일
    y_rail = -0.35
    ground = patches.Rectangle((-5.3, y_rail - 0.42), 11.6, 0.42, facecolor='#e8dfd5', edgecolor='none', zorder=1)
    ax_main.add_patch(ground)
    ax_main.plot([-5.3, 6.3], [y_rail, y_rail], color='#37474f', lw=2.5, zorder=2)
    for tx in np.linspace(-5.0, 6.0, 26):
        ax_main.plot([tx, tx], [y_rail - 0.06, y_rail], color='#4e342e', lw=2.5, zorder=2)

    # 화차 중심 위치 (시각화 스케일: 1 m = 0.45 유닛)
    scale = 0.45
    xc = -0.75 + x_flat * scale
    flat_L = 8.2
    xL = xc - flat_L / 2.0
    xR = xc + flat_L / 2.0
    y_deck = y_rail + 0.80

    # 화차 대차 및 바퀴 (좌·우 2개 보기)
    for bx in [xc - 2.55, xc + 2.55]:
        for wx in [-0.46, 0.46]:
            w = patches.Circle((bx + wx, y_rail + 0.22), 0.22, facecolor='#bcaaa4', edgecolor='#37474f', lw=1.8, zorder=3)
            ax_main.add_patch(w)
            hub = patches.Circle((bx + wx, y_rail + 0.22), 0.08, facecolor='#37474f', edgecolor='none', zorder=4)
            ax_main.add_patch(hub)
        sideframe = patches.Polygon([[bx - 0.60, y_rail + 0.18], [bx + 0.60, y_rail + 0.18],
                                     [bx + 0.44, y_rail + 0.36], [bx - 0.44, y_rail + 0.36]],
                                    facecolor='#8d6e63', edgecolor='#3e2723', lw=1.3, zorder=4)
        ax_main.add_patch(sideframe)

    # 편평 화차 본체 프레임 (청록색 교재 스타일)
    flat_poly = patches.Polygon([
        [xL, y_deck], [xR, y_deck],
        [xR, y_deck - 0.25], [xR - 1.1, y_deck - 0.25], [xR - 1.35, y_deck - 0.36],
        [xL + 1.35, y_deck - 0.36], [xL + 1.1, y_deck - 0.25], [xL, y_deck - 0.25]
    ], facecolor='#7da8be', edgecolor='#244759', lw=1.8, zorder=4)
    ax_main.add_patch(flat_poly)
    ax_main.text(xc, y_deck - 0.18, '25 Mg 편평 화차 (Flatcar)', fontsize=10, fontweight='bold', ha='center', va='center', color='#102a38', zorder=5)

    # 양 끝 커플러
    for cx_end in [xL - 0.12, xR + 0.02]:
        coup = patches.Rectangle((cx_end, y_deck - 0.21), 0.10, 0.15, facecolor='#455a64', edgecolor='#263238', lw=1.2, zorder=3)
        ax_main.add_patch(coup)

    # 5도 경사로 트러스 구조물 (좌측 끝 B는 낮고 우측 끝은 높음)
    p_B = np.array([xL + 0.08, y_deck + 0.04])
    u_inc = np.array([np.cos(vis_rad), np.sin(vis_rad)])
    n_inc = np.array([-np.sin(vis_rad), np.cos(vis_rad)])
    ramp_len = flat_L - 0.16
    p_topR = p_B + ramp_len * u_inc

    # 트러스 수직 및 사선 부재
    n_bays = 5
    for i in range(1, n_bays + 1):
        f_i = i / n_bays
        f_prev = (i - 1) / n_bays
        pt_top = p_B + (f_i * ramp_len) * u_inc
        pt_bot = np.array([pt_top[0], y_deck])
        pt_prev_top = p_B + (f_prev * ramp_len) * u_inc
        ax_main.plot([pt_top[0], pt_bot[0]], [pt_top[1], pt_bot[1]], color='#607d8b', lw=2.2, zorder=3)
        if i >= 2:
            ax_main.plot([pt_prev_top[0], pt_bot[0]], [pt_prev_top[1], pt_bot[1]], color='#78909c', lw=1.8, zorder=3)

    # 경사로 상판 빔 (Polygon)
    beam_poly = patches.Polygon([p_B, p_topR, p_topR + 0.07*n_inc, p_B + 0.07*n_inc],
                                facecolor='#b0bec5', edgecolor='#37474f', lw=1.6, zorder=5)
    ax_main.add_patch(beam_poly)

    # 좌측 끝 B 정지장치 (Stopper B)
    stop_B = patches.Polygon([p_B + 0.07*n_inc, p_B + 0.18*u_inc + 0.07*n_inc,
                              p_B + 0.12*u_inc + 0.25*n_inc, p_B + 0.25*n_inc],
                             facecolor='#78909c', edgecolor='#263238', lw=1.5, zorder=6)
    ax_main.add_patch(stop_B)
    ax_main.text(p_B[0] - 0.25, p_B[1] + 0.22, r'$B$', fontsize=13, fontweight='bold', color='#222222')

    # 우측 5° 각도 표시
    ax_main.plot([xR + 0.1, xR + 0.85], [y_deck, y_deck], color='#555555', lw=1.1)
    ax_main.plot([p_topR[0] + 0.1, p_topR[0] + 0.85], [p_topR[1], p_topR[1]], color='#555555', lw=1.1)
    ax_main.text(xR + 0.55, 0.5*(y_deck + p_topR[1]), r'$5^\circ$', fontsize=11, fontweight='bold', ha='center', va='center')

    # 7.5 Mg 차량 (경사면에 100% 밀착 회전 배치)
    s_vis_max = s_max * scale  # 5.4
    s_vis_curr = (s_max - s_curr) * scale
    car_front_dist = 0.18 + s_vis_curr
    car_len, car_h = 1.95, 0.52
    r_wheel = 0.14

    car_mid_dist = car_front_dist + car_len / 2.0
    p_track_mid = p_B + 0.07 * n_inc + car_mid_dist * u_inc

    # 차량 바퀴 2개 (트랙 상면에 정확히 접함: 중심 높이 = r_wheel)
    for dw in [-0.62, 0.62]:
        w_center = p_track_mid + dw * u_inc + r_wheel * n_inc
        cw = patches.Circle(w_center, r_wheel, facecolor='#cce4f0', edgecolor='#1d4564', lw=1.6, zorder=6)
        ax_main.add_patch(cw)
        ax_main.plot(w_center[0], w_center[1], 'ko', markersize=3, zorder=7)

    # 차량 본체 사각형 (바퀴 위쪽에 회전 변환으로 밀착)
    body_center = p_track_mid + (2 * r_wheel + car_h / 2.0 - 0.04) * n_inc
    car_rect = patches.Rectangle((-car_len/2, -car_h/2), car_len, car_h,
                                 facecolor='#e3a891', edgecolor='#6e3520', lw=1.8, zorder=7)
    t_car = plt.matplotlib.transforms.Affine2D().rotate_deg(vis_deg).translate(body_center[0], body_center[1]) + ax_main.transData
    car_rect.set_transform(t_car)
    ax_main.add_patch(car_rect)
    ax_main.text(body_center[0], body_center[1], '7.5 Mg', fontsize=9.8, fontweight='bold',
                 ha='center', va='center', rotation=vis_deg, color='#4a1c0d', zorder=8)

    # 치수선 s = 12 m (초기 출발점 A ~ 정지장치 B)
    pA_ref = p_B + 0.07 * n_inc + (0.18 + s_vis_max) * u_inc
    pB_ref = p_B + 0.07 * n_inc + 0.18 * u_inc
    dim_off = 1.25 * n_inc
    ax_main.plot([pA_ref[0], (pA_ref + dim_off)[0]], [pA_ref[1], (pA_ref + dim_off)[1]], color='#666666', lw=1.0)
    ax_main.plot([pB_ref[0], (pB_ref + dim_off)[0]], [pB_ref[1], (pB_ref + dim_off)[1]], color='#666666', lw=1.0)
    ax_main.annotate('', xy=pB_ref + 1.08*n_inc, xytext=pA_ref + 1.08*n_inc,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    mid_s = 0.5 * (pA_ref + pB_ref) + 1.28 * n_inc
    ax_main.text(mid_s[0], mid_s[1], r'$s = 12\ \mathrm{m}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', rotation=vis_deg)
    ax_main.text((pA_ref + dim_off)[0], (pA_ref + dim_off)[1] + 0.12, r'$A$', fontsize=12, fontweight='bold', ha='center')

    # 속도 벡터 표시 (초록색 표준: 차량 상대속도 ṡ 및 화차 반동속도 v)
    if v_curr > 0.05:
        # 화차 우측 속도 벡터 v (화차 우측 커플러 옆 흰 여백에 깔끔히 배치)
        v_f_start = np.array([xR + 0.18, y_deck - 0.14])
        v_f_end = v_f_start + np.array([0.45 + 0.45 * v_frac, 0.0])
        ax_main.annotate('', xy=v_f_end, xytext=v_f_start,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14), zorder=8)
        ax_main.text(v_f_start[0], v_f_start[1] - 0.25, rf'$v = {v_curr:.3f}\ \mathrm{{m/s}}$',
                     fontsize=10.2, fontweight='bold', color='#2e7d32', ha='left')

        # 차량 경사면 하향 속도 벡터 ṡ (치수선과 겹치지 않도록 차량 전면 중앙에서 배치)
        v_c_start = body_center - (car_len/2 + 0.08) * u_inc
        v_c_end = v_c_start - (0.45 + 0.55 * v_frac) * u_inc
        ax_main.annotate('', xy=v_c_end, xytext=v_c_start,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=8)
        ax_main.text(v_c_end[0] - 0.05, v_c_end[1] + 0.18, rf'$\dot{{s}} = {s_dot_curr:.2f}\ \mathrm{{m/s}}$',
                     fontsize=9.8, fontweight='bold', color='#2e7d32', ha='right',
                     bbox=dict(boxstyle='round,pad=0.10', facecolor='#ffffff', edgecolor='none', alpha=0.85), zorder=9)

    ax_main.set_title(r'문제 4/25: 25 Mg 편평 화차 위 $5^\circ$ 경사로를 활강하는 7.5 Mg 차량', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 우측 패널: 이론 해석 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    sol_box = (
        r"1. 보존계 에너지 보존 ($\Delta T + \Delta V_g = 0$):" "\n"
        r"  $\bullet\ \Delta T_{\mathrm{flatcar}} = \frac{1}{2}(25)(10^3)v^2 = 12,500\,v^2$" "\n"
        r"  $\bullet\ \Delta T_{\mathrm{car}} = \frac{1}{2}(7.5)(10^3)\left[(\dot{s}\cos 5^\circ - v)^2 + (\dot{s}\sin 5^\circ)^2\right]$" "\n"
        r"  $\quad\quad\quad = 3750(v^2 + \dot{s}^2 - 2v\dot{s}\cos 5^\circ)$" "\n"
        r"  $\bullet\ \Delta V_g = -7500(9.81)(12\sin 5^\circ) = -76.95(10^3)\ \mathrm{J}$" "\n"
        r"  $\Rightarrow 16,250\,v^2 + 3750\,\dot{s}^2 - 7500\,v\dot{s}\cos 5^\circ = 76,950\ \ \cdots (1)$" "\n\n"
        r"2. 수평 선운동량 보존 ($\sum F_x = 0 \Rightarrow \Delta G_x = 0$) 및 연립 풀이:" "\n"
        r"  $7.5(10^3)(\dot{s}\cos 5^\circ - v) - 25(10^3)v = 0 \Rightarrow \dot{s}\cos 5^\circ = 4.333\,v\ \ \cdots (2)$" "\n"
        r"  $54,706\,v^2 = 76,950 \Rightarrow v^2 = 1.4066$" "\n"
        r"  $\mathbf{v = 1.186\ \mathrm{m/s}}\quad (\dot{s} = 5.159\ \mathrm{m/s})$"
    )
    ax_calc.text(0.32, 6.0, sol_box, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    live_box = (
        f'차량 활강 거리: $s = {s_curr:.2f}\\ /\\ 12.00\\ \\mathrm{{m}}$  (화차 반동 변위: ${x_flat:.2f}\\ \\mathrm{{m}}$)\n'
        f'현재 속도: 화차 $v = {v_curr:.3f}\\ \\mathrm{{m/s}}$,  차량 상대속력 $\\dot{{s}} = {s_dot_curr:.3f}\\ \\mathrm{{m/s}}$\n'
        f'위치에너지 감소 / 운동에너지 증가: $-\\Delta V_g = {-dVg_curr/1000:.2f}\\ \\mathrm{{kJ}} = \\Delta T$\n'
        f'이론 최종값 ($s = 12\\ \\mathrm{{m}}$): $\\mathbf{{v = 1.186\\ \\mathrm{{m/s}}}}\\ (\\dot{{s}} = 5.159\\ \\mathrm{{m/s}})$'
    )
    ax_calc.text(0.32, 1.45, live_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title(r'이론 해석 및 정량 유도 ($\Delta T + \Delta V_g = 0,\ \Delta G_x = 0$)', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_25_flatcar_incline_car.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
