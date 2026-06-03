import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import itertools

# MULTI‑ARM DATA (Arm1 & Arm2 from Area 1)


# Arm1 – 10 trials per target, targets in order:
# (-4,2), (-8,3), (-3,3), (-7,7), (-2,4), (-3,8)
arm1_actual = [
    (-3.55, 1.85), (-3.42, 1.98), (-3.78, 2.02), (-3.68, 2.25), (-3.91, 1.56),
    (-3.61, 1.98), (-3.47, 2.17), (-3.83, 1.80), (-4.23, 1.38), (-4.19, 1.62),
    (-8.08, 2.67), (-8.17, 2.63), (-8.03, 2.90), (-7.70, 3.05), (-7.97, 2.85),
    (-7.85, 3.08), (-8.05, 2.77), (-7.80, 3.09), (-8.12, 2.89), (-8.14, 2.76),
    (-3.20, 3.05), (-3.04, 2.85), (-3.08, 3.05), (-2.85, 3.05), (-2.76, 3.10),
    (-2.87, 3.20), (-3.04, 3.19), (-3.26, 2.76), (-3.22, 2.85), (-3.14, 2.93),
    (-6.88, 6.90), (-6.61, 7.04), (-7.41, 6.58), (-6.98, 6.84), (-6.21, 7.19),
    (-6.65, 7.14), (-6.51, 7.08), (-7.54, 6.68), (-7.31, 6.67), (-6.32, 7.03),
    (-1.74, 4.00), (-1.84, 3.88), (-2.18, 4.07), (-1.89, 3.95), (-2.24, 3.68),
    (-1.98, 3.84), (-2.31, 3.77), (-1.83, 4.03), (-2.13, 3.96), (-1.68, 4.08),
    (-2.54, 8.19), (-2.75, 7.96), (-3.06, 7.89), (-2.57, 7.98), (-3.56, 7.81),
    (-2.92, 7.95), (-3.29, 7.78), (-2.84, 8.05), (-3.35, 7.89), (-2.58, 8.15)
]
arm1_targets = [(-4,2), (-8,3), (-3,3), (-7,7), (-2,4), (-3,8)]

# Arm2 – 10 trials per target, same target order
arm2_actual = [
    (-3.29, 2.11), (-3.55, 2.28), (-3.64, 2.38), (-3.82, 2.27), (-3.90, 1.84),
    (-3.71, 2.14), (-3.47, 2.17), (-3.82, 2.05), (-4.04, 1.82), (-4.16, 1.93),
    (-8.06, 2.99), (-8.04, 2.94), (-7.74, 3.14), (-7.72, 3.07), (-7.70, 3.30),
    (-7.86, 3.10), (-7.85, 3.06), (-7.70, 3.40), (-7.92, 3.08), (-7.90, 3.04),
    (-3.09, 2.63), (-2.93, 2.75), (-2.70, 2.85), (-3.41, 2.87), (-2.87, 2.90),
    (-2.67, 3.00), (-3.16, 2.75), (-2.59, 3.12), (-2.64, 3.27), (-2.85, 3.37),
    (-7.14, 6.78), (-7.18, 6.64), (-7.10, 7.13), (-7.53, 6.80), (-6.80, 7.00),
    (-6.82, 7.14), (-7.41, 6.76), (-6.47, 7.17), (-6.28, 7.29), (-7.27, 6.86),
    (-1.98, 4.13), (-2.26, 3.92), (-1.63, 4.01), (-2.21, 3.88), (-1.71, 4.25),
    (-2.10, 3.78), (-2.09, 3.87), (-1.69, 3.88), (-1.47, 4.19), (-2.18, 3.80),
    (-2.42, 8.14), (-3.34, 7.98), (-2.75, 8.16), (-3.38, 8.02), (-3.17, 8.00),
    (-3.29, 8.09), (-3.51, 7.92), (-2.98, 8.18), (-2.67, 8.07), (-3.57, 8.02)
]
arm2_targets = arm1_targets  # same targets

# Convert to (tx, ty, ax, ay) format
def build_data(targets, actuals):
    data = []
    for i, (tx, ty) in enumerate(targets):
        for j in range(10):
            ax, ay = actuals[i*10 + j]
            data.append((tx, ty, ax, ay))
    return data

arm1_data = build_data(arm1_targets, arm1_actual)
arm2_data = build_data(arm2_targets, arm2_actual)

# Start points
start_points = {
    'Arm1': (-1, 0),
    'Arm2': (0, 1)
}

# UTILITY FUNCTIONS (convex hull area, grouping, analysis)
def compute_cluster_area(points):
    """Convex hull area of a set of points. Returns 0 if <3 points."""
    pts = np.array(points)
    if len(pts) < 3:
        return 0.0
    try:
        hull = ConvexHull(pts)
        return hull.volume   # area in 2D
    except:
        return 0.0

def group_by_target(data):
    groups = {}
    for tx, ty, ax, ay in data:
        groups.setdefault((tx, ty), []).append((ax, ay))
    return groups

def analyze_arm(arm_name, arm_data, start):
    groups = group_by_target(arm_data)
    distances = []
    areas = []
    target_info = []
    for target, actual_points in groups.items():
        d = np.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
        area = compute_cluster_area(actual_points)
        distances.append(d)
        areas.append(area)
        target_info.append((target, d, area))
    return np.array(distances), np.array(areas), target_info

# ANALYSE BOTH ARMS
arm_details = {}
for arm_name in ['Arm1', 'Arm2']:
    data = arm1_data if arm_name == 'Arm1' else arm2_data
    dist, area, info = analyze_arm(arm_name, data, start_points[arm_name])
    arm_details[arm_name] = (dist, area, info)

# PLOTTING: one combined plot for clarity
plt.figure(figsize=(8, 6))
colors = {'Arm1': 'blue', 'Arm2': 'orange'}
markers = {'Arm1': 'o', 'Arm2': '^'}

for arm_name in ['Arm1', 'Arm2']:
    dist, area, info = arm_details[arm_name]
    plt.scatter(dist, area, c=colors[arm_name], marker=markers[arm_name],
                s=80, edgecolors='k', alpha=0.8, label=arm_name)

    # Add labels
    for (tx, ty), d, a in info:
        plt.annotate(f"({tx},{ty})", (d, a), textcoords="offset points",
                     xytext=(5,5), fontsize=8, color=colors[arm_name], alpha=0.9)

    # Linear fit
    if len(dist) > 1:
        coeffs = np.polyfit(dist, area, 1)
        x_line = np.linspace(dist.min(), dist.max(), 50)
        y_line = np.polyval(coeffs, x_line)
        corr = np.corrcoef(dist, area)[0, 1]
        plt.plot(x_line, y_line, '--', color=colors[arm_name], linewidth=2,
                 label=f'{arm_name} fit: slope={coeffs[0]:.3f}, R²={corr**2:.3f}')

plt.xlabel('Distance from start point to target (units)')
plt.ylabel('Convex hull area of cluster (units²)')
plt.title('Multi‑arm: Cluster spread vs target distance (Area 1)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# PRINT DETAILED TABLE
print("\n" + "="*60)
print("MULTI‑ARM CLUSTER AREAS (CONVEX HULL)")
print("="*60)
for arm_name in ['Arm1', 'Arm2']:
    dist, area, info = arm_details[arm_name]
    print(f"\n--- {arm_name} (start {start_points[arm_name]}) ---")
    print(f"{'Target':>12}  {'Distance':>9}  {'Area (units²)':>14}")
    print("-"*40)
    sorted_info = sorted(info, key=lambda x: x[1])
    for (tx, ty), d, a in sorted_info:
        print(f"({tx:5.1f}, {ty:5.1f})  {d:9.3f}  {a:14.4f}")

print("\n" + "="*60)
print("LINEAR FIT SUMMARY")
print("="*60)
for arm_name in ['Arm1', 'Arm2']:
    dist, area, _ = arm_details[arm_name]
    if len(dist) > 1:
        slope, intercept = np.polyfit(dist, area, 1)
        corr = np.corrcoef(dist, area)[0, 1]
        print(f"{arm_name}: slope={slope:.4f}, intercept={intercept:.4f}, R²={corr**2:.3f}")