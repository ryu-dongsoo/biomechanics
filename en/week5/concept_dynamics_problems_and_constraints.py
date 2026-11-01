# -*- coding: utf-8 -*-
"""
[Dynamics 9th Ed. Chapter 3 Kinetics of Particles]
1. Two Basic Problems of Dynamics (Force -> Motion vs. Motion -> Force)
2. Unconstrained vs. Constrained Motion
Conceptual Infographic Diagram Visualization
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(17.0, 11.2), dpi=150)
ax = fig.add_subplot(111)
ax.set_position([0.01, 0.02, 0.98, 0.92])

ax.clear()
ax.set_xlim(-0.5, 33.5)
ax.set_ylim(-0.5, 21.5)
ax.axis('off')

# Background
ax.add_patch(patches.Rectangle((-0.5, -0.5), 34.0, 22.0, fc='#f8fafc', ec='none', zorder=1))

# =========================================================================
# [Top Header]: PART 1 - Two Basic Problems of Dynamics
# =========================================================================
top_header = patches.FancyBboxPatch((0.2, 19.8), 32.6, 1.2, boxstyle="round,pad=0.2",
                                    fc="#0284c7", ec="none", zorder=3)
ax.add_patch(top_header)
ax.text(16.5, 20.4, "PART 1. Two Basic Problems of Dynamics",
        fontsize=13.0, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)

# -------------------------------------------------------------------------
# [Card 1] Top-Left: Type 1 - Direct Problem (Force -> Motion)
# -------------------------------------------------------------------------
card1 = patches.FancyBboxPatch((0.2, 10.8), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#38bdf8", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card1)

ax.text(8.2, 18.8, "Type 1: Direct Problem (Force → Motion)",
        fontsize=11.5, fontweight='bold', color="#0369a1", ha='center', zorder=5)
ax.plot([0.6, 15.8], [18.4, 18.4], color='#e0f2fe', lw=1.4, zorder=4)

c1_text = (
    "- Problem Statement:\n"
    "  • Given the specified forces ΣF(t, r, v) acting on the particle,\n"
    "    determine the resulting acceleration, velocity, and position by integration\n"
    "- Mathematical Flow:\n"
    "  • Forces ΣF  ⇒  Acceleration a(t) = ΣF/m  ⇒  Velocity v(t) = ∫ a dt  ⇒  Path r(t) = ∫ v dt\n"
    "- Typical Examples:\n"
    "  • Trajectory analysis of a projectile subject to aerodynamic drag (e.g. Sample 3/4)"
)
ax.text(0.6, 18.1, c1_text, fontsize=8.2, va='top', linespacing=1.35, zorder=5)

p_x0, p_y0 = 2.0, 11.6
t_pts = np.linspace(0, 2.8, 50)
traj_x = p_x0 + 4.2 * t_pts
traj_y = p_y0 + 4.2 * t_pts - 0.5 * 2.8 * (t_pts**2)

ax.plot([1.2, 15.2], [p_y0, p_y0], color='#64748b', lw=1.5, zorder=3)
ax.plot(traj_x, traj_y, color='#0284c7', lw=1.8, linestyle='--', zorder=4)

curr_idx = 25
cx, cy = traj_x[curr_idx], traj_y[curr_idx]
ax.scatter([cx], [cy], color='#0284c7', s=45, zorder=6)
ax.text(cx + 0.3, cy + 0.3, r'$m$', fontsize=10.0, fontweight='bold', color='#0284c7', zorder=7)

ax.annotate('', xy=(cx, cy - 1.6), xytext=(cx, cy),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx + 0.2, cy - 1.2, r'$mg$', fontsize=9.0, fontweight='bold', color='#b91c1c', zorder=8)

tang_v = np.array([4.2, 4.2 - 2.8 * t_pts[curr_idx]])
tang_u = tang_v / np.linalg.norm(tang_v)
ax.annotate('', xy=(cx - 1.4*tang_u[0], cy - 1.4*tang_u[1]), xytext=(cx, cy),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx - 1.6*tang_u[0] - 0.3, cy - 1.6*tang_u[1], r'$D(v)$', fontsize=8.5, fontweight='bold', color='#c2410c', zorder=8)

ax.annotate('', xy=(cx + 1.6*tang_u[0], cy + 1.6*tang_u[1]), xytext=(cx, cy),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(cx + 1.8*tang_u[0] + 0.1, cy + 1.8*tang_u[1], r'$\mathbf{v}(t), \mathbf{r}(t)$',
        fontsize=9.0, fontweight='bold', color='#2563eb', zorder=8)

ax.text(1.2, 14.6, "[Given Inputs]\n Forces: mg, D(v)", fontsize=7.6, color='#b91c1c',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fee2e2', edgecolor='#fca5a5', lw=1.0), zorder=6)
ax.text(11.2, 14.6, "[To Find (Outputs)]\n Trajectory r(t), Velocity v(t)", fontsize=7.6, color='#1e40af',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#dbeafe', edgecolor='#93c5fd', lw=1.0), zorder=6)

# -------------------------------------------------------------------------
# [Card 2] Top-Right: Type 2 - Inverse Problem (Motion -> Force)
# -------------------------------------------------------------------------
card2 = patches.FancyBboxPatch((16.8, 10.8), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#818cf8", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card2)

ax.text(24.8, 18.8, "Type 2: Inverse Problem (Motion → Force)",
        fontsize=11.5, fontweight='bold', color="#4338ca", ha='center', zorder=5)
ax.plot([17.2, 32.4], [18.4, 18.4], color='#e0e7ff', lw=1.4, zorder=4)

c2_text = (
    "- Problem Statement:\n"
    "  • Given the prescribed motion trajectory r(t) or acceleration a(t),\n"
    "    determine the required driving forces, thrust, cable tensions, or reactions\n"
    "- Mathematical Flow:\n"
    "  • Prescribed motion r(t), a(t)  ⇒  Newton's 2nd Law  ⇒  Required force ΣF = m a(t)\n"
    "- Typical Examples:\n"
    "  • Force calculation required to bring a collar to rest at specified time (e.g. Sample 3/5)"
)
ax.text(17.2, 18.1, c2_text, fontsize=8.2, va='top', linespacing=1.35, zorder=5)

loop_cx, loop_cy, loop_r = 24.8, 13.8, 2.0
theta_loop = np.linspace(-np.pi/2, np.pi/2, 50)
loop_x = loop_cx + loop_r * np.cos(theta_loop)
loop_y = loop_cy + loop_r * np.sin(theta_loop)
ax.plot(loop_x, loop_y, color='#4338ca', lw=2.4, zorder=4)

th_car = np.radians(30)
car_x = loop_cx + loop_r * np.cos(th_car)
car_y = loop_cy + loop_r * np.sin(th_car)

ax.scatter([car_x], [car_y], color='#4338ca', s=45, zorder=6)
ax.annotate('', xy=(car_x - 1.3*np.cos(th_car), car_y - 1.3*np.sin(th_car)), xytext=(car_x, car_y),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(car_x - 1.5*np.cos(th_car) - 0.2, car_y - 1.5*np.sin(th_car), r'$\mathbf{a}_n = \frac{v^2}{\rho}$',
        fontsize=8.5, fontweight='bold', color='#1d4ed8', zorder=8)

ax.annotate('', xy=(car_x + 1.5*np.cos(th_car), car_y + 1.5*np.sin(th_car)), xytext=(car_x, car_y),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=7)
ax.text(car_x + 1.6*np.cos(th_car) + 0.1, car_y + 1.6*np.sin(th_car), r'$N_{\text{req}}$',
        fontsize=9.5, fontweight='bold', color='#b91c1c', zorder=8)

ax.text(17.6, 14.6, "[Given Inputs]\n Velocity v(t), Radius ρ", fontsize=7.6, color='#1e40af',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#dbeafe', edgecolor='#93c5fd', lw=1.0), zorder=6)
ax.text(28.0, 14.6, "[To Find (Outputs)]\n Required Normal N, Thrust F", fontsize=7.6, color='#b91c1c',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fee2e2', edgecolor='#fca5a5', lw=1.0), zorder=6)

# =========================================================================
# [Bottom Header]: PART 2 - Unconstrained vs. Constrained Motion
# =========================================================================
bot_header = patches.FancyBboxPatch((0.2, 9.4), 32.6, 1.2, boxstyle="round,pad=0.2",
                                    fc="#059669", ec="none", zorder=3)
ax.add_patch(bot_header)
ax.text(16.5, 10.0, "PART 2. Unconstrained vs. Constrained Motion",
        fontsize=13.0, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)

# -------------------------------------------------------------------------
# [Card 3] Bottom-Left: Unconstrained Motion
# -------------------------------------------------------------------------
card3 = patches.FancyBboxPatch((0.2, 0.4), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#34d399", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card3)

ax.text(8.2, 8.4, "Unconstrained Motion (Free Flight)",
        fontsize=11.5, fontweight='bold', color="#047857", ha='center', zorder=5)
ax.plot([0.6, 15.8], [8.0, 8.0], color='#d1fae5', lw=1.4, zorder=4)

c3_text = (
    "- Concepts & Characteristics:\n"
    "  • No physical guide, rail, or contact surface limits the particle motion\n"
    "  • All Degrees of Freedom (DOF) are preserved (3-DOF in 3D space)\n"
    "  • Motion is determined solely by applied external forces (Gravity, Thrust, Drag)\n"
    "- Typical Examples:\n"
    "  • Rockets/Airplanes in flight, Satellite orbital motion, Free-falling bodies"
)
ax.text(0.6, 7.7, c3_text, fontsize=8.2, va='top', linespacing=1.35, zorder=5)

r_x, r_y = 7.8, 3.2
ang_r = np.radians(40)
u_r = np.array([np.cos(ang_r), np.sin(ang_r)])
n_r = np.array([-np.sin(ang_r), np.cos(ang_r)])

traj_u_x = np.linspace(2.0, 14.5, 40)
traj_u_y = 1.2 + 0.7 * (traj_u_x - 2.0) - 0.035 * ((traj_u_x - 2.0)**2)
ax.plot(traj_u_x, traj_u_y, color='#059669', lw=1.8, linestyle=':', zorder=4)

r_w, r_h = 2.2, 0.7
r_bl = np.array([r_x, r_y]) - (r_w/2)*u_r - (r_h/2)*n_r
ax.add_patch(patches.Rectangle(r_bl, r_w, r_h, angle=40, fc='#e0f2fe', ec='#0284c7', lw=1.4, zorder=6))

nose_tip = np.array([r_x, r_y]) + (r_w/2 + 0.6)*u_r
nose_l = np.array([r_x, r_y]) + (r_w/2)*u_r + (r_h/2)*n_r
nose_r = np.array([r_x, r_y]) + (r_w/2)*u_r - (r_h/2)*n_r
ax.add_patch(patches.Polygon([nose_tip, nose_l, nose_r], closed=True, fc='#ef4444', ec='#b91c1c', lw=1.2, zorder=7))

ax.annotate('', xy=nose_tip + 1.2*u_r, xytext=nose_tip,
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(nose_tip[0] + 1.3*u_r[0], nose_tip[1] + 1.3*u_r[1] + 0.1, r'$\mathbf{T}\text{ (Thrust)}$',
        fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=9)

ax.annotate('', xy=(r_x, r_y - 1.5), xytext=(r_x, r_y),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(r_x + 0.2, r_y - 1.2, r'$m\mathbf{g}$', fontsize=9.0, fontweight='bold', color='#c2410c', zorder=9)

ax.annotate('', xy=np.array([r_x, r_y]) - (r_w/2 + 1.0)*u_r, xytext=np.array([r_x, r_y]) - (r_w/2)*u_r,
            arrowprops=dict(facecolor='#64748b', edgecolor='#334155', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(r_x - (r_w/2 + 1.4)*u_r[0], r_y - (r_w/2 + 1.4)*u_r[1], r'$\mathbf{D}\text{ (Drag)}$',
        fontsize=8.5, fontweight='bold', color='#334155', zorder=9)

ax.text(1.2, 2.0, "* Key Feature: Constraint Reaction (N, R) = 0\n  Degrees of Freedom = 3 (Free Space Flight)", fontsize=7.6, color='#047857',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#ecfdf5', edgecolor='#a7f3d0', lw=1.0), zorder=8)

# -------------------------------------------------------------------------
# [Card 4] Bottom-Right: Constrained Motion
# -------------------------------------------------------------------------
card4 = patches.FancyBboxPatch((16.8, 0.4), 16.0, 8.6, boxstyle="round,pad=0.25",
                               fc="#ffffff", ec="#f59e0b", lw=1.6, alpha=0.98, zorder=2)
ax.add_patch(card4)

ax.text(24.8, 8.4, "Constrained Motion (Guided Track)",
        fontsize=11.5, fontweight='bold', color="#b45309", ha='center', zorder=5)
ax.plot([17.2, 32.4], [8.0, 8.0], color='#fef3c7', lw=1.4, zorder=4)

c4_text = (
    "- Concepts & Characteristics:\n"
    "  • Particle motion is physically restricted to a track, guide rod, surface, or cable\n"
    "  • The geometric constraint dictates the permissible trajectory in advance\n"
    "  • Constraint reaction forces (Normal N, Tension T, Reaction R) arise at contacts\n"
    "- Typical Examples:\n"
    "  • Incline/Cable cart (Sample 3/2, 3/3), Collar on vertical rod (Sample 3/5)"
)
ax.text(17.2, 7.7, c4_text, fontsize=8.2, va='top', linespacing=1.35, zorder=5)

c_base_x, c_base_y = 24.8, 3.2
x_rail = np.linspace(17.6, 32.0, 60)
y_rail = c_base_y + 1.2 * np.sin((x_rail - 18.0) * 0.45)
ax.plot(x_rail, y_rail, color='#475569', lw=4.0, zorder=4)
ax.plot(x_rail, y_rail, color='#cbd5e1', lw=1.8, linestyle='--', zorder=5)

target_x = 24.0
target_y = c_base_y + 1.2 * np.sin((target_x - 18.0) * 0.45)
slope = 1.2 * 0.45 * np.cos((target_x - 18.0) * 0.45)
ang_c = np.arctan(slope)
u_c = np.array([np.cos(ang_c), np.sin(ang_c)])
n_c = np.array([-np.sin(ang_c), np.cos(ang_c)])

cw, ch = 2.0, 1.2
c_bl = np.array([target_x, target_y]) - (cw/2)*u_c - (ch/2)*n_c
ax.add_patch(patches.Rectangle(c_bl, cw, ch, angle=np.degrees(ang_c),
                               fc='#fed7aa', ec='#c2410c', lw=1.5, zorder=6))
ax.scatter([target_x], [target_y], color='#c2410c', s=35, zorder=7)

ax.annotate('', xy=np.array([target_x, target_y]) + 1.8*n_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#16a34a', edgecolor='#15803d', width=2.2, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(target_x + 1.9*n_c[0], target_y + 1.9*n_c[1] + 0.1, r'$\mathbf{N}\text{ (Constraint Normal)}$',
        fontsize=8.5, fontweight='bold', color='#15803d', zorder=9)

ax.annotate('', xy=np.array([target_x, target_y]) - 1.3*u_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(target_x - 1.5*u_c[0] - 0.2, target_y - 1.5*u_c[1] - 0.3, r'$f_k = \mu_k N$',
        fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=9)

ax.annotate('', xy=np.array([target_x, target_y]) + 1.6*u_c, xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=2.0, headwidth=5.5, headlength=6.5), zorder=8)
ax.text(target_x + 1.7*u_c[0] + 0.1, target_y + 1.7*u_c[1], r'$\mathbf{F}\text{ (Driving Force)}$',
        fontsize=8.5, fontweight='bold', color='#1d4ed8', zorder=9)

ax.annotate('', xy=(target_x, target_y - 1.5), xytext=(target_x, target_y),
            arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=1.8, headwidth=5.0, headlength=6.0), zorder=8)
ax.text(target_x + 0.2, target_y - 1.3, r'$m\mathbf{g}$', fontsize=9.0, fontweight='bold', color='#c2410c', zorder=9)

ax.text(17.6, 2.0, "* Key Feature: Guide track dictates path\n  Normal constraint N & friction arise (1-DOF)", fontsize=7.6, color='#b45309',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#fffbeb', edgecolor='#fde68a', lw=1.0), zorder=8)

fig.suptitle('[Dynamics 9th Ed. Chapter 3] Two Basic Problems of Dynamics & Constrained/Unconstrained Motion',
             fontsize=14.0, fontweight='bold', y=0.985)

out_png = os.path.join(os.path.dirname(__file__), 'concept_dynamics_problems_and_constraints.png')
plt.savefig(out_png, dpi=150)
plt.close()
print(f'Rendered {out_png}')
