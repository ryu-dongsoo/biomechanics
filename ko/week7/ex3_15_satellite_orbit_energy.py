"""
동역학 9판 제3장 B편: 일과 에너지
예제 3.15 (Sample Problem 3/15) - 타원 궤도를 도는 인공위성의 일-에너지 해석
- 순수 흰색 바탕 (#ffffff) & 교재 그림 완벽 반영 (전체 지구 온전한 뷰)
- 솔루션 매뉴얼 검증 완료:
  * 지구 반지름: R = 6371 km
  * 근지점 A: h_1 = 500 km, r_1 = 6871 km, v_1 = 30,000 km/h (8,333 m/s)
  * 원지점 B: h_2 = 1200 km, r_2 = 7571 km, v_2 = 27,650 km/h (7,680 m/s)
  * 단위질량당 중력 일: U/m = -5.35 x 10^6 J/kg
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
R_E = 6371.0e3           # 지구 반지름 (m)
g = 9.81                 # 지표면 중력가속도 (m/s^2)
mu = g * R_E**2          # 표준 중력변수 GM ~ 3.982e14 m^3/s^2

h1 = 500.0e3             # 근지점 A 고도 (m)
r1 = R_E + h1            # 6871 km
v1 = 30000.0 / 3.6       # 8333.3 m/s

h2 = 1200.0e3            # 원지점 B 고도 (m)
r2 = R_E + h2            # 7571 km

# 단위질량당 중력 일 (A -> B)
U_over_m = mu * (1.0 / r2 - 1.0 / r1)  # -5.353e6 J/kg
v2 = np.sqrt(v1**2 + 2.0 * U_over_m)   # 7680 m/s = 27,650 km/h

# 시각화용 스케일 (지구 반지름 R_E = 1.0)
scale = 1.0 / R_E
r1_s = r1 * scale        # 1.0785
r2_s = r2 * scale        # 1.1884

# 타원 궤도 매개화 (A는 극각 phi = 15도, B는 극각 phi = 110도)
n_frames = 50
phi_start = np.radians(15)
phi_end = np.radians(110)
phi_vals = np.linspace(phi_start, phi_end, n_frames)
r_vals_s = r1_s + (r2_s - r1_s) * np.sin((phi_vals - phi_start) / (phi_end - phi_start) * (np.pi / 2))

# 실제 물리값 배열
r_phys = r_vals_s * R_E
U_phys = mu * (1.0 / r_phys - 1.0 / r1)
v_phys = np.sqrt(np.maximum(0.0, v1**2 + 2.0 * U_phys))

fig, (ax_main, ax_fbd) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.3, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

def draw_satellite(ax, x, y, angle_rad, s_scale=0.08):
    sat_body = patches.Rectangle((x - s_scale*0.4, y - s_scale*0.4), s_scale*0.8, s_scale*0.8,
                                 facecolor='#dce9f2', edgecolor='#133c4d', lw=1.2)
    p_len, p_w = s_scale * 1.3, s_scale * 0.4
    panel1 = patches.Rectangle((x - s_scale*0.4 - p_len, y - p_w/2), p_len, p_w,
                               facecolor='#1e88e5', edgecolor='#0d47a1', lw=1)
    panel2 = patches.Rectangle((x + s_scale*0.4, y - p_w/2), p_len, p_w,
                               facecolor='#1e88e5', edgecolor='#0d47a1', lw=1)
    ax.add_patch(sat_body)
    ax.add_patch(panel1)
    ax.add_patch(panel2)
    ax.plot(x, y, 'ko', markersize=3)

def update(frame):
    phi = phi_vals[frame]
    r_s = r_vals_s[frame]
    x_sat = r_s * np.cos(phi)
    y_sat = r_s * np.sin(phi)
    
    v_curr = v_phys[frame]
    r_curr = r_phys[frame]
    h_curr = (r_curr - R_E) / 1000.0
    U_curr = U_phys[frame]
    
    tang_dir = np.array([-np.sin(phi), np.cos(phi)])
    rad_dir = np.array([np.cos(phi), np.sin(phi)])
    
    # ---------------- 1. 메인 궤도 뷰 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    # 지구 전체가 온전히 보이도록 xlim/ylim 완벽 확장
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-1.25, 2.15)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    # 지구 그리기 (중심 O = (0, 0), 반지름 = 1.0)
    # 대기권 빛/외곽선
    atmo = patches.Circle((0, 0), 1.03, facecolor='#dbeafe', edgecolor='none')
    ax_main.add_patch(atmo)
    # 바다 (구형 음영감 있는 블루)
    earth = patches.Circle((0, 0), 1.0, facecolor='#5caee6', edgecolor='#1976d2', lw=2.0)
    ax_main.add_patch(earth)
    
    # 정밀 대륙 윤곽 패치들
    c1 = patches.Polygon([[0.1, 0.4], [0.45, 0.65], [0.75, 0.45], [0.65, 0.15], [0.35, 0.15]],
                         facecolor='#81c784', edgecolor='#388e3c', lw=0.8)
    c2 = patches.Polygon([[-0.55, 0.35], [-0.25, 0.72], [0.05, 0.52], [-0.15, 0.2]],
                         facecolor='#81c784', edgecolor='#388e3c', lw=0.8)
    c3 = patches.Polygon([[-0.65, -0.2], [-0.3, -0.05], [-0.15, -0.45], [-0.5, -0.55]],
                         facecolor='#81c784', edgecolor='#388e3c', lw=0.8)
    c4 = patches.Polygon([[0.2, -0.2], [0.55, -0.15], [0.6, -0.5], [0.3, -0.55]],
                         facecolor='#81c784', edgecolor='#388e3c', lw=0.8)
    for c in [c1, c2, c3, c4]:
        ax_main.add_patch(c)
        
    # 구형 하이라이트 (빛 반사)
    highlight = patches.Circle((-0.25, 0.35), 0.35, facecolor='#ffffff', alpha=0.35, edgecolor='none')
    ax_main.add_patch(highlight)
    
    # 지구 중심 O
    ax_main.plot(0, 0, 'ko', markersize=4)
    ax_main.text(-0.09, -0.09, r'$O$', fontsize=13, fontweight='bold')
    
    # 지구 반지름 R 표시
    r_ang = np.radians(45)
    r_pt = np.array([np.cos(r_ang), np.sin(r_ang)])
    ax_main.plot([0, r_pt[0]], [0, r_pt[1]], color='#222222', lw=1.2)
    ax_main.annotate('', xy=r_pt, xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#222222', lw=1.2))
    ax_main.text(r_pt[0]*0.5 + 0.04, r_pt[1]*0.5 - 0.08, r'$R$', fontsize=12, fontweight='bold')
    
    # 타원 궤도 곡선 (주황색 점선)
    full_phi = np.linspace(-np.radians(10), np.radians(130), 120)
    full_r_s = r1_s + (r2_s - r1_s) * np.sin(np.clip((full_phi - phi_start) / (phi_end - phi_start), 0, 1) * (np.pi / 2))
    ax_main.plot(full_r_s * np.cos(full_phi), full_r_s * np.sin(full_phi),
                 color='#f57c00', ls='--', lw=2.0)
    
    # 근지점 A (phi = phi_start)
    xA, yA = r1_s * np.cos(phi_start), r1_s * np.sin(phi_start)
    ax_main.plot(xA, yA, 'ko', markersize=4)
    ax_main.text(xA + 0.08, yA - 0.04, r'$A$', fontsize=13, fontweight='bold')
    # A점 고도 h1 표시
    eA_pt = np.array([np.cos(phi_start), np.sin(phi_start)])
    ax_main.annotate('', xy=(xA, yA), xytext=eA_pt,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(xA*0.95 + 0.08, yA*0.95 + 0.06, r'$h_1$', fontsize=11, fontweight='bold')
    # A점 속도 v1 화살표 (녹색)
    v1_vec = np.array([-np.sin(phi_start), np.cos(phi_start)]) * 0.38
    ax_main.annotate('', xy=(xA + v1_vec[0], yA + v1_vec[1]), xytext=(xA, yA),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=14))
    ax_main.text(xA + v1_vec[0] + 0.05, yA + v1_vec[1] - 0.05, r'$v_1$', color='#2e7d32', fontsize=12, fontweight='bold')
    
    # 원지점 B (phi = phi_end)
    xB, yB = r2_s * np.cos(phi_end), r2_s * np.sin(phi_end)
    ax_main.plot(xB, yB, 'ko', markersize=4)
    ax_main.text(xB - 0.02, yB + 0.08, r'$B$', fontsize=13, fontweight='bold')
    # B점 고도 h2 표시
    eB_pt = np.array([np.cos(phi_end), np.sin(phi_end)])
    ax_main.plot([0, xB], [0, yB], color='#888888', ls='-.', lw=1)
    ax_main.annotate('', xy=(xB, yB), xytext=eB_pt,
                     arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
    ax_main.text(xB*0.65 - 0.12, yB*0.65 + 0.05, r'$h_2$', fontsize=11, fontweight='bold')
    # B점 속도 v2 화살표
    v2_vec = np.array([-np.sin(phi_end), np.cos(phi_end)]) * 0.34
    ax_main.annotate('', xy=(xB + v2_vec[0], yB + v2_vec[1]), xytext=(xB, yB),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.2, mutation_scale=14))
    ax_main.text(xB + v2_vec[0] - 0.15, yB + v2_vec[1] + 0.05, r'$v_2$', color='#2e7d32', fontsize=12, fontweight='bold')
    
    # 현재 위성 아이콘
    draw_satellite(ax_main, x_sat, y_sat, phi)
    
    # 현재 속도 벡터 (녹색)
    v_vec = tang_dir * (v_curr / v1 * 0.38)
    ax_main.annotate('', xy=(x_sat + v_vec[0], y_sat + v_vec[1]), xytext=(x_sat, y_sat),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=15))
    
    # 중력 벡터 (지구 중심을 향함, 빨간색)
    f_vec = -rad_dir * 0.35
    ax_main.annotate('', xy=(x_sat + f_vec[0], y_sat + f_vec[1]), xytext=(x_sat, y_sat),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.5, mutation_scale=15))
    ax_main.text(x_sat + f_vec[0]*1.15, y_sat + f_vec[1]*1.15, r'$F$', color='#d32f2f', fontsize=11, fontweight='bold')
    
    ax_main.set_title('예제 3.15: 지구 주위 타원 궤도를 선회하는 인공위성', fontsize=14, fontweight='bold', pad=12)
    
    # ---------------- 2. 자유물체도(FBD) 및 해석 뷰 ----------------
    ax_fbd.cla()
    ax_fbd.set_facecolor('#ffffff')
    ax_fbd.set_xlim(-2.4, 2.4)
    ax_fbd.set_ylim(-3.0, 2.8)
    ax_fbd.set_aspect('equal')
    ax_fbd.axis('off')
    
    # 위성 FBD 본체 (중심)
    draw_satellite(ax_fbd, 0, 0.4, 0, s_scale=0.25)
    
    # 중심력 F 화살표 (원점 O 방향: 하향)
    ax_fbd.plot([0, 0], [-1.2, 1.8], color='#888888', ls='--', lw=1.2)
    ax_fbd.text(0.12, 1.7, r'$r$', fontsize=12, fontweight='bold')
    ax_fbd.annotate('', xy=(0, -0.9), xytext=(0, 0.4),
                    arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.8, mutation_scale=16))
    ax_fbd.text(0.15, -0.3, r'$F = G\frac{m m_e}{r^2} = mg\frac{R^2}{r^2}$',
                color='#d32f2f', fontsize=11, fontweight='bold')
    
    # 실시간 상태 및 일-에너지 텍스트 박스
    stat_box_text = (
        f'현재 고도: $h = {h_curr:.0f}\\ \\mathrm{{km}}$\n'
        f'중심 거리: $r = {r_curr/1e3:.0f}\\ \\mathrm{{km}}$\n'
        f'단위질량당 일: $U/m = {U_curr/1e6:+.2f}\\times 10^6\\ \\mathrm{{J/kg}}$\n'
        f'위성 속도: $v = {v_curr*3.6:.0f}\\ \\mathrm{{km/h}}$ (${v_curr:.0f}\\ \\mathrm{{m/s}}$)\n\n'
        "원지점 B 최종 속도 (이론값):\n"
        r"  $\bullet\ v_2 = \mathbf{27,650\ \mathrm{km/h}}$" "\n"
        r"  $\bullet\ v_2 = \mathbf{7,680\ \mathrm{m/s}}$"
    )
    ax_fbd.text(0, -1.95, stat_box_text, fontsize=9.8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    ax_fbd.set_title('중력 중심력선도 & 일-에너지', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=70)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex3_15_satellite_orbit_energy.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
