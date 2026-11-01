"""
Dynamics 9th Ed. Chapter 4: Kinetics of Systems of Particles
Sample Problem 4/2 - Three Spheres Welded to an Equilateral Rigid Frame
- Pure white background (#ffffff) & faithful textbook geometry
- Theoretical verification completed:
  * (a) Acceleration of point O (mass center G): a_bar = a_O = (F / 3m) i
  * (b) Angular acceleration of rigid frame: theta_ddot = F b / (3 m r^2) (CW)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

# Normalized parameters (m = 1 kg, r = 1 m, b = 0.6 m, F = 3 N)
m = 1.0
r = 1.0
b = 0.6
F = 3.0

a_O_x = F / (3.0 * m)                 # 1.00 m/s^2
alpha_cw = (F * b) / (3.0 * m * r**2) # 0.60 rad/s^2

n_frames = 48
t_vals = np.linspace(0.0, 0.85, n_frames)

fig, (ax_main, ax_calc) = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={'width_ratios': [1.2, 1.0]})
fig.patch.set_facecolor('#ffffff')
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.05, right=0.96, wspace=0.15)

base_angles = np.radians([90.0, 210.0, 330.0])

def update(frame):
    t = t_vals[frame]
    x_O = 0.5 * a_O_x * t**2
    y_O = 0.0
    theta_cw = 0.5 * alpha_cw * t**2
    omega_cw = alpha_cw * t
    v_O = a_O_x * t
    
    # ---------------- 1. Main Physical View ----------------
    ax_main.cla()
    ax_main.set_facecolor('#ffffff')
    ax_main.set_xlim(-1.45, 1.85)
    ax_main.set_ylim(-1.15, 1.45)
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    
    ax_main.plot([-1.2, 1.6], [0, 0], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.plot([0, 0], [-0.95, 1.3], color='#888888', ls='--', lw=1.2, zorder=1)
    ax_main.text(1.65, 0.0, r'$x$', fontsize=12, fontweight='bold', va='center')
    ax_main.text(0.0, 1.34, r'$y$', fontsize=12, fontweight='bold', ha='center')
    
    if frame > 0:
        for ang0 in base_angles:
            px0, py0 = r * np.cos(ang0), r * np.sin(ang0)
            ax_main.plot([0, px0], [0, py0], color='#dcdcdc', lw=3.0, zorder=1)
            c0 = patches.Circle((px0, py0), 0.12, facecolor='none', edgecolor='#cccccc', ls='--', lw=1.2, zorder=1)
            ax_main.add_patch(c0)
            
    pO = np.array([x_O, y_O])
    
    ang1_deg = 90.0 - np.degrees(theta_cw)
    ang3_deg = -30.0 - np.degrees(theta_cw)
    ang2_deg = -150.0 - np.degrees(theta_cw)
    arc1 = patches.Arc(pO, 0.52, 0.52, angle=0, theta1=ang3_deg, theta2=ang1_deg, color='#444444', lw=1.3, zorder=3)
    arc2 = patches.Arc(pO, 0.48, 0.48, angle=0, theta1=ang2_deg, theta2=ang3_deg, color='#444444', lw=1.3, zorder=3)
    ax_main.add_patch(arc1)
    ax_main.add_patch(arc2)
    mid1 = np.radians(0.5*(ang1_deg + ang3_deg))
    mid2 = np.radians(0.5*(ang2_deg + ang3_deg))
    ax_main.text(pO[0] + 0.36*np.cos(mid1), pO[1] + 0.36*np.sin(mid1), r'$120^\circ$', fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax_main.text(pO[0] + 0.34*np.cos(mid2), pO[1] + 0.34*np.sin(mid2), r'$120^\circ$', fontsize=9.5, fontweight='bold', ha='center', va='center')
    
    weld_pts = []
    sphere_pts = []
    for idx, ang0 in enumerate(base_angles):
        ang = ang0 - theta_cw
        u_vec = np.array([np.cos(ang), np.sin(ang)])
        p_end = pO + r * u_vec
        sphere_pts.append((p_end, u_vec, ang))
        weld_pts.append(pO + 0.14 * u_vec)
        
        ax_main.plot([pO[0], p_end[0]], [pO[1], p_end[1]], color='#4a5568', lw=4.5, solid_capstyle='round', zorder=4)
        ax_main.plot([pO[0], p_end[0]], [pO[1], p_end[1]], color='#cbd5e0', lw=2.0, solid_capstyle='round', zorder=4)
        
        n_perp = np.array([-np.sin(ang), np.cos(ang)])
        r_lbl_pt = pO + 0.52 * r * u_vec + (0.11 if idx != 0 else -0.11) * n_perp
        ax_main.text(r_lbl_pt[0], r_lbl_pt[1], r'$r$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
        
    weld_poly = patches.Polygon(weld_pts, closed=True, facecolor='#718096', edgecolor='#2d3748', lw=1.5, zorder=5)
    ax_main.add_patch(weld_poly)
    ax_main.plot(pO[0], pO[1], 'ko', markersize=4.5, zorder=6)
    ax_main.text(pO[0] - 0.16, pO[1] + 0.04, r'$O\ (G)$', fontsize=11, fontweight='bold', color='#1a202c', ha='right', va='bottom')
    ax_main.annotate('Welded', xy=(pO[0]-0.05, pO[1]+0.08), xytext=(pO[0]-0.55, pO[1]+0.32),
                     arrowprops=dict(arrowstyle='->', color='#444444', lw=1.1),
                     fontsize=9.5, fontweight='bold', color='#2d3748', ha='center')
    
    for idx, (p_end, u_vec, ang) in enumerate(sphere_pts):
        sph = patches.Circle(p_end, 0.135, facecolor='#7ab8e6', edgecolor='#1d4564', lw=1.8, zorder=7)
        ax_main.add_patch(sph)
        hl = patches.Circle(p_end + np.array([-0.04, 0.04]), 0.04, facecolor='#d6ecfa', edgecolor='none', zorder=8)
        ax_main.add_patch(hl)
        lbl_pos = p_end + 0.24 * u_vec
        ax_main.text(lbl_pos[0], lbl_pos[1], r'$m$', fontsize=11.5, fontweight='bold', color='#1d4564', ha='center', va='center')
        
        if omega_cw > 0.02:
            t_cw = np.array([np.sin(ang), -np.cos(ang)])
            v_end = p_end + 0.45 * omega_cw * t_cw
            ax_main.annotate('', xy=v_end, xytext=p_end,
                             arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.0, mutation_scale=12), zorder=9)
            
    u_top = sphere_pts[0][1]
    t_top_cw = np.array([u_top[1], -u_top[0]])
    p_force = pO + b * u_top
    f_start = p_force - 0.52 * t_top_cw
    ax_main.annotate('', xy=p_force, xytext=f_start,
                     arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2.6, mutation_scale=15), zorder=9)
    ax_main.text(f_start[0] - 0.08, f_start[1], r'$\mathbf{F}$', color='#d32f2f', fontsize=12.5, fontweight='bold', ha='right', va='center')
    
    b_mid = pO + 0.5 * b * u_top - 0.13 * t_top_cw
    ax_main.text(b_mid[0], b_mid[1], r'$b$', fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')
    
    ax_main.annotate('', xy=(pO[0] + 0.42, pO[1]), xytext=pO,
                     arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2.2, mutation_scale=13), zorder=9)
    ax_main.text(pO[0] + 0.46, pO[1] - 0.11, r'$\bar{\mathbf{a}} = \mathbf{a}_O$', color='#1565c0', fontsize=10.5, fontweight='bold')
    
    ax_main.set_title('Sample Problem 4/2: Spheres Welded to Rigid Frame', fontsize=13.5, fontweight='bold', pad=12)
    
    # ---------------- 2. Theoretical Derivation & Analysis View ----------------
    ax_calc.cla()
    ax_calc.set_facecolor('#ffffff')
    ax_calc.set_xlim(0, 10)
    ax_calc.set_ylim(0, 10)
    ax_calc.axis('off')
    
    sol_box = (
        "Theoretical Derivation & Analysis:\n"
        "(a) Acceleration of Point O (Mass Center G, Eq. 4.1):\n"
        r"  $\bullet$ By symmetry, point $O$ is the mass center $G$ of the 3 spheres" "\n"
        r"  $\bullet\ [\sum \mathbf{F} = m_{\mathrm{tot}}\bar{\mathbf{a}}] \quad F\mathbf{i} = 3m\bar{\mathbf{a}}$" "\n"
        r"  $\Rightarrow\ \mathbf{\bar{\mathbf{a}} = \mathbf{a}_O = \frac{F}{3m}\mathbf{i}}$ (Independent of dimension $b$!)" "\n\n"
        r"(b) Angular Acceleration $\ddot{\theta}$ of Frame (Eq. 4.9):" "\n"
        r"  $\bullet$ Welded bars share common angular velocity $\dot{\theta}$" "\n"
        r"  $\bullet$ Relative speed of each sphere about $O$: $v_{\mathrm{rel}} = r\dot{\theta}$" "\n"
        r"  $\bullet\ H_O = H_G = 3(m r\dot{\theta}) r = 3 m r^2 \dot{\theta}$ (CW)" "\n"
        r"  $\bullet\ [\sum M_G = \dot{H}_G] \quad F b = \frac{d}{dt}(3 m r^2 \dot{\theta}) = 3 m r^2 \ddot{\theta}$" "\n"
        r"  $\Rightarrow\ \mathbf{\ddot{\theta} = \frac{F b}{3 m r^2}}$ (Clockwise CW)"
    )
    ax_calc.text(0.35, 6.0, sol_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fbfbfb', edgecolor='#cccccc'))
    
    live_box = (
        f"Live Motion Monitor ($t = {t:.2f}\\ \\mathrm{{s}}$, normalized $F/(3m)=1.0,\\ Fb/(3mr^2)=0.6$):\n"
        f"Center O Accel: $a_O = F/(3m) = {a_O_x:.2f}\\ \\mathrm{{m/s^2}}$,  Speed: $v_O = {v_O:.2f}\\ \\mathrm{{m/s}}$\n"
        f"Frame Angular Accel: $\\ddot{{\\theta}} = Fb/(3mr^2) = {alpha_cw:.2f}\\ \\mathrm{{rad/s^2}}$ (common to all 3 bars)\n"
        f"Rotation Angle: $\\theta = {np.degrees(theta_cw):.1f}^\\circ$ ($120^\\circ$ spacing preserved)"
    )
    ax_calc.text(0.35, 1.45, live_box, fontsize=9.5, va='center',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#eef5f9', edgecolor='#90caf9'))
    
    ax_calc.set_title('Mass Center Motion & Angular Momentum Analysis', fontsize=13, fontweight='bold', pad=12)

anim = FuncAnimation(fig, update, frames=n_frames, interval=65)

gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex4_2_rigid_frame_spheres.gif')
anim.save(gif_path, writer='pillow', fps=15)
plt.close()
print(f'Saved: {gif_path}')
