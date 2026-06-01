import matplotlib.pyplot as plt
import numpy as np

# Data from Area 1 (Arm1 and Arm2)

# Arm1 reach points from Area 1 
arm1_points = [
    # from (-4,2)
    (-3.55, 1.85), (-3.42, 1.98), (-3.78, 2.02), (-3.68, 2.25), (-3.91, 1.56),
    (-3.61, 1.98), (-3.47, 2.17), (-3.83, 1.80), (-4.23, 1.38), (-4.19, 1.62),
    # from (-8,3)
    (-8.08, 2.67), (-8.17, 2.63), (-8.03, 2.90), (-7.70, 3.05), (-7.97, 2.85),
    (-7.85, 3.08), (-8.05, 2.77), (-7.80, 3.09), (-8.12, 2.89), (-8.14, 2.76),
    # from (-3,3)
    (-3.20, 3.05), (-3.04, 2.85), (-3.08, 3.05), (-2.85, 3.05), (-2.76, 3.10),
    (-2.87, 3.20), (-3.04, 3.19), (-3.26, 2.76), (-3.22, 2.85), (-3.14, 2.93),
    # from (-7,7)
    (-6.88, 6.90), (-6.61, 7.04), (-7.41, 6.58), (-6.98, 6.84), (-6.21, 7.19),
    (-6.65, 7.14), (-6.51, 7.08), (-7.54, 6.68), (-7.31, 6.67), (-6.32, 7.03),
    # from (-2,4)
    (-1.74, 4.00), (-1.84, 3.88), (-2.18, 4.07), (-1.89, 3.95), (-2.24, 3.68),
    (-1.98, 3.84), (-2.31, 3.77), (-1.83, 4.03), (-2.13, 3.96), (-1.68, 4.08),
    # from (-3,8)
    (-2.54, 8.19), (-2.75, 7.96), (-3.06, 7.89), (-2.57, 7.98), (-3.56, 7.81),
    (-2.92, 7.95), (-3.29, 7.78), (-2.84, 8.05), (-3.35, 7.89), (-2.58, 8.15)
]

# Arm2 reach points from Area 1 
arm2_points = [
    # from (-4,2)
    (-3.29, 2.11), (-3.55, 2.28), (-3.64, 2.38), (-3.82, 2.27), (-3.90, 1.84),
    (-3.71, 2.14), (-3.47, 2.17), (-3.82, 2.05), (-4.04, 1.82), (-4.16, 1.93),
    # from (-8,3)
    (-8.06, 2.99), (-8.04, 2.94), (-7.74, 3.14), (-7.72, 3.07), (-7.70, 3.30),
    (-7.86, 3.10), (-7.85, 3.06), (-7.70, 3.40), (-7.92, 3.08), (-7.90, 3.04),
    # from (-3,3)
    (-3.09, 2.63), (-2.93, 2.75), (-2.70, 2.85), (-3.41, 2.87), (-2.87, 2.90),
    (-2.67, 3.00), (-3.16, 2.75), (-2.59, 3.12), (-2.64, 3.27), (-2.85, 3.37),
    # from (-7,7)
    (-7.14, 6.78), (-7.18, 6.64), (-7.10, 7.13), (-7.53, 6.80), (-6.80, 7.00),
    (-6.82, 7.14), (-7.41, 6.76), (-6.47, 7.17), (-6.28, 7.29), (-7.27, 6.86),
    # from (-2,4)
    (-1.98, 4.13), (-2.26, 3.92), (-1.63, 4.01), (-2.21, 3.88), (-1.71, 4.25),
    (-2.10, 3.78), (-2.09, 3.87), (-1.69, 3.88), (-1.47, 4.19), (-2.18, 3.80),
    # from (-3,8)
    (-2.42, 8.14), (-3.34, 7.98), (-2.75, 8.16), (-3.38, 8.02), (-3.17, 8.00),
    (-3.29, 8.09), (-3.51, 7.92), (-2.98, 8.18), (-2.67, 8.07), (-3.57, 8.02)
]

# Target points
targets = {
    '(-4,2)': (-4, 2),
    '(-8,3)': (-8, 3),
    '(-3,3)': (-3, 3),
    '(-7,7)': (-7, 7),
    '(-2,4)': (-2, 4),
    '(-3,8)': (-3, 8)
}

# Start points for Arm1 and Arm2 (Arm3 start not used here, but included for completeness)
start_points = {
    'Arm1 start': (-1, 0),
    'Arm2 start': (0, 1),
    'Arm3 start': (1, 0)
}

# Plotting
plt.figure(figsize=(10, 10))

# Arm1 points (blue) 
arm1_x = [p[0] for p in arm1_points]
arm1_y = [p[1] for p in arm1_points]
plt.scatter(arm1_x, arm1_y, c='blue', marker='o', s=20, label='Arm1 reach', alpha=0.7)

# Arm2 points (orange) 
arm2_x = [p[0] for p in arm2_points]
arm2_y = [p[1] for p in arm2_points]
plt.scatter(arm2_x, arm2_y, c='orange', marker='^', s=20, label='Arm2 reach', alpha=0.7)

# Target points (red stars)
target_x = [p[0] for p in targets.values()]
target_y = [p[1] for p in targets.values()]
plt.scatter(target_x, target_y, c='red', marker='*', s=150, label='Targets', zorder=5)

# Start points (black squares)
start_x = [p[0] for p in start_points.values()]
start_y = [p[1] for p in start_points.values()]
plt.scatter(start_x, start_y, c='black', marker='s', s=100, label='Start points', zorder=5)

#add labels for targets
for name, (x, y) in targets.items():
    plt.annotate(name, (x, y), textcoords="offset points", xytext=(5,5), fontsize=9)

# Determine axis range 
all_x = arm1_x + arm2_x + target_x + start_x
all_y = arm1_y + arm2_y + target_y + start_y
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)

# Set axis of incrementing by 1
plt.xticks(np.arange(np.floor(x_min)-1, np.ceil(x_max)+2, 1))
plt.yticks(np.arange(np.floor(y_min)-1, np.ceil(y_max)+2, 1))

# Set limits with a little padding
plt.xlim(x_min-1, x_max+1)
plt.ylim(y_min-1, y_max+1)

# Grid and axis lines
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
plt.grid(True, linestyle=':', alpha=0.6)

plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Arm1 (blue) and Arm2 (orange) reach points from Area 1 multi‑arm tests')
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()