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

"""
[동역학 9판 예제 3.4] 비선형 유체 저항력(R=2v²) 하에서의 모터보트 감속 정지 해석
교재 원본 삽화 및 FBD, R-v 포물선 그래프 100% 동일 구현
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

# 물리 파라미터
m = 10.0          # 질량 (kg)
v0 = 2.0          # 초기 속도 (m/s)
k = 2.0           # 저항 계수 (N*s^2/m^2)
t_target = 2.5    # v=1 m/s 도달 시간 (s)
x_target = 5.0 * np.log(2.0)  # v=1 m/s 도달 이동거리 (약 3.466 m)

# 애니메이션 시간 설정
duration = 3.2    # 총 시뮬레이션 시간 (초)
fps = 30
n_sim_frames = int(fps * duration)
n_pause_frames = 18
total_frames = n_sim_frames + n_pause_frames

t_eval = np.linspace(0, duration, n_sim_frames)

fig = plt.figure(figsize=(11.5, 7.8), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.03, 0.03, 0.94, 0.90])
title_text = '[동역학 9판 예제 3.4] 예인선 분리 후 유체 저항력(R = 2v²)에 의한 모형 선박의 감속 운동'

def get_state(t):
    # v(t) = 10 / (2t + 5)
    v = 10.0 / (2.0 * t + 5.0)
    # x(t) = 5 * ln(1 + 0.4t)
    x = 5.0 * np.log(1.0 + 0.4 * t)
    # R(t) = 2 * v^2
    R = 2.0 * (v**2)
    # a(t) = -0.2 * v^2
    a = -0.2 * (v**2)
    return v, x, R, a

def update(frame):
    if frame < n_sim_frames:
        t = t_eval[frame]
    else:
        t = duration
        
    v_curr, x_curr, R_curr, a_curr = get_state(t)
    
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 17.5)
    ax.set_ylim(-5.5, 10.5)
    ax.axis('off')
    
    # 1. 배경 (밝은 슬레이트 톤)
    ax.add_patch(patches.Rectangle((-2.5, -5.5), 20.0, 16.0, fc='#f8fafc', ec='none', zorder=1))
    
    # -------------------------------------------------------------
    # 2. 우측 상단: 교재 원본과 100% 동일한 R-v 그래프 영역 (완전 박스형 그리드)
    # -------------------------------------------------------------
    graph_box = patches.FancyBboxPatch((9.2, 3.8), 7.8, 6.2,
                                       boxstyle="round,pad=0.25", fc="#ffffff", ec='#94a3b8', lw=1.2, alpha=0.98, zorder=10)
    ax.add_patch(graph_box)
    
    gx_min, gx_max = 10.5, 16.2
    gy_min, gy_max = 4.6, 9.4
    
    def map_v(v_val):
        return gx_min + (v_val / 2.0) * (gx_max - gx_min)
    def map_R(R_val):
        return gy_min + (R_val / 8.0) * (gy_max - gy_min)
    
    # 8x8 사각 격자선 (교재와 완벽 일치)
    for vi in np.linspace(0, 2, 9):
        xg = map_v(vi)
        ax.plot([xg, xg], [gy_min, gy_max], color='#cbd5e1', lw=0.9, zorder=11)
    for Ri in np.linspace(0, 8, 9):
        yg = map_R(Ri)
        ax.plot([gx_min, gx_max], [yg, yg], color='#cbd5e1', lw=0.9, zorder=11)
        
    # 축 외곽 박스 (사방 검은색 테두리)
    ax.plot([gx_min, gx_max, gx_max, gx_min, gx_min],
            [gy_min, gy_min, gy_max, gy_max, gy_min], color='#1e293b', lw=1.5, zorder=12)
    
    # 축 눈금 텍스트
    ax.text(map_v(0), gy_min - 0.28, '0', fontsize=8.5, color='#1e293b', ha='center', va='top', zorder=13)
    ax.text(map_v(1), gy_min - 0.28, '1', fontsize=8.5, color='#1e293b', ha='center', va='top', zorder=13)
    ax.text(map_v(2), gy_min - 0.28, '2', fontsize=8.5, color='#1e293b', ha='center', va='top', zorder=13)
    ax.text(map_v(1), gy_min - 0.65, r'$v\text{, m/s}$', fontsize=9.5, fontweight='bold', color='#1e293b', ha='center', va='top', zorder=13)
    
    ax.text(gx_min - 0.15, map_R(0) - 0.12, '0', fontsize=8.5, color='#1e293b', ha='right', va='center', zorder=13)
    ax.text(gx_min - 0.15, map_R(2), '2', fontsize=8.5, color='#1e293b', ha='right', va='center', zorder=13)
    ax.text(gx_min - 0.15, map_R(4), '4', fontsize=8.5, color='#1e293b', ha='right', va='center', zorder=13)
    ax.text(gx_min - 0.15, map_R(6), '6', fontsize=8.5, color='#1e293b', ha='right', va='center', zorder=13)
    ax.text(gx_min - 0.15, map_R(8), '8', fontsize=8.5, color='#1e293b', ha='right', va='center', zorder=13)
    ax.text(gx_min - 0.65, map_R(4), r'$R\text{, N}$', fontsize=9.5, fontweight='bold', color='#1e293b', ha='center', va='center', rotation=90, zorder=13)
    
    # 실험 측정 데이터 점들 (검은색 점)
    exp_pts = [(0.0, 0.0), (0.45, 0.42), (0.75, 1.12), (1.18, 2.75), (1.62, 5.25), (2.0, 8.0)]
    for ev, er in exp_pts:
        ax.scatter(map_v(ev), map_R(er), color='#0f172a', s=24, zorder=14)
    
    # 빨간색 점선 포물선 곡선: R = 2 v^2
    v_curve = np.linspace(0, 2.0, 100)
    R_curve = 2.0 * (v_curve**2)
    ax.plot(map_v(v_curve), map_R(R_curve), color='#ef4444', lw=1.8, linestyle='--', zorder=15)
    
    # 현재 작동점 마커 & 보조선
    g_curr_x = map_v(v_curr)
    g_curr_y = map_R(R_curr)
    ax.plot([gx_min, g_curr_x], [g_curr_y, g_curr_y], color='#ef4444', lw=1.1, linestyle=':', zorder=16)
    ax.plot([g_curr_x, g_curr_x], [gy_min, g_curr_y], color='#16a34a', lw=1.1, linestyle=':', zorder=16)
    ax.scatter([g_curr_x], [g_curr_y], color='#dc2626', edgecolors='#991b1b', s=50, zorder=17)
    ax.text(g_curr_x + 0.15, g_curr_y + 0.15, f'$({v_curr:.2f}, {R_curr:.2f})$',
            fontsize=8.0, fontweight='bold', color='#dc2626', zorder=18)
    
    # -------------------------------------------------------------
    # 3. 좌측 상단: HUD 정보 박스 (문제 조건 및 실시간 계산식)
    # -------------------------------------------------------------
    hud_str = (
        f"[예제 3.4 수조 내 모형 선박 감속 해석]\n"
        f"경과 시간:  t = {t:4.2f} s / {duration:.1f} s\n"
        f"-----------------------------------------\n"
        f"• 질량: m = 10 kg,  초기속도: v_0 = 2.0 m/s\n"
        f"• 저항력 모델: R = kv² = 2v² N  (k = 2 N·s²/m²)\n"
        f"• 운동방정식: ΣFx = -R = m(dv/dt)\n"
        f"  -2v² = 10(dv/dt) ⇒ dt = -5 (dv/v²)\n"
        f"  t = 5(1/v - 1/2) s  ⇔  v(t) = 10 / (2t + 5) m/s\n"
        f"• 이동거리: v(dv/dx) = -0.2v² ⇒ x = 5 ln(2/v) m\n"
        f"-----------------------------------------\n"
        f"• 현재 속도:   v(t) = {v_curr:4.2f} m/s\n"
        f"• 저항력:     R(t) = {R_curr:4.2f} N\n"
        f"• 감속 가속도: a(t) = {a_curr:4.2f} m/s²\n"
        f"• 이동 거리:   x(t) = {x_curr:4.2f} m\n"
        f"-----------------------------------------\n"
        f"▶ 목표(v=1 m/s) 도달 시간: t = 2.50 s\n"
        f"▶ 목표 도달 시 이동거리:   x = 3.47 m"
    )
    ax.text(-2.0, 10.0, hud_str, fontsize=7.6, va='top', family='monospace', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor='#0284c7', lw=1.3, alpha=0.98), zorder=20)
    
    # -------------------------------------------------------------
    # 4. 하단 물리 시뮬레이션 및 자유물체도 (FBD)
    # -------------------------------------------------------------
    ship_scale = 2.1
    ship_x_init = 1.8  # 시작 시점 선박 중심 위치
    ship_x = ship_x_init + x_curr * ship_scale
    ship_y = -1.2      # 수면 높이 기준
    
    # 수면 및 물 영역
    water_y = ship_y
    water = patches.Rectangle((-2.5, -5.5), 20.0, (water_y - (-5.5)), fc='#e0f2fe', ec='none', zorder=2)
    ax.add_patch(water)
    ax.plot([-2.5, 17.5], [water_y, water_y], color='#0284c7', lw=2.2, zorder=4)
    water_deep = patches.Rectangle((-2.5, -5.5), 20.0, 2.5, fc='#bae6fd', ec='none', alpha=0.6, zorder=2)
    ax.add_patch(water_deep)
    
    # 항적 (Wake / 뒤쪽 수면 파동)
    if ship_x > ship_x_init:
        wake_x = np.linspace(-2.0, ship_x - 2.8, 40)
        wake_y = water_y + 0.07 * np.sin((wake_x - ship_x) * 4.5 + t * 8.0)
        ax.plot(wake_x, wake_y, color='#ffffff', lw=1.5, alpha=0.85, zorder=5)
        
    # -------------------------------------------------------------
    # 선박 형상 그리기 (교재 삽화 100% 동일 디테일)
    # -------------------------------------------------------------
    # 선체(Hull) 외형 폴리곤
    hull_pts = [
        [ship_x - 3.2, water_y + 0.6],   # 이물(Bow) 상단 팁
        [ship_x - 3.0, water_y + 0.1],   # 이물 곡선
        [ship_x - 2.2, water_y - 0.7],   # 바닥 전방
        [ship_x + 2.2, water_y - 0.7],   # 바닥 후방
        [ship_x + 3.0, water_y + 0.7],   # 선미(Stern) 상단 팁
        [ship_x - 2.4, water_y + 0.7],   # 갑판 라인
    ]
    hull_poly = patches.Polygon(hull_pts, closed=True, fc='#dfcbb5', ec='#7c5e42', lw=1.6, zorder=6)
    ax.add_patch(hull_poly)
    
    # 선체 상부 구조물 (선실 및 굴뚝/타워)
    # 1) 선실 (중앙)
    cabin_pts = [
        [ship_x - 0.8, water_y + 0.7],
        [ship_x + 0.6, water_y + 0.7],
        [ship_x + 0.6, water_y + 1.8],
        [ship_x - 0.8, water_y + 1.8],
    ]
    cabin_poly = patches.Polygon(cabin_pts, closed=True, fc='#d2bba3', ec='#7c5e42', lw=1.4, zorder=7)
    ax.add_patch(cabin_poly)
    
    # 2) 후방 타워/조타실 (우측 높은 구조)
    tower_pts = [
        [ship_x + 0.7, water_y + 0.7],
        [ship_x + 2.0, water_y + 0.7],
        [ship_x + 2.2, water_y + 2.3],
        [ship_x + 0.8, water_y + 2.1],
    ]
    tower_poly = patches.Polygon(tower_pts, closed=True, fc='#c8af96', ec='#7c5e42', lw=1.4, zorder=7)
    ax.add_patch(tower_poly)
    
    # 선체 디테일 선
    ax.plot([ship_x - 2.3, ship_x + 2.8], [water_y + 0.4, water_y + 0.4], color='#b5997d', lw=0.8, linestyle=':', zorder=8)
    
    # 수면 아래 침수부 오버레이 (교재의 푸른색 투명 침수 영역)
    submerged_pts = [
        [ship_x - 2.8, water_y],
        [ship_x - 2.2, water_y - 0.7],
        [ship_x + 2.2, water_y - 0.7],
        [ship_x + 2.7, water_y],
    ]
    submerged_poly = patches.Polygon(submerged_pts, closed=True, fc='#38bdf8', ec='#0284c7', lw=1.2, alpha=0.55, zorder=9)
    ax.add_patch(submerged_poly)
    
    # 선체 질량 텍스트
    ax.text(ship_x - 0.1, water_y + 0.2, r'$m = 10\text{ kg}$', fontsize=8.0, fontweight='bold', color='#4a3525', ha='center', zorder=10)
    
    # -------------------------------------------------------------
    # 5. 힘 벡터 및 운동학 벡터 (FBD 교재 원본 100% 일치)
    # -------------------------------------------------------------
    # (1) 중력 하중 W (빨간색 하향 화살표, 선박 중심)
    w_top_y = water_y + 3.2
    w_bot_y = water_y + 1.2
    ax.annotate('', xy=(ship_x, w_bot_y), xytext=(ship_x, w_top_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=15)
    ax.text(ship_x, w_top_y + 0.15, r'$W$', fontsize=11.5, fontweight='bold', color='#b91c1c', ha='center', va='bottom', zorder=16)
    
    # (2) 부력 B = W (빨간색 상향 화살표, 바닥 중심)
    b_bot_y = water_y - 2.5
    b_top_y = water_y - 0.8
    ax.annotate('', xy=(ship_x, b_top_y), xytext=(ship_x, b_bot_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=15)
    ax.text(ship_x + 0.35, b_bot_y + 0.6, r'$B = W$', fontsize=10.5, fontweight='bold', color='#b91c1c', ha='left', va='center', zorder=16)
    
    # (3) 유체 저항력 R (빨간색 좌향 화살표, 침수부 우측)
    r_vec_len = 1.0 + (R_curr / 8.0) * 2.5
    r_start_x = ship_x + 2.7 + r_vec_len
    r_end_x = ship_x + 2.7
    r_y = water_y - 0.35
    ax.annotate('', xy=(r_end_x, r_y), xytext=(r_start_x, r_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=7.0, headlength=8.0), zorder=15)
    ax.text(r_start_x + 0.25, r_y, f'$R$', fontsize=11.5, fontweight='bold', color='#b91c1c', va='center', zorder=16)
    
    # (4) 현재 속도 벡터 v (초록색 우향 화살표)
    v_vec_len = 0.8 + (v_curr / 2.0) * 1.8
    v_start_x = ship_x + 1.8
    v_end_x = v_start_x + v_vec_len
    v_y = water_y + 3.5
    ax.annotate('', xy=(v_end_x, v_y), xytext=(v_start_x, v_y),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=6.0, headlength=7.0), zorder=15)
    ax.text(v_start_x + v_vec_len/2.0, v_y + 0.2, r'$v$', fontsize=11.0, fontweight='bold', color='#16a34a', ha='center', va='bottom', zorder=16)
    
    # (5) 초기 속도 표시 v0 = 2 m/s (시작 기준선 상단)
    v0_start_x = ship_x_init - 2.8
    v0_end_x = v0_start_x + 1.8
    v0_y = water_y + 3.5
    ax.annotate('', xy=(v0_end_x, v0_y), xytext=(v0_start_x, v0_y),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text((v0_start_x + v0_end_x)/2.0, v0_y + 0.2, r'$v_0 = 2\text{ m/s}$', fontsize=10.0, fontweight='bold', color='#16a34a', ha='center', va='bottom', zorder=16)
    
    # -------------------------------------------------------------
    # 6. 시작 기준선 및 이동거리 치수선 x (교재와 100% 동일한 양방향 화살표)
    # -------------------------------------------------------------
    init_ref_x = ship_x_init - 2.8  # 기준 세로선 위치
    curr_ref_x = ship_x             # 현재 배 중심 W 기준선
    
    dim_y = water_y + 2.8
    # 좌측 시작 기준선 (세로 실선)
    ax.plot([init_ref_x, init_ref_x], [water_y, dim_y + 0.5], color='#334155', lw=1.2, zorder=12)
    # 현재 배 중심선 (세로 점선/실선)
    ax.plot([curr_ref_x, curr_ref_x], [water_y + 1.8, dim_y + 0.5], color='#334155', lw=1.0, linestyle=':', zorder=12)
    
    # 양방향 치수선 x
    if curr_ref_x > init_ref_x + 0.5:
        ax.annotate('', xy=(init_ref_x, dim_y), xytext=(curr_ref_x, dim_y),
                    arrowprops=dict(arrowstyle='<->', color='#1e293b', lw=1.3), zorder=13)
        ax.text((init_ref_x + curr_ref_x)/2.0, dim_y + 0.15, r'$x$',
                fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', va='bottom', zorder=14)
    else:
        ax.plot([init_ref_x, curr_ref_x], [dim_y, dim_y], color='#1e293b', lw=1.3, zorder=13)
        ax.text(init_ref_x, dim_y + 0.15, r'$x$', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', va='bottom', zorder=14)

fig.suptitle(title_text, fontsize=12.0, fontweight='bold', y=0.965, fontproperties=font_prop)
anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'ex3_4_boat_resistance.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
