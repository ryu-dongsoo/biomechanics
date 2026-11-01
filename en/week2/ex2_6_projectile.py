# Example 2.6: Projectile motion over a fence
# v0 = 24 m/s, angle = 35 deg, y0 = 2 m
# 울타리 위치 x = 30 m, 높이 = 6 m

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

v0 = 24
theta = np.radians(35)
g = 9.81
y0 = 2

# 체공시간 계산 (y = 0 일 때)
# 0 = 2 + v0*sin(th)*t - 0.5*g*t^2
v_y0 = v0 * np.sin(theta)
v_x0 = v0 * np.cos(theta)
t_f = (v_y0 + np.sqrt(v_y0**2 - 4 * (-0.5*g) * y0)) / g
t = np.linspace(0, t_f, 200)

x = v_x0 * t
y = y0 + v_y0 * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Example 2.6: Projectile over a fence', fontsize=16)

ax.set_xlim(0, max(x) + 5)
ax.set_ylim(0, max(y) + 5)
ax.set_xlabel('Distance x (m)')
ax.set_ylabel('Height y (m)')
ax.grid(True)
ax.axhline(0, color='black', lw=1)

# 울타리 그리기
fence_x = 30
fence_y = 6
ax.plot([fence_x, fence_x], [0, fence_y], color='r', lw=3, label='Fence (6m)')

line, = ax.plot([], [], lw=2, color='b', ls='--')
point, = ax.plot([], [], 'o', color='b', markersize=8)
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
