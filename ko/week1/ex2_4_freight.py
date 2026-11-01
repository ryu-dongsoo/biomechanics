# 예제 2.4: 화물선의 엔진 정지 후 감속 운동
# 교재 그림의 역학적 시뮬레이션 및 그래프 (v-t, s-t) 시각화

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시간 배열 설정 (0 ~ 10분, t 단위: 분)
frames = 120
t = np.linspace(0, 10, frames)

# 운동학 함수
v = 80 / (t + 10)
s = (4 / 3) * np.log((t + 10) / 10)

fig = plt.figure(figsize=(10, 8))
fig.suptitle('예제 2.4: 화물선의 감속 운동 ($a \propto -v^2$)', fontsize=16, fontweight='bold')
gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1])

# --- 상단: 기계적 시뮬레이션 (바다와 화물선) ---
ax_mech = fig.add_subplot(gs[0, :])
ax_mech.set_xlim(-0.2, 1.2)
ax_mech.set_ylim(-0.3, 0.5)
ax_mech.axis('off')

# 바다 (Water)
ax_mech.axhline(0, color='#2980b9', lw=3)
ax_mech.fill_between([-0.5, 1.5], [-0.5, -0.5], [0, 0], color='#ebf5fb')

# 기준선 (s=0)
ax_mech.plot([0, 0], [0, 0.4], 'k-.', lw=1, alpha=0.5)

# 화물선 폴리곤 정의
hull_verts = np.array([[-0.1, 0], [0.08, 0], [0.1, 0.05], [-0.1, 0.05]])
hull = patches.Polygon(hull_verts, facecolor='#2c3e50', edgecolor='black', lw=1.5)
cabin_verts = np.array([[-0.05, 0.05], [0.03, 0.05], [0.03, 0.1], [-0.05, 0.1]])
cabin = patches.Polygon(cabin_verts, facecolor='#ecf0f1', edgecolor='black', lw=1.5)
stack_verts = np.array([[-0.03, 0.1], [-0.01, 0.1], [-0.01, 0.15], [-0.03, 0.15]])
stack = patches.Polygon(stack_verts, facecolor='#c0392b', edgecolor='black', lw=1.5)

ax_mech.add_patch(hull)
ax_mech.add_patch(cabin)
ax_mech.add_patch(stack)

# 치수선 및 연장선
ship_ext_line, = ax_mech.plot([], [], 'k-.', lw=1, alpha=0.5)
dim_s_line, = ax_mech.plot([], [], 'k-', lw=1.5)
dim_s_arrow_L, = ax_mech.plot([], [], 'k-', lw=1.5)
dim_s_arrow_R, = ax_mech.plot([], [], 'k-', lw=1.5)
dim_s_text = ax_mech.text(0, 0.37, '$s$', fontsize=14, ha='center', va='bottom')

# 속도 벡터
v_quiver = None

# 정보 텍스트
info_text = ax_mech.text(-0.15, 0.45, '', fontsize=12, va='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))

# --- 하단 좌측: v-t 그래프 ---
ax_v = fig.add_subplot(gs[1, 0])
ax_v.set_xlim(0, 10)
ax_v.set_ylim(0, 8.5)
ax_v.grid(True, linestyle='--', alpha=0.7)
ax_v.set_xlabel('시간 $t$ (min)')
ax_v.set_ylabel('속력 $v$ (knots)')
ax_v.set_title('속력 - 시간 그래프')
line_v, = ax_v.plot(t, v, color='#27ae60', lw=2.5)
time_marker_v, = ax_v.plot([0, 0], ax_v.get_ylim(), 'k--', lw=1)
point_v, = ax_v.plot([], [], 'o', color='#27ae60', markersize=6)

# --- 하단 우측: s-t 그래프 ---
ax_s = fig.add_subplot(gs[1, 1])
ax_s.set_xlim(0, 10)
ax_s.set_ylim(0, 1.0)
ax_s.grid(True, linestyle='--', alpha=0.7)
ax_s.set_xlabel('시간 $t$ (min)')
ax_s.set_ylabel('거리 $s$ (nmi)')
ax_s.set_title('이동거리 - 시간 그래프')
line_s, = ax_s.plot(t, s, color='#2980b9', lw=2.5)
time_marker_s, = ax_s.plot([0, 0], ax_s.get_ylim(), 'k--', lw=1)
point_s, = ax_s.plot([], [], 'o', color='#2980b9', markersize=6)

plt.tight_layout()

def animate(i):
    global v_quiver
    current_t = t[i]
    current_s = s[i]
    current_v = v[i]
    
    # 1. 화물선 갱신
    hull.set_xy(hull_verts + [current_s, 0])
    cabin.set_xy(cabin_verts + [current_s, 0])
    stack.set_xy(stack_verts + [current_s, 0])
    
    # 2. 치수선 갱신
    ship_ext_line.set_data([current_s, current_s], [0, 0.4])
    y_dim = 0.35
    dim_s_line.set_data([0, current_s], [y_dim, y_dim])
    
    arrow_len = 0.02
    if current_s > 0.01:
        dim_s_arrow_L.set_data([arrow_len, 0, arrow_len], [y_dim+0.01, y_dim, y_dim-0.01])
        dim_s_arrow_R.set_data([current_s - arrow_len, current_s, current_s - arrow_len], [y_dim+0.01, y_dim, y_dim-0.01])
        dim_s_text.set_position((current_s/2, y_dim + 0.01))
        dim_s_text.set_text('$s$')
    else:
        dim_s_arrow_L.set_data([], [])
        dim_s_arrow_R.set_data([], [])
        dim_s_text.set_text('')
        
    # 3. 속도 벡터 갱신
    if v_quiver is not None:
        v_quiver.remove()
    v_scale = 0.02
    v_quiver = ax_mech.quiver(current_s + 0.1, 0.025, current_v * v_scale, 0, 
                              color='#27ae60', angles='xy', scale_units='xy', scale=1, width=0.005)
                              
    info_text.set_text(f"시간 $t = {current_t:.1f}$ min\n거리 $s = {current_s:.3f}$ nmi\n속력 $v = {current_v:.2f}$ knots")
    
    # 4. 그래프 마커 갱신
    time_marker_v.set_data([current_t, current_t], ax_v.get_ylim())
    point_v.set_data([current_t], [current_v])
    
    time_marker_s.set_data([current_t, current_t], ax_s.get_ylim())
    point_s.set_data([current_t], [current_s])
    
    return hull, cabin, stack, ship_ext_line, dim_s_line, dim_s_arrow_L, dim_s_arrow_R, dim_s_text, info_text, time_marker_v, point_v, time_marker_s, point_s

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)

writer = PillowWriter(fps=25)
writer._kwargs = {'loop': None}
gif_path = 'ex2_4_freight.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")

# 딜레이 추가
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
