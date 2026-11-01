"""
보충 개념 애니메이션 2: 두 물체 충돌 시 내부 작용·반작용 충격량 상쇄와 선형 운동량 보존 원리
동역학 9판 (한국어판) - 제3장 3.9절 선형 운동량 보존 (교재 그림 3/13 원리 시각화)
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

# 질점 A (ma=2 kg, va1=+5 m/s -> Ga1=+10 N·s), 질점 B (mb=3 kg, vb1=-1 m/s -> Gb1=-3 N·s)
# 총 운동량 G_tot = +7.0 N·s 일정!
# 충돌 접촉 구간 t in [1.0, 2.0] s 동안 작용-반작용 충격량 J = 7.2 N·s 교환:
# 충돌 후: Ga2 = 10 - 7.2 = +2.8 N·s (va2 = +1.4 m/s), Gb2 = -3 + 7.2 = +4.2 N·s (vb2 = +1.4 m/s 일체화? 7/5 = 1.4! 10 - 2*1.4 = 7.2! 정확히 일치!)
ma, mb = 2.0, 3.0
va1, vb1 = 5.0, -1.0
Ga1, Gb1 = ma * va1, mb * vb1   # +10.0, -3.0 -> 합계 +7.0 N·s
vf = (Ga1 + Gb1) / (ma + mb)    # +1.40 m/s
J_tot = Ga1 - ma * vf           # 7.20 N·s

t1_c, t2_c = 1.0, 2.0

def contact_F(t):
    t = np.asarray(t)
    val = np.zeros_like(t, dtype=float)
    m_c = (t >= t1_c) & (t <= t2_c)
    # J = int_1^2 F_peak * sin^2(pi*(t-1)) dt = 0.5 * F_peak = 7.2 => F_peak = 14.4 N
    val[m_c] = 14.4 * (np.sin(np.pi * (t[m_c] - t1_c)) ** 2)
    return val

def impulse_J(t):
    if t <= t1_c:
        return 0.0
    elif t >= t2_c:
        return J_tot
    else:
        u = t - t1_c
        return 14.4 * (0.5 * u - np.sin(2.0 * np.pi * u) / (4.0 * np.pi))

n_frames = 66
t_arr = np.linspace(0.0, 3.2, n_frames)
t_plot = np.linspace(0.0, 3.2, 350)
Fp = contact_F(t_plot)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.15, 1.05], height_ratios=[1.05, 0.95],
              left=0.04, right=0.97, top=0.89, bottom=0.09, wspace=0.18, hspace=0.34)

ax_col = fig.add_subplot(gs[:, 0])
ax_imp = fig.add_subplot(gs[0, 1])
ax_mom = fig.add_subplot(gs[1, 1])

fig.suptitle(r"보충 개념 애니메이션 ②: 충돌 시 서로 미는 힘은 엄청 큰데, 왜 '합친 운동량'은 변하지 않을까요?",
             fontsize=13.8, fontweight='bold', color='#111827', y=0.965)

def update(frame):
    t = float(t_arr[frame])
    J = impulse_J(t)
    F_now = float(contact_F(t))

    Ga = Ga1 - J
    Gb = Gb1 + J
    va = Ga / ma
    vb = Gb / mb

    ax_col.clear()
    ax_imp.clear()
    ax_mom.clear()
    for ax in (ax_col, ax_imp, ax_mom):
        ax.set_facecolor('#ffffff')

    # =====================================================
    # [좌측 패널] 두 물체 충돌 및 작용·반작용 힘(-F, +F) 시각화
    # =====================================================
    ax_col.set_xlim(-3.2, 3.6)
    ax_col.set_ylim(-1.2, 4.3)
    ax_col.set_aspect('equal')
    ax_col.axis('off')
    ax_col.set_title("① 두 물체 충돌 시 작용·반작용 힘과 운동량 교환", fontsize=11.8, fontweight='bold', color='#1e293b', pad=6)

    ax_col.fill_between([-3.0, 3.4], -0.22, 0.0, color='#dfd9d2')
    ax_col.plot([-3.0, 3.4], [0.0, 0.0], color='#1e293b', lw=2.4)

    rA, rB = 0.36, 0.44
    if t < t1_c:
        dt_pre = t1_c - t
        xA = -0.36 - 1.65 * dt_pre
        xB = +0.44 + 0.55 * dt_pre
    elif t <= t2_c:
        prog = (t - t1_c) / (t2_c - t1_c)
        x_mid = 0.0 + 0.35 * prog
        xA = x_mid - rA * 0.94
        xB = x_mid + rB * 0.94
    else:
        dt_post = t - t2_c
        x_mid = 0.35 + 1.15 * dt_post
        xA = x_mid - rA
        xB = x_mid + rB

    ax_col.add_patch(patches.Circle((xA, rA), rA, facecolor='#93c5fd', edgecolor='#1d4ed8', lw=2.2, zorder=4))
    ax_col.add_patch(patches.Circle((xB, rB), rB, facecolor='#86efac', edgecolor='#15803d', lw=2.2, zorder=4))
    ax_col.text(xA, rA, "$m_a$\n2 kg", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e3a8a', zorder=5)
    ax_col.text(xB, rB, "$m_b$\n3 kg", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#14532d', zorder=5)

    # 속도 벡터 표시
    ax_col.annotate('', xy=(xA + 0.22 * va, rA + 0.56), xytext=(xA, rA + 0.56),
                    arrowprops=dict(arrowstyle='->', color='#1d4ed8', lw=2.5, mutation_scale=15), zorder=6)
    ax_col.text(xA + 0.11 * va, rA + 0.75, rf"$v_a={va:+.1f}\ \mathrm{{m/s}}$", fontsize=9.5, fontweight='bold', color='#1d4ed8', ha='center')

    ax_col.annotate('', xy=(xB + 0.32 * vb, rB + 0.62), xytext=(xB, rB + 0.62),
                    arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.5, mutation_scale=15), zorder=6)
    ax_col.text(xB + 0.16 * vb, rB + 0.82, rf"$v_b={vb:+.1f}\ \mathrm{{m/s}}$", fontsize=9.5, fontweight='bold', color='#15803d', ha='center')

    # 접촉 중 작용·반작용 힘 화살표 (-F on A, +F on B)
    if F_now > 0.2:
        xc = 0.5 * (xA + rA + xB - rB)
        flen = 0.25 + 0.08 * F_now
        ax_col.add_patch(patches.Circle((xc, rA), 0.14, facecolor='#fde047', alpha=0.75, zorder=5.5))
        ax_col.annotate('', xy=(xc - flen, rA - 0.12), xytext=(xc, rA - 0.12),
                        arrowprops=dict(arrowstyle='->', color='#e11d48', lw=3.0, mutation_scale=16), zorder=7)
        ax_col.annotate('', xy=(xc + flen, rA - 0.12), xytext=(xc, rA - 0.12),
                        arrowprops=dict(arrowstyle='->', color='#e11d48', lw=3.0, mutation_scale=16), zorder=7)
        ax_col.text(xc - 0.55 * flen, -0.48, rf"$-F(t)=-{F_now:.1f}\ \mathrm{{N}}$", fontsize=9.5, fontweight='bold', color='#be123c', ha='right')
        ax_col.text(xc + 0.55 * flen, -0.48, rf"$+F(t)=+{F_now:.1f}\ \mathrm{{N}}$", fontsize=9.5, fontweight='bold', color='#be123c', ha='left')

    # [말풍선 보충 설명]
    bubble = (
        "[말풍선 보충 설명] '내부 힘 상쇄' 한눈에 이해하기!\n"
        "• 충돌하는 동안 A는 왼쪽으로(-F), B는 오른쪽으로(+F) 똑같은 크기의 힘을 받아요.\n"
        "• 따라서 A가 잃은 운동량(-7.2 N·s)만큼 B가 정확히 얻게(+7.2 N·s) 되어,\n"
        "  두 물체를 하나로 묶어 보면 내부 충격량의 합이 (-7.2) + (+7.2) = 0 이 됩니다!\n"
        "• 결과: 외부 힘이 없으면 충돌 전후 합친 운동량($G_a + G_b = +7.0$ N·s)은 100% 보존!"
    )
    ax_col.text(-3.05, 4.18, bubble, fontsize=9.0, color='#78350f', va='top', ha='left', linespacing=1.40,
                bbox=dict(boxstyle='round,pad=0.45', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.6))

    eq_bot = (
        "전체 운동량 변화 "
        + r"$\Delta\mathbf{G} = \int_{t_1}^{t_2} (+\mathbf{F})\,dt + \int_{t_1}^{t_2} (-\mathbf{F})\,dt = \mathbf{0}"
        + r"\;\Rightarrow\; m_a\mathbf{v}_{a1} + m_b\mathbf{v}_{b1} = m_a\mathbf{v}_{a2} + m_b\mathbf{v}_{b2}$"
    )
    ax_col.text(0.2, -0.92, eq_bot, fontsize=10.0, color='#0f172a', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.38', facecolor='#eff6ff', edgecolor='#60a5fa', lw=1.4))

    # =====================================================
    # [우측 상단] 작용·반작용 충격량 넓이 상쇄 (+∫F dt vs -∫F dt)
    # =====================================================
    ax_imp.set_xlim(0.0, 3.2)
    ax_imp.set_ylim(-16.5, 16.5)
    ax_imp.set_ylabel("접촉력 (N)", fontsize=9.8, fontweight='bold')
    ax_imp.set_title(r"② 작용·반작용 충격량 넓이 상쇄: $+\int_{t_1}^{t_2} F\,dt - \int_{t_1}^{t_2} F\,dt = 0$",
                     fontsize=10.6, fontweight='bold', color='#1e293b', pad=5)
    ax_imp.axhline(0, color='#111827', lw=1.2)
    ax_imp.grid(True, ls=':', alpha=0.5)

    ax_imp.plot(t_plot, +Fp, color='#15803d', lw=2.3, label=r'B가 받는 힘 $+F(t)$')
    ax_imp.plot(t_plot, -Fp, color='#1d4ed8', lw=2.3, label=r'A가 받는 힘 $-F(t)$')
    mask = t_plot <= t
    ax_imp.fill_between(t_plot[mask], 0, +Fp[mask], color='#86efac', alpha=0.45)
    ax_imp.fill_between(t_plot[mask], 0, -Fp[mask], color='#93c5fd', alpha=0.45)
    ax_imp.text(2.08, +9.5, rf"$+\int_{{t_1}}^{{t}} F\,dt = +{J:.1f}\ \mathrm{{N\cdot s}}$", fontsize=9.2, fontweight='bold', color='#15803d')
    ax_imp.text(2.08, -10.5, rf"$-\int_{{t_1}}^{{t}} F\,dt = -{J:.1f}\ \mathrm{{N\cdot s}}$", fontsize=9.2, fontweight='bold', color='#1d4ed8')
    ax_imp.legend(loc='upper left', fontsize=8.2)

    # =====================================================
    # [우측 하단] 개별 운동량 변화 vs 전체 운동량 일정(보존) 곡선
    # =====================================================
    Ga_curve = np.array([Ga1 - impulse_J(tt) for tt in t_plot])
    Gb_curve = np.array([Gb1 + impulse_J(tt) for tt in t_plot])
    Gtot_curve = Ga_curve + Gb_curve

    ax_mom.set_xlim(0.0, 3.2)
    ax_mom.set_ylim(-5.0, 12.5)
    ax_mom.set_xlabel("시간 $t$ (s)", fontsize=9.8, fontweight='bold')
    ax_mom.set_ylabel(r"선형 운동량 ($\mathrm{N\cdot s}$)", fontsize=9.8, fontweight='bold')
    ax_mom.set_title(r"③ 개별 운동량은 변해도 합계 $G_a + G_b = +7.0\ \mathrm{N\cdot s}$ 는 항상 일정!",
                     fontsize=10.5, fontweight='bold', color='#1e293b', pad=5)
    ax_mom.axhline(0, color='#64748b', lw=0.9)
    ax_mom.grid(True, ls=':', alpha=0.5)

    ax_mom.plot(t_plot, Ga_curve, color='#1d4ed8', lw=2.0, ls='--', label=r'$G_a(t) = m_a v_a$')
    ax_mom.plot(t_plot, Gb_curve, color='#15803d', lw=2.0, ls='--', label=r'$G_b(t) = m_b v_b$')
    ax_mom.plot(t_plot, Gtot_curve, color='#e11d48', lw=3.0, label=r'전체 합계 $G_a + G_b = 7.0\ \mathrm{N\cdot s}$ (보존!)')
    ax_mom.plot([t, t, t], [Ga, Gb, Ga + Gb], 'o', color='#111827', markersize=6)
    ax_mom.legend(loc='lower right', fontsize=8.0)

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_internal_force_cancel.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=90)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved concept_internal_force_cancel.gif")
