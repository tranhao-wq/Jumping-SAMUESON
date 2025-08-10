import numpy as np
import matplotlib.pyplot as plt

# Trục Y (thu nhập)
Y = np.linspace(0, 10, 600)

# Hàm tiết kiệm S(Y) (dạng S cong - phi tuyến)
S = 0.2 + 0.8 / (1 + np.exp(-(Y - 5) / 1.1))

# Hàm đầu tư I(Y) (dạng cong có thể cắt S nhiều lần)
I = 0.95 * (Y / 10) + 0.32 * np.sin(1.2 * (Y - 1.8)) + 0.25

# Tìm điểm giao F(Y)=I-S=0
F = I - S
sign_change_idx = np.where(np.sign(F[:-1]) * np.sign(F[1:]) < 0)[0]

roots = []
for idx in sign_change_idx:
    y0, y1 = Y[idx], Y[idx+1]
    f0, f1 = F[idx], F[idx+1]
    # nội suy tuyến tính để ước lượng nghiệm
    y_star = y0 - f0 * (y1 - y0) / (f1 - f0)
    roots.append(y_star)

# Phân loại ổn định: F'(Y*) < 0 => ổn định
dF_dY = np.gradient(F, Y)
stability = []
for y_star in roots:
    i = np.argmin(np.abs(Y - y_star))
    stability.append('stable' if dF_dY[i] < 0 else 'unstable')

# Vẽ đồ thị
plt.figure(figsize=(10, 6))
plt.plot(Y, I, label='I(Y) – Đầu tư')
plt.plot(Y, S, label='S(Y) – Tiết kiệm')

# Đánh dấu điểm cân bằng
for y_star, st in zip(roots, stability):
    x = y_star
    y = np.interp(x, Y, I)  # I(x) == S(x)
    if st == 'stable':
        plt.plot(x, y, marker='o', markersize=8, label='_nolegend_')
        plt.annotate('Cân bằng ổn định', (x, y),
                     xytext=(x+0.2, y+0.15), arrowprops=dict(arrowstyle='->'))
    else:
        plt.plot(x, y, marker='x', markersize=8, label='_nolegend_')
        plt.annotate('Cân bằng không ổn định', (x, y),
                     xytext=(x+0.2, y-0.25), arrowprops=dict(arrowstyle='->'))

# Vẽ mũi tên động học dY/dt = I - S
segments = np.linspace(0, 10, 9)
midpoints = (segments[:-1] + segments[1:]) / 2
for m in midpoints:
    sign = np.sign(np.interp(m, Y, F))
    if sign > 0:
        txt = '↑ dY/dt>0'
        dy = 0.07
    else:
        txt = '↓ dY/dt<0'
        dy = -0.07
    plt.annotate(txt, (m, 0.02), xytext=(m, 0.02 + dy),
                 arrowprops=dict(arrowstyle='->'), ha='center', va='bottom', fontsize=9)

plt.xlabel('Y – Thu nhập')
plt.ylabel('I(Y), S(Y)')
plt.title('Đồ thị Kaldor phi tuyến với động học dY/dt = I(Y) - S(Y)\n(điểm tròn: ổn định, dấu x: không ổn định)')
plt.legend()
plt.ylim(0, 1.6)
plt.xlim(0, 10)
plt.grid(True, alpha=0.3)
plt.show()
