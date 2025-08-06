import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt

from math import *
from mpl_toolkits.mplot3d import Axes3D
kometa = cb.celestial_body(config.a_k*config.AU, config.e_k, config.i_k, config.t_0_k, config.arg_of_per_k, config.long_of_asc_z_k, config.r_m_k*config.AU, config.t_m, config.M, config.G)

#animacja 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter([], [], [], color='red', s=1, label='Cząstki')
traj_line, = ax.plot([], [], [], color='blue', label='Trajektoria komety')

ax.set_xlim([kometa.x -3e9, kometa.x +3e9])
ax.set_ylim([kometa.y -3e9, kometa.y +3e9])
ax.set_zlim([kometa.z -3e9, kometa.z +3e9])
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Trajektoria komety w 3D')
ax.legend()
plt.ion()  # Włącza interaktywne rysowanie
plt.show()

kometa = cb.celestial_body(config.a_k*config.AU, config.e_k, config.i_k, config.t_0_k, config.arg_of_per_k, config.long_of_asc_z_k, config.r_m_k*config.AU, config.t_m, config.M, config.G)
#zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []

#distances = []

for i in range(config.n_steps):
    '''if i % 3 == 0:
        traj_line.set_data(x_traj, y_traj)
        traj_line.set_3d_properties(z_traj)
        if pt.particles.shape[0] > 0:
            sc._offsets3d = (pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3])
        plt.draw()
        plt.pause(0.01)
        ax.set_xlim([kometa.x - 3e8, kometa.x + 3e8])
        ax.set_ylim([kometa.y - 3e8, kometa.y + 3e8])
        ax.set_zlim([kometa.z - 3e8, kometa.z + 3e8])'''
    x_traj.append(kometa.x)
    y_traj.append(kometa.y)
    z_traj.append(kometa.z)
    #utwórz cząstki
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, kometa.r, 3)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(100, kometa.x, kometa.y, kometa.z, kometa.v_x, kometa.v_y, kometa.v_z)
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
    #zmien prędkosc
    acceleration_x = -pt.particles[:, 1]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - pt.particles[:, 7])
    acceleration_y = -pt.particles[:, 2]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - pt.particles[:, 7])
    acceleration_z = -pt.particles[:, 3]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - pt.particles[:, 7])

    pt.particles[:, 4] += acceleration_x*config.dt
    pt.particles[:, 5] += acceleration_y*config.dt
    pt.particles[:, 6] += acceleration_z*config.dt
    #animacja 3d
#wizualizacja 3d
#print(f'Minimalna odległość komety: {min(distances):.2e} m')
#print(f'Maksymalna odległość komety: {max(distances):.2e} m')
'''print(pt.particles.shape)
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
plt.show()'''