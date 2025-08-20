from math import *
from datetime import date

# konwencja numeracji cząstek
# 0 - H2O
# 1 - H
# 2 - OH

# dane komety
name_k = ""  # nazwa obiektu
a_k = 2.1  # półoś wielka obiektu [AU]
e_k = 0.7  # mimośród oribty
i_k = 0  # inklinacja orbity [stopnie]
t_0_k = 0  # czas przejścia przez perycentrum [s]
arg_of_per_k = 0  # argument perycentrum[stopnie]
long_of_asc_z_k = 0  # długość węzła wstępującego[stopnie]
r_m_k = 3.3  # odległość od Słońca na początku symulacji [AU]
t_k = -1  # czas w momencie początku symulacji [s]

# dane Ziemi
a_m = 1.496*10**11  # półoś wielka obiektu [m]
e_m = 0.01671  # mimośród oribty
i_m = 23.44  # inklinacja orbity [stopnie]
t_0_m = 1  # czas przejścia przez perycentrum [s]
arg_of_per_m = 1  # argument perycentrum[stopnie]
long_of_asc_z_m = 1  # długość węzła wstępującego[stopnie]
r_m_m = 1  # odległość od Słońca na początku symulacji [m]
t_m = 1  # czas w momencie początku symulacji [s]

# Stałe
M = 1.9891 * 10 ** 30  # Masa Słońca
G = 6.67 * 10 ** -11  # Stała Grawitacyjna
AU = 1.496*10**11
I_s = 1361  # Stała Słoneczna
mu = [0, 1, 0]  # sotsunek siły ciśnienia promieniowania do siły grawitacji

# Stałe do powstawania cząstek
absolute_ratio_H_2O = 1*10**28  # stała mówiąca raz na ile powstaje H2O na komecie w odlełości 1AU
scale = 1*10**31  # ile cząstek w rzeczywistości oznacza jedna cząstka u nas

#stała symulacji
dt = 3*10**2 # ile s odpowiada jeden krok
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
#0 = red
#1 = aqua
#2 = green