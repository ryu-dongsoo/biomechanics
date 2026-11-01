# 문제 2/131: 야구 선수의 포물선 송구와 레이더 극좌표계(r-θ) 운동학
# 실시간 궤적, 단위벡터(e_r, e_theta), 속도/가속도 벡터 및 과제 힌트/최종 정답 시뮬레이션

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 물리 및 기하학적 매개변수 설정 ---
# 초기 조건: 속력 v0 = 35 m/s, 발사각 th0 = 30 deg, 중력가속도 g = 9.81 m/s^2
v0 = 35.0
th0_deg = 30.0
th0 = np.radians(th0_deg)
g = 9.81

t_target = 0.5  # 문제 목표 시점 (s)
t_total = 0.55  # 시뮬레이션 총 시간 (s)
frames = 110
t_arr = np.linspace(0.01, t_total, frames)

# 직교좌표계 궤적 및 도함수
vx0 = v0 * np.cos(th0)
vy0 = v0 * np.sin(th0)

x_arr = vx0 * t_arr
y_arr = vy0 * t_arr - 0.5 * g * (t_arr**2)

vx_arr = np.full_like(t_arr, vx0)
vy_arr = vy0 - g * t_arr
v_mag_arr = np.sqrt(vx_arr**2 + vy_arr**2)

# 극좌표계 변환
r_arr = np.sqrt(x_arr**2 + y_arr**2)
th_arr = np.arctan2(y_arr, x_arr)

# 극좌표 속도 성분 (v_r, v_theta)
vr_arr = vx_arr * np.cos(th_arr) + vy_arr * np.sin(th_arr)
vth_arr = -vx_arr * np.sin(th_arr) + vy_arr * np.cos(th_arr)

r_dot_arr = vr_arr
th_dot_arr = vth_arr / r_arr

# 극좌표 가속도 성분 (a_r, a_theta)
ar_arr = -g * np.sin(th_arr)
ath_arr = -g * np.cos(th_arr)

r_ddot_arr = ar_arr + r_arr * (th_dot_arr**2)
th_ddot_arr = (ath_arr - 2.0 * r_dot_arr * th_dot_arr) / r_arr

# --- 2. 캔버스 및 레이아웃 구성 (12.8 x 7.5 와이드) ---
fig, ax = plt.subplots(figsize=(12.8, 7.5))
fig.subplots_adjust(left=0.04, right=0.65, bottom=0.06, top=0.94)
ax.set_facecolor('#ebf5fb')
ax.set_aspect('equal')
ax.axis('off')

ax.set_xlim(-2.0, 20.0)
ax.set_ylim(-1.5, 11.5)

# 배경 사각 테두리
bg_box = patches.Rectangle((-1.5, -1.0), 21.0, 12.0, facecolor='#ebf5fb', edgecolor='#85929e', lw=1.5, zorder=0)
ax.add_patch(bg_box)

# 지면 및 직교좌표 축
ax.plot([-1.0, 19.0], [0, 0], 'k-', lw=1.5, zorder=2)
ax.plot([0, 0], [-0.5, 10.5], 'k--', lw=1.0, alpha=0.6, zorder=2)
ax.plot([-0.5, 18.5], [0, 0], 'k--', lw=1.0, alpha=0.6, zorder=2)

ax.text(18.8, 0, '$x$', fontsize=14, fontfamily='serif', fontstyle='italic', va='center', ha='left')
ax.text(0, 10.7, '$y$', fontsize=14, fontfamily='serif', fontstyle='italic', va='bottom', ha='center')

# 원점 O 마크
ax.plot(0, 0, 'ko', markersize=6, zorder=5)
ax.text(-0.5, -0.6, '$O$', fontsize=14, fontfamily='serif', fontweight='bold', ha='right', va='top')

# 초기 발사 방향 점선 및 각도 30 deg
ax.plot([0, 12 * np.cos(th0)], [0, 12 * np.sin(th0)], color='#7f8c8d', ls=':', lw=1.2, zorder=1)
arc_th0 = patches.Arc((0, 0), 5.0, 5.0, angle=0, theta1=0, theta2=th0_deg, color='#e67e22', lw=1.5, zorder=2)
ax.add_patch(arc_th0)
ax.text(3.0 * np.cos(np.radians(15)), 3.0 * np.sin(np.radians(15)), r'$30^\circ$', color='#e67e22', fontsize=11, fontweight='bold', ha='center', va='center')

# 비행 궤적 점선
ax.plot(x_arr, y_arr, color='#2980b9', ls='--', lw=1.5, alpha=0.7, zorder=2)

# 야구공 그래픽스
ball = patches.Circle((0, 0), 0.35, facecolor='white', edgecolor='#2c3e50', lw=1.5, zorder=10)
ax.add_patch(ball)

# 동적 그래픽스 객체
line_r, = ax.plot([], [], color='#e67e22', lw=2.0, ls='-', zorder=3)
txt_r_label = ax.text(0, 0, '', color='#d35400', fontsize=11, fontweight='bold', ha='center', va='center',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=1))

arc_theta = patches.Arc((0, 0), 6.0, 6.0, angle=0, theta1=0, theta2=0, color='#2980b9', lw=1.8, zorder=3)
ax.add_patch(arc_theta)
txt_theta_label = ax.text(0, 0, r'$\theta$', color='#2980b9', fontsize=12, fontweight='bold', ha='center', va='center')

# 단위벡터 e_r, e_theta
arr_er = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=3,head_length=6', color='#2c3e50', lw=1.5, zorder=6)
arr_eth = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=3,head_length=6', color='#2c3e50', lw=1.5, zorder=6)
ax.add_patch(arr_er)
ax.add_patch(arr_eth)
txt_er = ax.text(0, 0, r'$\mathbf{e}_r$', color='#2c3e50', fontsize=11, fontweight='bold', ha='center', va='center')
txt_eth = ax.text(0, 0, r'$\mathbf{e}_\theta$', color='#2c3e50', fontsize=11, fontweight='bold', ha='center', va='center')

# 속도 벡터
arr_v = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=4,head_length=8', color='#27ae60', lw=2.4, zorder=8)
ax.add_patch(arr_v)
txt_v = ax.text(0, 0, r'$\mathbf{v}$', color='#27ae60', fontsize=12, fontweight='bold')

# 가속도 벡터
arr_a = patches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='->,head_width=4,head_length=8', color='#c0392b', lw=2.4, zorder=8)
ax.add_patch(arr_a)
txt_a = ax.text(0, 0, r'$\mathbf{a} = -g\mathbf{j}$', color='#c0392b', fontsize=11, fontweight='bold')

# 우측 정보 패널 (우측 전용 영역 0.66 ~ 0.98)
info_panel = fig.text(0.66, 0.50, '', fontsize=10.0, va='center', ha='left',
                      bbox=dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.6', lw=1.5))

def animate(i):
    t_curr = t_arr[i]
    x_curr = x_arr[i]
    y_curr = y_arr[i]
    r_curr = r_arr[i]
    th_curr = th_arr[i]

    ball.center = (x_curr, y_curr)

    line_r.set_data([0, x_curr], [0, y_curr])
    txt_r_label.set_position((0.5 * x_curr - 0.4 * np.sin(th_curr), 0.5 * y_curr + 0.4 * np.cos(th_curr)))
    txt_r_label.set_text(f'$r = {r_curr:.2f}$ m')

    arc_theta.theta2 = np.degrees(th_curr)
    th_mid = th_curr / 2.0
    txt_theta_label.set_position((3.5 * np.cos(th_mid), 3.5 * np.sin(th_mid)))
    txt_theta_label.set_text(f'$\\theta = {np.degrees(th_curr):.1f}^\\circ$')

    er = np.array([np.cos(th_curr), np.sin(th_curr)])
    eth = np.array([-np.sin(th_curr), np.cos(th_curr)])
    u_len = 1.6

    arr_er.set_positions((x_curr, y_curr), (x_curr + u_len * er[0], y_curr + u_len * er[1]))
    arr_eth.set_positions((x_curr, y_curr), (x_curr + u_len * eth[0], y_curr + u_len * eth[1]))
    txt_er.set_position((x_curr + (u_len + 0.3) * er[0], y_curr + (u_len + 0.3) * er[1]))
    txt_eth.set_position((x_curr + (u_len + 0.3) * eth[0], y_curr + (u_len + 0.3) * eth[1]))

    v_scale = 0.10
    v_vec = np.array([vx_arr[i], vy_arr[i]])
    arr_v.set_positions((x_curr, y_curr), (x_curr + v_vec[0] * v_scale, y_curr + v_vec[1] * v_scale))
    txt_v.set_position((x_curr + v_vec[0] * v_scale + 0.2, y_curr + v_vec[1] * v_scale + 0.2))

    a_scale = 0.20
    a_vec = np.array([0, -g])
    arr_a.set_positions((x_curr, y_curr), (x_curr + a_vec[0] * a_scale, y_curr + a_vec[1] * a_scale))
    txt_a.set_position((x_curr + 0.3, y_curr - g * a_scale))

    is_final = (i == frames - 1)
    status_hdr = "★ [과제 과업 및 최종 정답 (t = 0.5 s)] ★" if is_final else "■ [문제 2/131: 야구 송구 극좌표 운동학]"

    info_str = (
        f"{status_hdr}\n"
        f"─────────────────────────────────────\n"
        f"【초기 발사 조건】\n"
        f" • 초기 속력: $v_0 = {v0:.0f}$ m/s,  발사각: $\\theta_0 = {th0_deg:.0f}^\\circ$\n"
        f" • 중력가속도: $g = {g:.2f}$ m/s² (수직 하향)\n"
        f" • 목표 해석 시점: $t = 0.5$ s\n"
        f"─────────────────────────────────────\n"
        f"【실시간 운동 상태 (Monitoring)】\n"
        f" • 시간 $t = {t_curr:.3f}$ s  ($x = {x_curr:.2f}$ m, $y = {y_curr:.2f}$ m)\n"
        f" • 속력 $|\\mathbf{{v}}| = {v_mag_arr[i]:.2f}$ m/s  (녹색 벡터)\n"
        f" • 가속도 $|\\mathbf{{a}}| = {g:.2f}$ m/s² (적색 벡터)\n"
        f"─────────────────────────────────────\n"
        f"▶ 【풀이 핵심 힌트 (Hint)】\n"
        f" • 직교 위치: $x = v_0\\cos\\theta_0 t,\\ y = v_0\\sin\\theta_0 t - \\frac{{1}}{{2}}gt^2$\n"
        f" • 극좌표 관계: $r = \\sqrt{{x^2+y^2}},\\ \\theta = \\arctan(y/x)$\n"
        f" • 속도 변환: $\\dot{{r}} = \\dot{{x}}\\cos\\theta + \\dot{{y}}\\sin\\theta$\n"
        f"              $r\\dot{{\\theta}} = -\\dot{{x}}\\sin\\theta + \\dot{{y}}\\cos\\theta$\n"
        f" • 가속도 변환: $\\ddot{{r}} - r\\dot{{\\theta}}^2 = -g\\sin\\theta$\n"
        f"                $r\\ddot{{\\theta}} + 2\\dot{{r}}\\dot{{\\theta}} = -g\\cos\\theta$\n"
        f"─────────────────────────────────────\n"
        f"★ 【최종 정답 ($t = 0.5$ s 순간)】\n"
        f" (1) 반경: $r = 16.59$ m\n"
        f" (2) 반경 속도: $\\dot{{r}} = 34.33$ m/s\n"
        f" (3) 반경 가속도: $\\ddot{{r}} = -2.85$ m/s²\n"
        f" (4) 각변위: $\\theta = 23.4^\\circ$ ($0.408$ rad)\n"
        f" (5) 각속도: $\\dot{{\\theta}} = -0.409$ rad/s\n"
        f" (6) 각가속도: $\\ddot{{\\theta}} = 1.144$ rad/s²"
    )
    info_panel.set_text(info_str)
    if is_final:
        info_panel.set_bbox(dict(facecolor='#fefde8', alpha=0.98, edgecolor='#e67e22', boxstyle='round,pad=0.6', lw=1.8))
    else:
        info_panel.set_bbox(dict(facecolor='white', alpha=0.98, edgecolor='#3498db', boxstyle='round,pad=0.5', lw=1.2))

    return []

ani = FuncAnimation(fig, animate, frames=frames, interval=35, blit=False)

gif_path = Path(__file__).parent / 'prob2_131_baseball_throw.gif'
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
