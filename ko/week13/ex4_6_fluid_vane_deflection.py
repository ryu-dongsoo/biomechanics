"""
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
예제 4.6 (Sample Problem 4/6) - 매끄러운 날개에 의한 개방유동 방향 전환 (고정 날개 vs. 이동 날개)
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 이론 검증:
  (a) 고정 날개 (u = 0): F = rho*A*v^2*(1 - cos(theta)), R = rho*A*v^2*sin(theta)
  (b) 이동 날개 (u < v): m' = rho*A*(v - u), F = rho*A*(v - u)^2*(1 - cos(theta)), R = rho*A*(v - u)^2*sin(theta)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 물리 파라미터 (정량 시각화용 표준 제원: rho=1000 kg/m^3, A=0.002 m^2, v=20 m/s, theta=60 deg)
rho = 1000.0
A = 0.002
v = 20.0
theta_deg = 60.0
theta = np.radians(theta_deg)

# 총 48 프레임: 전반부(0~19) 고정 날개 u=0, 후반부(20~47) 이동 날개 u=6 m/s (u/v = 0.3)
n_frames = 48

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def get_vane_curve(x0, y0, R_arc=2.4, th_max=theta):
    """원호 곡면 날개 좌표 생성 (접선 각도 0 -> theta)"""
    # 중심 (x0, y0 + R_arc), 각도 -pi/2 ~ -pi/2 + th_max
    ang = np.linspace(-np.pi / 2, -np.pi / 2 + th_max, 40)
    cx, cy = x0, y0 + R_arc
    xs = cx + R_arc * np.cos(ang)
    ys = cy + R_arc * np.sin(ang)
    nx = -np.cos(ang)
    ny = -np.sin(ang)
    return xs, ys, nx, ny


def draw_vane_and_stream(ax, x_vane, y_vane, u_val, phase_t, label_title, is_moving=False):
    R_arc = 2.2
    xs, ys, nx, ny = get_vane_curve(x_vane, y_vane, R_arc, theta)

    # 유체 제트 두께
    jet_h = 0.34
    vane_thick = 0.22

    # 1) 노즐 그리기 (좌측 고정)
    noz_x0, noz_x1 = 0.6, 1.9
    noz_poly = np.array([
        [noz_x0, y_vane - 0.30],
        [noz_x1, y_vane - jet_h / 2],
        [noz_x1, y_vane + jet_h / 2],
        [noz_x0, y_vane + 0.30]
    ])
    ax.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.8, zorder=4))
    ax.add_patch(patches.Rectangle((noz_x1 - 0.1, y_vane - jet_h / 2 - 0.04), 0.1, jet_h + 0.08,
                                   facecolor='#e6c65a', edgecolor='#5c4811', lw=1.5, zorder=5))

    # 2) 수평 입사 유체 스트림 (노즐 -> 날개 입구 x_vane)
    ax.fill_between([noz_x1, x_vane], y_vane - jet_h / 2, y_vane + jet_h / 2,
                    color='#bbdefb', alpha=0.85, zorder=2)
    ax.plot([noz_x1, x_vane], [y_vane + jet_h / 2, y_vane + jet_h / 2], color='#1976d2', lw=1.2, zorder=3)
    ax.plot([noz_x1, x_vane], [y_vane - jet_h / 2, y_vane - jet_h / 2], color='#1976d2', lw=1.2, zorder=3)

    # 3) 곡면 날개 위 유체 스트림 + 출구 연장 제트
    s_ext = np.linspace(0, 0.9, 15)
    tx_end, ty_end = np.cos(theta), np.sin(theta)
    nx_end, ny_end = -np.sin(theta), np.cos(theta)

    xs_ext = xs[-1] + s_ext * tx_end
    ys_ext = ys[-1] + s_ext * ty_end
    nx_ext = np.full_like(s_ext, nx_end)
    ny_ext = np.full_like(s_ext, ny_end)

    x_stream = np.concatenate([xs, xs_ext[1:]])
    y_stream = np.concatenate([ys, ys_ext[1:]])
    nx_stream = np.concatenate([nx, nx_ext[1:]])
    ny_stream = np.concatenate([ny, ny_ext[1:]])

    upper_x = x_stream + (jet_h / 2) * nx_stream
    upper_y = y_stream + (jet_h / 2) * ny_stream
    lower_x = x_stream - (jet_h / 2) * nx_stream
    lower_y = y_stream - (jet_h / 2) * ny_stream

    stream_poly = np.column_stack([
        np.concatenate([lower_x, upper_x[::-1]]),
        np.concatenate([lower_y, upper_y[::-1]])
    ])
    ax.add_patch(patches.Polygon(stream_poly, facecolor='#bbdefb', edgecolor='#1976d2', lw=1.2, alpha=0.85, zorder=2))

    # 4) 유체 입자 애니메이션 (유선 상의 이동 마커)
    n_pts = 7
    for k in range(n_pts):
        frac = ((k / n_pts) + phase_t) % 1.0
        idx = int(frac * (len(x_stream) - 1))
        ax.plot(x_stream[idx], y_stream[idx], 'o', color='#0d47a1', markersize=4.5, zorder=4)
    for k in range(4):
        frac = ((k / 4.0) + phase_t * 1.4) % 1.0
        px = noz_x1 + frac * (x_vane - noz_x1)
        ax.plot(px, y_vane, 'o', color='#0d47a1', markersize=4.5, zorder=4)

    # 5) 매끄러운 곡면 날개(Vane) 본체 (유체 아랫면)
    vane_top_x = xs - (jet_h / 2) * nx
    vane_top_y = ys - (jet_h / 2) * ny
    vane_bot_x = xs - (jet_h / 2 + vane_thick) * nx
    vane_bot_y = ys - (jet_h / 2 + vane_thick) * ny
    vane_poly = np.column_stack([
        np.concatenate([vane_bot_x, vane_top_x[::-1]]),
        np.concatenate([vane_bot_y, vane_top_y[::-1]])
    ])
    ax.add_patch(patches.Polygon(vane_poly, facecolor='#90a4ae', edgecolor='#263238', lw=2.0, zorder=5))

    # 6) 입구 속도 벡터 v
    ax.annotate('', xy=(noz_x1 + 1.15, y_vane), xytext=(noz_x1 + 0.15, y_vane),
                arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=6)
    ax.text(noz_x1 + 0.65, y_vane + 0.28, r'$v$', fontsize=11.5, fontweight='bold', color='#2e7d32', ha='center')

    # 7) 작용 반력 F (좌향) 및 R (상향)
    mid_i = len(xs) // 2
    vx_m, vy_m = vane_bot_x[mid_i], vane_bot_y[mid_i]
    # F 화살표 (오른쪽에서 왼쪽으로 날개를 미는 외력 -F)
    ax.annotate('', xy=(vx_m + 0.05, vy_m - 0.05), xytext=(vx_m + 1.25, vy_m - 0.05),
                arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax.text(vx_m + 1.32, vy_m - 0.05, r'$F$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    # R 화살표 (아래에서 위로 날개를 떠받치는 외력 +R)
    ax.annotate('', xy=(vx_m - 0.15, vy_m - 0.02), xytext=(vx_m - 0.15, vy_m - 0.95),
                arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14), zorder=6)
    ax.text(vx_m - 0.02, vy_m - 0.78, r'$R$', fontsize=11.5, fontweight='bold', color='#d32f2f', va='center')

    # 8) 출구 속도 및 각도 표시
    end_x, end_y = x_stream[-1], y_stream[-1]
    ax.plot([end_x - 0.1, end_x + 1.1], [end_y, end_y], color='#666666', ls='--', lw=1.1)
    arc = patches.Arc((end_x, end_y), 0.9, 0.9, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.3)
    ax.add_patch(arc)
    ax.text(end_x + 0.62, end_y + 0.24, r'$\theta=60^\circ$', fontsize=9.8, fontweight='bold', color='#333333')

    if not is_moving:
        v_out_end = (end_x + 0.95 * np.cos(theta), end_y + 0.95 * np.sin(theta))
        ax.annotate('', xy=v_out_end, xytext=(end_x, end_y),
                    arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=6)
        ax.text(v_out_end[0] + 0.1, v_out_end[1] + 0.05, r"$v' = v$", fontsize=11, fontweight='bold', color='#2e7d32')
    else:
        # 이동 날개 속도 u 표시
        ax.annotate('', xy=(vx_m + 1.45, vy_m - 0.52), xytext=(vx_m + 0.55, vy_m - 0.52),
                    arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=13), zorder=6)
        ax.text(vx_m + 1.52, vy_m - 0.52, r'$u$', fontsize=11, fontweight='bold', color='#1565c0', va='center')

        # 출구 속도 삼각형 (v' = u + (v-u)_rel)
        u_vec = np.array([0.45, 0.0])
        vrel_vec = np.array([0.85 * np.cos(theta), 0.85 * np.sin(theta)])
        vp_vec = u_vec + vrel_vec
        p0 = np.array([end_x, end_y])
        p_u = p0 + u_vec
        p_vp = p0 + vp_vec

        ax.annotate('', xy=p_u, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p_vp, xytext=p_u,
                    arrowprops=dict(arrowstyle='->', color='#00897b', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p_vp, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=14), zorder=7)
        ax.text(p_vp[0] + 0.1, p_vp[1], r"$v'$", fontsize=11, fontweight='bold', color='#2e7d32', va='center')
        ax.text(p0[0] - 0.15, p0[1] + 0.52, r'$v - u$', fontsize=9.8, fontweight='bold', color='#00897b', ha='right')

    ax.text(0.6, y_vane + 1.55, label_title, fontsize=11.2, fontweight='bold', color='#1d4564',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f4f8', edgecolor='#b0bec5'))


def update(frame):
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 9.2)
    ax_main.set_ylim(0.0, 9.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    phase_t = (frame * 0.08) % 1.0

    # 상단: (a) 고정 날개 (u = 0)
    draw_vane_and_stream(ax_main, x_vane=3.2, y_vane=6.1, u_val=0.0, phase_t=phase_t,
                         label_title='(a) 고정 날개 (Fixed Vane, $u = 0$)', is_moving=False)

    # 구분선
    ax_main.plot([0.3, 8.9], [4.55, 4.55], color='#cfd8dc', ls='--', lw=1.5)

    # 하단: (b) 이동 날개 (u = 0 -> 8 m/s 변화 애니메이션)
    u_curr = 8.0 * (0.5 - 0.5 * np.cos(2 * np.pi * frame / n_frames))
    x_shift = 2.8 + 0.9 * (u_curr / 8.0)
    draw_vane_and_stream(ax_main, x_vane=x_shift, y_vane=1.55, u_val=u_curr, phase_t=phase_t * 0.75,
                         label_title=f'(b) 이동 날개 (Moving Vane, $u = {u_curr:.1f}\\ \\mathrm{{m/s}}$)', is_moving=True)

    ax_main.set_title('예제 4.6: 매끄러운 날개에 의한 개방유동 방향 전환', fontsize=13.5, fontweight='bold', pad=10)

    # ---------------- 우측 패널: FBD / 속도선도 및 정량 해석 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단: 출구 속도 합성 삼각형 (Velocity Vector Diagram)
    ax_calc.text(5.0, 9.45, '출구 절대속도 합성 선도 ($\\mathbf{v}\' = \\mathbf{u} + \\mathbf{v}_{\\mathrm{rel}}$)',
                 fontsize=11.5, fontweight='bold', ha='center', color='#1d4564')

    tri_x0, tri_y0 = 2.2, 6.65
    u_len = 2.2
    vr_len = 2.55
    p_origin = np.array([tri_x0, tri_y0])
    p_u_end = p_origin + np.array([u_len, 0.0])
    p_vp_end = p_u_end + np.array([vr_len * np.cos(theta), vr_len * np.sin(theta)])

    # 평행사변형 보조 점선
    p_vr_top = p_origin + np.array([vr_len * np.cos(theta), vr_len * np.sin(theta)])
    ax_calc.plot([p_origin[0], p_vr_top[0]], [p_origin[1], p_vr_top[1]], color='#90a4ae', ls='--', lw=1.2)
    ax_calc.plot([p_vr_top[0], p_vp_end[0]], [p_vr_top[1], p_vp_end[1]], color='#90a4ae', ls='--', lw=1.2)

    ax_calc.annotate('', xy=p_u_end, xytext=p_origin,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=14))
    ax_calc.text(0.5 * (p_origin[0] + p_u_end[0]), p_origin[1] - 0.35, r'날개 속도 $u$',
                 fontsize=10.5, fontweight='bold', color='#1565c0', ha='center')

    ax_calc.annotate('', xy=p_vp_end, xytext=p_u_end,
                     arrowprops=dict(arrowstyle='->', color='#00897b', lw=2.3, mutation_scale=14))
    ax_calc.text(p_u_end[0] + 1.15, p_u_end[1] + 0.78, r'상대속도 $v - u$',
                 fontsize=10.5, fontweight='bold', color='#00897b', ha='left')

    ax_calc.annotate('', xy=p_vp_end, xytext=p_origin,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.6, mutation_scale=15))
    ax_calc.text(p_origin[0] + 1.35, p_origin[1] + 1.25, r"절대속도 $v'$",
                 fontsize=11, fontweight='bold', color='#2e7d32', ha='center')

    arc_v = patches.Arc(p_u_end, 1.3, 1.3, angle=0, theta1=0, theta2=theta_deg, color='#333333', lw=1.3)
    ax_calc.add_patch(arc_v)
    ax_calc.text(p_u_end[0] + 0.85, p_u_end[1] + 0.25, r'$\theta$', fontsize=11, fontweight='bold')

    # 중앙 카드 (sol_box): 이론 해석 및 정량 유도
    sol_text = (
        "[이론 해석 및 정량 유도 (" + r"$\Sigma\mathbf{F} = m'\Delta\mathbf{v}$" + ")]\n"
        "• (a) 고정 날개 (" + r"$u = 0,\ m' = \rho A v$" + "):\n"
        r"   $\Delta v_x = -v(1 - \cos\theta),\quad \Delta v_y = v\sin\theta$" + "\n"
        r"   $F = \rho A v^2(1 - \cos\theta),\quad R = \rho A v^2\sin\theta$" + "\n"
        "• (b) 이동 날개 (" + r"$u < v,\ m' = \rho A(v - u)$" + "):\n"
        r"   $v'_x = u + (v - u)\cos\theta \Rightarrow \Delta v_x = -(v - u)(1 - \cos\theta)$" + "\n"
        r"   $F = \rho A(v - u)^2(1 - \cos\theta),\quad R = \rho A(v - u)^2\sin\theta$"
    )
    ax_calc.text(5.0, 4.35, sol_text, fontsize=9.8, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드 (live_box): 실시간 물리량 모니터
    m_dot_a = rho * A * v
    F_a = m_dot_a * v * (1 - np.cos(theta))
    R_a = m_dot_a * v * np.sin(theta)

    m_dot_b = rho * A * (v - u_curr)
    F_b = rho * A * (v - u_curr)**2 * (1 - np.cos(theta))
    R_b = rho * A * (v - u_curr)**2 * np.sin(theta)

    live_text = (
        f"[실시간 수치 비교 ($v={v:.0f}\\ \\mathrm{{m/s}},\\ \\theta={theta_deg:.0f}^\\circ,\\ \\rho A={rho*A:.1f}\\ \\mathrm{{kg/m}}$)]\n"
        f"(a) 고정 ($u=0.0\\ \\mathrm{{m/s}}$): $m' = {m_dot_a:.1f}\\ \\mathrm{{kg/s}}$  |  "
        f"$F = {F_a:.1f}\\ \\mathrm{{N}},\\ R = {R_a:.1f}\\ \\mathrm{{N}}$\n"
        f"(b) 이동 ($u={u_curr:.1f}\\ \\mathrm{{m/s}}$): $m' = {m_dot_b:.1f}\\ \\mathrm{{kg/s}}$  |  "
        f"$F = {F_b:.1f}\\ \\mathrm{{N}},\\ R = {R_b:.1f}\\ \\mathrm{{N}}$"
    )
    ax_calc.text(5.0, 1.15, live_text, fontsize=9.6, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_6_fluid_vane_deflection.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
