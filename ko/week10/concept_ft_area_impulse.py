"""
보충 개념 애니메이션 1: 정적분 ∫_{t1}^{t2} F(t) dt 의 기하학적 의미 (힘-시간 그래프 넓이 = 운동량 변화량)
동역학 9판 (한국어판) - 제3장 3.9절 선형 충격량과 선형 운동량 기초 개념 시각화
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

# 예제 수치: 질량 m = 2 kg, t1 = 1 s (v1 = 2 m/s, G1 = 4 N·s) -> t2 = 5 s (총 넓이 = 16 N·s -> G2 = 20 N·s, v2 = 10 m/s)
# F(t) on [1, 5]: 사다리꼴 + 완만한 곡선 형태 F(t) = 4 + 3*sin(pi*(t-1)/4), 적분값 = 4*4 + 3*(4/pi)*2 = 16 + 24/pi?
# 깔끔한 정수를 위해 F(t) = 1 + 3*(t-1) on [1,3] (1->7, 넓이 8), 7 - 3*(t-3) on [3,5] (7->1, 넓이 8) => 총 넓이 정확히 16.0 N·s!
m = 2.0
t1, t2 = 1.0, 5.0
v1 = 2.0
G1 = m * v1   # 4.0 N·s

def F_func(t):
    t = np.asarray(t)
    val = np.ones_like(t, dtype=float)
    m1 = (t >= 1.0) & (t <= 3.0)
    m2 = (t > 3.0) & (t <= 5.0)
    val[m1] = 1.0 + 3.0 * (t[m1] - 1.0)
    val[m2] = 7.0 - 3.0 * (t[m2] - 3.0)
    val[t < 1.0] = 0.0
    val[t > 5.0] = 0.0
    return val

def impulse_up_to(t):
    if t <= 1.0:
        return 0.0
    elif t <= 3.0:
        dt = t - 1.0
        return 1.0 * dt + 1.5 * (dt ** 2)
    elif t <= 5.0:
        dt = t - 3.0
        return 8.0 + 7.0 * dt - 1.5 * (dt ** 2)
    else:
        return 16.0

n_frames = 68
t_arr = np.linspace(0.5, 5.6, n_frames)
t_plot = np.linspace(0.0, 6.0, 400)
F_plot = F_func(t_plot)

fig = plt.figure(figsize=(14, 6.5), dpi=100)
fig.patch.set_facecolor('#ffffff')
gs = GridSpec(2, 2, width_ratios=[1.08, 1.12], height_ratios=[1.15, 0.85],
              left=0.10, right=0.97, top=0.87, bottom=0.09, wspace=0.18, hspace=0.35)

ax_ft = fig.add_subplot(gs[0, 0])
ax_bar = fig.add_subplot(gs[1, 0])
ax_sim = fig.add_subplot(gs[:, 1])

fig.suptitle(r"보충 개념 애니메이션 ①: 정적분 $\int_{t_1}^{t_2} F(t)\,dt$는 왜 '힘-시간 그래프의 넓이'일까요?",
             fontsize=14.2, fontweight='bold', color='#111827', y=0.965)

def update(frame):
    t_curr = float(t_arr[frame])
    J_curr = impulse_up_to(t_curr)
    G_curr = G1 + J_curr
    v_curr = G_curr / m
    F_curr = float(F_func(t_curr))

    ax_ft.clear()
    ax_bar.clear()
    ax_sim.clear()
    for ax in (ax_ft, ax_bar, ax_sim):
        ax.set_facecolor('#ffffff')

    # 1) 좌상단: F-t 그래프 넓이 적분 과정 (리만 직사각형 조각 dt + 누적 면적)
    ax_ft.set_xlim(0.0, 6.0)
    ax_ft.set_ylim(0.0, 9.2)
    ax_ft.set_xlabel("시간 $t$ (s)", fontsize=10, fontweight='bold')
    ax_ft.set_ylabel("힘 $F(t)$ (N)", fontsize=10, fontweight='bold')
    ax_ft.set_title(r"① 힘-시간($F$-$t$) 그래프 아래 넓이 = 선형 충격량 $\int_{t_1}^{t} F(t)\,dt$",
                    fontsize=11.2, fontweight='bold', color='#1e293b', pad=6)
    ax_ft.grid(True, ls=':', alpha=0.5)

    ax_ft.plot(t_plot, F_plot, color='#e11d48', lw=2.8, label=r'시간에 따라 변하는 힘 $F(t)$')
    if t_curr > t1:
        t_end = min(t_curr, t2)
        mask = (t_plot >= t1) & (t_plot <= t_end)
        ax_ft.fill_between(t_plot[mask], 0, F_plot[mask], color='#fda4af', alpha=0.45,
                           label=rf'누적 넓이(충격량) = {J_curr:.1f} N·s')
        # 작은 직사각형 조각 F(t)*dt 시각화
        for ts in np.arange(1.0, t_end - 0.05, 0.25):
            w_s = min(0.25, t_end - ts)
            h_s = float(F_func(ts + 0.5 * w_s))
            ax_ft.add_patch(patches.Rectangle((ts, 0), w_s, h_s, facecolor='none', edgecolor='#be123c', lw=0.8, alpha=0.55))

    if t_curr >= t2:
        # 평균 힘 F_avg = 16 / (5-1) = 4.0 N 직사각형 비교 표시
        ax_ft.add_patch(patches.Rectangle((t1, 0), t2 - t1, 4.0, facecolor='none',
                                          edgecolor='#1d4ed8', lw=2.0, ls='--', zorder=5))
        ax_ft.text(3.0, 4.35, r"평균 힘 $F_{\mathrm{avg}} = 4\ \mathrm{N}$ 직사각형 넓이와 동일! ($4\times 4 = 16\ \mathrm{N\cdot s}$)",
                   fontsize=8.8, fontweight='bold', color='#1d4ed8', ha='center',
                   bbox=dict(boxstyle='round,pad=0.25', fc='#eff6ff', ec='#60a5fa'))

    ax_ft.axvline(t1, color='#1d4ed8', lw=1.6, ls='--')
    ax_ft.axvline(t2, color='#0ca678', lw=1.6, ls='--')
    ax_ft.text(t1 + 0.08, 6.2, r"아래끝 $t_1=1\ \mathrm{s}$" + "\n(힘 시작)", fontsize=8.6, color='#1d4ed8', fontweight='bold', ha='left')
    ax_ft.text(t2 - 0.08, 6.2, r"위끝 $t_2=5\ \mathrm{s}$" + "\n(힘 종료)", fontsize=8.6, color='#0ca678', fontweight='bold', ha='right')
    ax_ft.plot(min(max(t_curr, 0), 6), F_curr, 'o', color='#be123c', markersize=8, zorder=6)
    ax_ft.legend(loc='upper left', fontsize=8.4)

    # 2) 좌하단: 초기 운동량 G1 + 충격량 넓이 = 현재 운동량 G(t) 누적 막대
    ax_bar.set_xlim(0, 27)
    ax_bar.set_ylim(-0.55, 1.95)
    ax_bar.set_yticks([0.0, 0.85])
    ax_bar.set_yticklabels([r'현재 $G(t)$', r'$G_1$ + 넓이'], fontsize=9.8, fontweight='bold')
    ax_bar.set_xlabel(r"선형 운동량 및 충격량 ($\mathrm{N\cdot s = kg\cdot m/s}$)", fontsize=9.8, fontweight='bold')
    ax_bar.set_title(r"② 처음 운동량 $mv_1$에 그래프 넓이만큼 더해져 나중 운동량 $mv_2$가 됨!",
                     fontsize=10.6, fontweight='bold', color='#1e293b', pad=5)
    ax_bar.grid(axis='x', ls=':', alpha=0.5)

    ax_bar.barh(0.85, G1, height=0.40, color='#60a5fa', edgecolor='#1e293b', label=r'처음 $G_1 = 4\ \mathrm{N\cdot s}$')
    ax_bar.barh(0.85, J_curr, left=G1, height=0.40, color='#fb7185', edgecolor='#1e293b', label=rf'충격량 넓이 $= +{J_curr:.1f}\ \mathrm{{N\cdot s}}$')
    ax_bar.barh(0.0, G_curr, height=0.40, color='#10b981', edgecolor='#1e293b', label=rf'현재 $G(t) = {G_curr:.1f}\ \mathrm{{N\cdot s}}$')
    ax_bar.text(G_curr + 0.4, 0.0, rf"$G = {G_curr:.1f}\ \mathrm{{N\cdot s}}\ (v = {v_curr:.1f}\ \mathrm{{m/s}})$",
                va='center', fontsize=9.2, fontweight='bold', color='#047857')
    ax_bar.legend(loc='upper right', fontsize=7.8, ncol=3)

    # 3) 우측 패널: 실제 2 kg 블록 가속 모션 + 말풍선 수학 해설
    ax_sim.set_xlim(0.0, 10.0)
    ax_sim.set_ylim(0.0, 10.0)
    ax_sim.axis('off')
    ax_sim.set_title("③ 물체의 실제 가속 운동과 수학 기호 쉽게 읽기", fontsize=11.5, fontweight='bold', color='#1e293b', pad=6)

    # 수평 레일과 2 kg 블록 이동
    ax_sim.fill_between([0.4, 9.6], 4.55, 4.85, color='#dfd9d2')
    ax_sim.plot([0.4, 9.6], [4.85, 4.85], color='#1e293b', lw=2.4)

    prog_x = np.clip((t_curr - 0.5) / 5.1, 0.0, 1.0)
    bx = 1.4 + prog_x * 6.2
    by = 4.85
    ax_sim.add_patch(patches.Rectangle((bx - 0.75, by), 1.50, 1.05, facecolor='#bae6fd', edgecolor='#1e293b', lw=2.0, zorder=4))
    ax_sim.text(bx, by + 0.52, "m = 2 kg", fontsize=11.5, fontweight='bold', color='#0f172a', ha='center', va='center', zorder=5)

    # 힘 화살표 F(t) 및 속도 화살표 v(t)
    if F_curr > 0.05:
        flen = 0.4 + 0.22 * F_curr
        ax_sim.annotate('', xy=(bx - 0.78, by + 0.52), xytext=(bx - 0.78 - flen, by + 0.52),
                        arrowprops=dict(arrowstyle='->', color='#e11d48', lw=3.0, mutation_scale=17), zorder=6)
        ax_sim.text(bx - 0.78 - 0.5 * flen, by + 0.85, rf"$F(t)={F_curr:.1f}\ \mathrm{{N}}$",
                    fontsize=10.2, fontweight='bold', color='#be123c', ha='center')

    vlen = 0.45 + 0.14 * v_curr
    ax_sim.annotate('', xy=(bx + 0.78 + vlen, by + 0.52), xytext=(bx + 0.78, by + 0.52),
                    arrowprops=dict(arrowstyle='->', color='#0ca678', lw=2.8, mutation_scale=16), zorder=6)
    ax_sim.text(bx + 0.78 + 0.5 * vlen, by + 0.88, rf"$v={v_curr:.1f}\ \mathrm{{m/s}}$",
                fontsize=10.5, fontweight='bold', color='#047857', ha='center')

    # 상단 말풍선: 미분 기호와 정적분 기호 풀이
    bubble1 = (
        "[말풍선 보충 설명] 수식의 기호들을 말로 풀어서 읽어 볼까요?\n"
        "• 문자 위의 점(" + r"$\dot{v},\ \dot{\mathbf{G}}$" + "): '시간 t에 대한 미분(변화율)'을 뜻해요!\n"
        "  즉, " + r"$\Sigma\mathbf{F} = \dot{\mathbf{G}} = d\mathbf{G}/dt$" + " 는 '힘의 합 = 1초당 운동량이 변하는 빠르기'입니다.\n"
        "• 적분 기호 " + r"$\int_{t_1}^{t_2} F(t)\,dt$" + " : '시각 " + r"$t_1$" + "(아래끝)부터 시각 " + r"$t_2$" + "(위끝)까지\n"
        "  짧은 시간 조각 dt 마다 받은 힘×시간(F·dt 직사각형 넓이)을 모두 더하라'는 뜻이에요!"
    )
    ax_sim.text(0.35, 9.65, bubble1, fontsize=9.3, color='#78350f', va='top', ha='left', linespacing=1.42,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.7))

    # 하단 핵심 수식 정리 카드
    eq_summary = (
        "교재 핵심 공식 (3.8~3.9절):\n"
        + r"$\Sigma\mathbf{F} = \frac{d}{dt}(m\mathbf{v}) = \dot{\mathbf{G}} \quad\Longrightarrow\quad "
        + r"m\mathbf{v}_1 + \int_{t_1}^{t_2} \Sigma\mathbf{F}\,dt = m\mathbf{v}_2$" + "\n\n"
        + "이 예제의 계산 (그래프 넓이 = +16.0 N·s):\n"
        + r"$2(2) + \int_{1}^{5} F(t)\,dt = 2\,v_2 \;\Rightarrow\; 4 + 16 = 20 = 2\,v_2 \;\Rightarrow\; \mathbf{v_2 = 10\ m/s}$" + "\n"
        + "★ 복잡한 적분 공식 없이도, 그래프가 삼각형·사다리꼴이면 '도형 넓이'만 구하면 끝!"
    )
    ax_sim.text(0.35, 3.85, eq_summary, fontsize=9.5, color='#0f172a', va='top', ha='left', linespacing=1.48,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.5))

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(out_dir, "concept_ft_area_impulse.gif")
    print(f"Generating animation: {gif_path} ...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=90)
    anim.save(gif_path, writer='pillow', fps=12)
    plt.close(fig)
    print("Done! Saved concept_ft_area_impulse.gif")
