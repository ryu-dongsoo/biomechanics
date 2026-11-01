# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Problem 2/4: Integration based motion
# a = 2t - 10, v0 = 3, s0 = -4

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 10, 250)
a = 2 * t - 10
v = t**2 - 10 * t + 3
s = (1/3) * t**3 - 5 * t**2 + 3 * t - 4

fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig.suptitle('Problem 2/4: Integration of Acceleration', fontsize=16)

y_data = [s, v, a]
colors = ['b', 'g', 'r']
titles = ['Position (s-t)', 'Velocity (v-t)', 'Acceleration (a-t)']
lines = []
points = []

for i in range(3):
    axs[i].set_xlim(0, 10)
    axs[i].set_ylim(np.min(y_data[i]) - 10, np.max(y_data[i]) + 10)
    axs[i].set_title(titles[i])
    axs[i].grid(True)
    axs[i].axhline(0, color='black', lw=1, ls='--')
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
