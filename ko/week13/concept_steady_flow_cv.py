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
동역학 9판 제4장 4.6절: 정상 질량유동 (Steady Mass Flow)
보충 개념 애니메이션 1 - 검사체적(Control Volume) 정상 질량유동 원리와 절단 배관 정압력 vs 자유분류 비교
- 순수 흰색 배경 (#ffffff) & 2분할 패널 레이아웃 (14 x 6.5)
- Meriam 그림 4/5 기반 증분 질량 Delta m = m' Delta t 추적, 내부 운동량 상쇄 원리, 압력 외력 주의사항 시각화
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

n_frames = 54

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.18, 1.02]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.07, left=0.04, right=0.97, wspace=0.12)


def get_cv_duct():
    """Meriam 그림 4/5 형태의 완만한 곡관 검사체적 기하 생성"""
    s = np.linspace(0.0, 1.0, 60)[:, None]
    P0 = np.array([2.0, 3.35])
    P1 = np.array([3.9, 3.45])
    P2 = np.array([5.5, 4.55])
    P3 = np.array([7.2, 5.85])

    center = ((1 - s)**3) * P0 + 3 * ((1 - s)**2) * s * P1 + 3 * (1 - s) * (s**2) * P2 + (s**3) * P3
    dcenter = 3 * ((1 - s)**2) * (P1 - P0) + 6 * (1 - s) * s * (P2 - P1) + 3 * (s**2) * (P3 - P2)
    tang = dcenter / np.linalg.norm(dcenter, axis=1, keepdims=True)
    norm = np.column_stack([-tang[:, 1], tang[:, 0]])

    # 입구 반폭 r1 = 0.62 -> 출구 반폭 r2 = 0.36 (A1 > A2 -> v1 < v2)
    r_prof = 0.62 * (1.0 - s[:, 0]) + 0.36 * s[:, 0]
    upper = center + norm * r_prof[:, None]
    lower = center - norm * r_prof[:, None]
    return center, upper, lower, tang, norm, r_prof


center_pts, upper_pts, lower_pts, tang_pts, norm_pts, r_prof = get_cv_duct()
p1_c, t1, n1, r1 = center_pts[0], tang_pts[0], norm_pts[0], r_prof[0]
p2_c, t2, n2, r2 = center_pts[-1], tang_pts[-1], norm_pts[-1], r_prof[-1]


def make_parcel_poly(base_pt, tang_v, norm_v, half_w, s_start, s_end):
    """입구 또는 출구 방향 접선을 따라 두께 [s_start, s_end]인 미소 유체 덩어리 폴리곤"""
    c0 = base_pt + s_start * tang_v
    c1 = base_pt + s_end * tang_v
    return np.array([
        c0 - half_w * norm_v,
        c1 - half_w * norm_v,
        c1 + half_w * norm_v,
        c0 + half_w * norm_v,
    ])


def update(frame):
    # 0 -> 1 주기적 진행률 (시각 t 에서 t + Delta t 로 미소 질량 Delta m 이동)
    cyc = (frame % n_frames) / (n_frames - 1)
    prog = 0.5 - 0.5 * np.cos(np.pi * min(1.0, cyc * 1.25))  # 마지막 20% 프레임은 완료 상태 유지
    phase_stream = (frame * 0.06) % 1.0

    # ---------------- 1. 좌측 패널: 그림 4/5 검사체적 및 증분 질량 Delta m 이동 ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(0.2, 9.6)
    ax_main.set_ylim(0.7, 7.9)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # 입구/출구 연장 유로 배경 가이드
    in_guide = make_parcel_poly(p1_c, t1, n1, r1, -1.25, 0.0)
    out_guide = make_parcel_poly(p2_c, t2, n2, r2, 0.0, 1.65)
    ax_main.add_patch(patches.Polygon(in_guide, facecolor='#f1f5f9', edgecolor='#cbd5e1', ls=':', lw=1.2, zorder=1))
    ax_main.add_patch(patches.Polygon(out_guide, facecolor='#f1f5f9', edgecolor='#cbd5e1', ls=':', lw=1.2, zorder=1))

    # 고정 검사체적(CV) 내부 유체 영역 (하늘색, 정상유동이므로 내부 운동량 G_CV 일정)
    cv_poly = np.vstack([lower_pts, upper_pts[::-1]])
    ax_main.add_patch(patches.Polygon(cv_poly, facecolor='#dbeafe', edgecolor='none', alpha=0.88, zorder=2))

    # 상/하 유로 벽면 (굵은 회남색 실선)
    ax_main.plot(upper_pts[:, 0], upper_pts[:, 1], color='#1e293b', lw=2.5, zorder=5)
    ax_main.plot(lower_pts[:, 0], lower_pts[:, 1], color='#1e293b', lw=2.5, zorder=5)

    # 입구 유입 미소 질량 Delta m (시각 t -> 시각 t + Delta t 동안 CV 안으로 밀려 들어감)
    # A1*ds1 = A2*ds2 체적 보존 반영: ds1_max = 0.85, ds2_max = 1.46
    ds1_max = 0.85
    ds2_max = 1.46
    in_shift = -ds1_max * (1.0 - prog)
    in_parcel = make_parcel_poly(p1_c, t1, n1, r1 * 0.96, in_shift, in_shift + ds1_max)
    ax_main.add_patch(patches.Polygon(in_parcel, facecolor='#60a5fa', edgecolor='#1d4ed8', lw=1.8, alpha=0.82, zorder=3))

    # 출구 유출 미소 질량 Delta m (동일 질량이 출구 단면 2 바깥으로 밀려 나감)
    out_parcel = make_parcel_poly(p2_c, t2, n2, r2 * 0.95, 0.0, max(0.04, prog * ds2_max))
    ax_main.add_patch(patches.Polygon(out_parcel, facecolor='#fbbf24', edgecolor='#b45309', lw=1.8, alpha=0.85, zorder=3))

    # 고정 검사체적(Control Volume) 경계선 (붉은 점선 폐곡선)
    ax_main.plot(cv_poly[:, 0], cv_poly[:, 1], color='#dc2626', ls='--', lw=2.0, zorder=6)
    ax_main.plot([cv_poly[-1, 0], cv_poly[0, 0]], [cv_poly[-1, 1], cv_poly[0, 1]], color='#dc2626', ls='--', lw=2.0, zorder=6)

    # 내부 정상유동 유선 입자 마커
    for k in range(6):
        f_idx = ((k / 6.0) + phase_stream) % 1.0
        idx = int(f_idx * (len(center_pts) - 1))
        ax_main.plot(center_pts[idx, 0], center_pts[idx, 1], 'o', color='#1d4ed8', markersize=4.5, zorder=4)

    # 단면 1 속도 벡터 v1 및 압력 힘 p1*A1
    v1_start = p1_c - 1.15 * t1
    v1_end = p1_c - 0.18 * t1
    ax_main.annotate('', xy=v1_end, xytext=v1_start,
                     arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.5, mutation_scale=14), zorder=7)
    ax_main.text(v1_start[0] + 0.35, v1_start[1] + 0.35, r'$\mathbf{v}_1$', fontsize=12, fontweight='bold', color='#15803d')
    ax_main.text(p1_c[0] - 0.15, p1_c[1] + r1 + 0.30, r'단면 ① ($A_1,\ p_1$)', fontsize=10.5, fontweight='bold', color='#1e3a8a', ha='center')

    # 입구 정압력 외력 p1*A1 (단면 바깥에서 안쪽으로 미는 힘)
    p1_force_st = p1_c - 1.15 * t1 - 0.42 * n1
    p1_force_ed = p1_c - 0.12 * t1 - 0.42 * n1
    ax_main.annotate('', xy=p1_force_ed, xytext=p1_force_st,
                     arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2, mutation_scale=13), zorder=7)
    ax_main.text(p1_force_st[0] - 0.05, p1_force_st[1] - 0.28, r'$p_1 A_1$', fontsize=10.8, fontweight='bold', color='#dc2626')

    # 단면 2 속도 벡터 v2 및 압력 힘 p2*A2
    v2_start = p2_c + 0.25 * t2
    v2_end = p2_c + 1.65 * t2
    ax_main.annotate('', xy=v2_end, xytext=v2_start,
                     arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.6, mutation_scale=15), zorder=7)
    ax_main.text(v2_end[0] + 0.12, v2_end[1] + 0.08, r'$\mathbf{v}_2$', fontsize=12, fontweight='bold', color='#15803d')
    ax_main.text(p2_c[0] - 0.55, p2_c[1] + r2 + 0.36, r'단면 ② ($A_2,\ p_2$)', fontsize=10.5, fontweight='bold', color='#1e3a8a', ha='center')

    # 출구 정압력 외력 p2*A2 (단면 바깥에서 안쪽으로 역방향 미는 힘)
    p2_force_st = p2_c + 1.25 * t2 - 0.38 * n2
    p2_force_ed = p2_c + 0.12 * t2 - 0.38 * n2
    ax_main.annotate('', xy=p2_force_ed, xytext=p2_force_st,
                     arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2, mutation_scale=13), zorder=7)
    ax_main.text(p2_force_st[0] + 0.10, p2_force_st[1] - 0.18, r'$p_2 A_2$', fontsize=10.8, fontweight='bold', color='#dc2626')

    # 검사체적 내부 텍스트 및 외력 합력 Sigma F
    mid_cv = center_pts[28]
    ax_main.text(mid_cv[0] - 0.15, mid_cv[1] + 0.12,
                 '고정 검사체적 (CV)\n' + r'$\mathbf{G}_{\mathrm{CV}} = \mathrm{const}$',
                 fontsize=9.8, fontweight='bold', color='#1e3a8a', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.22', facecolor='#ffffff', edgecolor='#93c5fd', alpha=0.92), zorder=7)

    # 외력 합력 화살표 Sigma F
    f_ext_ed = lower_pts[30]
    f_ext_st = f_ext_ed + np.array([1.15, -1.05])
    ax_main.annotate('', xy=f_ext_ed, xytext=f_ext_st,
                     arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.8, mutation_scale=16), zorder=7)
    ax_main.text(f_ext_st[0] + 0.10, f_ext_st[1] - 0.12, r'벽면·외력 $\Sigma\mathbf{F}$',
                 fontsize=10.8, fontweight='bold', color='#dc2626')

    # 기준점 O 및 모멘트 팔 d1, d2 표시 (하단 우측에 깔끔하게 배치)
    O_pt = np.array([6.6, 1.85])
    ax_main.plot(O_pt[0], O_pt[1], 'ko', markersize=5.5, zorder=7)
    ax_main.text(O_pt[0] + 0.20, O_pt[1] - 0.08, r'모멘트 기준점 $O$', fontsize=10.2, fontweight='bold', color='#1e293b')
    # O에서 v1 연장선까지 수선 d1 표시
    foot1 = p1_c + np.dot(O_pt - p1_c, t1) * t1
    ax_main.plot([p1_c[0], foot1[0] + 0.4 * t1[0]], [p1_c[1], foot1[1] + 0.4 * t1[1]], color='#94a3b8', ls=':', lw=1.1)
    ax_main.annotate('', xy=foot1, xytext=O_pt, arrowprops=dict(arrowstyle='<->', color='#475569', lw=1.3, ls='--'))
    ax_main.text(0.5 * (O_pt[0] + foot1[0]) + 0.18, 0.5 * (O_pt[1] + foot1[1]), r'$d_1$', fontsize=10.5, fontweight='bold', color='#334155')

    # 미소 질량 안내 배지 (상단 좌측)
    ax_main.text(0.45, 7.25,
                 f"[시간 진행: $t \\rightarrow t + \\Delta t$ ({prog*100:.0f}%)]\n"
                 "• 파란 블록: 입구 유입 질량 " + r"$\Delta m = m'\Delta t$" + "\n"
                 "• 노란 블록: 출구 유출 질량 " + r"$\Delta m = m'\Delta t$" + " (질량보존 동일!)",
                 fontsize=9.6, fontweight='bold', color='#1e293b', va='top', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.38', facecolor='#f8fafc', edgecolor='#cbd5e1'))

    # 하단 수식 요약 배너
    ax_main.text(4.9, 1.02,
                 "내부 운동량 " + r"$\mathbf{G}_{\mathrm{CV}}$" + "는 정상유동에서 불변이므로 상쇄!  "
                 + r"$\Rightarrow\ \mathbf{\Sigma F = m'(\mathbf{v}_2 - \mathbf{v}_1)}$",
                 fontsize=10.3, fontweight='bold', color='#1e3a8a', ha='center',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#eff6ff', edgecolor='#93c5fd'))

    ax_main.set_title('개념 1: 정상 질량유동 검사체적(CV)과 운동량 보존 원리 (그림 4/5)', fontsize=13.0, fontweight='bold', pad=10)

    # ---------------- 2. 우측 패널: 유도 과정 & 절단 배관 압력 vs 자유분류 비교 ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')

    ax_calc.text(5.0, 9.60, '절단 배관 정압력($pA$) vs 대기 개방 자유분류($p=0$) 핵심 구분',
                 fontsize=11.0, fontweight='bold', ha='center', color='#1e3a8a')

    # 좌측 미니 카드: 절단 배관 단면 (예제 4.8)
    ax_calc.add_patch(patches.FancyBboxPatch((0.35, 6.75), 4.35, 2.45, boxstyle='round,pad=0.15',
                                             facecolor='#fef2f2', edgecolor='#ef4444', lw=1.5))
    ax_calc.text(2.52, 8.90, '① 배관 절단 단면 (예제 4.8)', fontsize=9.8, fontweight='bold', ha='center', color='#b91c1c')
    # 미니 파이프 그림
    ax_calc.add_patch(patches.Rectangle((1.55, 7.65), 1.9, 0.65, facecolor='#dbeafe', edgecolor='#1e293b', lw=1.6))
    ax_calc.plot([1.55, 1.55], [7.52, 8.43], color='#dc2626', ls='--', lw=1.8)
    ax_calc.annotate('', xy=(1.52, 7.98), xytext=(0.55, 7.98),
                     arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.3, mutation_scale=13))
    ax_calc.text(1.02, 8.28, r'$p A_0$', fontsize=10.2, fontweight='bold', color='#dc2626', ha='center')
    ax_calc.text(2.52, 7.12, '계기압력 ' + r'$p > 0$' + ' 존재!\n외력 ' + r'$+pA$' + ' 반드시 포함',
                 fontsize=9.1, fontweight='bold', color='#7f1d1d', ha='center', va='center', linespacing=1.35)

    # 우측 미니 카드: 대기 개방 자유분류 (예제 4.6, 문제 4/31, 4/37)
    ax_calc.add_patch(patches.FancyBboxPatch((5.30, 6.75), 4.35, 2.45, boxstyle='round,pad=0.15',
                                             facecolor='#f0fdf4', edgecolor='#22c55e', lw=1.5))
    ax_calc.text(7.48, 8.90, '② 대기 개방 자유분류 (예제 4.6)', fontsize=9.8, fontweight='bold', ha='center', color='#15803d')
    ax_calc.add_patch(patches.Rectangle((6.25, 7.72), 2.2, 0.50, facecolor='#bae6fd', edgecolor='#0284c7', lw=1.2))
    ax_calc.plot([6.25, 6.25], [7.58, 8.36], color='#15803d', ls='--', lw=1.6)
    ax_calc.text(7.35, 7.97, r'$p = p_{\mathrm{atm}} \Rightarrow p_{\mathrm{gauge}} = 0$',
                 fontsize=9.2, fontweight='bold', color='#0f766e', ha='center', va='center')
    ax_calc.text(7.48, 7.12, '사방이 대기압으로 평형!\n단면 압력 힘 ' + r'$pA = 0$' + ' 생략',
                 fontsize=9.1, fontweight='bold', color='#14532d', ha='center', va='center', linespacing=1.35)

    # 중앙 카드: 식 (4.17)~(4.19) 정량 유도 요약
    sol_text = (
        "[정상 질량유동 지배방정식 유도 (식 4.17 ~ 4.19)]\n"
        "1) 연속방정식(질량보존): " + r"$m' = \frac{dm}{dt} = \rho_1 A_1 v_1 = \rho_2 A_2 v_2$" + "  [단위: kg/s]\n"
        "2) 미소 시간 " + r"$\Delta t$" + " 동안 닫힌 질량계의 선운동량 변화:\n"
        r"   $\Sigma\mathbf{F}\,\Delta t = (\mathbf{G}_{\mathrm{CV}} + \Delta m\,\mathbf{v}_2) - (\mathbf{G}_{\mathrm{CV}} + \Delta m\,\mathbf{v}_1) = \Delta m(\mathbf{v}_2 - \mathbf{v}_1)$" + "\n"
        "3) 양변을 " + r"$\Delta t$" + "로 나누어 극한 취함 (" + r"$\Delta m / \Delta t \to m'$" + "):\n"
        "   • 힘-선운동량: " + r"$\mathbf{\Sigma F = m'(\mathbf{v}_2 - \mathbf{v}_1) = m'\Delta\mathbf{v}}$" + "   (식 4.18)\n"
        "   • 모멘트-각운동량: " + r"$\mathbf{\Sigma M_O = m'(v_2 d_2 - v_1 d_1)}$" + "   (식 4.19)"
    )
    ax_calc.text(5.0, 4.45, sol_text, fontsize=9.35, ha='center', va='center', linespacing=1.42,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#cbd5e1'))

    # 하단 노란 말풍선 카드: 부호 실수 방지 핵심 팁
    tip_text = (
        "[실전 풀이 핵심 포인트 (말풍선 보충 설명)]\n"
        "• 부호 주의: " + r"$\Delta\mathbf{v} = \mathbf{v}_2$" + "(출구) " + r"$- \mathbf{v}_1$" + "(입구) 에서 설정한 좌표축 부호(+, -)를 반드시 유지!\n"
        "• 작용-반작용 구분: 식 4.18의 " + r"$\Sigma\mathbf{F}$" + "는 '유체가 받는 힘'이며, 날개·노즐이 받는 힘은 그 반작용(" + r"$-\mathbf{R}$" + ")입니다."
    )
    ax_calc.text(5.0, 1.35, tip_text, fontsize=9.15, ha='center', va='center', linespacing=1.45,
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    ax_calc.set_title('지배방정식 유도 및 경계 압력 조건 비교', fontsize=13.0, fontweight='bold', pad=10)


anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_steady_flow_cv.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
