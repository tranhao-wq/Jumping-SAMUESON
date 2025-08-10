import matplotlib.pyplot as plt
import numpy as np

# Tạo dữ liệu mô phỏng chu kỳ Goodwin đơn giản cho trực quan
t = np.linspace(0, 2*np.pi, 200)
x = np.cos(t)  # việc làm
y = np.sin(t)  # tỷ lệ tiền lương

fig, ax = plt.subplots(figsize=(6,6))

# Vẽ quỹ đạo x-y
ax.plot(x, y, label='Quỹ đạo việc làm - tiền lương')
ax.set_xlabel('Tỷ lệ việc làm (x)')
ax.set_ylabel('Tỷ lệ tiền lương (y)')
ax.axhline(0, color='gray', linewidth=0.8)
ax.axvline(0, color='gray', linewidth=0.8)

# Các mũi tên minh họa chu kỳ
for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
    ax.arrow(np.cos(angle), np.sin(angle),
             -0.1*np.sin(angle), 0.1*np.cos(angle),
             head_width=0.05, head_length=0.05, fc='red', ec='red')

# Thêm chú thích các pha
ax.text(0.8, 0.2, "x cao → y tăng\n→ lợi nhuận giảm\n→ đầu tư giảm\n→ x giảm", fontsize=8, color='blue')
ax.text(-0.95, -0.1, "x thấp → y giảm\n→ lợi nhuận tăng\n→ đầu tư tăng\n→ x tăng", fontsize=8, color='green')

ax.set_title("Chu kỳ Goodwin – trực quan hóa quan hệ x & y")
ax.legend()
plt.show()
