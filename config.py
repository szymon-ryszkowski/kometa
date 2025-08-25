from math import *
from datetime import date
import numpy as np
from mpl_toolkits.mplot3d import proj3d
# konwencja numeracji cząstek
# 0 - H2O
# 1 - H
# 2 - OH

# dane komety
# inputy zakomentowane są do czasu prezentacji posterów, na jej czas zakomentować dane i odkomentować inputy


name_k = ""  # nazwa obiektu
# print("podaj półoś wielką obiektu, powinna być w przedziale (0.1, 5) ")
# a_k = input()
# while a_k < 0.1 or a_k > 5 :
#     print("podano nieprawidłową wielkość, powinna być w przedziale (0.1, 5)")
#     a_k= input()
a_k = 1.5# półoś wielka obiektu [AU]
# print("podaj ekscentryczność(mimośród) orbity, pamiętaj, że orbita o:
# e = 0 jest kołowa
# 0 < e > 1 jest eliptyczna
# e = 1 jest paraboliczna
# e > 1 jest hiperboliczna ")
# e_k = input()
# while e_k < 0
#     print("podano niepoprawną(mniejszą od zera) ekscentryczność, proszę poprawić: ")
#     e_k = input()
#if e_k == 1:
#   print(Proszę podać odległość komety od Słońca w peryhelium: )
#   r_p = input()
r_p = 1
e_k =  0.7# mimośród oribty
i_k = 0  # inklinacja orbity [stopnie]
t_0_k = 0  # czas przejścia przez perycentrum [s]
arg_of_per_k = 0 # argument perycentrum[stopnie]
long_of_asc_z_k = 0  # długość węzła wstępującego[stopnie]
theta = np.pi * 1.5
if e_k>=1:
    theta = 3.5

# mechanizm zamiany danych dla orbity hiperbolicznej
if e_k >1:
    a_k = -a_k



t_k = 1  # czas w momencie początku symulacji [s]
ecc = 0 #ekcentryczność (uznaje że planety mają kołowe orbity)

# dane Ziemi
a_m = 1 # półoś wielka obiektu [AU]
e_m = 0.01671  # mimośród oribty
i_m = 0 # inklinacja orbity [stopnie]
t_0_m = 0  # czas przejścia przez perycentrum [s]
arg_of_per_m = 0  # argument perycentrum[stopnie]
long_of_asc_z_m = 0  # długość węzła wstępującego[stopnie]
t_m = 0  # czas w momencie początku symulacji [s]
M_z = 5.9722 * 10 ** 24 # Masa Ziemi
M0_z = 357.529 #Mean anomaly 1 stycznia 2000 r. [stopnie]

# dane Merkurego
a_mer = 0.39 # półoś wielka obiektu [AU]
e_mer = 0.2056  # mimośród oribty
i_mer = 0 # inklinacja orbity [stopnie]
t_0_mer = 0  # czas przejścia przez perycentrum [s]
arg_of_per_mer = 0  # argument perycentrum[stopnie]
long_of_asc_z_mer = 0  # długość węzła wstępującego[stopnie]
t_mer = 0  # czas w momencie początku symulacji [s]
M_mer = 3.3011 * 10 ** 23 # Masa Merkurego
M0_mer = 174.795 #Mean anomaly 1 stycznia 2000 r. [stopnie]

# dane Wenus
a_w = 0.7233 # półoś wielka obiektu [AU]
e_w = 0.0068  # mimośród oribty
i_w = 0 # inklinacja orbity [stopnie]
t_0_w = 0  # czas przejścia przez perycentrum [s]
arg_of_per_w = 0  # argument perycentrum[stopnie]
long_of_asc_z_w = 0  # długość węzła wstępującego[stopnie]
t_w = 0  # czas w momencie początku symulacji [s]
M_w = 4.867 * 10 ** 24 # Masa
M0_w = 50.416 #Mean anomaly 1 stycznia 2000 r. [stopnie]

# dane Marsa
a_ma = 1.524 # półoś wielka obiektu [AU]
e_ma = 0.0934  # mimośród oribty
i_ma = 0 # inklinacja orbity [stopnie]
t_0_ma = 0  # czas przejścia przez perycentrum [s]
arg_of_per_ma = 0  # argument perycentrum[stopnie]
long_of_asc_z_ma = 0  # długość węzła wstępującego[stopnie]
t_ma = 0  # czas w momencie początku symulacji [s]
M_ma = 6.4171 * 10 ** 23 # Masa
M0_ma = 19.373 #Mean anomaly 1 stycznia 2000 r. [stopnie]

# dane Jowisza
a_j = 5.20 # półoś wielka obiektu [AU]
e_j = 0.04839  # mimośród oribty
i_j = 0 # inklinacja orbity [stopnie]
t_0_j = 0  # czas przejścia przez perycentrum [s]
arg_of_per_j = 0  # argument perycentrum[stopnie]
long_of_asc_z_j = 0  # długość węzła wstępującego[stopnie]
t_j = 0  # czas w momencie początku symulacji [s]
M_j = 1.89819 * 10 ** 27 # Masa
M0_j = 20.02 #Mean anomaly 1 stycznia 2000 r. [stopnie]

# Stałe
M = 1.9891 * 10 ** 30  # Masa Słońca
G = 6.67 * 10 ** -11  # Stała Grawitacyjna
AU = 1.496*10**11
I_s = 1361  # Stała Słoneczna
mu = [0, 1, 0]  # sotsunek siły ciśnienia promieniowania do siły grawitacji

# Stałe do powstawania cząstek
absolute_ratio_H_2O = 1*10**28  # stała mówiąca raz na ile powstaje H2O na komecie w odlełości 1AU
scale = 1*10**33  # ile cząstek w rzeczywistości oznacza jedna cząstka u nas

#stała symulacji
dt = 10**3 # ile s odpowiada jeden krok
n_steps = 5*10**4 # ile kroków ma się wykonać

# daty
data_startowa = date(1947, 2, 14)  # pierwsza data w danych słońca
dzien_krok = (60*60*24)/dt  # ile kroków w dniu

#dane rozpadu
min_OH_H = 1.03E-05
max_OH_H = 1.76E-05
min_H = 7.26E-08
max_H = 1.72E-07
min_OH = 1.20E-05
max_OH = 1.37E-05
# rozpad wody do tlenu i dwóch wodorów
min_H20_O_H_H = 7.54E-07
max_H20_O_H_H = 1.91E-06

#kolory cząstek
color_map = {
    1: (0, 1, 1, 0.2),  # aqua z opacity 0.3
    0: (1, 0.64, 0),  # pomarańczowy
    2: (0.5, 0, 0, 1.0),  # ciemnoczerwony
}



