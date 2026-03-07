import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

m = 1.0        # mass of the two identical balls
g = 9.81       # gravity
l = 1.0        # length of the ropes

t = np.linspace(0, 20, 300)
t_span = (0, 20)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

ball_1, = ax.plot([], [], 'ro', markersize=15)
ball_2, = ax.plot([], [], 'bo', markersize=15)
rope_1, = ax.plot([], [], 'orange', lw=3)
rope_2, = ax.plot([], [], 'c-', lw=3)

# Equations of Motion (ODE) for Double Pendulum derived from Euler-Lagrange equations
def Double_Pendulum(t, a, m = m, g = g, l = l):
  theta_1, w_1, theta_2, w_2= a
  dtheta_1dt = w_1
  dtheta_2dt = w_2
  dw_2dt = (- g*np.sin(theta_2)/l + w_1**2*np.sin(theta_1 - theta_2) + w_2**2*np.sin(theta_1 - theta_2)*np.cos(theta_1 - theta_2)/2 + g*np.sin(theta_1)*np.cos(theta_1 - theta_2)/l) / (1 - (np.cos(theta_1 - theta_2))**2/2)
  dw_1dt = (- g*np.sin(theta_1)/l - w_2**2*np.sin(theta_1 - theta_2)/2 - w_1**2*np.sin(theta_1 - theta_2)*np.cos(theta_1 - theta_2)/2 + g*np.sin(theta_2)*np.cos(theta_1 - theta_2)/(2*l)) / (1 - (np.cos(theta_1 - theta_2))**2 / 2)

  return [dtheta_1dt, dw_1dt, dtheta_2dt, dw_2dt]

def calculate(th1, th2):
  global x_tip_1, y_tip_1, x_tip_2, y_tip_2
  a0 = [th1, 0, th2, 0]
  sol = solve_ivp(lambda t, a: Double_Pendulum(t, a, m, g, l), t_span, a0, t_eval=t)
  theta_1 = sol.y[0]
  theta_2 = sol.y[2]

  x_tip_1 = l * np.sin(theta_1)
  y_tip_1 = - l * np.cos(theta_1)
  x_tip_2 = l * np.sin(theta_1) + l * np.sin(theta_2)
  y_tip_2 = - l * np.cos(theta_1) - l * np.cos(theta_2)

calculate(2*np.pi/3, -np.pi/2)

def update(i):
  rope_1.set_data([0, x_tip_1[i]], [0, y_tip_1[i]]) 
  rope_2.set_data([x_tip_1[i], x_tip_2[i]], [y_tip_1[i], y_tip_2[i]])
  ball_1.set_data([x_tip_1[i]], [y_tip_1[i]])
  ball_2.set_data([x_tip_2[i]], [y_tip_2[i]])

  return rope_1, rope_2, ball_1, ball_2

anim = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True)

# Axes of Sliders
ax_th1 = plt.axes([0.20, 0.15, 0.60, 0.03])
ax_th2 = plt.axes([0.20, 0.10, 0.60, 0.03])
ax_button = plt.axes([0.4, 0.02, 0.2, 0.05])

# valfmt='%0.0f' is to make it integer
slider_th1 = Slider(ax_th1, 'Theta 1 (°)', -180, 180, valinit=120, valstep=5, valfmt='%0.0f', color='red')
slider_th2 = Slider(ax_th2, 'Theta 2 (°)', -180, 180, valinit=-90, valstep=5, valfmt='%0.0f', color='blue')
btn_reset = Button(ax_button, 'Reset')

# degrees to radians
def reset_anim(event):
    calculate(np.radians(slider_th1.val), np.radians(slider_th2.val))
    
btn_reset.on_clicked(reset_anim)

ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-2.5, 2.0) 
ax.set_aspect('equal') 
ax.grid(True)
fig.suptitle("Double Pendulum", y=0.95, fontsize=16, fontweight='bold')
plt.show()

