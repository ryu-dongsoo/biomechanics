# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Dongsoo Ryu (유동수). All rights reserved.
#   - Affiliation : Dept. of Bioindustrial Machinery Engineering,
#                   Jeonbuk National University (전북대학교 생물산업기계공학과)
#   - Author      : Dongsoo Ryu (유동수)
#   - Contact     : ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com
#   - Course      : Biomechanics (생물역학)
# =============================================================================

# 3D Coordinate Systems Comparison in 3D Space
# Top row (3 columns): (a) Cartesian, (b) Cylindrical, (c) Spherical 3D views (titles at bottom)
# Bottom row (2 columns): (d) Unified 3D Overlay (title at bottom) + Dedicated Transformation Card

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# --- 1. Point P Coordinates ---
x_P = 4.0
y_P = 3.0
z_P = 5.0

# Cylindrical parameters (r, theta, z)
r_P = np.sqrt(x_P**2 + y_P**2)        # 5.0
theta_P = np.arctan2(y_P, x_P)        # ~36.87°
# Spherical parameters (R, theta, phi)
R_P = np.sqrt(x_P**2 + y_P**2 + z_P**2) # sqrt(50) ≈ 7.071
phi_P = np.arctan2(z_P, r_P)            # 45.0°

# --- 2. Canvas & GridSpec Layout (2 Rows, suptitle removed) ---
fig = plt.figure(figsize=(19, 13.5), dpi=150, facecolor='#f4f7f9')

gs = fig.add_gridspec(2, 6, height_ratios=[1.0, 1.05], hspace=0.25, wspace=0.22,
                      left=0.02, right=0.98, bottom=0.075, top=0.98)

def setup_3d_ax(ax):
    ax.set_facecolor('#ffffff')
    
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 5.5)
    ax.set_zlim(0, 6.5)
    
    ax.set_xlabel('$x$', fontsize=11.5, fontweight='bold', labelpad=2)
    ax.set_ylabel('$y$', fontsize=11.5, fontweight='bold', labelpad=2)
    ax.set_zlabel('$z$', fontsize=11.5, fontweight='bold', labelpad=2)
    
    ax.view_init(elev=22, azim=-55)
    
    ax.plot([0, 6.0], [0, 0], [0, 0], color='#2c3e50', lw=1.3)
    ax.plot([0, 0], [0, 5.0], [0, 0], color='#2c3e50', lw=1.3)
    ax.plot([0, 0], [0, 0], [0, 6.0], color='#2c3e50', lw=1.3)
    
    ax.grid(True, linestyle=':', alpha=0.5)

def add_bottom_title(ax, title, color_theme):
    ax.text2D(0.5, -0.035, title, transform=ax.transAxes,
              fontsize=13.0, fontweight='bold', color=color_theme,
              ha='center', va='top', linespacing=1.25)

vec_len = 1.3

# =============================================================
# [Top Row]: (a) Cartesian, (b) Cylindrical, (c) Spherical
# =============================================================

# (a) Cartesian (gs[0, 0:2])
ax1 = fig.add_subplot(gs[0, 0:2], projection='3d')
setup_3d_ax(ax1)
add_bottom_title(ax1, '(a) Cartesian (Rectangular) Coordinates\nVariables: $(x, y, z)$ | Unit Vectors: $(\\mathbf{i}, \\mathbf{j}, \\mathbf{k})$', '#2980b9')

ax1.plot([x_P, x_P], [0, y_P], [0, 0], color='#2980b9', ls='--', lw=1.2, alpha=0.7)
ax1.plot([0, x_P], [y_P, y_P], [0, 0], color='#2980b9', ls='--', lw=1.2, alpha=0.7)
ax1.plot([x_P, x_P], [y_P, y_P], [0, z_P], color='#2980b9', ls='--', lw=1.5, alpha=0.9)
ax1.plot([0, x_P], [0, y_P], [0, 0], color='#7f8c8d', ls=':', lw=1.0)

box_bottom = [[0,0,0], [x_P,0,0], [x_P,y_P,0], [0,y_P,0]]
box_side1 = [[x_P,0,0], [x_P,y_P,0], [x_P,y_P,z_P], [x_P,0,z_P]]
box_side2 = [[0,y_P,0], [x_P,y_P,0], [x_P,y_P,z_P], [0,y_P,z_P]]
poly1 = Poly3DCollection([box_bottom, box_side1, box_side2], alpha=0.08, facecolor='#3498db', edgecolor='#2980b9', lw=0.8)
ax1.add_collection3d(poly1)

ax1.scatter([x_P], [y_P], [z_P], color='#e74c3c', s=60, zorder=10)
ax1.text(x_P + 0.2, y_P + 0.2, z_P + 0.2, "$P(x, y, z)$", fontsize=11.5, fontweight='bold', color='#c0392b')
ax1.scatter([x_P], [y_P], [0], color='#7f8c8d', s=25)
ax1.text(x_P + 0.1, y_P + 0.1, -0.4, "$P'(x, y, 0)$", fontsize=9, color='#7f8c8d')

ax1.quiver(0, 0, 0, x_P, y_P, z_P, color='#2c3e50', lw=1.8, arrow_length_ratio=0.08)
ax1.text(x_P/2 - 0.3, y_P/2, z_P/2 + 0.35, "$\\mathbf{r}$", fontsize=12, fontweight='bold', color='#2c3e50')

ax1.text(x_P/2, -0.35, 0, "$x = 4$", fontsize=10.5, fontweight='bold', color='#2980b9', ha='center')
ax1.text(x_P + 0.35, y_P/2, 0, "$y = 3$", fontsize=10.5, fontweight='bold', color='#2980b9', ha='left')
ax1.text(x_P + 0.25, y_P + 0.25, z_P/2, "$z = 5$", fontsize=10.5, fontweight='bold', color='#2980b9', ha='left')

ax1.quiver(x_P, y_P, z_P, vec_len, 0, 0, color='#2980b9', lw=2.2, arrow_length_ratio=0.2)
ax1.text(x_P + vec_len + 0.1, y_P, z_P, "$\\mathbf{i}$", fontsize=12, fontweight='bold', color='#2980b9')
ax1.quiver(x_P, y_P, z_P, 0, vec_len, 0, color='#2980b9', lw=2.2, arrow_length_ratio=0.2)
ax1.text(x_P, y_P + vec_len + 0.1, z_P, "$\\mathbf{j}$", fontsize=12, fontweight='bold', color='#2980b9')
ax1.quiver(x_P, y_P, z_P, 0, 0, vec_len, color='#2980b9', lw=2.2, arrow_length_ratio=0.2)
ax1.text(x_P, y_P, z_P + vec_len + 0.1, "$\\mathbf{k}$", fontsize=12, fontweight='bold', color='#2980b9')

info1 = (
    "• $\\mathbf{r} = x\\mathbf{i} + y\\mathbf{j} + z\\mathbf{k}$\n"
    "• $\\mathbf{v} = \\dot{x}\\mathbf{i} + \\dot{y}\\mathbf{j} + \\dot{z}\\mathbf{k}$\n"
    "• $\\mathbf{a} = \\ddot{x}\\mathbf{i} + \\ddot{y}\\mathbf{j} + \\ddot{z}\\mathbf{k}$"
)
ax1.text2D(0.03, 0.82, info1, transform=ax1.transAxes, fontsize=9.2,
           bbox=dict(facecolor='white', alpha=0.92, edgecolor='#2980b9', boxstyle='round,pad=0.35', lw=1.2))

# (b) Cylindrical (gs[0, 2:4])
ax2 = fig.add_subplot(gs[0, 2:4], projection='3d')
setup_3d_ax(ax2)
add_bottom_title(ax2, '(b) Cylindrical Coordinates\nVariables: $(r, \\theta, z)$ | Unit Vectors: $(\\mathbf{e}_r, \\mathbf{e}_\\theta, \\mathbf{e}_z)$', '#27ae60')

th_arc = np.linspace(0, theta_P, 30)
x_arc = r_P * np.cos(th_arc)
y_arc = r_P * np.sin(th_arc)
ax2.plot(x_arc, y_arc, np.zeros_like(x_arc), color='#27ae60', lw=1.8, ls='-')

th_small = np.linspace(0, theta_P, 20)
r_small = 1.8
ax2.plot(r_small * np.cos(th_small), r_small * np.sin(th_small), np.zeros_like(th_small), color='#e67e22', lw=2.0)
ax2.text(2.1 * np.cos(theta_P/2), 2.1 * np.sin(theta_P/2), 0.1, "$\\theta$", fontsize=12, fontweight='bold', color='#e67e22')

z_ribbon = np.linspace(0, z_P, 20)
TH_mesh, Z_mesh = np.meshgrid(th_arc, z_ribbon)
X_cyl = r_P * np.cos(TH_mesh)
Y_cyl = r_P * np.sin(TH_mesh)
ax2.plot_surface(X_cyl, Y_cyl, Z_mesh, alpha=0.12, color='#2ecc71', edgecolor='none')

ax2.plot([0, x_P], [0, y_P], [0, 0], color='#27ae60', lw=2.0, ls='-')
ax2.text(x_P/2 + 0.1, y_P/2 - 0.35, 0.1, "$r = 5$", fontsize=10.5, fontweight='bold', color='#27ae60')

ax2.plot([x_P, x_P], [y_P, y_P], [0, z_P], color='#27ae60', lw=1.8, ls='--')
ax2.text(x_P + 0.25, y_P + 0.25, z_P/2, "$z = 5$", fontsize=10.5, fontweight='bold', color='#27ae60')

ax2.scatter([x_P], [y_P], [z_P], color='#e74c3c', s=60, zorder=10)
ax2.text(x_P + 0.2, y_P + 0.2, z_P + 0.2, "$P(r, \\theta, z)$", fontsize=11.5, fontweight='bold', color='#c0392b')
ax2.scatter([x_P], [y_P], [0], color='#7f8c8d', s=25)
ax2.text(x_P + 0.1, y_P + 0.1, -0.4, "$P'(r, \\theta, 0)$", fontsize=9, color='#7f8c8d')

ax2.quiver(0, 0, 0, x_P, y_P, z_P, color='#2c3e50', lw=1.8, arrow_length_ratio=0.08)
ax2.text(x_P/2 - 0.3, y_P/2, z_P/2 + 0.35, "$\\mathbf{r}$", fontsize=12, fontweight='bold', color='#2c3e50')

er_x = np.cos(theta_P)
er_y = np.sin(theta_P)
etheta_x = -np.sin(theta_P)
etheta_y = np.cos(theta_P)

ax2.quiver(x_P, y_P, z_P, er_x*vec_len, er_y*vec_len, 0, color='#27ae60', lw=2.2, arrow_length_ratio=0.2)
ax2.text(x_P + er_x*vec_len + 0.1, y_P + er_y*vec_len + 0.1, z_P, "$\\mathbf{e}_r$", fontsize=12, fontweight='bold', color='#27ae60')

ax2.quiver(x_P, y_P, z_P, etheta_x*vec_len, etheta_y*vec_len, 0, color='#e67e22', lw=2.2, arrow_length_ratio=0.2)
ax2.text(x_P + etheta_x*vec_len - 0.35, y_P + etheta_y*vec_len + 0.2, z_P, "$\\mathbf{e}_\\theta$", fontsize=12, fontweight='bold', color='#e67e22')

ax2.quiver(x_P, y_P, z_P, 0, 0, vec_len, color='#2980b9', lw=2.2, arrow_length_ratio=0.2)
ax2.text(x_P, y_P, z_P + vec_len + 0.1, "$\\mathbf{e}_z$", fontsize=12, fontweight='bold', color='#2980b9')

info2 = (
    "• $\\mathbf{r} = r\\mathbf{e}_r + z\\mathbf{e}_z$\n"
    "• $\\mathbf{v} = \\dot{r}\\mathbf{e}_r + r\\dot{\\theta}\\mathbf{e}_\\theta + \\dot{z}\\mathbf{e}_z$\n"
    "• $a_r = \\ddot{r} - r\\dot{\\theta}^2$\n"
    "• $a_\\theta = r\\ddot{\\theta} + 2\\dot{r}\\dot{\\theta}$\n"
    "• $a_z = \\ddot{z}$"
)
ax2.text2D(0.03, 0.76, info2, transform=ax2.transAxes, fontsize=8.8,
           bbox=dict(facecolor='white', alpha=0.92, edgecolor='#27ae60', boxstyle='round,pad=0.35', lw=1.2))

# (c) Spherical (gs[0, 4:6])
ax3 = fig.add_subplot(gs[0, 4:6], projection='3d')
setup_3d_ax(ax3)
add_bottom_title(ax3, '(c) Spherical Coordinates\nVariables: $(R, \\theta, \\phi)$ | Unit Vectors: $(\\mathbf{e}_R, \\mathbf{e}_\\theta, \\mathbf{e}_\\phi)$', '#8e44ad')

ax3.plot(r_small * np.cos(th_small), r_small * np.sin(th_small), np.zeros_like(th_small), color='#e67e22', lw=2.0)
ax3.text(2.1 * np.cos(theta_P/2), 2.1 * np.sin(theta_P/2), 0.1, "$\\theta$", fontsize=12, fontweight='bold', color='#e67e22')

phi_arc = np.linspace(0, phi_P, 25)
r_phi_arc = 2.5
x_phi = r_phi_arc * np.cos(phi_arc) * np.cos(theta_P)
y_phi = r_phi_arc * np.cos(phi_arc) * np.sin(theta_P)
z_phi = r_phi_arc * np.sin(phi_arc)
ax3.plot(x_phi, y_phi, z_phi, color='#8e44ad', lw=2.0)
ax3.text(x_phi[14] + 0.1, y_phi[14] + 0.1, z_phi[14] + 0.3, "$\\phi$", fontsize=12, fontweight='bold', color='#8e44ad')

rad_grid = np.linspace(0, R_P, 20)
RAD_mesh, PHI_mesh = np.meshgrid(rad_grid, phi_arc)
X_sph_wedge = RAD_mesh * np.cos(PHI_mesh) * np.cos(theta_P)
Y_sph_wedge = RAD_mesh * np.cos(PHI_mesh) * np.sin(theta_P)
Z_sph_wedge = RAD_mesh * np.sin(PHI_mesh)
ax3.plot_surface(X_sph_wedge, Y_sph_wedge, Z_sph_wedge, alpha=0.15, color='#9b59b6', edgecolor='none')

ax3.plot([0, x_P], [0, y_P], [0, 0], 'k--', lw=1.2, alpha=0.6)
ax3.plot([x_P, x_P], [y_P, y_P], [0, z_P], 'k:', lw=1.2, alpha=0.6)

ax3.quiver(0, 0, 0, x_P, y_P, z_P, color='#8e44ad', lw=2.2, arrow_length_ratio=0.08)
ax3.text(x_P/2 - 0.35, y_P/2 - 0.2, z_P/2 + 0.35, "$R = 7.07$", fontsize=10.5, fontweight='bold', color='#8e44ad')

ax3.scatter([x_P], [y_P], [z_P], color='#e74c3c', s=60, zorder=10)
ax3.text(x_P + 0.2, y_P + 0.2, z_P + 0.2, "$P(R, \\theta, \\phi)$", fontsize=11.5, fontweight='bold', color='#c0392b')

eR_x = np.cos(phi_P) * np.cos(theta_P)
eR_y = np.cos(phi_P) * np.sin(theta_P)
eR_z = np.sin(phi_P)

ephi_x = -np.sin(phi_P) * np.cos(theta_P)
ephi_y = -np.sin(phi_P) * np.sin(theta_P)
ephi_z = np.cos(phi_P)

ax3.quiver(x_P, y_P, z_P, eR_x*vec_len, eR_y*vec_len, eR_z*vec_len, color='#8e44ad', lw=2.2, arrow_length_ratio=0.2)
ax3.text(x_P + eR_x*vec_len + 0.1, y_P + eR_y*vec_len + 0.1, z_P + eR_z*vec_len + 0.1, "$\\mathbf{e}_R$", fontsize=12, fontweight='bold', color='#8e44ad')

ax3.quiver(x_P, y_P, z_P, etheta_x*vec_len, etheta_y*vec_len, 0, color='#e67e22', lw=2.2, arrow_length_ratio=0.2)
ax3.text(x_P + etheta_x*vec_len - 0.35, y_P + etheta_y*vec_len + 0.2, z_P, "$\\mathbf{e}_\\theta$", fontsize=12, fontweight='bold', color='#e67e22')

ax3.quiver(x_P, y_P, z_P, ephi_x*vec_len, ephi_y*vec_len, ephi_z*vec_len, color='#16a085', lw=2.2, arrow_length_ratio=0.2)
ax3.text(x_P + ephi_x*vec_len - 0.25, y_P + ephi_y*vec_len, z_P + ephi_z*vec_len + 0.2, "$\\mathbf{e}_\\phi$", fontsize=12, fontweight='bold', color='#16a085')

info3 = (
    "• $\\mathbf{r} = R\\mathbf{e}_R$\n"
    "• $\\mathbf{v} = \\dot{R}\\mathbf{e}_R + R\\dot{\\theta}\\cos\\phi\\mathbf{e}_\\theta + R\\dot{\\phi}\\mathbf{e}_\\phi$\n"
    "• $a_R = \\ddot{R} - R\\dot{\\phi}^2 - R\\dot{\\theta}^2\\cos^2\\phi$\n"
    "• $a_\\theta = \\frac{1}{R\\cos\\phi}\\frac{d}{dt}(R^2\\dot{\\theta}\\cos^2\\phi)$\n"
    "• $a_\\phi = \\frac{1}{R}\\frac{d}{dt}(R^2\\dot{\\phi}) + R\\dot{\\theta}^2\\sin\\phi\\cos\\phi$"
)
ax3.text2D(0.03, 0.72, info3, transform=ax3.transAxes, fontsize=8.6,
           bbox=dict(facecolor='white', alpha=0.92, edgecolor='#8e44ad', boxstyle='round,pad=0.35', lw=1.2))

# =============================================================
# [Bottom Row]: (d) Unified 3D Overlay (Left) + Dedicated Transformation Card (Right)
# =============================================================

# (d) Unified 3D Overlay (gs[1, 0:3]) - 100% CLEAN, ZERO OVERLAP
ax4 = fig.add_subplot(gs[1, 0:3], projection='3d')
setup_3d_ax(ax4)
add_bottom_title(ax4, '(d) Unified 3D Overlay Comparison\nVariables & Unit Vectors of All 3 Systems Overlaid at $P(4, 3, 5)$', '#d35400')

# (1) Cartesian bounding box lines
ax4.plot([x_P, x_P], [0, y_P], [0, 0], color='#2980b9', ls=':', lw=1.2)
ax4.plot([0, x_P], [y_P, y_P], [0, 0], color='#2980b9', ls=':', lw=1.2)
ax4.plot([x_P, x_P], [y_P, y_P], [0, z_P], color='#2980b9', ls='--', lw=1.5)

# (2) Cylindrical r and arc
ax4.plot(x_arc, y_arc, np.zeros_like(x_arc), color='#27ae60', lw=1.6)
ax4.plot([0, x_P], [0, y_P], [0, 0], color='#27ae60', lw=2.0)
ax4.text(x_P/2 + 0.1, y_P/2 - 0.35, 0.1, "$r$", fontsize=12, fontweight='bold', color='#27ae60')

# (3) Spherical R vector & phi arc
ax4.plot(x_phi, y_phi, z_phi, color='#8e44ad', lw=2.0)
ax4.quiver(0, 0, 0, x_P, y_P, z_P, color='#8e44ad', lw=2.5, arrow_length_ratio=0.08)
ax4.text(x_P/2 - 0.35, y_P/2 - 0.2, z_P/2 + 0.4, "$R$", fontsize=13, fontweight='bold', color='#8e44ad')

# Azimuth theta & Elevation phi
ax4.plot(r_small * np.cos(th_small), r_small * np.sin(th_small), np.zeros_like(th_small), color='#e67e22', lw=2.0)
ax4.text(2.1 * np.cos(theta_P/2), 2.1 * np.sin(theta_P/2), 0.1, "$\\theta$", fontsize=12, fontweight='bold', color='#e67e22')
ax4.text(x_phi[14] + 0.1, y_phi[14] + 0.1, z_phi[14] + 0.3, "$\\phi$", fontsize=12, fontweight='bold', color='#8e44ad')

# Point P
ax4.scatter([x_P], [y_P], [z_P], color='#e74c3c', s=80, zorder=10)
ax4.text(x_P + 0.2, y_P + 0.2, z_P + 0.2, "$P(4, 3, 5)$", fontsize=13, fontweight='bold', color='#c0392b')

# 4 Key Representative Unit Vectors
ax4.quiver(x_P, y_P, z_P, 0, 0, vec_len, color='#2980b9', lw=2.5, arrow_length_ratio=0.2)
ax4.text(x_P, y_P, z_P + vec_len + 0.1, "$\\mathbf{k}=\\mathbf{e}_z$", fontsize=12, fontweight='bold', color='#2980b9')

ax4.quiver(x_P, y_P, z_P, er_x*vec_len, er_y*vec_len, 0, color='#27ae60', lw=2.5, arrow_length_ratio=0.2)
ax4.text(x_P + er_x*vec_len + 0.1, y_P + er_y*vec_len + 0.1, z_P, "$\\mathbf{e}_r$", fontsize=12, fontweight='bold', color='#27ae60')

ax4.quiver(x_P, y_P, z_P, eR_x*vec_len, eR_y*vec_len, eR_z*vec_len, color='#8e44ad', lw=2.5, arrow_length_ratio=0.2)
ax4.text(x_P + eR_x*vec_len + 0.1, y_P + eR_y*vec_len + 0.1, z_P, "$\\mathbf{e}_R$", fontsize=12, fontweight='bold', color='#8e44ad')

ax4.quiver(x_P, y_P, z_P, ephi_x*vec_len, ephi_y*vec_len, ephi_z*vec_len, color='#16a085', lw=2.5, arrow_length_ratio=0.2)
ax4.text(x_P + ephi_x*vec_len - 0.25, y_P + ephi_y*vec_len, z_P + ephi_z*vec_len + 0.2, "$\\mathbf{e}_\\phi$", fontsize=12, fontweight='bold', color='#16a085')

# (e) Dedicated Transformation Card & Summary (gs[1, 3:6])
ax_card = fig.add_subplot(gs[1, 3:6])
ax_card.axis('off')
ax_card.set_facecolor('#ffffff')

# Card Border
card_bg = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle='round,pad=0.03,rounding_size=0.04',
                                 facecolor='#ffffff', edgecolor='#d35400', lw=1.8, transform=ax_card.transAxes)
ax_card.add_patch(card_bg)

card_title = "★ [Coordinate Transformation Formulas & Summary] ★"
ax_card.text(0.5, 0.93, card_title, transform=ax_card.transAxes, fontsize=14, fontweight='bold',
             ha='center', va='top', color='#d35400')

col1_text = (
    "[1. Cartesian <-> Cylindrical]\n"
    " - $x = r\\cos\\theta, \\quad y = r\\sin\\theta, \\quad z = z$\n"
    " - $r = \\sqrt{x^2 + y^2}, \\quad \\theta = \\arctan(y / x)$\n"
    " - $\\mathbf{e}_r = \\cos\\theta\\,\\mathbf{i} + \\sin\\theta\\,\\mathbf{j}, \\quad \\mathbf{e}_\\theta = -\\sin\\theta\\,\\mathbf{i} + \\cos\\theta\\,\\mathbf{j}$\n\n"
    "[2. Cartesian <-> Spherical (Elevation $\\phi$ Basis)]\n"
    " - $x = R\\cos\\phi\\cos\\theta, \\quad y = R\\cos\\phi\\sin\\theta, \\quad z = R\\sin\\phi$\n"
    " - $R = \\sqrt{x^2 + y^2 + z^2}, \\quad \\phi = \\arctan\\left(\\frac{z}{\\sqrt{x^2+y^2}}\\right)$\n\n"
    "[3. Cylindrical <-> Spherical]\n"
    " - $r = R\\cos\\phi, \\quad z = R\\sin\\phi, \\quad R = \\sqrt{r^2 + z^2}$"
)

ax_card.text(0.06, 0.84, col1_text, transform=ax_card.transAxes, fontsize=10.2,
             ha='left', va='top', color='#2c3e50', linespacing=1.35)

tip_box_text = (
    "* Coordinate Selection Guidelines:\n"
    " - Cartesian: Best for unconstrained linear / 3-axis decoupled motions.\n"
    " - Cylindrical: Best for axis-symmetric, helical, or robotic arm rotations.\n"
    " - Spherical: Best for radial tracking from origin (radars, spacecrafts, ball joints)."
)
ax_card.text(0.06, 0.16, tip_box_text, transform=ax_card.transAxes, fontsize=9.5,
             ha='left', va='center', color='#566573',
             bbox=dict(facecolor='#fef9e7', alpha=0.9, edgecolor='#f39c12', boxstyle='round,pad=0.35', lw=1.0))

out_path = Path(__file__).parent / 'coord_systems_3d_comparison.png'
fig.savefig(str(out_path), facecolor=fig.get_facecolor(), edgecolor='none', dpi=180)
print(f"Saved 3D coordinate systems comparison to: {out_path}")
