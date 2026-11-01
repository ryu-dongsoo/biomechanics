"""
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
문제 4/37 (Problem 4/37) - 물줄기(20 m/s)를 거슬러 왼쪽(10 m/s)으로 운동하는 90도 날개의 지지력 Fx, Fy
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 정량 검증:
  * 노즐 지름 d = 25 mm = 0.025 m, 물줄기 속력 v = 20 m/s (우향), 날개 속력 u = 10 m/s (좌향, +x 방향)
  * 상대속력 v_rel = v + u = 20 + 10 = 30 m/s
  * 유효 질량유량 m' = rho * A * v_rel = 1000 * (pi/4)*(0.025)^2 * (20 + 10) = 14.726 kg/s (~= 14.73 kg/s)
  * 출구 절대속도: v'_x = +u = +10 m/s (좌향), v'_y = +v_rel = +30 m/s (상향)
  * Sigma F_x = m' * Delta v_x -> F_x = 14.726 * (10 - (-20)) = 441.8 N -> F_x = 442 N
  * Sigma F_y = m' * Delta v_y -> F_y = 14.726 * (20 + 10 - 0) = 441.8 N -> F_y = 442 N
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터
rho = 1000.0
d = 0.025
A = 0.25 * np.pi * d**2      # 4.9087e-4 m^2
v_jet = 20.0                 # 우향 물줄기 속력 (m/s)
u_vane = 10.0                # 좌향 날개 이동 속력 (m/s)
v_rel = v_jet + u_vane       # 30.0 m/s
m_dot = rho * A * v_rel      # 14.7262 kg/s (~= 14.73 kg/s)

Fx_val = m_dot * (u_vane - (-v_jet))  # 441.79 N -> 442 N
Fy_val = m_dot * (v_rel - 0.0)        # 441.79 N -> 442 N

n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_90deg_vane_shapes(x_lip, y_jet, R_arc=2.15, jet_h=0.38):
    """교재 문제 4/37의 90도 곡면 웨지 블록(갈색) + 녹색 라이너 + 청색 수류 폴리곤 생성"""
    # 원호 중심: (x_lip, y_jet + R_arc - jet_h/2), 각도 -pi/2 -> 0
    r_water_center = R_arc
    cx, cy = x_lip, y_jet + r_water_center
    ang = np.linspace(-np.pi / 2, 0.0, 40)

    # 수류 내측/외측 경계 (cx, cy 기준 반경 r_in = R_arc - jet_h/2, r_out = R_arc + jet_h/2)
    r_in = R_arc - jet_h / 2
    r_out = R_arc + jet_h / 2
    xw_in = cx + r_in * np.cos(ang)
    yw_in = cy + r_in * np.sin(ang)
    xw_out = cx + r_out * np.cos(ang)
    yw_out = cy + r_out * np.sin(ang)

    # 녹색 곡면 라이너 (r_out -> r_liner = r_out + 0.14)
    r_liner = r_out + 0.14
    xl_out = cx + r_liner * np.cos(ang)
    yl_out = cy + r_liner * np.sin(ang)
    liner_poly = np.vstack([
        np.column_stack([xw_out, yw_out]),
        np.column_stack([xl_out[::-1], yl_out[::-1]])
    ])

    # 황갈색 웨지 블록 (외측 직각 모서리: x_back = cx + r_liner + 0.38, y_bot = y_jet - jet_h/2 - 0.42)
    x_back = cx + r_liner + 0.38
    y_bot = y_jet - jet_h / 2 - 0.42
    y_top = cy
    block_poly = np.vstack([
        [x_lip, y_bot],
        [x_back, y_bot],
        [x_back, y_top],
        [cx + r_liner, y_top],
        np.column_stack([xl_out[::-1], yl_out[::-1]])
    ])

    return (cx, cy, r_in, r_out, xw_in, yw_in, xw_out, yw_out, liner_poly, block_poly, x_back, y_bot, y_top)


def update(frame):
    phase_t = (frame * 0.09) % 1.0
    # 날개가 오른쪽(x=4.8)에서 왼쪽(x=3.5)으로 물줄기를 거슬러 전진하는 모션
    x_lip = 4.85 - 1.25 * (frame / (n_frames - 1))
    y_jet = 2.65
    jet_h = 0.38
    R_arc = 2.10

    (cx, cy, r_in, r_out, xw_in, yw_in, xw_out, yw_out,
     liner_poly, block_poly, x_back, y_bot, y_top) = get_90deg_vane_shapes(x_lip, y_jet, R_arc, jet_h)

    # ---------------- 1. 좌측 패널: 90도 이동 날개 물리 거동 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(0.8, 7.6)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 좌표축 점선 (좌측 +x, 상단 +y — 교재 원도 동일)
    ax_main.plot([0.65, 2.1], [y_jet, y_jet], color='#555555', ls='--', lw=1.2, zorder=1)
    ax_main.text(0.48, y_jet, r'$x$', fontsize=11.5, fontweight='bold', va='center')
    x_exit_center = cx + 0.5 * (r_in + r_out)
    ax_main.plot([x_exit_center, x_exit_center], [y_top + 0.2, 7.15], color='#555555', ls='--', lw=1.2, zorder=1)
    ax_main.text(x_exit_center, 7.30, r'$y$', fontsize=11.5, fontweight='bold', ha='center')

    # 1) 좌측 황동 노즐 (x: 1.45 -> 2.75, 오른쪽으로 20 m/s 물줄기 분사)
    noz_x0, noz_x1 = 1.45, 2.75
    noz_poly = np.array([
        [noz_x0, y_jet - 0.30],
        [noz_x1, y_jet - jet_h / 2],
        [noz_x1, y_jet + jet_h / 2],
        [noz_x0, y_jet + 0.30]
    ])
    ax_main.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.9, zorder=4))
    ax_main.add_patch(patches.Ellipse((noz_x0, y_jet), 0.14, 0.60, facecolor='#b8860b', edgecolor='#5c4811', lw=1.5, zorder=5))

    # 2) 수평 입사 물줄기 + 곡면 물줄기 + 상단 수직 방출 물줄기
    ax_main.fill_between([noz_x1, x_lip], y_jet - jet_h / 2, y_jet + jet_h / 2,
                         color='#cce7f8', alpha=0.88, zorder=2)
    ax_main.plot([noz_x1, x_lip], [y_jet + jet_h / 2, y_jet + jet_h / 2], color='#90caf9', lw=1.2, zorder=3)
    ax_main.plot([noz_x1, x_lip], [y_jet - jet_h / 2, y_jet - jet_h / 2], color='#90caf9', lw=1.2, zorder=3)

    # 곡면 및 상단 연장 수류 폴리곤
    y_plume_top = y_top + 1.45
    stream_poly = np.vstack([
        np.column_stack([xw_in, yw_in]),
        [cx + r_in, y_plume_top],
        [cx + r_out, y_plume_top],
        np.column_stack([xw_out[::-1], yw_out[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(stream_poly, facecolor='#cce7f8', edgecolor='#90caf9', lw=1.1, alpha=0.88, zorder=2))

    # 3) 날개 블록(황갈색) 및 녹색 곡면 라이너 그리기 (교재 원도 컬러 완벽 반영)
    ax_main.add_patch(patches.Polygon(block_poly, facecolor='#e2b49a', edgecolor='#3e2723', lw=1.8, zorder=4))
    ax_main.add_patch(patches.Polygon(liner_poly, facecolor='#81b29a', edgecolor='#1b4332', lw=1.6, zorder=5))

    # 4) 수류 내부 속도 화살표 (초록색) 및 이동 물 입자 애니메이션
    # 입구 수평 화살표 (20 m/s)
    x_arr_in = 0.5 * (noz_x1 + x_lip)
    ax_main.annotate('', xy=(x_arr_in + 0.42, y_jet), xytext=(x_arr_in - 0.42, y_jet),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.2, mutation_scale=13), zorder=5)
    ax_main.text(x_arr_in + 0.15, y_jet + 0.52, r'$20\ \mathrm{m/s}$', fontsize=11, fontweight='bold', color='#111111')
    # 지시 곡선
    ax_main.annotate('', xy=(x_arr_in - 0.05, y_jet + 0.06), xytext=(x_arr_in + 0.12, y_jet + 0.48),
                     arrowprops=dict(arrowstyle='-', color='#333333', lw=0.9, connectionstyle='arc3,rad=0.25'), zorder=5)

    # 곡면 위 초록 화살표 2개
    for ang_deg_a in [-65, -25]:
        a1 = np.radians(ang_deg_a - 12)
        a2 = np.radians(ang_deg_a + 12)
        rm = 0.5 * (r_in + r_out)
        p1 = np.array([cx + rm * np.cos(a1), cy + rm * np.sin(a1)])
        p2 = np.array([cx + rm * np.cos(a2), cy + rm * np.sin(a2)])
        ax_main.annotate('', xy=p2, xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.1, mutation_scale=12,
                                         connectionstyle='arc3,rad=0.2'), zorder=5)

    # 물 입자 이동 마커
    rm = 0.5 * (r_in + r_out)
    for k in range(6):
        s_p = ((k / 6.0) + phase_t) % 1.0
        ang_p = -np.pi / 2 + s_p * (np.pi / 2)
        ax_main.plot(cx + rm * np.cos(ang_p), cy + rm * np.sin(ang_p), 'o', color='#0277bd', markersize=4.5, zorder=6)

    # 5) 날개 하단 좌향 이동 속도 화살표 (10 m/s, 초록색)
    ax_main.annotate('', xy=(x_lip + 0.05, y_bot - 0.25), xytext=(x_lip + 0.95, y_bot - 0.25),
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13), zorder=6)
    ax_main.text(x_lip + 0.50, y_bot - 0.62, r'$10\ \mathrm{m/s}$', fontsize=11, fontweight='bold', color='#111111', ha='center')

    # 6) 날개에 가해지는 지지 외력 Fx (좌향, 우측면에서 밀어줌) 및 Fy (상향, 바닥면에서 밀어줌)
    ax_main.annotate('', xy=(x_back, y_bot + 0.65), xytext=(x_back + 1.25, y_bot + 0.65),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=16), zorder=6)
    ax_main.text(x_back + 1.32, y_bot + 0.65, r'$F_x = 442\ \mathrm{N}$',
                 fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    x_fy = x_back - 0.55
    ax_main.annotate('', xy=(x_fy, y_bot), xytext=(x_fy, y_bot - 1.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=16), zorder=6)
    ax_main.text(x_fy, y_bot - 1.38, r'$F_y = 442\ \mathrm{N}$',
                 fontsize=11.5, fontweight='bold', color='#d32f2f', ha='center')

    ax_main.set_title('문제 4/37: 물줄기를 거슬러 전진하는 $90^\\circ$ 날개의 지지력', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 출구 속도 합성 삼각형 및 정량 유도 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단(y: 6.5 ~ 9.6): 출구 절대속도 합성 선도 (v' = u + v_rel)
    ax_calc.text(5.0, 9.50, r"출구 절대속도 합성 ($\mathbf{v}' = \mathbf{u} + \mathbf{v}_{\mathrm{rel}}$) 및 상대 유입 유량",
                 fontsize=11.0, fontweight='bold', ha='center', color='#1d4564')

    # 속도 직각삼각형: 아래변 u = 10 m/s (좌향 +x), 오른쪽 수직변 v_rel = v + u = 30 m/s (상향 +y), 대각선 v' (좌상향)
    p_br = np.array([5.8, 6.75])   # 우하단 기준점
    p_bl = np.array([3.8, 6.75])   # 좌하단 (u = 10 m/s 좌향 끝)
    p_tl = np.array([3.8, 9.05])   # 좌상단 (v' 끝점)
    p_tr = np.array([5.8, 9.05])   # 우상단 (v_rel = v+u 끝점)

    # 보조 사각형 점선
    ax_calc.plot([p_bl[0], p_tl[0]], [p_bl[1], p_tl[1]], color='#90a4ae', ls='--', lw=1.2)
    ax_calc.plot([p_tl[0], p_tr[0]], [p_tl[1], p_tr[1]], color='#90a4ae', ls='--', lw=1.2)

    # u 벡터 (좌향)
    ax_calc.annotate('', xy=p_bl, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=13))
    ax_calc.text(4.8, 6.42, r'$u = 10\ \mathrm{m/s}\ (+x)$', fontsize=10.0, fontweight='bold', color='#1565c0', ha='center')

    # v_rel = v + u 벡터 (상향)
    ax_calc.annotate('', xy=p_tr, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=13))
    ax_calc.text(6.05, 7.90, r'$v_{\mathrm{rel}} = v + u = 30\ \mathrm{m/s}\ (+y)$',
                 fontsize=10.0, fontweight='bold', color='#00897b', va='center')

    # v' 절대속도 벡터 (좌상향 대각선)
    ax_calc.annotate('', xy=p_tl, xytext=p_br,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(4.25, 8.15, r"$\mathbf{v}'$", fontsize=11.5, fontweight='bold', color='#2e7d32', ha='right')

    # 좌측 좌표축 기호 (+x 좌향, +y 상향)
    ax_calc.annotate('', xy=(1.2, 7.2), xytext=(2.4, 7.2),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))
    ax_calc.text(1.0, 7.2, r'$+x$', fontsize=10, fontweight='bold', va='center', ha='right')
    ax_calc.annotate('', xy=(2.4, 8.4), xytext=(2.4, 7.2),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))
    ax_calc.text(2.4, 8.55, r'$+y$', fontsize=10, fontweight='bold', ha='center')

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (" + r"$v_{\mathrm{rel}} = v + u$" + ")]\n"
        r"1) 날개에 대한 물의 상대속력 및 유효 질량유량 ($m'$):" + "\n"
        r"   $v_{\mathrm{rel}} = v + u = 20 + 10 = 30\ \mathrm{m/s}$" + "\n"
        r"   $m' = \rho A v_{\mathrm{rel}} = 1000\left(\frac{\pi}{4}\right)(0.025)^2(20 + 10) = \mathbf{14.73\ \mathrm{kg/s}}$" + "\n"
        r"2) 출구 절대속도 성분 ($\mathbf{v}' = \mathbf{u} + \mathbf{v}_{\mathrm{rel}}$, 좌측 $+x$, 상향 $+y$):" + "\n"
        r"   입구: $v_{1x} = -20\ \mathrm{m/s},\ v_{1y} = 0$  |  출구: $v'_{x} = +10\ \mathrm{m/s},\ v'_{y} = +30\ \mathrm{m/s}$" + "\n"
        r"3) 힘-선운동량 방정식 ($\Sigma F = m'\Delta v$):" + "\n"
        r"   $\Sigma F_x = m'\Delta v_x:\ F_x = 14.73(10 - [-20]) = \mathbf{442\ \mathrm{N}}$" + "\n"
        r"   $\Sigma F_y = m'\Delta v_y:\ F_y = 14.73(20 + 10 - 0) = \mathbf{442\ \mathrm{N}}$"
    )
    ax_calc.text(5.0, 3.90, sol_text, fontsize=9.4, ha='center', va='center', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    live_text = (
        f"[정량 검증 요약 ($d = 25\\ \\mathrm{{mm}},\\ v = 20\\ \\mathrm{{m/s}},\\ u = 10\\ \\mathrm{{m/s}}$)]\n"
        f"상대 유입 유량: $m' = {m_dot:.2f}\\ \\mathrm{{kg/s}}$  |  속도 변화: $\\Delta v_x = +30\\ \\mathrm{{m/s}},\\ \\Delta v_y = +30\\ \\mathrm{{m/s}}$\n"
        f"이론 최종값: $\\mathbf{{F_x = {Fx_val:.0f}\\ \\mathrm{{N}}}}$,   $\\mathbf{{F_y = {Fy_val:.0f}\\ \\mathrm{{N}}}}$"
    )
    ax_calc.text(5.0, 1.05, live_text, fontsize=9.5, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.42', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_37_moving_90deg_vane.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
