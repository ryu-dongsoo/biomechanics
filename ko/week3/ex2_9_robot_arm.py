# 예제 2.9: 회전하는 로봇 팔 안의 슬라이더 (극좌표계 속도/가속도)
# 로봇 팔 거동과 궤적 그래프를 단일 좌표계로 통합

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from matplotlib.animation import FuncAnimation, PillowWriter

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 물리적 시뮬레이션 계산 ---
frames = 200
t_phys = np.linspace(0, 5.0, frames)
r_val = 0.2 + 0.04 * t_phys**2
theta_val = 0.2 * t_phys + 0.02 * t_phys**3

r_dot = 0.08 * t_phys
r_ddot = np.full_like(t_phys, 0.08)

theta_dot = 0.2 + 0.06 * t_phys**2
theta_ddot = 0.12 * t_phys

vr = r_dot
vth = r_val * theta_dot
v_mag = np.sqrt(vr**2 + vth**2)

ar = r_ddot - r_val * theta_dot**2
ath = r_val * theta_ddot + 2 * r_dot * theta_dot
a_mag = np.sqrt(ar**2 + ath**2)

# 데카르트 좌표계 궤적
x_full = r_val * np.cos(theta_val)
y_full = r_val * np.sin(theta_val)

# --- 단일 통합 캔버스 ---
fig, ax = plt.subplots(figsize=(12, 10))
fig.suptitle('예제 2.9: 로봇 팔 슬라이더의 극좌표 운동', fontsize=20, fontweight='bold', y=0.97)

ax.set_aspect('equal')
ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-0.8, 1.6)
ax.set_xticks([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
ax.set_yticks([-0.5, 0.0, 0.5, 1.0, 1.5])
ax.grid(True, color='#cccccc', lw=0.8)
ax.set_xlabel('$x$, m', fontsize=16, fontfamily='serif')
ax.set_ylabel('$y$, m', fontsize=16, fontfamily='serif', rotation=0, labelpad=25)
ax.set_facecolor('#fafafa')

# ===========================================
# 정적 배경: 답안 그래프 주석들
# ===========================================
# t=0 점 & 텍스트
x0, y0 = r_val[0] * np.cos(theta_val[0]), r_val[0] * np.sin(theta_val[0])
ax.plot(x0, y0, 'ko', markersize=7, zorder=15)
ax.annotate('$t = 0$', xy=(x0, y0), xytext=(x0 + 0.15, y0 - 0.15),
            fontsize=14, fontfamily='serif', ha='left', va='top',
            arrowprops=dict(arrowstyle='-', color='black', lw=1))

# t=3s 점 & 텍스트
idx3 = np.argmin(np.abs(t_phys - 3.0))
x3, y3 = x_full[idx3], y_full[idx3]
ax.plot(x3, y3, 'ko', markersize=7, zorder=15)
ax.annotate('$t = 3$ s', xy=(x3, y3), xytext=(x3 + 0.2, y3 + 0.15),
            fontsize=14, fontfamily='serif', ha='left',
            arrowprops=dict(arrowstyle='-', connectionstyle="arc3,rad=-0.2", color='black', lw=1))

# t=5s 점 & 텍스트
x5, y5 = x_full[-1], y_full[-1]
ax.plot(x5, y5, 'ko', markersize=7, zorder=15)
ax.text(x5 - 0.08, y5 + 0.06, '$t = 5$ s', fontsize=14, fontfamily='serif', ha='right', va='bottom')

# r3 치수선 (O에서 B(t=3)까지)
ax.plot([0, x3], [0, y3], 'k-', lw=1.2, zorder=4)
ax.text(x3/2 + 0.05, y3/2 + 0.08, '$r_3$', fontsize=16, fontfamily='serif', fontstyle='italic')

# r3, θ3 값 표시
r3_val = r_val[idx3]
th3_deg = np.degrees(theta_val[idx3])
ax.text(-0.55, 0.45, f'$r_3 = {r3_val:.2f}$ m', fontsize=14, fontfamily='serif',
        bbox=dict(facecolor='white', edgecolor='none', pad=2))
ax.text(-0.55, 0.32, f'$\\theta_3 = {th3_deg:.1f}^\\circ$', fontsize=14, fontfamily='serif',
        bbox=dict(facecolor='white', edgecolor='none', pad=2))

# θ3 각도 호
arc_th3 = patches.Arc((0, 0), 0.35, 0.35, angle=0, theta1=0,
                       theta2=np.degrees(theta_val[idx3]), color='black', lw=1.2, zorder=4)
ax.add_patch(arc_th3)
th3_arc_end = theta_val[idx3]
ax.annotate('', xy=(0.175*np.cos(th3_arc_end), 0.175*np.sin(th3_arc_end)),
            xytext=(0.175*np.cos(th3_arc_end - 0.15), 0.175*np.sin(th3_arc_end - 0.15)),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.text(0.22, 0.08, '$\\theta_3$', fontsize=14, fontfamily='serif', fontstyle='italic')

# ===========================================
# 동적 요소: 로봇 팔 메커니즘 (실축 좌표에 직접 그림)
# ===========================================

# 로봇 팔 본체 (반원형 뒤쪽 + 직사각형 앞쪽)
arm_length = 1.4  # max r 가 약 1.2이므로 넉넉하게
hw = 0.08  # 반폭

# 팔 외형 (로컬 좌표)
th_cap = np.linspace(np.pi/2, 3*np.pi/2, 20)
x_arm = np.concatenate([hw * np.cos(th_cap), [arm_length, arm_length]])
y_arm = np.concatenate([hw * np.sin(th_cap), [-hw*0.6, hw*0.6]])
arm_patch = patches.Polygon(np.column_stack([x_arm, y_arm]),
                            facecolor='#b9d9eb', edgecolor='#2c3e50', lw=1.5, alpha=0.7, zorder=6, clip_on=False)
ax.add_patch(arm_patch)

# 내부 슬롯
slot_x = [0.1, arm_length - 0.05, arm_length - 0.05, 0.1]
slot_y = [-0.03, -0.03, 0.03, 0.03]
slot_patch = patches.Polygon(np.column_stack([slot_x, slot_y]),
                             facecolor='white', edgecolor='#2c3e50', lw=1, alpha=0.7, zorder=7, clip_on=False)
ax.add_patch(slot_patch)

# 나사 (수평선들)
screw_lines = []
for xt in np.arange(0.12, arm_length - 0.05, 0.015):
    line, = ax.plot([xt, xt + 0.005], [-0.015, 0.015], color='#555', lw=0.4, zorder=7, alpha=0.5)
    screw_lines.append(line)

# 슬라이더 블록
slider_w, slider_h = 0.1, 0.12
slider_patch = patches.Rectangle((0, -slider_h/2), slider_w, slider_h,
                                  facecolor='#e1a987', edgecolor='#2c3e50', lw=1.5, alpha=0.85, zorder=8, clip_on=False)
ax.add_patch(slider_patch)

# 피벗 핀 (원점에 고정)
pivot_outer = patches.Circle((0, 0), 0.04, facecolor='white', edgecolor='#2c3e50', lw=1.5, zorder=12)
pivot_inner = patches.Circle((0, 0), 0.015, facecolor='#2c3e50', zorder=13)
ax.add_patch(pivot_outer)
ax.add_patch(pivot_inner)

# 삼각 베이스 (원점 아래에 고정 — 회전하지 않음)
base_tri = patches.Polygon([[0, 0], [-0.06, -0.12], [0.06, -0.12]],
                           facecolor='#d3d3d3', edgecolor='black', lw=1, zorder=11)
ax.add_patch(base_tri)
# 해칭 바닥선
ax.plot([-0.1, 0.1], [-0.12, -0.12], 'k-', lw=1.5, zorder=11)
for xh in np.linspace(-0.08, 0.08, 6):
    ax.plot([xh, xh - 0.02], [-0.12, -0.15], 'k-', lw=0.8, zorder=11)

# 텍스트 라벨들
txt_O = ax.text(-0.12, 0.06, '$O$', fontsize=18, fontfamily='serif', fontstyle='italic', zorder=14)
txt_B = ax.text(0, 0, '$B$', fontsize=16, fontfamily='serif', fontstyle='italic', fontweight='bold',
                color='#c0392b', zorder=14)
txt_A = ax.text(0, 0, '$A$', fontsize=16, fontfamily='serif', fontstyle='italic', zorder=14)

# 궤적 라인 (빨간색 굵은 실선)
line_traj, = ax.plot([], [], color='#e60033', lw=3, solid_capstyle='round', zorder=3)
dot_traj, = ax.plot([], [], 'o', color='#e60033', markersize=4, zorder=3)

# 벡터 화살표
arr_v = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->', mutation_scale=18,
                                 color='#27ae60', lw=2.5, zorder=10)
arr_a = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->', mutation_scale=18,
                                 color='#c0392b', lw=2.5, zorder=10)
ax.add_patch(arr_v)
ax.add_patch(arr_a)
lbl_v = ax.text(0, 0, '$\\mathbf{v}$', color='#27ae60', fontsize=15, fontweight='bold', zorder=14)
lbl_a = ax.text(0, 0, '$\\mathbf{a}$', color='#c0392b', fontsize=15, fontweight='bold', zorder=14)

# 정보 패널 (fig 좌표계로 우측 하단에 배치 → 팔에 겹치지 않음)
info_panel = fig.text(0.98, 0.03, '', fontsize=13, va='bottom', ha='right',
                      fontfamily='Malgun Gothic',
                      bbox=dict(facecolor='white', alpha=0.92, edgecolor='#888',
                                boxstyle='round,pad=0.5'))

# 궤적 화살표 (원본 그림처럼 곡선 위에 방향 표시)
traj_arrow_times = [1.5, 3.5, 4.5]
traj_arrows = []
for _ in traj_arrow_times:
    arr = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->', mutation_scale=18,
                                   color='#e60033', lw=2.5, zorder=4)
    arr.set_visible(False)
    ax.add_patch(arr)
    traj_arrows.append(arr)


def animate(i):
    r = r_val[i]
    th = theta_val[i]
    ux, uy = np.cos(th), np.sin(th)
    nx, ny = -np.sin(th), np.cos(th)

    # --- 로봇 팔 회전 ---
    trans = Affine2D().rotate(th) + ax.transData
    arm_patch.set_transform(trans)
    slot_patch.set_transform(trans)
    for line in screw_lines:
        line.set_transform(trans)

    slider_patch.set_xy((r - slider_w / 2, -slider_h / 2))
    slider_patch.set_transform(trans)

    # B, A 라벨
    Bx, By = r * ux, r * uy
    txt_B.set_position((Bx + 0.06 * nx, By + 0.06 * ny))
    Ax, Ay = arm_length * ux, arm_length * uy
    txt_A.set_position((Ax + 0.06, Ay + 0.06))

    # --- 궤적 ---
    line_traj.set_data(x_full[:i + 1], y_full[:i + 1])

    # 궤적 위 방향 화살표
    for k, t_arr in enumerate(traj_arrow_times):
        idx_arr = np.argmin(np.abs(t_phys - t_arr))
        if i >= idx_arr and not traj_arrows[k].get_visible():
            xp, yp = x_full[idx_arr], y_full[idx_arr]
            dx = x_full[min(idx_arr + 1, frames - 1)] - x_full[max(idx_arr - 1, 0)]
            dy = y_full[min(idx_arr + 1, frames - 1)] - y_full[max(idx_arr - 1, 0)]
            ln = np.sqrt(dx**2 + dy**2) + 1e-9
            sc = 0.08
            traj_arrows[k].set_positions((xp - dx / ln * sc, yp - dy / ln * sc), (xp, yp))
            traj_arrows[k].set_visible(True)

    # --- 벡터 ---
    vx_c = vr[i] * ux + vth[i] * nx
    vy_c = vr[i] * uy + vth[i] * ny
    ax_c = ar[i] * ux + ath[i] * nx
    ay_c = ar[i] * uy + ath[i] * ny

    sc_v, sc_a = 0.25, 0.15
    v_end_x, v_end_y = Bx + vx_c * sc_v, By + vy_c * sc_v
    a_end_x, a_end_y = Bx + ax_c * sc_a, By + ay_c * sc_a

    arr_v.set_positions((Bx, By), (v_end_x, v_end_y))
    arr_a.set_positions((Bx, By), (a_end_x, a_end_y))
    lbl_v.set_position((v_end_x + 0.03, v_end_y + 0.03))
    lbl_a.set_position((a_end_x + 0.03, a_end_y + 0.03))

    # --- 정보 패널 ---
    highlight = abs(t_phys[i] - 3.0) < 0.05
    bg = '#fffacd' if highlight else 'white'
    info_panel.set_bbox(dict(facecolor=bg, alpha=0.92, edgecolor='#888', boxstyle='round,pad=0.5'))

    hdr = "[t = 3 s 정답 확인!]\n" if highlight else ""
    info_panel.set_text(
        f"{hdr}"
        f"t = {t_phys[i]:.2f} s\n"
        f"r = {r:.3f} m   θ = {np.degrees(th):.1f}°\n"
        f"──────────────\n"
        f"vr = {vr[i]:.3f}   vθ = {vth[i]:.3f}\n"
        f"|v| = {v_mag[i]:.3f} m/s\n"
        f"──────────────\n"
        f"ar = {ar[i]:.3f}   aθ = {ath[i]:.3f}\n"
        f"|a| = {a_mag[i]:.3f} m/s²"
    )

    return []


ani = FuncAnimation(fig, animate, frames=frames, interval=30, blit=False)
writer = PillowWriter(fps=30)
writer._kwargs = {'loop': None}
gif_path = 'ex2_9_robot_arm.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")

try:
    from PIL import Image
    im = Image.open(gif_path)
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 30))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(gif_path, save_all=True, append_images=frames_img[1:],
                       duration=durations, loop=1)
except Exception:
    pass
