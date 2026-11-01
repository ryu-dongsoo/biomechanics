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

# 예제 2.2: 구간별 등가속도 운동 시뮬레이션
# 교재 그림 완벽 재현 (v-t 그래프 포함 3단 그래프)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시간 배열 설정 (0 ~ 12초)
t = np.linspace(0, 12, 240)
a = np.zeros_like(t)
v = np.zeros_like(t)
s = np.zeros_like(t)

for i, time in enumerate(t):
    if time <= 4:
        a[i] = 0
        v[i] = 50
        s[i] = 50 * time
    else:
        a[i] = -10
        v[i] = 50 - 10 * (time - 4)
        s[i] = 200 + 50 * (time - 4) - 5 * (time - 4)**2

fig, axs = plt.subplots(3, 1, figsize=(6, 11))

# 공통 축 스타일 적용
for ax in axs:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

ax1, ax2, ax3 = axs

# --- s-t Graph ---
line_s, = ax1.plot([], [], color='#d62728', lw=2)
ax1.set_xlim(0, 13)
ax1.set_ylim(-20, 360)
ax1.set_xticks([0, 4, 8, 12])
ax1.set_yticks([200, 325])
ax1.text(13.5, 0, '$t, \mathrm{s}$', va='center')
ax1.text(0, 380, '$s, \mathrm{m}$', ha='center')

# --- v-t Graph (이미지 완벽 재현 대상) ---
line_v, = ax2.plot([], [], color='#d62728', lw=2)
ax2.set_xlim(0, 13)
ax2.set_ylim(-40, 60)
ax2.set_xticks([0, 4, 8, 12])
ax2.set_yticks([50]) # 0과 -30은 수동 처리
ax2.text(-0.8, 4, '0')
ax2.text(13.5, 0, '$t, \mathrm{s}$', va='center')
ax2.text(0, 68, '$v_x, \mathrm{m/s}$', ha='center')

# --- a-t Graph ---
line_a, = ax3.plot([], [], color='#d62728', lw=2)
ax3.set_xlim(0, 13)
ax3.set_ylim(-15, 5)
ax3.set_xticks([0, 4, 8, 12])
ax3.set_yticks([-10])
ax3.text(13.5, 0, '$t, \mathrm{s}$', va='center')
ax3.text(0, 8, '$a, \mathrm{m/s^2}$', ha='center')

plt.tight_layout()

def animate(i):
    t_curr = t[:i]
    
    line_s.set_data(t_curr, s[:i])
    line_v.set_data(t_curr, v[:i])
    line_a.set_data(t_curr, a[:i])
    
    # 시간 진행에 따른 애니메이션 효과 (v-t 그래프)
    if t[i] >= 4 and not hasattr(ax2, 'line_4s'):
        ax2.plot([4, 4], [0, 50], 'k--', alpha=0.8)
        ax1.plot([4, 4], [0, 200], 'k--', alpha=0.5)
        ax2.line_4s = True
        
    if t[i] >= 12 and not hasattr(ax2, 'line_12s'):
        # v-t 그래프 수직선 및 -30 틱 마크
        ax2.plot([12, 12], [0, -30], 'k-', lw=1)
        ax2.plot([11.8, 12.2], [-30, -30], 'k-', lw=1)
        ax2.text(12.4, -30, '$-30$', va='center')
        ax2.line_12s = True
        
    # 기울기 삼각형
    if t[i] >= 7.5 and not hasattr(ax2, 'slope_tri'):
        t_tri = 6.5
        v_tri = 50 - 10 * (t_tri - 4)
        ax2.plot([t_tri, t_tri+1], [v_tri, v_tri], 'k-', lw=1)
        ax2.plot([t_tri+1, t_tri+1], [v_tri, v_tri-10], 'k-', lw=1)
        ax2.text(t_tri+0.5, v_tri+2, '1', ha='center', fontsize=10)
        ax2.text(t_tri+1.2, v_tri-5, '$-10$', va='center', fontsize=10)
        ax2.slope_tri = True
        
    # a-t 그래프 4초 수직 점선
    if t[i] >= 4 and not hasattr(ax3, 'line_4s'):
        ax3.plot([4, 4], [0, -10], 'k--', alpha=0.5)
        ax3.line_4s = True

    return line_s, line_v, line_a

ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=False)

from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=50)
writer._kwargs = {'loop': None} # 1회 재생 후 완전 멈춤 (루프 속성 제거)

gif_path = 'ex2_2_piecewise.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 1회 재생 설정으로 저장되었습니다.")
