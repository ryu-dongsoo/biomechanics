"""
동역학 9판 제4장: 질점계의 운동역학
기초문제 2 - 문제 4/5 (Problem 4/5) - 수평 안내로 내 스프링 연결 두 구와 힌지 막대 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (수평 가이드 채널, 코일 스프링, V자 힌지 봉)
- 이론 정량 검증 완료:
  * 스프링 중심 C는 두 구(각 2 kg)로 구성된 시스템의 질량중심 G와 일치
  * Sigma F_x = m_tot * a_C => 50 N = 2(2 kg) * a_C => a_C = 12.5 m/s^2 (->)
  * 치수 b는 수직항력 R_1, R_2에는 영향을 주지만 Sigma F_x 및 a_C에는 무관함
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

# 물리 매개변수
m_sphere = 2.0      # 각 구의 질량 (kg)
m_tot = 4.0         # 시스템 총 질량 (kg)
F_ext = 50.0        # 수평 외력 (N)
L_bar = 0.30        # 막대 길이 300 mm = 0.30 m
a_C = F_ext / m_tot # 12.5 m/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.16, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_coil_spring(ax, x_left, x_right, y_c, n_coils=10, amp=0.032):
    L = x_right - x_left
    pad = 0.045
    xs = [x_left, x_left + pad]
    ys = [y_c, y_c]
    coil_len = L - 2 * pad
    for i in range(2 * n_coils):
        frac = (i + 0.5) / (2 * n_coils)
        xs.append(x_left + pad + frac * coil_len)
        ys.append(y_c + (amp if i % 2 == 0 else -amp))
    xs.extend([x_right - pad, x_right])
    ys.extend([y_c, y_c])
    ax.plot(xs, ys, color='#2b2b2b', lw=2.0, zorder=5)

def update(frame):
    t = t_vals[frame]
    # 질량중심 C의 이동 거리 및 스프링 미소 신축 진동 중첩
    x_C = 0.5 * a_C * t**2
    v_C = a_C * t
    
    # 초기 반간격 d0 = 0.15 m (정삼각형 배치: 두 구 간격 0.30 m, 봉 길이 0.30 m)
    # 우측 봉에 힘이 가해지므로 우측 구가 미세하게 먼저 당겨지며 스프링 변형 동반, 그러나 중심 C는 정확히 0.5*a_C*t^2!
    delta_half = 0.018 * np.sin(18.0 * t)
    d_half = 0.15 + delta_half
    
    x1 = x_C - d_half
    x2 = x_C + d_half
    y_guide = 0.32
    r_sph = 0.072
    
    # 하단 힌지점 P_bot 위치 (기하학적 구속: 각 구 중심으로부터 거리 L_bar = 0.30 m)
    h_drop = np.sqrt(max(0.02, L_bar**2 - d_half**2))
    x_bot = x_C
    y_bot = y_guide - h_drop
    
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.34, 0.56)
    ax_main.set_ylim(-0.14, 0.50)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 수평 안내로 (상/하단 벽체 및 음영 패치)
    y_top_wall = y_guide + r_sph + 0.003
    y_bot_wall = y_guide - r_sph - 0.003
    ax_main.fill_between([-0.30, 0.52], y_top_wall, y_top_wall + 0.045, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.fill_between([-0.30, 0.52], y_bot_wall - 0.045, y_bot_wall, color='#e4ded7', edgecolor='none', zorder=1)
    ax_main.plot([-0.30, 0.52], [y_top_wall, y_top_wall], color='#333333', lw=2.2, zorder=2)
    ax_main.plot([-0.30, 0.52], [y_bot_wall, y_bot_wall], color='#333333', lw=2.2, zorder=2)
    
    # 두 개의 구 (2 kg)
    for x_s, lbl_x in [(x1, x1 - 0.115), (x2, x2 + 0.115)]:
        sph = patches.Circle((x_s, y_guide), r_sph, facecolor='#d48872', edgecolor='#59281a', lw=1.8, zorder=4)
        ax_main.add_patch(sph)
        hl = patches.Circle((x_s - 0.022, y_guide + 0.022), 0.022, facecolor='#f2cbbd', edgecolor='none', zorder=5)
        ax_main.add_patch(hl)
        ax_main.text(lbl_x, y_guide, '2 kg', fontsize=11.5, fontweight='bold', color='#222222', ha='center', va='center')
        
    # 코일 스프링 및 중심 C 마커
    draw_coil_spring(ax_main, x1, x2, y_guide, n_coils=9, amp=0.024)
    ax_main.plot(x_C, y_guide, 'ko', markersize=5.5, zorder=8)
    ax_main.text(x_C, y_guide - 0.048, r'$C\ (G)$', fontsize=11.5, fontweight='bold', color='#1565c0', ha='center', va='top', zorder=8)
    
    # 중심 C의 가속도/속도 화살표
    ax_main.annotate('', xy=(x_C + 0.09, y_guide + 0.048), xytext=(x_C, y_guide + 0.048),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13), zorder=9)
    ax_main.text(x_C + 0.045, y_guide + 0.088, f'$a_C = 12.5\\ \\mathrm{{m/s^2}}$',
                 fontsize=10.5, fontweight='bold', color='#2e7d32', ha='center')
    
    # 두 개의 경량 힌지 막대 (300 mm)
    for x_s in [x1, x2]:
        ax_main.plot([x_s, x_bot], [y_guide, y_bot], color='#3a5a78', lw=6.5, solid_capstyle='round', zorder=6)
        ax_main.plot([x_s, x_bot], [y_guide, y_bot], color='#a7c7e7', lw=3.8, solid_capstyle='round', zorder=6)
        # 상단 힌지 핀
        p_pin = patches.Circle((x_s, y_guide), 0.015, facecolor='#ffffff', edgecolor='#222222', lw=1.5, zorder=7)
        ax_main.add_patch(p_pin)
        p_dot = patches.Circle((x_s, y_guide), 0.005, facecolor='#222222', edgecolor='none', zorder=8)
        ax_main.add_patch(p_dot)
        
    # 하단 힌지 핀
    b_pin = patches.Circle((x_bot, y_bot), 0.016, facecolor='#ffffff', edgecolor='#222222', lw=1.5, zorder=7)
    ax_main.add_patch(b_pin)
    b_dot = patches.Circle((x_bot, y_bot), 0.006, facecolor='#222222', edgecolor='none', zorder=8)
    ax_main.add_patch(b_dot)
    
    # 막대 치수 300 mm 표시
    ax_main.text(0.5*(x1 + x_bot) - 0.085, 0.5*(y_guide + y_bot) - 0.01, '300 mm', fontsize=10.5, fontweight='bold', ha='center')
    ax_main.text(0.5*(x2 + x_bot) - 0.055, 0.5*(y_guide + y_bot) + 0.01, '300 mm', fontsize=10.5, fontweight='bold', ha='center')
    
    # 우측 막대에 작용하는 수평 외력 50 N (하단으로부터 거리 b 비율 위치)
    frac_b = 0.36
    px_F = x_bot + frac_b * (x2 - x_bot)
    py_F = y_bot + frac_b * (y_guide - y_bot)
    ax_main.annotate('', xy=(px_F + 0.13, py_F), xytext=(px_F + 0.008, py_F),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(px_F + 0.14, py_F, '50 N', color='#d32f2f', fontsize=12, fontweight='bold', va='center')
    ax_main.text(0.5*(x_bot + px_F) + 0.032, 0.5*(y_bot + py_F) - 0.018, r'$b$', fontsize=11.5, fontweight='bold', color='#222222')
    
    ax_main.set_title('문제 4/5: 수평 안내로 내 스프링 연결 2구 및 힌지 봉 시스템', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. 시스템 경계 FBD 및 정량 유도 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "이론 해석 및 정량 유도 (전체 시스템 경계 설정):\n"
        "1) 시스템의 질량중심 확인:\n"
        r"  $\bullet$ 두 구의 질량($2\ \mathrm{kg}$)이 같고 스프링·봉의 질량을 무시하므로," "\n"
        r"     스프링 중심 $C$는 전체 시스템의 질량중심 $G$와 항상 일치!" "\n\n"
        "2) 일반화된 뉴턴 제2법칙 (식 4.1, 수평 x 방향):\n"
        r"  $\bullet$ 내력(스프링 탄성력, 핀 반력)은 시스템 내부에서 완전 상쇄 ($\sum f_x = 0$)" "\n"
        r"  $\bullet\ [\sum F_x = m\bar{a}_x] \quad 50\ \mathrm{N} = 2(2\ \mathrm{kg})\, a_C$" "\n"
        r"  $\Rightarrow\ \mathbf{a_C = 12.5\ \mathrm{m/s^2}}\ (\rightarrow)$" "\n\n"
        "3) 치수 b의 크기에 영향을 받지 않는 이유:\n"
        r"  $\bullet$ 치수 $b$는 모멘트 평형을 통해 수직항력 $R_1, R_2$의 크기에만" "\n"
        r"     영향을 줄 뿐, 수평 외력의 합 $\sum F_x = 50\ \mathrm{N}$ 과 $a_C$에는 무관함!"
    )
    ax_calc.text(0.35, 6.0, sol_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"실시간 질량중심 C 모니터 ($t = {t:.3f}\\ \\mathrm{{s}}$):\n"
        f"수평 외력 합: $\\sum F_x = 50.0\\ \\mathrm{{N}}$,  총 질량: $m = 4.0\\ \\mathrm{{kg}}$\n"
        f"중심 C 가속도: $a_C = 12.50\\ \\mathrm{{m/s^2}}$ (일정),  속도: $v_C = {v_C:.2f}\\ \\mathrm{{m/s}}$\n"
        f"중심 C 이동 변위: $x_C = {x_C*1000:.1f}\\ \\mathrm{{mm}}$"
    )
    ax_calc.text(0.35, 1.4, live_box, fontsize=9.6, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('시스템 경계 자유물체도 및 가속도 검증', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob4_5_spring_linked_spheres.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
