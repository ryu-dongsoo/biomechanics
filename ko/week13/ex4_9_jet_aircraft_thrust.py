"""
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
예제 4.9 (Sample Problem 4/9) - 공기흡입식 제트기(Air-Breathing Jet Aircraft)의 운동방정식 및 추진력 T
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 이론 검증:
  * 이동 좌표계(비행기 기준 +x 전방):
    - 공기 유량 m'_a: Delta v_a = -u - (-v) = -(u - v)
    - 연료 유량 m'_f: Delta v_f = -u - 0 = -u
    - 배기가스 유량: m'_g = m'_a + m'_f
  * 힘-운동량 방정식: -m*g*sin(theta) - D = -m'_a*(u - v) - m'_f*u = -m'_g*u + m'_a*v
  * 유효 추진력(Thrust): T = m'_g*u - m'_a*v  (근사식: m'_g ~= m'_a 일 때 T ~= m'_g*(u - v))
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 물리 파라미터 (정량 검증용 표준 제트기 제원)
m = 8000.0            # 비행기 질량 (8 Mg)
g = 9.81
v = 250.0             # 비행 속력 (250 m/s = 900 km/h)
u = 750.0             # 배기가스 상대속도 (750 m/s)
m_dot_a = 80.0        # 공기 흡입률 (80 kg/s)
m_dot_f = 1.6         # 연료 소모율 (1.6 kg/s, m'_a의 2%)
m_dot_g = m_dot_a + m_dot_f  # 81.6 kg/s
theta_deg = 12.0      # 상승 비행 앙각 (deg)
theta = np.radians(theta_deg)

# 추진력 T 및 평형 항력 D
T_exact = m_dot_g * u - m_dot_a * v          # 81.6*750 - 80*250 = 61200 - 20000 = 41,200 N (41.2 kN)
T_approx = m_dot_g * (u - v)                 # 81.6*500 = 40,800 N (40.8 kN)
D_eq = T_exact - m * g * np.sin(theta)       # 평형 항력

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_jet_polygon(cx, cy, scale=1.0, ang_deg=theta_deg):
    """교재 그림 스타일 제트 항공기 측면 실루엣 좌표 생성"""
    # 기준 자세 (수평 +x 전방, 중심 (0,0))
    body = np.array([
        [2.6, 0.0],     # 기수 노즈콘
        [1.5, 0.25],    # 캐노피 앞
        [0.8, 0.42],    # 캐노피 정점
        [0.1, 0.30],    # 캐노피 뒤
        [-1.6, 0.28],   # 동체 상단 뒤
        [-2.3, 0.95],   # 수직미익 앞전 상단
        [-2.65, 0.95],  # 수직미익 뒷전 상단
        [-2.45, 0.25],  # 수직미익 하단
        [-2.55, 0.14],  # 배기 노즐 상단
        [-2.55, -0.14], # 배기 노즐 하단
        [-1.8, -0.22],  # 동체 하단 뒤
        [0.4, -0.26],   # 공기 흡입구 하단
        [0.7, -0.12],   # 흡입구 립
        [1.6, -0.15],   # 기수 하단
    ]) * scale

    wing = np.array([
        [0.3, -0.05],
        [-0.9, -0.18],
        [-1.3, -0.05],
        [0.1, 0.05]
    ]) * scale

    canopy = np.array([
        [1.45, 0.22],
        [0.8, 0.39],
        [0.18, 0.28],
        [0.8, 0.18]
    ]) * scale

    rad = np.radians(ang_deg)
    R_mat = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])

    body_rot = body @ R_mat.T + np.array([cx, cy])
    wing_rot = wing @ R_mat.T + np.array([cx, cy])
    canopy_rot = canopy @ R_mat.T + np.array([cx, cy])
    return body_rot, wing_rot, canopy_rot, R_mat


def update(frame):
    phase_t = (frame * 0.08) % 1.0
    # 비행기가 앙각 theta 방향으로 완만하게 순항 전진하는 모션
    s_flight = -0.45 + 0.90 * (frame / (n_frames - 1))
    tx, ty = np.cos(theta), np.sin(theta)
    nx, ny = -np.sin(theta), np.cos(theta)

    cx = 4.9 + s_flight * tx
    cy = 4.6 + s_flight * ty

    # ---------------- 1. 좌측 패널: 제트기 정상 질량유동 및 외력 메커니즘 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(1.2, 8.0)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 비행 경로 기준선 (x축) 및 수평 기준선 (앙각 theta)
    p_base = np.array([cx, cy]) - 3.6 * np.array([tx, ty])
    p_front = np.array([cx, cy]) + 3.8 * np.array([tx, ty])
    ax_main.plot([p_base[0], p_front[0]], [p_base[1], p_front[1]], color='#90a4ae', ls='--', lw=1.2, zorder=1)
    ax_main.text(p_front[0] + 0.15, p_front[1] + 0.05, r'$x$', fontsize=11, fontweight='bold', color='#546e7a')

    # 수평선 및 각도 theta 표시 (우측 전방)
    ang_pivot = np.array([cx, cy]) + 1.8 * np.array([tx, ty])
    ax_main.plot([ang_pivot[0], ang_pivot[0] + 1.6], [ang_pivot[1], ang_pivot[1]], color='#777777', ls=':', lw=1.2)
    arc_th = patches.Arc(ang_pivot, 1.3, 1.3, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.4)
    ax_main.add_patch(arc_th)
    ax_main.text(ang_pivot[0] + 0.92, ang_pivot[1] + 0.14, r'$\theta = 12^\circ$', fontsize=9.8, fontweight='bold')

    # 제트기 본체 그리기
    body_pts, wing_pts, canopy_pts, R_mat = get_jet_polygon(cx, cy, scale=1.05, ang_deg=theta_deg)
    ax_main.add_patch(patches.Polygon(body_pts, facecolor='#cfd8dc', edgecolor='#263238', lw=1.9, zorder=4))
    ax_main.add_patch(patches.Polygon(wing_pts, facecolor='#90a4ae', edgecolor='#263238', lw=1.5, zorder=5))
    ax_main.add_patch(patches.Polygon(canopy_pts, facecolor='#81d4fa', edgecolor='#0277bd', lw=1.4, zorder=5))

    # 배기 화염 및 배기가스 제트 유선 (뒤쪽 -x 방향 상대속도 u)
    noz_pos = np.array([cx, cy]) + R_mat @ np.array([-2.68, 0.0])
    for dy_off in [-0.12, 0.0, 0.12]:
        p_start = noz_pos + dy_off * np.array([nx, ny])
        p_end = p_start - 1.35 * np.array([tx, ty])
        ax_main.annotate('', xy=p_end, xytext=p_start,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=3)
    ax_main.text(noz_pos[0] - 0.95 * tx + 0.35 * nx, noz_pos[1] - 0.95 * ty + 0.35 * ny,
                 r"배기가스 $m'_g,\ u$", fontsize=9.8, fontweight='bold', color='#00695c', ha='center')

    # 흡입 공기 유선 (앞쪽에서 흡입구로 유입 m'_a)
    intake_pos = np.array([cx, cy]) + R_mat @ np.array([0.85, -0.18])
    for k in range(3):
        frac = ((k / 3.0) + phase_t) % 1.0
        pt_air = intake_pos + (1.2 - frac * 1.0) * np.array([tx, ty])
        ax_main.plot(pt_air[0], pt_air[1], 'o', color='#0288d1', markersize=4.0, zorder=5)

    # 비행 속도 벡터 v (초록색, 기체 상단 전방)
    v_orig = np.array([cx, cy]) + 0.55 * np.array([nx, ny]) + 0.4 * np.array([tx, ty])
    v_end = v_orig + 1.45 * np.array([tx, ty])
    ax_main.annotate('', xy=v_end, xytext=v_orig,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(0.5 * (v_orig[0] + v_end[0]) - 0.1, 0.5 * (v_orig[1] + v_end[1]) + 0.25,
                 f'$v = {v:.0f}\\ \\mathrm{{m/s}}$', fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')

    # 외력 벡터들 (붉은색: 중력 mg, 양력 L, 항력 D, 그리고 유효 추진력 T)
    cg = np.array([cx, cy])
    # 1) 중력 mg (위에서 중심을 향해 수직 하향, 교재 그림 스타일)
    ax_main.annotate('', xy=cg + np.array([0, 0.32]), xytext=cg + np.array([0, 1.85]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(cg[0] + 0.15, cg[1] + 1.75, r'$mg$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    # 2) 양력 L (아래에서 위로 비행 수직 방향 +y)
    ax_main.annotate('', xy=cg - 0.25 * np.array([nx, ny]), xytext=cg - 1.85 * np.array([nx, ny]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(cg[0] - 1.75 * nx + 0.22, cg[1] - 1.75 * ny, r'$L$', fontsize=11.5, fontweight='bold', color='#d32f2f')

    # 3) 항력 D (전방에서 후방 -x 방향)
    d_pt = cg + 1.25 * np.array([tx, ty]) - 0.38 * np.array([nx, ny])
    ax_main.annotate('', xy=d_pt, xytext=d_pt + 1.25 * np.array([tx, ty]),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax_main.text(d_pt[0] + 0.75 * tx, d_pt[1] + 0.75 * ty - 0.32, r'$D$', fontsize=11.5, fontweight='bold', color='#d32f2f')

    # 하단 모델 비교 배너 (유효 추진력 T = m'_g u - m'_a v)
    banner_text = (
        "유효 추진력(Thrust) 모델: 배기가스 반력 (" + r"$+m'_g u$" + ") - 공기 흡입 저항 (" + r"$-m'_a v$" + ")  "
        + r"$\Rightarrow\ \mathbf{T = m'_g u - m'_a v}$"
    )
    ax_main.text(4.9, 1.75, banner_text, fontsize=10.0, fontweight='bold', color='#1d4564', ha='center',
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    ax_main.set_title('예제 4.9: 공기흡입식 제트기의 운동방정식 및 추진력 $T$', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 등가 추력 모델 비교 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단(y: 6.8 ~ 9.6): 내부 유동 작용력 모델 vs 외부 등가 추진력 T 모델 다이어그램
    ax_calc.text(5.0, 9.50, '제트엔진 내부 유동 힘 모델 vs. 외부 등가 추진력($T$) 모델',
                 fontsize=11.2, fontweight='bold', ha='center', color='#1d4564')

    # 좌측 미니 카드: 내부 유동 힘 (m'_g u 전방, m'_a v 후방)
    ax_calc.add_patch(patches.FancyBboxPatch((0.4, 6.85), 4.2, 2.2, boxstyle='round,pad=0.15',
                                             facecolor='#fff8e1', edgecolor='#ffb300', lw=1.4))
    ax_calc.text(2.5, 8.75, '① 내부 경계면 노출 모델', fontsize=10.0, fontweight='bold', ha='center', color='#e65100')
    ax_calc.annotate('', xy=(2.3, 7.95), xytext=(0.8, 7.95),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.3, mutation_scale=13))
    ax_calc.text(1.55, 8.22, r"$m'_g u$ (배기 추력)", fontsize=9.3, fontweight='bold', color='#d32f2f', ha='center')
    ax_calc.annotate('', xy=(2.7, 7.35), xytext=(4.2, 7.35),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=13))
    ax_calc.text(3.45, 7.62, r"$m'_a v$ (램 항력)", fontsize=9.3, fontweight='bold', color='#1565c0', ha='center')

    # 우측 미니 카드: 외부 가상 추진력 T 모델
    ax_calc.add_patch(patches.FancyBboxPatch((5.4, 6.85), 4.2, 2.2, boxstyle='round,pad=0.15',
                                             facecolor='#e8f5e9', edgecolor='#43a047', lw=1.4))
    ax_calc.text(7.5, 8.75, '② 등가 추진력($T$) 모델', fontsize=10.0, fontweight='bold', ha='center', color='#1b5e20')
    ax_calc.annotate('', xy=(8.6, 7.85), xytext=(6.2, 7.85),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(7.4, 8.18, r"$T = m'_g u - m'_a v$", fontsize=10.0, fontweight='bold', color='#2e7d32', ha='center')
    ax_calc.text(7.5, 7.20, r"$T - mg\sin\theta - D = m\dot{v}$", fontsize=9.5, fontweight='bold', color='#263238', ha='center')

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (이동 좌표계 " + r"$\Sigma F_x = m'\Delta v_x$" + ")]\n"
        "• 공기 유동 (" + r"$m'_a$" + "): " + r"$\Delta v_a = (-u) - (-v) = -(u - v)$" + "\n"
        "• 연료 유동 (" + r"$m'_f$" + "): " + r"$\Delta v_f = (-u) - 0 = -u \quad (m'_g = m'_a + m'_f)$" + "\n"
        "• 비행 방향 운동량 방정식:\n"
        r"   $-mg\sin\theta - D = -m'_a(u - v) - m'_f u = -m'_g u + m'_a v$" + "\n"
        "• 추진력(Thrust) 엄밀해 및 근사식 (" + r"$m'_f \ll m'_a \Rightarrow m'_g \cong m'_a$" + "):\n"
        "   " + r"$\mathbf{T = m'_g u - m'_a v}$" + "     및     " + r"$\mathbf{T \cong m'_g(u - v)}$"
    )
    ax_calc.text(5.0, 4.30, sol_text, fontsize=9.5, ha='center', va='center', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.48', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    gross_thrust = m_dot_g * u
    ram_drag = m_dot_a * v
    err_pct = abs(T_exact - T_approx) / T_exact * 100.0

    live_text = (
        f"[정량 수치 검증 ($m'_a={m_dot_a:.0f}\\ \\mathrm{{kg/s}},\\ m'_f={m_dot_f:.1f}\\ \\mathrm{{kg/s}},\\ "
        f"v={v:.0f}\\ \\mathrm{{m/s}},\\ u={u:.0f}\\ \\mathrm{{m/s}}$)]\n"
        f"배기 총추력: $m'_g u = {gross_thrust/1000:.2f}\\ \\mathrm{{kN}}$  |  흡입 램 항력: $m'_a v = {ram_drag/1000:.2f}\\ \\mathrm{{kN}}$\n"
        f"이론 엄밀 추력: $\\mathbf{{T = {T_exact/1000:.2f}\\ \\mathrm{{kN}}}}$  |  "
        f"근사 추력: $T \\cong m'_g(u-v) = {T_approx/1000:.2f}\\ \\mathrm{{kN}}$ (차이 {err_pct:.2f}%)"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.3, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_9_jet_aircraft_thrust.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
