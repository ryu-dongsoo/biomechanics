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

# 과제: 극좌표계 시뮬레이션
# TODO: 문제의 조건에 맞는 운동방정식을 세우세요.

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
fig.suptitle('과제: 극좌표계 시뮬레이션', fontsize=14)
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
