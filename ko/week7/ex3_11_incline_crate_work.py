"""
동역학 9판 제3장 B편: 일과 에너지
예제 3.11 (Sample Problem 3/11) - 경사면을 미끄러져 내려가는 상자의 일-에너지 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영
- 솔루션 매뉴얼 검증 완료:
  * U_g = +1269.5 J, U_f = -1421.4 J, U_total = -151.9 J
  * v_1 = 4.00 m/s -> v_2 = 3.15 m/s
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
m = 50.0            # 질량 (kg)
g = 9.81            # 중력가속도 (m/s^2)
theta_deg = 15.0    # 경사각 (도)
theta = np.radians(theta_deg)
mu_k = 0.30         # 운동마찰계수
v1 = 4.0            # 초기 속도 (m/s)
s_total = 10.0      # 이동 거리 (m)

# 힘 계산
W = m * g                          # 490.5 N
N = W * np.cos(theta)              # 수직항력 R = 473.8 N
F_f = mu_k * N                     # 마찰력 = 142.1 N

# 가속도 (경사면 아래 방향)
# a = g * sin(theta) - mu_k * g * cos(theta)
a = g * np.sin(theta) - mu_k * g * np.cos(theta)  # 음수 가속도 (감속)

# 일과 에너지 계산
U_g = W * np.sin(theta) * s_total  # +1269.5 J
U_f = -F_f * s_total               # -1421.4 J
U_total = U_g + U_f                # -151.9 J
T1 = 0.5 * m * v1**2               # 400.0 J
T2 = T1 + U_total                  # 248.1 J
v2 = np.sqrt(2 * T2 / m)           # 3.15 m/s

# 운동 시간
t_total = (v2 - v1) / a            # 약 2.79 초

# 애니메이션 설정
n_frames = 50
t_vals = np.linspace(0, t_total, n_frames)

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

# 단위 벡터 (접선: A->B 아래쪽, 법선: 위쪽)
tang_vec = np.array([-np.cos(theta), -np.sin(theta)])
norm_vec = np.array([-np.sin(theta), np.cos(theta)])

# 경사면 좌표 설정 (A: 우상단, B: 좌하단)
x_B, y_B = 2.2, 1.8
x_A = x_B + s_total * np.cos(theta)
y_A = y_B + s_total * np.sin(theta)

box_w, box_h = 1.3, 0.75

def update(frame):
    t = t_vals[frame]
    s_curr = v1 * t + 0.5 * a * t**2
    v_curr = v1 + a * t
    T_curr = 0.5 * m * v_curr**2
    Ug_curr = W * np.sin(theta) * s_curr
    Uf_curr = -F_f * s_curr
    Utot_curr = Ug_curr + Uf_curr
    
    # ---------------- 1. 메인 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0, 14.5)
    ax_main.set_ylim(0.2, 6.8)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 경사면 선 및 지면 해칭 (교재 스타일)
    ax_main.plot([x_B - 1.5, x_B, x_A + 1.2], [y_B, y_B, y_A + 1.2 * np.sin(theta)], color='#2b2b2b', lw=2.2)
    ramp_poly = np.array([
        [x_B - 1.5, y_B],
        [x_B, y_B],
        [x_A + 1.2, y_A + 1.2 * np.sin(theta)],
        [x_A + 1.2, 0.6],
        [x_B - 1.5, 0.6]
    ])
    ax_main.fill(ramp_poly[:, 0], ramp_poly[:, 1], color='#f4ede4', edgecolor='none')
    ax_main.plot([x_B - 1.5, x_A + 1.2], [0.6, 0.6], color='#b0a89f', lw=1.0)
    
    # 수평 기준선 및 각도 표시 (15도)
    ax_main.plot([x_B - 0.6, x_B + 3.2], [y_B, y_B], color='#777777', ls='--', lw=1.2)
    arc = patches.Arc((x_B, y_B), 3.2, 3.2, angle=0, theta1=0, theta2=theta_deg, color='#222222', lw=1.5)
    ax_main.add_patch(arc)
    ax_main.text(x_B + 2.0, y_B + 0.25, r'$15^\circ$', fontsize=12, fontweight='bold', color='#222222')
    
    # 치수선: A와 B 사이 10 m
    offset = 1.4
    pA_dim = np.array([x_A, y_A]) + offset * norm_vec
    pB_dim = np.array([x_B, y_B]) + offset * norm_vec
    ax_main.plot([x_A, pA_dim[0]], [y_A, pA_dim[1]], color='#888888', lw=1)
    ax_main.plot([x_B, pB_dim[0]], [y_B, pB_dim[1]], color='#888888', lw=1)
    ax_main.annotate('', xy=pB_dim, xytext=pA_dim,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.3))
    dim_center = 0.5 * (pA_dim + pB_dim) + 0.22 * norm_vec
    ax_main.text(dim_center[0], dim_center[1], '10 m', fontsize=11, ha='center', va='bottom',
                 rotation=theta_deg, fontweight='bold')
    
    # 위치 A, B 마커
    ax_main.plot(x_A, y_A, 'ko', markersize=4)
    ax_main.text(x_A + 0.1, y_A + 0.35, r'$A$', fontsize=13, fontweight='bold')
    ax_main.plot(x_B, y_B, 'ko', markersize=4)
    ax_main.text(x_B - 0.35, y_B + 0.35, r'$B$', fontsize=13, fontweight='bold')
    
    # 상자 현재 위치
    crate_base = np.array([x_A, y_A]) + s_curr * tang_vec
    crate_center = crate_base + (box_h / 2.0) * norm_vec
    
    # 상자 본체 (회전 단 한 번만 적용)
    crate_poly = patches.Rectangle((-box_w/2, -box_h/2), box_w, box_h,
                                   facecolor='#bdd8ea', edgecolor='#1d4564', lw=2.0)
    trans = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(crate_center[0], crate_center[1]) + ax_main.transData
    crate_poly.set_transform(trans)
    ax_main.add_patch(crate_poly)
    
    # 상자 위 50 kg 텍스트
    ax_main.text(crate_center[0], crate_center[1], '50 kg', fontsize=10.5, fontweight='bold',
                 ha='center', va='center', color='#1d4564')
    
    # 속도 벡터 (상자 앞쪽에서 경사면 아래로 연장, 치수선과 겹치지 않게 배치)
    v_start = crate_center + (box_w/2 + 0.1) * tang_vec - 0.15 * norm_vec
    v_len = v_curr * 0.35
    v_end = v_start + v_len * tang_vec
    ax_main.annotate('', xy=v_end, xytext=v_start,
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
    ax_main.text(v_start[0] + 0.5 * (v_end[0] - v_start[0]) - 0.2, v_start[1] + 0.32,
                 f'$v = {v_curr:.2f}\\ \\mathrm{{m/s}}$', color='#2e7d32', fontsize=11, fontweight='bold', ha='center')
    
    ax_main.set_title('예제 3.11: 경사면을 따라 미끄러지는 상자', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 자유물체도 (FBD) ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-2.8, 2.8)
    ax_fbd.set_ylim(-3.2, 3.2)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    # FBD 상자 본체 (경사각 15도로 기울어짐)
    fbd_w, fbd_h = 1.6, 0.85
    fbd_crate = patches.Rectangle((-fbd_w/2, -fbd_h/2), fbd_w, fbd_h,
                                  facecolor='#bdd8ea', edgecolor='#1d4564', lw=2.0)
    t_fbd = plt.matplotlib.transforms.Affine2D().rotate_deg(theta_deg).translate(0, 0.35) + ax_fbd.transData
    fbd_crate.set_transform(t_fbd)
    ax_fbd.add_patch(fbd_crate)
    
    fbd_center = np.array([0, 0.35])
    
    # FBD 힘 벡터들 (교재 그림 완벽 일치: 화살표가 작용면/질량중심을 향함)
    # 1) 중력: 위에서 중심을 향해 수직 하향 W = 50(9.81) N
    ax_fbd.annotate('', xy=fbd_center, xytext=fbd_center + np.array([0, 1.4]),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(fbd_center[0], fbd_center[1] + 1.55, r'$50(9.81)\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center')
    
    # 2) 수직항력 R: 아래에서 바닥면을 향해 경사면 법선 방향 (105도 = 2사분면 방향)
    norm_dir = np.array([-np.sin(theta), np.cos(theta)])
    contact_pt = fbd_center - (fbd_h/2) * norm_dir
    r_start = contact_pt - 1.1 * norm_dir
    ax_fbd.annotate('', xy=contact_pt, xytext=r_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(r_start[0], r_start[1] - 0.22, r'$R = 474\ \mathrm{N}$',
                color='#d32f2f', fontsize=11, fontweight='bold', ha='center', va='top')
    
    # 3) 마찰력 mu_k * R: 경사면을 따라 위쪽 방향 (+15도, 1사분면)
    up_slope = np.array([np.cos(theta), np.sin(theta)])
    friction_end = contact_pt
    friction_start = friction_end - 1.2 * up_slope
    ax_fbd.annotate('', xy=friction_end, xytext=friction_start,
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_fbd.text(friction_start[0] - 0.15, friction_start[1] - 0.1,
                r'$\mu_k R = 142.1\ \mathrm{N}$', color='#d32f2f', fontsize=10.5, fontweight='bold', ha='right')
    
    # 정보 텍스트 박스
    info_text = (
        f'이동 거리: $s = {s_curr:.2f}\\ /\\ 10.00\\ \\mathrm{{m}}$\n'
        f'중력 일: $U_g = {Ug_curr:+.1f}\\ \\mathrm{{J}}$   마찰력 일: $U_f = {Uf_curr:+.1f}\\ \\mathrm{{J}}$\n'
        f'총 일량: $U_{{1-2}} = {Utot_curr:+.1f}\\ \\mathrm{{J}}$   운동에너지: $T = {T_curr:.1f}\\ \\mathrm{{J}}$\n'
        f'속도: $v = {v_curr:.2f}\\ \\mathrm{{m/s}}$ (최종: $3.15\\ \\mathrm{{m/s}}$)'
    )
    ax_fbd.text(0, -2.35, info_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('자유물체도 (FBD) 및 일-에너지', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=60)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_11_incline_crate_work.gif')
anim.save(gif_path, writer='pillow', fps=16)
plt.close()
print(f'Saved: {gif_path}')
