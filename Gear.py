import matplotlib.pyplot as plt
import math
import numpy as np


def radial_line(theta, r1, r2):  # To draw line a radial line from r1 to r2
    return [[r1 * math.cos(theta), r2 * math.cos(theta)], [r1 * math.sin(theta), r2 * math.sin(theta)]]


def arc(r, theta1, theta2):  # To draw arc
    coords = np.array([[], []])
    for theta in np.arange(theta1, theta2, 0.001):
        coords = np.append(coords, [[r * math.cos(theta)], [r * math.sin(theta)]], axis=1)
    return coords


def rot_matrix(theta):  # Rotational Matrix
    return [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]


# initialising
N = 20
m = 10
phi = 20 * math.pi / 180
b_width = 17.63

r_p = m * N / 2
r_b = r_p * math.cos(phi)
r_d = r_p - 1.25 * m
r_a = r_p + m
t_angle = b_width / r_b  # angle subtended by tooth width at base circle

right_side = left_side = tooth_coords = gear_coords = np.array([[], []])

# Construction of involute curve
t = 0
while True:  # Right side of tooth
    x = r_b * (math.cos(t) + t * math.sin(t))
    y = r_b * (math.sin(t) - t * math.cos(t))
    if r_d ** 2 <= x ** 2 + y ** 2 <= r_a ** 2:
        right_side = np.append(right_side, [[x], [y]], axis=1)
    elif x ** 2 + y ** 2 > r_a ** 2:
        t1 = math.atan2(y, x)
        break
    t += 0.001

left_side = np.flip(np.dot(rot_matrix(t_angle), [right_side[0], right_side[1] * -1]), 1)  # Left side of tooth

# Construction of tooth profile
if r_d < r_b:
    tooth_coords = radial_line(0, r_d, r_b)  # line connecting dedentum circle and involute curve

tooth_coords = np.concatenate((tooth_coords, right_side, arc(r_a, t1, t_angle - t1), left_side), axis=1)  # Tooth

if r_d < r_b:
    tooth_coords = np.concatenate((tooth_coords, radial_line(t_angle, r_d, r_b)),
                                  axis=1)  # line connecting dedentum circle and involute curve

tooth_coords = np.concatenate((tooth_coords, arc(r_d, t_angle, 2 * math.pi / 20)), axis=1)  # Dedendum arc

# Construction of N number of teeth
for j in range(N):
    t = j * 2 * math.pi / N
    gear_coords = np.concatenate((gear_coords, np.dot(rot_matrix(t), tooth_coords)), axis=1)

# Plotting gear profile
plt.axis('equal')
plt.plot(gear_coords[0], gear_coords[1])
plt.show()

