# -*- coding: utf-8 -*-
"""
[Dynamics 9th Ed. Problem 3/30] Range of Force P for No Slip on a 20° Wedge Cart
- Wedge Cart m1 (20° incline, negligible wheel friction)
- Block m2 (μs = 0.30, μk = 0.25)
- Textbook visual styling + 3-panel split FBD (Case 1: P_min, Case 2: P_max)
"""
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from PIL import Image

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------------------------------------
# 1. Physical Parameters & Rigorous Analytical Solution
# -------------------------------------------------------------
th_deg = 20.0
th_rad = np.radians(th_deg)
mu_s = 0.30
mu_k = 0.25
g = 9.81

sin_th = np.sin(th_rad)  # 0.34202
cos_th = np.cos(th_rad)  # 0.93969

# (1) Minimum Acceleration for Impending Downward Slip (a_min, fs = +mu_s N up-incline)
a_min = g * (sin_th - mu_s * cos_th) / (cos_th + mu_s * sin_th)   # 0.5657 m/s^2

# (2) Maximum Acceleration for Impending Upward Slip (a_max, fs = -mu_s N down-incline)
a_max = g * (sin_th + mu_s * cos_th) / (cos_th - mu_s * sin_th)   # 7.3118 m/s^2

# Nominal driving acceleration (safe intermediate value a_nom = 3.5 m/s^2)
a_nom = 3.5

# -------------------------------------------------------------
# 2. Single Frame Rendering Function
# -------------------------------------------------------------
def render_frame(t, total_time=3.0):
    # Horizontal travel displacement
    x_disp = 0.5 * a_nom * (t**2) * 0.12  # Visual scaling factor
    v_curr = a_nom * t
    
    fig = plt.figure(figsize=(15.6, 8.4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_position([0.01, 0.02, 0.98, 0.92])
    
    ax.clear()
    ax.set_xlim(-0.8, 27.2)
    ax.set_ylim(-0.6, 14.8)
    ax.axis('off')
    
    # Background
    ax.add_patch(patches.Rectangle((-0.8, -0.6), 28.0, 15.4, fc='#f8fafc', ec='none', zorder=1))
    
    # =============================================================
    # [Panel 1] Left: Theoretical Kinetics & Telemetry Card
    # =============================================================
    card1 = patches.FancyBboxPatch((-0.4, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#0284c7', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card1)
    
    ax.text(3.7, 13.4, '[Problem 3/30 Kinetics Analysis]', fontsize=11.0, fontweight='bold', color='#0369a1', ha='center', zorder=5)
    ax.plot([-0.1, 7.5], [13.0, 13.0], color='#bae6fd', lw=1.2, zorder=5)
    
    hud_theory = (
        "■ Given Parameters:\n"
        f"  • Wedge cart mass: m1 (20° incline, frictionless wheels)\n"
        f"  • Top block mass: m2 (resting on incline)\n"
        f"  • Friction coeff: μs = {mu_s:.2f}, μk = {mu_k:.2f}\n"
        f"  • Total system horiz. accel: a = P / (m1 + m2)\n\n"
        "■ Step 1: Lower Bound Force (P_min, Impending Downward Slip)\n"
        "  • Static friction fs = μs N acts UP along incline\n"
        "  • ΣFx = N sin 20° - μs N cos 20° = m2 a_min\n"
        "  • ΣFy = N cos 20° + μs N sin 20° - m2 g = 0\n"
        f"  ▶ a_min = g(sin 20° - μs cos 20°)/(cos 20° + μs sin 20°)\n"
        f"          = {a_min:.3f} m/s² [0.0577 g]\n"
        f"  ▶ P_min = {a_min:.3f} (m1 + m2) N\n\n"
        "■ Step 2: Upper Bound Force (P_max, Impending Upward Slip)\n"
        "  • Static friction fs = μs N acts DOWN along incline\n"
        "  • ΣFx = N sin 20° + μs N cos 20° = m2 a_max\n"
        "  • ΣFy = N cos 20° - μs N sin 20° - m2 g = 0\n"
        f"  ▶ a_max = g(sin 20° + μs cos 20°)/(cos 20° - μs sin 20°)\n"
        f"          = {a_max:.3f} m/s² [0.745 g]\n"
        f"  ▶ P_max = {a_max:.3f} (m1 + m2) N\n\n"
        "■ Allowable Force Range for No Slipping:\n"
        f"  ▶ {a_min:.3f}(m1+m2) ≤ P ≤ {a_max:.3f}(m1+m2) N"
    )
    ax.text(0.0, 12.6, hud_theory, fontsize=7.6, va='top', linespacing=1.26, zorder=5)
    
    ax.plot([-0.1, 7.5], [2.6, 2.6], color='#bae6fd', lw=1.2, zorder=5)
    ax.text(3.7, 2.3, '[Live Telemetry]', fontsize=9.2, fontweight='bold', color='#0284c7', ha='center', zorder=5)
    
    status_str = (
        f"• Elapsed Time:    t = {t:4.2f} s / {total_time:.2f} s\n"
        f"• Acceleration:    a = {a_nom:4.2f} m/s² (Safe driving regime)\n"
        f"• Displacement:    x = {x_disp:4.2f} m (v = {v_curr:4.2f} m/s)\n"
        f"• Slip Status:     Safe (a_min ≤ {a_nom:.1f} ≤ a_max)"
    )
    ax.text(0.0, 1.9, status_str, fontsize=8.0, va='top', family='monospace', linespacing=1.32, zorder=5)
    
    # =============================================================
    # [Panel 2] Center: Physical System (Exact Textbook Illustration)
    # =============================================================
    card2 = patches.FancyBboxPatch((8.2, 0.2), 10.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#64748b', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card2)
    
    ax.text(13.3, 13.4, '[Physical System (Wedge & Block)]', fontsize=11.0, fontweight='bold', color='#1e293b', ha='center', zorder=5)
    ax.plot([8.5, 18.1], [13.0, 13.0], color='#e2e8f0', lw=1.2, zorder=5)
    
    # Ground & Hatching
    ground_y = 3.6
    ax.plot([8.5, 18.1], [ground_y, ground_y], color='#334155', lw=2.2, zorder=3)
    for hx in np.linspace(8.6, 18.0, 24):
        ax.plot([hx, hx - 0.25], [ground_y, ground_y - 0.35], color='#94a3b8', lw=1.1, zorder=2)
    
    # Wedge Cart Geometry
    w_len = 6.4
    w_h = w_len * np.tan(th_rad)
    
    wheel_r = 0.26
    wheel_y = ground_y + wheel_r
    wedge_base_y = ground_y + 2 * wheel_r
    
    init_wx = 9.4
    wx = init_wx + x_disp
    
    # 1) Wedge cart polygon (m1, light blue)
    poly_wedge = [
        [wx, wedge_base_y],
        [wx + w_len, wedge_base_y],
        [wx, wedge_base_y + w_h]
    ]
    ax.add_patch(patches.Polygon(poly_wedge, closed=True, fc='#c7e9fb', ec='#0284c7', lw=1.8, zorder=4))
    
    # Wedge label "m1"
    ax.text(wx + 1.2, wedge_base_y + 0.48*w_h, r'$m_1$', fontsize=11.5, fontweight='bold', color='#0369a1', ha='center', va='center', zorder=7)
    
    # 2) Wedge wheels (left & right)
    wh1_x = wx + 1.4
    wh2_x = wx + w_len - 1.5
    ax.add_patch(patches.Circle((wh1_x, wheel_y), wheel_r, fc='#e2e8f0', ec='#334155', lw=1.3, zorder=5))
    ax.add_patch(patches.Circle((wh1_x, wheel_y), 0.07, fc='#0f172a', ec='none', zorder=6))
    ax.add_patch(patches.Circle((wh2_x, wheel_y), wheel_r, fc='#e2e8f0', ec='#334155', lw=1.3, zorder=5))
    ax.add_patch(patches.Circle((wh2_x, wheel_y), 0.07, fc='#0f172a', ec='none', zorder=6))
    
    # 3) 20° incline angle arc & label
    arc_cx = wx + w_len
    arc_cy = wedge_base_y
    ax.plot([arc_cx - 2.2, arc_cx], [arc_cy, arc_cy], color='#334155', lw=1.0, linestyle=':', zorder=6)
    ax.add_patch(patches.Arc((arc_cx, arc_cy), 3.2, 3.2, angle=180, theta1=0, theta2=20, color='#0f172a', lw=1.3, zorder=7))
    ax.text(arc_cx - 1.8, arc_cy + 0.35, r'$20^\circ$', fontsize=9.5, fontweight='bold', color='#0f172a', zorder=8)
    
    # 4) Block m2 (rectangle, peach color)
    u_down = np.array([cos_th, -sin_th])
    n_out = np.array([sin_th, cos_th])
    
    dist_along_wedge = 2.8
    b_center_on_incline = np.array([wx, wedge_base_y + w_h]) + dist_along_wedge * u_down
    
    box2_w = 2.4
    box2_h = 1.35
    b_center = b_center_on_incline + (box2_h/2) * n_out
    
    bl2 = b_center - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(bl2, box2_w, box2_h, angle=-th_deg,
                                   fc='#ea997b', ec='#802611', lw=1.8, zorder=6))
    
    ax.text(b_center[0], b_center[1], r'$m_2$', fontsize=11.5, fontweight='bold', color='#802611', ha='center', va='center', zorder=8)
    
    # 5) Applied Force P
    p_len = 1.8
    p_start_x = wx - p_len - 0.2
    p_y = wedge_base_y + 0.50 * w_h
    ax.annotate('', xy=(wx, p_y), xytext=(p_start_x, p_y),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.4, headwidth=6.5, headlength=7.5), zorder=8)
    ax.text(p_start_x - 0.2, p_y, r'$P$', fontsize=11.5, fontweight='bold', color='#ef4444', ha='right', va='center', zorder=9)
    
    # 6) Friction coefficient annotations
    contact_pt = b_center_on_incline + (box2_w/2)*u_down
    label_pt = contact_pt + np.array([0.9, 0.4])
    ax.annotate('', xy=contact_pt, xytext=label_pt,
                arrowprops=dict(arrowstyle='->', color='#334155', lw=1.2, connectionstyle="arc3,rad=-0.15"), zorder=9)
    
    ax.text(label_pt[0] + 0.1, label_pt[1] + 0.22, r'$\mu_s = 0.30$', fontsize=9.2, fontweight='bold', color='#0f172a', va='center', zorder=10)
    ax.text(label_pt[0] + 0.1, label_pt[1] - 0.22, r'$\mu_k = 0.25$', fontsize=9.2, fontweight='bold', color='#0f172a', va='center', zorder=10)
    
    # =============================================================
    # [Panel 3] Right: Free-Body Diagrams (FBD: 2 Limiting Cases)
    # =============================================================
    card3 = patches.FancyBboxPatch((18.6, 0.2), 8.2, 13.8,
                                   boxstyle="round,pad=0.25", fc="#ffffff", ec='#b91c1c', lw=1.4, alpha=0.98, zorder=2)
    ax.add_patch(card3)
    
    ax.text(22.7, 13.4, '[Free-Body Diagram (2 Limiting Cases)]', fontsize=11.0, fontweight='bold', color='#b91c1c', ha='center', zorder=5)
    ax.plot([18.9, 26.5], [13.0, 13.0], color='#fee2e2', lw=1.2, zorder=5)
    
    # -------------------------------------------------------------
    # (1) Upper FBD: Case 1: P_min Limiting Condition (Impending Downward Slip)
    # -------------------------------------------------------------
    fbd1_cx = 22.4
    fbd1_cy = 9.8
    
    ax.text(19.2, 12.5, '▶ Case 1: P_min (Downward Slip Threshold, fs = μs N Up-Incline)',
            fontsize=7.4, fontweight='bold', color='#991b1b', zorder=6)
    
    fbd1_bl = np.array([fbd1_cx, fbd1_cy]) - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(fbd1_bl, box2_w, box2_h, angle=-th_deg,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbd1_cx - 0.35*u_down[0] + 0.35*n_out[0], fbd1_cy - 0.35*u_down[1] + 0.35*n_out[1],
            r'$m_2$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbd1_cx], [fbd1_cy], color='#ef4444', s=24, zorder=9)
    
    # N
    ax.annotate('', xy=(fbd1_cx + 2.2*n_out[0], fbd1_cy + 2.2*n_out[1]), xytext=(fbd1_cx, fbd1_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd1_cx + 2.3*n_out[0] + 0.1, fbd1_cy + 2.3*n_out[1] + 0.1, r'$N$',
            fontsize=9.0, fontweight='bold', color='#15803d', zorder=11)
    
    # fs (up-incline)
    fs1_start = np.array([fbd1_cx, fbd1_cy]) - (box2_h/2)*n_out
    ax.annotate('', xy=fs1_start - 1.8*u_down, xytext=fs1_start,
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fs1_start[0] - 1.9*u_down[0] - 0.1, fs1_start[1] - 1.9*u_down[1] + 0.25, r'$f_s = \mu_s N$',
            fontsize=8.5, fontweight='bold', color='#7e22ce', ha='right', zorder=11)
    
    # m2 g
    ax.annotate('', xy=(fbd1_cx, fbd1_cy - 2.2), xytext=(fbd1_cx, fbd1_cy),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd1_cx + 0.2, fbd1_cy - 1.8, r'$m_2 g$',
            fontsize=9.0, fontweight='bold', color='#c2410c', zorder=11)
    
    # a_min
    ax.annotate('', xy=(fbd1_cx + 2.2, fbd1_cy - 1.2), xytext=(fbd1_cx + 0.2, fbd1_cy - 1.2),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.6, headwidth=4.5, headlength=5.5), zorder=10)
    ax.text(fbd1_cx + 2.3, fbd1_cy - 1.2, r'$a_{\min} = 0.566\text{ m/s}^2$',
            fontsize=8.0, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    # Divider
    ax.plot([18.9, 26.5], [6.6, 6.6], color='#fee2e2', lw=1.0, linestyle='--', zorder=5)
    
    # -------------------------------------------------------------
    # (2) Lower FBD: Case 2: P_max Limiting Condition (Impending Upward Slip)
    # -------------------------------------------------------------
    fbd2_cx = 22.4
    fbd2_cy = 3.8
    
    ax.text(19.2, 6.2, '▶ Case 2: P_max (Upward Slip Threshold, fs = μs N Down-Incline)',
            fontsize=7.4, fontweight='bold', color='#991b1b', zorder=6)
    
    fbd2_bl = np.array([fbd2_cx, fbd2_cy]) - (box2_w/2)*u_down - (box2_h/2)*n_out
    ax.add_patch(patches.Rectangle(fbd2_bl, box2_w, box2_h, angle=-th_deg,
                                   fc='#fef2f2', ec='#991b1b', lw=1.5, zorder=6))
    ax.text(fbd2_cx - 0.35*u_down[0] + 0.35*n_out[0], fbd2_cy - 0.35*u_down[1] + 0.35*n_out[1],
            r'$m_2$', fontsize=10.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=8)
    ax.scatter([fbd2_cx], [fbd2_cy], color='#ef4444', s=24, zorder=9)
    
    # N
    ax.annotate('', xy=(fbd2_cx + 2.2*n_out[0], fbd2_cy + 2.2*n_out[1]), xytext=(fbd2_cx, fbd2_cy),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd2_cx + 2.3*n_out[0] + 0.1, fbd2_cy + 2.3*n_out[1] + 0.1, r'$N$',
            fontsize=9.0, fontweight='bold', color='#15803d', zorder=11)
    
    # fs (down-incline)
    fs2_start = np.array([fbd2_cx, fbd2_cy]) - (box2_h/2)*n_out
    ax.annotate('', xy=fs2_start + 1.8*u_down, xytext=fs2_start,
                arrowprops=dict(facecolor='#a855f7', edgecolor='#7e22ce', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fs2_start[0] + 1.9*u_down[0] + 0.1, fs2_start[1] + 1.9*u_down[1] - 0.25, r'$f_s = \mu_s N$',
            fontsize=8.5, fontweight='bold', color='#7e22ce', ha='left', zorder=11)
    
    # m2 g
    ax.annotate('', xy=(fbd2_cx, fbd2_cy - 2.2), xytext=(fbd2_cx, fbd2_cy),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=10)
    ax.text(fbd2_cx - 0.2, fbd2_cy - 1.8, r'$m_2 g$',
            fontsize=9.0, fontweight='bold', color='#c2410c', ha='right', zorder=11)
    
    # a_max
    ax.annotate('', xy=(fbd2_cx + 2.2, fbd2_cy - 1.2), xytext=(fbd2_cx + 0.2, fbd2_cy - 1.2),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.6, headwidth=4.5, headlength=5.5), zorder=10)
    ax.text(fbd2_cx + 2.3, fbd2_cy - 1.2, r'$a_{\max} = 7.311\text{ m/s}^2$',
            fontsize=8.0, fontweight='bold', color='#2563eb', va='center', zorder=11)
    
    # Title
    fig.suptitle('[Dynamics 9th Ed. Problem 3/30] Range of Force P for No Slip on a 20° Wedge Cart',
                 fontsize=12.0, fontweight='bold', y=0.98)
    
    # Convert to Pillow Image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    return img

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, 'prob3_30_wedge_blocks.gif')
    
    fps = 30
    duration = 3.0
    total_frames = int(fps * duration)
    
    print(f"Rendering {total_frames} frames (30 FPS, {duration:.1f}s) for Problem 3/30 (EN)...")
    frames = []
    
    times = np.linspace(0.0, duration, total_frames)
    for idx, t in enumerate(times):
        img = render_frame(t, duration)
        frames.append(img)
        if (idx + 1) % 15 == 0 or idx == total_frames - 1:
            print(f"  Frame {idx + 1}/{total_frames} (t = {t:.2f}s) rendered.")
            
    print(f"Saving GIF to: {gif_path}")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True
    )
    print("EN GIF generation complete successfully!")

if __name__ == '__main__':
    main()
