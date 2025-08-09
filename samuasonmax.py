import numpy as np
import matplotlib.pyplot as plt

# --- Samuelson model simulation ---
def simulate(alpha, beta, T=80, Y0=0.0, Y1=1.0, G=0.0):
    Y = [Y0, Y1]
    for t in range(2, T):
        Y_next = G + (alpha + beta) * Y[t-1] - beta * Y[t-2]
        Y.append(Y_next)
    return np.array(Y)

T = 80
alpha = 0.99
beta_safe_max_bounce = 0.94   # ρ≈0.97 : sát mép nhưng an toàn dài hạn
beta_safer = 0.885            # ρ≈0.941 : an toàn hơn, bật vẫn lớn

Y_safe = simulate(alpha, beta_safe_max_bounce, T=T, Y0=0.0, Y1=1.0)
Y_safer = simulate(alpha, beta_safer, T=T, Y0=0.0, Y1=1.0)

# --- Plot ---
plt.figure(figsize=(10,6))
plt.plot(Y_safe, label=f"α={alpha}, β={beta_safe_max_bounce} (ρ≈{np.sqrt(beta_safe_max_bounce):.3f})")
plt.plot(Y_safer, label=f"α={alpha}, β={beta_safer} (ρ≈{np.sqrt(beta_safer):.3f})")
plt.axhline(0, linestyle='--', linewidth=1)
plt.title("Đáp ứng sau cú sốc đơn vị – mục tiêu: an toàn dài hạn & bật tối đa")
plt.xlabel("Kỳ (t)")
plt.ylabel("Sai lệch so với cân bằng")
plt.legend()
plt.grid(True)
plt.show()
