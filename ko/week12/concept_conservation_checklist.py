"""
동역학 9판 제4장 4.5절: 에너지와 운동량 보존
보충 개념 애니메이션 2 - 다체계 보존 법칙 판별: 비탄성 결합 충돌 vs 무마찰 이동 경사대
- 순수 흰색 바탕 (#ffffff) & STIX 수식 표준 적용
- 좌측(사례 A): 수평 비탄성 연결 충돌 -> 선운동량 보존(ΔG_x = 0) O, 역학적 에너지 보존 X (ΔE < 0 소산)
- 우측(사례 B): 무마찰 이동 경사대 + 활강 블록 -> 수평 선운동량(ΔG_x = 0)과 역학적 에너지(ΔT + ΔV_g = 0) 동시 보존 O!
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

# ---------------- 사례 A 물리 매개변수 (비탄성 연결 충돌) ----------------
m1_A, m2_A = 4.0, 2.0               # kg
v10_A, v20_A = 3.0, 0.0             # m/s
vf_A = (m1_A * v10_A + m2_A * v20_A) / (m1_A + m2_A)  # 2.0 m/s
Gx0_A = m1_A * v10_A                # 12.0 N·s
E0_A = 0.5 * m1_A * v10_A**2        # 18.0 J
Ef_A = 0.5 * (m1_A + m2_A) * vf_A**2  # 12.0 J (6.0 J 손실)

# ---------------- 사례 B 물리 매개변수 (무마찰 이동 경사대 + 활강 블록) ----------------
M_cart, m_blk = 4.0, 2.0            # kg
g = 9.81
th_deg = 25.0
th = np.radians(th_deg)
h0 = 0.60                           # m
s_max = h0 / np.sin(th)             # 1.4197 m
E0_B = m_blk * g * h0               # 11.772 J
# (M + m) v = m s_dot cos(th) => s_dot = ((M+m)/(m cos th)) v
ratio_B = (M_cart + m_blk) / (m_blk * np.cos(th))  # 3.3101
# 0.5 M v^2 + 0.5 m [(s_dot cos th - v)^2 + (s_dot sin th)^2] = m g h0
coeff_v2 = 0.5 * M_cart + 0.5 * m_blk * (1.0 + ratio_B**2 - 2.0 * ratio_B * np.cos(th))
vf_B = np.sqrt(E0_B / coeff_v2)     # 1.180 m/s (경사대 우측 반동)
sdot_f_B = ratio_B * vf_B           # 3.906 m/s (블록 상대속력)
t_end_B = 2.0 * s_max / sdot_f_B    # 0.727 s

n_frames = 56
u_vals = np.linspace(0.0, 1.0, n_frames)  # 정규화 진행률 0 ~ 1

fig = plt.figure(figsize=(14, 6.5))
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, figure=fig, height_ratios=[1.25, 1.0],
              left=0.105, right=0.975, top=0.89, bottom=0.10, wspace=0.30, hspace=0.34)

ax_motA = fig.add_subplot(gs[0, 0])
ax_motB = fig.add_subplot(gs[0, 1])
ax_barA = fig.add_subplot(gs[1, 0])
ax_barB = fig.add_subplot(gs[1, 1])

def update(frame):
    u = u_vals[frame]

    # ==================== 좌상단: 사례 A 비탄성 충돌 모션 ====================
    ax_motA.cla()
    ax_motA.set_facecolor('#ffffff')
    ax_motA.set_xlim(-2.6, 3.2)
    ax_motA.set_ylim(-0.55, 1.95)
    ax_motA.set_aspect('equal')
    ax_motA.axis('off')
    ax_motA.set_title(r'사례 A: 비탄성 연결 충돌 ($\Delta G_x = 0$, $\Delta E_{\mathrm{mech}} < 0$)',
                      fontsize=12.2, fontweight='bold', color='#1a237e', pad=8)

    # 지면 레일
    ax_motA.add_patch(patches.Rectangle((-2.5, -0.35), 5.6, 0.35, facecolor='#ece4db', edgecolor='none'))
    ax_motA.plot([-2.5, 3.1], [0, 0], color='#37474f', lw=2.2)

    u_c = 0.45  # 충돌 시점
    w1, w2 = 1.05, 0.90
    gap0 = 0.95
    x2_0 = 0.25
    x1_0 = x2_0 - 0.5 * (w1 + w2) - gap0
    if u < u_c:
        f = u / u_c
        x1 = x1_0 + gap0 * f
        x2 = x2_0
        v1_now, v2_now = v10_A, 0.0
        E_now_A = E0_A
        coupled = False
    else:
        f = (u - u_c) / (1.0 - u_c)
        dx_post = 1.05 * f
        x2 = x2_0 + dx_post
        x1 = x2 - 0.5 * (w1 + w2)
        v1_now = v2_now = vf_A
        E_now_A = Ef_A
        coupled = True

    # 대차 1 (4 kg) & 대차 2 (2 kg)
    for xc, wc, col, edg, lbl in [
        (x1, w1, '#90caf9', '#1565c0', r'$4\ \mathrm{kg}$'),
        (x2, w2, '#ffcc80', '#ef6c00', r'$2\ \mathrm{kg}$'),
    ]:
        for dxw in [-0.28 * wc, 0.28 * wc]:
            ax_motA.add_patch(patches.Circle((xc + dxw, 0.12), 0.12, facecolor='#78909c', edgecolor='#263238', lw=1.4, zorder=4))
        ax_motA.add_patch(patches.FancyBboxPatch((xc - wc/2, 0.24), wc, 0.56,
                                                 boxstyle='round,pad=0.02,rounding_size=0.06',
                                                 facecolor=col, edgecolor=edg, lw=1.8, zorder=3))
        ax_motA.text(xc, 0.52, lbl, fontsize=10, fontweight='bold', ha='center', va='center', color='#102027', zorder=5)

    # 연결 커플러 표시
    cx_mid = 0.5 * ((x1 + w1/2) + (x2 - w2/2))
    ax_motA.plot([x1 + w1/2, x1 + w1/2 + 0.07], [0.45, 0.45], color='#263238', lw=3.0)
    ax_motA.plot([x2 - w2/2 - 0.07, x2 - w2/2], [0.45, 0.45], color='#263238', lw=3.0)
    if coupled:
        ax_motA.plot(cx_mid, 0.45, 'o', color='#d32f2f', markersize=7, zorder=6)
        if u < u_c + 0.14:
            ax_motA.text(cx_mid, 1.02, r'소성·결합 손실 ($-6.0\ \mathrm{J}$)', fontsize=9.2, fontweight='bold',
                         color='#c62828', ha='center',
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffebee', edgecolor='#ef9a9a'))
        ax_motA.annotate('', xy=(cx_mid + 0.65, 1.32), xytext=(cx_mid - 0.45, 1.32),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5, mutation_scale=14))
        ax_motA.text(cx_mid + 0.10, 1.55, r'공통 속도 $v_f = 2.0\ \mathrm{m/s}$', fontsize=10, fontweight='bold',
                     color='#2e7d32', ha='center')
    else:
        ax_motA.annotate('', xy=(x1 + 0.48, 1.15), xytext=(x1 - 0.48, 1.15),
                         arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.3, mutation_scale=13))
        ax_motA.text(x1, 1.36, r'$v_{10} = 3.0\ \mathrm{m/s}$', fontsize=9.8, fontweight='bold', color='#2e7d32', ha='center')
        ax_motA.text(x2, 1.12, r'정지 ($0\ \mathrm{m/s}$)', fontsize=9.2, fontweight='bold', color='#616161', ha='center')

    # ==================== 우상단: 사례 B 무마찰 이동 경사대 + 블록 ====================
    ax_motB.cla()
    ax_motB.set_facecolor('#ffffff')
    ax_motB.set_xlim(-2.6, 3.2)
    ax_motB.set_ylim(-0.55, 1.95)
    ax_motB.set_aspect('equal')
    ax_motB.axis('off')
    ax_motB.set_title(r'사례 B: 무마찰 이동 경사대 ($\Delta G_x = 0$ 및 $\Delta T + \Delta V_g = 0$ 동시 성립!)',
                      fontsize=11.8, fontweight='bold', color='#1b5e20', pad=8)

    ax_motB.add_patch(patches.Rectangle((-2.5, -0.35), 5.6, 0.35, facecolor='#ece4db', edgecolor='none'))
    ax_motB.plot([-2.5, 3.1], [0, 0], color='#37474f', lw=2.2)

    # 등가속도 활강 진행률: s = s_max * u^2, 속도 = 최종속도 * u
    s_frac = u**2
    s_curr = s_max * s_frac
    v_cart = vf_B * u
    s_dot = sdot_f_B * u
    x_recoil = (m_blk * np.cos(th) / (M_cart + m_blk)) * s_curr  # 최대 0.429 m

    # 시각화 기하학
    xc_B = -0.35 + x_recoil * 1.35
    w_base = 2.55
    h_wedge = 1.12
    y_base = 0.24
    p_BL = np.array([xc_B - w_base/2, y_base])
    p_BR = np.array([xc_B + w_base/2, y_base])
    p_TR = np.array([xc_B + w_base/2, y_base + h_wedge])

    for dxw in [-0.85, 0.85]:
        ax_motB.add_patch(patches.Circle((xc_B + dxw, 0.12), 0.12, facecolor='#78909c', edgecolor='#263238', lw=1.4, zorder=4))
    wedge_poly = patches.Polygon([p_BL, p_BR, p_TR], facecolor='#b2dfdb', edgecolor='#00695c', lw=1.8, zorder=3)
    ax_motB.add_patch(wedge_poly)
    ax_motB.text(xc_B + 0.42, y_base + 0.26, r'$M = 4\ \mathrm{kg}$', fontsize=9.8, fontweight='bold', color='#004d40', ha='center')
    ax_motB.text(p_BL[0] + 0.48, y_base + 0.10, r'$25^\circ$', fontsize=9.2, fontweight='bold', color='#004d40')

    # 경사면 단위벡터 (우상단 -> 좌하단 방향)
    vec_slope = p_BL - p_TR
    L_slope = np.linalg.norm(vec_slope)
    u_down = vec_slope / L_slope
    n_out = np.array([-np.sin(np.arctan2(h_wedge, w_base)), np.cos(np.arctan2(h_wedge, w_base))])
    ang_vis = np.degrees(np.arctan2(h_wedge, w_base))

    pos_along = 0.32 + (L_slope - 0.72) * s_frac
    blk_bot = p_TR + pos_along * u_down
    blk_w, blk_h = 0.48, 0.30
    blk_ctr = blk_bot + (blk_h / 2.0) * n_out
    blk_rect = patches.Rectangle((-blk_w/2, -blk_h/2), blk_w, blk_h,
                                 facecolor='#ef9a9a', edgecolor='#b71c1c', lw=1.8, zorder=5)
    t_blk = plt.matplotlib.transforms.Affine2D().rotate_deg(ang_vis).translate(blk_ctr[0], blk_ctr[1]) + ax_motB.transData
    blk_rect.set_transform(t_blk)
    ax_motB.add_patch(blk_rect)
    ax_motB.text(blk_ctr[0], blk_ctr[1], r'$2\ \mathrm{kg}$', fontsize=8.8, fontweight='bold',
                 rotation=ang_vis, ha='center', va='center', color='#4a0e0e', zorder=6)

    if u > 0.08:
        # 경사대 우측 반동 화살표
        ax_motB.annotate('', xy=(p_BR[0] + 0.15 + 0.55 * u, y_base + 0.35), xytext=(p_BR[0] + 0.08, y_base + 0.35),
                         arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.3, mutation_scale=13))
        ax_motB.text(p_BR[0] + 0.12, y_base + 0.56, rf'$v = {v_cart:.2f}\ \mathrm{{m/s}}$',
                     fontsize=9.3, fontweight='bold', color='#1565c0', ha='left')
        # 블록 상대 활강 화살표
        v_st = blk_ctr + 0.32 * u_down + 0.14 * n_out
        v_en = v_st + (0.25 + 0.48 * u) * u_down
        ax_motB.annotate('', xy=v_en, xytext=v_st,
                         arrowprops=dict(arrowstyle='->', color='#c62828', lw=2.2, mutation_scale=13))
        ax_motB.text(v_st[0] - 0.15, v_st[1] + 0.22, rf'$\dot{{s}} = {s_dot:.2f}\ \mathrm{{m/s}}$',
                     fontsize=9.3, fontweight='bold', color='#c62828', ha='right')

    # ==================== 좌하단: 사례 A 정량 보존 막대 차트 ====================
    ax_barA.cla()
    ax_barA.set_facecolor('#ffffff')
    ax_barA.set_xlim(0, 162)
    ax_barA.set_ylim(-0.85, 2.45)
    ax_barA.spines['top'].set_visible(False)
    ax_barA.spines['right'].set_visible(False)
    ax_barA.set_yticks([0.4, 1.5])
    ax_barA.set_yticklabels([r'에너지 $E$', r'선운동량 $G_x$'], fontsize=9.8, fontweight='bold')
    ax_barA.set_xlabel('초기값 대비 보존 비율 (%)', fontsize=9.3, fontweight='bold')
    ax_barA.axvline(100, color='#757575', ls='--', lw=1.3)

    pct_E_A = 100.0 * (E_now_A / E0_A)
    col_EA = '#2e7d32' if not coupled else '#d32f2f'
    ax_barA.barh(1.5, 100.0, height=0.52, color='#1976d2', edgecolor='#0d47a1', lw=1.3)
    ax_barA.barh(0.4, pct_E_A, height=0.52, color=col_EA, edgecolor='#263238', lw=1.3)
    ax_barA.text(103, 1.5, r'$12.0\ \mathrm{N\cdot s}$ (보존 O)', fontsize=9.0, fontweight='bold', color='#0d47a1', va='center')
    lbl_EA = rf'${E_now_A:.1f}\ \mathrm{{J}}$ ({pct_E_A:.0f}% ' + ('유지)' if not coupled else '소산 X)')
    ax_barA.text(pct_E_A + 3, 0.4, lbl_EA, fontsize=9.0, fontweight='bold', color=col_EA, va='center')
    ax_barA.text(1.0, -0.58, r'[보존 O] $\sum F_x = 0 \Rightarrow \Delta G_x = 0$  |  [보존 X] $\Delta E_{\mathrm{mech}} = -6.0\ \mathrm{J}$',
                 fontsize=8.6, fontweight='bold', color='#37474f')

    # ==================== 우하단: 사례 B 정량 보존 막대 차트 ====================
    ax_barB.cla()
    ax_barB.set_facecolor('#ffffff')
    ax_barB.set_xlim(0, 21.5)
    ax_barB.set_ylim(-0.85, 2.45)
    ax_barB.spines['top'].set_visible(False)
    ax_barB.spines['right'].set_visible(False)
    ax_barB.set_yticks([0.4, 1.5])
    ax_barB.set_yticklabels([r'총 에너지 $E$', r'수평 $|p_x|$'], fontsize=9.8, fontweight='bold')
    ax_barB.set_xlabel(r'크기 비교 ($\mathrm{N\cdot s}$ 및 $\mathrm{J}$)', fontsize=9.3, fontweight='bold')

    Vg_B = E0_B * (1.0 - s_frac)
    T_cart_B = 0.5 * M_cart * v_cart**2
    T_blk_B = E0_B - Vg_B - T_cart_B
    px_mag = M_cart * v_cart  # |p_cart| = |p_block,x| -> 합산 G_x = 0!

    # 수평 운동량 상쇄 표시 (경사대 +px vs 블록 -px -> 합 0)
    ax_barB.barh(1.64, px_mag, height=0.25, color='#1976d2', label=r'경사대 $+M v$')
    ax_barB.barh(1.36, px_mag, height=0.25, color='#e53935', label=r'블록 $|p_{x,\mathrm{blk}}|$')
    ax_barB.text(px_mag + 0.35, 1.5, rf'$\pm{px_mag:.2f} \Rightarrow G_x = 0$ (보존 O)',
                 fontsize=8.9, fontweight='bold', color='#1b5e20', va='center')

    # 총 역학적 에너지 누적 막대 (V_g + T_blk + T_cart = 11.77 J 일정!)
    ax_barB.barh(0.4, Vg_B, height=0.52, color='#ffb74d', edgecolor='#e65100', lw=1.0, label=r'$V_g$')
    ax_barB.barh(0.4, T_blk_B, left=Vg_B, height=0.52, color='#ef5350', edgecolor='#b71c1c', lw=1.0, label=r'$T_{\mathrm{blk}}$')
    ax_barB.barh(0.4, T_cart_B, left=Vg_B + T_blk_B, height=0.52, color='#42a5f5', edgecolor='#0d47a1', lw=1.0, label=r'$T_{\mathrm{cart}}$')
    ax_barB.axvline(E0_B, ymin=0.18, ymax=0.56, color='#1b5e20', ls='--', lw=1.5)
    ax_barB.text(E0_B + 0.35, 0.4, r'$11.77\ \mathrm{J}$ 일정 (보존 O!)', fontsize=8.9, fontweight='bold', color='#1b5e20', va='center')
    ax_barB.text(0.15, -0.58, r'[보존 O] $\Delta G_x = 0$  |  [보존 O] 내부 수직항력 총일 $= 0 \Rightarrow \Delta T + \Delta V_g = 0$',
                 fontsize=8.4, fontweight='bold', color='#1b5e20')

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concept_conservation_checklist.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
