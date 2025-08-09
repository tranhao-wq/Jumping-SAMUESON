import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from caas_jupyter_tools import display_dataframe_to_user

# ----- Model and helpers -----
def simulate(alpha, beta, T=60, Y0=0.0, Y1=1.0, G=0.0):
    Y = [Y0, Y1]
    for t in range(2, T):
        Y_next = G + (alpha + beta) * Y[t-1] - beta * Y[t-2]
        Y.append(Y_next)
    return np.array(Y)

def is_complex_roots(alpha, beta):
    return (alpha + beta)**2 < 4*beta

def stable(beta):
    return beta < 1.0

def overshoot_metric(Y, baseline=0.0):
    # measure peak above baseline after t=1
    return np.max(Y[1:] - baseline)

# ----- Grid search over parameters -----
alphas = np.round(np.arange(0.1, 0.991, 0.005), 3)
betas  = np.round(np.arange(0.1, 0.991, 0.005), 3)

records = []
for a in alphas:
    for b in betas:
        if stable(b) and is_complex_roots(a,b):
            Y = simulate(a, b, T=80, Y0=0.0, Y1=1.0, G=0.0)
            peak = overshoot_metric(Y, baseline=0.0)
            decay = np.sqrt(b)  # spectral radius; closer to 1 = slower decay (riskier)
            period_cos = (a + b) / (2*np.sqrt(b))
            period_cos = np.clip(period_cos, -1, 1)
            theta = np.arccos(period_cos)
            period = 2*np.pi/theta if theta>0 else np.inf
            records.append((a,b,peak,decay,period))

df = pd.DataFrame(records, columns=["alpha","beta","overshoot","radius_sqrt_beta","approx_period"])

# Identify efficient frontier: maximize overshoot and minimize radius (risk)
# Sort by overshoot descending; keep those that aren't dominated in both dimensions
df_sorted = df.sort_values(by="overshoot", ascending=False).reset_index(drop=True)

def pareto_frontier(data):
    frontier = []
    best_radius = 1.0
    for _, row in data.iterrows():
        r = row["radius_sqrt_beta"]
        if r < best_radius - 1e-6:  # strictly smaller radius (safer)
            frontier.append(row)
            best_radius = r
    return pd.DataFrame(frontier)

front = pareto_frontier(df_sorted)

# Choose two operating points:
# 1) "Max bounce but safe" = highest overshoot subject to radius <= 0.98
safe_cap = 0.98
cand1 = df[(df["radius_sqrt_beta"]<=safe_cap)].sort_values(by="overshoot", ascending=False).head(1)
# 2) "Balanced" = point on pareto frontier with mid radius ~0.93-0.95
balanced = front.iloc[(np.abs(front["radius_sqrt_beta"]-0.94)).argsort()[:1]]

# Prepare time series for these choices
choices = pd.concat([cand1, balanced]).drop_duplicates().reset_index(drop=True)

series = {}
for i,row in choices.iterrows():
    a,b = row["alpha"], row["beta"]
    Y = simulate(a,b,T=80, Y0=0.0, Y1=1.0, G=0.0)
    series[f"α={a}, β={b}, ρ≈{row['radius_sqrt_beta']:.3f}, peak≈{row['overshoot']:.2f}"] = Y

# Display the frontier table (top 20 points) to the user
frontier_display = front.head(20).copy()
frontier_display.rename(columns={
    "alpha":"α (MPC)",
    "beta":"β (accelerator)",
    "overshoot":"Đỉnh bật nhảy",
    "radius_sqrt_beta":"Độ rủi ro ρ=√β",
    "approx_period":"Chu kỳ xấp xỉ"
}, inplace=True)
display_dataframe_to_user("Pareto frontier: Điểm tham số tối ưu (top 20)", frontier_display)

# Plot the selected time series
plt.figure(figsize=(10,6))
for label, Y in series.items():
    plt.plot(Y, label=label)
plt.axhline(0, linestyle='--', linewidth=1)
plt.title("Bật nhảy sau cú sốc đơn vị (Y0=0, Y1=1) – mô hình Samuelson")
plt.xlabel("Kỳ (t)")
plt.ylabel("Sai lệch so với cân bằng")
plt.legend()
plt.grid(True)
plt.show()
