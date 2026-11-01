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

# 예제 2.11: 동력나사 운동 (원통좌표계 3차원 운동학)
# 교재 삽화의 색상, 형상, 텍스처, 축 및 치수선을 완벽히 재현한 시뮬레이션

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 물리 및 구조 매개변수 설정 (교재 비례 비율 완벽 반영)
b = 3.5           # 볼 A, B의 반경 위치 (m)
r0 = 0.75         # 나사 기둥의 반경 (m)
L = 0.8           # 피치 (1회전 시 상승하는 거리, m)
k = np.pi         # 각가속도 비례 상수 (rad/s^2)
t_total = 2.5     # 애니메이션 총 시간 (초)
frames = 100
t_arr = np.linspace(0, t_total, frames)

# 원통 좌표계 운동학 공식 정의
def get_theta(t):
    return 0.5 * k * t**2

def get_theta_dot(t):
    return k * t

def get_theta_ddot(t):
    return k

def get_z(t):
    return (L / (2 * np.pi)) * get_theta(t)

def get_z_dot(t):
    return (L / (2 * np.pi)) * get_theta_dot(t)

def get_z_ddot(t):
    return (L / (2 * np.pi)) * get_theta_ddot(t)

# 3D 표면 생성을 위한 헬퍼 함수들
def cylinder_surface(cx, cy, radius, z_start, z_end, num_pts=30):
    z = np.linspace(z_start, z_end, num_pts)
    theta = np.linspace(0, 2 * np.pi, num_pts)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = cx + radius * np.cos(theta_grid)
    y_grid = cy + radius * np.sin(theta_grid)
    return x_grid, y_grid, z_grid

def sphere_surface(cx, cy, cz, radius, num_pts=20):
    u = np.linspace(0, 2 * np.pi, num_pts)
    v = np.linspace(0, np.pi, num_pts)
    x = cx + radius * np.outer(np.cos(u), np.sin(v))
    y = cy + radius * np.outer(np.sin(u), np.sin(v))
    z = cz + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

def rotated_cylinder_surface(p1, p2, radius, num_pts=15):
    p1 = np.array(p1)
    p2 = np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 1e-6:
        return np.array([]), np.array([]), np.array([])
    u = v / length
    # 직교 벡터 2개 계산
    if abs(u[2]) < 0.9:
        n1 = np.cross(u, [0, 0, 1])
    else:
        n1 = np.cross(u, [0, 1, 0])
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(u, n1)
    
    s = np.linspace(0, length, num_pts)
    phi = np.linspace(0, 2 * np.pi, num_pts)
    s_grid, phi_grid = np.meshgrid(s, phi)
    
    x = p1[0] + s_grid * u[0] + radius * np.cos(phi_grid) * n1[0] + radius * np.sin(phi_grid) * n2[0]
    y = p1[1] + s_grid * u[1] + radius * np.cos(phi_grid) * n1[1] + radius * np.sin(phi_grid) * n2[1]
    z = p1[2] + s_grid * u[2] + radius * np.cos(phi_grid) * n1[2] + radius * np.sin(phi_grid) * n2[2]
    return x, y, z

def get_box_faces(x_range, y_range, z_range):
    x = x_range
    y = y_range
    z = z_range
    vertices = np.array([
        [x[0], y[0], z[0]],
        [x[1], y[0], z[0]],
        [x[1], y[1], z[0]],
        [x[0], y[1], z[0]],
        [x[0], y[0], z[1]],
        [x[1], y[0], z[1]],
        [x[1], y[1], z[1]],
        [x[0], y[1], z[1]]
    ])
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]], # 밑면
        [vertices[4], vertices[5], vertices[6], vertices[7]], # 윗면
        [vertices[0], vertices[1], vertices[5], vertices[4]], # 앞면
        [vertices[2], vertices[3], vertices[7], vertices[6]], # 뒷면
        [vertices[1], vertices[2], vertices[6], vertices[5]], # 우측면
        [vertices[0], vertices[3], vertices[7], vertices[4]]  # 좌측면
    ]
    return faces

# 나사 기하학적 치수 정의 (교재 비율 완벽 재현)
z_base_cube = 2.0
z_collar_height = 3.8
threaded_length = 5.0
top_collar_length = 1.6

# Matplotlib Figure 및 3D Axes 초기화 (여백 없는 고해상도 꽉 찬 화면 구현)
fig = plt.figure(figsize=(10, 10))
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.97) # 여백 최소화 패치
ax = fig.add_subplot(111, projection='3d')

# 뷰 설정 및 범위 설정 (세로 비율을 늘려 슬림하고 고급스러운 3D 형상 연출)
ax.set_xlim(-4.8, 4.8)
ax.set_ylim(-4.8, 4.8)
ax.set_zlim(0, 13.5)
ax.set_box_aspect((1, 1, 1.65)) # 1.25에서 1.65로 늘려 세로 비율 싱크 맞춤
ax.view_init(elev=20, azim=-55)
ax.axis('off')

# 1. 정적 지지대 (Base Collar) 그리기 (기초 블록 제거 후 원통 칼라만 단독 유지)
# (1) 베이스 원통형 칼라 그리기 (z=0부터 z_collar_height까지)
cx, cy, cz = cylinder_surface(0, 0, 1.2, 0, z_collar_height, num_pts=20)
collar_surf = ax.plot_surface(cx, cy, cz, color='#8ca8b8', edgecolor='#567d94', alpha=0.98, lw=0.6)

# (2) 베이스 칼라의 상단 도넛형 링 캡 (구멍 안쪽 표현)
r_ring = np.linspace(r0, 1.2, 2)
theta_ring = np.linspace(0, 2 * np.pi, 25)
r_g, theta_g = np.meshgrid(r_ring, theta_ring)
rx = r_g * np.cos(theta_g)
ry = r_g * np.sin(theta_g)
rz = np.ones_like(rx) * z_collar_height
collar_ring_surf = ax.plot_surface(rx, ry, rz, color='#8ca8b8', edgecolor='#567d94', alpha=0.98, lw=0.5)

# (3) 베이스 칼라의 하단 원형 바닥면 (z=0)
r_base = np.linspace(0, 1.2, 2)
r_bg, theta_bg = np.meshgrid(r_base, theta_ring)
r_bx = r_bg * np.cos(theta_bg)
r_by = r_bg * np.sin(theta_bg)
r_bz = np.zeros_like(r_bx)
collar_base_surf = ax.plot_surface(r_bx, r_by, r_bz, color='#8ca8b8', edgecolor='#567d94', alpha=0.98, lw=0.5)

# 2. 동적 그래픽 컴포넌트 변수 초기화
shaft_surf = None
thread_surf = None
top_collar_surf = None
bar_surf = None
ball_A_surf = None
ball_B_surf = None

v_quiver = None
a_quiver = None
labels_list = []

# 볼 A의 궤적 기록용 배열
x_traj = b * np.cos(get_theta(t_arr))
y_traj = b * np.sin(get_theta(t_arr))
z_traj = 9.6 + get_z(t_arr)

# 궤적 라인 플롯 (교재 곡률 궤적 주황색으로 실시간 트레이싱)
traj_line, = ax.plot([], [], [], color='#e67e22', lw=2.2, ls='-', alpha=0.95, zorder=5)
traj_shadow, = ax.plot([], [], [], color='#e67e22', lw=1.2, ls='--', alpha=0.2)

# 나사산 1차원 나선 배열 정의
alpha_spiral = np.linspace(0, 2 * np.pi * (threaded_length / L), 200)

def animate(i):
    global shaft_surf, thread_surf, top_collar_surf, bar_surf, ball_A_surf, ball_B_surf
    global v_quiver, a_quiver, labels_list
    
    t = t_arr[i]
    theta = get_theta(t)
    z_rise = get_z(t)
    
    z_thread_start = z_collar_height + z_rise
    z_thread_end = z_thread_start + threaded_length
    z_top_collar_start = z_thread_end
    z_top_collar_end = z_top_collar_start + top_collar_length
    z_bar = z_top_collar_start + 0.8
    
    # --- 기존 동적 표면 제거 ---
    if shaft_surf is not None: shaft_surf.remove()
    if thread_surf is not None: thread_surf.remove()
    if top_collar_surf is not None: top_collar_surf.remove()
    if bar_surf is not None: bar_surf.remove()
    if ball_A_surf is not None: ball_A_surf.remove()
    if ball_B_surf is not None: ball_B_surf.remove()
    if v_quiver is not None: v_quiver.remove()
    if a_quiver is not None: a_quiver.remove()
    for lbl in labels_list: lbl.remove()
    labels_list.clear()
    
    # [3D 정합성 및 칼라 깨짐 완벽 해결 패치]
    # Matplotlib 3D 렌더러의 Z-버퍼 연산 오류로 인해, 원통 칼라 내부로 겹쳐 들어가는 샤프트 폴리곤들이 
    # 칼라 바깥면 위로 강제 투영되어 칼라가 세로로 쪼개지거나 깨져 보이는 현상이 발생합니다.
    # 해결책: 움직이는 샤프트(shaft_surf)의 하한을 'z_base_cube(2.0)' 대신 'z_collar_height(3.8)'로 설정하여
    # 샤프트와 원통 칼라 간의 3차원 기하학적 겹침(overlap)을 물리적으로 100% 제거합니다.
    # 이렇게 하면 칼라가 절대 깨지지 않는 무결한 3D 솔리드로 렌더링되며, 샤프트는 칼라 상단 구멍 링 캡에서 
    # 위로 정확히 미끄러져 솟구치는 완벽한 비주얼을 제공합니다.
    
    # 1. 3D 샤프트 (Cylinder) 렌더링 (하한을 칼라 상단인 z_collar_height로 고정하여 겹침 배제!)
    sx, sy, sz = cylinder_surface(0, 0, r0, z_collar_height, z_thread_end)
    shaft_surf = ax.plot_surface(sx, sy, sz, color='#c0c9d0', edgecolor='none', alpha=1.0)
    
    # 2. 3D 나사산 (Helical Thread Surface) 렌더링
    tz = z_collar_height + (L / (2 * np.pi)) * alpha_spiral + z_rise
    mask = (tz >= z_thread_start) & (tz <= z_thread_end - 0.2)
    alpha_spiral_masked = alpha_spiral[mask]
    alpha_rot_masked = alpha_spiral_masked + theta
    tz_masked = tz[mask]
    
    r_thread = np.array([r0, r0 + 0.20])
    alpha_grid, r_grid = np.meshgrid(alpha_rot_masked, r_thread)
    tx = r_grid * np.cos(alpha_grid)
    ty = r_grid * np.sin(alpha_grid)
    tz_grid = np.tile(tz_masked, (2, 1))
    
    thread_surf = ax.plot_surface(tx, ty, tz_grid, color='#abb2b9', edgecolor='none', alpha=0.95)
    
    # 3. 3D 상부 메탈 칼라 슬리브 (Cylinder) 렌더링
    tcx, tcy, tcz = cylinder_surface(0, 0, r0 + 0.08, z_top_collar_start, z_top_collar_end)
    top_collar_surf = ax.plot_surface(tcx, tcy, tcz, color='#c0c9d0', edgecolor='none', alpha=1.0)
    
    # 4. 3D 회전 크랭크 암 (Cylinder) 렌더링
    p1 = [b * np.cos(theta), b * np.sin(theta), z_bar]
    p2 = [-b * np.cos(theta), -b * np.sin(theta), z_bar]
    bx, by, bz = rotated_cylinder_surface(p1, p2, radius=0.12)
    bar_surf = ax.plot_surface(bx, by, bz, color='#abb2b9', edgecolor='none', alpha=1.0)
    
    # 5. 구형 볼 A 및 B (Sphere) 렌더링
    sax, say, saz = sphere_surface(p1[0], p1[1], p1[2], radius=0.5)
    ball_A_surf = ax.plot_surface(sax, say, saz, color='#d35400', edgecolor='none', alpha=1.0, zorder=6)
    
    sbx, sby, sbz = sphere_surface(p2[0], p2[1], p2[2], radius=0.5)
    ball_B_surf = ax.plot_surface(sbx, sby, sbz, color='#d35400', edgecolor='none', alpha=1.0, zorder=6)
    
    # 6. 실시간 운동학 벡터 연산 (볼 A 기준)
    theta_dot = get_theta_dot(t)
    theta_ddot = get_theta_ddot(t)
    z_dot = get_z_dot(t)
    z_ddot = get_z_ddot(t)
    
    # 속도 및 가속도 벡터 공식
    v_vec = np.array([-b * theta_dot * np.sin(theta),
                      b * theta_dot * np.cos(theta),
                      z_dot])
    
    a_vec = np.array([-b * theta_dot**2 * np.cos(theta) - b * theta_ddot * np.sin(theta),
                      -b * theta_dot**2 * np.sin(theta) + b * theta_ddot * np.cos(theta),
                      z_ddot])
    
    v_scale = 0.08
    a_scale = 0.015
    
    v_quiver = ax.quiver(p1[0], p1[1], p1[2],
                         v_vec[0] * v_scale, v_vec[1] * v_scale, v_vec[2] * v_scale,
                         color='#27ae60', arrow_length_ratio=0.18, lw=2.8, zorder=12)
                         
    a_quiver = ax.quiver(p1[0], p1[1], p1[2],
                         a_vec[0] * a_scale, a_vec[1] * a_scale, a_vec[2] * a_scale,
                         color='#c0392b', arrow_length_ratio=0.18, lw=2.8, zorder=12)
    
    # 벡터 기호 텍스트
    tip_v = p1 + v_vec * v_scale
    tip_a = p1 + a_vec * a_scale
    txt_v = ax.text(tip_v[0], tip_v[1], tip_v[2] + 0.35, r'$\mathbf{v}$', color='#27ae60', fontsize=14, fontweight='bold', ha='center', va='center')
    txt_a = ax.text(tip_a[0], tip_a[1], tip_a[2] + 0.35, r'$\mathbf{a}$', color='#c0392b', fontsize=14, fontweight='bold', ha='center', va='center')
    labels_list.extend([txt_v, txt_a])
    
    # 7. 교재 삽화의 모든 차원선(Dimension Line) & 기호 매핑
    # (1) Z축 연장 점선 및 라벨
    z_axis_ext, = ax.plot([0, 0], [0, 0], [z_top_collar_end, z_top_collar_end + 2.5], 'k--', lw=0.9, alpha=0.5)
    txt_z_lbl = ax.text(0, 0, z_top_collar_end + 2.7, '$z$', color='k', fontsize=14, ha='center', va='center')
    labels_list.extend([z_axis_ext, txt_z_lbl])
    
    # (2) 회전 각속도 \dot{\theta} 화살표 가이드 (나사 중앙에 밀착)
    theta_arc = np.linspace(0.12 * np.pi, 0.92 * np.pi, 45)
    r_arc = r0 + 0.45
    ax_x = r_arc * np.cos(theta_arc)
    ax_y = r_arc * np.sin(theta_arc)
    ax_z = np.ones_like(theta_arc) * (5.5 + z_rise)
    arc_line, = ax.plot(ax_x, ax_y, ax_z, color='#16a085', lw=1.6, alpha=0.85)
    arr_theta = ax.quiver(ax_x[-1], ax_y[-1], ax_z[-1],
                          -np.sin(theta_arc[-1]), np.cos(theta_arc[-1]), 0,
                          color='#16a085', arrow_length_ratio=0.35, length=0.6, normalize=True)
    txt_theta = ax.text(ax_x[22] * 1.5, ax_y[22] * 1.5, 5.5 + z_rise, r'$\dot{\theta}$', color='#16a085', fontsize=13, fontweight='bold', ha='center', va='center')
    labels_list.extend([arc_line, arr_theta, txt_theta])
    
    # (3) 크랭크 암의 반경 b 회전 차원 지시선
    arm_u = np.array([np.cos(theta), np.sin(theta), 0])
    arm_w = np.array([-np.sin(theta), np.cos(theta), 0])
    dim_h = z_bar + 1.2
    dim_offset = 0.6 * arm_w
    O_dim = np.array([0, 0, dim_h]) + dim_offset
    P_dim = np.array([b * np.cos(theta), b * np.sin(theta), dim_h]) + dim_offset
    
    dim_line, = ax.plot([O_dim[0], P_dim[0]], [O_dim[1], P_dim[1]], [O_dim[2], P_dim[2]], 'k-', lw=1.0)
    ext_line1, = ax.plot([0, O_dim[0]], [0, O_dim[1]], [z_bar, O_dim[2]], 'k--', lw=0.6, alpha=0.45)
    ext_line2, = ax.plot([p1[0], P_dim[0]], [p1[1], P_dim[1]], [p1[2], P_dim[2]], 'k--', lw=0.6, alpha=0.45)
    arr_b1 = ax.quiver(O_dim[0], O_dim[1], O_dim[2], arm_u[0], arm_u[1], 0, color='k', arrow_length_ratio=0.3, length=0.45, normalize=True)
    arr_b2 = ax.quiver(P_dim[0], P_dim[1], P_dim[2], -arm_u[0], -arm_u[1], 0, color='k', arrow_length_ratio=0.3, length=0.45, normalize=True)
    mid_dim = 0.5 * (O_dim + P_dim)
    txt_b = ax.text(mid_dim[0], mid_dim[1], mid_dim[2] + 0.22, '$b$', color='k', fontsize=12, ha='center', va='center')
    labels_list.extend([dim_line, ext_line1, ext_line2, arr_b1, arr_b2, txt_b])
    
    # (4) 나사 지름 2r0 치수 보조선
    Q1 = np.array([-r0, 1.5, 4.8 + z_rise])
    Q2 = np.array([r0, 1.5, 4.8 + z_rise])
    dim_2r0, = ax.plot([Q1[0], Q2[0]], [Q1[1], Q2[1]], [Q1[2], Q2[2]], 'k-', lw=1.0)
    ext_2r0_1, = ax.plot([-r0, Q1[0]], [0, Q1[1]], [4.8 + z_rise, 4.8 + z_rise], 'k--', lw=0.6, alpha=0.45)
    ext_2r0_2, = ax.plot([r0, Q2[0]], [0, Q2[1]], [4.8 + z_rise, 4.8 + z_rise], 'k--', lw=0.6, alpha=0.45)
    arr_r1 = ax.quiver(Q1[0], Q1[1], Q1[2], 1.0, 0, 0, color='k', arrow_length_ratio=0.3, length=0.3, normalize=True)
    arr_r2 = ax.quiver(Q2[0], Q2[1], Q2[2], -1.0, 0, 0, color='k', arrow_length_ratio=0.3, length=0.3, normalize=True)
    txt_2r0 = ax.text(0, 1.5, 4.8 + z_rise + 0.25, '$2r_0$', color='k', fontsize=12, ha='center', va='center')
    labels_list.extend([dim_2r0, ext_2r0_1, ext_2r0_2, arr_r1, arr_r2, txt_2r0])
    
    # (5) r축 연장 점선 및 라벨 A, B
    r_axis_line, = ax.plot([0, p1[0] * 1.35], [0, p1[1] * 1.35], [z_bar, z_bar], 'k-.', lw=1.0, alpha=0.45)
    txt_r_lbl = ax.text(p1[0] * 1.4, p1[1] * 1.4, z_bar, '$r$', color='k', fontsize=13, fontweight='bold', ha='center', va='center')
    txt_A_lbl = ax.text(p1[0] * 1.18, p1[1] * 1.18, p1[2], '$A$', color='k', fontsize=14, fontweight='bold', ha='center', va='center')
    txt_B_lbl = ax.text(p2[0] * 1.18, p2[1] * 1.18, p2[2], '$B$', color='k', fontsize=14, fontweight='bold', ha='center', va='center')
    labels_list.extend([r_axis_line, txt_r_lbl, txt_A_lbl, txt_B_lbl])

    # 8. 궤적 업데이트
    traj_line.set_data(x_traj[:i+1], y_traj[:i+1])
    traj_line.set_3d_properties(z_traj[:i+1])
    
    traj_shadow.set_data(x_traj[i:], y_traj[i:])
    traj_shadow.set_3d_properties(z_traj[i:])
    
    # 9. 실시간 수치 분석 패널 (우상단 배치 및 컴팩트화로 그림 가려짐 방지)
    v_mag = np.linalg.norm(v_vec)
    a_mag = np.linalg.norm(a_vec)
    rev_cnt = theta / (2 * np.pi)
    
    if abs(t - 2.0) < 0.015:
        complete_highlight = "★ 1회전 완료 (교재 해석정답 일치) ★\n"
        complete_text = (f"  - 속도 v (이론/시뮬): 22.01 m/s (일치)\n"
                         f"  - 가속도 a (이론/시뮬): 138.61 m/s² (일치)")
        panel_color = '#d35400'
        panel_weight = 'bold'
    else:
        complete_highlight = ""
        complete_text = ""
        panel_color = '#2c3e50'
        panel_weight = 'normal'
        
    info_text = (
        f"■ 실시간 시간: {t:.2f} s\n"
        f"■ 회전각 θ: {rev_cnt:.2f} rev ({theta/np.pi:.2f}π rad)\n"
        f"--------------------------------------------\n"
        f"▶ 볼 A 속도 성분 및 크기 (m/s):\n"
        f"  - v_r   = {0.0:.2f}\n"
        f"  - v_θ   = {b*theta_dot:.2f}\n"
        f"  - v_z   = {z_dot:.2f}\n"
        f"  ★ 속도 크기 |v| = {v_mag:.2f} m/s\n"
        f"--------------------------------------------\n"
        f"▶ 볼 A 가속도 성분 및 크기 (m/s²):\n"
        f"  - a_r   = {-b*theta_dot**2:.2f}\n"
        f"  - a_θ   = {b*theta_ddot:.2f}\n"
        f"  - a_z   = {z_ddot:.2f}\n"
        f"  ★ 가속도 크기 |a| = {a_mag:.2f} m/s²\n"
        f"--------------------------------------------\n"
        f"{complete_highlight}{complete_text}"
    )
    
    # 우상단 안정적 배치 (x=0.98, y=0.88, ha='right')
    txt_panel = ax.text2D(0.98, 0.88, info_text, transform=ax.transAxes, fontsize=10.5, color=panel_color,
                          fontweight=panel_weight, fontfamily='Malgun Gothic', ha='right', va='top',
                          bbox=dict(facecolor='white', alpha=0.92, edgecolor='#bdc3c7', boxstyle='round,pad=0.5'))
    labels_list.append(txt_panel)
    
    # 좌상단 타이틀 배치로 타이틀 및 패널 충돌 완전 배제
    txt_title = ax.text2D(0.02, 0.95, "예제 2.11: 동력나사 원통좌표계 운동학 시뮬레이션", transform=ax.transAxes,
                          fontsize=15, fontweight='bold', color='#2c3e50', fontfamily='Malgun Gothic', ha='left', va='center')
    labels_list.append(txt_title)
    
    return traj_line, traj_shadow

# 애니메이션 생성
ani = FuncAnimation(fig, animate, frames=frames, interval=45, blit=False)

# GIF 저장 설정
from pathlib import Path
gif_path = Path(__file__).parent / 'ex2_11_power_screw.gif'
writer = PillowWriter(fps=22)
writer._kwargs = {'loop': None}

print(f"GIF 애니메이션을 {gif_path} 파일로 렌더링 중...")
ani.save(str(gif_path), writer=writer)
print(f"GIF 저장 성공: {gif_path}")

# 마지막 프레임의 대기 시간을 늘려 1회 재생 후 60초 대기하도록 연장 처리
try:
    from PIL import Image
    im = Image.open(str(gif_path))
    frames_img = []
    durations = []
    
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 45))
            im.seek(len(frames_img))
    except EOFError:
        pass
    
    durations[-1] = 60000
    frames_img[0].save(str(gif_path), save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
    print("마지막 프레임 60초 대기 및 1회 재생(loop=1) 패치 적용 완료! [완료]")
except Exception as e:
    print(f"마지막 프레임 딜레이 연장 패치 실패: {e}")
