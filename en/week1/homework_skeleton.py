# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Week 1 Homework: 스켈레톤 코드 (Skeleton Code)
# Problem 2/5, 2/6, 2/7, 2/8, 2/10 중 하나를 선택하여 직접 시뮬레이션해 보세요.

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

# 1. Time array setup
# TODO: 시뮬레이션할 시간(t) 범위를 설정하세요. (예: np.linspace(0, 10, 200))
t = np.linspace(0, 10, 200)

# 2. Equations of motion implementation
# TODO: 과제로 주어진 문제의 s, v, a 관계식을 작성하세요.
s = np.zeros_like(t) # 위치
v = np.zeros_like(t) # 속도
a = np.zeros_like(t) # 가속도

# 3. Graph setup
fig, axs = plt.subplots(3, 1, figsize=(8, 10))
fig.suptitle('Homework: Rectilinear Motion Simulation', fontsize=16)

y_data = [s, v, a]
colors = ['b', 'g', 'r']
titles = ['Position (s-t)', 'Velocity (v-t)', 'Acceleration (a-t)']
lines = []
points = []

# 4. Graph initialization
for i in range(3):
    axs[i].set_xlim(0, np.max(t))
    # TODO: y축 범위를 데이터에 맞게 적절히 조정하세요.
    axs[i].set_ylim(-10, 10) 
    axs[i].set_title(titles[i])
    axs[i].grid(True)
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

# 5. Run animation
ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()
