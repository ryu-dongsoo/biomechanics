# 예제 2.6: 울타리를 넘는 포물체 운동
# 교재 그림 완벽 재현

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

v0 = 24
theta = np.radians(35)
g = 9.81
y0 = 2

v_x0 = v0 * np.cos(theta)
v_y0 = v0 * np.sin(theta)

# 충돌 지점 계산 (지면 y=6 에 도달하는 시간 및 x좌표)
a_coeff = g / (2 * v_x0**2)
b_coeff = np.tan(theta)
c_coeff = 6 - y0
x_impact = (b_coeff + np.sqrt(b_coeff**2 - 4 * a_coeff * c_coeff)) / (2 * a_coeff)
t_impact = x_impact / v_x0

t = np.linspace(0, t_impact, 120)
x = v_x0 * t
y = y0 + v_y0 * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_xlim(-5, 55)
ax.set_ylim(-4, 15)
ax.axis('off') # 기본 축 숨기기

# 1. 지형 그리기 (그라데이션 느낌의 단색 + 테두리)
x_ground = [-5, 0, 30, 40, 55]
y_ground = [0, 0, 0, 6, 6]
ax.fill_between(x_ground, y_ground, -4, color='#a8caba', alpha=0.6) # 옅은 녹청색
ax.plot(x_ground, y_ground, color='#6b6b6b', lw=1.5)

# 2. 기준선 및 좌표축 그리기
# y축 (점선)
ax.plot([0, 0], [0, 12], 'k--', lw=1.5)
ax.text(0, 12.5, '$y$', ha='center', fontsize=12)

# 발사대 위치
ax.plot([0], [2], 'ro', markersize=4) # 발사점
ax.plot([-3, 0], [2, 2], 'k-', lw=1)
ax.annotate('', xy=(-3, 2), xytext=(-3, 0), arrowprops=dict(arrowstyle='<->', lw=0.8))
ax.text(-3.5, 1, '2 m', ha='right', va='center', fontsize=11)

# 3. 울타리
ax.plot([40, 40], [6, 8.4], color='k', lw=2)
ax.text(38, 9.5, '울타리', ha='right', va='bottom', fontsize=11)
ax.annotate('', xy=(40, 8.4), xytext=(36, 10), arrowprops=dict(arrowstyle='->', lw=0.8, connectionstyle="arc3,rad=.2"))

# 4. 치수선
# 하단 30m, 10m
ax.plot([0, 0], [0, -1.5], 'k-', lw=0.8)
ax.plot([30, 30], [0, -1.5], 'k-', lw=0.8)
ax.plot([40, 40], [0, -1.5], 'k-', lw=0.8)

ax.annotate('', xy=(30, -1), xytext=(0, -1), arrowprops=dict(arrowstyle='<->', lw=0.8))
ax.text(15, -1.5, '30 m', ha='center', va='top', fontsize=11)

ax.annotate('', xy=(40, -1), xytext=(30, -1), arrowprops=dict(arrowstyle='<->', lw=0.8))
ax.text(35, -1.5, '10 m', ha='center', va='top', fontsize=11)

# 우측 6m, 2.4m 치수선
ax.plot([40, 50], [6, 6], 'k-', lw=0.8)
ax.plot([40, 50], [8.4, 8.4], 'k-', lw=0.8)
ax.plot([30, 50], [0, 0], 'k-', lw=0.8) # 연장선

ax.annotate('', xy=(48, 6), xytext=(48, 0), arrowprops=dict(arrowstyle='<->', lw=0.8))
ax.text(49, 3, '6 m', ha='left', va='center', fontsize=11)

ax.annotate('', xy=(48, 8.4), xytext=(48, 6), arrowprops=dict(arrowstyle='<->', lw=0.8))
ax.text(49, 7.2, '2.4 m', ha='left', va='center', fontsize=11)

# x축 표시 (오른쪽 하단)
ax.annotate('', xy=(53, 0), xytext=(50, 0), arrowprops=dict(arrowstyle='<-', lw=0.8))
ax.text(54, 0, '$-x$', ha='left', va='center', fontsize=12) # 교재에 -x 라고 쓰여있음

# 5. 발사 벡터 (초기 각도 표시)
vx_arrow = 8 * np.cos(theta)
vy_arrow = 8 * np.sin(theta)
ax.annotate('', xy=(vx_arrow, y0 + vy_arrow), xytext=(0, y0), arrowprops=dict(arrowstyle='->', color='#2ca02c', lw=2))
ax.text(10, 10, '$v_0 = 24 \mathrm{m/s}$', fontsize=12)
ax.text(5, 3.5, r'$\theta = 35^\circ$', fontsize=11)
ax.plot([0, 5], [2, 2], 'k-', lw=0.8)

# 6. 애니메이션 객체
line_traj, = ax.plot([], [], color='#ff7f0e', ls='--', lw=2) # 주황색 점선
point, = ax.plot([], [], 'o', color='#ff7f0e', markersize=5) # 주황색 점

def animate(i):
    line_traj.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    return line_traj, point

ani = FuncAnimation(fig, animate, frames=len(t), interval=30, blit=False)

writer = PillowWriter(fps=30)
writer._kwargs = {'loop': None}
gif_path = 'ex2_6_projectile.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")
