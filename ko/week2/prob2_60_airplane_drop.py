# 연습문제 2/60: 비행기 우편물 투하
# v_x0 = 55.56 m/s, y0 = 100 m

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

v_x0 = 55.56
y0 = 100
g = 9.81

t_f = np.sqrt(2 * y0 / g)
t = np.linspace(0, t_f, 200)

x = v_x0 * t
y = y0 - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Problem 2/60: Airplane Mail Drop', fontsize=16)

ax.set_xlim(0, max(x) + 20)
ax.set_ylim(0, y0 + 10)
ax.set_xlabel('Horizontal Distance x (m)')
ax.set_ylabel('Altitude y (m)')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='b', ls='--')
point, = ax.plot([], [], 'o', color='r', markersize=8, label='Mail')
target, = ax.plot([max(x)], [0], 'X', color='g', markersize=12, label='Target')
ax.legend()

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
