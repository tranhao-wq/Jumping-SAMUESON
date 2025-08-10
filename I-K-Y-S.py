import matplotlib.pyplot as plt
import networkx as nx

# Tạo đồ thị
G = nx.DiGraph()

# Các nút
nodes = {
    "Y": "Thu nhập (Y)\nTỷ lệ thay đổi thu nhập",
    "K": "Vốn (K)\nTỷ lệ thay đổi vốn",
    "I": "Đầu tư (I)",
    "S": "Tiết kiệm (S)",
    "alpha": "α\nHệ số phản ứng"
}

# Thêm nút
for k, v in nodes.items():
    G.add_node(k, label=v)

# Các cạnh thể hiện quan hệ
edges = [
    ("Y", "S"),  # Thu nhập ảnh hưởng tiết kiệm
    ("S", "I"),  # Tiết kiệm tạo ra đầu tư
    ("I", "K"),  # Đầu tư làm tăng vốn
    ("K", "Y"),  # Vốn tác động tới thu nhập
    ("alpha", "Y"), # Hệ số phản ứng điều chỉnh Y
    ("alpha", "K")  # Hệ số phản ứng điều chỉnh K
]

G.add_edges_from(edges)

# Vẽ đồ thị
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 7))
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="#cce5ff", edgecolors='black')
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, width=2)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)

plt.title("Sơ đồ vòng phản hồi mô hình Y-K-I-S (Chang & Smyth 1971)", fontsize=14)
plt.axis('off')
plt.show()
