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

# 문제 2/135: 코르크 스크루(Corkscrew) 롤러코스터의 원통나선 운동
# 교재 원본 삽화와 100% 동일한 정밀 기하학 투영, 레일 시작점/끝점(A), 차량 이동 궤적 및 동역학 가속도 해석

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 물리 및 기하학적 매개변수 설정 ---
# 원통 유효반지름 r = 5 m, 나선각 gamma = 40 deg, 속력 v = 15 m/s, 중력가속도 g = 9.81 m/s^2
r_cyl = 5.0
gamma_deg = 40.0
gamma_rad = np.radians(gamma_deg)
v_A = 15.0
g = 9.81

# 동역학 정답 수치
rho_A = r_cyl / (np.cos(gamma_rad)**2) # 8.520 m
at_A = g * np.cos(gamma_rad)          # 7.515 m/s^2
an_A = (v_A**2) / rho_A               # 26.407 m/s^2
a_mag_A = np.sqrt(at_A**2 + an_A**2)   # 27.46 m/s^2 (2.80 G)

# --- 2. 캔버스 및 2.5D 정밀 기하학 구성 (12.8 x 7.5 와이드) ---
fig, ax = plt.subplots(figsize=(12.8, 7.5))
fig.subplots_adjust(left=0.02, right=0.65, bottom=0.04, top=0.96)
ax.set_facecolor('#ebf5fb')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-12, 28)
ax.set_ylim(-14, 15)

# 단위벡터 정의 (교재와 100% 일치하는 투영 평면)
ang_ax = np.radians(20.0)
e_X = np.array([np.cos(ang_ax), np.sin(ang_ax)]) # 원통 축 방향 (좌하단 -> 우상단 20도)
ang_Y = np.radians(-35.0)
e_Y = np.array([np.cos(ang_Y), np.sin(ang_Y)])   # 수평 앞쪽 방향 (우하단 -35도)
e_Z = np.array([0.0, 1.0])                       # 수직 위쪽 방향

xA = 16.0    # 점 A의 중심축 위치
L_cyl = 23.0 # 원통 총 길이

def to_2d(X, Y, Z):
    return X * e_X[0] + Y * e_Y[0] + Z * e_Z[0], X * e_X[1] + Y * e_Y[1] + Z * e_Z[1]

# (1) 원통 본체 서피스 렌더링
th_sample = np.linspace(0, 2*np.pi, 100)
xl_rim, yl_rim = to_2d(0, r_cyl*np.cos(th_sample), r_cyl*np.sin(th_sample))
xr_rim, yr_rim = to_2d(L_cyl, r_cyl*np.cos(th_sample), r_cyl*np.sin(th_sample))

xt_l, yt_l = to_2d(0, 0, r_cyl)
xt_r, yt_r = to_2d(L_cyl, 0, r_cyl)
xb_l, yb_l = to_2d(0, 0, -r_cyl)
xb_r, yb_r = to_2d(L_cyl, 0, -r_cyl)

# 원통 바디
cyl_poly = patches.Polygon([[xt_l, yt_l], [xt_r, yt_r], [xb_r, yb_r], [xb_l, yb_l]],
                           facecolor='#e1f1fa', edgecolor='#aed6f1', lw=1.2, alpha=0.55, zorder=1)
ax.add_patch(cyl_poly)

# 좌측 원형 단면 타원 캡
cap_poly = patches.Polygon(np.column_stack([xl_rim, yl_rim]),
                           facecolor='#c7e4f7', edgecolor='#7fb3d5', lw=1.6, alpha=0.75, zorder=2)
ax.add_patch(cap_poly)

# 우측 림 및 외곽선
ax.plot(xr_rim, yr_rim, color='#aed6f1', lw=1.2, zorder=2)
ax.plot([xt_l, xt_r], [yt_l, yt_r], color='#aed6f1', lw=1.2, zorder=2)
ax.plot([xb_l, xb_r], [yb_l, yb_r], color='#aed6f1', lw=1.2, zorder=2)

# (2) 중심 축선 (파선 및 "수평" 라벨)
ax_s_x, ax_s_y = to_2d(-4, 0, 0)
ax_e_x, ax_e_y = to_2d(L_cyl + 4, 0, 0)
ax.plot([ax_s_x, ax_e_x], [ax_s_y, ax_e_y], 'k--', lw=1.2, alpha=0.75, zorder=3)

t1_x, t1_y = to_2d(7.0, 0, 0)
t2_x, t2_y = to_2d(12.5, 0, 0)
ax.text(t1_x, t1_y + 0.6, '수평', fontsize=11, color='#2c3e50', ha='center', va='bottom')
ax.text(t2_x, t2_y + 0.6, '수평', fontsize=11, color='#2c3e50', ha='center', va='bottom')

# (3) 좌측 단면 기준선 및 5 m 치수선
zv_top_x, zv_top_y = to_2d(0, 0, r_cyl + 2.5)
zv_bot_x, zv_bot_y = to_2d(0, 0, -r_cyl - 2.5)
ax.plot([zv_top_x, zv_bot_x], [zv_top_y, zv_bot_y], 'k-.', lw=1.0, alpha=0.7, zorder=3)

yh_x, yh_y = to_2d(0, r_cyl, 0)
ax.plot([0, yh_x], [0, yh_y], 'k--', lw=1.0, alpha=0.7, zorder=3)
ax.text(yh_x*0.5 + 0.3, yh_y*0.5 + 0.6, '수평', fontsize=10, color='#2c3e50')

d_s_x, d_s_y = to_2d(0, 0, 0)
d_e_x, d_e_y = to_2d(0, 0, -r_cyl)
ax.annotate('', xy=(d_e_x + 0.6, d_e_y), xytext=(d_s_x + 0.6, d_s_y),
            arrowprops=dict(arrowstyle='<->,head_width=0.15,head_length=0.35', color='black', lw=0.8, mutation_scale=8), zorder=4)
ax.plot([d_s_x + 0.2, d_s_x + 1.0], [d_s_y, d_s_y], 'k-', lw=0.8, zorder=4)
ax.plot([d_e_x + 0.2, d_e_x + 1.0], [d_e_y, d_e_y], 'k-', lw=0.8, zorder=4)
ax.text(d_s_x + 1.3, (d_s_y + d_e_y)*0.5, '$5\\text{ m}$', fontsize=11, va='center', color='#2c3e50')

# (4) 점 A (교재와 100% 동일: 중심축 xA에서 수평선 방향 r_cyl 위치)
pA_x, pA_y = to_2d(xA, r_cyl, 0)
pAc_x, pAc_y = to_2d(xA, 0, 0)
ax.plot([pAc_x, pA_x], [pAc_y, pA_y], 'k--', lw=1.0, alpha=0.7, zorder=3)
ax.plot([pA_x], [pA_y], 'ko', markersize=6.5, zorder=10)
ax.text(pA_x + 0.4, pA_y + 0.6, '$A$', fontsize=15, fontfamily='serif', fontweight='bold', color='#1a5276', zorder=10)

# 점 A 수직선
v_top_x, v_top_y = to_2d(xA, r_cyl, 1.8)
v_bot_x, v_bot_y = to_2d(xA, r_cyl, -5.2)
ax.plot([v_top_x, v_bot_x], [v_top_y, v_bot_y], 'k-', lw=1.0, alpha=0.75, zorder=4)
ax.text(v_bot_x - 0.2, v_bot_y - 0.5, '수직', fontsize=11, ha='right', va='top', color='#2c3e50')

# 점 A에서의 접선 단위벡터
u_tang_2d = np.sin(gamma_rad) * e_X - np.cos(gamma_rad) * e_Z
tang_s = np.array([pA_x, pA_y]) - 2.5 * u_tang_2d
tang_e = np.array([pA_x, pA_y]) + 4.8 * u_tang_2d
ax.plot([tang_s[0], tang_e[0]], [tang_s[1], tang_e[1]], 'k:', lw=1.0, zorder=4)

# gamma = 40 deg 각도 호
arc_x = pA_x + 3.4 * np.sin(np.linspace(0, gamma_rad, 20)) * e_X[0]
arc_y = pA_y + 3.4 * np.sin(np.linspace(0, gamma_rad, 20)) * e_X[1] - 3.4 * np.cos(np.linspace(0, gamma_rad, 20))
ax.plot(arc_x, arc_y, 'k-', lw=1.0, zorder=4)
ax.text(pA_x + 1.8, pA_y - 4.0, r'$\gamma = 40^\circ$', fontsize=11, fontweight='bold', color='#2c3e50')

# (5) 나선 레일 전체 궤적 (교재와 100% 동일한 시작점과 끝점)
# 시작점: 좌측 림 (th = 1.18 pi) -> 꼭대기 (th = 0.5 pi) -> 점 A (th = 0) -> 바닥 (th = -0.45 pi)
th_rail = np.linspace(1.18 * np.pi, -0.45 * np.pi, 300)
X_rail = xA - r_cyl * np.tan(gamma_rad) * th_rail
Y_rail = r_cyl * np.cos(th_rail)
Z_rail = r_cyl * np.sin(th_rail)

r_2d_x, r_2d_y = to_2d(X_rail, Y_rail, Z_rail)
ax.plot(r_2d_x, r_2d_y, color='#7f8c8d', lw=2.8, alpha=0.9, zorder=5)

# 레일 시작점 마커
ax.plot([r_2d_x[0]], [r_2d_y[0]], 'o', color='#7f8c8d', markersize=3.5, zorder=6)

# 교재의 초록색 진행 화살표 (th = 0.35 pi 인근)
idx_arr = 160
p_arr_tail = np.array([r_2d_x[idx_arr], r_2d_y[idx_arr]]) + np.array([0.9, 0.9])
p_arr_head = p_arr_tail + 2.8 * u_tang_2d
ax.annotate('', xy=(p_arr_head[0], p_arr_head[1]), xytext=(p_arr_tail[0], p_arr_tail[1]),
            arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.45', color='#27ae60', lw=2.0, mutation_scale=10), zorder=6)

# 우측 정보 패널 (우측 전용 영역 0.66 ~ 0.98)
info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

dynamic_artists = []

# 애니메이션: 차량이 좌측 시작점(th = 1.10 pi)에서 출발하여 점 A(th = 0.0)까지 전체 주행!
frames = 110
th_cars = np.linspace(1.10 * np.pi, 0.0, frames)

def animate(i):
    global dynamic_artists
    for art in dynamic_artists:
        art.remove()
    dynamic_artists.clear()

    th_c = th_cars[i]
    
    # 4연속 롤러코스터 객차 (빨간색 블록)
    for k in range(5):
        d_th = (k - 2) * 0.08
        th_k = th_c + d_th
        X_k = xA - r_cyl * np.tan(gamma_rad) * th_k
        Y_k = r_cyl * np.cos(th_k)
        Z_k = r_cyl * np.sin(th_k)
        cx, cy = to_2d(X_k, Y_k, Z_k)
        
        # 차량 진행 방향 각도
        # 접선 벡터: sin(gamma)*e_X - cos(gamma)*sin(th)*e_Y - cos(gamma)*cos(th)*e_Z
        tang_k_2d = np.sin(gamma_rad)*e_X - np.cos(gamma_rad)*np.sin(th_k)*e_Y - np.cos(gamma_rad)*np.cos(th_k)*e_Z
        ang_k_deg = np.degrees(np.arctan2(tang_k_2d[1], tang_k_2d[0]))

        box = patches.Rectangle((cx - 0.45, cy - 0.35), 0.9, 0.7, angle=ang_k_deg,
                                facecolor='#e74c3c', edgecolor='#78281f', lw=1.2, zorder=8)
        ax.add_patch(box)
        dynamic_artists.append(box)

    # 선두 차량 위치
    X_head = xA - r_cyl * np.tan(gamma_rad) * th_c
    Y_head = r_cyl * np.cos(th_c)
    Z_head = r_cyl * np.sin(th_c)
    p_head_x, p_head_y = to_2d(X_head, Y_head, Z_head)

    # 접선 및 법선 단위벡터 (2D 투영)
    tang_head = np.sin(gamma_rad)*e_X - np.cos(gamma_rad)*np.sin(th_c)*e_Y - np.cos(gamma_rad)*np.cos(th_c)*e_Z
    norm_head = -np.cos(th_c)*e_Y - np.sin(th_c)*e_Z

    v_scale = 0.22
    v_patch = patches.FancyArrowPatch((p_head_x, p_head_y),
                                      (p_head_x + v_A * tang_head[0] * v_scale, p_head_y + v_A * tang_head[1] * v_scale),
                                      arrowstyle='->,head_width=0.25,head_length=0.45', color='#27ae60', lw=2.4, mutation_scale=10, zorder=12)
    ax.add_patch(v_patch)
    txt_v = ax.text(p_head_x + v_A * tang_head[0] * v_scale + 0.4, p_head_y + v_A * tang_head[1] * v_scale,
                    r'$\mathbf{v}$', color='#27ae60', fontsize=12, fontweight='bold', va='center')
    dynamic_artists.extend([v_patch, txt_v])

    a_scale = 0.12
    a_tot_2d = at_A * tang_head + an_A * norm_head
    a_patch = patches.FancyArrowPatch((p_head_x, p_head_y),
                                      (p_head_x + a_tot_2d[0] * a_scale, p_head_y + a_tot_2d[1] * a_scale),
                                      arrowstyle='->,head_width=0.25,head_length=0.45', color='#c0392b', lw=2.4, mutation_scale=10, zorder=12)
    ax.add_patch(a_patch)
    txt_a = ax.text(p_head_x + a_tot_2d[0] * a_scale + 0.4, p_head_y + a_tot_2d[1] * a_scale,
                    r'$\mathbf{a}$', color='#c0392b', fontsize=12, fontweight='bold', va='center')
    dynamic_artists.extend([a_patch, txt_a])

    is_final = (i == frames - 1)
    status_hdr = "★ [과제 과업 및 최종 정답 (점 A 도달 순간)] ★" if is_final else "■ [문제 2/135: 코르크 스크루 나선 운동]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【시스템 기하 및 조건】\n"
        f" • 원통 유효반지름: $r = {r_cyl:.1f}$ m\n"
        f" • 나선각: $\\gamma = {gamma_deg:.1f}^\\circ$\n"
        f" • 점 A에서의 속력: $v = {v_A:.1f}$ m/s\n"
        f" • 접선 가속도 성분: $a_t = g\\cos\\gamma$\n"
        f"─────────────────────────────────────\n"
        f"【실시간 운동 상태 (Monitoring)】\n"
        f" • 주행 위치: $\\theta = {np.degrees(th_c):.1f}^\\circ$ ($\\rightarrow$ 목표 점 A: $0^\\circ$)\n"
        f" • 차량 속력: $|\\mathbf{{v}}| = {v_A:.1f}$ m/s  (녹색 벡터)\n"
        f" • 가속도 크기: $|\\mathbf{{a}}| = {a_mag_A:.2f}$ m/s² ({a_mag_A/g:.2f} G, 적색)\n"
        f"─────────────────────────────────────\n"
        f"▶ 【풀이 핵심 힌트 (Hint)】\n"
        f" • 원통나선 곡률반지름 공식: $\\rho = \\frac{{r}}{{\\cos^2\\gamma}}$\n"
        f" • 접선방향 가속도: $a_t = g\\cos\\gamma$\n"
        f" • 법선방향 가속도: $a_n = \\frac{{v^2}}{{\\rho}}$\n"
        f" • 총 가속도 크기: $|a| = \\sqrt{{a_t^2 + a_n^2}}$\n"
        f"─────────────────────────────────────\n"
        f"★ 【최종 정답 (점 A 통과 순간)】\n"
        f" • 곡률반지름: $\\rho = 8.520$ m\n"
        f" • 접선 가속도: $a_t = 7.515$ m/s²\n"
        f" • 법선 가속도: $a_n = 26.407$ m/s²\n"
        f" • 총 가속도 크기: $|a| = 27.46$ m/s² ($2.80$ G)"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)

gif_path = Path(__file__).parent / 'prob2_135_corkscrew.gif'
writer = PillowWriter(fps=28)
writer._kwargs = {'loop': None}

print(f"GIF 애니메이션을 {gif_path} 파일로 렌더링 중...")
ani.save(str(gif_path), writer=writer)
print(f"GIF 저장 성공: {gif_path}")

try:
    from PIL import Image
    im = Image.open(str(gif_path))
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 35))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(str(gif_path), save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("마지막 프레임 60초 대기 및 1회 재생(loop=1) 적용 완료!")
except Exception as e:
    print(f"딜레이 패치 실패: {e}")
