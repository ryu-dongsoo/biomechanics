# -*- coding: utf-8 -*-
"""
[동역학 9판 예제 3.2] 공중 케이블카의 가속도(a) 및 지지케이블 수직반력(P) 해석
교재 원본 삽화, 5-12 경사 캐빈 및 완벽한 분리형 FBD 100% 동일 구현
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
m = 200.0          # 질량 (kg)
g = 9.81           # 중력가속도 (m/s^2)
W = m * g          # 자중 (1962 N)
cos_th = 12.0 / 13.0
sin_th = 5.0 / 13.0
th_rad = np.arcsin(sin_th)
th_deg = np.degrees(th_rad)

T_val = 2400.0     # 수평 견인 장력 (N)

# 운동방정식 해석
Fx = T_val * cos_th - W * sin_th   # 1460.77 N
a_val = Fx / m                     # 7.3038 m/s^2
P_val = W * cos_th + T_val * sin_th # 2734.15 N (2.73 kN)

# 애니메이션 설정
duration = 2.0     # 이동 시간 (초)
fps = 30
n_sim_frames = int(fps * duration)
n_pause_frames = 18
total_frames = n_sim_frames + n_pause_frames

t_eval = np.linspace(0, duration, n_sim_frames)

fig = plt.figure(figsize=(13.2, 8.4), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.92])
title_text = '[동역학 9판 예제 3.2] 수평 견인력(T = 2.4kN)을 받는 5-12 경사 공중 케이블카(200kg)의 FBD 및 가속도 해석'

def update(frame):
    if frame < n_sim_frames:
        t = t_eval[frame]
        s = 0.5 * a_val * (t**2)
        v = a_val * t
    else:
        t = duration
        s = 0.5 * a_val * (duration**2)
        v = a_val * duration
        
    ax.clear()
    ax.set_xlim(-1.2, 25.2)
    ax.set_ylim(-1.2, 15.2)
    ax.axis('off')
    
    # 1. 배경
    ax.add_patch(patches.Rectangle((-1.2, -1.2), 26.5, 16.5, fc='#f8fafc', ec='none', zorder=1))
    
    # -------------------------------------------------------------
    # 2. 좌측 상단: HUD 정보 박스 (수식 전개 및 실시간 수치)
    # -------------------------------------------------------------
    hud_str = (
        f"[예제 3.2: 5-12 경사 공중 케이블카 운동역학]\n"
        f"경과 시간:  t = {t:4.2f} s / {duration:4.2f} s\n"
        f"-----------------------------------------\n"
        f"• 질량: m = 200 kg,  자중 W = 200(9.81) = 1962 N\n"
        f"• 경사 기울기: 5-12-13 (cos θ = 12/13, sin θ = 5/13, θ = 22.6°)\n"
        f"• 수평 견인력: T = 2.4 kN = 2400 N (수평 방향)\n"
        f"• 케이블 방향(x축 운동방정식): ΣFx = m a\n"
        f"  T cos θ - mg sin θ = m a\n"
        f"  2400(12/13) - 1962(5/13) = 200 a ⇒ a = 7.30 m/s²\n"
        f"• 수직 방향(y축 평형방정식): ΣFy = 0\n"
        f"  P - T sin θ - mg cos θ = 0\n"
        f"  P = 2400(5/13) + 1962(12/13) ⇒ P = 2.73 kN\n"
        f"-----------------------------------------\n"
        f"• 현재 속도:   v(t) = {v:4.2f} m/s  ({v*3.6:4.1f} km/h)\n"
        f"• 이동 변위:   s(t) = {s:4.2f} m\n"
        f"-----------------------------------------\n"
        f"▶ 케이블카 가속도: a = 7.30 m/s² (케이블 상향)\n"
        f"▶ 지지케이블 수직반력: P = 2.73 kN"
    )
    ax.text(-0.2, 14.8, hud_str, fontsize=7.4, va='top', family='monospace', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#0284c7', lw=1.3, alpha=0.98), zorder=20)
    
    # -------------------------------------------------------------
    # 3. 좌측 하단: 실제 물리 시스템 거동 애니메이션 (Schematic Diagram)
    # -------------------------------------------------------------
    u_c = np.array([cos_th, sin_th])
    n_c = np.array([-sin_th, cos_th])
    
    cable_p0 = np.array([0.0, 3.5])
    cable_p1 = cable_p0 + 13.0 * u_c
    
    # 지지 케이블 와이어
    ax.plot([cable_p0[0] - 0.8, cable_p1[0] + 0.8],
            [cable_p0[1] - 0.8*sin_th/cos_th, cable_p1[1] + 0.8*sin_th/cos_th],
            color='#334155', lw=3.2, zorder=3)
    
    # 5-12 경사 삼각형
    tri_s = cable_p0 + 9.5 * u_c + 0.6 * n_c
    tri_len = 2.4
    tri_h = tri_len * (5.0 / 12.0)
    ax.plot([tri_s[0], tri_s[0] + tri_len], [tri_s[1], tri_s[1]], color='#dc2626', lw=1.4, zorder=5)
    ax.plot([tri_s[0] + tri_len, tri_s[0] + tri_len], [tri_s[1], tri_s[1] + tri_h], color='#dc2626', lw=1.4, zorder=5)
    ax.plot([tri_s[0], tri_s[0] + tri_len], [tri_s[1], tri_s[1] + tri_h], color='#dc2626', lw=1.4, zorder=5)
    ax.text(tri_s[0] + tri_len/2, tri_s[1] - 0.35, '12', fontsize=8.0, fontweight='bold', color='#dc2626', ha='center', zorder=6)
    ax.text(tri_s[0] + tri_len + 0.15, tri_s[1] + tri_h/2, '5', fontsize=8.0, fontweight='bold', color='#dc2626', va='center', zorder=6)
    
    # 케이블카 위치 (스케일 매핑)
    s_scale = 0.50
    car_pos_dist = 1.8 + s * s_scale
    car_center_c = cable_p0 + car_pos_dist * u_c
    
    # 1) 트롤리 롤러 바퀴 2개
    roller_r = 0.35
    roller_span = 1.3
    w1_c = car_center_c - (roller_span/2) * u_c + roller_r * n_c
    w2_c = car_center_c + (roller_span/2) * u_c + roller_r * n_c
    
    ax.add_patch(patches.Circle(w1_c, roller_r, fc='#e2e8f0', ec='#0f172a', lw=1.2, zorder=6))
    ax.add_patch(patches.Circle(w2_c, roller_r, fc='#e2e8f0', ec='#0f172a', lw=1.2, zorder=6))
    ax.scatter([w1_c[0], w2_c[0]], [w1_c[1], w2_c[1]], color='#0f172a', s=10, zorder=7)
    
    # 2) 트롤리 상부 행어 프레임 (교재 원본 곡선 형상)
    hanger_pts = [
        w1_c - 0.2*u_c - 0.1*n_c,
        w2_c + 0.2*u_c - 0.1*n_c,
        car_center_c + 0.9*u_c - 0.8*n_c,
        car_center_c - 0.9*u_c - 0.8*n_c,
    ]
    hanger_poly = patches.Polygon(hanger_pts, closed=True, fc='#ea580c', ec='#9a3412', lw=1.3, zorder=5)
    ax.add_patch(hanger_poly)
    
    # 3) 케이블카 캐빈 (경사각 theta에 맞춰 기울어진 완벽한 3D 캐빈)
    cab_L = 3.6
    cab_H = 2.2
    cab_c = car_center_c - 2.0 * n_c
    
    p_cab_bl = cab_c - (cab_L/2)*u_c - (cab_H/2)*n_c
    p_cab_br = cab_c + (cab_L/2)*u_c - (cab_H/2)*n_c
    p_cab_tr = cab_c + (cab_L/2)*u_c + (cab_H/2)*n_c
    p_cab_tl = cab_c - (cab_L/2)*u_c + (cab_H/2)*n_c
    
    cab_poly = patches.Polygon([p_cab_bl, p_cab_br, p_cab_tr, p_cab_tl], closed=True,
                               fc='#fed7aa', ec='#c2410c', lw=1.6, zorder=6)
    ax.add_patch(cab_poly)
    
    # 캐빈 하부 가드
    p_guard_tr = p_cab_br + 0.5 * n_c
    p_guard_tl = p_cab_bl + 0.5 * n_c
    guard_poly = patches.Polygon([p_cab_bl, p_cab_br, p_guard_tr, p_guard_tl], closed=True,
                                 fc='#fdba74', ec='#c2410c', lw=1.2, zorder=7)
    ax.add_patch(guard_poly)
    
    # 3개 유리창 (경사 프레임 내부에 정렬)
    win_len = 0.8
    win_h = 1.0
    for i in range(3):
        win_offset_u = - (cab_L/2) + 0.3 + i * (win_len + 0.35)
        w_bl = p_cab_bl + 0.6*n_c + (win_offset_u + (cab_L/2))*u_c
        w_br = w_bl + win_len*u_c
        w_tr = w_br + win_h*n_c
        w_tl = w_bl + win_h*n_c
        win_poly = patches.Polygon([w_bl, w_br, w_tr, w_tl], closed=True,
                                   fc='#bae6fd', ec='#0284c7', lw=1.1, zorder=7)
        ax.add_patch(win_poly)
        # 창문 반사광
        r_s = w_bl + 0.2*u_c + 0.2*n_c
        r_e = w_bl + 0.6*u_c + 0.8*n_c
        ax.plot([r_s[0], r_e[0]], [r_s[1], r_e[1]], color='#ffffff', lw=1.2, alpha=0.85, zorder=8)
        
    ax.text(cab_c[0] - 0.2, cab_c[1] - 0.7, r'$200\text{ kg}$', fontsize=8.0, fontweight='bold', color='#7c2d12', zorder=8)
    
    # 4) 우측 견인 핀 점 A (캐빈 우측 하단)
    pt_A = p_cab_br + 0.4 * n_c
    ax.add_patch(patches.Circle(pt_A + np.array([0.2, 0]), 0.12, fc='#ffffff', ec='#1e293b', lw=1.2, zorder=9))
    ax.text(pt_A[0] + 0.1, pt_A[1] - 0.4, r'$A$', fontsize=10.0, fontweight='bold', color='#0f172a', zorder=10)
    
    # 수평 견인 로프 및 장력 T
    t_arrow_len = 2.2
    ax.plot([pt_A[0] + 0.32, pt_A[0] + 0.7], [pt_A[1], pt_A[1]], color='#334155', lw=1.8, zorder=8)
    ax.annotate('', xy=(pt_A[0] + 0.7 + t_arrow_len, pt_A[1]), xytext=(pt_A[0] + 0.7, pt_A[1]),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.2, headwidth=6.0, headlength=7.0), zorder=9)
    ax.text(pt_A[0] + 0.7 + t_arrow_len + 0.2, pt_A[1], r'$T$', fontsize=11.0, fontweight='bold', color='#b91c1c', va='center', zorder=10)
    
    # -------------------------------------------------------------
    # 4. 우측 영역: 교재 원본 100% 동일 독립 FBD 카드 (Free-Body Diagram)
    # -------------------------------------------------------------
    fbd_card = patches.FancyBboxPatch((12.5, 0.4), 12.2, 14.3,
                                      boxstyle="round,pad=0.25", fc="#ffffff", ec='#94a3b8', lw=1.3, alpha=0.98, zorder=10)
    ax.add_patch(fbd_card)
    
    ax.text(18.6, 14.2, r'【자유물체도 (Free-Body Diagram)】', fontsize=9.2, fontweight='bold', color='#b91c1c', ha='center', fontproperties=font_prop, zorder=12)
    
    # FBD 케이블카 바디 중심점 G 위치
    G_x, G_y = 17.5, 6.2
    G_pt = np.array([G_x, G_y])
    
    # FBD 케이블카 실루엣 (경사각 theta로 기울어진 교재 원본 실루엣)
    fbd_L, fbd_H = 3.8, 2.6
    f_bl = G_pt - (fbd_L/2)*u_c - (fbd_H/2)*n_c
    f_br = G_pt + (fbd_L/2)*u_c - (fbd_H/2)*n_c
    f_tr = G_pt + (fbd_L/2)*u_c + (fbd_H/2)*n_c
    f_top_r = G_pt + 0.8*u_c + (fbd_H/2 + 0.8)*n_c
    f_top_l = G_pt - 0.8*u_c + (fbd_H/2 + 0.8)*n_c
    f_tl = G_pt - (fbd_L/2)*u_c + (fbd_H/2)*n_c
    
    fbd_poly_pts = [f_bl, f_br, f_tr, f_top_r, f_top_l, f_tl]
    ax.add_patch(patches.Polygon(fbd_poly_pts, closed=True, fc='#ffedd5', ec='#ea580c', lw=1.6, zorder=12))
    
    # 질량중심 점 G 마크 (원형 흑백 4분할 마크)
    ax.add_patch(patches.Circle(G_pt, 0.28, fc='#ffffff', ec='#0f172a', lw=1.2, zorder=15))
    ax.add_patch(patches.Wedge(G_pt, 0.28, 0, 90, fc='#0f172a', ec='none', zorder=16))
    ax.add_patch(patches.Wedge(G_pt, 0.28, 180, 270, fc='#0f172a', ec='none', zorder=16))
    ax.text(G_x - 0.45, G_y, r'$G$', fontsize=10.5, fontweight='bold', color='#0f172a', ha='right', va='center', zorder=17)
    
    # 좌표축 x, y (점선 축 및 5-12 경사 삼각형)
    # x축
    x_axis_len = 4.2
    ax.plot([G_x - 1.5*cos_th, G_x + x_axis_len*cos_th],
            [G_y - 1.5*sin_th, G_y + x_axis_len*sin_th], color='#475569', lw=1.2, linestyle='--', zorder=13)
    ax.text(G_x + (x_axis_len + 0.3)*cos_th, G_y + (x_axis_len + 0.3)*sin_th, r'$x$',
            fontsize=10.0, fontweight='bold', color='#475569', va='center', zorder=14)
    
    # y축
    y_axis_len = 4.8
    ax.plot([G_x - 1.2*(-sin_th), G_x + y_axis_len*(-sin_th)],
            [G_y - 1.2*cos_th, G_y + y_axis_len*cos_th], color='#475569', lw=1.2, linestyle='--', zorder=13)
    ax.text(G_x + (y_axis_len + 0.3)*(-sin_th), G_y + (y_axis_len + 0.3)*cos_th, r'$y$',
            fontsize=10.0, fontweight='bold', color='#475569', ha='center', va='bottom', zorder=14)
    
    # x축 위의 5-12 삼각형 (교재 FBD 동일)
    fbd_tri_s = np.array([G_x + 2.0*cos_th, G_y + 2.0*sin_th - 0.6])
    fbd_tri_l = 1.6
    fbd_tri_h = fbd_tri_l * (5.0 / 12.0)
    ax.plot([fbd_tri_s[0], fbd_tri_s[0] + fbd_tri_l], [fbd_tri_s[1], fbd_tri_s[1]], color='#dc2626', lw=1.2, zorder=14)
    ax.plot([fbd_tri_s[0] + fbd_tri_l, fbd_tri_s[0] + fbd_tri_l], [fbd_tri_s[1], fbd_tri_s[1] + fbd_tri_h], color='#dc2626', lw=1.2, zorder=14)
    ax.plot([fbd_tri_s[0], fbd_tri_s[0] + fbd_tri_l], [fbd_tri_s[1], fbd_tri_s[1] + fbd_tri_h], color='#dc2626', lw=1.2, zorder=14)
    ax.text(fbd_tri_s[0] + fbd_tri_l/2, fbd_tri_s[1] - 0.28, '12', fontsize=7.5, fontweight='bold', color='#dc2626', ha='center', zorder=15)
    ax.text(fbd_tri_s[0] + fbd_tri_l + 0.1, fbd_tri_s[1] + fbd_tri_h/2, '5', fontsize=7.5, fontweight='bold', color='#dc2626', va='center', zorder=15)
    
    # y축 위의 5-12 삼각형 (교재 FBD 동일)
    y_tri_s = np.array([G_x + 3.2*(-sin_th) - 0.6, G_y + 3.2*cos_th])
    y_tri_v = 1.4
    y_tri_h = y_tri_v * (5.0 / 12.0)
    ax.plot([y_tri_s[0], y_tri_s[0]], [y_tri_s[1], y_tri_s[1] - y_tri_v], color='#dc2626', lw=1.2, zorder=14)
    ax.plot([y_tri_s[0], y_tri_s[0] + y_tri_h], [y_tri_s[1] - y_tri_v, y_tri_s[1] - y_tri_v], color='#dc2626', lw=1.2, zorder=14)
    ax.plot([y_tri_s[0], y_tri_s[0] + y_tri_h], [y_tri_s[1], y_tri_s[1] - y_tri_v], color='#dc2626', lw=1.2, zorder=14)
    ax.text(y_tri_s[0] - 0.25, y_tri_s[1] - y_tri_v/2, '12', fontsize=7.5, fontweight='bold', color='#dc2626', ha='right', va='center', zorder=15)
    ax.text(y_tri_s[0] + y_tri_h/2, y_tri_s[1] - y_tri_v - 0.25, '5', fontsize=7.5, fontweight='bold', color='#dc2626', ha='center', va='top', zorder=15)
    
    # 가속도 벡터 a (초록색 화살표)
    a_vec_s = G_pt + 1.2*u_c + 1.2*n_c
    a_vec_e = a_vec_s + 1.8 * u_c
    ax.annotate('', xy=a_vec_e, xytext=a_vec_s,
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=18)
    ax.text((a_vec_s[0] + a_vec_e[0])/2 - 0.1, (a_vec_s[1] + a_vec_e[1])/2 + 0.35, r'$a$',
            fontsize=11.0, fontweight='bold', color='#16a34a', ha='center', zorder=19)
    
    # 중력 하중 W = mg = 1962 N (점 G에서 수직 하향)
    w_vec_len = 2.8
    ax.annotate('', xy=(G_x, G_y - w_vec_len), xytext=(G_x, G_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=18)
    ax.text(G_x, G_y - w_vec_len - 0.3, r'$W = mg = 1962\text{ N}$',
            fontsize=9.5, fontweight='bold', color='#b91c1c', ha='center', va='top', zorder=19)
    
    # 수평 견인 장력 T = 2.4 kN (점 A에서 수평 우향)
    t_fbd_s = f_br + 0.4 * n_c
    t_fbd_len = 2.6
    ax.annotate('', xy=(t_fbd_s[0] + t_fbd_len, t_fbd_s[1]), xytext=(t_fbd_s[0], t_fbd_s[1]),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=18)
    ax.text(t_fbd_s[0] + t_fbd_len + 0.25, t_fbd_s[1], r'$T = 2.4\text{ kN}$',
            fontsize=9.5, fontweight='bold', color='#b91c1c', va='center', zorder=19)
    
    # 케이블 수직 지지력 P (상부 트롤리 접촉점에서 y축 방향 상향)
    p_fbd_s = (f_top_r + f_top_l) / 2
    p_fbd_len = 2.8
    p_fbd_e = p_fbd_s + p_fbd_len * n_c
    ax.annotate('', xy=p_fbd_e, xytext=p_fbd_s,
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=18)
    ax.text(p_fbd_e[0] + 0.2, p_fbd_e[1], r'$P$',
            fontsize=11.5, fontweight='bold', color='#b91c1c', va='center', zorder=19)

fig.suptitle(title_text, fontsize=11.5, fontweight='bold', y=0.97, fontproperties=font_prop)
anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'ex3_2_cable_car.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
