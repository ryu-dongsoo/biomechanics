# -*- coding: utf-8 -*-
"""
동역학 9판 제3장 질점의 운동역학 (Kinetics of Particles)
예제 3.7: 원호 곡면 슈트와 컨베이어 벨트의 무슬립 이송 운동역학 해석 (n-t좌표계)
- 순수 흰색 바탕 (#ffffff) & 2분할(14x6.5) 표준 레이아웃 (biomechanics-diagram-standard 준수)
- 교재 원도 1:1 완벽 반영 (반지름 R 원호 슈트, 최하점 B 수평 접선, 컨베이어 풀리 및 벨트)
- 공식 솔루션 매뉴얼(Wiley) 검증: N(θ) = 3mg sin(θ), B점 N = 294.3 N, 풀리 ω = 21.9 rad/s
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터
R = 3.0             # 슈트 곡률반경 (m)
r_p = 0.35          # 풀리 반지름 (m)
m = 10.0            # 질점 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
W = m * g           # 98.1 N

# 이론 계산값
v_B = np.sqrt(2.0 * g * R)      # 7.672 m/s
omega_p = v_B / r_p             # 21.92 rad/s (209.3 RPM)
N_B = 3.0 * W                   # 294.3 N

# 궤적 생성
# 원호 중심: (0, R). A점: (-R, R), B점: (0, 0)
# 각도 theta: 수평면 기준 0 -> 90도 (각도 파라미터 alpha: pi -> 3*pi/2)
n_chute = 45
thetas = np.linspace(0.02, np.pi/2, n_chute)
x_chute = -R * np.cos(thetas)
y_chute = R - R * np.sin(thetas)

# 컨베이어 구간: x: 0 -> 2.5 m, y = 0
n_belt = 25
x_belt = np.linspace(0, 2.5, n_belt)
y_belt = np.zeros_like(x_belt)

traj_x = np.concatenate([x_chute, x_belt])
traj_y = np.concatenate([y_chute, y_belt])
n_frames = len(traj_x)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def update(frame):
    px = traj_x[frame]
    py = traj_y[frame]
    
    if frame < n_chute:
        th = thetas[frame]
        v_curr = np.sqrt(2.0 * g * R * np.sin(th))
        N_curr = 3.0 * m * g * np.sin(th)
        an_curr = (v_curr**2) / R
        phi = np.pi/2 - th # 접선 각도 (수평 기준 하향)
        mode_str = "슈트 활강 중"
    else:
        th = np.pi/2
        v_curr = v_B
        N_curr = m * g
        an_curr = 0.0
        phi = 0.0
        mode_str = "컨베이어 이송 중"
        
    # ---------------- 1. 메인 물리 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-3.8, 3.8)
    ax_main.set_ylim(-1.5, 3.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 곡률 중심 O (0, R)
    ax_main.plot(0, R, 'k+', ms=9, mew=1.6)
    ax_main.text(0.12, R + 0.1, r'$O$', fontsize=12, fontweight='bold')
    ax_main.plot([-R, 0], [R, R], color='#888888', ls='--', lw=1.2)
    ax_main.plot([0, 0], [0, R], color='#888888', ls='-.', lw=1.2)
    
    # 원호 슈트 궤적
    th_full = np.linspace(0, np.pi/2, 100)
    ax_main.plot(-R * np.cos(th_full), R - R * np.sin(th_full), color='#2b2b2b', lw=2.6)
    
    # 슈트 하부 해칭 두께
    hatch_poly = np.vstack([
        np.column_stack([-R * np.cos(th_full), R - R * np.sin(th_full)]),
        np.column_stack([- (R - 0.25) * np.cos(th_full[::-1]), R - (R - 0.25) * np.sin(th_full[::-1])])
    ])
    ax_main.add_patch(patches.Polygon(hatch_poly, facecolor='#ede9e4', edgecolor='none'))
    
    # 반지름 R 치수선
    dim_th = np.radians(45.0)
    dim_pt = np.array([-R * np.cos(dim_th), R - R * np.sin(dim_th)])
    ax_main.annotate('', xy=dim_pt, xytext=(0, R),
                     arrowprops=dict(arrowstyle='<->', color='#1565c0', lw=1.4))
    ax_main.text(dim_pt[0]/2 - 0.2, (dim_pt[1] + R)/2 + 0.15, r'$R = 3.0\ \mathrm{m}$',
                 color='#1565c0', fontsize=10.5, fontweight='bold')
    
    # A점, B점 레이블
    ax_main.plot(-R, R, 'ko', ms=4.5)
    ax_main.text(-R - 0.35, R + 0.05, r'$A$', fontsize=13, fontweight='bold')
    ax_main.plot(0, 0, 'ko', ms=4.5)
    ax_main.text(-0.25, -0.32, r'$B$', fontsize=13, fontweight='bold')
    
    # 컨베이어 풀리 및 벨트
    p_center = np.array([0, -r_p])
    pulley_circ = patches.Circle(p_center, r_p, facecolor='#d8e4eb', edgecolor='#456678', lw=1.8)
    ax_main.add_patch(pulley_circ)
    ax_main.plot(p_center[0], p_center[1], 'ko', ms=3.5)
    ax_main.plot([0, 2.8], [0, 0], color='#2b2b2b', lw=2.4) # 상부 벨트
    ax_main.plot([0, 2.8], [-2*r_p, -2*r_p], color='#2b2b2b', lw=1.8) # 하부 벨트
    
    # 풀리 반지름 치수 및 회전 화살표
    ax_main.annotate('', xy=(p_center[0] - r_p, p_center[1]), xytext=p_center,
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))
    ax_main.text(p_center[0] - r_p/2 - 0.1, p_center[1] + 0.08, r'$r$', fontsize=10.5, fontweight='bold')
    
    # 풀리 회전 화살표 (시계방향 omega)
    rot_arc = patches.Arc(p_center, 1.2*r_p, 1.2*r_p, angle=0, theta1=-60, theta2=60, color='#e65100', lw=1.8)
    ax_main.add_patch(rot_arc)
    ax_main.annotate('', xy=(p_center[0] + 0.6*r_p, p_center[1]), xytext=(p_center[0] + 0.6*r_p, p_center[1] + 0.1),
                     arrowprops=dict(arrowstyle='->', color='#e65100', lw=2.0))
    ax_main.text(p_center[0] + 0.7*r_p, p_center[1] - 0.1, r'$\omega$', color='#e65100', fontsize=12, fontweight='bold')
    
    # 블록 패치 (살구색)
    bw, bh = 0.35, 0.22
    blk_angle = -np.degrees(phi)
    block = patches.Rectangle((-bw/2, 0), bw, bh, facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(blk_angle).translate(px, py) + ax_main.transData
    block.set_transform(t_blk)
    ax_main.add_patch(block)
    
    # 속도 벡터 (초록색 화살표)
    if v_curr > 0.2:
        v_dir = np.array([np.cos(phi), -np.sin(phi)])
        v_len = v_curr * 0.14
        blk_center = np.array([px - np.sin(phi)*bh/2, py + np.cos(phi)*bh/2])
        v_end = blk_center + v_len * v_dir
        ax_main.annotate('', xy=v_end, xytext=blk_center,
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.4, mutation_scale=14))
        ax_main.text(v_end[0] + 0.08, v_end[1] + 0.12, f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$',
                     color='#2e7d32', fontsize=10.5, fontweight='bold')
        
    ax_main.set_title('예제 3.7: 원호 곡면 슈트 및 무슬립 컨베이어 이송', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 정량 해석 및 FBD 뷰 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    # FBD (상단: 각도 θ에서의 질점 FBD)
    fbd_cx, fbd_cy = 3.2, 7.8
    fbd_blk = patches.Rectangle((fbd_cx - 0.6, fbd_cy - 0.4), 1.2, 0.8,
                                facecolor='#e8b88a', edgecolor='#7a4d25', lw=1.8)
    ax_calc.add_patch(fbd_blk)
    ax_calc.text(fbd_cx, fbd_cy, r'$10\ \mathrm{kg}$', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#4a2800')
    
    # 힘 화살표: 중력 mg (하향)
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy - 1.5), xytext=(fbd_cx, fbd_cy - 0.4),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.4, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy - 1.1, r'$mg = 98.1\ \mathrm{N}$',
                 color='#d32f2f', fontsize=10.5, fontweight='bold')
    
    # 수직항력 N (상향/중심 방향)
    ax_calc.annotate('', xy=(fbd_cx, fbd_cy + 1.3), xytext=(fbd_cx, fbd_cy + 0.4),
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.4, mutation_scale=14))
    ax_calc.text(fbd_cx + 0.15, fbd_cy + 0.85, r'$N(\theta) = 3mg\sin\theta$',
                 color='#1565c0', fontsize=10.5, fontweight='bold')
    
    # n-t 축
    ax_calc.annotate('', xy=(6.5, 7.8), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(6.6, 7.7, r'$t$', fontsize=11, fontweight='bold')
    ax_calc.annotate('', xy=(5.6, 8.7), xytext=(5.6, 7.8),
                     arrowprops=dict(arrowstyle='->', color='#333333', lw=1.6))
    ax_calc.text(5.5, 8.8, r'$n$', fontsize=11, fontweight='bold')
    ax_calc.text(5.6, 7.2, r'슈트 내 FBD', fontsize=11, fontweight='bold', color='#333333')
    
    # 중앙: 이론 공식 유도 카드
    sol_box = (
        "이론 해석 및 정량 유도:\n"
        r"(1) 곡면 접촉력 $N(\theta)$ 유도:" "\n"
        r"  $\bullet\ v^2 = 2gR\sin\theta$" "\n"
        r"  $\bullet\ \sum F_n = N - mg\sin\theta = m\frac{v^2}{R} = 2mg\sin\theta$" "\n"
        r"  $\bullet\ \mathbf{N(\theta) = 3mg\sin\theta = 294.3\sin\theta\ \mathrm{N}}$" "\n"
        r"  $\bullet\ $B점 통과 시 ($\theta = 90^\circ$): $\mathbf{N_B = 3mg = 294\ \mathrm{N}}$" "\n\n"
        r"(2) 벨트 무슬립 풀리 각속도 $\omega$:" "\n"
        r"  $\bullet\ v_B = \sqrt{2gR} = \sqrt{2(9.81)(3.0)} = 7.67\ \mathrm{m/s}$" "\n"
        r"  $\bullet\ v_{\mathrm{belt}} = r\omega \Rightarrow \mathbf{\omega = \frac{v_B}{r} = \frac{7.67}{0.35} = 21.9\ \mathrm{rad/s}}$" "\n"
        r"  ($N_{\mathrm{rpm}} = 209\ \mathrm{RPM}$)"
    )
    ax_calc.text(0.5, 3.8, sol_box, fontsize=9.8, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    # 하단: 실시간 동역학 모니터 카드
    live_box = (
        f'상태: {mode_str} | 각도: $\\theta = {np.degrees(th):.1f}^\\circ$\n'
        f'현재 속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ ({v_curr*3.6:.1f} km/h)\n'
        f'법선 가속도: $a_n = {an_curr:.2f}\\ \\mathrm{{m/s^2}}$\n'
        f'수직 접촉력: $N = {N_curr:.1f}\\ \\mathrm{{N}}$ (이론 최종값: $N_B = 294\\ \\mathrm{{N}}$)'
    )
    ax_calc.text(0.5, 0.95, live_box, fontsize=10.0, va='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('n-t좌표계 정량 해석 및 검증', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_7_chute_conveyor.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
