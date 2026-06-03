import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

# MULTI‑ARM DATA (Area 2: Arm2 & Arm3)

# Arm2 actual points, 10 trials per target, targets in order:
# (2,4), (3,8), (3,3), (7,7), (4,2), (8,3)
arm2_actual = [
    (2.49, 3.92), (2.02, 3.75), (1.82, 3.89), (2.25, 3.79), (1.88, 4.14),
    (2.19, 4.07), (1.66, 4.08), (1.69, 3.89), (2.15, 3.96), (2.33, 4.08),
    (2.52, 8.15), (3.06, 7.91), (2.90, 7.92), (2.32, 8.33), (3.42, 8.07),
    (3.55, 7.87), (2.32, 7.95), (3.31, 7.86), (2.72, 7.95), (3.25, 8.15),
    (2.68, 3.02), (3.35, 2.76), (3.01, 2.87), (2.56, 3.07), (2.89, 3.30),
    (2.91, 2.92), (2.75, 3.22), (3.10, 3.05), (3.38, 2.88), (3.67, 2.73),
    (6.51, 7.24), (7.29, 6.74), (6.67, 7.06), (6.88, 6.93), (6.36, 7.37),
    (6.30, 7.22), (6.86, 7.19), (7.45, 6.63), (6.99, 7.31), (7.44, 6.83),
    (4.36, 1.94), (4.30, 1.84), (4.11, 2.34), (3.78, 1.86), (4.21, 1.64),
    (3.77, 2.47), (4.41, 1.73), (4.18, 1.96), (3.91, 1.73), (4.04, 2.18),
    (7.93, 3.20), (8.21, 3.07), (7.62, 3.43), (7.99, 2.84), (7.19, 3.58),
    (7.78, 3.17), (8.18, 2.91), (7.38, 3.30), (8.11, 2.77), (7.29, 3.36)
]

# Arm3 actual points, same target order
arm3_actual = [
    (2.40, 3.80), (1.75, 4.00), (2.30, 3.87), (1.62, 4.21), (1.38, 4.11),
    (2.09, 3.83), (1.49, 4.34), (1.96, 3.87), (2.02, 4.14), (1.50, 3.91),
    (2.55, 7.89), (2.80, 8.01), (3.25, 7.98), (3.29, 8.02), (3.44, 7.85),
    (2.66, 8.11), (2.96, 8.17), (3.44, 7.69), (2.80, 8.01), (2.55, 8.14),
    (3.11, 2.86), (3.27, 2.65), (3.22, 3.01), (3.11, 2.71), (2.65, 3.47),
    (3.26, 2.82), (2.73, 2.86), (2.94, 3.15), (2.48, 3.14), (2.81, 3.03),
    (6.18, 7.26), (7.69, 6.68), (7.08, 7.09), (7.18, 6.99), (7.05, 6.86),
    (6.59, 7.35), (6.83, 7.15), (6.67, 7.15), (6.63, 7.11), (6.48, 7.11),
    (3.81, 2.28), (4.50, 1.91), (4.20, 1.81), (3.90, 1.95), (3.47, 2.37),
    (4.22, 2.15), (3.83, 2.12), (4.06, 1.74), (3.66, 1.98), (3.63, 2.14),
    (8.15, 3.18), (7.78, 3.39), (8.29, 2.53), (7.83, 2.92), (7.50, 3.19),
    (8.68, 2.60), (7.67, 2.99), (8.17, 2.68), (7.43, 3.46), (8.29, 2.77)
]

# Targets in order
targets_list = [(2,4), (3,8), (3,3), (7,7), (4,2), (8,3)]

# Convert to (tx, ty, ax, ay) format
def build_data(targets, actuals):
    data = []
    for i, (tx, ty) in enumerate(targets):
        for j in range(10):
            ax, ay = actuals[i*10 + j]
            data.append((tx, ty, ax, ay))
    return data

arm2_data = build_data(targets_list, arm2_actual)
arm3_data = build_data(targets_list, arm3_actual)

# Start points
start_points = {
    'Arm2': (0, 1),
    'Arm3': (1, 0)
}

# METRIC: Convex hull area
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

# ANALYSIS: group by target, distance from start, hull area
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

arm_details = {}
for arm_name in ['Arm2', 'Arm3']:
    data = arm2_data if arm_name == 'Arm2' else arm3_data
    dist, area, info = analyze_arm(arm_name, data, start_points[arm_name])
    arm_details[arm_name] = (dist, area, info)

# PLOT: Convex hull area vs target distance
plt.figure(figsize=(8, 6))
colors = {'Arm2': 'blue', 'Arm3': 'green'}
markers = {'Arm2': 'o', 'Arm3': '^'}

for arm_name in ['Arm2', 'Arm3']:
    dist, area, info = arm_details[arm_name]
    plt.scatter(dist, area, c=colors[arm_name], marker=markers[arm_name],
                s=80, edgecolors='k', alpha=0.8, label=arm_name)

    # Target labels
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
                 label=f'{arm_name} fit: slope={coeffs[0]:.4f}, R²={corr**2:.3f}')

plt.xlabel('Distance from start point to target (units)')
plt.ylabel('Convex hull area of cluster (units²)')
plt.title('Multi‑arm (Area 2): Cluster spread vs target distance')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# PRINT TABLE
print("\n" + "="*60)
print("MULTI‑ARM CONVEX HULL AREAS (Area 2)")
print("="*60)
for arm_name in ['Arm2', 'Arm3']:
    dist, area, info = arm_details[arm_name]
    print(f"\n--- {arm_name} (start {start_points[arm_name]}) ---")
    print(f"{'Target':>12}  {'Distance':>9}  {'Area (units²)':>14}")
    print("-"*45)
    sorted_info = sorted(info, key=lambda x: x[1])
    for (tx, ty), d, a in sorted_info:
        print(f"({tx:5.1f}, {ty:5.1f})  {d:9.3f}  {a:14.4f}")

print("\n" + "="*60)
print("LINEAR FIT SUMMARY")
print("="*60)
for arm_name in ['Arm2', 'Arm3']:
    dist, area, _ = arm_details[arm_name]
    if len(dist) > 1:
        slope, intercept = np.polyfit(dist, area, 1)
        corr = np.corrcoef(dist, area)[0, 1]
        print(f"{arm_name}: slope={slope:.4f}, intercept={intercept:.4f}, R²={corr**2:.3f}")