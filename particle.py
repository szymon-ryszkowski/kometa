# plik odpowiadający za cząsteczki
import random

import numpy as np
from math import *
import config as config

# tablica particles i kolejka do generowania H2O
particles = np.zeros((0, 8))
queue_H_2O = 0


def generate_velocity(v):
    velocity = [0, 0, 0]
    angle = np.random.uniform(0, 1) * 2*pi  # longnitude
    sin_theta = np.random.uniform(0, 1) * 2 - 1  # cos(latitude)
    cos_theta = sqrt(1 - sin_theta**2)
    velocity[2] = v*sin_theta  # składowa z
    velocity[1] = v*cos_theta*sin(angle)  # składowa y
    velocity[0] = v*cos_theta*cos(angle)  # składowa x
    return velocity

def generate_velocity2(l_czastek, velocities, probabilities):
    velocity = [0, 0, 0]
    probabilities = np.array(probabilities, dtype=float)
    probabilities /= probabilities.sum()
    v = np.random.choice(velocities, size = l_czastek, p=probabilities)
    angle = np.random.uniform(0, 2 * pi, size=l_czastek)
    sin_theta = np.random.uniform(-1, 1, size=l_czastek)
    cos_theta = np.sqrt(1 - sin_theta**2)
    velocity[2] = sin_theta  # składowa z
    velocity[1] = cos_theta*np.sin(angle)  # składowa y
    velocity[0] = cos_theta*np.cos(angle)  # składowa x
    velocity = np.vstack((velocity[0], velocity[1], velocity[2])).T * v[:, None]
    return velocity


# dodanie wiersza do czastek
def create_particle(v, x, y, z, v_x, v_y, v_z):
    n = random.random()
    velocity = generate_velocity(v)
    particle = np.zeros((1, 8))
    particle[0][0] = 0  # typ według config.py
    particle[0][1] = x + velocity[0]*n*config.dt  # x, przesuwa o losowy czas, żeby pokazywało generację cząstek w
    # czasie, a nie skokami
    particle[0][2] = y + velocity[1]*n*config.dt  # y
    particle[0][3] = z + velocity[2]*n*config.dt # z
    particle[0][4] = velocity[0] + v_x  # v_x
    particle[0][5] = velocity[1] + v_y  # v_y
    particle[0][6] = velocity[2] + v_z  # v_z
    particle[0][7] = config.mu[0]  # mu
    return particle


# przeliczanie rozpadania sie czastek
def calculate_sim_ratio(absolute_ratio, r, n):
    return absolute_ratio*(r/config.AU)**n

# dodanie czastek na podstawie kolejki


def add_particles(v, x, y, z, v_x, v_y, v_z):
    global particles
    global queue_H_2O
    n = int((queue_H_2O - queue_H_2O % config.scale)/config.scale)
    queue_H_2O -= n*config.scale
    for i in range(n):
        particles = np.vstack([particles, create_particle(v, x, y, z, v_x, v_y, v_z)])

def define_activity(y,P,Q):
    delta = Q - P
    return P + delta * y

#rozpadanie(przemiana jak na razie) cząstek
def dissect(aktywnosc, odlegosc, dt):
    global particles
    au2 = (odlegosc/config.AU)**-2

# rozpad wodoru na protony i elektrony
    mask_h = particles[:, 0] == 1
    chance = 1 - np.exp(-define_activity(aktywnosc, config.max_H ,config.min_H) * dt * au2)
    mask = np.random.rand(particles[mask_h].shape[0]) > chance
    particles = np.vstack([particles[~mask_h], particles[mask_h][mask]])

    # rozpad OH do wodoru
    mask_oh = particles[:, 0] == 2
    chance = 1 - np.exp(-define_activity(aktywnosc, config.max_OH ,config.min_OH) * dt * au2)
    mask = np.random.rand(particles[mask_oh].shape[0]) <= chance
    particles[mask_oh][mask, 0] = 1
    particles[mask_oh][mask, 4:7] = generate_velocity2(particles[mask_oh][mask].shape[0],[7940, 10990, 26300, 22730, 23160, 23610, 21830, 22350, 22080, 21570, 21310, 21070, 17080, 24090, 24570, 25020, 20810, 26770, 26350, 25480], [4.05E-06, 5.00E-07, 4.65E-07, 2.49E-07, 2.21E-07, 1.32E-07, 1.23E-07, 1.18E-07, 1.18E-07, 1.13E-07, 9.62E-08, 6.46E-08, 5.00E-08, 4.70E-08, 3.99E-08, 2.59E-08, 2.25E-08, 2.05E-08, 2.05E-08, 1.88E-08])

    # rozpad wody na O, H i H
    mask_h2o = particles[:, 0] == 0
    chance = define_activity(aktywnosc, config.min_H20_O_H_H, config.max_H20_O_H_H) * dt * au2

    mask = np.random.rand(particles[mask_h2o].shape[0]) < chance
    nowe_particles = particles[mask_h2o][mask]
    duplikaty = np.repeat(nowe_particles, 2, axis=0)
    duplikaty[::2, 0] = 1
    duplikaty[1::2, 0] = 1
    duplikaty[:, 4:7] += generate_velocity2(duplikaty.shape[0],[7400, 8030, 1620, 5720, 7140, 16180, 6200, 17530, 6750, 12380, 4510, 15930, 5180, 2680, 3790, 8670, 7590, 15630, 13900, 17890], [7.80E-07, 1.16E-08, 1.06E-08, 7.92E-09, 6.79E-09, 6.13E-09, 3.57E-09, 3.50E-09, 3.43E-09, 3.29E-09, 3.15E-09, 2.93E-09, 2.72E-09, 2.60E-09, 2.31E-09, 2.22E-09, 2.18E-09, 1.70E-09, 1.48E-09, 1.01E-09])
    particles = np.concatenate([particles[~mask_h2o], particles[mask_h2o][~mask], duplikaty], axis=0)
# rozpad wody na OH i H
    mask_h2o = particles[:, 0] == 0
    chance = define_activity(aktywnosc, config.min_OH_H ,config.max_OH_H) * dt * au2
    mask = np.random.rand(particles[mask_h2o].shape[0]) < chance
    nowe_particles = particles[mask_h2o][mask]
    duplikaty = np.repeat(nowe_particles, 2, axis=0)
    duplikaty[::2, 0] = 1
    duplikaty[1::2, 0] = 2
    duplikaty[::2, 4:7] += generate_velocity2([duplikaty[::2].shape[0]],[7200,19690,20200,5000,20730,18650,18940,19250,18350,18050,21810,21280,17740,22300,17430,22800,27420,24070,19430,17120],[4.53E-06,8.03E-07,7.24E-07,5.20E-07,5.18E-07,4.84E-07,4.68E-07,4.22E-07,4.00E-07,2.85E-07,2.43E-07,2.22E-07,1.96E-07,1.46E-07,1.46E-07,8.46E-08,7.62E-08,7.56E-08,6.97E-08,6.05E-08])
    duplikaty[1::2, 4:7] += generate_velocity2(duplikaty[1::2].shape[0], [1011.76, 1158.24, 1188.24, 294.12, 1219.41, 1097.06, 1114.12, 1132.35, 1079.41, 1061.76, 1282.94, 1251.76, 1043.53, 1311.76, 1025.29, 1341.18, 1612.94, 1415.88, 1142.94, 1007.06],[4.53E-06,8.03E-07,7.24E-07,5.20E-07,5.18E-07,4.84E-07,4.68E-07,4.22E-07,4.00E-07,2.85E-07,2.43E-07,2.22E-07,1.96E-07,1.46E-07,1.46E-07,8.46E-08,7.62E-08,7.56E-08,6.97E-08,6.05E-08])
    particles = np.concatenate([particles[~mask_h2o], particles[mask_h2o][~mask], duplikaty], axis=0)
    print(chance)


    particles[:, 7] = np.array(config.mu)[particles[:, 0].astype(int)]


def count_particles():
    global particles
    mask_h20 = particles[:, 0] == 0
    mask_h = particles[:, 0] == 1
    mask_oh = particles[:, 0] == 2
    print("n H_20: ", len(particles[mask_h20]), ", n H: ", len(particles[mask_h]), ", n OH: ", len(particles[mask_oh]))
