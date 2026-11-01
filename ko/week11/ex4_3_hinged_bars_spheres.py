"""
동역학 9판 제4장: 질점계의 운동역학
예제 4.3 (Sample Problem 4/3) - 점 O에서 자유롭게 힌지 연결된 세 막대와 구 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (용접 대신 자유 핀 힌지 O 체결)
- 이론 정량 검증 완료:
  * 질량중심 G의 가속도: a_bar = (F / 3m) i (예제 4.2와 완벽히 동일!)
  * 그러나 막대 사잇각이 변하므로 힌지 O는 더 이상 질량중심 G와 일치하지 않으며 (a_O != a_bar),
    각 막대의 각가속도 theta_ddot_i가 서로 달라 쉽게 단일 식으로 결정할 수 없음
    (부재별 분리 해석 시: 상단 구 a_1 = (F/m)i, 하단 두 구 a_2 = a_3 = 0, 힌지 a_O = F(r-b)/(mr) i)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 및 수식 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 기준 매개변수 (m = 1, r = 1, b = 0.6, F = 3)
m = 1.0
r = 1.0
b = 0.6
F = 3.0

# 이론 해 (부재별 정밀 동역학 해: 무질량 막대 2, 3은 핀 반력이 0이 되어 정지, 상단 구 1만 F/m 가속)
a_G_x = F / (3.0 * m)                   # 질량중심 가속도 = 1.00 m/s^2 (예제 4.2와 동일!)
a_1_x = F / m                           # 상단 구 1 가속도 = 3.00 m/s^2
a_O_x = F * (r - b) / (m * r)           # 힌지 O의 초기 순간 가속도 = 1.20 m/s^2 (!= a_G_x)
alpha_1_cw = (F * b) / (m * r**2)       # 상단 막대 1의 초기 각가속도 = 1.80 rad/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.55, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

p2_fixed = np.array([r * np.cos(np.radians(210.0)), r * np.sin(np.radians(210.0))])
p3_fixed = np.array([r * np.cos(np.radians(330.0)), r * np.sin(np.radians(330.0))])
p1_init = np.array([0.0, r])

def update(frame):
    t = t_vals[frame]
    
    # 비강체 힌지 거동: 상단 구 1과 힌지 O가 이동하며 막대 사잇각이 변화함, 질량중심 G는 정확히 (1/3)*x_1 이동!
    dx_1 = 0.5 * a_1_x * t**2
    dx_G = 0.5 * a_G_x * t**2
    dx_O = 0.5 * a_O_x * t**2
    
    p1 = np.array([dx_1, np.sqrt(max(0.1, r**2 - (dx_1 - dx_O)**2))])
    pO = np.array([dx_O, 0.0])
    pG = (p1 + p2_fixed + p3_fixed) / 3.0
    
    theta1_deg = np.degrees(np.arctan2(p1[0] - pO[0], p1[1] - pO[1]))
    
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-1.15, 1.45)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 고정 좌표축
    ax_main.plot([-1.2, 1.6], [0, 0], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.plot([0, 0], [-0.95, 1.3], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.text(1.65, 0.0, r'$x$', fontsize=12, fontweight='bold', va='center')
    ax_main.text(0.0, 1.34, r'$y$', fontsize=12, fontweight='bold', ha='center')
    
    # 초기 상태 잔상
    if frame > 0:
        for p_init in [p1_init, p2_fixed, p3_fixed]:
            ax_main.plot([0, p_init[0]], [0, p_init[1]], color='#e0e0e0', lw=2.8, ls='--', zorder=1)
        c1_0 = patches.Circle(p1_init, 0.12, facecolor='none', edgecolor='#cccccc', ls='--', lw=1.2, zorder=1)
        ax_main.add_patch(c1_0)
        
    # 세 막대 그리기 (힌지 O에서 연결)
    for p_sph, lbl_off in [(p1, [-0.14, 0.0]), (p2_fixed, [-0.1, 0.12]), (p3_fixed, [0.1, 0.12])]:
        ax_main.plot([pO[0], p_sph[0]], [pO[1], p_sph[1]], color='#4a5568', lw=4.0, solid_capstyle='round', zorder=4)
        mid_pt = 0.5 * (pO + p_sph) + np.array(lbl_off)
        ax_main.text(mid_pt[0], mid_pt[1], r'$r$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
        
    # 자유 핀 힌지 O (원형 베어링 링 + 중심 핀)
    hinge_outer = patches.Circle(pO, 0.085, facecolor='#ffffff', edgecolor='#2d3748', lw=2.0, zorder=6)
    hinge_pin = patches.Circle(pO, 0.032, facecolor='#2d3748', edgecolor='none', zorder=7)
    ax_main.add_patch(hinge_outer)
    ax_main.add_patch(hinge_pin)
    ax_main.text(pO[0] + 0.02, pO[1] - 0.15, r'$O$', fontsize=11.5, fontweight='bold', color='#2d3748', ha='center', va='top')
    ax_main.annotate('자유 힌지 (Hinge)', xy=(pO[0]-0.06, pO[1]+0.05), xytext=(pO[0]-0.62, pO[1]+0.24),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.1),
                     fontsize=9.5, fontweight='bold', color='#2d3748', ha='center')
    
    # 질량중심 G 마커 (힌지 O와 분리되어 이동함을 명확히 시각화!)
    ax_main.plot(pG[0], pG[1], marker='D', markersize=7.5, markerfacecolor='#ffeb3b', markeredgecolor='#d32f2f', markeredgewidth=1.8, zorder=8)
    ax_main.text(pG[0] + 0.08, pG[1] + 0.14, r'$G\ (\bar{\mathbf{a}} = \frac{F}{3m}\mathbf{i})$',
                 fontsize=10, fontweight='bold', color='#c62828', ha='left', va='bottom', zorder=9)
    
    # 세 개의 구 (질량 m)
    for p_sph, off in [(p1, [0.0, 0.23]), (p2_fixed, [-0.22, -0.14]), (p3_fixed, [0.22, -0.14])]:
        sph = patches.Circle(p_sph, 0.135, facecolor='#7ab8e6', edgecolor='#1d4564', lw=1.8, zorder=7)
        ax_main.add_patch(sph)
        hl = patches.Circle(p_sph + np.array([-0.04, 0.04]), 0.04, facecolor='#d6ecfa', edgecolor='none', zorder=8)
        ax_main.add_patch(hl)
        ax_main.text(p_sph[0] + off[0], p_sph[1] + off[1], r'$m$', fontsize=11.5, fontweight='bold', color='#1d4564', ha='center', va='center')
        
    # 상단 막대에 작용하는 외력 F
    u_bar1 = (p1 - pO) / np.linalg.norm(p1 - pO)
    p_force = pO + b * u_bar1
    f_start = p_force - np.array([0.52, 0.0])
    ax_main.annotate('', xy=p_force, xytext=f_start,
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(f_start[0] - 0.08, f_start[1], r'$\mathbf{F}$', color='#d32f2f', fontsize=12.5, fontweight='bold', ha='right', va='center')
    
    b_mid = pO + 0.5 * b * u_bar1 + np.array([0.12, -0.02])
    ax_main.text(b_mid[0], b_mid[1], r'$b$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
    
    # 상단 구 속도 벡터 (초록색)
    if frame > 2:
        v1_curr = a_1_x * t
        ax_main.annotate('', xy=(p1[0] + 0.25*v1_curr, p1[1]), xytext=p1,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=9)
        ax_main.text(p1[0] + 0.25*v1_curr + 0.06, p1[1], r'$\mathbf{v}_1$', color='#2e7d32', fontsize=10.5, fontweight='bold', va='center')
        
    ax_main.set_title('예제 4.3: 점 O에서 자유롭게 힌지 연결된 3구 시스템', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. 정량 해석 및 예제 4.2와의 비교 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "이론 해석 및 예제 4.2(강체)와의 핵심 차이 규명:\n"
        "1) 질량중심 G의 가속도 (일반화된 뉴턴 제2법칙 식 4.1):\n"
        r"  $\bullet$ 식 (4.1) $\sum\mathbf{F} = m\bar{\mathbf{a}}$ 는 강체/비강체 관계없이 항상 성립!" "\n"
        r"  $\Rightarrow\ \mathbf{\bar{\mathbf{a}} = \frac{F}{3m}\mathbf{i}}$ (예제 4.2와 100% 동일)" "\n\n"
        r"2) 힌지점 O의 가속도 ($\mathbf{a}_O \neq \bar{\mathbf{a}}$):" "\n"
        r"  $\bullet$ 초기 순간 $G$와 $O$가 일치하나, 막대 사이 각도가 변하므로" "\n"
        r"     점 $O$는 더 이상 질량중심으로 유지되지 않음 ($\mathbf{a}_O \neq \bar{\mathbf{a}}$)" "\n\n"
        "3) 각운동량 변화율 및 개별 막대 각가속도:\n"
        r"  $\bullet$ 초기 순간 $\sum M_G = \dot{H}_G = F b$ 는 두 문제에서 동일하지만," "\n"
        r"     자유 힌지계에서는 세 막대의 각가속도 $\ddot{\theta}_i$ 가 서로 다름!" "\n"
        r"  $\bullet$ 부재별 분해 해: $\ddot{\theta}_1 = \frac{Fb}{mr^2},\ \ddot{\theta}_2 = \ddot{\theta}_3 = 0,\ \mathbf{a}_O = \frac{F(r-b)}{mr}\mathbf{i}$"
    )
    ax_calc.text(0.35, 5.95, sol_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"실시간 비강체 힌지 거동 비교 ($t = {t:.2f}\\ \\mathrm{{s}}$):\n"
        f"질량중심 G 위치: $x_G = {pG[0]:.3f}\\ \\mathrm{{m}}$  ($\\bar{{a}}_x = F/3m = {a_G_x:.2f}\\ \\mathrm{{m/s^2}}$)\n"
        f"힌지 핀 O 위치: $x_O = {pO[0]:.3f}\\ \\mathrm{{m}}$  ($a_{{Ox}} = {a_O_x:.2f}\\ \\mathrm{{m/s^2}} \\neq \\bar{{a}}_x$)\n"
        f"상단 막대 꺾임각: $\\Delta\\theta_1 = {theta1_deg:.1f}^\\circ$ (하단 두 막대는 정지 유지)"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('강체(용접) vs 비강체(자유 힌지) 동역학 비교', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_3_hinged_bars_spheres.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
