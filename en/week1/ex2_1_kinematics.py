# Example 2.1: Motion simulation given position function s(t)
# s(t) = 2*t^3 - 24*t + 6

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

# 시간 배열 설정 (0 ~ 5초)
t = np.linspace(0, 5, 200)

# 운동 방정식
s = 2 * t**3 - 24 * t + 6
v = 6 * t**2 - 24
a = 12 * t

fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig.suptitle('Example 2.1: s(t) = 2t³ - 24t + 6', fontsize=16)

titles = ['Position (s-t)', 'Velocity (v-t)', 'Acceleration (a-t)']
y_data = [s, v, a]
colors = ['b', 'g', 'r']
lines = []
points = []

for i in range(3):
    axs[i].set_xlim(0, 5)
    axs[i].set_ylim(np.min(y_data[i]) - 10, np.max(y_data[i]) + 10)
    axs[i].set_title(titles[i])
    axs[i].grid(True)
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
    for j in range(3):
        lines[j].set_data(t[:i], y_data[j][:i])
        points[j].set_data([t[i]], [y_data[j][i]])
    return lines + points

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()
