import numpy as np
import matplotlib.pyplot as plt

# ---- Kaldor-style 2D system with sign-change (divergence) to create a limit cycle ----
# State variables: Y (income), K (capital)
# Dynamics:
#   dY/dt = α * ( I(Y,K) - S(Y) )
#   dK/dt = I(Y,K) - δ K
#
# Choose nonlinear I(Y,K) (hump-shaped in Y; decreasing in K) and S(Y) increasing in Y.
# This yields local instability near equilibrium and global damping far away -> self-sustained cycle.

# Parameters
alpha = 1.0
delta = 0.35
b = 2.2       # sensitivity of investment to Y
c = 0.18      # saturation (cubic) -> hump shape
e = 0.8       # negative sensitivity to K (capacity constraint)
kappa = 0.5   # desired K proportional to Y
s0 = 0.2
s1 = 0.35     # marginal propensity to save

def S(Y):
    # Saving function (monotone increasing, slightly nonlinear for realism)
    return s0 + s1*Y/(1+0.05*Y**2)

def I(Y, K):
    # Investment: accelerator (bY), saturation (-cY^3), and capacity gap term -e(K - kappa*Y)
    return b*Y - c*Y**3 - e*(K - kappa*Y)

def f(Y, K):
    return alpha * (I(Y, K) - S(Y))

def g(Y, K):
    return I(Y, K) - delta*K

def divergence(Y, K):
    # div = ∂f/∂Y + ∂g/∂K
    I_Y = b - 3*c*Y**2 + e*kappa
    S_Y = (s1*(1+0.05*Y**2) - s1*Y*(0.1*Y))/(1+0.05*Y**2)**2  # derivative of S(Y)
    I_K = -e
    return alpha*(I_Y - S_Y) + (I_K - delta)

# ---- Simulate trajectory (RK4) ----
def rk4_step(Y, K, h):
    k1Y = f(Y, K);           k1K = g(Y, K)
    k2Y = f(Y + 0.5*h*k1Y, K + 0.5*h*k1K);   k2K = g(Y + 0.5*h*k1Y, K + 0.5*h*k1K)
    k3Y = f(Y + 0.5*h*k2Y, K + 0.5*h*k2K);   k3K = g(Y + 0.5*h*k2Y, K + 0.5*h*k2K)
    k4Y = f(Y + h*k3Y, K + h*k3K);           k4K = g(Y + h*k3Y, K + h*k3K)
    Y_new = Y + (h/6.0)*(k1Y + 2*k2Y + 2*k3Y + k4Y)
    K_new = K + (h/6.0)*(k1K + 2*k2K + 2*k3K + k4K)
    return Y_new, K_new

T = 1200
h = 0.02
steps = int(T/h)
Yt = np.zeros(steps); Kt = np.zeros(steps)
Yt[0], Kt[0] = 0.2, 0.1   # initial condition

for t in range(steps-1):
    Yt[t+1], Kt[t+1] = rk4_step(Yt[t], Kt[t], h)

# ---- Phase portrait ----
Y_grid = np.linspace(-1.0, 4.0, 40)
K_grid = np.linspace(-0.5, 3.5, 40)
Yg, Kg = np.meshgrid(Y_grid, K_grid)
FY = f(Yg, Kg)
GK = g(Yg, Kg)

plt.figure(figsize=(9, 7))
# Vector field
plt.streamplot(Y_grid, K_grid, FY.T, GK.T, density=1.1, linewidth=1)

# Nullclines f=0 and g=0
cs1 = plt.contour(Yg, Kg, FY, levels=[0], linewidths=2)
cs2 = plt.contour(Yg, Kg, GK, levels=[0], linewidths=2, linestyles='--')

# Trajectory
plt.plot(Yt[::20], Kt[::20], lw=1.5)

# Divergence zero contour (where sign can flip)
div = divergence(Yg, Kg)
plt.contour(Yg, Kg, div, levels=[0], linewidths=1.5)

plt.xlabel('Y (Thu nhập)')
plt.ylabel('K (Vốn)')
plt.title('Pha đồ hệ Kaldor 2 biến: chu kỳ tự duy trì qua đổi dấu phân kỳ (divergence)')
plt.xlim(Y_grid.min(), Y_grid.max())
plt.ylim(K_grid.min(), K_grid.max())
plt.grid(True, alpha=0.3)
plt.show()

# ---- Time series plot ----
plt.figure(figsize=(10, 4))
t = np.arange(steps)*h
plt.plot(t, Yt, label='Y(t)')
plt.plot(t, Kt, label='K(t)')
plt.xlabel('Thời gian')
plt.ylabel('Mức độ')
plt.title('Quỹ đạo thời gian: dao động tự duy trì (limit cycle)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
