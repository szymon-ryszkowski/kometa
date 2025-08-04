import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt

from math import *
from mpl_toolkits.mplot3d import Axes3D

kometa = cb.celestial_body(2*config.AU, 0.2, 4, 0, 36, 72, 2.1*config.AU, -1, config.M, config.G)
#zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []

#distances = []

for i in range(config.n_steps):
    x_traj.append(kometa.x)
    y_traj.append(kometa.y)
    z_traj.append(kometa.z)
    #utwórz cząstki
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, kometa.r, 2)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(4000, kometa.x, kometa.y, kometa.z, kometa.v_x, kometa.v_y, kometa.v_z)

    #przesun komete i zmien predkosc
    kometa.x += kometa.v_x*config.dt
    kometa.y += kometa.v_y*config.dt
    kometa.z += kometa.v_z*config.dt
    acceleration_x = -kometa.x*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_y = -kometa.y*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_z = -kometa.z*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    kometa.v_x += acceleration_x*config.dt
    kometa.v_y += acceleration_y*config.dt
    kometa.v_z += acceleration_z*config.dt

    #distance = sqrt(kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2)/config.AU
    #distances.append(distance)

    #przesun czastke
    pt.particles[:, 1] += pt.particles[:, 4] * config.dt
    pt.particles[:, 2] += pt.particles[:, 5] * config.dt
    pt.particles[:, 3] += pt.particles[:, 6] * config.dt


#wizualizacja 3d
#print(f'Minimalna odległość komety: {min(distances):.2e} m')
#print(f'Maksymalna odległość komety: {max(distances):.2e} m')
print(pt.particles.shape)
#print(pt.particles[:, 4], pt.particles[:, 5], pt.particles[:, 6])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3], color='red', s=1, label='Cząstki')
ax.plot(x_traj, y_traj, z_traj, label='Trajektoria komety')
#ax.scatter(0, 0, 0, color='yellow', label='Słońce')  # Pozycja Słońca w środku
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Trajektoria komety w 3D')
ax.legend()
plt.show()