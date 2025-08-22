import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt
import numpy as np
import Sun
from datetime import date
from datetime import timedelta
from math import *
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
# deklaracja komety
kometa = (
    cb.Celestial_Body(config.a_k*config.AU, config.e_k, config.i_k, config.t_0_k, config.arg_of_per_k,
                      config.long_of_asc_z_k, config.theta, config.t_m, config.M, config.G,config.r_p))
ziemia = (
    cb.Celestial_Body(config.a_m*config.AU, config.e_m, config.i_m, config.t_0_m, config.arg_of_per_m,
                     config.long_of_asc_z_m, 1, config.t_m, config.M, config.G,0))


print("podaj rok w zakresie od 1948 do 2024- ")
rok = int(input())
while rok < 1948 or rok > 2024 and rok == int(rok):
    print("podano nieprawidłową datę")
    rok = int(input())
print("podaj miesiąc - ")
miesiac = int(input())
while miesiac < 1 or miesiac > 12 and miesiac == int(miesiac):
    print("podano nieprawidłową datę")
    miesiac = int(input())

print("podaj dzien - ")
dzien = int(input())
while (dzien < 1 or dzien > 31 or (miesiac == 2 and dzien > 29) or (rok % 4 != 0 and miesiac == 2 and dzien > 28) or
       ((miesiac == 4 or miesiac == 6 or miesiac == 9 or miesiac == 11) and dzien > 30) and dzien == int(dzien)):
    print("podano nieprawidłową datę")
    dzien = int(input())

dany_dzien = date(rok, miesiac, dzien)


# animacja 3d przygotowanie wykresu (czerwone cząstki - H2O, turkusowe - typu 1)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(0, 0, 0, color='yellow', s=100, label='Słońce')  # Pozycja Słońca w środku
Ziemia_o = ax.scatter(ziemia.x, ziemia.y, ziemia.z, color='darkblue', s=10, label='Ziemia')
traj_Ziemia, = ax.plot([], [],[], color='blue', linewidth=.5)
Kometa = ax.scatter(kometa.x, kometa.y, kometa.z, color='grey', s=5, label='Kometa')
sc = ax.scatter([], [], [], color=config.color_map[1], s=1, label='Cząstki H')
sc = ax.scatter([], [], [], color=config.color_map[0], s=1, label='Cząstki H20')
sc = ax.scatter([], [], [], color=config.color_map[2], s=1, label='Cząstki OH')
traj_line, = ax.plot([], [], [], color='grey')


ax.set_xlabel('X [AU]')
ax.set_ylabel('Y [AU]')
ax.set_zlabel('Z [AU]')
ax.set_title('Trajektoria komety w 3D')
ax.legend(
    prop={'size': 8},
    loc='lower left',
    bbox_to_anchor=(1, 0)
)
plt.subplots_adjust(right=0.8)
plt.ion()  # Włącza interaktywne rysowanie
plt.show()

# zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []

x_traj_z = []
y_traj_z = []
z_traj_z = []

# zapis odległości do Słońca komety(do sprawdzania poprawności celestial_body.pu i loop.py)
distances = []

ile_dni = dany_dzien - config.data_startowa
ile_dni = int(ile_dni.days)

time_text = ax.text2D(.1, .9, dany_dzien,transform=ax.transAxes)

def show_final ():
    liczba_krokow = 0
    for i in range(config.n_steps):
        liczba_krokow += 1
        aktualna_data = dany_dzien + timedelta(days=liczba_krokow / config.dzien_krok)
        pt.count_particles()
        aktywnosc = Sun.sun_aktywnosc(int(ile_dni + (liczba_krokow / config.dzien_krok)))
        pt.count_particles()
        # animacja 3d
        if i % 50 == 0:
            time_text.set_text(aktualna_data)
            traj_line.set_data(x_traj, y_traj)
            traj_line.set_3d_properties(z_traj)
            traj_Ziemia.set_data(x_traj_z, y_traj_z)
            traj_Ziemia.set_3d_properties(z_traj_z)
            #Ziemia_o._offsets3d = (ziemia.x, ziemia.y, ziemia.z)
            if pt.particles.shape[0] > 0:
                sc._offsets3d = (pt.particles[:, 1], pt.particles[:, 2], pt.particles[:, 3])
                if pt.particles.shape[0] > 0:
                    # mapa typów do kolorów
                    mask = (
                            (pt.particles[:, 1] >= ax.get_xlim()[0]) & (pt.particles[:, 1] <= ax.get_xlim()[1]) &
                            (pt.particles[:, 2] >= ax.get_ylim()[0]) & (pt.particles[:, 2] <= ax.get_ylim()[1]) &
                            (pt.particles[:, 3] >= ax.get_zlim()[0]) & (pt.particles[:, 3] <= ax.get_zlim()[1])
                    )
                    widoczne_particles = pt.particles[mask]
                    # przypisanie kolorów
                    if widoczne_particles.shape[0] > 0:
                        sc._offsets3d = (
                            widoczne_particles[:, 1],  # X
                            widoczne_particles[:, 2],  # Y
                            widoczne_particles[:, 3]  # Z
                        )
                        colors = [config.color_map[t] for t in widoczne_particles[:, 0]]
                        sc.set_color(colors)
                    else:
                        # jeśli nic nie jest w granicach, czyścimy
                        sc._offsets3d = ([], [], [])
            # policz minimalną i maksymalną odległość do komety(do sprawdzania poprawności celestial_body.pu i loop.py)
            distance = sqrt(kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2)
            distances.append(distance)
            plt.draw()
            plt.pause(0.01)
            ax.set_xlim([0.5*kometa.x - distance, 0.5*kometa.x + distance])
            ax.set_ylim([0.5*kometa.y - distance, 0.5*kometa.y + distance])
            ax.set_zlim([0.5*kometa.z - distance, 0.5*kometa.z + distance])

        # dodaj trajektorie do wyswietlenia
        x_traj.append(kometa.x)
        y_traj.append(kometa.y)
        z_traj.append(kometa.z)

        x_traj_z.append(ziemia.x)
        y_traj_z.append(ziemia.y)
        z_traj_z.append(ziemia.z)

        # utwórz cząstki
        ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, sqrt(kometa.x**2 + kometa.y**2 + kometa.z**2), -3)
        pt.queue_H_2O += ratio*config.dt
        pt.add_particles(1000, kometa.x, kometa.y, kometa.z, kometa.v_x, kometa.v_y, kometa.v_z)

        # przesun komete i Ziemie
        kometa.x += kometa.v_x * config.dt
        kometa.y += kometa.v_y * config.dt
        kometa.z += kometa.v_z * config.dt

        ziemia.x += ziemia.v_x * config.dt
        ziemia.y += ziemia.v_y * config.dt
        ziemia.z += ziemia.v_z * config.dt

        # aktualizacja pozycji Ziemi
        Ziemia_o._offsets3d = (np.array([ziemia.x]), np.array([ziemia.y]), np.array([ziemia.z]))
        # aktualizacja pozycji komety
        Kometa._offsets3d = (np.array([kometa.x]), np.array([kometa.y]), np.array([kometa.z]))

        #odległość Ziemi od komety
        distane_zk = sqrt((kometa.x-ziemia.x)**2+(kometa.y-ziemia.y)**2+(kometa.z-ziemia.z)**2)
        wektor_zk = [kometa.x - ziemia.x, kometa.y - ziemia.y, kometa.z - ziemia.z]

        # zmien predkosc
        acceleration_x = - kometa.x * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5
        acceleration_y = - kometa.y * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5
        acceleration_z = - kometa.z * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5

        acceleration_x += wektor_zk[0] * config.G * config.M_z / (
                    wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5
        acceleration_y += wektor_zk[1] * config.G * config.M_z / (
                    wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5
        acceleration_z += wektor_zk[2] * config.G * config.M_z / (
                    wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5

        kometa.v_x += acceleration_x * config.dt
        kometa.v_y += acceleration_y * config.dt
        kometa.v_z += acceleration_z * config.dt

        acceleration_x_z = -ziemia.x * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        acceleration_y_z = -ziemia.y * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        acceleration_z_z = -ziemia.z * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        ziemia.v_x += acceleration_x_z * config.dt
        ziemia.v_y += acceleration_y_z * config.dt
        ziemia.v_z += acceleration_z_z * config.dt



        #rozpadnij cząstki
        pt.dissect(aktywnosc, distance, config.dt)

        # przesun czastke
        pt.particles[:, 1] += pt.particles[:, 4] * config.dt
        pt.particles[:, 2] += pt.particles[:, 5] * config.dt
        pt.particles[:, 3] += pt.particles[:, 6] * config.dt
        # zmien prędkosc
        mu = pt.particles[:, 7] *(0.89+0.54*aktywnosc)  #ciśnienie promieniowania
        acceleration_x = -pt.particles[:, 1]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)
        acceleration_y = -pt.particles[:, 2]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)
        acceleration_z = -pt.particles[:, 3]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)

        pt.particles[:, 4] += acceleration_x*config.dt
        pt.particles[:, 5] += acceleration_y*config.dt
        pt.particles[:, 6] += acceleration_z*config.dt