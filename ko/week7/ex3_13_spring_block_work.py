"""
동역학 9판 제3장 B편: 일과 에너지
예제 3.13 (Sample Problem 3/13) - 스프링과 케이블 견인에 의한 블록의 운동
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영
- 솔루션 매뉴얼 검증 완료:
  * 스프링 일: U_s = -80.0 J
  * 케이블 일: U_cable = +180.0 J
  * 순 일량: U_total = +100.0 J
  * B지점 도달 속도: v_B = 2.00 m/s
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
m = 50.0        # 질량 (kg)
k = 80.0        # 스프링 상수 (N/m)
P = 300.0       # 케이블 인장력 (N)
x1 = 0.233      # A 위치에서 스프링 초기 늘어남 (m)
d_AB = 1.2      # A에서 B까지 수평 거리 (m)
h_C = 0.9       # 도르래 C의 높이 (m)

# 기하학적 초기치
L1 = np.sqrt(d_AB**2 + h_C**2)  # 1.50 m
L2 = h_C                         # 0.90 m
delta_s_C = L1 - L2              # 0.60 m

# 총 일량 및 최종 속도
U_s_final = -0.5 * k * ((x1 + d_AB)**2 - x1**2) # -80.0 J
U_cable_final = P * delta_s_C                   # +180.0 J
U_total_final = U_s_final + U_cable_final       # +100.0 J
v_B = np.sqrt(2 * U_total_final / m)            # 2.00 m/s

# 궤적 생성 (수치 적분 dt = dx / v(x))
x_grid = np.linspace(0.0, d_AB, 200)
U_grid = np.zeros_like(x_grid)
v_grid = np.zeros_like(x_grid)

for i, x in enumerate(x_grid):
    U_s = -0.5 * k * ((x1 + x)**2 - x1**2)
    L_curr = np.sqrt((d_AB - x)**2 + h_C**2)
    U_c = P * (L1 - L_curr)
    Utot = max(0.0, U_s + U_c)
    U_grid[i] = Utot
    v_grid[i] = np.sqrt(2 * Utot / m)

dt_grid = 1.0 / np.maximum(v_grid, 0.05)
t_steps = 0.5 * (dt_grid[:-1] + dt_grid[1:]) * np.diff(x_grid)
t_grid = np.concatenate([[0], np.cumsum(t_steps)])
t_total = t_grid[-1]

# 애니메이션 시간 프레임
n_frames = 50
t_anim = np.linspace(0, t_total, n_frames)
x_anim = np.interp(t_anim, t_grid, x_grid)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_spring(ax, start, end, n_turns=11, width=0.10):
    vec = np.array(end) - np.array(start)
    length = np.linalg.norm(vec)
    if length < 1e-4:
        return
    unit_vec = vec / length
    norm_vec = np.array([-unit_vec[1], unit_vec[0]])
    
    lead_in = 0.12 * length
    lead_out = 0.12 * length
    active_len = length - lead_in - lead_out
    
    xs = [0, lead_in]
    ys = [0, 0]
    turn_step = active_len / n_turns
    for i in range(n_turns):
        xs.append(lead_in + (i + 0.25) * turn_step)
        ys.append(width)
        xs.append(lead_in + (i + 0.75) * turn_step)
        ys.append(-width)
    xs.extend([length - lead_out, length])
    ys.extend([0, 0])
    
    pts = np.array([np.array(start) + x * unit_vec + y * norm_vec for x, y in zip(xs, ys)])
    ax.plot(pts[:, 0], pts[:, 1], color='#333333', lw=1.8)

def update(frame):
    x_curr = x_anim[frame]
    L_curr = np.sqrt((d_AB - x_curr)**2 + h_C**2)
    s_C_curr = L1 - L_curr
    
    Us_curr = -0.5 * k * ((x1 + x_curr)**2 - x1**2)
    Uc_curr = P * s_C_curr
    Utot_curr = Us_curr + Uc_curr
    v_curr = np.sqrt(2 * max(0.0, Utot_curr) / m)
    T_curr = 0.5 * m * v_curr**2
    
    # ---------------- 1. 메인 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-0.85, 2.3)
    ax_main.set_ylim(-0.6, 1.45)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 레일 베이스 (연청색 슬롯 베이스)
    rail_base = patches.Rectangle((-0.7, -0.22), 2.7, 0.40, facecolor='#cbe2ee', edgecolor='#56829a', lw=1.8)
    ax_main.add_patch(rail_base)
    # 슬롯 구멍
    slot = patches.Rectangle((-0.45, -0.04), 2.2, 0.08, facecolor='#ffffff', edgecolor='#56829a', lw=1.2)
    ax_main.add_patch(slot)
    
    # 좌측 고정 벽 브래킷
    wall_bracket = patches.Polygon([[-0.7, -0.22], [-0.7, 0.32], [-0.55, 0.32], [-0.55, 0.1], [-0.55, -0.22]],
                                  facecolor='#a4c5d8', edgecolor='#56829a', lw=1.8)
    ax_main.add_patch(wall_bracket)
    
    # 가이드 중심선 (dash-dot)
    ax_main.plot([-0.5, 1.8], [0, 0], color='#888888', ls='-.', lw=1.2)
    
    # 도르래 C 브래킷 및 도르래
    pulley_x, pulley_y = d_AB, h_C
    pulley_sup = patches.Polygon([[pulley_x - 0.09, pulley_y - 0.22], [pulley_x + 0.09, pulley_y - 0.22], [pulley_x, pulley_y]],
                                 facecolor='#d0dbe2', edgecolor='#56829a', lw=1.4)
    ax_main.add_patch(pulley_sup)
    ax_main.plot([pulley_x - 0.13, pulley_x + 0.13], [pulley_y - 0.22, pulley_y - 0.22], color='#333333', lw=2)
    ax_main.add_patch(patches.Circle((pulley_x, pulley_y), 0.045, facecolor='#ffffff', edgecolor='#333333', lw=1.5))
    ax_main.text(pulley_x - 0.08, pulley_y + 0.08, r'$C$', fontsize=13, fontweight='bold')
    
    # 수직 기준선 B - C
    ax_main.plot([pulley_x, pulley_x], [0, pulley_y], color='#888888', ls='-.', lw=1.2)
    ax_main.text(pulley_x + 0.06, pulley_y / 2, '0.9 m', fontsize=11, ha='left', va='center', fontweight='bold')
    
    # 위치 A, B 마커
    ax_main.plot(0, 0, 'ko', markersize=3.5)
    ax_main.text(0, 0.24, r'$A$', fontsize=13, fontweight='bold', ha='center')
    ax_main.plot(d_AB, 0, 'ko', markersize=3.5)
    ax_main.text(d_AB + 0.06, 0.08, r'$B$', fontsize=13, fontweight='bold', ha='left')
    
    # 치수선: A와 B 사이 1.2 m
    ax_main.plot([0, 0], [-0.28, -0.42], color='#888888', lw=1)
    ax_main.plot([d_AB, d_AB], [-0.28, -0.42], color='#888888', lw=1)
    ax_main.annotate('', xy=(d_AB, -0.38), xytext=(0, -0.38),
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(d_AB / 2, -0.44, '1.2 m', fontsize=11, ha='center', va='top', fontweight='bold')
    
    # 블록 위치
    blk_w, blk_h = 0.35, 0.24
    blk_x, blk_y = x_curr, 0
    blk = patches.Rectangle((blk_x - blk_w/2, blk_y - blk_h/2), blk_w, blk_h,
                            facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    ax_main.add_patch(blk)
    ax_main.plot(blk_x, blk_y, 'ko', markersize=3)
    ax_main.text(blk_x, blk_y - 0.05, '50 kg', fontsize=9, fontweight='bold', ha='center', va='center', color='#4a2800')
    
    # 스프링 그리기 (벽에서 블록 좌측면까지)
    draw_spring(ax_main, (-0.55, 0), (blk_x - blk_w/2, 0), n_turns=10, width=0.06)
    
    # 케이블 그리기 (블록 중심 -> 도르래 C -> 우측 수평 당김)
    ax_main.plot([blk_x, pulley_x], [blk_y, pulley_y], color='#111111', lw=2)
    pull_end_x = pulley_x + 0.45
    ax_main.plot([pulley_x, pull_end_x], [pulley_y, pulley_y], color='#111111', lw=2)
    # 300 N 인장력 화살표 (빨강)
    ax_main.annotate('', xy=(pull_end_x + 0.25, pulley_y), xytext=(pull_end_x, pulley_y),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_main.text(pull_end_x + 0.12, pulley_y + 0.08, '300 N', fontsize=11, fontweight='bold', color='#d32f2f', ha='center')
    
    # 속도 벡터 (블록 우측 전방에 깔끔하게 배치하여 케이블과 겹침 방지)
    if v_curr > 0.05:
        v_arrow_len = v_curr * 0.14
        v_start_x = blk_x + blk_w/2 + 0.05
        v_y = 0.0
        ax_main.annotate('', xy=(v_start_x + v_arrow_len, v_y), xytext=(v_start_x, v_y),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=13))
        ax_main.text(v_start_x + v_arrow_len * 0.5, v_y + 0.10, f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$',
                     color='#2e7d32', fontsize=9.5, fontweight='bold', ha='center')
        
    ax_main.set_title('예제 3.13: 수평 가이드 상의 스프링-블록-케이블 시스템', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 시스템 작용력선도 & 계산 뷰 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-1.6, 2.6)
    ax_fbd.set_ylim(-2.5, 2.5)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    # 블록 본체
    fbd_blk = patches.Rectangle((-0.4, 0.1 - 0.3), 0.8, 0.6, facecolor='#f5e4d3', edgecolor='#7a4d25', lw=2.0)
    ax_fbd.add_patch(fbd_blk)
    ax_fbd.plot(0, 0.1, 'ko', markersize=3)
    
    # 가상 도르래 위치
    fbd_c_x, fbd_c_y = 1.3, 1.3
    ax_fbd.plot([0, fbd_c_x], [0.1, fbd_c_y], color='#111111', lw=2)
    ax_fbd.add_patch(patches.Circle((fbd_c_x, fbd_c_y), 0.07, facecolor='#ffffff', edgecolor='#333333', lw=1.5))
    
    # 시스템 경계 점선 (블록 + 케이블)
    sys_bound = patches.Polygon([[-0.6, -0.4], [0.6, -0.4], [1.6, 1.1], [1.6, 1.5], [1.0, 1.6], [-0.6, 0.6]],
                                closed=True, fill=False, edgecolor='#666666', ls='--', lw=1.5)
    ax_fbd.add_patch(sys_bound)
    ax_fbd.text(0.9, 0.5, '시스템 경계', fontsize=10.5, color='#555555', rotation=35)
    
    # 외력 1: 스프링 힘 80x (좌측)
    spring_force = k * (x1 + x_curr)
    ax_fbd.annotate('', xy=(-1.2, 0.1), xytext=(-0.4, 0.1),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(-1.25, 0.22, r'$80x\ \mathrm{N}$' f'\n(${spring_force:.1f}\\ \\mathrm{{N}}$)',
                color='#d32f2f', fontsize=10.5, fontweight='bold', ha='right', va='center')
    
    # 외력 2: 케이블 인장력 300 N (우측)
    ax_fbd.annotate('', xy=(fbd_c_x + 0.9, fbd_c_y), xytext=(fbd_c_x, fbd_c_y),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(fbd_c_x + 0.45, fbd_c_y + 0.14, r'$300\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center')
    
    # 수평 변위 x 표시 (y = -0.65 에 명확히 분리)
    ax_fbd.annotate('', xy=(0, -0.65), xytext=(-0.8, -0.65),
                    arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.2))
    ax_fbd.text(-0.4, -0.75, f'$x = {x_curr:.2f}\\ \\mathrm{{m}}$', fontsize=10.5, ha='center', va='top')
    
    # 계산 결과 요약 박스 (y = -1.65 에 배치하여 치수선과 완벽 분리)
    calc_text = (
        f'스프링 일: $U_s = {Us_curr:+.1f}\\ \\mathrm{{J}}$\n'
        f'케이블 일: $U_{{\\mathrm{{cable}}}} = {Uc_curr:+.1f}\\ \\mathrm{{J}}$\n'
        f'순 일량: $U_{{1-2}} = {Utot_curr:+.1f}\\ \\mathrm{{J}}$   운동에너지: $T = {T_curr:.1f}\\ \\mathrm{{J}}$\n'
        f'속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (최종 $B$점 속도: $\\mathbf{{2.00\\ \\mathrm{{m/s}}}}$)'
    )
    ax_fbd.text(0.3, -1.65, calc_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('시스템 작용력선도 & 일-에너지', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_13_spring_block_work.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
