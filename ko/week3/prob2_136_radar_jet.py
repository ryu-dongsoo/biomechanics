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

# 문제 2/136: 레이더의 제트기 추적과 구면좌표계(R-θ-φ) 속도 성분 분해
# 고도 h, 수평 오프셋 b, 수평 속력 u 제트기 추적 3D 시뮬레이션 (과제 힌트 및 정답 모드)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 물리 및 기하학적 매개변수 설정 ---
# 고도 h = 4.0 km, 수평 이격거리 b = 3.0 km, 수평 비행속도 u = 0.8 km/s (800 m/s)
h = 4.0
b = 3.0
u = 0.8 # km/s

# 시간 범위 (t = -4.0 s ~ +4.0 s)
t_start = -4.0
t_end = 4.0
frames = 100
t_arr = np.linspace(t_start, t_end, frames)
y_arr = u * t_arr # y(t) = u * t

# 구면좌표계 변환 함수
def get_spherical_state(y):
    r_xy = np.sqrt(b**2 + y**2)
    R = np.sqrt(b**2 + y**2 + h**2)
    theta = np.arctan2(y, b)
    phi = np.arctan2(h, r_xy)

    # 구면 단위벡터
    er = np.array([np.cos(phi)*np.cos(theta), np.cos(phi)*np.sin(theta), np.sin(phi)])
    eth = np.array([-np.sin(theta), np.cos(theta), 0.0])
    ephi = np.array([-np.sin(phi)*np.cos(theta), -np.sin(phi)*np.sin(theta), np.cos(phi)])

    # 속도 구면 성분
    vR = u * np.cos(phi) * np.sin(theta)
    vth = u * np.cos(theta)
    vphi = -u * np.sin(phi) * np.sin(theta)

    return R, theta, phi, r_xy, er, eth, ephi, vR, vth, vphi

# --- 2. 캔버스 및 레이아웃 구성 (12.8 x 7.5 와이드) ---
fig = plt.figure(figsize=(12.8, 7.5))
ax = fig.add_axes([0.0, 0.02, 0.65, 0.96], projection='3d')
ax.set_facecolor('#ebf5fb')
ax.axis('off')

ax.set_xlim(-1, 5)
ax.set_ylim(-4.5, 4.5)
ax.set_zlim(-0.5, 5.5)
ax.set_box_aspect((1.2, 1.6, 1.1))
ax.view_init(elev=24, azim=-55)

# 축 및 기준선
ax.plot([0, 4.5], [0, 0], [0, 0], 'k--', lw=1.2, alpha=0.7)
ax.text(4.7, 0, 0, '$x$', fontsize=13, fontfamily='serif', fontstyle='italic', va='center')
ax.plot([0, 0], [-4.2, 4.2], [0, 0], 'k--', lw=1.2, alpha=0.7)
ax.text(0, 4.4, 0, '$y$', fontsize=13, fontfamily='serif', fontstyle='italic', va='center')
ax.plot([0, 0], [0, 0], [0, 5.0], 'k--', lw=1.2, alpha=0.7)
ax.text(0, 0, 5.2, '$z$', fontsize=13, fontfamily='serif', fontstyle='italic', ha='center')

# 제트기 비행 궤적선
ax.plot(np.full_like(y_arr, b), y_arr, np.full_like(y_arr, h), color='#e67e22', ls='--', lw=2.0, alpha=0.8, zorder=3)

# 지면 오프셋 기준선
ax.plot([0, b], [0, 0], [0, 0], color='#7f8c8d', ls='-', lw=1.2)
ax.plot([b, b], [-4.0, 4.0], [0, 0], color='#bdc3c7', ls=':', lw=1.0)

# 레이더 안테나 P 마커
ax.plot([0], [0], [0], 'ko', markersize=6, zorder=10)
ax.text(-0.3, -0.3, 0.2, '$P$', fontsize=15, fontfamily='serif', fontweight='bold', color='#1a5276')

# 제트기 모델링 헬퍼
def draw_jet(ax, pos, heading=1):
    x, y, z = pos
    pts = np.array([
        [0, 0.7*heading, 0],
        [-0.15, -0.6*heading, 0],
        [0.15, -0.6*heading, 0],
        [0, 0.7*heading, 0.1],
        [-0.9, -0.2*heading, 0],
        [0.9, -0.2*heading, 0],
        [0, -0.6*heading, 0.35]
    ])
    pts[:, 0] += x
    pts[:, 1] += y
    pts[:, 2] += z

    lines = []
    l1, = ax.plot([pts[0,0], pts[1,0], pts[2,0], pts[0,0]],
                  [pts[0,1], pts[1,1], pts[2,1], pts[0,1]],
                  [pts[0,2], pts[1,2], pts[2,2], pts[0,2]], color='#c0392b', lw=2.0)
    l2, = ax.plot([pts[4,0], pts[5,0]], [pts[4,1], pts[5,1]], [pts[4,2], pts[5,2]], color='#c0392b', lw=2.2)
    l3, = ax.plot([pts[2,0], pts[6,0], pts[1,0]], [pts[2,1], pts[6,1], pts[1,1]], [pts[2,2], pts[6,2], pts[1,2]], color='#c0392b', lw=1.8)
    lines.extend([l1, l2, l3])
    return lines

dynamic_artists = []
dynamic_tri_surf = []

# 우측 정보 패널 (우측 전용 영역 0.66 ~ 0.98)
info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    global dynamic_artists, dynamic_tri_surf
    for art in dynamic_artists:
        if isinstance(art, list):
            for sub in art: sub.remove()
        else:
            art.remove()
    for surf in dynamic_tri_surf:
        surf.remove()
    dynamic_artists.clear()
    dynamic_tri_surf.clear()

    y_c = y_arr[i]
    x_c = b
    z_c = h

    R, theta, phi, r_xy, er, eth, ephi, vR, vth, vphi = get_spherical_state(y_c)

    # 삼각 투영 평면
    tri_pts = np.array([[0, 0, 0], [x_c, y_c, 0], [x_c, y_c, z_c]])
    tri_poly = Poly3DCollection([tri_pts], facecolors='#f9e79f', edgecolors='#d4ac0d', alpha=0.35, lw=1.0)
    ax.add_collection3d(tri_poly)
    dynamic_tri_surf.append(tri_poly)

    # 시선 R 및 보조선
    line_R, = ax.plot([0, x_c], [0, y_c], [0, z_c], color='#e67e22', lw=2.2, ls='-', zorder=5)
    line_hproj, = ax.plot([0, x_c], [0, y_c], [0, 0], color='#7f8c8d', lw=1.2, ls=':', zorder=4)
    line_hvert, = ax.plot([x_c, x_c], [y_c, y_c], [0, z_c], color='#7f8c8d', lw=1.2, ls='--', zorder=4)
    txt_h_dim = ax.text(x_c + 0.15, y_c, z_c * 0.5, '$h$', fontsize=12, color='#2c3e50', fontstyle='italic')
    txt_b_dim = ax.text(b * 0.5, -0.4, 0, '$b$', fontsize=12, color='#2c3e50', fontstyle='italic')
    dynamic_artists.extend([line_R, line_hproj, line_hvert, txt_h_dim, txt_b_dim])

    # 방위각 theta 및 앙각 phi 호
    if abs(theta) > 0.05:
        th_samples = np.linspace(0, theta, 20)
        arc_th_x = 2.0 * np.cos(th_samples)
        arc_th_y = 2.0 * np.sin(th_samples)
        arc_th_z = np.zeros_like(th_samples)
        arc_th, = ax.plot(arc_th_x, arc_th_y, arc_th_z, color='#2980b9', lw=1.5, zorder=4)
        txt_th = ax.text(2.3*np.cos(theta/2), 2.3*np.sin(theta/2), 0, r'$\theta$', color='#2980b9', fontsize=12, fontweight='bold')
        dynamic_artists.extend([arc_th, txt_th])

    phi_samples = np.linspace(0, phi, 20)
    arc_phi_x = 2.5 * np.cos(phi_samples) * np.cos(theta)
    arc_phi_y = 2.5 * np.cos(phi_samples) * np.sin(theta)
    arc_phi_z = 2.5 * np.sin(phi_samples)
    arc_phi, = ax.plot(arc_phi_x, arc_phi_y, arc_phi_z, color='#8e44ad', lw=1.5, zorder=4)
    txt_phi = ax.text(2.8*np.cos(phi/2)*np.cos(theta), 2.8*np.cos(phi/2)*np.sin(theta), 2.8*np.sin(phi/2),
                      r'$\phi$', color='#8e44ad', fontsize=12, fontweight='bold')
    dynamic_artists.extend([arc_phi, txt_phi])

    # 제트기 A
    jet_parts = draw_jet(ax, (x_c, y_c, z_c), heading=1)
    txt_A = ax.text(x_c, y_c, z_c + 0.4, '$A$', fontsize=14, fontfamily='serif', fontweight='bold', color='#1a5276')
    dynamic_artists.append(jet_parts)
    dynamic_artists.append(txt_A)

    # 속도 벡터 v (녹색)
    v_scale = 2.2
    q_v = ax.quiver(x_c, y_c, z_c, 0, u*v_scale, 0, color='#27ae60', arrow_length_ratio=0.25, lw=2.4, zorder=12)
    txt_v = ax.text(x_c, y_c + u*v_scale + 0.3, z_c, r'$\mathbf{v} = u\mathbf{j}$', color='#27ae60', fontsize=11, fontweight='bold')
    dynamic_artists.extend([q_v, txt_v])

    is_final = (i == frames - 1)
    status_hdr = "★ [과제 과업 및 구면 속도 유도 정답] ★" if is_final else "■ [문제 2/136: 레이더 제트기 추적]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【시스템 기하 및 조건】\n"
        f" • 제트기 고도: $h = {h:.1f}$ km,  수평 이격거리: $b = {b:.1f}$ km\n"
        f" • 수평 비행속도: $\\mathbf{{v}} = u\\,\\hat{{\\mathbf{{j}}}}$  ($u = {u*1000:.0f}$ m/s)\n"
        f"─────────────────────────────────────\n"
        f"【실시간 구면좌표 상태 (Monitoring)】\n"
        f" • 위치: $y = {y_c:+.2f}$ km $\\rightarrow R = {R:.2f}$ km\n"
        f" • 방위각 $\\theta = {np.degrees(theta):+.1f}^\\circ$,  앙각 $\\phi = {np.degrees(phi):.1f}^\\circ$\n"
        f" • 실시간 속도 성분:\n"
        f"   - $v_R = {vR*1000:+.1f}$ m/s, $v_\\theta = {vth*1000:+.1f}$ m/s, $v_\\phi = {vphi*1000:+.1f}$ m/s\n"
        f"─────────────────────────────────────\n"
        f"▶ 【풀이 핵심 힌트 (Hint)】\n"
        f" • 구면 좌표계 위치 표현:\n"
        f"   $x = R\\cos\\phi\\cos\\theta = b,\\ y = R\\cos\\phi\\sin\\theta,\\ z = R\\sin\\phi = h$\n"
        f" • 속도 벡터 $\\mathbf{{v}} = u\\,\\hat{{\\mathbf{{j}}}}$와 구면 단위벡터 내적:\n"
        f"   - $v_R = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_R$\n"
        f"   - $v_\\theta = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_\\theta$\n"
        f"   - $v_\\phi = \\mathbf{{v}}\\cdot\\hat{{\\mathbf{{e}}}}_\\phi$\n"
        f"─────────────────────────────────────\n"
        f"★ 【구면좌표계 속도 성분 최종 정답】\n"
        f" (1) $v_R = u\\cos\\phi\\sin\\theta$\n"
        f" (2) $v_\\theta = u\\cos\\theta$\n"
        f" (3) $v_\\phi = -u\\sin\\phi\\sin\\theta$\n"
        f" ★ 속력 검증: $\\sqrt{{v_R^2 + v_\\theta^2 + v_\\phi^2}} = u$ (일치)"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)

gif_path = Path(__file__).parent / 'prob2_136_radar_jet.gif'
writer = PillowWriter(fps=25)
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
            durations.append(im.info.get('duration', 40))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(str(gif_path), save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("마지막 프레임 60초 대기 및 1회 재생(loop=1) 적용 완료!")
except Exception as e:
    print(f"딜레이 패치 실패: {e}")
