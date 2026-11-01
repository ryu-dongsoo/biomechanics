# 예제 2.1: 위치 함수 s(t)가 주어졌을 때의 운동 시뮬레이션
# 교재 예제 2.1 그림 완벽 재현

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시간 배열 설정 (0 ~ 4초)
t = np.linspace(0, 4, 160)

# 운동 방정식
s = 2 * t**3 - 24 * t + 6
v = 6 * t**2 - 24
a = 12 * t

fig, axs = plt.subplots(3, 1, figsize=(6, 11))

# 공통 축 스타일 적용
for ax in axs:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    # 화살표 표시
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

ax1, ax2, ax3 = axs

# --- s-t Graph ---
line_s, = ax1.plot([], [], color='#d62728', lw=2)
ax1.set_xlim(0, 4.5)
ax1.set_ylim(-30, 45)
ax1.set_xticks([0, 1, 2, 3, 4])
ax1.set_yticks([-26, 6, 38])
ax1.text(4.6, 0, '$t, \mathrm{s}$', va='center')
ax1.text(0, 48, '$s, \mathrm{m}$', ha='center')

# --- v-t Graph ---
line_v, = ax2.plot([], [], color='#d62728', lw=2)
ax2.set_xlim(0, 4.5)
ax2.set_ylim(-30, 80)
ax2.set_xticks([0, 1, 2, 3, 4])
ax2.set_yticks([-24, 30, 72])
ax2.text(4.6, 0, '$t, \mathrm{s}$', va='center')
ax2.text(0, 85, '$v, \mathrm{m/s}$', ha='center')

# --- a-t Graph ---
line_a, = ax3.plot([], [], color='#d62728', lw=2)
ax3.set_xlim(0, 4.5)
ax3.set_ylim(0, 55)
ax3.set_xticks([0, 1, 2, 3, 4])
ax3.set_yticks([36, 48])
ax3.text(4.6, 0, '$t, \mathrm{s}$', va='center')
ax3.text(0, 58, '$a, \mathrm{m/s^2}$', ha='center')

plt.tight_layout()

fill1 = None
fill2 = None

def animate(i):
    global fill1, fill2
    
    t_curr = t[:i]
    s_curr = s[:i]
    v_curr = v[:i]
    a_curr = a[:i]
    
    line_s.set_data(t_curr, s_curr)
    line_v.set_data(t_curr, v_curr)
    line_a.set_data(t_curr, a_curr)
    
    # 시간 진행에 따라 점선 표시
    if t[i] >= 2 and not hasattr(ax1, 'line_added_2s'):
        ax1.plot([2, 2], [0, -26], 'k--', alpha=0.5)
        ax1.plot([0, 2], [-26, -26], 'k--', alpha=0.5)
        ax1.line_added_2s = True
        
    if t[i] >= 3 and not hasattr(ax2, 'line_added_3s'):
        ax2.plot([3, 3], [0, 30], 'k--', alpha=0.5)
        ax2.plot([0, 3], [30, 30], 'k--', alpha=0.5)
        ax3.plot([3, 3], [0, 36], 'k--', alpha=0.5)
        ax3.plot([0, 3], [36, 36], 'k--', alpha=0.5)
        ax2.line_added_3s = True

    if t[i] >= 4 and not hasattr(ax2, 'line_added_4s'):
        ax2.plot([4, 4], [0, 72], 'k-', alpha=0.5)
        ax2.line_added_4s = True
        
    if t[i] >= 1 and not hasattr(ax2, 'line_added_1s'):
        ax2.plot([1, 1], [0, -18], 'k-', alpha=0.5)
        ax2.line_added_1s = True

    # 면적 채우기 (fill_between) 애니메이션
    if fill1 is not None:
        fill1.remove()
    if fill2 is not None:
        fill2.remove()
        
    t1 = t_curr[(t_curr >= 1) & (t_curr <= 2)]
    v1 = v_curr[(t_curr >= 1) & (t_curr <= 2)]
    if len(t1) > 0:
        fill1 = ax2.fill_between(t1, 0, v1, color='#f4a59d', alpha=0.8)
    else:
        fill1 = None
        
    t2 = t_curr[(t_curr >= 2) & (t_curr <= 4)]
    v2 = v_curr[(t_curr >= 2) & (t_curr <= 4)]
    if len(t2) > 0:
        fill2 = ax2.fill_between(t2, 0, v2, color='#f4a59d', alpha=0.8)
    else:
        fill2 = None

    # 면적 수식 텍스트
    if t[i] >= 1.5 and not hasattr(ax2, 'text1_added'):
        ax2.annotate('$\Delta s_{1-2}$', xy=(1.5, -9), xytext=(2, -18),
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
                     fontsize=12)
        ax2.text1_added = True
        
    if t[i] >= 3.0 and not hasattr(ax2, 'text2_added'):
        ax2.text(3, 15, '$\Delta s_{2-4}$', ha='center', va='center', fontsize=12)
        ax2.text2_added = True

    return line_s, line_v, line_a

# blit=False 로 두어야 fill_between 갱신이 정상적으로 처리됨
ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=False)

from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=50)
writer._kwargs = {'loop': None} # 1회 재생 후 완전 멈춤 (루프 속성 제거)

gif_path = 'ex2_1_kinematics.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 1회 재생 설정으로 저장되었습니다.")
