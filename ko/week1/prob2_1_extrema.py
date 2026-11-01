# 연습문제 2/1: 속도 극값 및 가속도 관찰
# v = 20t^2 - 100t + 50

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 5, 200)
v = 20 * t**2 - 100 * t + 50
a = 40 * t - 100

fig, axs = plt.subplots(2, 1, figsize=(8, 8))
fig.suptitle('Problem 2/1: Velocity and Acceleration', fontsize=16)

y_data = [v, a]
colors = ['g', 'r']
titles = ['Velocity (v-t)', 'Acceleration (a-t)']
lines = []
points = []

for i in range(2):
    axs[i].set_xlim(0, 5)
    axs[i].set_ylim(np.min(y_data[i]) - 20, np.max(y_data[i]) + 20)
    axs[i].set_title(titles[i])
    axs[i].grid(True)
    axs[i].axhline(0, color='black', lw=1, ls='--')  # y=0 라인
    line, = axs[i].plot([], [], lw=2, color=colors[i])
    point, = axs[i].plot([], [], 'o', color=colors[i], markersize=8)
    lines.append(line)
    points.append(point)

def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        point.set_data([], [])
    return lines + points

def animate(i):
    for j in range(2):
        lines[j].set_data(t[:i], y_data[j][:i])
        points[j].set_data([t[i]], [y_data[j][i]])
    return lines + points

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()
