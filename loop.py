import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

kometa = cb.celestial_body(2*config.AU, 0.2, 90, 0, 0, 0, 2*config.AU, -1, config.M, config.G)
#zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []
for i in range(config.n_steps):
    x_traj.append(kometa.x)
    y_traj.append(kometa.y)
    z_traj.append(kometa.z)
    #utwórz cząstki
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, kometa.r, 2)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(4, kometa.x, kometa.y, kometa.z)

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
#wizualizacja 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_traj, y_traj, z_traj, label='Trajektoria komety')
ax.scatter(0, 0, 0, color='yellow', label='Słońce')  # Pozycja Słońca w środku
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Trajektoria komety w 3D')
ax.legend()
plt.show()