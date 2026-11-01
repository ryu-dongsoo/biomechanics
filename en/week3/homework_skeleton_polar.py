# Homework: Polar Coordinates
# TODO: Set up the equations of motion according to the problem conditions.

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 5, 100)
x = np.zeros_like(t)
y = np.zeros_like(t)

fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('Homework: Polar Coordinates', fontsize=14)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.grid(True)

line, = ax.plot([], [], lw=2, color='g', ls='--')
point = ax.text(0, 0, '🎯', fontsize=30, fontname='Segoe UI Emoji', ha='center', va='center')

def init():
    line.set_data([], [])
    point.set_position((0, 0))
    return line, point

def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_position((x[i], y[i]))
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=30)
plt.show()
