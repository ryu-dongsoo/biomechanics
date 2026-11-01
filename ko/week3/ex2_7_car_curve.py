import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from matplotlib.animation import FuncAnimation, PillowWriter

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

vA = 100 / 3.6
vC = 50 / 3.6
s_total = 120
at = (vC**2 - vA**2) / (2 * s_total)
rho_A = 432
rho_C = 150

# A 이전 지점부터 렌더링하기 위해 t_start 계산 (s = -30)
# s = vA*t + 0.5*at*t^2 => 0.5*at*t^2 + vA*t - s = 0 
a_quad = 0.5 * at
b_quad = vA
c_quad = 30
t_start = (-b_quad + np.sqrt(b_quad**2 - 4*a_quad*c_quad)) / (2*a_quad)
t_end = (vC - vA) / at
frames = 200
t = np.linspace(t_start, t_end + 0.5, frames)
s = vA * t + 0.5 * at * t**2
v = vA + at * t

s_road = np.linspace(-40, 140, 600)
poly_kappa = np.polyfit([0, 60, 120], [1/rho_A, 0, -1/rho_C], 2)
kappa_road = np.polyval(poly_kappa, s_road)

ds = s_road[1] - s_road[0]
theta_raw = np.cumsum(kappa_road) * ds
idx_A = np.argmin(np.abs(s_road))
theta_road = theta_raw - theta_raw[idx_A] + 0.0435
x_road = np.cumsum(np.cos(theta_road)) * ds
y_road = np.cumsum(np.sin(theta_road)) * ds
x_road -= x_road[idx_A]
y_road -= y_road[idx_A]

x_c = np.interp(s, s_road, x_road)
y_c = np.interp(s, s_road, y_road)
theta_c = np.interp(s, s_road, theta_road)
kappa_c = np.interp(s, s_road, kappa_road)

an_signed = kappa_c * v**2
an_mag = np.abs(an_signed)
a_tot_mag = np.sqrt(at**2 + an_mag**2)

fig = plt.figure(figsize=(12, 8))
fig.suptitle('예제 2.7: 요철 도로 감속 주행 시뮬레이션', fontsize=16, fontweight='bold')
gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1])

ax_mech = fig.add_subplot(gs[0, :])
ax_mech.set_aspect('equal')
ax_mech.axis('off')

# 그림 원본과 동일한 그라데이션 및 지면 효과
for i in range(20):
    ax_mech.fill_between(x_road, y_road - i*0.5, y_road - (i+1)*0.5, color='#4a3b32', alpha=0.4 * (1 - i/20), zorder=1)
ax_mech.plot(x_road, y_road, color='black', lw=1.5, zorder=2)

ax_mech.set_xlim(np.min(x_road) - 5, np.max(x_road) + 5)
ax_mech.set_ylim(-30, 25)

# A, B, C 마커 및 라벨 (원본 동일)
for sm, lbl in zip([0, 60, 120], ['A', 'B', 'C']):
    xm = np.interp(sm, s_road, x_road)
    ym = np.interp(sm, s_road, y_road)
    th = np.interp(sm, s_road, theta_road)
    dx = np.sin(th) * 3
    dy = np.cos(th) * 3
    ax_mech.plot([xm - dx, xm + dx], [ym + dy, ym - dy], 'k-', lw=1.2, zorder=3)
    ax_mech.text(xm - dx*1.5, ym - dy*1.5 - 1.5, lbl, fontsize=18, fontfamily='serif', fontstyle='italic', ha='center', va='top')

# 60m 텍스트
for s_mid in [30, 90]:
    xm = np.interp(s_mid, s_road, x_road)
    ym = np.interp(s_mid, s_road, y_road)
    ax_mech.text(xm, ym + 3, "60 m", fontsize=16, fontfamily='serif', ha='center', va='bottom', color='#004488')

# C 지점의 곡률반경 표시 (150 m)
xC = np.interp(120, s_road, x_road)
yC = np.interp(120, s_road, y_road)
ax_mech.annotate('', xy=(xC, yC - 18), xytext=(xC, yC), arrowprops=dict(arrowstyle='<-', color='black', lw=1.2))
ax_mech.plot(xC, yC - 18, 'kx', markersize=8)
ax_mech.text(xC + 2, yC - 9, "150 m", fontsize=16, fontfamily='serif', ha='left', va='center')

# 자동차 객체 (그림의 스포츠카 형태 재현)
car_verts = np.array([
    [-2.5, 0.3], [ 2.5, 0.3], [ 2.8, 0.6], [ 1.5, 1.2], 
    [ 0.5, 1.6], [-1.0, 1.7], [-2.0, 1.2], [-2.8, 0.8]
])
car_poly = patches.Polygon(car_verts, facecolor='#e74c3c', edgecolor='black', zorder=4)
ax_mech.add_patch(car_poly)
wheel1 = patches.Circle((-1.5, 0.3), radius=0.5, facecolor='#2c3e50', zorder=5)
wheel2 = patches.Circle(( 1.5, 0.3), radius=0.5, facecolor='#2c3e50', zorder=5)
ax_mech.add_patch(wheel1)
ax_mech.add_patch(wheel2)

info_text = fig.text(0.05, 0.85, '', fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

ax_vel = fig.add_subplot(gs[1, 0])
ax_vel.plot(t, v * 3.6, color='#27ae60', lw=2, label='속력 $v$')
ax_vel.set_xlim(t[0], t[-1])
ax_vel.set_ylim(40, 110)
ax_vel.set_xlabel('시간 $t$ (s)')
ax_vel.set_ylabel('속력 (km/h)')
ax_vel.grid(True, ls='--')
ax_vel.legend(loc='best')
time_line_v, = ax_vel.plot([0, 0], ax_vel.get_ylim(), 'k--', lw=1)
point_v, = ax_vel.plot([], [], 'o', color='#27ae60')

ax_acc = fig.add_subplot(gs[1, 1])
ax_acc.plot(s, np.full_like(s, at), color='#3498db', lw=2, label='$a_t$ (접선)')
ax_acc.plot(s, an_mag, color='#9b59b6', lw=2, label='$a_n$ (법선)')
ax_acc.plot(s, a_tot_mag, color='#c0392b', lw=2, label='$|a|$ (총가속도)')
ax_acc.set_xlim(-30, 130)
ax_acc.set_ylim(-3.5, 4.5)
ax_acc.set_xlabel('이동 거리 $s$ (m)')
ax_acc.set_ylabel('가속도 (m/s²)')
ax_acc.grid(True, ls='--')
ax_acc.legend(loc='best')
for sm, lbl in zip([0, 60, 120], ['A', 'B', 'C']):
    ax_acc.axvline(sm, color='gray', ls=':', lw=1)
    ax_acc.text(sm, 4.0, lbl, ha='center', va='bottom', fontweight='bold', fontfamily='serif')

dist_line_a, = ax_acc.plot([0, 0], ax_acc.get_ylim(), 'k--', lw=1)
point_at, = ax_acc.plot([], [], 'o', color='#3498db')
point_an, = ax_acc.plot([], [], 'o', color='#9b59b6')
point_atot, = ax_acc.plot([], [], 'o', color='#c0392b')

plt.tight_layout()

q_v = None
q_at = None
q_an = None
q_a = None

def animate(i):
    global q_v, q_at, q_an, q_a
    trans = Affine2D().rotate(theta_c[i]).translate(x_c[i], y_c[i]) + ax_mech.transData
    car_poly.set_transform(trans)
    wheel1.set_transform(trans)
    wheel2.set_transform(trans)
    
    if q_v: q_v.remove()
    if q_at: q_at.remove()
    if q_an: q_an.remove()
    if q_a: q_a.remove()
    
    et_x, et_y = np.cos(theta_c[i]), np.sin(theta_c[i])
    en_x, en_y = -np.sin(theta_c[i]), np.cos(theta_c[i])
    
    # 원본 이미지의 초록색 속도 화살표 스타일 재현 (진행방향 앞쪽에 배치)
    v_scale = 0.3
    q_v = ax_mech.quiver(x_c[i] + et_x*3, y_c[i] + et_y*3, et_x * v[i] * v_scale, et_y * v[i] * v_scale, 
                         color='#1abc9c', angles='xy', scale_units='xy', scale=1, width=0.005, headwidth=5, zorder=6)
    
    a_scale = 3.0
    q_at = ax_mech.quiver(x_c[i], y_c[i], et_x * at * a_scale, et_y * at * a_scale, 
                          color='#3498db', angles='xy', scale_units='xy', scale=1, width=0.003, zorder=5, alpha=0.8)
    q_an = ax_mech.quiver(x_c[i], y_c[i], en_x * an_signed[i] * a_scale, en_y * an_signed[i] * a_scale, 
                          color='#9b59b6', angles='xy', scale_units='xy', scale=1, width=0.003, zorder=5, alpha=0.8)
    ax_tot = et_x * at + en_x * an_signed[i]
    ay_tot = et_y * at + en_y * an_signed[i]
    q_a = ax_mech.quiver(x_c[i], y_c[i], ax_tot * a_scale, ay_tot * a_scale, 
                         color='#c0392b', angles='xy', scale_units='xy', scale=1, width=0.004, zorder=6)
    
    info_str = (
        f"시간 $t = {t[i]:.2f}$ s\n"
        f"거리 $s = {s[i]:.1f}$ m\n"
        f"속력 $v = {v[i]*3.6:.1f}$ km/h\n"
        f"$a_t = {at:.2f}$ m/s²\n"
        f"$a_n = {an_mag[i]:.2f}$ m/s²\n"
        f"총가속도 $|a| = {a_tot_mag[i]:.2f}$ m/s²"
    )
    info_text.set_text(info_str)
    
    time_line_v.set_data([t[i], t[i]], ax_vel.get_ylim())
    point_v.set_data([t[i]], [v[i]*3.6])
    dist_line_a.set_data([s[i], s[i]], ax_acc.get_ylim())
    point_at.set_data([s[i]], [at])
    point_an.set_data([s[i]], [an_mag[i]])
    point_atot.set_data([s[i]], [a_tot_mag[i]])
    
    return car_poly, wheel1, wheel2, time_line_v, point_v, dist_line_a, point_at, point_an, point_atot

ani = FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)

writer = PillowWriter(fps=25)
writer._kwargs = {'loop': None}
gif_path = 'ex2_7_car_curve.gif'
ani.save(gif_path, writer=writer)
print(f"GIF 애니메이션이 {gif_path}에 저장되었습니다.")

try:
    from PIL import Image
    im = Image.open(gif_path)
    frames_img = []
    durations = []
    try:
        while True:
            frames_img.append(im.copy())
            durations.append(im.info.get('duration', 40))
            im.seek(len(frames_img))
    except EOFError:
        pass
    durations[-1] = 60000
    frames_img[0].save(gif_path, save_all=True, append_images=frames_img[1:], duration=durations, loop=1)
except Exception as e:
    pass
