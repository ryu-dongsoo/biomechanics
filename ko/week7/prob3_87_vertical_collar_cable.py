"""
동역학 9판 제3장 B편: 일과 에너지
기초문제 3 - 문제 3/87 (Problem 3/87) - 케이블로 당겨지는 수직 봉 상의 칼라 운동
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (상단 치수선 및 도르래 C 온전한 뷰)
- 솔루션 매뉴얼 검증 완료:
  * 케이블 당김 변위: d = sqrt(R^2 + (R/2)^2) - R/2 = 0.989 m
  * 힘 P가 한 일: U_P = 20(0.989) = +19.78 J
  * 중력이 한 일: U_g = -0.8(9.81)(1.6) = -12.56 J
  * 순 일량: U_total = +7.22 J
  * B지점 통과 속도: v_B = 4.25 m/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 매개변수
m = 0.8             # 칼라 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
R = 1.6             # 수직 이동 거리 (m)
P = 20.0            # 케이블 당김 힘 (N)
d_pulley = R / 2.0  # 풀리 C의 수평 거리 = 0.8 m

# 기하 계산
LA = np.sqrt(R**2 + d_pulley**2)  # sqrt(3.20) ~ 1.7889 m
LB = d_pulley                     # 0.80 m
delta_L_final = LA - LB           # 0.9889 m

# 일 및 속도 계산
U_P_final = P * delta_L_final             # +19.777 J
U_g_final = -m * g * R                    # -12.557 J
U_tot_final = U_P_final + U_g_final       # +7.220 J
v_B = np.sqrt(2 * U_tot_final / m)        # 4.249 m/s (~4.25 m/s)

# 수치 궤적 생성
y_grid = np.linspace(0.0, R, 200)
U_grid = np.zeros_like(y_grid)
v_grid = np.zeros_like(y_grid)

for i, y in enumerate(y_grid):
    L_curr = np.sqrt((R - y)**2 + d_pulley**2)
    dL = LA - L_curr
    Up = P * dL
    Ug = -m * g * y
    Utot = max(0.0, Up + Ug)
    U_grid[i] = Utot
    v_grid[i] = np.sqrt(2 * Utot / m)

dt_grid = 1.0 / np.maximum(v_grid, 0.1)
t_steps = 0.5 * (dt_grid[:-1] + dt_grid[1:]) * np.diff(y_grid)
t_grid = np.concatenate([[0], np.cumsum(t_steps)])
t_total = t_grid[-1]

# 애니메이션 시계열
n_frames = 50
t_anim = np.linspace(0, t_total, n_frames)
y_anim = np.interp(t_anim, t_grid, y_grid)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.1, 1.1]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    y_curr = y_anim[frame]
    L_curr = np.sqrt((R - y_curr)**2 + d_pulley**2)
    dL_curr = LA - L_curr
    
    Up_curr = P * dL_curr
    Ug_curr = -m * g * y_curr
    Utot_curr = Up_curr + Ug_curr
    v_curr = np.sqrt(2 * max(0.0, Utot_curr) / m)
    
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    # 상단 치수선과 하단 브래킷이 잘리지 않도록 y-범위 충분히 확보
    ax_main.set_xlim(-0.65, 1.45)
    ax_main.set_ylim(-0.35, 2.30)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 수직 가이드 봉 (스틸 블루 원통)
    rod_x = 0.0
    rod_poly = patches.Rectangle((rod_x - 0.02, -0.16), 0.04, R + 0.32,
                                 facecolor='#b8d5e5', edgecolor='#466f85', lw=1.5)
    ax_main.add_patch(rod_poly)
    
    # 상하단 지지대 (목재/금속 브래킷)
    top_bracket = patches.Polygon([[-0.1, R + 0.16], [0.1, R + 0.16], [0.06, R + 0.24], [-0.06, R + 0.24]],
                                  facecolor='#d7a15c', edgecolor='#6d4013', lw=1.5)
    bot_bracket = patches.Polygon([[-0.1, -0.16], [0.1, -0.16], [0.06, -0.24], [-0.06, -0.24]],
                                  facecolor='#d7a15c', edgecolor='#6d4013', lw=1.5)
    ax_main.add_patch(top_bracket)
    ax_main.add_patch(bot_bracket)
    
    # 도르래 C 및 지지대
    pulley_x, pulley_y = d_pulley, R
    c_sup = patches.Polygon([[pulley_x - 0.08, pulley_y + 0.14], [pulley_x + 0.08, pulley_y + 0.14],
                             [pulley_x + 0.04, pulley_y], [pulley_x - 0.04, pulley_y]],
                            facecolor='#cfd8dc', edgecolor='#37474f', lw=1.4)
    ax_main.add_patch(c_sup)
    ax_main.plot([pulley_x - 0.12, pulley_x + 0.12], [pulley_y + 0.14, pulley_y + 0.14], color='#333333', lw=2.2)
    ax_main.add_patch(patches.Circle((pulley_x, pulley_y), 0.045, facecolor='#ffffff', edgecolor='#333333', lw=1.6))
    ax_main.text(pulley_x + 0.08, pulley_y, r'$C$', fontsize=13, fontweight='bold', va='center')
    
    # 수평 점선 B - C
    ax_main.plot([0, pulley_x], [R, R], color='#888888', ls='--', lw=1.2)
    
    # 치수선 R/2 (B와 C 사이)
    dim_y_top = R + 0.32
    ax_main.plot([0, 0], [R + 0.18, dim_y_top + 0.05], color='#888888', lw=1)
    ax_main.plot([pulley_x, pulley_x], [R + 0.18, dim_y_top + 0.05], color='#888888', lw=1)
    ax_main.annotate('', xy=(pulley_x, dim_y_top), xytext=(0, dim_y_top),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(d_pulley / 2, dim_y_top + 0.05, r'$\frac{R}{2}$', fontsize=12, fontweight='bold', ha='center', va='bottom')
    
    # 치수선 R (A와 B 사이)
    dim_x = -0.28
    ax_main.plot([0, dim_x - 0.05], [0, 0], color='#888888', lw=1)
    ax_main.plot([0, dim_x - 0.05], [R, R], color='#888888', lw=1)
    ax_main.annotate('', xy=(dim_x, R), xytext=(dim_x, 0),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(dim_x - 0.05, R / 2, r'$R = 1.6\ \mathrm{m}$', fontsize=11, fontweight='bold', ha='right', va='center')
    
    # A, B 위치 레이블
    ax_main.plot(0, 0, 'ko', markersize=3.5)
    ax_main.text(-0.08, 0, r'$A$', fontsize=13, fontweight='bold', ha='right', va='center')
    ax_main.plot(0, R, 'ko', markersize=3.5)
    ax_main.text(-0.08, R, r'$B$', fontsize=13, fontweight='bold', ha='right', va='center')
    
    # 칼라 블록 (구리색 슬라이더)
    c_w, c_h = 0.16, 0.20
    collar = patches.Rectangle((-c_w/2, y_curr - c_h/2), c_w, c_h,
                               facecolor='#e8b88a', edgecolor='#7a4d25', lw=2.0)
    ax_main.add_patch(collar)
    ax_main.plot(0, y_curr, 'ko', markersize=3)
    ax_main.text(0.12, y_curr - 0.05, r'$m = 0.8\ \mathrm{kg}$', fontsize=10, fontweight='bold', color='#4a2800')
    
    # 케이블 (칼라 중심 -> 도르래 C -> 수직 하향 당김)
    cable_down_len = 0.45 + dL_curr * 0.4
    ax_main.plot([0, pulley_x], [y_curr, pulley_y], color='#111111', lw=2.0)
    ax_main.plot([pulley_x, pulley_x], [pulley_y, pulley_y - cable_down_len], color='#111111', lw=2.0)
    
    # 당김 힘 P = 20 N 화살표 (빨간색, 수직 하향)
    ax_main.annotate('', xy=(pulley_x, pulley_y - cable_down_len - 0.25),
                     xytext=(pulley_x, pulley_y - cable_down_len),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_main.text(pulley_x + 0.08, pulley_y - cable_down_len - 0.12,
                 r'$P = 20\ \mathrm{N}$', color='#d32f2f', fontsize=11, fontweight='bold')
    
    # 칼라 속도 벡터 (녹색 화살표)
    if v_curr > 0.05:
        v_arrow_len = v_curr * 0.07
        ax_main.annotate('', xy=(0, y_curr + c_h/2 + v_arrow_len), xytext=(0, y_curr + c_h/2),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
        ax_main.text(-0.10, y_curr + c_h/2 + v_arrow_len * 0.5,
                     f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$', color='#2e7d32', fontsize=10.5, fontweight='bold', ha='right')
        
    ax_main.set_title('문제 3/87: 케이블로 당겨지는 수직 봉 상의 칼라', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 정량 계산 및 솔루션 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "문제 조건 및 기하학:\n"
        r"  $\bullet\ m = 0.8\ \mathrm{kg},\ R = 1.6\ \mathrm{m},\ P = 20\ \mathrm{N}$" "\n"
        r"  $\bullet\ L_A = \sqrt{1.6^2 + 0.8^2} = \sqrt{3.20} \approx 1.7889\ \mathrm{m}$" "\n"
        r"  $\bullet\ L_B = 0.80\ \mathrm{m}$" "\n"
        r"  $\bullet\ \Delta L = L_A - L_B = 1.7889 - 0.80 = \mathbf{0.9889\ \mathrm{m}}$" "\n\n"
        "일-에너지 방정식 및 일 계산:\n"
        r"  $\bullet\ U_P = P \cdot \Delta L = 20(0.9889) = \mathbf{+19.78\ \mathrm{J}}$" "\n"
        r"  $\bullet\ U_g = -m g R = -0.8(9.81)(1.6) = \mathbf{-12.56\ \mathrm{J}}$" "\n"
        r"  $\bullet\ U_{\mathrm{total}} = 19.78 - 12.56 = \mathbf{+7.22\ \mathrm{J}}$" "\n\n"
        "B점 통과 속도 v_B:\n"
        r"  $T_1 + U_{1-2} = T_2 \quad (T_1 = 0)$" "\n"
        r"  $0 + 7.22 = \frac{1}{2}(0.8) v_B^2 \Rightarrow 0.4 v_B^2 = 7.22$" "\n"
        r"  $\mathbf{v_B = 4.25\ \mathrm{m/s}}$"
    )
    ax_calc.text(0.5, 6.2, sol_box, fontsize=10.2, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f'상승 높이: $y = {y_curr:.3f}\\ /\\ 1.600\\ \\mathrm{{m}}$\n'
        f'케이블 이동 변위: $\\Delta L = {dL_curr:.3f}\\ /\\ 0.989\\ \\mathrm{{m}}$\n'
        f'케이블 장력 일: $U_P = {Up_curr:+.2f}\\ \\mathrm{{J}}$\n'
        f'중력 일: $U_g = {Ug_curr:+.2f}\\ \\mathrm{{J}}$\n'
        f'순 일량: $U = {Utot_curr:+.2f}\\ \\mathrm{{J}}$\n'
        f'현재 칼라 속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (최종: $4.25\\ \\mathrm{{m/s}}$)'
    )
    ax_calc.text(0.5, 1.6, live_box, fontsize=10.2, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('일과 에너지 정량 해석', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_87_vertical_collar_cable.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
