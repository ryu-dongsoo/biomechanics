# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Week 2 Lab Homework: Skeleton Code
# Problem 2/62 ~ 2/66 중 하나를 선택하여 포물체 궤적을 시각화하세요.

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

# 1. Set Initial Conditions
# TODO: 중력가속도, 발사속도, 발사각 등을 설정하세요.
g = 9.81
v0 = 10
theta = np.radians(45)

# 2. Set Time Array
# TODO: 체공시간을 계산하고 시간 배열 t를 생성하세요.
t_f = 2.0
t = np.linspace(0, t_f, 200)

# 3. Implement Equations of Motion
# TODO: x방향 등속운동, y방향 등가속도 운동 방정식을 작성하세요.
x = np.zeros_like(t)
y = np.zeros_like(t)

# 4. Graph Setup
fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Homework: 2D Projectile Motion', fontsize=16)

ax.set_xlim(0, 20) # TODO: x축 범위 조정
ax.set_ylim(0, 20) # TODO: y축 범위 조정
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='b', ls='--')
point, = ax.plot([], [], 'o', color='r', markersize=8)

# 5. Graph Init
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# 6. Run Animation
def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
