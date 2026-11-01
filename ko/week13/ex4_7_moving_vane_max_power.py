"""
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
예제 4.7 (Sample Problem 4/7) - 이동 날개에 의해 발생하는 최대 일률 최적 속도 (u = v/3)
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 이론 검증:
  * 단일 날개 일률: P = F*u = rho*A*(v - u)^2 * u * (1 - cos(theta))
  * 극값 조건: dP/du = rho*A*(1 - cos(theta))*(v^2 - 4*u*v + 3*u^2) = 0 -> (v - 3u)(v - u) = 0
  * 최적 속도: u_opt = v / 3 (단일 날개), 참고: 다중 블레이드 터빈 원판(m'=rho*A*v)은 u_opt = v / 2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 물리 파라미터 (정규화 및 수치 예시: rho=1000 kg/m^3, A=0.002 m^2, v=15 m/s, theta=180 deg 반원 버킷 또는 60 deg)
rho = 1000.0
A = 0.002
v = 15.0
theta_deg = 120.0
theta = np.radians(theta_deg)

n_frames = 50
ratio_vals = np.linspace(0.02, 0.98, n_frames)  # u / v

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_vane_curve(x0, y0, R_arc=1.7, th_max=theta):
    ang = np.linspace(-np.pi / 2, -np.pi / 2 + th_max, 40)
    cx, cy = x0, y0 + R_arc
    xs = cx + R_arc * np.cos(ang)
    ys = cy + R_arc * np.sin(ang)
    nx = -np.cos(ang)
    ny = -np.sin(ang)
    return xs, ys, nx, ny


def update(frame):
    r_curr = ratio_vals[frame]
    u_curr = r_curr * v
    phase_t = (frame * 0.09) % 1.0

    # ---------------- 1. 좌측 패널: 물리 메커니즘 + 정규화 일률 곡선 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 10.0)
    ax_main.set_ylim(0, 9.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 상단 절반(y: 4.9 ~ 8.9): 움직이는 날개와 유체 제트 및 추진력 F_fluid -> 일률 P = F*u
    y_jet = 5.8
    x_vane = 2.8 + 2.8 * r_curr
    xs, ys, nx, ny = get_vane_curve(x_vane, y_jet, R_arc=1.55, th_max=theta)
    jet_h = 0.30
    vane_thick = 0.20

    # 노즐
    noz_x0, noz_x1 = 0.5, 1.7
    noz_poly = np.array([
        [noz_x0, y_jet - 0.28],
        [noz_x1, y_jet - jet_h / 2],
        [noz_x1, y_jet + jet_h / 2],
        [noz_x0, y_jet + 0.28]
    ])
    ax_main.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.8, zorder=4))

    # 입사 유체 스트림
    ax_main.fill_between([noz_x1, x_vane], y_jet - jet_h / 2, y_jet + jet_h / 2,
                         color='#bbdefb', alpha=0.85, zorder=2)
    ax_main.plot([noz_x1, x_vane], [y_jet + jet_h / 2, y_jet + jet_h / 2], color='#1976d2', lw=1.2, zorder=3)
    ax_main.plot([noz_x1, x_vane], [y_jet - jet_h / 2, y_jet - jet_h / 2], color='#1976d2', lw=1.2, zorder=3)

    # 날개 위 유체 스트림
    upper_x = xs + (jet_h / 2) * nx
    upper_y = ys + (jet_h / 2) * ny
    lower_x = xs - (jet_h / 2) * nx
    lower_y = ys - (jet_h / 2) * ny
    stream_poly = np.column_stack([
        np.concatenate([lower_x, upper_x[::-1]]),
        np.concatenate([lower_y, upper_y[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(stream_poly, facecolor='#bbdefb', edgecolor='#1976d2', lw=1.2, alpha=0.85, zorder=2))

    # 유체 입자 마커
    for k in range(5):
        frac = ((k / 5.0) + phase_t * (1.0 - r_curr)) % 1.0
        idx = int(frac * (len(xs) - 1))
        ax_main.plot(xs[idx], ys[idx], 'o', color='#0d47a1', markersize=4.2, zorder=4)

    # 곡면 날개 본체
    vane_top_x = xs - (jet_h / 2) * nx
    vane_top_y = ys - (jet_h / 2) * ny
    vane_bot_x = xs - (jet_h / 2 + vane_thick) * nx
    vane_bot_y = ys - (jet_h / 2 + vane_thick) * ny
    vane_poly = np.column_stack([
        np.concatenate([vane_bot_x, vane_top_x[::-1]]),
        np.concatenate([vane_bot_y, vane_top_y[::-1]])
    ])
    ax_main.add_patch(patches.Polygon(vane_poly, facecolor='#78909c', edgecolor='#263238', lw=2.0, zorder=5))

    # 입구 제트 속도 v
    ax_main.annotate('', xy=(noz_x1 + 0.95, y_jet), xytext=(noz_x1 + 0.1, y_jet),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=6)
    ax_main.text(noz_x1 + 0.52, y_jet + 0.26, f'$v = {v:.0f}\\ \\mathrm{{m/s}}$',
                 fontsize=10.2, fontweight='bold', color='#2e7d32', ha='center')

    # 유체가 날개에 가하는 추진력 F (우향) 및 날개 이동 속도 u (우향)
    mid_i = len(xs) // 3
    px_f, py_f = vane_bot_x[mid_i], vane_bot_y[mid_i]
    f_scale = 1.4 * (1.0 - r_curr)**2
    if f_scale > 0.12:
        ax_main.annotate('', xy=(px_f + f_scale + 0.25, py_f), xytext=(px_f + 0.05, py_f),
                         arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=14), zorder=6)
    ax_main.text(px_f + max(f_scale, 0.2) + 0.32, py_f + 0.08, r'$F_{\mathrm{fluid}} = F$',
                 fontsize=10.5, fontweight='bold', color='#d32f2f', va='center')

    u_scale = 1.4 * r_curr
    ax_main.annotate('', xy=(px_f + u_scale + 0.25, py_f - 0.50), xytext=(px_f + 0.05, py_f - 0.50),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=13), zorder=6)
    ax_main.text(px_f + u_scale + 0.32, py_f - 0.50,
                 f'$u = {u_curr:.2f}\\ \\mathrm{{m/s}}\\ ({r_curr:.2f}v)$',
                 fontsize=10.2, fontweight='bold', color='#1565c0', va='center')

    ax_main.text(0.5, 8.55, r'유체가 이동 날개에 전달하는 일률: $P = F \cdot u = \rho A(v-u)^2 u(1-\cos\theta)$',
                 fontsize=10.5, fontweight='bold', color='#1d4564',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f4f8', edgecolor='#b0bec5'))

    # ---------------- 하단 절반(y: 0.6 ~ 4.4): 일률 곡선 P(u/v) 플롯 ----------------
    gx0, gy0 = 1.2, 0.95
    gw, gh = 7.8, 3.25

    # 좌표축 틀
    ax_main.annotate('', xy=(gx0 + gw + 0.3, gy0), xytext=(gx0, gy0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.6))
    ax_main.annotate('', xy=(gx0, gy0 + gh + 0.3), xytext=(gx0, gy0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.6))
    ax_main.text(gx0 + gw + 0.35, gy0, r'$u / v$', fontsize=11, fontweight='bold', va='center')
    ax_main.text(gx0, gy0 + gh + 0.38, r'일률 $P / P_{\max}$', fontsize=10.5, fontweight='bold', ha='center')

    # 단일 날개 곡선: P_norm(r) = (27/4) * (1 - r)^2 * r (최댓값 1.0 at r = 1/3)
    r_grid = np.linspace(0, 1.0, 200)
    p_single_norm = (27.0 / 4.0) * ((1.0 - r_grid)**2) * r_grid
    # 다중 블레이드 터빈 곡선 (비교용 점선): r=1/2에서 최대
    p_turb_norm = 4.0 * (1.0 - r_grid) * r_grid * 0.85

    ax_main.plot(gx0 + r_grid * gw, gy0 + p_single_norm * gh, color='#d32f2f', lw=2.5, label='단일 날개')
    ax_main.plot(gx0 + r_grid * gw, gy0 + p_turb_norm * gh, color='#78909c', ls='--', lw=1.6)

    # 최적점 (u/v = 1/3) 수직 점선 및 마커
    x_opt = gx0 + (1.0 / 3.0) * gw
    y_opt = gy0 + 1.0 * gh
    ax_main.plot([x_opt, x_opt], [gy0, y_opt], color='#2e7d32', ls=':', lw=1.6)
    ax_main.plot(x_opt, y_opt, 'o', color='#2e7d32', markersize=7, zorder=5)
    ax_main.text(x_opt, y_opt + 0.18, r'최대 일률 ($u = \frac{v}{3}$)', fontsize=10.2,
                 fontweight='bold', color='#2e7d32', ha='center')

    # 다중 날개 터빈 최적점 (u/v = 1/2) 표시
    x_turb = gx0 + 0.5 * gw
    y_turb = gy0 + 0.85 * gh
    ax_main.plot([x_turb, x_turb], [gy0, y_turb], color='#607d8b', ls=':', lw=1.2)
    ax_main.text(x_turb + 0.15, y_turb + 0.08, r'다중 날개 터빈 ($u = \frac{v}{2}$)',
                 fontsize=9.2, color='#455a64', fontweight='bold')

    # x축 눈금 레이블
    for rv, lbl in [(0.0, '0'), (1.0/3.0, '1/3'), (0.5, '1/2'), (1.0, '1.0')]:
        xp = gx0 + rv * gw
        ax_main.plot([xp, xp], [gy0 - 0.08, gy0 + 0.08], color='#222222', lw=1.3)
        ax_main.text(xp, gy0 - 0.32, lbl, fontsize=9.8, fontweight='bold', ha='center')

    # 현재 상태 점 마커
    p_curr_norm = (27.0 / 4.0) * ((1.0 - r_curr)**2) * r_curr
    xc = gx0 + r_curr * gw
    yc = gy0 + p_curr_norm * gh
    ax_main.plot([xc, xc], [gy0, yc], color='#1565c0', lw=1.4, alpha=0.7)
    ax_main.plot(xc, yc, 'o', color='#1565c0', markersize=8.5, zorder=6)

    ax_main.set_title('예제 4.7: 이동 날개의 최대 일률 최적 속도 ($u = v / 3$)', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 미분 유도 및 실시간 물리량 모니터 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단: 물리적 트레이드오프 다이어그램 (힘 F 감소 vs 속도 u 증가)
    ax_calc.text(5.0, 9.45, '일률 형성 메커니즘 ($P = F \\cdot u$) 및 극값 조건',
                 fontsize=11.5, fontweight='bold', ha='center', color='#1d4564')

    box_top = (
        "• 일률(Power) 정의: 수직력 " + r"$R$" + "은 운동 방향(" + r"$+x$" + ")에 수직이므로 " + r"$U_R = 0$" + "\n"
        r"   유체가 날개를 미는 힘 $F$에 의해 발생되는 일률:" + "\n"
        r"   $P = F u = \rho A(v - u)^2 u (1 - \cos\theta)$"
    )
    ax_calc.text(5.0, 8.20, box_top, fontsize=9.8, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8f9fa', edgecolor='#cfd8dc'))

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (" + r"$dP / du = 0$" + ")]\n"
        r"1) 일률 함수 전개:" + "\n"
        r"   $P(u) = \rho A(1 - \cos\theta)(v^2 u - 2 v u^2 + u^3)$" + "\n"
        r"2) 속도 $u$에 대한 미분 극값 조건 ($\frac{dP}{du} = 0$):" + "\n"
        r"   $\frac{dP}{du} = \rho A(1 - \cos\theta)(v^2 - 4 u v + 3 u^2) = 0$" + "\n"
        r"   $\Rightarrow (v - 3u)(v - u) = 0$" + "\n"
        r"3) 최적 속도 및 최대 일률 (단일 날개):" + "\n"
        "   " + r"$\mathbf{u_{\mathrm{opt}} = \frac{v}{3}}$" + "   (" + r"$u = v$" + "는 " + r"$P = 0$" + "인 최소치 조건)\n"
        r"   $P_{\max} = \frac{4}{27}\rho A v^3(1 - \cos\theta)$  (참고: 다중 날개 터빈은 $u = \frac{v}{2}$)"
    )
    ax_calc.text(5.0, 4.90, sol_text, fontsize=9.8, ha='center', va='center', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    F_curr = rho * A * (v - u_curr)**2 * (1.0 - np.cos(theta))
    P_curr = F_curr * u_curr
    P_max = (4.0 / 27.0) * rho * A * (v**3) * (1.0 - np.cos(theta))
    dP_du = rho * A * (1.0 - np.cos(theta)) * (v**2 - 4.0 * u_curr * v + 3.0 * u_curr**2)

    live_text = (
        f"[실시간 물리량 모니터 ($v={v:.1f}\\ \\mathrm{{m/s}},\\ u_{{\\mathrm{{opt}}}} = v/3 = {v/3:.2f}\\ \\mathrm{{m/s}}$)]\n"
        f"현재 날개 속도: $u = {u_curr:.2f}\\ \\mathrm{{m/s}}$ ($u/v = {r_curr:.2f}$)  |  작용력: $F = {F_curr:.1f}\\ \\mathrm{{N}}$\n"
        f"현재 발생 일률: $P = {P_curr/1000:.2f}\\ \\mathrm{{kW}}$ (이론 최댓값 $P_{{\\max}} = {P_max/1000:.2f}\\ \\mathrm{{kW}}$의 {p_curr_norm*100:.1f}%)\n"
        f"기울기: $dP/du = {dP_du:+.1f}\\ \\mathrm{{N}}$  $\\rightarrow$  이론 최종값: $\\mathbf{{u = v/3}}$"
    )
    ax_calc.text(5.0, 1.30, live_text, fontsize=9.5, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_7_moving_vane_max_power.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
