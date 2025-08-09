import matplotlib.pyplot as plt

# Dữ liệu cho 2 chế độ chính sách
policies = [
    "Giảm ưu đãi đầu tư",
    "Siết tín dụng ngành nóng",
    "Tăng chi đầu tư công",
    "Ưu đãi tín dụng mục tiêu"
]

modes = ["Hãm phanh", "Hãm phanh", "Đạp ga", "Đạp ga"]
colors = ["#e74c3c", "#e74c3c", "#27ae60", "#27ae60"]  # đỏ = hãm, xanh = đạp

# Tạo hình
fig, ax = plt.subplots(figsize=(8, 4))

# Vẽ các thanh chính sách
for i, (policy, mode, color) in enumerate(zip(policies, modes, colors)):
    ax.barh(i, 1, color=color)
    ax.text(0.02, i, f"{policy} ({mode})", va='center', ha='left', color="white", fontsize=11, fontweight='bold')

# Tùy chỉnh trục
ax.set_xlim(0, 1)
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("Hai chế độ chính sách: Hãm phanh vs. Đạp ga", fontsize=14, fontweight='bold')
ax.set_frame_on(False)

plt.tight_layout()
plt.show()
