2D Projectile Motion Simulator with Aerodynamic Drag

![Drag_motion](https://github.com/user-attachments/assets/f3fc0655-3495-44c3-91fa-07a65643b317)

(GIF above is slightly cropped, I highly recommend running the code)

Overview:
This project simulates and visualizes the 2D projectile motion of an object, directly comparing a frictionless environment with a realistic environment affected by air resistance (aerodynamic drag).
Instead of relying on basic kinematic equations, the frictional trajectory is computed numerically by solving the underlying system of Ordinary Differential Equations (ODEs) derived from Newton's Second Law.

Libraries Used:
PythonSciPy (solve_ivp): Used for the numerical integration of the differential equations.
NumPy: Used for array manipulations and linear space generation.
Matplotlib: Used for data visualization and rendering the 2D animation of the trajectories.
