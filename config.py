from math import *

#dane komety
name_k = "" # nazwa obiektu

a_k = 1# półoś wielka obiektu [m]

e_k = 1# mimośród oribty

i_k = 1# inklinacja orbity [stopnie]

t_0_k = 1 # czas przejścia przez perycentrum [s]

arg_of_per_k = 1#argument perycentrum[stopnie]

long_of_asc_z_k =  1# długość węzła wstępującego[stopnie]

r_m_k = 1# odległość od Słońca na początku symulacji [m]

t_k = 1# czas w momencie początku symulacji [s]

#dane Ziemi

a_m = 1.496*10**11  # półoś wielka obiektu [m]

e_m = 0.01671 # mimośród oribty

i_m = 23.44# inklinacja orbity [stopnie]

t_0_m = 1 # czas przejścia przez perycentrum [s]

arg_of_per_m = 1#argument perycentrum[stopnie]

long_of_asc_z_m =  1# długość węzła wstępującego[stopnie]

r_m_m = 1# odległość od Słońca na początku symulacji [m]

t_m = 1# czas w momencie początku symulacji [s]

#Stałe

M = 1.9891 *10**30 # Masa Słońca

G = 6.67 *10**-11 # Stała Grawitacyjna

AU = 1.496*10**11

# Stałe do powstawania cząstek

absolute_ratio_H_2O = 10**9 # stała mówiąca raz na ile powstaje H2O na komecie w odlełości 1AU

scale = 1*10**12 # ile cząstek w rzeczywistości oznacza jedna cząstka u nas

#stała symulacji

dt = 10**1 # ile s odpowiada jeden krok

n_steps = 10**4 # ile kroków ma się wykonać