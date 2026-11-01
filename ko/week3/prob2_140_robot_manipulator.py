# 문제 2/140: 산업용 로봇의 원통좌표계(r-θ-z) 운동학
# 수직축 회전(omega), 수직 신축(h), 수평 신축(l) 로봇 암과 선단 P의 속도/가속도 실시간 3D 시뮬레이션 (과제 힌트 및 정답 모드)

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
# 고정 베이스 치수:
h0 = 0.8  # 고정 베이스 높이 (m)
l0 = 1.0  # 고정 수평 암 길이 (m)
omega = 1.2 # 일정 회전 각속도 (rad/s, \dot{\theta} = \omega, \ddot{\theta} = 0)

# 시간 함수 설정 (t = 0 ~ 2.5 s):
t_total = 2.5
frames = 100
t_arr = np.linspace(0, t_total, frames)

def get_state(t):
    h = 0.3 + 0.30 * t
    h_dot = 0.30
    h_ddot = 0.0

    l = 0.2 + 0.35 * t
    l_dot = 0.35
    l_ddot = 0.0

    theta = omega * t
    theta_dot = omega
    theta_ddot = 0.0

    r = l0 + l
    z = h0 + h

    vr = l_dot
    vth = r * omega
    vz = h_dot
    v_mag = np.sqrt(vr**2 + vth**2 + vz**2)

    ar = l_ddot - r * (omega**2)
    ath = r * theta_ddot + 2.0 * l_dot * omega
    az = h_ddot
    a_mag = np.sqrt(ar**2 + ath**2 + az**2)

    return h, h_dot, l, l_dot, theta, r, z, vr, vth, vz, v_mag, ar, ath, az, a_mag

def cylinder_mesh(cx, cy, radius, z_start, z_end, num_pts=16):
    z = np.linspace(z_start, z_end, 2)
    th = np.linspace(0, 2*np.pi, num_pts)
    Tg, Zg = np.meshgrid(th, z)
    Xg = cx + radius * np.cos(Tg)
    Yg = cy + radius * np.sin(Tg)
    return Xg, Yg, Zg

# 캔버스 및 레이아웃 설정 (12.8 x 7.5 와이드)
fig = plt.figure(figsize=(12.8, 7.5))
ax = fig.add_axes([0.0, 0.02, 0.65, 0.96], projection='3d')
ax.set_facecolor('#ebf5fb')
ax.axis('off')

ax.set_xlim(-1.6, 2.6)
ax.set_ylim(-2.2, 2.2)
ax.set_zlim(0, 3.2)
ax.set_box_aspect((1.2, 1.2, 0.95))
ax.view_init(elev=22, azim=-55)

# 1. 정적 베이스
bx, by, bz = cylinder_mesh(0, 0, 0.42, 0, h0)
ax.plot_surface(bx, by, bz, color='#d4ac0d', edgecolor='#b7950b', alpha=0.92, shade=True)

fx, fy, fz = cylinder_mesh(0, 0, 0.58, 0, 0.10)
ax.plot_surface(fx, fy, fz, color='#95a5a6', edgecolor='#7f8c8d', alpha=0.95, shade=True)

for ang in np.linspace(0, 2*np.pi, 12, endpoint=False):
    ax.plot([0.50*np.cos(ang)], [0.50*np.sin(ang)], [0.10], 'k.', markersize=4)

ax.plot([0, 0], [0, 0], [0, 3.1], 'k--', lw=1.2, alpha=0.7)
ax.text(0, 0, 3.15, '$z$', fontsize=13, fontfamily='serif', fontstyle='italic', ha='center', color='#2c3e50')

ax.plot([-0.7, -0.7], [0, 0], [0, h0], 'k-', lw=1.0, alpha=0.6)
ax.plot([-0.75, -0.65], [0, 0], [0, 0], 'k-', lw=1.0, alpha=0.6)
ax.plot([-0.75, -0.65], [0, 0], [h0, h0], 'k-', lw=1.0, alpha=0.6)
ax.text(-0.85, 0, h0*0.5, '$h_0$', fontsize=12, ha='right', va='center', color='#7f8c8d', fontstyle='italic')

dynamic_surfs = []
dynamic_lines = []
vector_artists = []

x_traj, y_traj, z_traj = [], [], []
for t in t_arr:
    _, _, _, _, th, r, z, _, _, _, _, _, _, _, _ = get_state(t)
    x_traj.append(r * np.cos(th))
    y_traj.append(r * np.sin(th))
    z_traj.append(z)

traj_line, = ax.plot([], [], [], color='#e67e22', lw=2.2, ls='--', alpha=0.85, zorder=5)

info_box = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                    bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    global dynamic_surfs, dynamic_lines, vector_artists
    for s in dynamic_surfs: s.remove()
    for l in dynamic_lines: l.remove()
    for v in vector_artists: v.remove()
    dynamic_surfs.clear()
    dynamic_lines.clear()
    vector_artists.clear()

    t = t_arr[i]
    h, h_dot, l, l_dot, theta, r, z, vr, vth, vz, v_mag, ar, ath, az, a_mag = get_state(t)

    # 수직 승강 샤프트
    sx, sy, sz = cylinder_mesh(0, 0, 0.22, h0, z)
    s_surf = ax.plot_surface(sx, sy, sz, color='#bdc3c7', edgecolor='#7f8c8d', alpha=0.95, shade=True)
    dynamic_surfs.append(s_surf)

    # 회전 화살표
    arc_th = np.linspace(theta - np.pi*0.4, theta + np.pi*0.4, 20)
    arc_r = 0.38
    arc_x = arc_r * np.cos(arc_th)
    arc_y = arc_r * np.sin(arc_th)
    arc_z = np.full_like(arc_th, h0 + 0.15)
    l_arc, = ax.plot(arc_x, arc_y, arc_z, color='#27ae60', lw=2.2)
    txt_om = ax.text(arc_x[-1], arc_y[-1], arc_z[-1], r'$\omega$', color='#27ae60', fontsize=13, fontweight='bold')
    dynamic_lines.extend([l_arc, txt_om])

    # 상단 허브 블록
    bw, bd, bh = 0.50, 0.45, 0.36
    corners_local = np.array([
        [-bw/2, -bd/2, -bh/2],
        [ bw/2, -bd/2, -bh/2],
        [ bw/2,  bd/2, -bh/2],
        [-bw/2,  bd/2, -bh/2],
        [-bw/2, -bd/2,  bh/2],
        [ bw/2, -bd/2,  bh/2],
        [ bw/2,  bd/2,  bh/2],
        [-bw/2,  bd/2,  bh/2]
    ])
    R_z = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])
    corners_rot = (corners_local @ R_z.T) + np.array([0, 0, z])
    faces = [
        [corners_rot[0], corners_rot[1], corners_rot[5], corners_rot[4]],
        [corners_rot[1], corners_rot[2], corners_rot[6], corners_rot[5]],
        [corners_rot[2], corners_rot[3], corners_rot[7], corners_rot[6]],
        [corners_rot[3], corners_rot[0], corners_rot[4], corners_rot[7]],
        [corners_rot[0], corners_rot[1], corners_rot[2], corners_rot[3]],
        [corners_rot[4], corners_rot[5], corners_rot[6], corners_rot[7]]
    ]
    block_coll = Poly3DCollection(faces, facecolors='#5dade2', edgecolors='#2980b9', alpha=0.85, lw=1.2)
    ax.add_collection3d(block_coll)
    dynamic_surfs.append(block_coll)

    # 수평 붐
    er = np.array([np.cos(theta), np.sin(theta), 0])
    eth = np.array([-np.sin(theta), np.cos(theta), 0])
    ez = np.array([0, 0, 1])

    s_boom = np.linspace(0.22, l0, 10)
    th_b = np.linspace(0, 2*np.pi, 12)
    Sg, Tg = np.meshgrid(s_boom, th_b)
    Xb = Sg * er[0] + 0.18 * np.cos(Tg) * eth[0]
    Yb = Sg * er[1] + 0.18 * np.cos(Tg) * eth[1]
    Zb = z + 0.18 * np.sin(Tg)
    boom_surf = ax.plot_surface(Xb, Yb, Zb, color='#f39c12', edgecolor='#d68910', alpha=0.92, shade=True)
    dynamic_surfs.append(boom_surf)

    # 텔레스코픽 로드
    s_rod = np.linspace(l0 - 0.05, r - 0.10, 8)
    Sr, Tr = np.meshgrid(s_rod, th_b)
    Xr = Sr * er[0] + 0.09 * np.cos(Tr) * eth[0]
    Yr = Sr * er[1] + 0.09 * np.cos(Tr) * eth[1]
    Zr = z + 0.09 * np.sin(Tr)
    rod_surf = ax.plot_surface(Xr, Yr, Zr, color='#ecf0f1', edgecolor='#bdc3c7', alpha=0.98, shade=True)
    dynamic_surfs.append(rod_surf)

    # 끝점 P
    Px, Py, Pz = r * er[0], r * er[1], z
    p_dot, = ax.plot([Px], [Py], [Pz], 'ko', markersize=5.5, zorder=10)
    txt_P = ax.text(Px + 0.12*er[0], Py + 0.12*er[1], Pz, '$P$', fontsize=14, fontfamily='serif', fontweight='bold', color='#1a5276')
    vector_artists.extend([p_dot, txt_P])

    traj_line.set_data(x_traj[:i+1], y_traj[:i+1])
    traj_line.set_3d_properties(z_traj[:i+1])

    # 벡터 화살표
    v_vec = vr * er + vth * eth + vz * ez
    v_scale = 0.32
    q_v = ax.quiver(Px, Py, Pz, v_vec[0]*v_scale, v_vec[1]*v_scale, v_vec[2]*v_scale,
                    color='#27ae60', arrow_length_ratio=0.25, lw=2.4, zorder=12)
    txt_v = ax.text(Px + v_vec[0]*v_scale + 0.08, Py + v_vec[1]*v_scale + 0.08, Pz + v_vec[2]*v_scale,
                    r'$\mathbf{v}$', color='#27ae60', fontsize=12, fontweight='bold')

    a_vec = ar * er + ath * eth + az * ez
    a_scale = 0.16
    q_a = ax.quiver(Px, Py, Pz, a_vec[0]*a_scale, a_vec[1]*a_scale, a_vec[2]*a_scale,
                    color='#c0392b', arrow_length_ratio=0.25, lw=2.4, zorder=12)
    txt_a = ax.text(Px + a_vec[0]*a_scale + 0.08, Py + a_vec[1]*a_scale + 0.08, Pz + a_vec[2]*a_scale,
                    r'$\mathbf{a}$', color='#c0392b', fontsize=12, fontweight='bold')
    
    vector_artists.extend([q_v, txt_v, q_a, txt_a])

    # 치수선
    l_h_dim, = ax.plot([-0.7, -0.7], [0, 0], [h0, z], 'b-', lw=1.0, alpha=0.6)
    l_h_top, = ax.plot([-0.75, -0.65], [0, 0], [z, z], 'b-', lw=1.0, alpha=0.6)
    txt_h = ax.text(-0.85, 0, (h0+z)*0.5, '$h$', fontsize=12, ha='right', va='center', color='#2980b9', fontstyle='italic')
    dynamic_lines.extend([l_h_dim, l_h_top, txt_h])

    p_boom_end = l0 * er + np.array([0, 0, z + 0.35])
    p_P_dim = r * er + np.array([0, 0, z + 0.35])
    l_l_dim, = ax.plot([p_boom_end[0], p_P_dim[0]], [p_boom_end[1], p_P_dim[1]], [p_boom_end[2], p_P_dim[2]], 'k-', lw=1.0, alpha=0.6)
    txt_l = ax.text(0.5*(p_boom_end[0]+p_P_dim[0]), 0.5*(p_boom_end[1]+p_P_dim[1]), p_boom_end[2]+0.06, '$l$',
                    fontsize=12, ha='center', color='#2c3e50', fontstyle='italic')
    dynamic_lines.extend([l_l_dim, txt_l])

    is_final = (i == frames - 1)
    status_hdr = "★ [과제 과업 및 일반 해석 정답] ★" if is_final else "■ [문제 2/140: 산업용 로봇 기구학]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【시스템 기하 및 조건】\n"
        f" • 고정 치수: $h_0 = {h0:.1f}$ m,  $l_0 = {l0:.1f}$ m\n"
        f" • 회전 각속도: $\\omega = {omega:.1f}$ rad/s (일정, $\\ddot{{\\theta}}=0$)\n"
        f" • 신축 변위: $h(t)$, $l(t)$ (시간의 함수)\n"
        f"─────────────────────────────────────\n"
        f"【실시간 운동 상태 (Monitoring)】\n"
        f" • 위치: $r(t) = {r:.2f}$ m, $z(t) = {z:.2f}$ m ($\\theta = {np.degrees(theta):.1f}^\\circ$)\n"
        f" • 선단 P 속력: $|\\mathbf{{v}}| = {v_mag:.2f}$ m/s  (녹색 벡터)\n"
        f" • 선단 P 가속도: $|\\mathbf{{a}}| = {a_mag:.2f}$ m/s² (적색 벡터)\n"
        f"─────────────────────────────────────\n"
        f"▶ 【풀이 핵심 힌트 (Hint)】\n"
        f" • $\\mathbf{{v}} = \\dot{{r}}\\,\\hat{{\\mathbf{{e}}}}_r + r\\dot{{\\theta}}\\,\\hat{{\\mathbf{{e}}}}_\\theta + \\dot{{z}}\\,\\hat{{\\mathbf{{e}}}}_z$\n"
        f" • $\\mathbf{{a}} = (\\ddot{{r}} - r\\dot{{\\theta}}^2)\\,\\hat{{\\mathbf{{e}}}}_r\n"
        f"        + (r\\ddot{{\\theta}} + 2\\dot{{r}}\\dot{{\\theta}})\\,\\hat{{\\mathbf{{e}}}}_\\theta + \\ddot{{z}}\\,\\hat{{\\mathbf{{e}}}}_z$\n"
        f" • $r = l_0+l,\\ \\dot{{\\theta}}=\\omega,\\ z=h_0+h$ 관계를 대입하여 정리!\n"
        f"─────────────────────────────────────\n"
        f"★ 【속도 및 가속도 크기 최종 정답 (일반식)】\n"
        f" • 속력: $v = \\sqrt{{\\dot{{l}}^2 + (l_0+l)^2\\omega^2 + \\dot{{h}}^2}}$\n"
        f" • 가속도: $a = \\sqrt{{[\\ddot{{l}}-(l_0+l)\\omega^2]^2 + (2\\dot{{l}}\\omega)^2 + \\ddot{{h}}^2}}$"
    )
    info_box.set_text(info_str)
    if is_final:
        info_box.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_box.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)

gif_path = Path(__file__).parent / 'prob2_140_robot_manipulator.gif'
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
