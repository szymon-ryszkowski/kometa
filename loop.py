import config
import particle as pt
import celestial_body as cb
import matplotlib.pyplot as plt
import numpy as np
import Sun
from datetime import date
from datetime import timedelta
from math import *
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
# deklaracja komety
kometa = (
    cb.Celestial_Body(config.a_k*config.AU, config.e_k, config.i_k, config.t_0_k, config.arg_of_per_k,
                      config.long_of_asc_z_k, config.theta, config.t_m, config.M, config.G,config.r_p))
#głupi fix
kometa.y = - kometa.y
kometa.v_x = -kometa.v_x
ziemia = (
    cb.Celestial_Body(config.a_m*config.AU, config.e_m, config.i_m, config.t_0_m, config.arg_of_per_m,
                     config.long_of_asc_z_m, 1, config.t_m, config.M, config.G,0))

merkury = (
    cb.Celestial_Body(config.a_mer*config.AU, config.e_mer, config.i_mer, config.t_0_mer, config.arg_of_per_mer,
                     config.long_of_asc_z_mer, 1, config.t_mer, config.M, config.G,0))

wenus = (
    cb.Celestial_Body(config.a_w*config.AU, config.e_w, config.i_w, config.t_0_w, config.arg_of_per_w,
                     config.long_of_asc_z_w, 1, config.t_w, config.M, config.G,0))

mars = (
    cb.Celestial_Body(config.a_ma*config.AU, config.e_ma, config.i_ma, config.t_0_ma, config.arg_of_per_ma,
                     config.long_of_asc_z_ma, 1, config.t_ma, config.M, config.G,0))

jowisz = (
    cb.Celestial_Body(config.a_j*config.AU, config.e_j, config.i_j, config.t_0_j, config.arg_of_per_j,
                     config.long_of_asc_z_j, 1, config.t_j, config.M, config.G,0))


print("podaj rok w zakresie od 1948 do 2024- ")

while True:
    rok_str = input()
    # sprawdzenie, czy wpisano cokolwiek i czy to liczba
    if not rok_str.isdigit():
        print("podano nieprawidłową datę")
        continue
    rok = int(rok_str)
    # sprawdzenie zakresu
    if 1948 <= rok <= 2024:
        break
    else:
        print("podano nieprawidłową datę")

print("podaj miesiąc - ")
while True:
    miesiac_str = input()
    # sprawdzenie, czy wpisano cokolwiek i czy to liczba
    if not miesiac_str.isdigit():
        print("podano nieprawidłową datę")
        continue
    miesiac = int(miesiac_str)
    # sprawdzenie zakresu
    if 1 <= miesiac <=12:
        break
    else:
        print("podano nieprawidłową datę")

print("Podaj dzień: ")

while True:
    dzien_str = input()  # pobieramy jako string

    if not dzien_str.isdigit():  # sprawdzenie czy nie pusty i same cyfry
        print("podano nieprawidłową datę")
        continue

    dzien = int(dzien_str)

    # sprawdzenie poprawności dnia w zależności od miesiąca i roku
    if dzien < 1:
        print("podano nieprawidłową datę")
        continue

    if miesiac == 2:
        if (rok % 4 == 0 and dzien > 29) or (rok % 4 != 0 and dzien > 28):
            print("podano nieprawidłową datę")
            continue
    elif miesiac in [4, 6, 9, 11] and dzien > 30:
        print("podano nieprawidłową datę")
        continue
    elif dzien > 31:
        print("podano nieprawidłową datę")
        continue

    break

dany_dzien = date(rok, miesiac, dzien)
print("wybierz rodzaj wykresu: ")
typ_wykresu = int(input())
# animacja 3d przygotowanie wykresu (czerwone cząstki - H2O, turkusowe - typu 1)
fig = plt.figure(figsize=(14.4, 8.1), dpi=100)
ax = fig.add_subplot(111, projection='3d')

#elementy wykresu
ax.scatter(0, 0, 0, color='yellow', s=100, label='Słońce')  # Pozycja Słońca w środku
Ziemia_o = ax.scatter(ziemia.x, ziemia.y, ziemia.z, color='darkblue', s=10, label='Ziemia')
Merkury_o = ax.scatter(merkury.x, merkury.y, merkury.z, color='grey', s=3, label='Merkury')
Wenus_o = ax.scatter(wenus.x, wenus.y, wenus.z, color='grey', s=10, label='Wenus')
Mars_o = ax.scatter(mars.x, mars.y, mars.z, color='grey', s=7, label='Mars')
Jowisz_o = ax.scatter(jowisz.x, jowisz.y, jowisz.z, color='grey', s=20, label='Jowisz')
traj_Ziemia, = ax.plot([], [],[], color='blue', linewidth=.5)
traj_Merkury, = ax.plot([], [],[], color='grey', linewidth=.5)
traj_Wenus, = ax.plot([], [],[], color='grey', linewidth=.5)
traj_Mars, = ax.plot([], [],[], color='grey', linewidth=.5)
traj_Jowisz, = ax.plot([], [],[], color='grey', linewidth=.5)
Kometa = ax.scatter(kometa.x, kometa.y, kometa.z, color='red', s=5, label='Kometa')
sc = ax.scatter([], [], [], color=config.color_map[1], s=1, label='Cząstki H' )
sc = ax.scatter([], [], [], color=config.color_map[0], s=1, label='Cząstki H20')
sc = ax.scatter([], [], [], color=config.color_map[2], s=1, label='Cząstki OH')
traj_line, = ax.plot([], [], [], color='red', linewidth = .5)

ax.set_xlabel('X [AU]')
ax.set_ylabel('Y [AU]')
ax.set_zlabel('Z [AU]')
ax.set_title('Trajektoria komety w 3D')

#elementy legendy, potrzebne do skalowania
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Kometa',
           markerfacecolor='red', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Cząstki H',
           markerfacecolor=config.color_map[1], markersize=6),
    Line2D([0], [0], marker='o', color='w', label='Cząstki H2O',
           markerfacecolor=config.color_map[0], markersize=6),
    Line2D([0], [0], marker='o', color='w', label='Cząstki OH',
           markerfacecolor=config.color_map[2], markersize=6)
]

# Legenda - skalowanie
ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=12, title='Legenda')
plt.tight_layout()
plt.subplots_adjust(right=0.8)
plt.ion()  # Włącza interaktywne rysowanie
plt.show()
sun_label    = ax.text2D(0, 0, "Słońce", color="orange")
earth_label  = ax.text2D(0, 0, "Ziemia",fontsize=7, color="blue")
merkury_label  = ax.text2D(0, 0, "Merkury",fontsize=7, color="darkgrey")
wenus_label  = ax.text2D(0, 0, "Wenus",fontsize=7, color="darkgrey")
mars_label  = ax.text2D(0, 0, "Mars",fontsize=7, color="darkgrey")
jowisz_label  = ax.text2D(0, 0, "Jowisz",fontsize=7, color="darkgrey")

def update_labels():
    # projekcja 3D -> 2D dla Słońca
    x2, y2, _ = proj3d.proj_transform(0, 0, 0, ax.get_proj())
    sun_label.set_position((x2 + 0.001, y2 + 0.002))
    # projekcja 3D -> 2D dla Ziemi
    x2, y2, _ = proj3d.proj_transform(ziemia.x, ziemia.y, ziemia.z, ax.get_proj())
    earth_label.set_position((x2 + 0.001, y2 + 0.002))
    # projekcja 3D -> 2D dla Merkurego
    x2, y2, _ = proj3d.proj_transform(merkury.x, merkury.y, merkury.z, ax.get_proj())
    merkury_label.set_position((x2 + 0.001, y2 + 0.002))
    # projekcja 3D -> 2D dla Wenus
    x2, y2, _ = proj3d.proj_transform(wenus.x, wenus.y, wenus.z, ax.get_proj())
    wenus_label.set_position((x2 + 0.001, y2 + 0.002))
    # projekcja 3D -> 2D dla Marsa
    x2, y2, _ = proj3d.proj_transform(mars.x, mars.y, mars.z, ax.get_proj())
    mars_label.set_position((x2 + 0.001, y2 + 0.002))
    # projekcja 3D -> 2D dla Jowisza
    x2, y2, _ = proj3d.proj_transform(jowisz.x, jowisz.y, jowisz.z, ax.get_proj())
    jowisz_label.set_position((x2 + 0.001, y2 + 0.002))


# zapis trajektorii komety
x_traj = []
y_traj = []
z_traj = []

x_traj_z = []
y_traj_z = []
z_traj_z = []

x_traj_mer = []
y_traj_mer = []
z_traj_mer = []

x_traj_w = []
y_traj_w = []
z_traj_w = []

x_traj_ma = []
y_traj_ma = []
z_traj_ma = []

x_traj_j = []
y_traj_j = []
z_traj_j = []

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
        distance = sqrt(kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2)
        distances.append(distance)
        # animacja 3d
        if i % 50 == 0 and typ_wykresu==1:
            time_text.set_text(aktualna_data)

            traj_line.set_data(x_traj, y_traj)
            traj_line.set_3d_properties(z_traj)

            traj_Ziemia.set_data(x_traj_z, y_traj_z)
            traj_Ziemia.set_3d_properties(z_traj_z)

            traj_Merkury.set_data(x_traj_mer, y_traj_mer)
            traj_Merkury.set_3d_properties(z_traj_mer)

            traj_Wenus.set_data(x_traj_w, y_traj_w)
            traj_Wenus.set_3d_properties(z_traj_w)

            traj_Mars.set_data(x_traj_ma, y_traj_ma)
            (traj_Mars.set_3d_properties(z_traj_ma))

            traj_Jowisz.set_data(x_traj_j, y_traj_j)
            traj_Jowisz.set_3d_properties(z_traj_j)

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

        x_traj_mer.append(merkury.x)
        y_traj_mer.append(merkury.y)
        z_traj_mer.append(merkury.z)

        x_traj_w.append(wenus.x)
        y_traj_w.append(wenus.y)
        z_traj_w.append(wenus.z)

        x_traj_ma.append(mars.x)
        y_traj_ma.append(mars.y)
        z_traj_ma.append(mars.z)

        x_traj_j.append(jowisz.x)
        y_traj_j.append(jowisz.y)
        z_traj_j.append(jowisz.z)

        # utwórz cząstki
        ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, sqrt(kometa.x**2 + kometa.y**2 + kometa.z**2), -3)
        pt.queue_H_2O += ratio*config.dt
        pt.add_particles(1000, kometa.x, kometa.y, kometa.z, kometa.v_x, kometa.v_y, kometa.v_z)

        # przesun komete i planety
        kometa.x += kometa.v_x * config.dt
        kometa.y += kometa.v_y * config.dt
        kometa.z += kometa.v_z * config.dt

        ziemia.x += ziemia.v_x * config.dt
        ziemia.y += ziemia.v_y * config.dt
        ziemia.z += ziemia.v_z * config.dt

        merkury.x += merkury.v_x * config.dt
        merkury.y += merkury.v_y * config.dt
        merkury.z += merkury.v_z * config.dt

        wenus.x += wenus.v_x * config.dt
        wenus.y += wenus.v_y * config.dt
        wenus.z += wenus.v_z * config.dt

        mars.x += mars.v_x * config.dt
        mars.y += mars.v_y * config.dt
        mars.z += mars.v_z * config.dt

        jowisz.x += jowisz.v_x * config.dt
        jowisz.y += jowisz.v_y * config.dt
        jowisz.z += jowisz.v_z * config.dt

        # aktualizacja pozycji Ziemi
        Ziemia_o._offsets3d = (np.array([ziemia.x]), np.array([ziemia.y]), np.array([ziemia.z]))

        Merkury_o._offsets3d = (np.array([merkury.x]), np.array([merkury.y]), np.array([merkury.z]))

        Wenus_o._offsets3d = (np.array([wenus.x]), np.array([wenus.y]), np.array([wenus.z]))

        Mars_o._offsets3d = (np.array([mars.x]), np.array([mars.y]), np.array([mars.z]))

        Jowisz_o._offsets3d = (np.array([jowisz.x]), np.array([jowisz.y]), np.array([jowisz.z]))
        # aktualizacja pozycji komety
        Kometa._offsets3d = (np.array([kometa.x]), np.array([kometa.y]), np.array([kometa.z]))

        #odległość Ziemi od komety
        #distane_zk = sqrt((kometa.x-ziemia.x)**2+(kometa.y-ziemia.y)**2+(kometa.z-ziemia.z)**2)
        wektor_zk = [kometa.x - ziemia.x, kometa.y - ziemia.y, kometa.z - ziemia.z]

        # zmien predkosc
        acceleration_x = - kometa.x * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5
        acceleration_y = - kometa.y * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5
        acceleration_z = - kometa.z * config.G * config.M / (kometa.x ** 2 + kometa.y ** 2 + kometa.z ** 2) ** 1.5
            # kometa ziemia
        acceleration_x += wektor_zk[0] * config.G * config.M_z / (wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5
        acceleration_y += wektor_zk[1] * config.G * config.M_z / (wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5
        acceleration_z += wektor_zk[2] * config.G * config.M_z / (wektor_zk[0] ** 2 + wektor_zk[1] ** 2 + wektor_zk[2] ** 2) ** 1.5
            # kometa jowisz
        wektor_jk = [kometa.x - jowisz.x, kometa.y - jowisz.y, kometa.z - jowisz.z]

        acceleration_x += -wektor_jk[0] * config.G * config.M_j / (wektor_jk[0] ** 2 + wektor_jk[1] ** 2 + wektor_jk[2] ** 2) ** 1.5
        acceleration_y += -wektor_jk[1] * config.G * config.M_j / (wektor_jk[0] ** 2 + wektor_jk[1] ** 2 + wektor_jk[2] ** 2) ** 1.5
        acceleration_z += -wektor_jk[2] * config.G * config.M_j / (wektor_jk[0] ** 2 + wektor_jk[1] ** 2 + wektor_jk[2] ** 2) ** 1.5

        kometa.v_x += acceleration_x * config.dt
        kometa.v_y += acceleration_y * config.dt
        kometa.v_z += acceleration_z * config.dt

        # predkosc ziemi
        acceleration_x_z = -ziemia.x * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        acceleration_y_z = -ziemia.y * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        acceleration_z_z = -ziemia.z * config.G * config.M / (ziemia.x ** 2 + ziemia.y ** 2 + ziemia.z ** 2) ** 1.5
        ziemia.v_x += acceleration_x_z * config.dt
        ziemia.v_y += acceleration_y_z * config.dt
        ziemia.v_z += acceleration_z_z * config.dt

        acceleration_x_me = -merkury.x * config.G * config.M / (merkury.x ** 2 + merkury.y ** 2 + merkury.z ** 2) ** 1.5
        acceleration_y_me = -merkury.y * config.G * config.M / (merkury.x ** 2 + merkury.y ** 2 + merkury.z ** 2) ** 1.5
        acceleration_z_me = -merkury.z * config.G * config.M / (merkury.x ** 2 + merkury.y ** 2 + merkury.z ** 2) ** 1.5
        merkury.v_x += acceleration_x_me * config.dt
        merkury.v_y += acceleration_y_me * config.dt
        merkury.v_z += acceleration_z_me * config.dt

        acceleration_x_w = -wenus.x * config.G * config.M / (wenus.x ** 2 + wenus.y ** 2 + wenus.z ** 2) ** 1.5
        acceleration_y_w = -wenus.y * config.G * config.M / (wenus.x ** 2 + wenus.y ** 2 + wenus.z ** 2) ** 1.5
        acceleration_z_w = -wenus.z * config.G * config.M / (wenus.x ** 2 + wenus.y ** 2 + wenus.z ** 2) ** 1.5
        wenus.v_x += acceleration_x_w * config.dt
        wenus.v_y += acceleration_y_w * config.dt
        wenus.v_z += acceleration_z_w * config.dt


        acceleration_x_ma = -mars.x * config.G * config.M / (mars.x ** 2 + mars.y ** 2 + mars.z ** 2) ** 1.5
        acceleration_y_ma = -mars.y * config.G * config.M / (mars.x ** 2 + mars.y ** 2 + mars.z ** 2) ** 1.5
        acceleration_z_ma = -mars.z * config.G * config.M / (mars.x ** 2 + mars.y ** 2 + mars.z ** 2) ** 1.5
        mars.v_x += acceleration_x_ma * config.dt
        mars.v_y += acceleration_y_ma * config.dt
        mars.v_z += acceleration_z_ma * config.dt

        acceleration_x_j = -jowisz.x * config.G * config.M / (jowisz.x ** 2 + jowisz.y ** 2 + jowisz.z ** 2) ** 1.5
        acceleration_y_j = -jowisz.y * config.G * config.M / (jowisz.x ** 2 + jowisz.y ** 2 + jowisz.z ** 2) ** 1.5
        acceleration_z_j = -jowisz.z * config.G * config.M / (jowisz.x ** 2 + jowisz.y ** 2 + jowisz.z ** 2) ** 1.5
        jowisz.v_x += acceleration_x_j * config.dt
        jowisz.v_y += acceleration_y_j * config.dt
        jowisz.v_z += acceleration_z_j * config.dt

        #rozpadnij cząstki
        pt.dissect(aktywnosc, distance, config.dt)

        #zaktualizuj podpisy
        update_labels()
        # przesun czastke
        pt.particles[:, 1] += pt.particles[:, 4] * config.dt
        pt.particles[:, 2] += pt.particles[:, 5] * config.dt
        pt.particles[:, 3] += pt.particles[:, 6] * config.dt
        # zmien prędkosc
        mu = pt.particles[:, 7] *(0.89+0.54*aktywnosc)  #ciśnienie promieniowania
        acceleration_x = -pt.particles[:, 1]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)
        acceleration_y = -pt.particles[:, 2]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)
        acceleration_z = -pt.particles[:, 3]*config.G*config.M/(pt.particles[:, 1]**2 + pt.particles[:, 2]**2 + pt.particles[:, 3])**1.5*(1 - mu)
            #cząsteczki - Ziemia
        wektor_z_cz = [pt.particles[:,1] - ziemia.x, pt.particles[:,2] - ziemia.y, pt.particles[:,3] - ziemia.z] # wektor ziemia cząstka
        acceleration_x += -wektor_z_cz[0] *config.G*config.M_z/np.maximum(wektor_z_cz[0]**2 + wektor_z_cz[1]**2 + wektor_z_cz[2], 100)**1.5
        acceleration_y += -wektor_z_cz[1] *config.G*config.M_z/np.maximum(wektor_z_cz[0]**2 + wektor_z_cz[1]**2 + wektor_z_cz[2], 100)**1.5
        acceleration_z += -wektor_z_cz[2] *config.G*config.M_z/np.maximum(wektor_z_cz[0]**2 + wektor_z_cz[1]**2 + wektor_z_cz[2], 100)**1.5
            #cząsteczki - Jowisz
        wektor_j_cz = [pt.particles[:,1] - jowisz.x, pt.particles[:,2] - jowisz.y, pt.particles[:,3] - jowisz.z]
        acceleration_x += -wektor_j_cz[0] *config.G*config.M_j/np.maximum(wektor_j_cz[0]**2 + wektor_j_cz[1]**2 + wektor_j_cz[2], 100)**1.5
        acceleration_y += -wektor_j_cz[1] *config.G*config.M_j/np.maximum(wektor_j_cz[0]**2 + wektor_j_cz[1]**2 + wektor_j_cz[2], 100)**1.5
        acceleration_z += -wektor_j_cz[2] *config.G*config.M_j/np.maximum(wektor_j_cz[0]**2 + wektor_j_cz[1]**2 + wektor_j_cz[2], 100)**1.5

        pt.particles[:, 4] += acceleration_x*config.dt
        pt.particles[:, 5] += acceleration_y*config.dt
        pt.particles[:, 6] += acceleration_z*config.dt
        print(distance/config.AU)