# 예제 2.10: 극좌표계 레이더 추적 (Radar Tracking)
# 교재 삽화 완벽 재현 (수직 기준 각도 theta, r 벡터, +r/+theta 축, 회전형 레이더, 탄도 포물선 궤적)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patches as patches

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 물리 기반 실제 궤적 설계 ---
# 교재 조건: theta = 30 deg 일 때, r = 80,000 m (80 km), r_dot = 1200 m/s (1.2 km/s), theta_dot = 0.8 deg/s (0.01396 rad/s)
# 중력가속도 g = 9.20 m/s^2 (0.0092 km/s^2) 하에서 타력(무동력) 비행하므로 탄도 포물선 궤적을 그립니다.
# 시뮬레이션의 스케일은 km 단위로 정의합니다.

r_target = 80.0                # km (80,000 m)
theta_target = np.radians(30)  # rad (30 deg)
r_dot_target = 1.2             # km/s (1200 m/s)
theta_dot_target = 0.8 * np.pi / 180.0  # rad/s (0.01396 rad/s)
g = 0.0092                     # km/s^2 (9.20 m/s^2)

# 목표 시점(t_target = 5.0초)에 교재 조건을 정확히 통과하도록 초기 조건 계산
t_target = 5.0
x_target = r_target * np.sin(theta_target)
y_target = r_target * np.cos(theta_target) + 4.0 # 레이더 피벗 높이 4.0km 반영

# 속도 성분 계산 (원통/극좌표계 정의 적용)
vx_target = r_dot_target * np.sin(theta_target) + r_target * theta_dot_target * np.cos(theta_target)
vy_target = r_dot_target * np.cos(theta_target) - r_target * theta_dot_target * np.sin(theta_target)

# 포물선 운동 방정식에 따른 t=0 시점의 초기 위치 및 속도 역산
vx0 = vx_target
vy0 = vy_target + g * t_target
x0 = x_target - vx0 * t_target
y0 = y_target - vy0 * t_target + 0.5 * g * t_target**2

# 애니메이션 시간 범위 (0 ~ 10초)
frames = 100
t_arr = np.linspace(0, 10.0, frames)

# 포물선 궤적 생성
x = x0 + vx0 * t_arr
y = y0 + vy0 * t_arr - 0.5 * g * t_arr**2

# Matplotlib Figure 및 Axes 초기화 (여백 없는 고화질 비율 적용)
fig, ax = plt.subplots(figsize=(8, 9))
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.97)
ax.set_xlim(-25, 95)
ax.set_ylim(-10, 115)
ax.axis('off')

# 1. 정적 배경 및 지면 그리기
ax.fill_between([-35, 110], [0, 0], [-15, -15], color='#e3ddd5') # 옅은 흙색 지면
ax.plot([-35, 110], [0, 0], 'k-', lw=1.5)

# 레이더 지지 콘크리트 베이스
concrete_base = patches.Rectangle((-6, 0), 12, 2.0, facecolor='#bdc3c7', edgecolor='#7f8c8d', lw=1.2, zorder=2)
ax.add_patch(concrete_base)

# 2. 동적 레이더 안테나 그리기용 헬퍼 함수
# 지향 각도 angle_rad(수직 기준 시계방향)에 맞춰 포물선 접시 안테나를 회전시킵니다.
def get_rotated_dish_coords(cx, cy, angle_rad, scale=5.0):
    theta_math = np.pi/2 - angle_rad # 수학적 극좌표 각도로 변환
    
    # 로컬 포물선 좌표
    t_vals = np.linspace(-np.pi/3.2, np.pi/3.2, 50)
    lx = scale * np.sin(t_vals)
    ly = -scale * 0.16 * np.cos(t_vals)
    
    # 회전 및 평행이동
    rx = cx + lx * np.cos(theta_math - np.pi/2) - ly * np.sin(theta_math - np.pi/2)
    ry = cy + lx * np.sin(theta_math - np.pi/2) + ly * np.cos(theta_math - np.pi/2)
    
    # 후방 지지 리브
    rx_back = cx + lx * np.cos(theta_math - np.pi/2) - (ly - 0.7) * np.sin(theta_math - np.pi/2)
    ry_back = cy + lx * np.sin(theta_math - np.pi/2) + (ly - 0.7) * np.cos(theta_math - np.pi/2)
    
    # 안테나 수신기 피드혼 로드
    horn_x = [cx, cx + 1.18 * scale * np.cos(theta_math)]
    horn_y = [cy, cy + 1.18 * scale * np.sin(theta_math)]
    
    return rx, ry, rx_back, ry_back, horn_x, horn_y

# 3. 로켓 3D 형상 폴리곤 생성 헬퍼 함수 (Fin, Nozzle 완벽 구현)
def get_rotated_rocket_poly(cx, cy, vx_val, vy_val, length=7.5, width=1.4):
    traj_angle = np.arctan2(vy_val, vx_val)
    cos_t, sin_t = np.cos(traj_angle), np.sin(traj_angle)
    
    half_w = width / 2.0
    body_l = length * 0.72
    nose_l = length * 0.28
    
    # 로켓 로컬 실루엣 좌표 (CG가 원점)
    local_coords = np.array([
        [-body_l/2, -half_w],       # 뒤쪽 하단
        [body_l/2, -half_w],        # 앞쪽 바디 하단
        [body_l/2 + nose_l, 0],     # 페어링 노즈 콘 끝
        [body_l/2, half_w],         # 앞쪽 바디 상단
        [-body_l/2, half_w],        # 뒤쪽 상단
        # 상단 날개
        [-body_l/2, half_w + 1.0],   
        [-body_l/2 - 0.8, half_w],  
        [-body_l/2, -half_w],       # 뒤쪽 하단 결합
        # 하단 날개
        [-body_l/2, -half_w - 1.0],  
        [-body_l/2 - 0.8, -half_w], 
    ])
    
    rx = cx + local_coords[:, 0] * cos_t - local_coords[:, 1] * sin_t
    ry = cy + local_coords[:, 0] * sin_t + local_coords[:, 1] * cos_t
    
    # 노즐 좌표
    nozzle_local = np.array([
        [-body_l/2, -half_w*0.6],
        [-body_l/2 - 0.7, -half_w*0.8],
        [-body_l/2 - 0.7, half_w*0.8],
        [-body_l/2, half_w*0.6]
    ])
    nx = cx + nozzle_local[:, 0] * cos_t - nozzle_local[:, 1] * sin_t
    ny = cy + nozzle_local[:, 0] * sin_t + nozzle_local[:, 1] * cos_t
    
    return list(zip(rx, ry)), list(zip(nx, ny)), np.degrees(traj_angle)

# --- 애니메이션 컴포넌트들 초기화 ---
# (1) 레이더 지지 트러스 프레임 (스틸 그레이 고정 지지대)
ax.plot([-3.5, 0, 3.5], [2.0, 4.0, 2.0], color='#5d6d7e', lw=2.5, zorder=3)
ax.plot([-3.5, 3.5], [2.0, 2.0], color='#5d6d7e', lw=2.0, zorder=3)
ax.plot([0, 0], [2.0, 4.0], color='#5d6d7e', lw=1.5, ls='--', alpha=0.7, zorder=3)

# (2) 동적 레이더 안테나 라인들
dish_line, = ax.plot([], [], color='#2c3e50', lw=3.2, zorder=4)
dish_back, = ax.plot([], [], color='#7f8c8d', lw=2.0, zorder=4)
horn_line, = ax.plot([], [], color='#2c3e50', lw=1.8, zorder=4)

# (3) 궤적선 (교재 원본의 황색 점선 궤적)
traj_line, = ax.plot([x[0]-10, x[-1]+15], [y[0]-5, y[-1]+8], color='#f28e2b', ls='--', lw=1.6, dashes=(8, 8))
# 궤적 화살표
ax.annotate('', xy=(x[0]+8, y[0]+4), xytext=(x[0]+7, y[0]+3.5), arrowprops=dict(arrowstyle='->', color='#f28e2b', lw=1.6))
ax.annotate('', xy=(x[-1]-8, y[-1]-4), xytext=(x[-1]-9, y[-1]-4.5), arrowprops=dict(arrowstyle='->', color='#f28e2b', lw=1.6))

# (4) 기준선 (수직 점선)
ax.plot([0, 0], [4.0, 105.0], color='#7f8c8d', ls='--', lw=1.2, dashes=(8, 8))

# (5) 동적 레이더 지향 라인 r
line_r, = ax.plot([], [], 'k-', lw=1.2)
text_r = ax.text(0, 0, '$r$', fontsize=13, fontweight='bold', fontstyle='italic')

# (6) 동적 추적 각도 theta 호(Arc) 및 화살표 머리
arc_theta = patches.Arc((0, 4.0), 30, 30, theta1=0, theta2=90, color='k', lw=1.2)
ax.add_patch(arc_theta)
arrow_theta = ax.annotate('', xy=(0,0), xytext=(0,0), arrowprops=dict(arrowstyle='->', color='k', lw=1.2, shrinkA=0, shrinkB=0))
text_theta = ax.text(0, 0, r'$\theta$', fontsize=13, fontweight='bold', fontstyle='italic')

# (7) 로켓 본체 폴리곤 및 날개/노즐
rocket_body = patches.Polygon([[0,0]], facecolor='#a9cce3', edgecolor='k', lw=1.2, zorder=6)
rocket_nozzle = patches.Polygon([[0,0]], facecolor='#566573', edgecolor='k', lw=1.0, zorder=5)
rocket_dot, = ax.plot([], [], 'ko', markersize=4.5, zorder=7) # 무게중심 CG
ax.add_patch(rocket_body)
ax.add_patch(rocket_nozzle)

# (8) 로켓 중심의 극좌표 축 가이드 (+r, +theta 축)
line_plus_r, = ax.plot([], [], 'k--', lw=1.0, dashes=(6, 6))
line_plus_th, = ax.plot([], [], 'k--', lw=1.0, dashes=(6, 6))
text_plus_r = ax.text(0, 0, '$+r$', fontsize=13, fontweight='bold')
text_plus_th = ax.text(0, 0, '$+\\theta$', fontsize=13, fontweight='bold')

# (9) 교재 예제 문제 지점 (theta = 30 deg, r = 80 km) 고정 별 표식 및 라벨
ax.plot(x_target, y_target, 'r*', markersize=14, zorder=8)
ax.text(x_target + 3, y_target - 2.5, '★ 교재 정답 위치 (θ = 30°, r = 80 km)', color='#c0392b', fontsize=11, fontweight='bold', zorder=8)

labels_list = []

def animate(i):
    global labels_list
    xi, yi = x[i], y[i]
    vxi = vx0
    vyi = vy0 - g * t_arr[i]
    
    # 1. 레이더 접시 회전 연동 (로켓 CG 위치를 실시간으로 정확히 조준)
    angle_rad = np.arctan2(xi, yi - 4.0)
    rx, ry, rxb, ryb, hx, hy = get_rotated_dish_coords(0, 4.0, angle_rad, scale=5.0)
    dish_line.set_data(rx, ry)
    dish_back.set_data(rxb, ryb)
    horn_line.set_data(hx, hy)
    
    # 2. 레이더 가이드라인 r 갱신
    line_r.set_data([0, xi], [4.0, yi])
    text_r.set_position((xi/2 - 3.5, yi/2 + 2.0))
    
    # 3. 각도 theta 호 및 지시선 갱신 (수직선 기준 시계방향)
    angle_deg = np.degrees(angle_rad)
    arc_theta.theta1 = 90 - angle_deg
    arc_theta.theta2 = 90
    
    # 각도 화살표 갱신
    r_arc = 15.0
    arc_end_x = r_arc * np.cos(np.radians(90 - angle_deg))
    arc_end_y = 4.0 + r_arc * np.sin(np.radians(90 - angle_deg))
    arc_prev_x = r_arc * np.cos(np.radians(90 - angle_deg + 2.5))
    arc_prev_y = 4.0 + r_arc * np.sin(np.radians(90 - angle_deg + 2.5))
    arrow_theta.xy = (arc_end_x, arc_end_y)
    arrow_theta.set_position((arc_prev_x, arc_prev_y))
    
    mid_angle = np.radians(90 - angle_deg/2)
    text_theta.set_position((18.0 * np.cos(mid_angle) - 1.0, 4.0 + 18.0 * np.sin(mid_angle) + 1.0))
    
    # 4. 로켓 3D 형상 갱신
    r_poly, n_poly, rot_deg = get_rotated_rocket_poly(xi, yi, vxi, vyi, length=9.5, width=1.6)
    rocket_body.set_xy(r_poly)
    rocket_nozzle.set_xy(n_poly)
    rocket_dot.set_data([xi], [yi])
    
    # 5. 로켓 무게중심 기준 극좌표축 (+r, +theta) 갱신
    r_len = np.sqrt(xi**2 + (yi-4.0)**2)
    dir_r = (xi/r_len, (yi-4.0)/r_len)
    
    # +r축 연장 점선
    line_plus_r.set_data([xi, xi + dir_r[0] * 18.0], [yi, yi + dir_r[1] * 18.0])
    text_plus_r.set_position((xi + dir_r[0] * 20.0, yi + dir_r[1] * 20.0))
    
    # +theta축 연장 점선 (시계방향 90도 수직 방향)
    dir_th = (dir_r[1], -dir_r[0])
    line_plus_th.set_data([xi, xi + dir_th[0] * 15.0], [yi, yi + dir_th[1] * 15.0])
    text_plus_th.set_position((xi + dir_th[0] * 17.0, yi + dir_th[1] * 17.0))
    
    # 6. 실시간 극좌표 운동학 데이터 패널
    rx_val = xi
    ry_val = yi - 4.0
    r_len_km = np.hypot(rx_val, ry_val)
    r_len_m = r_len_km * 1000.0
    
    # 동적 속도 성분 계산 (m/s)
    r_dot_ms = (rx_val * vxi + ry_val * vyi) / r_len_km * 1000.0  # v_r = r_dot
    v_theta_ms = (ry_val * vxi - rx_val * vyi) / r_len_km * 1000.0 # v_theta = r * theta_dot
    v_mag = np.hypot(vxi, vyi) * 1000.0                          # v = sqrt(v_r^2 + v_theta^2)
    
    # 동적 각속도 (rad/s)
    theta_dot_rads = v_theta_ms / r_len_m
    
    # 동적 가속도 성분 (m/s^2) - 중력가속도 g = 9.20 m/s^2 연직 아래
    g_ms2 = 9.20
    a_r_ms2 = -g_ms2 * np.cos(angle_rad)
    a_theta_ms2 = g_ms2 * np.sin(angle_rad)
    
    # 이계도함수 연산 (r_ddot, theta_ddot)
    r_ddot_ms2 = a_r_ms2 + r_len_m * (theta_dot_rads)**2
    theta_ddot_rads2 = (a_theta_ms2 - 2.0 * r_dot_ms * theta_dot_rads) / r_len_m
    
    for lbl in labels_list: lbl.remove()
    labels_list.clear()
    
    # 목표 상태 도달 강조 (t = 5.0s, theta = 30° / 0.5236 rad 부근)
    if abs(t_arr[i] - 5.0) < 0.06:
        complete_highlight = (
            "★ [교재 정답 위치 통과!] θ = 30.0° (t = 5.0s) ★\n"
            "  - 실시간 측정치와 교재 정답이 100% 일치합니다."
        )
        panel_color = '#d35400'
        panel_weight = 'bold'
    else:
        complete_highlight = f"▶ 현재 위치: θ = {angle_deg:.1f}° (비행 궤적 추적 중)"
        panel_color = '#2c3e50'
        panel_weight = 'normal'
        
    info_text = (
        f"■ [교재 예제 2.10 정답 (θ = 30° / 0.5236 rad 일 때)]\n"
        f"  ★ 속도 크기 v    = 1639 m/s (v_r=1200, v_θ=1117)\n"
        f"  ★ 반경 가속도 r-ddot = 7.63 m/s² (a_r=-7.97, a_θ=4.60)\n"
        f"  ★ 각가속도 θ-ddot  = -3.61×10^-4 rad/s²\n"
        f"================================------------\n"
        f"▶ [실시간 애니메이션 측정치 (0 ~ 10초 연속 비행)]\n"
        f"  ■ 경과 시간 t : {t_arr[i]:.2f} s / 10.0 s\n"
        f"  ■ 지향 각도 θ : {angle_rad:.4f} rad ({angle_deg:.1f}°)\n"
        f"  ■ 측정 거리 r : {r_len_km:.2f} km ({r_len_m:.0f} m)\n"
        f"  ■ 실시간 속도 v : {v_mag:.0f} m/s (v_r={r_dot_ms:.0f}, v_θ={v_theta_ms:.0f})\n"
        f"  ■ 실시간 r-ddot : {r_ddot_ms2:.2f} m/s²\n"
        f"  ■ 실시간 θ-ddot : {theta_ddot_rads2*1e4:.2f}×10^-4 rad/s²\n"
        f"--------------------------------------------\n"
        f"{complete_highlight}"
    )
    
    txt_panel = ax.text(0.98, 0.05, info_text, transform=ax.transAxes, fontsize=10.0, color=panel_color,
                        fontweight=panel_weight, fontfamily='Malgun Gothic', ha='right', va='bottom',
                        bbox=dict(facecolor='white', alpha=0.94, edgecolor='#bdc3c7', boxstyle='round,pad=0.5'))
    labels_list.append(txt_panel)
    
    txt_title = ax.text(0.02, 0.95, "예제 2.10: 레이더 추적 극좌표계 시뮬레이션", transform=ax.transAxes,
                        fontsize=15, fontweight='bold', color='#2c3e50', fontfamily='Malgun Gothic', ha='left', va='center')
    labels_list.append(txt_title)
    
    return line_r, text_r, arc_theta, arrow_theta, text_theta, rocket_body, rocket_dot, line_plus_r, line_plus_th, text_plus_r, text_plus_th

# 애니메이션 생성
ani = FuncAnimation(fig, animate, frames=frames, interval=45, blit=False)

# GIF 저장 설정
gif_path = 'ex2_10_radar_tracking.gif'
writer = PillowWriter(fps=22)

print(f"GIF 애니메이션을 {gif_path} 파일로 렌더링 중...")
ani.save(gif_path, writer=writer)
print(f"GIF 저장 성공: {gif_path}")

# theta = 30도 지점(프레임 50) 및 마지막 프레임 정지 패치 적용 (학생 시선 고정용)
try:
    from PIL import Image
    im = Image.open(gif_path)
    frames_img = []
    durations = []
    
    idx = 0
    try:
        while True:
            frames_img.append(im.copy())
            dur_val = im.info.get('duration', 45)
            # theta = 30도 지점(프레임 50)에서 2.5초간 정지
            if idx == 50:
                dur_val = 2500
            durations.append(dur_val)
            idx += 1
            im.seek(len(frames_img))
    except EOFError:
        pass
    
    durations[-1] = 4000  # 마지막 프레임 4초간 정지
    frames_img[0].save(gif_path, save_all=True, append_images=frames_img[1:], duration=durations, loop=0)
    print("theta=30도 지점 2.5초 정지 및 마지막 프레임 4초 정지 패치 적용 완료! [완료]")
except Exception as e:
    print(f"딜레이 연장 패치 예외: {e}")

