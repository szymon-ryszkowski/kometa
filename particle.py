#plik odpowiadający za cząsteczki

import numpy as np
from math import *
import config as config

#tablica particles i kolejka do generowania H2O
particles = np.zeros((0, 8))
queue_H_2O = 0

def generate_velocity(v):
    velocity = [0, 0, 0]
    angle = np.random.uniform(0, 1) * 2*pi #longnitude
    sin_theta = np.random.uniform(0, 1) * 2 - 1 # cos(latitude)
    cos_theta = sqrt(1 - sin_theta**2)
    velocity[2] = v*sin_theta # składowa z
    velocity[1] = v*cos_theta*sin(angle) # składowa y
    velocity[0] = v*cos_theta*cos(angle) #składowa x
    return velocity


#dodanie wiersza do czastek
def create_particle(v, x, y, z, v_x, v_y, v_z):
    velocity = generate_velocity(v)
    particle = np.zeros((1, 8))
    particle[0][0] = 0 # typ według config.py
    particle[0][1] = x # x
    particle[0][2] = y # y
    particle[0][3] = z # z
    particle[0][4] = velocity[0] + v_x# v_x
    particle[0][5] = velocity[1] + v_y# v_y
    particle[0][6] = velocity[2] + v_z# v_z
    particle[0][7] = config.mu[0] # mu
    return particle


#przeliczanie rozpadania sie czastek
def calculate_sim_ratio(absolute_ratio, r, n):
    return absolute_ratio*(r/config.AU)**n

#dodanie czastek na podstawie kolejki
def add_particles(v, x, y, z, v_x, v_y, v_z):
    global particles
    global queue_H_2O
    n = int((queue_H_2O - queue_H_2O % config.scale)/config.scale)
    queue_H_2O -= n*config.scale
    for i in range(n):
        particles = np.vstack([particles, create_particle(v, x, y, z, v_x, v_y, v_z)])


#rozpadanie(przemiana jak na razie) cząstek
def dissect(distance, dt):
    global particles
#rozpad wodoru na protony i elektrony
    mask_h = particles[:, 0] == 1
    #chance = 7.26e-8 * dt
    #mask = np.random.rand(particles[mask_h].shape[0]) > chance
    #particles = np.vstack([particles[~mask_h], particles[mask_h][mask]])

    # rozpad OH do wodoru
    mask_oh = particles[:, 0] == 2
    chance = 1.2e-5 * dt
    mask = np.random.rand(particles[mask_oh].shape[0]) <= chance
    particles[mask_oh][mask, 0] = 1

#rozpad wody na OH i H
    mask_h2o = particles[:, 0] == 0
    chance = 1 - np.exp(-1.03e-5 * dt)
    mask = np.random.rand(particles[mask_h2o].shape[0]) < chance
    print(mask)
    nowe_particles = particles[mask_h2o][mask]
    duplikaty = np.repeat(nowe_particles, 2, axis=0)
    duplikaty[::2,0]=1
    duplikaty[1::2, 0] = 2
    particles = np.concatenate([particles[~mask_h2o], particles[mask_h2o][~mask], duplikaty], axis=0)


    particles[:, 7] = np.array(config.mu)[particles[:, 0].astype(int)]

def count_particles():
    global particles
    mask_h20 = particles[:,0] == 0
    mask_h = particles[:,0] == 1
    mask_oh = particles [:, 0] == 2
    print("n H_20: ",len(particles[mask_h20]), ", n H: ", len(particles[mask_h]), ", n OH: ", len(particles[mask_oh]))
