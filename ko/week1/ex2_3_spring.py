# 예제 2.3: 가속도가 위치의 함수일 때 (a = -k^2 * s)
# 조화 진동 모델 및 기계적 도식화 시각화 (교재 그림 재현)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 초기 조건 및 파라미터
v0 = 10
k_const = 2 # 가속도 상수 (a = -k^2 * s)
t_total = 2 * np.pi / k_const # 주기 T (약 3.14초)
frames = 120
t = np.linspace(0, t_total * 2, frames) # 2주기 동안의 애니메이션

# 운동학 방정식
s = (v0 / k_const) * np.sin(k_const * t)
v = v0 * np.cos(k_const * t)
a = -k_const**2 * s

fig = plt.figure(figsize=(10, 8))
fig.suptitle('예제 2.3: 양방향 스프링 슬라이더 진동 ($a = -k^2 s$)', fontsize=16, fontweight='bold')
gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 1])

# --- 상단: 기계적 시뮬레이션 ---
ax_mech = fig.add_subplot(gs[0])
ax_mech.set_xlim(-10, 10)
ax_mech.set_ylim(-3, 3)
ax_mech.axis('off')

# 가이드 트랙 (상하 벽)
ax_mech.plot([-9, 9], [1.3, 1.3], 'k-', lw=4)
ax_mech.plot([-9, 9], [-1.3, -1.3], 'k-', lw=4)

# 양쪽 고정 벽 (스프링 부착점)
ax_mech.plot([-9, -9], [-1.3, 1.3], 'k-', lw=8)
ax_mech.plot([9, 9], [-1.3, 1.3], 'k-', lw=8)

# 중앙 기준선 (s=0)
ax_mech.plot([0, 0], [-1.5, 2.8], 'k-.', lw=1, alpha=0.5)

# 슬라이더 (블록)
block_width = 3
block_height = 2
block = patches.Rectangle((-1.5, -1), block_width, block_height, facecolor='#a9cce3', edgecolor='black', lw=2)
ax_mech.add_patch(block)

# 바퀴 4개
wheel_r = 0.2
w1 = patches.Circle((-1, 1.1), wheel_r, facecolor='#d4e6f1', edgecolor='black')
w2 = patches.Circle((1, 1.1), wheel_r, facecolor='#d4e6f1', edgecolor='black')
w3 = patches.Circle((-1, -1.1), wheel_r, facecolor='#d4e6f1', edgecolor='black')
w4 = patches.Circle((1, -1.1), wheel_r, facecolor='#d4e6f1', edgecolor='black')
for w in [w1, w2, w3, w4]:
    ax_mech.add_patch(w)
    
# 중심점 마커
center_dot, = ax_mech.plot([0], [0], 'ko', markersize=6)

# 스프링 라인 초기화
spring_L, = ax_mech.plot([], [], 'k-', lw=1.5)
spring_R, = ax_mech.plot([], [], 'k-', lw=1.5)

# 치수선 (s) 및 연장선
slider_ext_line, = ax_mech.plot([], [], 'k-.', lw=1, alpha=0.5)
dim_s_line, = ax_mech.plot([], [], 'k-', lw=1)
dim_s_arrow_L, = ax_mech.plot([], [], 'k-', lw=1)
dim_s_arrow_R, = ax_mech.plot([], [], 'k-', lw=1)
dim_s_text = ax_mech.text(0, 2.2, '$s$', fontsize=14, ha='center', va='bottom')

# 정보 텍스트 패널
info_text = ax_mech.text(-9.5, 2.8, '', fontsize=12, va='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))

def generate_spring(x_start, x_end, y=0, num_coils=12, width=0.6):
    """지그재그 형태의 스프링 좌표 생성"""
    straight_len = 0.5
    coil_start = x_start + straight_len
    coil_end = x_end - straight_len
    if coil_end <= coil_start:
        coil_end = coil_start + 0.1
        
    x = [x_start, coil_start]
    y_vals = [y, y]
    
    coil_len = (coil_end - coil_start) / (2 * num_coils)
    for i in range(num_coils):
        x.append(coil_start + coil_len * (2*i + 0.5))
        y_vals.append(y + width/2)
        x.append(coil_start + coil_len * (2*i + 1.5))
        y_vals.append(y - width/2)
        
    x.append(coil_end)
    y_vals.append(y)
    x.append(x_end)
    y_vals.append(y)
    return x, y_vals

# --- 하단: 역학(Kinematics) 그래프 ---
ax_graph = fig.add_subplot(gs[1])
ax_graph.set_xlim(0, t_total * 2)
ax_graph.set_ylim(-np.max(a)*1.1, np.max(a)*1.1)
ax_graph.grid(True, linestyle='--', alpha=0.7)
ax_graph.set_xlabel('시간 $t$ (s)')
ax_graph.set_ylabel('위치, 속도, 가속도')

line_s, = ax_graph.plot(t, s, 'b-', lw=2, label='위치 $s$')
line_v, = ax_graph.plot(t, v, 'g-', lw=2, label='속도 $v$')
line_a, = ax_graph.plot(t, a, 'r-', lw=2, label='가속도 $a$')
ax_graph.legend(loc='upper right')

# 타임라인 및 현재 값 마커
time_marker, = ax_graph.plot([0, 0], ax_graph.get_ylim(), 'k--', lw=1)
point_s, = ax_graph.plot([], [], 'bo', markersize=6)
point_v, = ax_graph.plot([], [], 'go', markersize=6)
point_a, = ax_graph.plot([], [], 'ro', markersize=6)

def animate(i):
    current_s = s[i]
    current_t = t[i]
    
    # 1. 기계적 요소 업데이트
    block.set_x(current_s - block_width/2)
    w1.center = (current_s - 1, 1.1)
    w2.center = (current_s + 1, 1.1)
    w3.center = (current_s - 1, -1.1)
    w4.center = (current_s + 1, -1.1)
    center_dot.set_data([current_s], [0])
    
    # 스프링 신축 업데이트
    sxL, syL = generate_spring(-9, current_s - 1.5)
    spring_L.set_data(sxL, syL)
    sxR, syR = generate_spring(current_s + 1.5, 9)
    spring_R.set_data(sxR, syR)
    
    # 치수선(s) 및 연장선 업데이트
    slider_ext_line.set_data([current_s, current_s], [0, 2.5])
    
    y_dim = 2.0
    dim_s_line.set_data([0, current_s], [y_dim, y_dim])
    
    arrow_len = 0.25
    if abs(current_s) > 0.1:
        sign = np.sign(current_s)
        dim_s_arrow_L.set_data([sign*arrow_len, 0, sign*arrow_len], [y_dim+0.1, y_dim, y_dim-0.1])
        dim_s_arrow_R.set_data([current_s - sign*arrow_len, current_s, current_s - sign*arrow_len], [y_dim+0.1, y_dim, y_dim-0.1])
        dim_s_text.set_position((current_s/2, y_dim + 0.1))
        dim_s_text.set_text('$s$')
    else:
        dim_s_arrow_L.set_data([], [])
        dim_s_arrow_R.set_data([], [])
        dim_s_text.set_text('')
        
    info_text.set_text(f"시간 $t = {current_t:.2f}$ s\n위치 $s = {current_s:.2f}$ m\n속도 $v = {v[i]:.2f}$ m/s\n가속도 $a = {a[i]:.2f}$ m/s²")
    
    # 2. 그래프 마커 업데이트
    time_marker.set_data([current_t, current_t], ax_graph.get_ylim())
    point_s.set_data([current_t], [current_s])
    point_v.set_data([current_t], [v[i]])
    point_a.set_data([current_t], [a[i]])
    
    return (block, w1, w2, w3, w4, center_dot, spring_L, spring_R, 
            slider_ext_line, dim_s_line, dim_s_arrow_L, dim_s_arrow_R, dim_s_text, info_text, 
            time_marker, point_s, point_v, point_a)

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=True)

writer = PillowWriter(fps=25)
writer._kwargs = {'loop': None}
gif_path = 'ex2_3_spring.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")

# 딜레이 추가 로직
try:
    from PIL import Image
    im = Image.open(gif_path)
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 40))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(gif_path, save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("딜레이 연장 성공")
except Exception as e:
    print("딜레이 연장 실패:", e)
