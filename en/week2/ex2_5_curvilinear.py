# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Example 2.5: Curvilinear motion in rectangular coordinates
# v_x = 50 - 16t, y = 100 - 4t^2

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 6, 200)

# 운동 방정식
x = 50 * t - 8 * t**2
y = 100 - 4 * t**2

v_x = 50 - 16 * t
v_y = -8 * t

fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('Example 2.5: Curvilinear Motion', fontsize=16)

ax.set_xlim(np.min(x) - 10, np.max(x) + 10)
ax.set_ylim(np.min(y) - 10, np.max(y) + 10)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.grid(True)
ax.axhline(0, color='black', lw=1, ls='--')

line, = ax.plot([], [], lw=2, color='b', label='Trajectory')
point, = ax.plot([], [], 'o', color='r', markersize=8, label='Particle')
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
