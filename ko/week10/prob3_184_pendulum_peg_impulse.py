"""
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
문제 3/184 - 회전 수평 봉 위 두 구의 반경 확장(r -> 2r) 각속도 및 에너지 손실 분율
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * 초기 반경 r_1 = r (각속도 omega_0), 최종 반경 r_2 = 2r (각속도 omega)
  * 회전축에 대한 각운동량 보존: Delta H = 0 => 2 m (r omega_0) r - 2 m (2r omega)(2r) = 0
  * 새 각속도: omega = omega_0 / 4
  * 운동에너지 손실량: Delta T = T_1 - T_2 = 2[1/2 m (r omega_0)^2] - 2[1/2 m (2r omega_0/4)^2] = (3/4) m r^2 omega_0^2
  * 손실 에너지 분율: n = Delta T / T_1 = 3/4 (75.0%)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

r_init = 1.0
r_final = 2.0
omega0 = 1.0

n_frames = 55
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    if frame < 10:
        s_prog = 0.0
        state_msg = r"초기 회전 상태 ($r_1 = r,\ \omega_1 = \omega_0$)"
    elif frame < 42:
        s_prog = ((frame - 10) / 32.0)**1.3
        state_msg = r"래치 해제: 바깥쪽 미끄럼에 따른 회전 감속 ($\omega = \omega_0 (r/R)^2$)"
    else:
        s_prog = 1.0
        state_msg = r"끝단 스토퍼($2r$) 도달 정착: $\omega = \omega_0 / 4,\ n = \Delta T / T_1 = 3/4$"

    R_curr = r_init + (r_final - r_init) * s_prog
    omega_curr = omega0 * (r_init / R_curr)**2
    T_ratio = (r_init / R_curr)**2
    loss_ratio = 1.0 - T_ratio

    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.75, 2.75)
    ax_main.set_ylim(-1.55, 1.85)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('문제 3/184: 회전 수평 봉 위 두 구의 반경 확장 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    tilt_deg = 11.0
    tilt_rad = np.radians(tilt_deg)
    u_rod = np.array([np.cos(tilt_rad), np.sin(tilt_rad)])

    pedestal = patches.Polygon([[-0.26, -1.25], [0.26, -1.25], [0.16, -0.68], [-0.16, -0.68]],
                               facecolor='#9ec5e5', edgecolor='#2b4c6f', lw=1.6, zorder=3)
    ax_main.add_patch(pedestal)
    shaft = patches.Rectangle((-0.055, -0.68), 0.11, 0.68, facecolor='#cbd5e1', edgecolor='#334155', lw=1.5, zorder=2)
    ax_main.add_patch(shaft)

    arc_t = np.linspace(-np.pi*0.85, np.pi*0.35, 40)
    ax_main.plot(0.24 * np.cos(arc_t), -0.45 + 0.08 * np.sin(arc_t), color='#00897b', lw=2.2, zorder=5)
    ax_main.annotate('', xy=(0.24 * np.cos(np.pi*0.35), -0.45 + 0.08 * np.sin(np.pi*0.35)),
                     xytext=(0.24 * np.cos(np.pi*0.15), -0.45 + 0.08 * np.sin(np.pi*0.15)),
                     arrowprops=dict(arrowstyle='-|>', color='#00897b', lw=2.0, mutation_scale=13), zorder=5)
    ax_main.text(0.32, -0.48, r'$\omega_0$', fontsize=12, fontweight='bold', color='#111111')

    rod_len = 2.25
    t_rod = patches.transforms.Affine2D().rotate(tilt_rad) + ax_main.transData
    rod_patch = patches.Rectangle((-rod_len, -0.055), 2*rod_len, 0.11,
                                  facecolor='#d8dee9', edgecolor='#334155', lw=1.5, zorder=3)
    rod_patch.set_transform(t_rod)
    ax_main.add_patch(rod_patch)

    hub = patches.Rectangle((-0.16, -0.10), 0.32, 0.20, facecolor='#9ec5e5', edgecolor='#2b4c6f', lw=1.5, zorder=4)
    hub.set_transform(t_rod)
    ax_main.add_patch(hub)

    for sgn in [-1, 1]:
        stop_c = patches.Rectangle((sgn * 2.22 - 0.06, -0.13), 0.12, 0.26,
                                   facecolor='#9ec5e5', edgecolor='#2b4c6f', lw=1.5, zorder=5)
        stop_c.set_transform(t_rod)
        ax_main.add_patch(stop_c)

    for sgn in [-1, 1]:
        p_2r = sgn * r_final * u_rod
        ghost_2r = patches.Circle(p_2r, 0.27, facecolor='none', edgecolor='#333333', ls='--', lw=1.2, zorder=4)
        ax_main.add_patch(ghost_2r)

    for sgn in [-1, 1]:
        p_m = sgn * R_curr * u_rod
        sphere = patches.Circle(p_m, 0.27, facecolor='#e5989b', edgecolor='#6d2e46', lw=1.6, zorder=6)
        hi = patches.Circle(p_m + np.array([-0.08, 0.08]), 0.09, facecolor='#ffccd5', edgecolor='none', zorder=7)
        ax_main.add_patch(sphere)
        ax_main.add_patch(hi)
        ax_main.text(p_m[0], p_m[1] - 0.42, '$m$', fontsize=11.5, fontweight='bold', ha='center')

    for x_pos, h_ext in [(-2.0, 0.85), (-1.0, 0.45), (0.0, 0.90), (1.0, 0.45), (2.0, 0.85)]:
        pt_base = x_pos * u_rod + 0.30 * np.array([0, 1])
        pt_top = x_pos * u_rod + (h_ext + 0.12) * np.array([0, 1])
        ax_main.plot([pt_base[0], pt_top[0]], [pt_base[1], pt_top[1]], color='#444444', lw=1.0)

    for sgn in [-1, 1]:
        p_start = np.array([0.0, 0.45])
        p_end = sgn * 1.0 * u_rod + np.array([0.0, 0.45])
        ax_main.annotate('', xy=p_end, xytext=p_start, arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
        mid = 0.5 * (p_start + p_end)
        ax_main.text(mid[0], mid[1], '$r$', ha='center', va='center', fontsize=11, style='italic', fontweight='bold',
                     bbox=dict(boxstyle='square,pad=0.12', facecolor='#ffffff', edgecolor='none'))

    for sgn in [-1, 1]:
        p_start = np.array([0.0, 0.85])
        p_end = sgn * 2.0 * u_rod + np.array([0.0, 0.85])
        ax_main.annotate('', xy=p_end, xytext=p_start, arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
        mid = 0.5 * (p_start + p_end)
        ax_main.text(mid[0], mid[1], '$2r$', ha='center', va='center', fontsize=11, style='italic', fontweight='bold',
                     bbox=dict(boxstyle='square,pad=0.12', facecolor='#ffffff', edgecolor='none'))

    ax_main.text(0.0, 1.52, state_msg, fontsize=10.2, fontweight='bold', color='#1f618d', ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8f9fa', edgecolor='#1f618d', lw=1.3))

    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('회전축 각운동량 보존 및 에너지 손실 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_card = (
        r"【수직 회전축 각운동량 보존 조건 ($\Delta H_O = 0$)】" + "\n"
        r"• 회전축은 마찰 없이 자유 회전하므로 외부 비틀림 모멘트 $\Sigma M_O = 0$" + "\n"
        r"• 두 구의 반경이 $r \to 2r$로 2배 증가하면 $mr^2$ 항이 4배로 커짐" + "\n"
        r"• 따라서 각속도는 $1/4$로 감소하고, 스토퍼 정지 시 운동에너지의 $3/4$ 소실!"
    )
    ax_calc.text(0.35, 8.45, top_card, fontsize=9.3, va='center', ha='left', linespacing=1.4,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (3.10절)】\n"
        r"1) 각운동량 보존 ($\Delta H = 0 \Rightarrow H_1 = H_2$):" + "\n"
        r"   $2m(r\omega_0)r - 2m(2r\omega)(2r) = 0 \Rightarrow \mathbf{\omega = \frac{\omega_0}{4}}$" + "\n\n"
        r"2) 손실된 운동에너지 ($\Delta T = T_1 - T_2$):" + "\n"
        r"   $\Delta T = 2\left[\frac{1}{2}m(r\omega_0)^2\right] - 2\left[\frac{1}{2}m\left(2r\frac{\omega_0}{4}\right)^2\right] = \frac{3}{4}m r^2 \omega_0^2$" + "\n\n"
        r"3) 초기 운동에너지에 대한 손실 에너지 분수 $n$:" + "\n"
        r"   $n = \frac{\Delta T}{T_1} = \frac{\frac{3}{4}m r^2 \omega_0^2}{m r^2 \omega_0^2} = \mathbf{\frac{3}{4}\ (0.75)}$"
    )
    ax_calc.text(0.35, 4.75, sol_text, fontsize=9.4, va='center', ha='left', linespacing=1.35,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        "【실시간 반경·각속도·에너지 모니터】\n"
        rf"• 현재 구 위치 반경: $R = {R_curr:.2f}\,r$  |  현재 각속도: $\omega = {omega_curr:.3f}\,\omega_0$" + "\n"
        rf"• 잔류 운동에너지 비: $T/T_1 = {T_ratio:.3f}$  |  누적 손실 분율: $n = {loss_ratio:.3f}$" + "\n"
        r"• 이론 최종값 ($R = 2r$): $\omega = \frac{\omega_0}{4}$ ($0.250\,\omega_0$),  손실 분수 $n = \frac{3}{4}$ ($0.750$)"
    )
    ax_calc.text(0.35, 1.25, live_text, fontsize=9.2, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_184_pendulum_peg_impulse.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
