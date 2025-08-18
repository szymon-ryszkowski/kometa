import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt
import numpy as np
import Sun
from datetime import date
from datetime import timedelta
from math import *
from mpl_toolkits.mplot3d import Axes3D
#deklaracja komety
kometa = cb.celestial_body(config.a_k*config.AU, config.e_k, config.i_k, config.t_0_k, config.arg_of_per_k, config.long_of_asc_z_k, config.r_m_k*config.AU, config.t_m, config.M, config.G)

dany_dzien = date(int(input()),int(input()),int(input()))

#animacja 3d przygotowanie wykresu (czerwone cząstki - H2O, turkusowe - typu 1)
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




#zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []
#zapis odległości do Słońca komety(do sprawdzania poprawności celestial_body.pu i loop.py)
distances = []
liczba_krokow = 0
ile_dni = dany_dzien - config.data_startowa
ile_dni = int(ile_dni.days)

for i in range(config.n_steps):
    liczba_krokow +=1
    aktualna_data = dany_dzien + timedelta(days = liczba_krokow / config.dzien_krok)
    print(aktualna_data)
    print(int(liczba_krokow / config.dzien_krok))
    aktywnosc = Sun.sun_aktywnosc(int(ile_dni + (liczba_krokow / config.dzien_krok)))
    # animacja 3d
    if i % 100 == 0:
        traj_line.set_data(x_traj, y_traj)
        traj_line.set_3d_properties(z_traj)
        if pt.particles.shape[0] > 0:
            sc._offsets3d = (pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3])
            if pt.particles.shape[0] > 0:
                colors = np.where(pt.particles[:, 0] == 1, 'aqua', 'red')
                sc._offsets3d = (pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3])
                sc.set_color(colors)
        plt.draw()
        plt.pause(0.01)
        ax.set_xlim([kometa.x - 5e11, kometa.x + 5e11])
        ax.set_ylim([kometa.y - 5e11, kometa.y + 5e11])
        ax.set_zlim([kometa.z - 5e11, kometa.z + 5e11])
    #dodaj trajektorie do wyswietlenia
    x_traj.append(kometa.x)
    y_traj.append(kometa.y)
    z_traj.append(kometa.z)
    #utwórz cząstki
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, sqrt(kometa.x**2 + kometa.y**2 + kometa.z**2), -3)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(1000, kometa.x, kometa.y, kometa.z, kometa.v_x, kometa.v_y, kometa.v_z)
    #przesun komete
    kometa.x += kometa.v_x*config.dt
    kometa.y += kometa.v_y*config.dt
    kometa.z += kometa.v_z*config.dt
    #zmien predkosc
    acceleration_x = -kometa.x*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_y = -kometa.y*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_z = -kometa.z*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    kometa.v_x += acceleration_x*config.dt
    kometa.v_y += acceleration_y*config.dt
    kometa.v_z += acceleration_z*config.dt

    #rozpadnij cząstki
    pt.dissect(config.dissection_rate, config.dt)

    #policz minimalną i maksymalną odległość do komety(do sprawdzania poprawności celestial_body.pu i loop.py)
    distance = sqrt(kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2)/config.AU
    distances.append(distance)

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



print(f'Minimalna odległość komety: {min(distances):.2e} m')
print(f'Maksymalna odległość komety: {max(distances):.2e} m')
#wizualizacja 3d końcowego stanu
def show_final():
    print(pt.particles.shape)
    global x_traj, y_traj, z_traj
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = np.where(pt.particles[:, 0] == 1, 'green', 'red')
    ax.scatter(pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3], c=colors, s=1, label='Cząstki')
    ax.plot(x_traj, y_traj, z_traj, label='Trajektoria komety')
    #ax.scatter(0, 0, 0, color='yellow', label='Słońce')  # Pozycja Słońca w środku
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    ax.set_title('Trajektoria komety w 3D')
    ax.legend()
    plt.show()


#show_final()
#print(pt.particles.shape)