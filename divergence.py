import matplotlib.pyplot as plt
import numpy as np

# Tạo lưới tọa độ
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)

# Hai trường vector: divergence dương (nguồn) và âm (hố)
U_source = X
V_source = Y

U_sink = -X
V_sink = -Y

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Vẽ nguồn (divergence dương)
axes[0].quiver(X, Y, U_source, V_source, color='tab:red')
axes[0].set_title("Divergence Dương (Nguồn phát)", fontsize=14)
axes[0].set_aspect('equal')
axes[0].set_xticks([])
axes[0].set_yticks([])
axes[0].text(0, 2.3, "Ví dụ: Vòi phun nước, tin đồn lan rộng", ha='center', fontsize=10, color='tab:red')

# Vẽ hố (divergence âm)
axes[1].quiver(X, Y, U_sink, V_sink, color='tab:blue')
axes[1].set_title("Divergence Âm (Hố hút)", fontsize=14)
axes[1].set_aspect('equal')
axes[1].set_xticks([])
axes[1].set_yticks([])
axes[1].text(0, 2.3, "Ví dụ: Nước rút vào cống, hút chân không", ha='center', fontsize=10, color='tab:blue')

plt.tight_layout()
plt.show()
