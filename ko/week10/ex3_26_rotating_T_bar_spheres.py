"""
동역학 9판 제3장 C편: 충격량과 운동량 (Section 3.10 각충격량과 각운동량)
예제 3.26 - 가벼운 봉-질량 조합체와 가루뭉치 충돌 각운동량 보존
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 2분할 레이아웃 (14 x 6.5)
- 정량 계산 결과:
  * 좌측 질량 4m (거리 2l), 우측 질량 2m (거리 l), 낙하 가루뭉치 m (속도 v_1)
  * 점 O에 대한 시스템 각운동량 보존: (H_O)_1 = (H_O)_2
  * m v_1 l = (m + 2m)(l * omega_2) l + 4m (2l * omega_2)(2l) = 19 m l^2 omega_2
  * omega_2 = theta_dot_2 = v_1 / (19 l) (시계방향 CW)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 정규화 수치 매개변수 (기호 해 theta_dot_2 = v_1 / (19 l) 및 수치 예시 병행)
l_val = 1.0      # m
v1_val = 9.5     # m/s -> omega_2 = 9.5 / 19 = 0.50 rad/s
omega2_val = v1_val / (19.0 * l_val)

n_frames = 54
fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=100, gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-2.65, 1.85)
    ax_main.set_ylim(-1.45, 1.55)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('예제 3.26: 봉-질량 조립체와 가루뭉치 충돌 (교재 원도 1:1)', fontsize=12.5, fontweight='bold', pad=10)

    # 피벗 지지대 O (교재 원도와 동일한 사다리꼴 브래킷 + 지면 해칭)
    base_y = -0.45
    ax_main.fill_between([-0.42, 0.42], base_y - 0.14, base_y, color='#d5cbb8', alpha=0.8, zorder=1)
    ax_main.plot([-0.42, 0.42], [base_y, base_y], color='#333333', lw=2.0, zorder=2)
    bracket = patches.Polygon([[-0.22, base_y], [0.22, base_y], [0.09, 0.0], [-0.09, 0.0]],
                              facecolor='#b0c4de', edgecolor='#2b2b2b', lw=1.6, zorder=3)
    ax_main.add_patch(bracket)

    # 프레임 구간 분리: 0~19 낙하, 20~24 충돌 부착, 25~53 시계방향(CW) 회전
    if frame < 20:
        theta_cw = 0.0
        putty_y = 0.95 - (frame / 20.0) * 0.72
        phase_str = r"충돌 전: 가루뭉치($m$) 연직 낙하 중 (속력 $v_1$)"
        phase_col = '#1971c2'
    elif frame < 25:
        theta_cw = 0.0
        putty_y = 0.18
        phase_str = r"충돌 순간: 우측 질량($2m$)에 완전 비탄성 부착!"
        phase_col = '#d32f2f'
    else:
        dt_rot = (frame - 24) / 29.0
        theta_cw = dt_rot * 0.52  # rad (CW)
        putty_y = 0.18
        phase_str = r"충돌 후: 조립체 일체 시계방향 회전 ($\dot{\theta}_2 = v_1 / 19l\ \mathrm{CW}$)"
        phase_col = '#2e7d32'

    # 회전 변환 행렬 (시계방향 각도 theta_cw -> 수학적 각도 -theta_cw)
    ang = -theta_cw
    t_rot = patches.transforms.Affine2D().rotate(ang) + ax_main.transData

    # 가벼운 봉 (-2l ~ +l, 황갈색 막대)
    rod_rect = patches.Rectangle((-2.0, -0.035), 3.0, 0.07, facecolor='#d99b66', edgecolor='#5c3a21', lw=1.5, zorder=4)
    rod_rect.set_transform(t_rot)
    ax_main.add_patch(rod_rect)

    # 좌측 끝단 질량 4m (중심 x = -2.0)
    m4_rect = patches.Rectangle((-2.22, -0.22), 0.44, 0.44, facecolor='#a9cce3', edgecolor='#1f618d', lw=1.6, zorder=5)
    m4_rect.set_transform(t_rot)
    ax_main.add_patch(m4_rect)
    p_left = np.array([-2.0 * np.cos(ang), -2.0 * np.sin(ang)])
    ax_main.text(p_left[0], p_left[1], '$4m$', fontsize=11, fontweight='bold', ha='center', va='center', zorder=6)

    # 우측 끝단 질량 2m (중심 x = +1.0)
    m2_rect = patches.Rectangle((0.82, -0.16), 0.36, 0.32, facecolor='#a9cce3', edgecolor='#1f618d', lw=1.6, zorder=5)
    m2_rect.set_transform(t_rot)
    ax_main.add_patch(m2_rect)
    p_right = np.array([1.0 * np.cos(ang), 1.0 * np.sin(ang)])
    ax_main.text(p_right[0], p_right[1], '$2m$', fontsize=11, fontweight='bold', ha='center', va='center', zorder=6)

    # 피벗 핀 O
    pin_outer = patches.Circle((0, 0), 0.085, facecolor='#b0c4de', edgecolor='#222222', lw=1.5, zorder=7)
    pin_inner = patches.Circle((0, 0), 0.038, facecolor='#ffffff', edgecolor='#222222', lw=1.2, zorder=8)
    ax_main.add_patch(pin_outer)
    ax_main.add_patch(pin_inner)
    ax_main.text(0.0, 0.16, '$O$', fontsize=12, fontweight='bold', ha='center', zorder=8)

    # 가루뭉치 (Putty m) 렌더링
    if frame < 20:
        px_c, py_c = 1.0, putty_y
        putty_blob = patches.Ellipse((px_c, py_c), 0.28, 0.20, angle=-10,
                                     facecolor='#d96b6b', edgecolor='#641e16', lw=1.5, zorder=6)
        ax_main.add_patch(putty_blob)
        ax_main.text(px_c + 0.05, py_c + 0.18, '$m$', fontsize=11, fontweight='bold')
        # 낙하 속도 화살표 v_1
        ax_main.annotate('', xy=(1.08, py_c - 0.38), xytext=(1.08, py_c - 0.05),
                         arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=7)
        ax_main.text(1.24, py_c - 0.22, '$v_1$', color='#2e7d32', fontsize=11, fontweight='bold')
    else:
        # 우측 블록(2m) 상단에 납작하게 들러붙어 함께 회전
        putty_attached = patches.Ellipse((1.0, 0.19), 0.32, 0.14,
                                         facecolor='#d96b6b', edgecolor='#641e16', lw=1.5, zorder=6)
        putty_attached.set_transform(t_rot)
        ax_main.add_patch(putty_attached)
        p_putty = np.array([1.0 * np.cos(ang) - 0.32 * np.sin(ang), 1.0 * np.sin(ang) + 0.32 * np.cos(ang)])
        ax_main.text(p_putty[0] + 0.12, p_putty[1], '$m$', fontsize=10.5, fontweight='bold', color='#641e16', zorder=7)

        if frame >= 25:
            # 충돌 후 회전 각속도 호 및 양 끝단 접선 속도 벡터 표시
            arc_t = np.linspace(0.3, -0.5, 25)
            ax_main.plot(0.45 * np.cos(arc_t), 0.45 * np.sin(arc_t), color='#2e7d32', lw=2.0)
            ax_main.annotate('', xy=(0.45 * np.cos(-0.55), 0.45 * np.sin(-0.55)),
                             xytext=(0.45 * np.cos(-0.40), 0.45 * np.sin(-0.40)),
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12))
            ax_main.text(0.42, -0.45, r'$\dot{\theta}_2 = \frac{v_1}{19l}$', color='#2e7d32', fontsize=10.5, fontweight='bold')

            # 우측 끝 접선 속도 l * theta_dot_2 (하향 접선)
            t_vec_r = np.array([np.sin(theta_cw), -np.cos(theta_cw)]) * 0.38
            ax_main.annotate('', xy=p_right + t_vec_r, xytext=p_right,
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=7)
            # 좌측 끝 접선 속도 2l * theta_dot_2 (상향 접선)
            t_vec_l = np.array([-np.sin(theta_cw), np.cos(theta_cw)]) * 0.65
            ax_main.annotate('', xy=p_left + t_vec_l, xytext=p_left,
                             arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=7)

    # 하단 교재 원도 치수선 (2l, l)
    y_dim = -0.95
    ax_main.plot([-2.0, -2.0], [-0.25, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.plot([0.0, 0.0], [-0.48, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.plot([1.0, 1.0], [-0.25, y_dim - 0.12], color='#555555', lw=1.0)
    ax_main.annotate('', xy=(-2.0, y_dim), xytext=(0.0, y_dim), arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
    ax_main.annotate('', xy=(0.0, y_dim), xytext=(1.0, y_dim), arrowprops=dict(arrowstyle='<->', color='#222222', lw=1.2))
    ax_main.text(-1.0, y_dim, '$2l$', ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='#ffffff', edgecolor='none'))
    ax_main.text(0.5, y_dim, '$l$', ha='center', va='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='#ffffff', edgecolor='none'))

    # 상단 상태 배지
    ax_main.text(-0.4, 1.32, phase_str, fontsize=10.2, fontweight='bold', color=phase_col, ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8f9fa', edgecolor=phase_col, lw=1.3))

    # 우측 패널: 각운동량 보존 유도 및 검증
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    ax_calc.set_title('피벗 점 O 각운동량 보존 해석 및 정량 검증', fontsize=12.5, fontweight='bold', pad=10)

    top_card = (
        "【충돌 시 피벗 점 $O$에 대한 각운동량 보존 조건】\n"
        r"• 피벗 핀 반력 $\mathbf{R}_O$는 점 $O$를 통과하므로 모멘트 팔 $d = 0$" + "\n"
        r"• 극초단 충돌 중 자중($mg$)의 각충격량은 비충격력으로 생략 가능" + "\n"
        r"• 따라서 점 $O$에 대한 시스템 총 각운동량 보존: $(H_O)_1 = (H_O)_2$"
    )
    ax_calc.text(0.4, 8.45, top_card, fontsize=9.5, va='center', ha='left', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#adb5bd', lw=1.3))

    sol_text = (
        "【이론 해석 및 정량 유도 (시계방향 CW $+$ 기준)】\n"
        r"1) 충돌 직전 각운동량 $(H_O)_1$:" + "\n"
        r"   $(H_O)_1 = m v_1 l$" + "\n\n"
        r"2) 충돌 직후 각운동량 $(H_O)_2$ ($v_{\mathrm{right}} = l\dot{\theta}_2,\ v_{\mathrm{left}} = 2l\dot{\theta}_2$):" + "\n"
        r"   $(H_O)_2 = (m + 2m)(l\dot{\theta}_2)l + 4m(2l\dot{\theta}_2)(2l)$" + "\n"
        r"   $(H_O)_2 = 3m l^2 \dot{\theta}_2 + 16m l^2 \dot{\theta}_2 = 19m l^2 \dot{\theta}_2$" + "\n\n"
        r"3) 최종 각속도 도출: $m v_1 l = 19m l^2 \dot{\theta}_2 \Rightarrow \mathbf{\dot{\theta}_2 = \frac{v_1}{19l}\ \mathrm{CW}}$"
    )
    ax_calc.text(0.4, 4.85, sol_text, fontsize=9.5, va='center', ha='left', linespacing=1.38,
                 bbox=dict(boxstyle='round,pad=0.55', facecolor='#fbfbfb', edgecolor='#cccccc', lw=1.4))

    live_text = (
        "【각 질점의 각운동량 기여도 및 에너지 비교】\n"
        r"• 우측($m+2m$, 거리 $l$) 기여분: $3 m l^2 \dot{\theta}_2$ (전체의 $3/19 = 15.8\%$)" + "\n"
        r"• 좌측($4m$, 거리 $2l$) 기여분: $16 m l^2 \dot{\theta}_2$ (전체의 $16/19 = 84.2\%$)" + "\n"
        r"• 이론 최종값: $\dot{\theta}_2 = \frac{v_1}{19l}\ \mathrm{CW}$  (운동에너지 비 $T_2/T_1 = \frac{1}{19} = 5.26\%$)"
    )
    ax_calc.text(0.4, 1.35, live_text, fontsize=9.3, va='center', ha='left', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9', lw=1.4))

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_26_rotating_T_bar_spheres.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
