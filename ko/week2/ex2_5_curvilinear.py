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

# 예제 2.5: 직교좌표 곡선운동
# 교재 그림 재현 및 역학 그래프 동기화 애니메이션

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시간 배열 설정 (0 ~ 5초)
frames = 125 # 5초 * 25fps = 125프레임
t = np.linspace(0, 5, frames)

# 운동학 함수
x = 50 * t - 8 * t**2
y = 100 - 4 * t**2

vx = 50 - 16 * t
vy = -8 * t
v_mag = np.sqrt(vx**2 + vy**2)

ax_const = -16 * np.ones_like(t)
ay_const = -8 * np.ones_like(t)
a_mag = np.sqrt((-16)**2 + (-8)**2) * np.ones_like(t)

fig = plt.figure(figsize=(10, 8))
fig.suptitle('예제 2.5: 질점의 곡선운동 ($x-y$ 직교좌표계)', fontsize=16, fontweight='bold')
gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1])

# --- 상단: 궤적 도식화 (교재 그림 완벽 재현) ---
ax_mech = fig.add_subplot(gs[0, :])
ax_mech.set_aspect('equal') # x, y 비율 동일하게 설정 (중요: 궤적 모양이 교재와 같아짐)
# 교재 x축은 0~80, y축은 0~100
ax_mech.set_xlim(0, 85)
ax_mech.set_ylim(0, 105)
ax_mech.set_xticks(np.arange(0, 100, 20))
ax_mech.set_yticks(np.arange(0, 120, 20))
ax_mech.set_xlabel('$x$, m', fontsize=14)
ax_mech.set_ylabel('$y$, m', fontsize=14)
ax_mech.grid(True, color='black', linestyle='-', linewidth=0.8, alpha=0.7)

for spine in ax_mech.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(1.5)

# 정적 마커들 그리기 (t=0, 1, 2, 3, 4, 5)
t_marks = [0, 1, 2, 3, 4, 5]
x_marks = [50*tm - 8*tm**2 for tm in t_marks]
y_marks = [100 - 4*tm**2 for tm in t_marks]

# 미리 점들을 흐리게 그려둠 (가이드 역할)
ax_mech.plot(x_marks, y_marks, 'o', mfc='white', mec='gray', markersize=6, alpha=0.5)

# 동적 요소들
traj_line, = ax_mech.plot([], [], color='#e74c3c', lw=2.5) # 빨간색 궤적
particle, = ax_mech.plot([], [], 'o', mfc='white', mec='black', markersize=8, zorder=5)

v_quiver = None
a_quiver = None

# 정보 텍스트 패널 (그래프, 궤적과 절대 겹치지 않도록 피규어 좌측 상단 빈 공간으로 완전 이동)
info_text = fig.text(0.05, 0.85, '', fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.95, edgecolor='gray', boxstyle='round,pad=0.5'))

# --- 하단 좌측: 위치-시간 그래프 ---
ax_pos = fig.add_subplot(gs[1, 0])
ax_pos.set_xlim(0, 5)
ax_pos.set_ylim(0, 105)
ax_pos.grid(True, linestyle='--', alpha=0.7)
ax_pos.set_xlabel('시간 $t$ (s)')
ax_pos.set_ylabel('위치 (m)')
ax_pos.set_title('위치 - 시간 그래프')
line_x, = ax_pos.plot(t, x, color='#3498db', lw=2, label='$x$ 위치')
line_y, = ax_pos.plot(t, y, color='#9b59b6', lw=2, label='$y$ 위치')
ax_pos.legend(loc='best')
time_marker_pos, = ax_pos.plot([0, 0], ax_pos.get_ylim(), 'k--', lw=1)
point_x, = ax_pos.plot([], [], 'o', color='#3498db', markersize=6)
point_y, = ax_pos.plot([], [], 'o', color='#9b59b6', markersize=6)

# --- 하단 우측: 속도-시간 그래프 ---
ax_vel = fig.add_subplot(gs[1, 1])
ax_vel.set_xlim(0, 5)
ax_vel.set_ylim(-50, 60)
ax_vel.grid(True, linestyle='--', alpha=0.7)
ax_vel.set_xlabel('시간 $t$ (s)')
ax_vel.set_ylabel('속도 (m/s)')
ax_vel.set_title('속도 - 시간 그래프')
line_vx, = ax_vel.plot(t, vx, color='#2ecc71', lw=2, label='$v_x$')
line_vy, = ax_vel.plot(t, vy, color='#f1c40f', lw=2, label='$v_y$')
line_vmag, = ax_vel.plot(t, v_mag, color='#e67e22', lw=2, ls='-', label='$|v|$')
ax_vel.legend(loc='best')
time_marker_vel, = ax_vel.plot([0, 0], ax_vel.get_ylim(), 'k--', lw=1)
point_vx, = ax_vel.plot([], [], 'o', color='#2ecc71', markersize=6)
point_vy, = ax_vel.plot([], [], 'o', color='#f1c40f', markersize=6)
point_vmag, = ax_vel.plot([], [], 'o', color='#e67e22', markersize=6)

plt.tight_layout()

drawn_markers = []
marker_texts = []

def animate(i):
    global v_quiver, a_quiver, drawn_markers, marker_texts
    
    if i == 0:
        drawn_markers.clear()
        for mt in marker_texts:
            mt.remove()
        marker_texts.clear()
        
    current_t = t[i]
    current_x = x[i]
    current_y = y[i]
    
    # 궤적 및 파티클 갱신
    traj_line.set_data(x[:i], y[:i])
    particle.set_data([current_x], [current_y])
    
    # 정적 마커 도달 시 라벨 표시
    for tm, xm, ym in zip(t_marks, x_marks, y_marks):
        if current_t >= tm and tm not in drawn_markers:
            ax_mech.plot([xm], [ym], 'o', mfc='white', mec='black', markersize=6, zorder=4)
            if tm == 0:
                txt = ax_mech.text(xm, ym + 2, f'$t={tm}$', fontsize=12, ha='center', va='bottom')
            elif tm == 5:
                txt = ax_mech.text(xm, ym + 2, f'$t={tm}$ s', fontsize=12, ha='right', va='bottom')
                txt2 = ax_mech.text(xm + 2, ym, 'A', fontsize=12, ha='left', va='center')
                marker_texts.append(txt2)
            else:
                txt = ax_mech.text(xm - 2, ym - 2, f'{tm}', fontsize=12, ha='right', va='top')
            marker_texts.append(txt)
            drawn_markers.append(tm)
            
    # 벡터 갱신
    if v_quiver is not None:
        v_quiver.remove()
    if a_quiver is not None:
        a_quiver.remove()
        
    v_scale = 0.3
    a_scale = 0.5
    
    v_quiver = ax_mech.quiver(current_x, current_y, vx[i] * v_scale, vy[i] * v_scale, 
                              color='#27ae60', angles='xy', scale_units='xy', scale=1, width=0.005, zorder=3)
    a_quiver = ax_mech.quiver(current_x, current_y, ax_const[i] * a_scale, ay_const[i] * a_scale, 
                              color='#c0392b', angles='xy', scale_units='xy', scale=1, width=0.005, zorder=3)
                              
    info_text.set_text(f"시간 $t = {current_t:.1f}$ s\n좌표 $(x, y) = ({current_x:.1f}, {current_y:.1f})$ m\n"
                       f"속도 $(v_x, v_y) = ({vx[i]:.1f}, {vy[i]:.1f})$ m/s\n"
                       f"가속도 $(a_x, a_y) = ({ax_const[i]:.1f}, {ay_const[i]:.1f})$ m/s²")
                       
    # 그래프 갱신
    time_marker_pos.set_data([current_t, current_t], ax_pos.get_ylim())
    point_x.set_data([current_t], [current_x])
    point_y.set_data([current_t], [current_y])
    
    time_marker_vel.set_data([current_t, current_t], ax_vel.get_ylim())
    point_vx.set_data([current_t], [vx[i]])
    point_vy.set_data([current_t], [vy[i]])
    point_vmag.set_data([current_t], [v_mag[i]])
    
    return traj_line, particle, time_marker_pos, point_x, point_y, time_marker_vel, point_vx, point_vy, point_vmag

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)

writer = PillowWriter(fps=25)
writer._kwargs = {'loop': None}
gif_path = 'ex2_5_curvilinear.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")

# 딜레이 연장
try:
    from PIL import Image
    im = Image.open(gif_path)
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 40))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(gif_path, save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("딜레이 연장 성공")
except Exception as e:
    print("딜레이 연장 실패:", e)
