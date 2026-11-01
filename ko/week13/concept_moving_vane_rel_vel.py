"""
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
보충 개념 애니메이션 2 - 고정 날개(u=0) vs 단일 이동 날개(u>0) 유효 질량유량 및 출구 속도 삼각형 비교
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- 왜 단일 이동 날개가 꺾는 유효 질량유량은 m'_eff = rho*A*(v - u) 인지(다중 날개 터빈 m'_0 = rho*A*v 와의 차이) 및
  출구 절대속도 합성 v_2 = u + v_rel,2 를 직관적으로 비교 애니메이션화
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 기준 제원: 물 rho=1000 kg/m^3, A=0.002 m^2, v=20 m/s, theta=60 deg -> m'_0 = 40 kg/s
rho = 1000.0
A = 0.002
v = 20.0
theta_deg = 60.0
theta = np.radians(theta_deg)
m_dot_0 = rho * A * v  # 40.0 kg/s

n_frames = 52

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.20, 1.00]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.07, left=0.04, right=0.97, wspace=0.12)


def get_vane_arc(x0, y0, R_arc=1.85, th_max=theta):
    ang = np.linspace(-np.pi / 2, -np.pi / 2 + th_max, 36)
    cx, cy = x0, y0 + R_arc
    xs = cx + R_arc * np.cos(ang)
    ys = cy + R_arc * np.sin(ang)
    nx = -np.cos(ang)
    ny = -np.sin(ang)
    return xs, ys, nx, ny


def draw_case(ax, x_vane, y_base, u_val, phase_t, is_moving):
    jet_h = 0.32
    vane_thick = 0.20
    noz_x0, noz_x1 = 0.55, 1.75

    # 노즐 본체
    noz_poly = np.array([
        [noz_x0, y_base - 0.28],
        [noz_x1, y_base - jet_h / 2],
        [noz_x1, y_base + jet_h / 2],
        [noz_x0, y_base + 0.28]
    ])
    ax.add_patch(patches.Polygon(noz_poly, facecolor='#d4af37', edgecolor='#5c4811', lw=1.7, zorder=4))

    if not is_moving:
        # 고정 날개: 노즐 출구 -> 날개까지 전 구간 유량이 날개에 도달
        ax.fill_between([noz_x1, x_vane], y_base - jet_h / 2, y_base + jet_h / 2,
                        color='#93c5fd', alpha=0.88, zorder=2)
        ax.plot([noz_x1, x_vane], [y_base + jet_h / 2, y_base + jet_h / 2], color='#1d4ed8', lw=1.2, zorder=3)
        ax.plot([noz_x1, x_vane], [y_base - jet_h / 2, y_base - jet_h / 2], color='#1d4ed8', lw=1.2, zorder=3)
    else:
        # 이동 날개: 초기 위치 x_init=3.0 에서 x_vane 까지 날개가 도망간 거리 (u*Delta t) 구간을 주황 해칭으로 강조!
        x_init = 3.00
        ax.fill_between([noz_x1, x_init], y_base - jet_h / 2, y_base + jet_h / 2,
                        color='#93c5fd', alpha=0.88, zorder=2)
        if x_vane > x_init + 0.03:
            ax.fill_between([x_init, x_vane], y_base - jet_h / 2, y_base + jet_h / 2,
                            color='#fde68a', alpha=0.92, zorder=2)
            ax.plot([x_init, x_init], [y_base - 0.48, y_base + 0.25], color='#d97706', ls=':', lw=1.5, zorder=5)
            ax.plot([x_vane, x_vane], [y_base - 0.48, y_base + 0.25], color='#d97706', ls=':', lw=1.5, zorder=5)
            ax.annotate('', xy=(x_vane, y_base - 0.38), xytext=(x_init, y_base - 0.38),
                        arrowprops=dict(arrowstyle='<->', color='#b45309', lw=1.6), zorder=6)
            ax.text(0.5 * (x_init + x_vane), y_base - 0.68,
                    '날개 후퇴 구간 (' + r'$u\Delta t$' + ': 아직 미도달 유체)',
                    fontsize=8.8, fontweight='bold', color='#b45309', ha='center')
        ax.plot([noz_x1, x_vane], [y_base + jet_h / 2, y_base + jet_h / 2], color='#1d4ed8', lw=1.2, zorder=3)
        ax.plot([noz_x1, x_vane], [y_base - jet_h / 2, y_base - jet_h / 2], color='#1d4ed8', lw=1.2, zorder=3)

    # 곡면 날개 및 굴절 유체 스트림
    xs, ys, nx, ny = get_vane_arc(x_vane, y_base, R_arc=1.80, th_max=theta)
    s_ext = np.linspace(0, 0.75, 12)
    tx_e, ty_e = np.cos(theta), np.sin(theta)
    nx_e, ny_e = -np.sin(theta), np.cos(theta)
    x_st = np.concatenate([xs, xs[-1] + s_ext[1:] * tx_e])
    y_st = np.concatenate([ys, ys[-1] + s_ext[1:] * ty_e])
    nx_st = np.concatenate([nx, np.full(len(s_ext) - 1, nx_e)])
    ny_st = np.concatenate([ny, np.full(len(s_ext) - 1, ny_e)])

    up_x, up_y = x_st + (jet_h / 2) * nx_st, y_st + (jet_h / 2) * ny_st
    lo_x, lo_y = x_st - (jet_h / 2) * nx_st, y_st - (jet_h / 2) * ny_st
    st_poly = np.column_stack([np.concatenate([lo_x, up_x[::-1]]), np.concatenate([lo_y, up_y[::-1]])])
    ax.add_patch(patches.Polygon(st_poly, facecolor='#93c5fd', edgecolor='#1d4ed8', lw=1.2, alpha=0.88, zorder=3))

    # 날개 본체
    vt_x, vt_y = xs - (jet_h / 2) * nx, ys - (jet_h / 2) * ny
    vb_x, vb_y = xs - (jet_h / 2 + vane_thick) * nx, ys - (jet_h / 2 + vane_thick) * ny
    v_poly = np.column_stack([np.concatenate([vb_x, vt_x[::-1]]), np.concatenate([vb_y, vt_y[::-1]])])
    ax.add_patch(patches.Polygon(v_poly, facecolor='#64748b', edgecolor='#1e293b', lw=1.9, zorder=5))

    # 유체 입자 이동 마커 (상대속도 비례)
    rel_factor = 1.0 if not is_moving else (v - u_val) / v
    for k in range(5):
        frac = ((k / 5.0) + phase_t * rel_factor) % 1.0
        idx = int(frac * (len(x_st) - 1))
        ax.plot(x_st[idx], y_st[idx], 'o', color='#1e3a8a', markersize=4.3, zorder=4)

    # 입구 제트 속도 v 화살표
    ax.annotate('', xy=(noz_x1 + 0.95, y_base), xytext=(noz_x1 + 0.12, y_base),
                arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.2, mutation_scale=13), zorder=6)
    ax.text(noz_x1 + 0.54, y_base + 0.34, r'$v = 20\ \mathrm{m/s}$', fontsize=9.6, fontweight='bold', color='#15803d', ha='center')

    # 출구 속도 표시
    ex, ey = x_st[-1], y_st[-1]
    if not is_moving:
        ax.annotate('', xy=(ex + 0.85 * tx_e, ey + 0.85 * ty_e), xytext=(ex, ey),
                    arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.3, mutation_scale=14), zorder=6)
        ax.text(ex + 0.92 * tx_e, ey + 0.85 * ty_e, r'$v_2 = v$', fontsize=10.5, fontweight='bold', color='#15803d')
    else:
        # 날개 속도 u 표시
        mid_i = len(xs) // 2
        ax.annotate('', xy=(vb_x[mid_i] + 1.15, vb_y[mid_i] - 0.18), xytext=(vb_x[mid_i] + 0.25, vb_y[mid_i] - 0.18),
                    arrowprops=dict(arrowstyle='->', color='#2563eb', lw=2.2, mutation_scale=13), zorder=6)
        ax.text(vb_x[mid_i] + 1.22, vb_y[mid_i] - 0.18, f'$u = {u_val:.1f}\\ \\mathrm{{m/s}}$',
                fontsize=9.8, fontweight='bold', color='#2563eb', va='center')

        # 출구 미니 속도 삼각형
        u_vec = np.array([0.42, 0.0])
        vr_vec = np.array([0.75 * tx_e, 0.75 * ty_e])
        p0 = np.array([ex, ey])
        ax.annotate('', xy=p0 + u_vec, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#2563eb', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p0 + u_vec + vr_vec, xytext=p0 + u_vec,
                    arrowprops=dict(arrowstyle='->', color='#0d9488', lw=1.8, mutation_scale=11), zorder=6)
        ax.annotate('', xy=p0 + u_vec + vr_vec, xytext=p0,
                    arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.3, mutation_scale=14), zorder=7)
        ax.text(p0[0] + u_vec[0] + vr_vec[0] + 0.08, p0[1] + vr_vec[1], r'$\mathbf{v}_2$',
                fontsize=10.5, fontweight='bold', color='#15803d', va='center')


def update(frame):
    phase_t = (frame * 0.08) % 1.0
    # 이동 날개 속도 u = 8.0 m/s 기준으로 전진 모션 (주기적 진행 0 -> 1)
    u_curr = 8.0
    prog = (frame % n_frames) / (n_frames - 1)
    x_moving = 3.00 + 2.15 * prog

    # ---------------- 1. 좌측 패널: 고정 날개(u=0) vs 단일 이동 날개(u>0) 직관 비교 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.4)
    ax_main.set_ylim(0.30, 9.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 상단: (1) 고정 날개 (u = 0)
    draw_case(ax_main, x_vane=3.00, y_base=6.05, u_val=0.0, phase_t=phase_t, is_moving=False)
    ax_main.text(0.50, 8.55,
                 "① 고정 날개 (" + r"$u = 0$" + "): 노즐 방출량 전부가 날개에 충돌  "
                 + r"$\Rightarrow\ m'_0 = \rho A v = 40.0\ \mathrm{kg/s}$",
                 fontsize=9.8, fontweight='bold', color='#1e3a8a',
                 bbox=dict(boxstyle='round,pad=0.30', facecolor='#eff6ff', edgecolor='#93c5fd'))

    # 중앙 구분선
    ax_main.plot([0.35, 9.1], [4.65, 4.65], color='#cbd5e1', ls='--', lw=1.5)

    # 하단: (2) 단일 이동 날개 (u = 8 m/s > 0)
    draw_case(ax_main, x_vane=x_moving, y_base=1.50, u_val=u_curr, phase_t=phase_t, is_moving=True)
    m_eff = rho * A * (v - u_curr)  # 24.0 kg/s
    ax_main.text(0.50, 4.02,
                 "② 단일 이동 날개 (" + r"$u = 8\ \mathrm{m/s}$" + "): 상대속도만큼만 유입!  "
                 + f"$\\Rightarrow\\ m'_{{\\mathrm{{eff}}}} = \\rho A(v - u) = {m_eff:.1f}\\ \\mathrm{{kg/s}}$",
                 fontsize=9.8, fontweight='bold', color='#b45309',
                 bbox=dict(boxstyle='round,pad=0.30', facecolor='#fffbeb', edgecolor='#fcd34d'))

    ax_main.set_title('개념 2: 고정 날개 vs 단일 이동 날개의 유효 질량유량 비교', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 출구 속도 합성 삼각형 및 터빈 휠 차이 해설 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.58, r'출구 절대속도 벡터 삼각형 ($\mathbf{v}_2 = \mathbf{u} + \mathbf{v}_{\mathrm{rel},2}$)',
                 fontsize=11.2, fontweight='bold', ha='center', color='#1e3a8a')

    # 상단 속도 삼각형 크게 작도 (y: 6.65 ~ 9.15)
    p0 = np.array([1.85, 6.80])
    u_vec = np.array([2.55, 0.0])
    vr_len = 2.75
    vr_vec = np.array([vr_len * np.cos(theta), vr_len * np.sin(theta)])
    p_u = p0 + u_vec
    p_v2 = p_u + vr_vec

    # 보조 점선
    ax_calc.plot([p0[0], p0[0] + vr_vec[0]], [p0[1], p0[1] + vr_vec[1]], color='#94a3b8', ls='--', lw=1.2)
    ax_calc.plot([p0[0] + vr_vec[0], p_v2[0]], [p0[1] + vr_vec[1], p_v2[1]], color='#94a3b8', ls='--', lw=1.2)

    # u 벡터
    ax_calc.annotate('', xy=p_u, xytext=p0,
                     arrowprops=dict(arrowstyle='->', color='#2563eb', lw=2.5, mutation_scale=14))
    ax_calc.text(0.5 * (p0[0] + p_u[0]), p0[1] - 0.36, '날개 이동 속도 ' + r'$\mathbf{u}$',
                 fontsize=10.0, fontweight='bold', color='#2563eb', ha='center')

    # v_rel,2 벡터 (크기 v - u, 방향 theta)
    ax_calc.annotate('', xy=p_v2, xytext=p_u,
                     arrowprops=dict(arrowstyle='->', color='#0d9488', lw=2.5, mutation_scale=14))
    ax_calc.text(p_u[0] + 1.35, p_u[1] + 0.98,
                 '날개면 상대속도 ' + r'$\mathbf{v}_{\mathrm{rel},2}$' + '\n(크기 ' + r'$v_{\mathrm{rel}} = v - u$' + ')',
                 fontsize=9.6, fontweight='bold', color='#0f766e', ha='left', va='center')

    # 합벡터 v_2 (절대속도)
    ax_calc.annotate('', xy=p_v2, xytext=p0,
                     arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.8, mutation_scale=16))
    ax_calc.text(p0[0] + 1.35, p0[1] + 1.58, '출구 절대속도 ' + r'$\mathbf{v}_2$',
                 fontsize=10.5, fontweight='bold', color='#15803d', ha='center')

    arc_th = patches.Arc(p_u, 1.25, 1.25, angle=0, theta1=0, theta2=theta_deg, color='#334155', lw=1.4)
    ax_calc.add_patch(arc_th)
    ax_calc.text(p_u[0] + 0.80, p_u[1] + 0.24, r'$\theta$', fontsize=11, fontweight='bold')

    # 중앙 비교 표 스타일 요약 박스
    comp_text = (
        "[이동 날개 해석의 2단계 핵심 공식 (예제 4.6b, 4.7, 문제 4/37)]\n"
        "• 1단계 — 상대속도로 유효 질량유량 결정:\n"
        "   - 같은 방향 후퇴(예제 4.6b): " + r"$v_{\mathrm{rel}} = v - u \ \Rightarrow\ m'_{\mathrm{eff}} = \rho A(v - u)$" + "\n"
        "   - 마주 보며 전진(문제 4/37): " + r"$v_{\mathrm{rel}} = v + u \ \Rightarrow\ m'_{\mathrm{eff}} = \rho A(v + u)$" + "\n"
        "• 2단계 — 출구 절대속도로 운동량 변화량 계산:\n"
        "   " + r"$v_{2x} = u + (v - u)\cos\theta,\quad \Delta v_x = v_{2x} - v = -(v - u)(1 - \cos\theta)$" + "\n"
        "   " + r"$\Rightarrow\ \mathbf{F = m'_{\mathrm{eff}}|\Delta v_x| = \rho A(v - u)^2(1 - \cos\theta)}$"
    )
    ax_calc.text(5.0, 4.25, comp_text, fontsize=9.15, ha='center', va='center', linespacing=1.40,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#cbd5e1'))

    # 하단 노란 말풍선: 단일 날개 vs 다중 날개 펠턴 수차(터빈) 차이
    F_fixed = rho * A * (v**2) * (1.0 - np.cos(theta))
    F_single = rho * A * ((v - u_curr)**2) * (1.0 - np.cos(theta))
    tip_text = (
        f"[단일 날개 vs 다중 날개 펠턴 터빈 휠 비교 ($v=20,\\ u=8\\ \\mathrm{{m/s}}$)]\n"
        f"• 단일 날개: $m'_{{\\mathrm{{eff}}}}=24\\ \\mathrm{{kg/s}} \\Rightarrow F={F_single:.0f}\\ \\mathrm{{N}}$ (고정 날개 {F_fixed:.0f} N 대비 36%), 최적 속도 $u=v/3$\n"
        "• 다중 날개 터빈 휠: 뒤따르는 날개들이 노즐 수류 전량(" + r"$m'_0 = \rho A v$" + ")을 가로채므로 최적 속도 " + r"$u = v/2$"
    )
    ax_calc.text(5.0, 1.25, tip_text, fontsize=8.95, ha='center', va='center', linespacing=1.44,
                 bbox=dict(boxstyle='round,pad=0.43', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    ax_calc.set_title('출구 속도 합성 및 단일 날개 vs 터빈 휠 비교', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_moving_vane_rel_vel.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
