import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig, ax = plt.subplots()

t = np.linspace(0, 15, 300)
t_span = (0, 15)

b = 1.0      # air resistance
m = 1.0      # mass
g = 10.0     # gravity
h = 50.0     # height
v_x0 = 30.0  # first horizontal speed
x0 = 0       # starting position on x-axis
v_y0 = 0     # first vertical speed
y0 = h       # starting position on y-axis

point_1, = ax.plot([], [], 'ro', markersize=10)
point_2, = ax.plot([], [], 'bo', markersize=10)

# ma_x + bv_x = 0
def projectile_x(t, a1, b = b, m = m):
    x, v_x= a1
    dxdt = v_x
    dv_xdt = -b * v_x / m
    return [dxdt, dv_xdt]

a10 = [x0, v_x0]
sol_x = solve_ivp(lambda t, a1: projectile_x(t, a1, b, m), t_span, a10, t_eval=t)

# ma_y + bv_y = mg
def projectile_y(t, a2, b = b, m = m, g = g):
    y, v_y= a2
    dydt = v_y
    dv_ydt = - g - b * v_y / m
    return [dydt, dv_ydt]

a20 = [y0, v_y0]
sol_y = solve_ivp(lambda t, a2: projectile_y(t, a2, b, m, g), t_span, a20, t_eval=t)

x = sol_x.y[0]
y = sol_y.y[0]

ax.set_xlim(0, 110)
ax.set_ylim(0, 55)

# and here is the "friction-free" movement for comparison:
x1 = x0 + v_x0 * t
y1 = h + v_y0 * t - 0.5 * g * t**2

def update(i):
    point_1.set_data([x1[i]], [y1[i]])
    point_2.set_data([x[i]], [y[i]])
    return point_1, point_2

# corrections:
w = np.where(y >= 0)[0]
max_frame = w[-1] if len(w) > 0 else len(t)

# we say "frames=len(t)" instead of "frames=t", so that the number i increases from 0 to 199.
anim = FuncAnimation(fig, update, frames=max_frame, interval=20, blit=True, repeat=True)

# display:
ax.set_xlabel("X-axis (Range)")
ax.set_ylabel("Y-axis (Altitude)")
plt.title("Frictionless vs. Frictional Environment", fontsize=14, fontweight='bold')
plt.plot(x1, y1, 'r--', alpha=0.5, label="frictionless trajectory")
plt.plot(x, y, 'b--', alpha=0.5, label="frictional trajectory")
plt.grid(True)
plt.legend()
plt.show()