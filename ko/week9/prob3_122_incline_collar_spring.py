"""
동역학 9판 제3장 B편: 일과 에너지 (Section 3.7 위치에너지 및 비보존력 일)
연습문제 심화 1 (Problem 3/122) - 수직봉을 따라 외력을 받으며 상승하는 고리와 스프링 시스템
- 순수 흰색 바탕 (#ffffff) & 교재 원도 1:1 완벽 반영 (수직 안내봉, 50 N 경사 외력, 수평 2 m 스프링 지지벽)
- 교재 공식 솔루션 매뉴얼 검증 완료:
  * 외력 일: U'_{1-2} = 50 * 1.5 * cos 30° = 64.95 J
  * 중력 위치에너지: Delta V_g = 2 * 9.81 * 1.5 = 29.43 J
  * 탄성 위치에너지: Delta V_e = 0.5 * 30 * [(2.5 - 1.5)^2 - (2.0 - 1.5)^2] = 11.25 J
  * 일-에너지 방정식: 64.95 = v^2 + 11.25 + 29.43  =>  v = 4.93 m/s
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
m = 2.0             # 고리 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
k = 30.0            # 스프링 강성계수 (N/m)
L0 = 1.5            # 자유 길이 (m)
P = 50.0            # 외력 크기 (N)
phi_deg = 30.0      # 수직축에 대한 외력 경사각 (도)
phi = np.radians(phi_deg)
d_wall = 2.0        # 수직봉과 우측 벽면 사이 거리 (m)
y_final = 1.5       # A -> B 수직 이동 거리 (m)

# 기하 좌표계 (A점 = (0.0, 0.0))
# B점: (0.0, 1.5)
# 스프링 벽면 앵커: (2.0, 0.0)
x_anchor, y_anchor = 2.0, 0.0

# 에너지 계산
xA = d_wall - L0                               # 2.0 - 1.5 = 0.5 m
LB = np.sqrt(d_wall**2 + y_final**2)           # sqrt(2^2 + 1.5^2) = 2.5 m
xB = LB - L0                                   # 2.5 - 1.5 = 1.0 m
U_ext = P * y_final * np.cos(phi)              # 64.95 J
Delta_Vg = m * g * y_final                     # 29.43 J
Delta_Ve = 0.5 * k * (xB**2 - xA**2)           # 11.25 J
T_final = U_ext - Delta_Vg - Delta_Ve          # 24.27 J
v_final = np.sqrt(2.0 * T_final / m)           # 4.93 m/s

# 애니메이션 설정 (0 -> y_final)
n_frames = 50
y_vals = np.linspace(0.0, y_final, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.06, right=0.95, wspace=0.18)

def draw_spring(ax, start, end, nodes=14, width=0.06, color='#444444', lw=1.8):
    start = np.array(start)
    end = np.array(end)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-5:
        return
    u_par = vec / length
    u_perp = np.array([-u_par[1], u_par[0]])
    lead_len = 0.08
    active_len = max(length - 2 * lead_len, 0.04)
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
    y = y_vals[frame]
    
    # 스프링 길이 및 변위
    L_curr = np.sqrt(x_anchor**2 + y**2)
    x_curr = L_curr - L0
    
    # 에너지
    U_curr = P * y * np.cos(phi)
    Vg_curr = m * g * y
    Ve_curr = 0.5 * k * (x_curr**2 - xA**2)
    T_curr = max(U_curr - Vg_curr - Ve_curr, 0.0)
    v_curr = np.sqrt(2.0 * T_curr / m)
    
    # ---------------- 1. 메인 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.8, 2.5)
    ax_main.set_ylim(-0.35, 2.1)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 상단 천장 지지대
    ax_main.plot([-0.25, 0.25], [1.95, 1.95], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.24, 0.20, 6):
        ax_main.plot([hx, hx + 0.05], [1.95, 2.05], color='#666666', lw=1.2)
    mount_top = patches.Rectangle((-0.15, 1.82), 0.30, 0.13, facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(mount_top)
    
    # 하단 바닥 지지대
    ax_main.plot([-0.4, 0.4], [-0.15, -0.15], color='#2b2b2b', lw=2.5)
    for hx in np.linspace(-0.38, 0.34, 8):
        ax_main.plot([hx, hx + 0.05], [-0.15, -0.25], color='#666666', lw=1.2)
    
    # 우측 벽면 지지대 (x = 2.0)
    ax_main.plot([2.08, 2.08], [-0.2, 0.2], color='#2b2b2b', lw=2.5)
    for hy in np.linspace(-0.18, 0.15, 6):
        ax_main.plot([2.08, 2.18], [hy, hy + 0.04], color='#666666', lw=1.2)
    anchor_mount = patches.Polygon([[2.0, 0.0], [2.08, 0.08], [2.08, -0.08]],
                                   facecolor='#a0b2c6', edgecolor='#2b2b2b', lw=1.5)
    ax_main.add_patch(anchor_mount)
    ax_main.plot(x_anchor, y_anchor, 'o', color='#2b2b2b', markersize=5)
    
    # 수직 안내봉 (원통 강봉)
    ax_main.plot([0.0, 0.0], [-0.15, 1.85], color='#4682b4', lw=8.0, solid_capstyle='round', zorder=2)
    ax_main.plot([0.0, 0.0], [-0.15, 1.85], color='#d0e4f7', lw=3.0, solid_capstyle='round', zorder=2)
    
    # 가상 B점 스프링 (점선)
    draw_spring(ax_main, (0.0, 1.5), (x_anchor, y_anchor), nodes=16, width=0.045, color='#bbbbbb', lw=1.2)
    
    # 현재 작동 스프링
    draw_spring(ax_main, (0.0, y), (x_anchor, y_anchor), nodes=15, width=0.055, color='#2b2b2b', lw=2.0)
    ax_main.text(1.0, 0.10, r'$k = 30\ \mathrm{N/m}$', ha='center', fontsize=10.5, fontweight='bold', color='#1a5276')
    
    # 슬라이더 칼라 (원통형 블록)
    cw, ch = 0.28, 0.24
    c_rect = patches.Rectangle((-cw/2, y - ch/2), cw, ch,
                               facecolor='#b87333', edgecolor='#5a2d0c', lw=1.8, zorder=5)
    ax_main.add_patch(c_rect)
    ax_main.plot(0.0, y, 'o', color='#2b2b2b', markersize=4, zorder=6)
    
    # 50 N 외력 벡터 (30도 경사, 좌상향)
    F_len = 0.45
    Fx = -F_len * np.sin(phi)
    Fy = F_len * np.cos(phi)
    ax_main.annotate('', xy=(Fx, y + Fy), xytext=(0.0, y),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15), zorder=7)
    ax_main.text(Fx - 0.12, y + Fy + 0.04, r'$50\ \mathrm{N}$', color='#d32f2f', fontsize=11, fontweight='bold')
    
    # 30도 각도 보조선
    ax_main.plot([-0.25, 0.0], [y + 0.45, y], color='#777777', ls=':', lw=1.0)
    ax_main.text(-0.22, y + 0.28, r'$30^\circ$', fontsize=10, color='#333333')
    
    # 속도 화살표
    if v_curr > 0.1:
        v_scale = 0.05 * (v_curr / v_final)
        ax_main.annotate('', xy=(0.0, y + ch/2 + v_scale), xytext=(0.0, y + ch/2),
                         arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5, mutation_scale=14), zorder=7)
    
    # 치수선: 수직 1.5 m 및 수평 2 m
    ax_main.plot([-0.5, -0.5], [0.0, 1.5], color='#333333', lw=1.2)
    ax_main.plot([-0.55, 0.0], [0.0, 0.0], color='#777777', ls='--', lw=1.0)
    ax_main.plot([-0.55, 0.0], [1.5, 1.5], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(-0.5, 1.5), xytext=(-0.5, 0.9), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(-0.5, 0.0), xytext=(-0.5, 0.6), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(-0.72, 0.75, r'$1.5\ \mathrm{m}$', va='center', fontsize=11, fontweight='bold')
    
    # 수평 2 m 치수선
    ax_main.plot([0.0, 2.0], [-0.3, -0.3], color='#333333', lw=1.2)
    ax_main.plot([0.0, 0.0], [-0.15, -0.33], color='#777777', ls='--', lw=1.0)
    ax_main.plot([2.0, 2.0], [0.0, -0.33], color='#777777', ls='--', lw=1.0)
    ax_main.annotate('', xy=(0.0, -0.3), xytext=(0.8, -0.3), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.annotate('', xy=(2.0, -0.3), xytext=(1.2, -0.3), arrowprops=dict(arrowstyle='->', color='#333333'))
    ax_main.text(1.0, -0.27, r'$2\ \mathrm{m}$', ha='center', fontsize=11, fontweight='bold')
    
    # 위치 A, B 표시
    ax_main.text(-0.25, 0.0, r'$A$', fontsize=13, fontweight='bold', color='#111111')
    ax_main.text(-0.25, 1.5, r'$B$', fontsize=13, fontweight='bold', color='#111111')
    
    ax_main.set_title('문제 3/122 기구도 (수직 안내봉 및 외력 칼라 시스템)', fontsize=12.5, fontweight='bold', pad=12)

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
    bar_labels = [r'$T$', r'$\Delta V_e$', r'$\Delta V_g$', r"$U'_{\mathrm{ext}}$"]
    
    for bx, val, col, lab in zip(bar_x, bar_vals, bar_colors, bar_labels):
        h_norm = (val / 70.0) * 0.9
        rect = patches.Rectangle((bx - 0.15, 0.4), 0.30, h_norm, facecolor=col, edgecolor='#2b2b2b', lw=1.5)
        ax_fbd.add_patch(rect)
        ax_fbd.text(bx, 0.28, lab, ha='center', fontsize=11, fontweight='bold')
        ax_fbd.text(bx, 0.4 + h_norm + 0.06, f'{val:.1f} J', ha='center', fontsize=9.5)
    ax_fbd.plot([0.0, 2.0], [0.4, 0.4], color='#333333', lw=1.2)
    
    summary_box = (
        f"【교재 공식 일-에너지 해석 (Problem 3/122)】\n"
        f"• 외력 비보존력 일: $U'_{{1-2}} = 50(1.5)\\cos 30^\\circ = \\mathbf{{64.95\\ \\mathrm{{J}}}}$\n"
        f"• 중력 위치에너지: $\\Delta V_g = 2(9.81)(1.5) = \\mathbf{{29.43\\ \\mathrm{{J}}}}$\n"
        f"• 탄성 위치에너지 변화:\n"
        f"  $L_A = 2.0\\ \\mathrm{{m}},\\quad L_B = \\sqrt{{2^2 + 1.5^2}} = 2.5\\ \\mathrm{{m}}$\n"
        f"  $\\Delta V_e = \\frac{{1}}{{2}}(30)[(2.5 - 1.5)^2 - (2.0 - 1.5)^2] = \\mathbf{{11.25\\ \\mathrm{{J}}}}$\n"
        f"• 일-에너지 방정식: $U'_{{1-2}} = \\Delta T + \\Delta V_e + \\Delta V_g$\n"
        f"  $64.95 = \\frac{{1}}{{2}}(2)v^2 + 11.25 + 29.43$\n"
        f"  $v^2 = 24.27\\ \\rightarrow\\ v = \\mathbf{{4.93\\ \\mathrm{{m/s}}}}$\n"
        f"─────────────────────────────\n"
        f"• 현재 고리 상승: $y = {y:.2f}\\ /\\ 1.50\\ \\mathrm{{m}}$\n"
        f"• 현재 속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (B점 통과: $4.93\\ \\mathrm{{m/s}}$)"
    )
    ax_fbd.text(0.0, -0.65, summary_box, fontsize=9.2, va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fbfcfd', edgecolor='#bdc3c7', lw=1.5))
    
    ax_fbd.set_title('일-에너지 원리 모니터 및 이론 검증', fontsize=12.5, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prob3_122_incline_collar_spring.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
