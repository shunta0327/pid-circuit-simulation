import matplotlib.pyplot as plt
import math
import numpy as np
course_x = []
course_y = []
def generate_course(num_points=800):
    pts = []

    # 1. 上側の直線
    n1 = int(num_points * 0.2)

    x = np.linspace(-10, 8, n1, endpoint=False)
    y = np.full(n1, 8.0)

    pts.append(np.vstack([x, y]).T)


    # 2. 右上コーナー
    n2 = int(num_points * 0.15)

    theta = np.linspace(np.pi / 2, 0, n2, endpoint=False)

    cx = 8
    cy = 4
    r = 4

    x = cx + r * np.cos(theta)
    y = cy + r * np.sin(theta)

    pts.append(np.vstack([x, y]).T)


    # 3. 右側のS字
    n3 = int(num_points * 0.2)

    x = np.linspace(12, 12, n3, endpoint=False)
    t = np.linspace(0, 1, n3, endpoint=False)

    y = 4 - 12 * t

    # x方向にS字を作る
    x = x + 2 * np.sin(2 * np.pi * t)

    pts.append(np.vstack([x, y]).T)


    # 4. 右下コーナー
    n4 = int(num_points * 0.15)

    theta = np.linspace(0, -np.pi / 2, n4, endpoint=False)

    cx = 8
    cy = -8
    r = 4

    x = cx + r * np.cos(theta)
    y = cy + r * np.sin(theta)

    pts.append(np.vstack([x, y]).T)


    # 5. 下側の直線
    n5 = int(num_points * 0.15)

    x = np.linspace(8, -10, n5, endpoint=False)
    y = np.full(n5, -12.0)

    pts.append(np.vstack([x, y]).T)


    # 6. 左側の大きな半円
    n6 = num_points - (n1 + n2 + n3 + n4 + n5)

    theta = np.linspace(-np.pi / 2, np.pi / 2, n6)

    cx = -10
    cy = -2
    r = 10

    x = cx - r * np.cos(theta)
    y = cy + r * np.sin(theta)

    pts.append(np.vstack([x, y]).T)


    # 全部つなげる
    pts = np.vstack(pts)

    course_x = pts[:, 0]
    course_y = pts[:, 1]

    return course_x, course_y


# コース生成
course_x, course_y = generate_course()

plt.plot(course_x,course_y)
plt.axis("equal")
plt.savefig("pid_course.png")
x = 10
y = 0
psi = 0
v = 4
L = 2.5
dt = 0.1
kr = 0.1
kpsi = 1.0
ki = 0
kd = 0.45
kv = 2.0
kster = 3.0
ke = 0.5
integral_psi = 0
t = 0
pre_error_psi = 0
target_v = v
x_list = []
y_list = []
v_list = []
v_target_list = []
delta_theta_list = []
delta_list = []
for j in range(3000):
 x_list.append(x)
 y_list.append(y)
 dmin = math.sqrt((course_x[t] - x)**2 + (course_y[t] - y)**2)
 new_t = t
 for offset in range(0,80):
  i = (t + offset) % len(course_x)
  di = math.sqrt((course_x[i] - x)**2 + (course_y[i] - y)**2)
  if di <= dmin:
   dmin = di
   new_t = i
 t = new_t
 p1 = t
 p2 = (t + 30) % len(course_x)
 p3 = (t + 60) % len(course_x)
 theta1 = math.atan2(course_y[p2] - course_y[p1],course_x[p2] - course_x[p1])
 theta2 = math.atan2(course_y[p3] - course_y[p2],course_x[p3] - course_x[p2])
 delta_theta = theta2 - theta1
 delta_theta = math.atan2(math.sin(delta_theta),math.cos(delta_theta))
 target_index = (t + 5) % len(course_x)
 target_x = course_x[target_index]
 target_y = course_y[target_index]
 psi_target = math.atan2(target_y - y,target_x - x)
 error_psi = psi_target - psi
 error_psi = math.atan2(math.sin(error_psi),math.cos(error_psi))
 der = (error_psi - pre_error_psi) / dt
 integral_psi += error_psi * dt
 next_x = course_x[target_index] - course_x[t]
 next_y = course_y[target_index] - course_y[t]
 ed_x = x - course_x[t]
 ed_y = y - course_y[t]
 ed_r = math.sqrt((x - course_x[t])**2 + (y - course_y[t]) ** 2)
 judge = next_x * ed_y - next_y * ed_x
 ed = judge / math.sqrt(next_x**2 + next_y**2)
 
 delta =   kpsi * error_psi +ki * integral_psi + kd * der - ke * ed
 delta_max = math.radians(30)
 delta = max(-delta_max, min(delta,delta_max))
 delta_theta_list.append(abs(delta_theta))
 delta_list.append(abs(delta))
 v_min = 1
 v_max = 8
 target_v_raw  = max(v_min,v_max - kv * abs(delta_theta) - kster * abs(delta))
 target_v = 0.9 * target_v + 0.1 * target_v_raw
 v_target_list.append(target_v)
 a = 2.0
 v += a * (target_v - v) * dt
 v_list.append(v)
 x += v*math.cos(psi) * dt
 y += v*math.sin(psi) * dt
 psi += v / L * math.tan(delta) * dt
 pre_error_psi = error_psi
plt.plot(x_list,y_list)
plt.savefig("pid_result.png")
plt.figure()

plt.plot(v_list, label="v")
plt.plot(v_target_list, label="target_v")

plt.xlabel("step")
plt.ylabel("speed")
plt.legend()
plt.grid()

plt.savefig("speed_result.png")
plt.figure()

plt.plot(delta_theta_list, label="abs(delta_theta)")
plt.plot(delta_list, label="abs(delta)")

plt.xlabel("step")
plt.ylabel("angle [rad]")

plt.legend()
plt.grid()

plt.savefig("angle_result.png")