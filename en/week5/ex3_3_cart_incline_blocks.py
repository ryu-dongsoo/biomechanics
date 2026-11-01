# -*- coding: utf-8 -*-
"""
[Dynamics 9th Ed. Sample Problem 3.3] Constrained Motion Analysis of a Log on a 30° Incline with a 2:1 Pulley System
Reproducing Textbook Schematic, Kinematics Coordinate Diagram & Detailed Free-Body Diagrams (FBD)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# Physical Parameters
mA = 125.0        # Concrete block A mass (kg)
mC = 200.0        # Log C mass (kg)
mu_k = 0.5        # Coefficient of kinetic friction
th_deg = 30.0     # Incline angle (degrees)
th_rad = np.radians(th_deg)
g = 9.81          # Gravitational acceleration (m/s^2)
h_drop = 6.0      # Drop height of Block A (m)

# FBD Equilibrium & Equation of Motion
N_C = mC * g * np.cos(th_rad)           # 1699.14 N
f_k = mu_k * N_C                        # 849.57 N
W_A = mA * g                            # 1226.25 N
W_C = mC * g                            # 1962.00 N

# 2T - mC*g*sin30 - f_k = mC*aC  (1)
# mA*g - T = mA*aA = mA*(2*aC)   (2) => 2T = 2*mA*g - 4*mA*aC
# aC = (2*mA*g - mC*g*sin30 - f_k) / (4*mA + mC)
aC = (2.0 * W_A - W_C * np.sin(th_rad) - f_k) / (4.0 * mA + mC)  # 0.8885 m/s^2
aA = 2.0 * aC                                                    # 1.7769 m/s^2
T_val = W_A - mA * aA                                            # 1004.13 N
T2_val = 2.0 * T_val                                             # 2008.26 N

# Impact Time and Final Velocity
t_impact = np.sqrt(2.0 * h_drop / aA)   # 2.599 s
vA_impact = np.sqrt(2.0 * aA * h_drop)  # 4.618 m/s
vC_impact = 0.5 * vA_impact             # 2.309 m/s

# Animation Setup
fps = 30
n_sim_frames = int(fps * t_impact)
n_pause_frames = 20
total_frames = n_sim_frames + n_pause_frames

t_eval = np.linspace(0, t_impact, n_sim_frames)

fig = plt.figure(figsize=(13.2, 8.4), dpi=120)
ax = fig.add_subplot(111)
ax.set_position([0.02, 0.02, 0.96, 0.92])
title_text = '[Dynamics 9th Ed. Sample Problem 3.3] FBD & Impact Velocity Analysis of Incline Log (200kg) & Block (125kg)'

def update(frame):
    if frame < n_sim_frames:
        t = t_eval[frame]
        sA = 0.5 * aA * (t**2)
        sC = 0.5 * aC * (t**2)
        vA = aA * t
        vC = aC * t
        is_impact = False
    else:
        t = t_impact
        sA = h_drop
        sC = 0.5 * h_drop
        vA = vA_impact
        vC = vC_impact
        is_impact = True
        
    ax.clear()
    ax.set_xlim(-1.2, 25.2)
    ax.set_ylim(-1.2, 15.2)
    ax.axis('off')
    
    # 1. Background
    ax.add_patch(patches.Rectangle((-1.2, -1.2), 26.5, 16.5, fc='#f8fafc', ec='none', zorder=1))
    
    # -------------------------------------------------------------
    # 2. Top-Left: HUD Information Box
    # -------------------------------------------------------------
    hud_str = (
        f"[Sample Problem 3.3: 2:1 Pulley Constrained Motion & FBD]\n"
        f"Time Elapsed: t = {t:4.2f} s / {t_impact:4.2f} s\n"
        f"-----------------------------------------\n"
        f"• Cable Constraint: L = 2s_C + s_A + C ⇒ a_A = 2a_C\n"
        f"• Log C (200kg, μ_k=0.5): ΣFy = 0 ⇒ N = 200(9.81)cos 30° = {N_C:.0f} N\n"
        f"  Friction: f_k = μ_k N = 0.5({N_C:.0f}) = {f_k:.0f} N\n"
        f"  ΣFx = m_C a_C ⇒ 2T - 200(9.81)sin 30° - f_k = 200 a_C\n"
        f"• Block A (125kg): ΣFy = m_A a_A ⇒ 125(9.81) - T = 125 a_A\n"
        f"• Simultaneous Sol: a_A = 1.78 m/s², a_C = 0.89 m/s², T = 1004 N, 2T = 2008 N\n"
        f"-----------------------------------------\n"
        f"• Block A Displacement: s_A(t) = {sA:4.2f} m  (Velocity v_A = {vA:4.2f} m/s)\n"
        f"• Log C Displacement:   s_C(t) = {sC:4.2f} m  (Velocity v_C = {vC:4.2f} m/s)\n"
        f"-----------------------------------------\n"
        f"▶ Block A Impact Time at Floor B (6m): t = {t_impact:.2f} s\n"
        f"▶ Impact Velocity:                    v_A = √(2·a_A·6) = {vA_impact:.2f} m/s"
    )
    ax.text(-0.2, 14.8, hud_str, fontsize=7.4, va='top', family='monospace',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#0284c7', lw=1.3, alpha=0.98), zorder=20)
    
    # -------------------------------------------------------------
    # 3. Bottom-Left: Physical Mechanism Simulation
    # -------------------------------------------------------------
    u_vec = np.array([np.cos(th_rad), np.sin(th_rad)])
    n_vec = np.array([-np.sin(th_rad), np.cos(th_rad)])
    
    P0 = np.array([0.2, 0.8])
    incline_len = 11.2
    apex_p = P0 + incline_len * u_vec
    
    incline_poly = [
        P0.tolist(),
        apex_p.tolist(),
        [apex_p[0], P0[1] - 0.6],
        [P0[0] - 0.5, P0[1] - 0.6],
    ]
    ax.add_patch(patches.Polygon(incline_poly, closed=True, fc='#e2e8f0', ec='#64748b', lw=1.5, zorder=2))
    ax.plot([P0[0] - 0.5, apex_p[0] + 0.3], [P0[1] - 0.5*np.tan(th_rad), apex_p[1] + 0.3*np.tan(th_rad)],
            color='#334155', lw=2.4, zorder=3)
    
    arc = patches.Arc((P0[0], P0[1]), 2.8, 2.8, angle=0, theta1=0, theta2=30, color='#0f172a', lw=1.3, zorder=4)
    ax.add_patch(arc)
    ax.text(P0[0] + 1.8, P0[1] + 0.35, r'$30^\circ$', fontsize=8.5, fontweight='bold', color='#0f172a', zorder=5)
    
    ground_y = P0[1] - 0.6
    ax.plot([P0[0] - 0.8, apex_p[0] + 3.8], [ground_y, ground_y], color='#334155', lw=2.0, zorder=3)
    for hx in np.linspace(P0[0] - 0.6, apex_p[0] + 3.6, 24):
        ax.plot([hx, hx - 0.3], [ground_y, ground_y - 0.35], color='#94a3b8', lw=1.0, zorder=2)
        
    # Log C
    log_L = 3.2
    log_H = 0.75
    scale_m = 0.85
    log_init_dist = 2.0
    log_dist = log_init_dist + sC * scale_m
    
    p_b_aft = P0 + (log_dist - log_L/2) * u_vec
    p_b_fore = P0 + (log_dist + log_L/2) * u_vec
    p_t_fore = p_b_fore + log_H * n_vec
    p_t_aft = p_b_aft + log_H * n_vec
    
    log_poly_pts = [p_b_aft, p_b_fore, p_t_fore, p_t_aft]
    log_poly = patches.Polygon(log_poly_pts, closed=True, fc='#d97706', ec='#78350f', lw=1.5, zorder=6)
    ax.add_patch(log_poly)
    
    ellipse_c = (p_b_aft + p_t_aft) / 2
    ellipse = patches.Ellipse(ellipse_c, log_H*0.45, log_H, angle=30+90, fc='#b45309', ec='#78350f', lw=1.2, zorder=7)
    ax.add_patch(ellipse)
    ax.scatter([ellipse_c[0]], [ellipse_c[1]], color='#78350f', s=6, zorder=8)
    
    mid_aft = (p_b_aft + p_t_aft)/2
    mid_fore = (p_b_fore + p_t_fore)/2
    ax.plot([mid_aft[0], mid_fore[0]], [mid_aft[1], mid_fore[1]], color='#b45309', lw=0.9, linestyle='--', zorder=7)
    
    log_center = (p_b_aft + p_b_fore + p_t_fore + p_t_aft) / 4
    ax.text(log_center[0] - 0.2, log_center[1] + 0.8, r'$200\text{ kg}$', fontsize=8.5, fontweight='bold', color='#78350f', zorder=8)
    ax.text(log_center[0] + 0.6, log_center[1] - 0.7, r'$\mu_k = 0.5$', fontsize=8.0, fontweight='bold', color='#0f172a', zorder=8)
    
    # Movable Pulley C
    pulleyC_R = 0.42
    pulleyC_dist = log_dist + log_L/2 + 1.3
    pulleyC_c = P0 + pulleyC_dist * u_vec + (log_H/2) * n_vec
    
    link_start = (p_b_fore + p_t_fore) / 2
    ax.plot([link_start[0], pulleyC_c[0]], [link_start[1], pulleyC_c[1]], color='#334155', lw=2.2, zorder=5)
    ax.add_patch(patches.Circle(pulleyC_c, pulleyC_R, fc='#fef08a', ec='#ca8a04', lw=1.4, zorder=6))
    ax.scatter([pulleyC_c[0]], [pulleyC_c[1]], color='#ca8a04', s=16, zorder=7)
    ax.text(pulleyC_c[0] - 0.35, pulleyC_c[1] + 0.55, r'$C$', fontsize=10.0, fontweight='bold', color='#ca8a04', zorder=8)
    
    # Fixed Pulley
    fix_R = 0.52
    fix_dist = 11.5
    fix_c = P0 + fix_dist * u_vec + (log_H/2 + pulleyC_R - fix_R) * n_vec
    
    bracket_top = fix_c + 1.4 * np.array([0, 1])
    ax.plot([fix_c[0], fix_c[0]], [fix_c[1], bracket_top[1]], color='#475569', lw=2.4, zorder=4)
    ax.add_patch(patches.Rectangle((fix_c[0] - 0.6, bracket_top[1]), 1.2, 0.3, fc='#64748b', ec='#334155', lw=1.2, zorder=4))
    for bx in np.linspace(fix_c[0] - 0.5, fix_c[0] + 0.5, 5):
        ax.plot([bx, bx + 0.2], [bracket_top[1] + 0.3, bracket_top[1] + 0.5], color='#94a3b8', lw=1.0, zorder=3)
        
    ax.add_patch(patches.Circle(fix_c, fix_R, fc='#e0f2fe', ec='#0284c7', lw=1.5, zorder=5))
    ax.scatter([fix_c[0]], [fix_c[1]], color='#0284c7', s=18, zorder=6)
    
    # Cable path
    c_bot_p = pulleyC_c - pulleyC_R * n_vec
    c_top_p = pulleyC_c + pulleyC_R * n_vec
    fix_top_p = fix_c + fix_R * n_vec
    fix_right_p = fix_c + np.array([fix_R, 0])
    
    anchor_p = fix_c - (fix_R - pulleyC_R) * n_vec - 0.3 * u_vec
    
    # (1) Anchor -> Pulley C bottom
    ax.plot([anchor_p[0], c_bot_p[0]], [anchor_p[1], c_bot_p[1]], color='#1e293b', lw=1.6, zorder=5)
    ax.scatter([anchor_p[0]], [anchor_p[1]], color='#334155', s=14, zorder=6)
    
    # (2) Pulley C arc
    theta_c_start = th_deg - 90
    theta_c_end = th_deg + 90
    arc_c = patches.Arc(pulleyC_c, 2*pulleyC_R, 2*pulleyC_R, angle=0,
                        theta1=theta_c_end, theta2=theta_c_start+360, color='#1e293b', lw=1.6, zorder=5)
    ax.add_patch(arc_c)
    
    # (3) Pulley C top -> Fixed pulley top
    ax.plot([c_top_p[0], fix_top_p[0]], [c_top_p[1], fix_top_p[1]], color='#1e293b', lw=1.6, zorder=5)
    
    # (4) Fixed pulley arc
    arc_fix = patches.Arc(fix_c, 2*fix_R, 2*fix_R, angle=0,
                          theta1=0, theta2=th_deg + 90, color='#1e293b', lw=1.6, zorder=5)
    ax.add_patch(arc_fix)
    
    # (5) Fixed pulley -> Block A
    blockA_x = fix_right_p[0]
    blockA_init_y = fix_c[1] - 1.2
    blockA_y = blockA_init_y - sA * scale_m
    
    ax.plot([blockA_x, blockA_x], [fix_right_p[1], blockA_y + 0.6], color='#1e293b', lw=1.8, zorder=5)
    
    blockA_w, blockA_h = 1.2, 1.2
    block_fc = '#ef4444' if is_impact else '#fca5a5'
    ax.add_patch(patches.Rectangle((blockA_x - blockA_w/2, blockA_y - blockA_h/2), blockA_w, blockA_h,
                                   fc=block_fc, ec='#991b1b', lw=1.4, zorder=6))
    ax.text(blockA_x, blockA_y + 0.15, r'$A$', fontsize=9.5, fontweight='bold', color='#ffffff' if is_impact else '#7f1d1d', ha='center', zorder=7)
    ax.text(blockA_x, blockA_y - 0.25, r'$125\text{ kg}$', fontsize=7.5, fontweight='bold', color='#ffffff' if is_impact else '#7f1d1d', ha='center', zorder=7)
    
    # Floor B
    floorB_y = blockA_init_y - h_drop * scale_m - blockA_h/2
    ax.plot([blockA_x - 1.2, blockA_x + 1.2], [floorB_y, floorB_y], color='#1e293b', lw=2.4, zorder=3)
    for fx in np.linspace(blockA_x - 1.0, blockA_x + 1.0, 6):
        ax.plot([fx, fx - 0.2], [floorB_y, floorB_y - 0.25], color='#94a3b8', lw=1.0, zorder=2)
    ax.text(blockA_x + 1.4, floorB_y + 0.05, r'$B$', fontsize=10.5, fontweight='bold', color='#0f172a', va='bottom', zorder=8)
    
    # 6m dimension line
    dim_x = blockA_x - 1.2
    ax.plot([blockA_x - 0.7, dim_x - 0.2], [blockA_init_y - blockA_h/2, blockA_init_y - blockA_h/2], color='#64748b', lw=0.9, zorder=4)
    ax.plot([blockA_x - 0.7, dim_x - 0.2], [floorB_y, floorB_y], color='#64748b', lw=0.9, zorder=4)
    ax.annotate('', xy=(dim_x, floorB_y), xytext=(dim_x, blockA_init_y - blockA_h/2),
                arrowprops=dict(arrowstyle='<->', color='#b91c1c', lw=1.2), zorder=6)
    ax.text(dim_x - 0.15, (blockA_init_y - blockA_h/2 + floorB_y)/2, r'$6\text{ m}$',
            fontsize=8.5, fontweight='bold', color='#b91c1c', ha='right', va='center', zorder=7)
    
    # -------------------------------------------------------------
    # 4. Right Area: Kinematics Coordinates & Separated FBDs
    # -------------------------------------------------------------
    fbd_card = patches.FancyBboxPatch((12.5, 0.4), 12.2, 14.3,
                                      boxstyle="round,pad=0.25", fc="#ffffff", ec='#94a3b8', lw=1.3, alpha=0.98, zorder=10)
    ax.add_patch(fbd_card)
    
    # (1) Top: Kinematics Coordinates
    ax.text(18.6, 14.2, '[Kinematics & Coordinate System]', fontsize=9.0, fontweight='bold', color='#0f172a', ha='center', zorder=12)
    
    k_apex_x = 21.5
    k_apex_y = 12.8
    ax.plot([k_apex_x - 1.5, k_apex_x + 0.8], [k_apex_y + 1.5*np.tan(th_rad), k_apex_y - 0.8*np.tan(th_rad)],
            color='#94a3b8', lw=1.0, linestyle='--', zorder=11)
    ax.add_patch(patches.Circle((k_apex_x, k_apex_y), 0.35, fc='#e0f2fe', ec='#0284c7', lw=1.2, zorder=12))
    
    k_sc_len = 3.2
    k_pulleyC_x = k_apex_x - k_sc_len * np.cos(th_rad)
    k_pulleyC_y = k_apex_y - k_sc_len * np.sin(th_rad)
    ax.add_patch(patches.Circle((k_pulleyC_x, k_pulleyC_y), 0.3, fc='#fef08a', ec='#ca8a04', lw=1.2, zorder=12))
    ax.text(k_pulleyC_x - 0.25, k_pulleyC_y - 0.35, r'$C$', fontsize=8.5, fontweight='bold', color='#ca8a04', zorder=13)
    
    ax.plot([k_pulleyC_x, k_apex_x], [k_pulleyC_y + 0.2, k_apex_y + 0.2], color='#1e293b', lw=1.2, zorder=11)
    ax.plot([k_pulleyC_x, k_apex_x], [k_pulleyC_y - 0.2, k_apex_y - 0.2], color='#1e293b', lw=1.2, zorder=11)
    
    # s_C dimension
    ax.plot([k_apex_x + 0.4*np.sin(th_rad), k_apex_x + 1.2*np.sin(th_rad)],
            [k_apex_y + 0.4*np.cos(th_rad), k_apex_y + 1.2*np.cos(th_rad)], color='#64748b', lw=0.9, zorder=11)
    ax.plot([k_pulleyC_x + 0.4*np.sin(th_rad), k_pulleyC_x + 1.2*np.sin(th_rad)],
            [k_pulleyC_y + 0.4*np.cos(th_rad), k_pulleyC_y + 1.2*np.cos(th_rad)], color='#64748b', lw=0.9, zorder=11)
    
    dim_sc_p1 = (k_pulleyC_x + 0.8*np.sin(th_rad), k_pulleyC_y + 0.8*np.cos(th_rad))
    dim_sc_p2 = (k_apex_x + 0.8*np.sin(th_rad), k_apex_y + 0.8*np.cos(th_rad))
    ax.annotate('', xy=dim_sc_p1, xytext=dim_sc_p2, arrowprops=dict(arrowstyle='<->', color='#0284c7', lw=1.2), zorder=12)
    ax.text((dim_sc_p1[0] + dim_sc_p2[0])/2 + 0.1, (dim_sc_p1[1] + dim_sc_p2[1])/2 + 0.25, r'$s_C$',
            fontsize=9.0, fontweight='bold', color='#0284c7', ha='center', zorder=13)
    
    # Block A & s_A dimension
    k_blockA_x = k_apex_x + 0.35
    k_blockA_y = k_apex_y - 2.4
    ax.plot([k_blockA_x, k_blockA_x], [k_apex_y, k_blockA_y + 0.4], color='#1e293b', lw=1.2, zorder=11)
    ax.add_patch(patches.Rectangle((k_blockA_x - 0.4, k_blockA_y - 0.4), 0.8, 0.8, fc='#fca5a5', ec='#991b1b', lw=1.1, zorder=12))
    ax.text(k_blockA_x, k_blockA_y, r'$A$', fontsize=8.5, fontweight='bold', color='#7f1d1d', ha='center', va='center', zorder=13)
    
    ax.plot([k_blockA_x + 0.5, k_blockA_x + 1.3], [k_apex_y, k_apex_y], color='#64748b', lw=0.9, zorder=11)
    ax.plot([k_blockA_x + 0.5, k_blockA_x + 1.3], [k_blockA_y, k_blockA_y], color='#64748b', lw=0.9, zorder=11)
    ax.annotate('', xy=(k_blockA_x + 1.0, k_blockA_y), xytext=(k_blockA_x + 1.0, k_apex_y),
                arrowprops=dict(arrowstyle='<->', color='#b91c1c', lw=1.2), zorder=12)
    ax.text(k_blockA_x + 1.2, (k_apex_y + k_blockA_y)/2, r'$s_A$', fontsize=9.0, fontweight='bold', color='#b91c1c', va='center', zorder=13)
    
    ax.text(18.6, 9.7, r'$L = 2s_C + s_A + \text{const} \quad \Longrightarrow \quad a_A = 2a_C$',
            fontsize=8.2, fontweight='bold', color='#0f172a', ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=0.8), zorder=13)
    
    ax.plot([13.0, 24.2], [9.3, 9.3], color='#e2e8f0', lw=1.2, zorder=11)
    
    # (2) Bottom: Free-Body Diagrams (FBD)
    ax.text(18.6, 9.0, '[Free-Body Diagrams (FBD)]', fontsize=9.0, fontweight='bold', color='#b91c1c', ha='center', zorder=12)
    
    # [FBD 1] Pulley C
    fbd_c_x = 20.2
    fbd_c_y = 7.7
    ax.add_patch(patches.Circle((fbd_c_x, fbd_c_y), 0.32, fc='#fef08a', ec='#ca8a04', lw=1.2, zorder=12))
    ax.text(fbd_c_x - 0.45, fbd_c_y + 0.1, r'$C$', fontsize=8.5, fontweight='bold', color='#ca8a04', zorder=13)
    
    t1_s = (fbd_c_x + 0.2*np.sin(th_rad), fbd_c_y + 0.2*np.cos(th_rad))
    t1_e = (t1_s[0] + 1.2*np.cos(th_rad), t1_s[1] + 1.2*np.sin(th_rad))
    ax.annotate('', xy=t1_e, xytext=t1_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.5, headwidth=4.5, headlength=5.5), zorder=14)
    ax.text(t1_e[0] + 0.15, t1_e[1] + 0.1, r'$T$', fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=15)
    
    t2_s = (fbd_c_x - 0.2*np.sin(th_rad), fbd_c_y - 0.2*np.cos(th_rad))
    t2_e = (t2_s[0] + 1.2*np.cos(th_rad), t2_s[1] + 1.2*np.sin(th_rad))
    ax.annotate('', xy=t2_e, xytext=t2_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.5, headwidth=4.5, headlength=5.5), zorder=14)
    ax.text(t2_e[0] + 0.15, t2_e[1] - 0.1, r'$T$', fontsize=8.5, fontweight='bold', color='#b91c1c', zorder=15)
    
    t3_e = (fbd_c_x - 1.4*np.cos(th_rad), fbd_c_y - 1.4*np.sin(th_rad))
    ax.annotate('', xy=t3_e, xytext=(fbd_c_x, fbd_c_y), arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.0, headlength=6.0), zorder=14)
    ax.text(t3_e[0] - 0.2, t3_e[1] - 0.2, r'$2T$', fontsize=9.0, fontweight='bold', color='#b91c1c', ha='right', zorder=15)
    
    # [FBD 2] Log FBD
    fbd_log_cx = 15.6
    fbd_log_cy = 4.2
    fbd_len = 2.4
    fbd_w = 0.6
    
    fl_dx = (fbd_len/2)*np.cos(th_rad)
    fl_dy = (fbd_len/2)*np.sin(th_rad)
    fl_nx = -(fbd_w/2)*np.sin(th_rad)
    fl_ny = (fbd_w/2)*np.cos(th_rad)
    
    fbd_log_pts = [
        [fbd_log_cx - fl_dx + fl_nx, fbd_log_cy - fl_dy + fl_ny],
        [fbd_log_cx + fl_dx + fl_nx, fbd_log_cy + fl_dy + fl_ny],
        [fbd_log_cx + fl_dx - fl_nx, fbd_log_cy + fl_dy - fl_ny],
        [fbd_log_cx - fl_dx - fl_nx, fbd_log_cy - fl_dy - fl_ny],
    ]
    ax.add_patch(patches.Polygon(fbd_log_pts, closed=True, fc='#ffffff', ec='#78350f', lw=1.3, zorder=12))
    
    ax.plot([fbd_log_cx, fbd_log_cx - 2.0*np.cos(th_rad)], [fbd_log_cy, fbd_log_cy - 2.0*np.sin(th_rad)],
            color='#475569', lw=1.0, linestyle='--', zorder=13)
    ax.text(fbd_log_cx - 2.1*np.cos(th_rad) - 0.15, fbd_log_cy - 2.1*np.sin(th_rad), r'$x$',
            fontsize=8.5, fontweight='bold', color='#475569', ha='right', zorder=14)
    
    ax.plot([fbd_log_cx, fbd_log_cx - 1.8*np.sin(th_rad)], [fbd_log_cy, fbd_log_cy + 1.8*np.cos(th_rad)],
            color='#475569', lw=1.0, linestyle='--', zorder=13)
    ax.text(fbd_log_cx - 1.9*np.sin(th_rad) - 0.2, fbd_log_cy + 1.9*np.cos(th_rad), r'$y$',
            fontsize=8.5, fontweight='bold', color='#475569', va='bottom', zorder=14)
    
    # 1) Tension 2T
    t_pull_s = (fbd_log_cx + fl_dx, fbd_log_cy + fl_dy)
    t_pull_e = (t_pull_s[0] + 1.4*np.cos(th_rad), t_pull_s[1] + 1.4*np.sin(th_rad))
    ax.annotate('', xy=t_pull_e, xytext=t_pull_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text(t_pull_e[0] + 0.15, t_pull_e[1], r'$2T$', fontsize=9.5, fontweight='bold', color='#b91c1c', zorder=16)
    
    # 2) Normal force N
    n_s = (fbd_log_cx - 1.4*np.sin(th_rad), fbd_log_cy - 1.4*np.cos(th_rad))
    n_e = (fbd_log_cx, fbd_log_cy)
    ax.annotate('', xy=n_e, xytext=n_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text(n_s[0] + 0.15, n_s[1] - 0.2, r'$N$', fontsize=9.5, fontweight='bold', color='#b91c1c', zorder=16)
    
    # 3) Friction force 0.5N
    f_s = (fbd_log_cx, fbd_log_cy - fl_ny)
    f_e = (f_s[0] - 1.2*np.cos(th_rad), f_s[1] - 1.2*np.sin(th_rad))
    ax.annotate('', xy=f_e, xytext=f_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.6, headwidth=5.0, headlength=6.0), zorder=15)
    ax.text(f_e[0] - 0.1, f_e[1] - 0.25, r'$0.5N$', fontsize=8.5, fontweight='bold', color='#b91c1c', ha='right', zorder=16)
    
    # 4) Weight 200(9.81) N
    w_log_s = (fbd_log_cx, fbd_log_cy + 1.6)
    w_log_e = (fbd_log_cx, fbd_log_cy)
    ax.annotate('', xy=w_log_e, xytext=w_log_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text(w_log_s[0] + 0.1, w_log_s[1] + 0.1, r'$200(9.81)\text{ N}$', fontsize=8.5, fontweight='bold', color='#b91c1c', ha='center', va='bottom', zorder=16)
    
    # [FBD 3] Block A FBD
    fbd_a_cx = 22.0
    fbd_a_cy = 3.2
    fbd_a_w, fbd_a_h = 0.9, 0.9
    ax.add_patch(patches.Rectangle((fbd_a_cx - fbd_a_w/2, fbd_a_cy - fbd_a_h/2), fbd_a_w, fbd_a_h,
                                   fc='#ffffff', ec='#991b1b', lw=1.2, zorder=12))
    
    # 1) Tension T
    a_t_s = (fbd_a_cx, fbd_a_cy + fbd_a_h/2)
    a_t_e = (fbd_a_cx, a_t_s[1] + 1.4)
    ax.annotate('', xy=a_t_e, xytext=a_t_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text(a_t_e[0], a_t_e[1] + 0.15, r'$T$', fontsize=9.5, fontweight='bold', color='#b91c1c', ha='center', va='bottom', zorder=16)
    
    # 2) Weight 125(9.81) N
    a_w_s = (fbd_a_cx, fbd_a_cy - fbd_a_h/2)
    a_w_e = (fbd_a_cx, a_w_s[1] - 1.4)
    ax.annotate('', xy=a_w_e, xytext=a_w_s, arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=1.8, headwidth=5.5, headlength=6.5), zorder=15)
    ax.text(a_w_e[0], a_w_e[1] - 0.25, r'$125(9.81)\text{ N}$', fontsize=8.5, fontweight='bold', color='#b91c1c', ha='center', va='top', zorder=16)
    
    # 3) Acceleration axis +
    ax.plot([fbd_a_cx + 0.8, fbd_a_cx + 0.8], [fbd_a_cy - 0.8, fbd_a_cy - 1.5], color='#475569', lw=1.0, linestyle='--', zorder=13)
    ax.text(fbd_a_cx + 1.0, fbd_a_cy - 1.5, r'$+$', fontsize=9.0, fontweight='bold', color='#475569', va='center', zorder=14)

fig.suptitle(title_text, fontsize=11.5, fontweight='bold', y=0.97)
anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
out_gif = os.path.join(os.path.dirname(__file__), 'ex3_3_cart_incline_blocks.gif')
anim.save(out_gif, writer=writer)
plt.close()
print(f'Rendered {out_gif}')
