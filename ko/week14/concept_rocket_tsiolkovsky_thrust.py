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
보충 개념 애니메이션 2: 로켓 추진 동역학 및 치올콥스키(Tsiolkovsky) 속도 방정식 유도 시각화
동역학 9판 (한국어판) - 제4장 4.7절 가변질량 핵심 개념 시각화
- 순수 흰색 바탕 (#ffffff), STIX 수식 폰트, 한글 $...$ 외부 분리 원칙 준수
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# 대표 로켓 물리 제원 (질량비 m0/mb = 4.0)
m0 = 1000.0        # 초기 총질량 (kg)
mb = 250.0         # 연료 소진 후 구조물 질량 (kg)
m_prime = 15.0     # 양수 연료 연소율 m' = -dm/dt (kg/s)
m_dot = -m_prime   # 부호 있는 질량 변화율 dm/dt = -15.0 kg/s
u = 2000.0         # 배기가스 상대 분사속도 (m/s)
g = 9.81           # 중력가속도 (m/s^2)

tb = (m0 - mb) / m_prime                      # 50.0 s
T_thrust = m_prime * u                        # 30,000 N = 30.0 kN (일정)
v_max = u * np.log(m0 / mb) - g * tb          # 2772.6 - 490.5 = 2282.1 m/s
a_init = T_thrust / m0 - g                    # 20.19 m/s^2
a_final = T_thrust / mb - g                   # 110.19 m/s^2

n_frames = 54
t_vals = np.concatenate([
    np.linspace(0.0, tb, 45),
    np.full(9, tb)
])

fig = plt.figure(figsize=(14, 6.5), dpi=120)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.02, 1.18], height_ratios=[1.0, 1.0, 1.15],
              left=0.04, right=0.97, top=0.87, bottom=0.09, wspace=0.18, hspace=0.38)

ax_phys = fig.add_subplot(gs[:, 0])
ax_m = fig.add_subplot(gs[0, 1])
ax_a = fig.add_subplot(gs[1, 1])
ax_v = fig.add_subplot(gs[2, 1])

fig.suptitle('보충 개념 2: 로켓 연료 소모에 따른 비선형 가속도 증가 및 치올콥스키 속도 적분',
             fontsize=14.5, fontweight='bold', color='#1e3a5f', y=0.96)


def draw_rocket_cutaway(ax, xc, yc, fuel_frac):
    bw, bh = 0.56, 1.95
    # 동체 외벽
    ax.add_patch(patches.Rectangle((xc - bw / 2, yc), bw, bh,
                                   facecolor='#eceff1', edgecolor='#263238', lw=2.0, zorder=3))
    # 내부 연료 탱크 창 (투시 단면)
    tw, th = 0.38, 1.32
    ty0 = yc + 0.30
    ax.add_patch(patches.Rectangle((xc - tw / 2, ty0), tw, th,
                                   facecolor='#ffffff', edgecolor='#78909c', lw=1.3, zorder=4))
    if fuel_frac > 0.005:
        ax.add_patch(patches.Rectangle((xc - tw / 2, ty0), tw, th * fuel_frac,
                                       facecolor='#ffb74d', edgecolor='none', zorder=5))
        ax.plot([xc - tw / 2, xc + tw / 2], [ty0 + th * fuel_frac, ty0 + th * fuel_frac],
                color='#e65100', lw=1.6, zorder=6)

    # 노즈콘
    nose = patches.Polygon([[xc - bw / 2, yc + bh], [xc + bw / 2, yc + bh], [xc, yc + bh + 0.62]],
                           facecolor='#90caf9', edgecolor='#1e3a5f', lw=2.0, zorder=3)
    ax.add_patch(nose)

    # 좌우 안정핀
    fin_l = patches.Polygon([[xc - bw / 2, yc + 0.45], [xc - bw / 2 - 0.30, yc - 0.08], [xc - bw / 2, yc + 0.05]],
                            facecolor='#78909c', edgecolor='#263238', lw=1.6, zorder=2)
    fin_r = patches.Polygon([[xc + bw / 2, yc + 0.45], [xc + bw / 2 + 0.30, yc - 0.08], [xc + bw / 2, yc + 0.05]],
                            facecolor='#78909c', edgecolor='#263238', lw=1.6, zorder=2)
    ax.add_patch(fin_l)
    ax.add_patch(fin_r)

    # 하단 노즐
    noz = patches.Polygon([[xc - 0.14, yc], [xc + 0.14, yc], [xc + 0.22, yc - 0.22], [xc - 0.22, yc - 0.22]],
                          facecolor='#455a64', edgecolor='#263238', lw=1.5, zorder=3)
    ax.add_patch(noz)

    # 분사 화염 (연료 잔존 시)
    if fuel_frac > 0.001:
        ax.add_patch(patches.Polygon([[xc - 0.18, yc - 0.22], [xc + 0.18, yc - 0.22], [xc, yc - 1.08]],
                                     facecolor='#ff7043', alpha=0.85, zorder=2))
        ax.add_patch(patches.Polygon([[xc - 0.09, yc - 0.22], [xc + 0.09, yc - 0.22], [xc, yc - 0.72]],
                                     facecolor='#fff176', alpha=0.95, zorder=3))


t_dense = np.linspace(0, tb, 150)
m_dense = m0 - m_prime * t_dense
a_dense = T_thrust / m_dense - g
a_const_m = np.full_like(t_dense, a_init)
v_ideal_dense = u * np.log(m0 / m_dense)
v_act_dense = v_ideal_dense - g * t_dense


def update(frame):
    t = t_vals[frame]
    m_curr = m0 - m_prime * t
    fuel_frac = max(0.0, (m_curr - mb) / (m0 - mb))
    W_curr = m_curr * g
    a_curr = T_thrust / m_curr - g
    v_curr = u * np.log(m0 / m_curr) - g * t

    # ---------------- 1. 좌측: 가변질량 로켓 자유물체도 및 힘/가속도 변화 ----------------
    ax_phys.cla()
    ax_phys.set_facecolor('#ffffff')
    ax_phys.set_xlim(-2.6, 2.7)
    ax_phys.set_ylim(-1.35, 5.15)
    ax_phys.set_aspect('equal')
    ax_phys.axis('off')

    yc = 1.15 + 0.55 * (t / tb)
    draw_rocket_cutaway(ax_phys, 0.0, yc, fuel_frac)

    # 1) 일정 추력 T = m'u = -m_dot u (우측 하단 상향 빨간 화살표 - 길이 고정)
    ax_phys.annotate('', xy=(0.55, yc + 0.95), xytext=(0.55, yc - 0.20),
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=3.0, mutation_scale=18), zorder=7)
    ax_phys.text(0.68, yc + 0.35,
                 f'추력 일정!\n$T = m\'u = -\\dot{{m}}u$\n$= {T_thrust/1000:.1f}\\,\\mathrm{{kN}}$',
                 fontsize=9.6, fontweight='bold', color='#d32f2f', va='center')

    # 2) 배기가스 상대속도 u (하향 파란 화살표)
    ax_phys.annotate('', xy=(-0.52, yc - 1.00), xytext=(-0.52, yc - 0.22),
                     arrowprops=dict(arrowstyle='->', color='#0277bd', lw=2.3, mutation_scale=15), zorder=7)
    ax_phys.text(-0.64, yc - 0.62, f'배기 상대속도\n$u = {u:.0f}\\,\\mathrm{{m/s}}$',
                 fontsize=9.2, fontweight='bold', color='#01579b', ha='right', va='center')

    # 3) 감소하는 자중 m(t)g (우측 상단 하향 보라/적갈색 화살표 - 길이 축소!)
    w_len = 0.28 + 0.65 * (m_curr / m0)
    ax_phys.annotate('', xy=(0.55, yc + 1.85 - w_len), xytext=(0.55, yc + 1.85),
                     arrowprops=dict(arrowstyle='->', color='#6a1b9a', lw=2.3, mutation_scale=15), zorder=7)
    ax_phys.text(0.68, yc + 1.62,
                 f'감소하는 중량\n$m(t)g = {W_curr/1000:.2f}\\,\\mathrm{{kN}}$\n$(m = {m_curr:.0f}\\,\\mathrm{{kg}})$',
                 fontsize=9.3, fontweight='bold', color='#6a1b9a', va='center')

    # 4) 급증하는 가속도 a(t) (좌측 상향 초록 화살표 - 길이 크게 신장!)
    a_len = 0.35 + 1.25 * (a_curr / a_final)
    ax_phys.annotate('', xy=(-0.62, yc + 0.55 + a_len), xytext=(-0.62, yc + 0.55),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=3.0, mutation_scale=18), zorder=7)
    ax_phys.text(-0.76, yc + 0.55 + a_len * 0.55,
                 f'가속도 급증!\n$a(t) = {a_curr:.1f}\\,\\mathrm{{m/s^2}}$\n$({a_curr/g:.1f}g)$\n$v = {v_curr:.0f}\\,\\mathrm{{m/s}}$',
                 fontsize=9.6, fontweight='bold', color='#1b5e20', ha='right', va='center')

    # 하단 핵심 정적분 공식 요약 박스
    eq_str = (
        r'운동방정식: $T - mg = m\frac{dv}{dt} \quad (T = m^\prime u = -\dot{m}u)$' '\n'
        r'변수분리 정적분: $\int_0^v dv = -u\int_{m_0}^m \frac{dm}{m} - g\int_0^t dt \;\Rightarrow\; v = u\ln\frac{m_0}{m} - gt$'
    )
    ax_phys.text(0.05, -0.92, eq_str, fontsize=9.3, ha='center', va='center', color='#1e3a5f',
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f4f8fb', edgecolor='#90caf9', lw=1.3))

    # ---------------- 2. 우측 1단: 질량 m(t) 선형 감소 ----------------
    ax_m.cla()
    ax_m.set_facecolor('#ffffff')
    ax_m.plot(t_dense, m_dense, color='#e65100', lw=2.3, label=r'$m(t) = m_0 - m^\prime t$')
    ax_m.axhline(mb, color='#78909c', ls='--', lw=1.2, label=r'구조물 질량 $m_b = 250\,\mathrm{kg}$')
    ax_m.fill_between(t_dense[t_dense <= t], mb, m_dense[t_dense <= t], color='#ffe0b2', alpha=0.55)
    ax_m.plot(t, m_curr, 'o', color='#e65100', markersize=6.5, zorder=5)
    ax_m.set_xlim(0, tb * 1.03)
    ax_m.set_ylim(0, 1120)
    ax_m.set_ylabel(r'$m(t)\ (\mathrm{kg})$', fontsize=9.8, fontweight='bold')
    ax_m.set_title(f'① 총질량 선형 감소: $m(t) = {m_curr:.0f}\\,\\mathrm{{kg}}$  (연료 잔량 {fuel_frac*100:.0f}%, 질량비 $m_0/m_b = 4$)',
                   fontsize=10.3, fontweight='bold', color='#1e3a5f')
    ax_m.grid(True, ls=':', alpha=0.45)
    ax_m.legend(loc='upper right', fontsize=8.3, framealpha=0.95)

    # ---------------- 3. 우측 2단: 가속도 a(t) 비선형 급증 ----------------
    ax_a.cla()
    ax_a.set_facecolor('#ffffff')
    ax_a.plot(t_dense, a_dense, color='#2e7d32', lw=2.4, label=r'실제 가속도 $a(t) = \frac{m^\prime u}{m(t)} - g$')
    ax_a.plot(t_dense, a_const_m, color='#90a4ae', ls='--', lw=1.5, label=r'질량 불변 가정 시 $a_0 = 20.2\,\mathrm{m/s^2}$')
    ax_a.plot(t, a_curr, 'o', color='#2e7d32', markersize=6.5, zorder=5)
    ax_a.set_xlim(0, tb * 1.03)
    ax_a.set_ylim(0, 125)
    ax_a.set_ylabel(r'$a(t)\ (\mathrm{m/s^2})$', fontsize=9.8, fontweight='bold')
    ax_a.set_title(f'② 추력은 일정하나 분모 $m(t)$ 감소로 가속도 5.5배 급증: $a(t) = {a_curr:.1f}\\,\\mathrm{{m/s^2}}$',
                   fontsize=10.3, fontweight='bold', color='#1e3a5f')
    ax_a.grid(True, ls=':', alpha=0.45)
    ax_a.legend(loc='upper left', fontsize=8.3, framealpha=0.95)

    # ---------------- 4. 우측 3단: 치올콥스키 속도 v(t) ----------------
    ax_v.cla()
    ax_v.set_facecolor('#ffffff')
    ax_v.plot(t_dense, v_ideal_dense, color='#00897b', ls='--', lw=1.7, label=r'무중력 이상 속도 $u\ln(m_0/m)$')
    ax_v.plot(t_dense, v_act_dense, color='#1565c0', lw=2.5, label=r'실제 상승 속도 $v(t) = u\ln(m_0/m) - gt$')

    mask = t_dense <= t
    ax_v.fill_between(t_dense[mask], v_act_dense[mask], v_ideal_dense[mask],
                      color='#ffcdd2', alpha=0.45, label=r'중력 속도 손실 $-gt$')
    ax_v.plot(t, v_curr, 'o', color='#d32f2f', markersize=6.8, zorder=6)

    ax_v.set_xlim(0, tb * 1.03)
    ax_v.set_ylim(0, 3050)
    ax_v.set_xlabel(r'연소 시간 $t\ (\mathrm{s})$', fontsize=10, fontweight='bold')
    ax_v.set_ylabel(r'$v(t)\ (\mathrm{m/s})$', fontsize=9.8, fontweight='bold')
    ax_v.set_title(f'③ 치올콥스키 로켓 속도: $v(t) = {v_curr:.0f}\\,\\mathrm{{m/s}}$  (연소 종료 $t_b=50\\,\\mathrm{{s}}$ 최대 $v_{{\\max}} = {v_max:.0f}\\,\\mathrm{{m/s}}$)',
                   fontsize=10.3, fontweight='bold', color='#1e3a5f')
    ax_v.grid(True, ls=':', alpha=0.45)
    ax_v.legend(loc='upper left', fontsize=8.2, framealpha=0.95)


anim = FuncAnimation(fig, update, frames=n_frames, interval=75)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_rocket_tsiolkovsky_thrust.gif')
anim.save(gif_path, writer='pillow', fps=14)
plt.close()
print(f'Saved: {gif_path}')
