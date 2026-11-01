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

# 2주차 실습 과제: 스켈레톤 코드 (Skeleton Code)
# 연습문제 2/62 ~ 2/66 중 하나를 선택하여 포물체 궤적을 시각화하세요.

import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

# 1. 초기 조건 설정
# TODO: 중력가속도, 발사속도, 발사각 등을 설정하세요.
g = 9.81
v0 = 10
theta = np.radians(45)

# 2. 시간 배열 설정
# TODO: 체공시간을 계산하고 시간 배열 t를 생성하세요.
t_f = 2.0
t = np.linspace(0, t_f, 200)

# 3. 운동 방정식 구현
# TODO: x방향 등속운동, y방향 등가속도 운동 방정식을 작성하세요.
x = np.zeros_like(t)
y = np.zeros_like(t)

# 4. 그래프 설정
fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Homework: 2D Projectile Motion', fontsize=16)

ax.set_xlim(0, 20) # TODO: x축 범위 조정
ax.set_ylim(0, 20) # TODO: y축 범위 조정
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='b', ls='--')
point, = ax.plot([], [], 'o', color='r', markersize=8)

# 5. 그래프 초기화
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# 6. 애니메이션 실행
def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
