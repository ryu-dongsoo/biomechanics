# Example 2.9: Robot Arm Slider
import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 5, 200)
r = 0.5 + 3 * t
theta = 2 * t

x = r * np.cos(theta)
y = r * np.sin(theta)

fig, ax = plt.subplots(figsize=(6, 6))
fig.suptitle('Example 2.9: Robot Arm Slider', fontsize=14)
ax.plot(x, y, 'k--', alpha=0.5)
ax.set_aspect('equal')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='g')
arm, = ax.plot([], [], 'r-', lw=3)
point = ax.text(0, 0, '🦾', fontsize=30, fontname='Segoe UI Emoji', ha='center', va='center')

def init():
    line.set_data([], [])
    arm.set_data([], [])
    point.set_position((0, 0))
    return line, arm, point

def animate(i):
    line.set_data(x[:i], y[:i])
    arm.set_data([0, x[i]], [0, y[i]])
    point.set_position((x[i], y[i]))
    return line, arm, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
