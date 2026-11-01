"""
동역학 9판 제4장 질점계의 운동역학 (4.7 가변질량)
기초문제 2 - 문제 4/61 (Problem 4/61) - 고체연료 모형 로켓의 발사 초기 가속도 및 연료 소진 속도
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (녹색 모형 로켓 및 삼각대 발사대)
- 이론 검증 결과:
  * m_0 = 0.75 kg, 연료 0.05 kg (m_b = 0.70 kg), t_b = 0.9 s, u = 900 m/s
  * m' = 0.05 / 0.9 = 0.0556 kg/s
  * 발사 순간 가속도: a_0 = 56.9 m/s^2 (5.80g)
  * 연료 소진 시 최대 속도: v_max = 900 ln(0.75/0.70) - 9.81(0.9) = 53.3 m/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수 (문제 4/61)
m0 = 0.75               # 초기 질량 (kg)
dm_fuel = 0.05          # 고체연료 질량 (kg)
mb = m0 - dm_fuel       # 0.70 kg
tb = 0.90               # 연소 시간 (s)
u = 900.0               # 배기가스 상대속도 (m/s)
g = 9.81                # 중력가속도 (m/s^2)

m_prime = dm_fuel / tb  # 0.05556 kg/s
m_dot = -m_prime
T_thrust = m_prime * u  # 50.0 N
a0 = (T_thrust - m0 * g) / m0                 # 56.856 -> 56.9 m/s^2 (5.80g)
v_max = u * np.log(m0 / mb) + (g / m_dot) * (m0 - mb)  # 62.09 - 8.83 = 53.26 -> 53.3 m/s

n_frames = 50
t_vals = np.linspace(0.0, tb, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)


def draw_model_rocket(ax, xc, yc):
    # 모형 로켓 (교재 p.275 문제 4/61 원도: 녹색 슬렌더 원통 + 삼각 날개 + 주황색 화염 + 발사 삼각대)
    bw, bh = 0.24, 1.65
    body = patches.Rectangle((xc - bw / 2, yc), bw, bh,
                             facecolor='#4db6ac', edgecolor='#004d40', lw=1.8, zorder=4)
    ax.add_patch(body)
    # 동체 마디 가로줄 (교재 원도 디테일)
    for dy in (0.45, 0.85, 1.25):
        ax.plot([xc - bw / 2, xc + bw / 2], [yc + dy, yc + dy], color='#00695c', lw=1.0, zorder=5)

    # 원추형 노즈콘
    nose_pts = np.array([
        [xc - bw / 2, yc + bh],
        [xc + bw / 2, yc + bh],
        [xc, yc + bh + 0.42]
    ])
    ax.add_patch(patches.Polygon(nose_pts, facecolor='#80cbc4', edgecolor='#004d40', lw=1.8, zorder=4))

    # 좌·우·중앙 녹색 핀(Fin)
    fin_l = patches.Polygon([
        [xc - bw / 2, yc + 0.38],
        [xc - bw / 2 - 0.28, yc + 0.14],
        [xc - bw / 2 - 0.28, yc - 0.08],
        [xc - bw / 2, yc + 0.08]
    ], facecolor='#4db6ac', edgecolor='#004d40', lw=1.6, zorder=3)
    fin_r = patches.Polygon([
        [xc + bw / 2, yc + 0.38],
        [xc + bw / 2 + 0.28, yc + 0.14],
        [xc + bw / 2 + 0.28, yc - 0.08],
        [xc + bw / 2, yc + 0.08]
    ], facecolor='#4db6ac', edgecolor='#004d40', lw=1.6, zorder=3)
    ax.add_patch(fin_l)
    ax.add_patch(fin_r)
    ax.plot([xc, xc], [yc - 0.06, yc + 0.38], color='#004d40', lw=3.0, zorder=5)

    # 길게 뻗은 고체연료 제트 화염 (교재 원도 스타일)
    flame_out = patches.Polygon([
        [xc - 0.07, yc],
        [xc + 0.07, yc],
        [xc, yc - 0.95]
    ], facecolor='#ff8a65', edgecolor='none', alpha=0.85, zorder=2)
    flame_in = patches.Polygon([
        [xc - 0.035, yc],
        [xc + 0.035, yc],
        [xc, yc - 0.62]
    ], facecolor='#fff176', edgecolor='none', alpha=0.95, zorder=3)
    ax.add_patch(flame_out)
    ax.add_patch(flame_in)


def update(frame):
    t = t_vals[frame]
    m_curr = m0 + m_dot * t
    a_curr = (T_thrust - m_curr * g) / m_curr
    v_curr = u * np.log(m0 / m_curr) - g * t
    W_curr = m_curr * g

    yc = 1.05 + 2.05 * (frame / (n_frames - 1))**1.5

    # ---------------- 1. 메인 뷰 (교재 원도 1:1) ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.5, 2.7)
    ax_main.set_ylim(-0.5, 5.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 지면 및 청회색 삼각대 발사대 (교재 문제 4/61 원도 1:1 재현)
    ax_main.fill_between([-2.1, 2.1], -0.35, 0.0, color='#e0dcd3')
    ax_main.plot([-2.1, 2.1], [0.0, 0.0], color='#3e2723', lw=2.2)

    stand_pts = np.array([
        [-0.58, 0.0], [-0.30, 0.45], [0.30, 0.45], [0.58, 0.0],
        [0.40, 0.0], [0.22, 0.30], [0.08, 0.30], [0.05, 0.0],
        [-0.05, 0.0], [-0.08, 0.30], [-0.22, 0.30], [-0.40, 0.0]
    ])
    ax_main.add_patch(patches.Polygon(stand_pts, facecolor='#607d8b', edgecolor='#263238', lw=1.6, zorder=3))

    # 발사 연기 구름 (양측 확산)
    for sx, sr in [(-0.85, 0.25), (-0.52, 0.22), (0.52, 0.22), (0.85, 0.25), (0.0, 0.20)]:
        smoke = patches.Ellipse((sx, 0.52), sr * 2.4, sr * 1.3, facecolor='#eceff1', edgecolor='#cfd8dc', lw=1.0, zorder=1)
        ax_main.add_patch(smoke)

    draw_model_rocket(ax_main, 0.0, yc)

    # 추력 T = m'u = 50.0 N (빨간색 상향 화살표)
    ax_main.annotate('', xy=(0.35, yc + 0.65), xytext=(0.35, yc - 0.15),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=16), zorder=6)
    ax_main.text(0.50, yc + 0.25, f'$T = m\'u = {T_thrust:.1f}\\ \\mathrm{{N}}$\n$(u = 900\\ \\mathrm{{m/s}})$',
                 color='#d32f2f', fontsize=10.2, fontweight='bold', va='center')

    # 자중 mg (빨간색 하향 화살표)
    ax_main.annotate('', xy=(0.35, yc + 0.85), xytext=(0.35, yc + 1.45),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.2, mutation_scale=14), zorder=6)
    ax_main.text(0.50, yc + 1.18, f'$mg = {W_curr:.2f}\\ \\mathrm{{N}}$\n$(m = {m_curr:.3f}\\ \\mathrm{{kg}})$',
                 color='#d32f2f', fontsize=10.0, fontweight='bold', va='center')

    # 속도 및 가속도 벡터 (좌측 초록색 상향 화살표)
    ax_main.annotate('', xy=(-0.45, yc + 1.45), xytext=(-0.45, yc + 0.60),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=16), zorder=6)
    ax_main.text(-0.60, yc + 1.02, f'$v = {v_curr:.1f}\\ \\mathrm{{m/s}}$\n$a = {a_curr:.1f}\\ \\mathrm{{m/s^2}}$',
                 color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right', va='center')

    ax_main.set_title('문제 4/61: 고체연료 모형 로켓 발사 동역학', fontsize=13.5, fontweight='bold', pad=12)

    # ---------------- 2. 우측 패널 (이론 유도 & 실시간 정량 검증) ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    # 상단 속도-시간 프로파일 그래프
    gx0, gy0, gw, gh = 1.1, 6.70, 8.2, 2.65
    ax_calc.add_patch(patches.Rectangle((gx0, gy0), gw, gh, facecolor='#ffffff', edgecolor='#b0bec5', lw=1.2))
    t_dense = np.linspace(0, tb, 80)
    m_dense = m0 + m_dot * t_dense
    v_dense = u * np.log(m0 / m_dense) - g * t_dense
    tx_plot = gx0 + (t_dense / tb) * gw
    ty_plot = gy0 + (v_dense / 60.0) * gh
    ax_calc.plot(tx_plot, ty_plot, color='#00796b', lw=2.3)

    cur_px = gx0 + (t / tb) * gw
    cur_py = gy0 + (v_curr / 60.0) * gh
    ax_calc.plot(cur_px, cur_py, 'ro', markersize=6, zorder=5)
    ax_calc.text(gx0 + 0.25, gy0 + gh - 0.38, r'모형 로켓 속도 곡선: $v(t) = 900\ln(0.75/m) - 9.81t$',
                 fontsize=9.5, fontweight='bold', color='#004d40')
    ax_calc.text(gx0 + gw - 0.2, gy0 + 0.22, r'초기 $a_0 = 56.9\ \mathrm{m/s^2}\ (5.80g),\quad v_{\max} = 53.3\ \mathrm{m/s}$',
                 fontsize=9.2, fontweight='bold', color='#d32f2f', ha='right')

    # 중앙 카드: 정량 유도
    sol_text = (
        r"■ 평균 질량유량($m'$) 및 발사 순간 가속도($\dot{v}_0$):" "\n"
        r"  $\bullet\ m' = \frac{0.05}{0.9} = 0.0556\ \mathrm{kg/s}$ (일정 연소율 및 $pA = R = 0$ 가정)" "\n"
        r"  $\bullet\ m'u - m_0 g = m_0\dot{v}_0 \Rightarrow 0.0556(900) - 0.75(9.81) = 0.75\dot{v}_0 \Rightarrow \mathbf{\dot{v}_0 = 56.9\ \mathrm{m/s^2}\ (5.80g)}$" "\n"
        r"■ 연료 소진 시점($t_b = 0.9\ \mathrm{s},\ m_b = 0.70\ \mathrm{kg}$) 최대 속도($v_{\max}$):" "\n"
        r"  $\bullet\ \int_0^{v_{\max}} dv = -u\int_{m_0}^{m_b}\frac{dm}{m} - g\int_0^{t_b} dt$" "\n"
        r"  $\bullet\ v_{\max} = 900\ln\left(\frac{0.75}{0.70}\right) - 9.81(0.9) \Rightarrow \mathbf{v_{\max} = 53.3\ \mathrm{m/s}}$"
    )
    ax_calc.text(0.35, 4.25, sol_text, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fbfbfb', edgecolor='#cccccc'))

    # 하단 카드: 실시간 모니터
    live_text = (
        f"[실시간 연소 모니터: $t = {t:.2f}\\ /\\ 0.90\\ \\mathrm{{s}}$]\n"
        f"• 현재 질량: $m(t) = {m_curr:.4f}\\ \\mathrm{{kg}}$   |   추진력: $T = {T_thrust:.1f}\\ \\mathrm{{N}}$ (일정)\n"
        f"• 현재 가속도: $a(t) = {a_curr:.1f}\\ \\mathrm{{m/s^2}}$ (발사 초기값: $\\mathbf{{56.9\\ \\mathrm{{m/s^2}}}}$)\n"
        f"• 현재 속도: $v(t) = {v_curr:.1f}\\ \\mathrm{{m/s}}$ (이론 최종값: $\\mathbf{{53.3\\ \\mathrm{{m/s}}}}$)"
    )
    ax_calc.text(0.35, 1.15, live_text, fontsize=9.4, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))

    ax_calc.set_title('이론 해석 및 정량 유도', fontsize=13.5, fontweight='bold', pad=12)


anim = FuncAnimation(fig, update, frames=n_frames, interval=70)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_61_model_rocket_launch.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
