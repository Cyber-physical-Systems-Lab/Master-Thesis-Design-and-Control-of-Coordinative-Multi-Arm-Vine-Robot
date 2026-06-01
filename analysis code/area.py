import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.patches import Rectangle
from matplotlib.path import Path

# ---------- original data ----------
red_points = [(-1, 0), (0, 1), (1, 0)]

blue_points = [
    (-0.45, -9.87), (-7.33, -6.55), (-10.18, 0.18), (-8.38, 6.36), (-1.16, 10.56),
    (-1.19, -10.39), (-7.36, -6.88), (-9.65, 0.75), (-7.82, 7.15), (-0.17, 9.93),
    (-1.44, -10.21), (-8.84, -5.61), (-10.14, -0.69), (-8.22, 7.54), (-1.52, 9.87),
    (-1.85, -10.11), (-8.09, -6.85), (-9.79, 1.11), (-8.33, 7.03), (-1.16, 9.86),
    (-0.95, -10.53), (-7.53, -7.58), (-9.57, 1.44), (-8.48, 6.72), (-0.80, 10.00),
    (-0.86, -9.89), (-8.63, -6.03), (-9.69, -0.73), (-7.35, 7.19), (-1.39, 10.12),
    (-1.32, -9.99), (-8.00, -6.45), (-10.28, 0.73), (-6.98, 7.42), (-0.75, 10.34),
    (-0.74, -10.39), (-8.45, -7.17), (-10.24, -0.23), (-6.40, 7.79), (-1.06, 10.18),
    (-0.35, -10.17), (-7.79, -6.94), (-10.14, 0.46), (-7.73, 7.46), (-0.37, 10.22),
    (-0.14, -9.75), (-8.52, -6.52), (-10.48, 0.10), (-8.16, 7.10), (-0.60, 10.12),
]

green_points = [
    (-10.65, 1.25), (-8.41, 7.83), (-0.19, 10.35), (8.36, 8.27), (10.38, 1.01),
    (-10.65, 0.8), (-8.33, 8.34), (-0.74, 10.58), (7.88, 8.75), (10.03, 0.32),
    (-10.7, 0.33), (-7.84, 8.68), (-1.18, 10.08), (9.02, 8.29), (10.38, 0.29),
    (-10.57, 1.59), (-7.89, 7.62), (0.94, 9.7), (8.71, 8.56), (10.41, 0.72),
    (-10.46, 1.04), (-7.71, 8.01), (-0.79, 9.78), (9.16, 7.5), (9.64, 0.5),
    (-10.31, 0.44), (-7.6, 8.29), (1.134, 10.25), (8.31, 8.77), (10.19, 1.7),
    (-10.28, 1.31), (-6.95, 8.82), (0.22, 10.39), (9.05, 9.06), (9.98, 0.61),
    (-10.17, 0.96), (7.32, 7.98), (0.36, 10.06), (8.57, 9.17), (9.72, 1.38),
    (-10.28, 1.91), (-7.19, 8.32), (-0.54, 10.16), (7.99, 9.14), (10.27, 1.28),
    (-10.31, 0.44), (-6.69, 8.42), (0.55, 10.55), (7.48, 9.22), (9.69, 1.91),
]

yellow_points = [
    (0.64, 9.98), (8.37, 8.48), (9.82, 0.18), (8.36, -6.67), (1.62, -10.19),
    (0.76, 10.23), (9.38, 7.49), (10.13, 0.26), (7.85, -7.27), (0.88, -10.45),
    (1.15, 10.13), (9.14, 8.87), (9.78, -0.13), (7.40, -7.83), (0.60, -10.67),
    (1.92, 9.69), (8.71, 7.71), (10.37, 0.02), (8.09, -7.38), (1.44, -10.01),
    (1.52, 9.87), (8.73, 8.63), (10.05, 0.15), (8.30, -7.29), (1.40, -10.50),
    (1.15, 10.42), (8.39, 8.86), (9.56, -0.29), (7.66, -7.73), (0.15, -10.18),
    (0.88, 10.53), (8.54, 8.20), (10.24, -0.20), (8.04, -7.77), (0.98, -10.71),
    (1.34, 10.22), (9.33, 8.14), (9.89, 0.39), (8.25, -6.95), (1.23, -10.27),
    (0.36, 9.84), (8.11, 8.61), (9.96, -0.15), (7.89, -7.53), (0.91, -10.13),
    (1.87, 9.99), (9.01, 8.33), (9.66, 0.57), (7.42, -7.53), (0.56, -10.25),
]

# ---------- merge points ----------
all_points = np.array(red_points + blue_points + green_points + yellow_points)
rx, ry = zip(*red_points)
bx, by = zip(*blue_points)
gx, gy = zip(*green_points)
yx, yy = zip(*yellow_points)

# ---------- convex hull ----------
hull = ConvexHull(all_points)
hull_vertices = all_points[hull.vertices]

# shoelace area
x = hull_vertices[:, 0]
y = hull_vertices[:, 1]
area_hull = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
perimeter_hull = hull.area   # 2D: area -> perimeter

# excluded central 2x2 square (4 unit²)
hull_path = Path(hull_vertices)
corners = np.array([[1,1], [1,-1], [-1,1], [-1,-1]])
inside = hull_path.contains_points(corners)
if np.all(inside):
    excluded_area = 4.0
else:
    excluded_area = 0.0
area_net = area_hull - excluded_area

# real-world conversion: 1 unit = 10 cm
scale = 10.0
area_net_cm2 = area_net * (scale ** 2)
area_net_m2 = area_net_cm2 / 10000

# ---------- plot (zoomed to [-11, 11]) ----------
fig, ax = plt.subplots(figsize=(10, 10))

# scatter points
ax.scatter(bx, by, color='blue', s=15, zorder=5, label='Arm1 reaches')
ax.scatter(gx, gy, color='green', s=15, zorder=5, label='Arm2 reaches')
ax.scatter(yx, yy, color='goldenrod', s=15, zorder=5, label='Arm3 reaches',
           edgecolors='goldenrod', linewidths=0.3)
ax.scatter(rx, ry, color='red', s=100, zorder=6, label='Vine arm starting point')

# convex hull (red line)
for simplex in hull.simplices:
    ax.plot(all_points[simplex, 0], all_points[simplex, 1], 'r-', linewidth=2)

# excluded central square
excl_rect = Rectangle((-1, -1), 2, 2, linewidth=1.5, edgecolor='darkred',
                       facecolor='red', alpha=0.25, zorder=7,
                       label='Excluded central region\n(2×2 square, area=4 units²)')
ax.add_patch(excl_rect)

# axes and grid
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(f'Coverage area after excluding centre: {area_net:.1f} units² = {area_net_m2:.3f} m²')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_aspect('equal')

# Force exactly -11 to 11 on both axes
ax.set_xlim(-11, 11)
ax.set_ylim(-11, 11)
ax.set_xticks(np.arange(-11, 12, 1))
ax.set_yticks(np.arange(-11, 12, 1))

ax.legend(loc='upper right')
plt.tight_layout()
plt.show()

# ---------- printed results ----------
print(f"Convex hull perimeter (red line): {perimeter_hull:.4f} units")
print(f"Convex hull total area:            {area_hull:.4f} units²")
print(f"Excluded central square area:      {excluded_area:.2f} units²")
print(f"Net coverage area (units²):         {area_net:.4f} units²")
print(f"Net coverage area (cm²):            {area_net_cm2:.2f} cm²")
print(f"Net coverage area (m²):             {area_net_m2:.4f} m²")