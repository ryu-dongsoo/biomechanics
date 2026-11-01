"""
동역학 9판 제3장 B편: 일과 에너지 (Section 3.7 위치에너지 및 비보존력 일)
예제 3.17 (Sample Problem 3/17) - 경사면을 따라 당겨지는 슬라이더와 스프링 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 (경사각 30도, 도르래 B, 케이블 견인력 250 N)
- 교재 공식 해답 검증 완료:
  * 비보존력 일: U'_{A-C} = 250 * (1.5 - 0.9) = 150.0 J
  * 중력 위치에너지: V_C(g) = 10 * 9.81 * (1.2 * sin 30°) = 58.9 J
  * 탄성 위치에너지: V_A = 10.8 J, V_C = 97.2 J
  * 일-에너지 방정식: T_A + V_A + U'_{A-C} = T_C + V_C  =>  v_C = 0.974 m/s
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
m = 10.0            # 슬라이더 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
theta_deg = 30.0    # 경사각 (도)
theta = np.radians(theta_deg)
k = 60.0            # 스프링 강성계수 (N/m)
xA = 0.6            # A점에서의 스프링 초기 인장량 (m)
P = 250.0           # 케이블 견인력 (N)
s_total = 1.2       # A -> C 이동 거리 (m)

# 기하 좌표계 설정:
# 경사면 방향 단위벡터 u_slope, 법선 단위벡터 u_normal
u_slope = np.array([np.cos(theta), np.sin(theta)])
u_norm = np.array([-np.sin(theta), np.cos(theta)])

# 기준 A점 좌표
p_A = np.array([1.5, 1.2])
p_C = p_A + s_total * u_slope
p_B = p_C + 0.9 * u_norm  # 직각 삼각형 형태 (AB = sqrt(1.2^2 + 0.9^2) = 1.5 m)
p_spring_base = p_A - 1.4 * u_slope

# 에너지 계산
h_C = s_total * np.sin(theta) # 0.6 m
Vg_C = m * g * h_C            # 58.86 J
Ve_A = 0.5 * k * xA**2        # 10.8 J
Ve_C = 0.5 * k * (xA + s_total)**2 # 97.2 J
U_ext = P * 0.6               # 150.0 J
T_C = Ve_A + U_ext - (Vg_C + Ve_C) # 4.74 J
v_C = np.sqrt(2 * T_C / m)    # 0.974 m/s

# 애니메이션 설정
n_frames = 50
s_vals = np.linspace(0, s_total, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.06, color='#444444', lw=1.8):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-6:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.08
    active_len = max(length - 2 * lead_len, 0.05)
    pts = [start, start + lead_len * u_par]
    step = active_len / nodes
    for i in range(1, nodes):
        sgn = 1 if i % 2 == 1 else -1
        p = start + lead_len * u_par + i * step * u_par + sgn * width * u_perp
        pts.append(p)
    pts.append(end - lead_len * u_par)
    pts.append(end)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle='round')

def update(frame):
    s = s_vals[frame]
    p_curr = p_A + s * u_slope
    
    # 케이블 길이 변화: AB - (거리 curr to B)
    dist_curr_B = np.linalg.norm(p_B - p_curr)
    cable_pulled = 1.5 - dist_curr_B
    U_curr = P * cable_pulled
    
    # 에너지
    x_curr = xA + s
    Ve_curr = 0.5 * k * x_curr**2
    Vg_curr = m * g * (s * np.sin(theta))
    T_curr = max(Ve_A + U_curr - (Ve_curr + Vg_curr), 0.0)
    v_curr = np.sqrt(2 * T_curr / m)
    
    # ---------------- 1. 메인 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.2, 3.8)
    ax_main.set_ylim(0.2, 3.2)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 경사면 램프 (Ramp wedge)
    ramp_x0 = 0.0
    ramp_y0 = 0.5
    ramp_poly = np.array([
        [ramp_x0, ramp_y0],
        [ramp_x0 + 3.4 * np.cos(theta), ramp_y0 + 3.4 * np.sin(theta)],
        [ramp_x0 + 3.4 * np.cos(theta), ramp_y0],
    ])
    ax_main.fill(ramp_poly[:, 0], ramp_poly[:, 1], color='#f4ede4', edgecolor='none')
    ax_main.plot([ramp_x0, ramp_x0 + 3.6 * np.cos(theta)], [ramp_y0, ramp_y0 + 3.6 * np.sin(theta)], color='#2b2b2b', lw=2.2)
    ax_main.plot([ramp_x0 - 0.2, ramp_x0 + 3.4 * np.cos(theta) + 0.2], [ramp_y0, ramp_y0], color='#2b2b2b', lw=1.5)
    
    # 각도 30도 표시
    ax_main.plot([ramp_x0, ramp_x0 + 1.2], [ramp_y0, ramp_y0], color='#777777', ls='--', lw=1.0)
    arc = patches.Arc((ramp_x0, ramp_y0), 1.6, 1.6, angle=0, theta1=0, theta2=30, color='#222222', lw=1.5)
    ax_main.add_patch(arc)
    ax_main.text(ramp_x0 + 0.9, ramp_y0 + 0.18, r'$30^\circ$', fontsize=11, fontweight='bold')
    
    # 스프링 하단 고정 지지대
    sp_mount = patches.Rectangle(p_spring_base - 0.12 * u_norm - 0.08 * u_slope, 0.08, 0.24,
                                 angle=theta_deg, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(sp_mount)
    
    # 스프링
    draw_spring(ax_main, p_spring_base, p_curr - 0.25 * u_slope, nodes=14, width=0.06, color='#2b2b2b', lw=1.8)
    
    # 도르래 B (지름 0.16)
    r_pulley = 0.08
    ax_main.plot([p_B[0], p_B[0] - 0.2], [p_B[1], p_B[1] + 0.35], color='#777777', lw=2.0)
    pulley_circle = patches.Circle(p_B, r_pulley, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.8, zorder=4)
    ax_main.add_patch(pulley_circle)
    ax_main.plot(p_B[0], p_B[1], 'o', color='#2b2b2b', markersize=4, zorder=5)
    ax_main.text(p_B[0] - 0.15, p_B[1] + 0.02, r'$B$', fontsize=12, fontweight='bold')
    
    # 케이블: 슬라이더 -> 도르래 B -> 당김 방향
    ax_main.plot([p_curr[0], p_B[0]], [p_curr[1], p_B[1]], color='#2b2b2b', lw=1.8, zorder=3)
    # 도르래에서 당겨지는 케이블 (P = 250 N)
    pull_dir = np.array([0.5, 0.2])
    pull_end = p_B + 0.7 * pull_dir
    ax_main.plot([p_B[0], pull_end[0]], [p_B[1], pull_end[1]], color='#2b2b2b', lw=2.0, zorder=3)
    ax_main.annotate('', xy=pull_end + 0.3 * pull_dir, xytext=pull_end,
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_main.text(pull_end[0] + 0.15, pull_end[1] + 0.1, r'$250\ \mathrm{N}$', color='#d32f2f', fontsize=11, fontweight='bold')
    
    # 슬라이더 블록 (10 kg)
    bw, bh = 0.50, 0.26
    slider_rect = patches.Rectangle(p_curr - (bw/2) * u_slope, bw, bh,
                                    angle=theta_deg, facecolor='#4682b4', edgecolor='#1a3c5a', lw=1.8, zorder=5)
    ax_main.add_patch(slider_rect)
    ax_main.text(p_curr[0] - 0.05 * u_norm[0], p_curr[1] + 0.08, r'$10\ \mathrm{kg}$',
                 color='#ffffff', fontsize=9.5, fontweight='bold', ha='center', zorder=6)
    
    # 속도 벡터
    if v_curr > 0.1:
        v_scale = 0.35 * (v_curr / v_C)
        v_end = p_curr + v_scale * u_slope
        ax_main.annotate('', xy=v_end, xytext=p_curr,
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
        ax_main.text(v_end[0] + 0.08, v_end[1] + 0.05, r'$v$', color='#27ae60', fontsize=11, fontweight='bold')
    
    # 위치 A, C 및 이동거리 1.2 m, 0.9 m 표시
    ax_main.plot([p_A[0], p_A[0] - 0.4 * u_norm[0]], [p_A[1], p_A[1] - 0.4 * u_norm[1]], color='#999999', ls='--', lw=1.0)
    ax_main.plot([p_C[0], p_C[0] - 0.4 * u_norm[0]], [p_C[1], p_C[1] - 0.4 * u_norm[1]], color='#999999', ls='--', lw=1.0)
    dim_A = p_A - 0.35 * u_norm
    dim_C = p_C - 0.35 * u_norm
    ax_main.annotate('', xy=dim_C, xytext=dim_A,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    dim_mid = 0.5 * (dim_A + dim_C) - 0.12 * u_norm
    ax_main.text(dim_mid[0], dim_mid[1], r'$1.2\ \mathrm{m}$', ha='center', va='center', fontsize=10.5, rotation=theta_deg)
    
    # BC = 0.9 m 표시
    ax_main.plot([p_C[0], p_B[0]], [p_C[1], p_B[1]], color='#777777', ls=':', lw=1.2)
    dim_BC = 0.5 * (p_C + p_B) + 0.15 * u_slope
    ax_main.text(dim_BC[0], dim_BC[1], r'$0.9\ \mathrm{m}$', fontsize=10, rotation=theta_deg + 90, color='#555555')
    
    ax_main.text(p_A[0] - 0.25, p_A[1] + 0.25, r'$A$', fontsize=12, fontweight='bold', color='#2b2b2b')
    ax_main.text(p_C[0] - 0.2, p_C[1] + 0.3, r'$C$', fontsize=12, fontweight='bold', color='#2b2b2b')
    
    ax_main.set_title('예제 3.17 기구도 (경사면 슬라이더 및 케이블 시스템)', fontsize=12.5, fontweight='bold', pad=12)

    # ---------------- 2. 실시간 에너지 보존 & 이론 검증 패널 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-0.2, 2.2)
    ax_fbd.set_ylim(-1.6, 1.6)
    ax_fbd.axis('off')
    
    # 에너지 막대 그래프 (T, Ve, Vg, U')
    bar_x = [0.2, 0.7, 1.2, 1.7]
    bar_vals = [T_curr, Ve_curr, Vg_curr, U_curr]
    bar_colors = ['#27ae60', '#2980b9', '#e67e22', '#d32f2f']
    bar_labels = [r'$T$', r'$V_e$', r'$V_g$', r"$U'_{\mathrm{ext}}$"]
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 160.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + 0.06, f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"【교재 공식 일-에너지 해석 (Section 3.7)】\n"
        f"• 케이블 외력 일: $U'_{{A-C}} = 250(1.5 - 0.9) = \\mathbf{{150.0\\ \\mathrm{{J}}}}$\n"
        f"• 중력 위치에너지: $V_C(g) = 10(9.81)(1.2\\sin 30^\\circ) = 58.9\\ \\mathrm{{J}}$\n"
        f"• 탄성 위치에너지: \n"
        f"  $V_A = \\frac{{1}}{{2}}(60)(0.6)^2 = 10.8\\ \\mathrm{{J}}$\n"
        f"  $V_C = \\frac{{1}}{{2}}(60)(0.6 + 1.2)^2 = 97.2\\ \\mathrm{{J}}$\n"
        f"• 일-에너지 방정식: $T_A + V_A + U'_{{A-C}} = T_C + V_C$\n"
        f"  $0 + 10.8 + 150 = \\frac{{1}}{{2}}(10)v_C^2 + 58.9 + 97.2$\n"
        f"  $\\rightarrow\\ v_C = \\mathbf{{0.974\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• 슬라이더 변위: $s = {s:.2f}\\ /\\ 1.20\\ \\mathrm{{m}}$\n"
        f"• 현재 속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (최종: $0.974\\ \\mathrm{{m/s}}$)"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.5, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('에너지 보존 모니터 및 이론적 검증', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_17_incline_slider_spring.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
