# Example 2.3: Acceleration as a function of position (a = -k^2 * s)
# 조화 진동 모델

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

v0 = 10
k = 2
t = np.linspace(0, 5, 200)

s = (v0 / k) * np.sin(k * t)
v = v0 * np.cos(k * t)
a = -k**2 * s

fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig.suptitle('Example 2.3: Harmonic Oscillation (a = -k²s)', fontsize=16)

y_data = [s, v, a]
colors = ['b', 'g', 'r']
titles = ['Position (s-t)', 'Velocity (v-t)', 'Acceleration (a-t)']
lines = []
points = []

for i in range(3):
    axs[i].set_xlim(0, 5)
    axs[i].set_ylim(np.min(y_data[i]) * 1.2, np.max(y_data[i]) * 1.2)
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
