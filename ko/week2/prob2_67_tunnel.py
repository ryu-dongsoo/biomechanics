# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 유동수 (Dongsoo Ryu). All rights reserved.
#   - 소속 (Affiliation) : 전북대학교 생물산업기계공학과
#                          (Dept. of Bioindustrial Machinery Engineering,
#                           Jeonbuk National University)
#   - 성명 (Author)      : 유동수 (Dongsoo Ryu)
#   - 이메일 (Contact)   : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - 교과목 (Course)    : 생물역학 (Biomechanics)
# =============================================================================

# 연습문제 2/67: 터널 안 포물체
# v0 = 25 m/s, 최대 높이 y_max = 5 m

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

v0 = 25
g = 9.81
y_max = 5

# v_y0^2 = 2*g*y_max
v_y0 = np.sqrt(2 * g * y_max)
theta = np.arcsin(v_y0 / v0)
v_x0 = v0 * np.cos(theta)

t_f = 2 * v_y0 / g
t = np.linspace(0, t_f, 200)

x = v_x0 * t
y = v_y0 * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(12, 4))
fig.suptitle('Problem 2/67: Projectile in a Tunnel', fontsize=16)

ax.set_xlim(0, max(x) + 5)
ax.set_ylim(0, y_max + 2)
ax.set_xlabel('Distance x (m)')
ax.set_ylabel('Height y (m)')
ax.grid(True)

# 천장 그리기
ax.axhline(y_max, color='r', lw=2, label='Ceiling (5m)')

line, = ax.plot([], [], lw=2, color='b')
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
