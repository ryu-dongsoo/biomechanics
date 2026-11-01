# -*- coding: utf-8 -*-
"""
[동역학 9판 제3장 질점의 운동역학]
1. 동역학의 두 가지 문제 (Two Basic Problems of Dynamics: Force -> Motion vs. Motion -> Force)
2. 구속 운동과 비구속 운동 (Constrained Motion vs. Unconstrained Motion)
개념 인포그래픽 다이어그램 시각화 (완전 한글 폰트 지원 및 정밀 일러스트)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = fm.FontProperties(family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(17.0, 11.2), dpi=150)
ax = fig.add_subplot(111)
ax.set_position([0.01, 0.02, 0.98, 0.92])

ax.clear()
ax.set_xlim(-0.5, 33.5)
ax.set_ylim(-0.5, 21.5)
ax.axis('off')

# 전체 배경
ax.add_patch(patches.Rectangle((-0.5, -0.5), 34.0, 22.0, fc='#f8fafc', ec='none', zorder=1))

# =========================================================================
# [상단 헤더]: 메인 대주제 1 - 동역학의 두 가지 문제 (Two Basic Problems of Dynamics)
# =========================================================================
top_header = patches.FancyBboxPatch((0.2, 19.8), 32.6, 1.2, boxstyle="round,pad=0.2",
                                    fc="#0284c7", ec="none", zorder=3)
ax.add_patch(top_header)
ax.text(16.5, 20.4, "PART 1. 동역학의 두 가지 기본 문제 (Two Basic Problems of Dynamics)",
        fontsize=13.0, fontweight='bold', color='#ffffff', ha='center', va='center', fontproperties=font_prop, zorder=4)

# -------------------------------------------------------------------------
# [카드 1] 좌상단: 유형 1 - 정방향 문제 (Direct Problem: Force -> Motion)
# -------------------------------------------------------------------------
card1 = patches.FancyBboxPatch((0.2, 10.8), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#38bdf8", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card1)

ax.text(8.2, 18.8, "유형 1: 정방향 문제 (Direct Problem: Force → Motion)",
        fontsize=11.5, fontweight='bold', color="#0369a1", ha='center', fontproperties=font_prop, zorder=5)
ax.plot([0.6, 15.8], [18.4, 18.4], color='#e0f2fe', lw=1.4, zorder=4)

c1_text = (
    "■ 문제 정의:\n"
    "  • 질점에 작용하는 힘 ΣF(t, r, v)가 주어졌을 때,\n"
    "    뉴턴 제2법칙을 시간 적분하여 물체의 가속도, 속도, 위치 궤적을 구함\n"
    "■ 수학적 흐름:\n"
    "  • 작용력 ΣF  ⇒  가속도 a(t) = ΣF/m  ⇒  속도 v(t) = ∫ a dt  ⇒  위치 r(t) = ∫ v dt\n"
    "■ 대표 예시:\n"
    "  • 초기속도와 공기저항력을 받는 발사체 궤적 해석 (예: 예제 3.4 모터보트 감속)"
)
ax.text(0.6, 18.1, c1_text, fontsize=8.2, va='top', fontproperties=font_prop, linespacing=1.35, zorder=5)

# 유형 1 다이어그램 드로잉 (발사체 포물선 비행)
p_x0, p_y0 = 2.0, 11.6
t_pts = np.linspace(0, 2.8, 50)
traj_x = p_x0 + 4.2 * t_pts
traj_y = p_y0 + 4.2 * t_pts - 0.5 * 2.8 * (t_pts**2)

# 지면
ax.plot([1.2, 15.2], [p_y0, p_y0], color='#64748b', lw=1.5, zorder=3)
# 궤적 점선
ax.plot(traj_x, traj_y, color='#0284c7', lw=1.8, linestyle='--', zorder=4)

# 발사체 질점 (중간 시점)
curr_idx = 25
cx, cy = traj_x[curr_idx], traj_y[curr_idx]
ax.scatter([cx], [cy], color='#0284c7', s=45, zorder=6)
ax.text(cx + 0.3, cy + 0.3, r'$m$', fontsize=10.0, fontweight='bold', color='#0284c7', zorder=7)

# 입력 힘 화살표 (중력 mg, 공기저항 D)
ax.annotate('', xy=(cx, cy - 1.6), xytext=(cx, cy),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx + 0.2, cy - 1.2, r'$m\mathbf{g}$', fontsize=9.0, fontweight='bold', color='#b91c1c', zorder=8)

tang_v = np.array([4.2, 4.2 - 2.8 * t_pts[curr_idx]])
tang_u = tang_v / np.linalg.norm(tang_v)
ax.annotate('', xy=(cx - 1.4*tang_u[0], cy - 1.4*tang_u[1]), xytext=(cx, cy),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx - 1.6*tang_u[0] - 0.8, cy - 1.6*tang_u[1], r'$\mathbf{D}(v)$', fontsize=8.5, fontweight='bold', color='#c2410c', zorder=8)

# 출력 궤적 화살표
ax.annotate('', xy=(cx + 1.6*tang_u[0], cy + 1.6*tang_u[1]), xytext=(cx, cy),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx + 1.8*tang_u[0] + 0.1, cy + 1.8*tang_u[1], r'$\mathbf{v}(t), \mathbf{r}(t)$',
        fontsize=9.0, fontweight='bold', color='#2563eb', zorder=8)

# 입력/출력 뱃지 박스
ax.text(1.2, 14.6, "【주어진 입력】\n 힘: mg, D(v)", fontsize=7.6, color='#b91c1c', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fee2e2', edgecolor='#fca5a5', lw=1.0), zorder=6)
ax.text(11.2, 14.6, "【구해야 할 출력】\n 궤적 r(t), 속도 v(t)", fontsize=7.6, color='#1e40af', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#dbeafe', edgecolor='#93c5fd', lw=1.0), zorder=6)

# -------------------------------------------------------------------------
# [카드 2] 우상단: 유형 2 - 역방향 문제 (Inverse Problem: Motion -> Force)
# -------------------------------------------------------------------------
card2 = patches.FancyBboxPatch((16.8, 10.8), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#818cf8", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card2)

ax.text(24.8, 18.8, "유형 2: 역방향 문제 (Inverse Problem: Motion → Force)",
        fontsize=11.5, fontweight='bold', color="#4338ca", ha='center', fontproperties=font_prop, zorder=5)
ax.plot([17.2, 32.4], [18.4, 18.4], color='#e0e7ff', lw=1.4, zorder=4)

c2_text = (
    "■ 문제 정의:\n"
    "  • 물체가 지정된 운동 경로 r(t)나 가속도 a(t)를 만족하도록 기동할 때,\n"
    "    이를 발생시키는 데 필요한 구동력, 엔진 추력, 케이블 장력, 반력을 계산\n"
    "■ 수학적 흐름:\n"
    "  • 규정된 운동 r(t), a(t)  ⇒  뉴턴 제2법칙  ⇒  소요 구동력 ΣF = m a(t)\n"
    "■ 대표 예시:\n"
    "  • 정해진 시간에 정지시키기 위한 외력 계산 (예: 예제 3.5 칼라 소요 외력 F)"
)
ax.text(17.2, 18.1, c2_text, fontsize=8.2, va='top', fontproperties=font_prop, linespacing=1.35, zorder=5)

# 유형 2 다이어그램 드로잉 (곡면 레일 위의 롤러코스터 루프 기동)
loop_cx, loop_cy, loop_r = 24.8, 13.8, 2.0
theta_loop = np.linspace(-np.pi/2, np.pi/2, 50)
loop_x = loop_cx + loop_r * np.cos(theta_loop)
loop_y = loop_cy + loop_r * np.sin(theta_loop)
ax.plot(loop_x, loop_y, color='#4338ca', lw=2.4, zorder=4)

# 롤러 카트 위치 (특정 각도 th = 30도)
th_car = np.radians(30)
car_x = loop_cx + loop_r * np.cos(th_car)
car_y = loop_cy + loop_r * np.sin(th_car)

ax.scatter([car_x], [car_y], color='#4338ca', s=45, zorder=6)
# 지정된 가속도 벡터 (법선 방향 구심가속도 a_n)
ax.annotate('', xy=(car_x - 1.3*np.cos(th_car), car_y - 1.3*np.sin(th_car)), xytext=(car_x, car_y),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(car_x - 1.5*np.cos(th_car) - 0.4, car_y - 1.5*np.sin(th_car) - 0.2, r'$\mathbf{a}_n = \frac{v^2}{\rho}$',
        fontsize=8.5, fontweight='bold', color='#1d4ed8', zorder=8)

# 구해야 할 소요 지지력/수직항력 N
ax.annotate('', xy=(car_x + 1.5*np.cos(th_car), car_y + 1.5*np.sin(th_car)), xytext=(car_x, car_y),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(car_x + 1.6*np.cos(th_car) + 0.1, car_y + 1.6*np.sin(th_car), r'$N_{\mathrm{req}}$ (소요 반력)',
        fontsize=8.8, fontweight='bold', color='#b91c1c', fontproperties=font_prop, zorder=8)

# 입력/출력 뱃지 박스
ax.text(17.6, 14.6, "【주어진 입력】\n 규정 속도 v(t), 곡률 ρ", fontsize=7.6, color='#1e40af', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#dbeafe', edgecolor='#93c5fd', lw=1.0), zorder=6)
ax.text(27.8, 14.6, "【구해야 할 출력】\n 소요 수직항력 N, 추력 F", fontsize=7.6, color='#b91c1c', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fee2e2', edgecolor='#fca5a5', lw=1.0), zorder=6)

# =========================================================================
# [하단 헤더]: 메인 대주제 2 - 구속 운동 vs 비구속 운동 (Constrained vs. Unconstrained)
# =========================================================================
bot_header = patches.FancyBboxPatch((0.2, 9.4), 32.6, 1.2, boxstyle="round,pad=0.2",
                                    fc="#059669", ec="none", zorder=3)
ax.add_patch(bot_header)
ax.text(16.5, 10.0, "PART 2. 비구속 운동 vs 구속 운동 (Unconstrained vs. Constrained Motion)",
        fontsize=13.0, fontweight='bold', color='#ffffff', ha='center', va='center', fontproperties=font_prop, zorder=4)

# -------------------------------------------------------------------------
# [카드 3] 좌하단: 비구속 운동 (Unconstrained Motion: Free Flight)
# -------------------------------------------------------------------------
card3 = patches.FancyBboxPatch((0.2, 0.4), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#34d399", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card3)

ax.text(8.2, 8.4, "비구속 운동 (Unconstrained Motion)",
        fontsize=11.5, fontweight='bold', color="#047857", ha='center', fontproperties=font_prop, zorder=5)
ax.plot([0.6, 15.8], [8.0, 8.0], color='#d1fae5', lw=1.4, zorder=4)

c3_text = (
    "■ 개념 및 특징:\n"
    "  • 물체를 기하학적으로 제한하는 물리적 가이드, 레일, 접촉면이 전혀 없음\n"
    "  • 공간 내에서 자유도(DOF)가 온전히 유지됨 (3D 공간에서 3자유도)\n"
    "  • 오직 물체에 작용하는 외력(중력, 추력, 유체저항 등)에 의해서만 운동 궤적이 결정\n"
    "■ 대표 예시:\n"
    "  • 대기 중을 비행하는 로켓/항공기, 인공위성의 궤도 운동, 자유낙하 물체"
)
ax.text(0.6, 7.7, c3_text, fontsize=8.2, va='top', fontproperties=font_prop, linespacing=1.35, zorder=5)

# 비구속 운동 다이어그램 드로잉 (로켓 비행 및 외력계)
r_x, r_y = 7.8, 3.2
ang_r = np.radians(40)
u_r = np.array([np.cos(ang_r), np.sin(ang_r)])
n_r = np.array([-np.sin(ang_r), np.cos(ang_r)])

# 비행 궤적 (자유 곡선 점선)
traj_u_x = np.linspace(2.0, 14.5, 40)
traj_u_y = 1.2 + 0.7 * (traj_u_x - 2.0) - 0.035 * ((traj_u_x - 2.0)**2)
ax.plot(traj_u_x, traj_u_y, color='#059669', lw=1.8, linestyle=':', zorder=4)

# 3D 좌표계 표시
ax.annotate('', xy=(3.0, 4.0), xytext=(2.0, 4.0), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2), zorder=6)
ax.text(3.1, 4.0, r'$x$', fontsize=8.5, color='#64748b', va='center')
ax.annotate('', xy=(2.0, 5.0), xytext=(2.0, 4.0), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2), zorder=6)
ax.text(2.0, 5.1, r'$y$', fontsize=8.5, color='#64748b', ha='center')
ax.annotate('', xy=(1.3, 3.3), xytext=(2.0, 4.0), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2), zorder=6)
ax.text(1.2, 3.2, r'$z$', fontsize=8.5, color='#64748b', ha='right')
ax.text(2.1, 4.2, '(3-DOF)', fontsize=7.5, color='#64748b', fontproperties=font_prop)

# 로켓 그래픽
r_w, r_h = 2.2, 0.7
r_bl = np.array([r_x, r_y]) - (r_w/2)*u_r - (r_h/2)*n_r
ax.add_patch(patches.Rectangle(r_bl, r_w, r_h, angle=40, fc='#e0f2fe', ec='#0284c7', lw=1.4, zorder=6))
nose_tip = np.array([r_x, r_y]) + (r_w/2 + 0.6)*u_r
nose_l = np.array([r_x, r_y]) + (r_w/2)*u_r + (r_h/2)*n_r
nose_r = np.array([r_x, r_y]) + (r_w/2)*u_r - (r_h/2)*n_r
ax.add_patch(patches.Polygon([nose_tip, nose_l, nose_r], closed=True, fc='#ef4444', ec='#b91c1c', lw=1.2, zorder=7))

# 3대 외력 벡터 (구속 반력 없음!)
# 1) 엔진 추력 T
ax.annotate('', xy=nose_tip + 1.2*u_r, xytext=nose_tip,
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(nose_tip[0] + 1.3*u_r[0], nose_tip[1] + 1.3*u_r[1] + 0.1, r'$\mathbf{T}$' + ' (추력)',
        fontsize=8.5, fontweight='bold', color='#b91c1c', fontproperties=font_prop, zorder=9)

# 2) 중력 W = mg
ax.annotate('', xy=(r_x, r_y - 1.5), xytext=(r_x, r_y),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(r_x + 0.2, r_y - 1.2, r'$m\mathbf{g}$', fontsize=9.0, fontweight='bold', color='#c2410c', zorder=9)

# 3) 공기역학적 항력 D
ax.annotate('', xy=np.array([r_x, r_y]) - (r_w/2 + 1.0)*u_r, xytext=np.array([r_x, r_y]) - (r_w/2)*u_r,
            arrowprops=dict(facecolor='#64748b', edgecolor='#334155', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(r_x - (r_w/2 + 1.4)*u_r[0], r_y - (r_w/2 + 1.4)*u_r[1], r'$\mathbf{D}$' + ' (항력)',
        fontsize=8.5, fontweight='bold', color='#334155', fontproperties=font_prop, zorder=9)

ax.text(1.2, 2.0, "★ 특징: 구속 반력(N, R) = 0\n  자유도 = 3 (자유 공간 3D 비행)", fontsize=7.6, color='#047857', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#ecfdf5', edgecolor='#a7f3d0', lw=1.0), zorder=8)

# -------------------------------------------------------------------------
# [카드 4] 우하단: 구속 운동 (Constrained Motion: Guided Track)
# -------------------------------------------------------------------------
card4 = patches.FancyBboxPatch((16.8, 0.4), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#f59e0b", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card4)

ax.text(24.8, 8.4, "구속 운동 (Constrained Motion)",
        fontsize=11.5, fontweight='bold', color="#b45309", ha='center', fontproperties=font_prop, zorder=5)
ax.plot([17.2, 32.4], [8.0, 8.0], color='#fef3c7', lw=1.4, zorder=4)

c4_text = (
    "■ 개념 및 특징:\n"
    "  • 물체가 물리적 가이드(레일, 와이어, 슬롯, 경사면)에 접촉하여 특정 경로로 제한\n"
    "  • 기하학적 구속 조건에 의해 운동 경로가 사전에 물리적으로 결정됨\n"
    "  • 경로를 유지하기 위해 접촉면에서 구속력(수직항력 N, 장력 T, 반력 R)이 발생\n"
    "■ 대표 예시:\n"
    "  • 경사면/레일 카트 (예제 3.2, 3.3), 수직 환봉 칼라 (예제 3.5), 도르래 연결체"
)
ax.text(17.2, 7.7, c4_text, fontsize=8.2, va='top', fontproperties=font_prop, linespacing=1.35, zorder=5)

# 구속 운동 다이어그램 드로잉 (곡면 가이드 레일 위의 칼라 블록)
c_base_x, c_base_y = 24.8, 3.2
# 사인파 곡면 가이드 레일
x_rail = np.linspace(17.6, 32.0, 60)
y_rail = c_base_y + 1.2 * np.sin((x_rail - 18.0) * 0.45)
ax.plot(x_rail, y_rail, color='#475569', lw=4.0, zorder=4)
ax.plot(x_rail, y_rail, color='#cbd5e1', lw=1.8, linestyle='--', zorder=5)
ax.text(30.2, c_base_y + 0.6, "가이드 레일 (1-DOF)", fontsize=7.8, color='#475569', fontproperties=font_prop, zorder=6)

# 특정 지점의 칼라 슬라이더
target_x = 24.0
target_y = c_base_y + 1.2 * np.sin((target_x - 18.0) * 0.45)
slope = 1.2 * 0.45 * np.cos((target_x - 18.0) * 0.45)
ang_c = np.arctan(slope)
u_c = np.array([np.cos(ang_c), np.sin(ang_c)])
n_c = np.array([-np.sin(ang_c), np.cos(ang_c)])

# 칼라 박스
cw, ch = 2.0, 1.2
c_bl = np.array([target_x, target_y]) - (cw/2)*u_c - (ch/2)*n_c
ax.add_patch(patches.Rectangle(c_bl, cw, ch, angle=np.degrees(ang_c),
                               fc='#fed7aa', ec='#c2410c', lw=1.5, zorder=6))
ax.scatter([target_x], [target_y], color='#c2410c', s=35, zorder=7)

# 구속에 의해 발생하는 힘 벡터
# 1) 구속 수직항력 N (레일에 수직)
ax.annotate('', xy=np.array([target_x, target_y]) + 1.8*n_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.2, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(target_x + 1.9*n_c[0], target_y + 1.9*n_c[1] + 0.1, r'$\mathbf{N}$' + ' (구속 수직항력)',
        fontsize=8.5, fontweight='bold', color='#15803d', fontproperties=font_prop, zorder=9)

# 2) 접촉 마찰력 f_k = mu * N (접선 반대 방향)
ax.annotate('', xy=np.array([target_x, target_y]) - 1.3*u_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(target_x - 1.5*u_c[0] - 0.2, target_y - 1.5*u_c[1] - 0.3, r'$f_k = \mu_k N$',
        fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=9)

# 3) 구동력/외력 F (접선 방향)
ax.annotate('', xy=np.array([target_x, target_y]) + 1.6*u_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(target_x + 1.7*u_c[0] + 0.1, target_y + 1.7*u_c[1], r'$\mathbf{F}$' + ' (구동력)',
        fontsize=8.5, fontweight='bold', color='#1d4ed8', fontproperties=font_prop, zorder=9)

# 4) 중력 mg
ax.annotate('', xy=(target_x, target_y - 1.5), xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(target_x + 0.2, target_y - 1.3, r'$m\mathbf{g}$', fontsize=9.0, fontweight='bold', color='#c2410c', zorder=9)

ax.text(17.6, 2.0, "★ 특징: 가이드가 운동 경로를 강제\n  수직 구속력 N 및 마찰력 발생 (1-DOF)", fontsize=7.6, color='#b45309', fontproperties=font_prop,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fffbeb', edgecolor='#fde68a', lw=1.0), zorder=8)

# 메인 타이틀
fig.suptitle('[동역학 9판 제3장 질점의 운동역학] 동역학의 두 가지 문제 & 구속·비구속 운동 개념도',
             fontsize=14.0, fontweight='bold', y=0.985, fontproperties=font_prop)

out_png = os.path.join(os.path.dirname(__file__), 'concept_dynamics_problems_and_constraints.png')
plt.savefig(out_png, dpi=150)
plt.close()
print(f'Rendered {out_png}')
