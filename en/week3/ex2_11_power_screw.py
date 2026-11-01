# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# Example 2.11: 3D Helix Motion
import numpy as np
import matplotlib.pyplot as plt
# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.animation import FuncAnimation

t = np.linspace(0, 10, 200)
R = 5
omega = 2
v_z = 1

x = R * np.cos(omega * t)
y = R * np.sin(omega * t)
z = v_z * t

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
fig.suptitle('Example 2.11: 3D Helix Motion', fontsize=14)

ax.plot(x, y, z, 'k--', alpha=0.3)
ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_zlim(0, 10)

line, = ax.plot([], [], [], lw=2, color='b')
# 3D Axes doesn't support text() update easily in animation with blit in standard way,
# But we can use text inside 3D! However set_position is 2D. For 3D we do set_position_3d.
point = ax.text(x[0], y[0], z[0], '🦅', fontsize=30, fontname='Segoe UI Emoji', ha='center', va='center')

def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_position_3d((x[0], y[0], z[0]))
    return line, point

def animate(i):
    line.set_data(x[:i], y[:i])
    line.set_3d_properties(z[:i])
    point.set_position_3d((x[i], y[i], z[i]))
    return line, point

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)
plt.show()
