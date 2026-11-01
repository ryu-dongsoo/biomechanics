# Example 2.7: Car Curve Simulation
import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

# Parameters
R = 150  # Radius
v0 = 20  # Initial speed
at = -2  # Tangential acceleration

t_f = 10
t = np.linspace(0, t_f, 200)
s = v0 * t + 0.5 * at * t**2
theta = s / R

x = R * np.cos(theta)
y = R * np.sin(theta)

fig, ax = plt.subplots(figsize=(6, 6))
fig.suptitle('Example 2.7: Car Curve Simulation', fontsize=14)
ax.plot(R * np.cos(np.linspace(0, 2*np.pi, 100)), R * np.sin(np.linspace(0, 2*np.pi, 100)), 'k--', alpha=0.5)
ax.set_aspect('equal')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='b')
point = ax.text(0, 0, '🚗', fontsize=30, fontname='Segoe UI Emoji', ha='center', va='center')

def init():
    line.set_data([], [])
    point.set_position((0, 0))
    return line, point

def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_position((x[i], y[i]))
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
