import matplotlib.pyplot as plt
import numpy as np

# Data 
# Arm2 reach points 
arm2_points = [
    # from (2,4)
    (2.49, 3.92), (2.02, 3.75), (1.82, 3.89), (2.25, 3.79), (1.88, 4.14),
    (2.19, 4.07), (1.66, 4.08), (1.69, 3.89), (2.15, 3.96), (2.33, 4.08),
    # from (3,8)
    (2.52, 8.15), (3.06, 7.91), (2.90, 7.92), (2.32, 8.33), (3.42, 8.07),
    (3.55, 7.87), (2.32, 7.95), (3.31, 7.86), (2.72, 7.95), (3.25, 8.15),
    # from (3,3)
    (2.68, 3.02), (3.35, 2.76), (3.01, 2.87), (2.56, 3.07), (2.89, 3.30),
    (2.91, 2.92), (2.75, 3.22), (3.10, 3.05), (3.38, 2.88), (3.67, 2.73),
    # from (7,7)
    (6.51, 7.24), (7.29, 6.74), (6.67, 7.06), (6.88, 6.93), (6.36, 7.37),
    (6.30, 7.22), (6.86, 7.19), (7.45, 6.63), (6.99, 7.31), (7.44, 6.83),
    # from (4,2)
    (4.36, 1.94), (4.30, 1.84), (4.11, 2.34), (3.78, 1.86), (4.21, 1.64),
    (3.77, 2.47), (4.41, 1.73), (4.18, 1.96), (3.91, 1.73), (4.04, 2.18),
    # from (8,3)
    (7.93, 3.20), (8.21, 3.07), (7.62, 3.43), (7.99, 2.84), (7.19, 3.58),
    (7.78, 3.17), (8.18, 2.91), (7.38, 3.30), (8.11, 2.77), (7.29, 3.36)
]

# Arm3 reach points
arm3_points = [
    # from (2,4)
    (2.40, 3.80), (1.75, 4.00), (2.30, 3.87), (1.62, 4.21), (1.38, 4.11),
    (2.09, 3.83), (1.49, 4.34), (1.96, 3.87), (2.02, 4.14), (1.50, 3.91),
    # from (3,8)
    (2.55, 7.89), (2.80, 8.01), (3.25, 7.98), (3.29, 8.02), (3.44, 7.85),
    (2.66, 8.11), (2.96, 8.17), (3.44, 7.69), (2.80, 8.01), (2.55, 8.14),
    # from (3,3)
    (3.11, 2.86), (3.27, 2.65), (3.22, 3.01), (3.11, 2.71), (2.65, 3.47),
    (3.26, 2.82), (2.73, 2.86), (2.94, 3.15), (2.48, 3.14), (2.81, 3.03),
    # from (7,7)
    (6.18, 7.26), (7.69, 6.68), (7.08, 7.09), (7.18, 6.99), (7.05, 6.86),
    (6.59, 7.35), (6.83, 7.15), (6.67, 7.15), (6.63, 7.11), (6.48, 7.11),
    # from (4,2)
    (3.81, 2.28), (4.50, 1.91), (4.20, 1.81), (3.90, 1.95), (3.47, 2.37),
    (4.22, 2.15), (3.83, 2.12), (4.06, 1.74), (3.66, 1.98), (3.63, 2.14),
    # from (8,3)
    (8.15, 3.18), (7.78, 3.39), (8.29, 2.53), (7.83, 2.92), (7.50, 3.19),
    (8.68, 2.60), (7.67, 2.99), (8.17, 2.68), (7.43, 3.46), (8.29, 2.77)
]

# Target points
targets = {
    '(2,4)': (2,4), '(3,8)': (3,8), '(3,3)': (3,3),
    '(7,7)': (7,7), '(4,2)': (4,2), '(8,3)': (8,3)
}

# Start points
start_points = {
    'Arm1 start': (-1,0),
    'Arm2 start': (0,1),
    'Arm3 start': (1,0)
}

# Plotting
plt.figure(figsize=(10, 10))

# Arm2 points (blue) 
arm2_x = [p[0] for p in arm2_points]
arm2_y = [p[1] for p in arm2_points]
plt.scatter(arm2_x, arm2_y, c='blue', marker='o', s=20, label='Arm2 reach', alpha=0.7)

# Arm3 points (green) 
arm3_x = [p[0] for p in arm3_points]
arm3_y = [p[1] for p in arm3_points]
plt.scatter(arm3_x, arm3_y, c='green', marker='^', s=20, label='Arm3 reach', alpha=0.7)

# Target points (red stars)
target_x = [p[0] for p in targets.values()]
target_y = [p[1] for p in targets.values()]
plt.scatter(target_x, target_y, c='red', marker='*', s=150, label='Targets', zorder=5)

# Start points (black squares)
start_x = [p[0] for p in start_points.values()]
start_y = [p[1] for p in start_points.values()]
plt.scatter(start_x, start_y, c='black', marker='s', s=100, label='Start points', zorder=5)

# Optional: add labels for targets
for name, (x,y) in targets.items():
    plt.annotate(name, (x,y), textcoords="offset points", xytext=(5,5), fontsize=9)

# Set axis ticks to increments of 1
# Determine range from all points
all_x = arm2_x + arm3_x + target_x + start_x
all_y = arm2_y + arm3_y + target_y + start_y
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
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
plt.title('Arm2 (blue) and Arm3 (green) reach points from all multi‑arm tests')
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()