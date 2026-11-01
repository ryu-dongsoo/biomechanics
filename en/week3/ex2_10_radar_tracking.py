# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Example 2.10: Radar Tracking Plane
import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 10, 200)
v = 100
h = 500
x = v * t - 500
y = np.full_like(t, h)

fig, ax = plt.subplots(figsize=(8, 4))
fig.suptitle('Example 2.10: Radar Tracking Plane', fontsize=14)
ax.set_xlim(-600, 600)
ax.set_ylim(0, 600)
ax.grid(True)

line, = ax.plot([], [], 'b--', lw=1)
radar_beam, = ax.plot([], [], 'g-', lw=2, alpha=0.6)
ax.text(0, 0, '📡', fontsize=35, fontname='Segoe UI Emoji', ha='center', va='bottom', label='Radar')
point = ax.text(0, 0, '✈️', fontsize=35, fontname='Segoe UI Emoji', ha='center', va='center')

def init():
    line.set_data([], [])
    radar_beam.set_data([], [])
    point.set_position((0, h))
    return line, radar_beam, point

def animate(i):
    line.set_data(x[:i], y[:i])
    radar_beam.set_data([0, x[i]], [0, y[i]])
    point.set_position((x[i], y[i]))
    return line, radar_beam, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
