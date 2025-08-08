#plik odpowiadający za cząsteczki

import numpy as np
from math import *
import config as config
from config import scale, absolute_ratio_H_2O

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
    particle[0][0] = 0
    particle[0][1] = x # x
    particle[0][2] = y # y
    particle[0][3] = z # z
    particle[0][4] = velocity[0] + v_x# v_x
    particle[0][5] = velocity[1] + v_y# v_y
    particle[0][6] = velocity[2] + v_z# v_z
    particle[0][7] = config.mu[0]
    return particle
create_particle(4, 1, 1, 1, 4, 4, 4)

#przeliczanie rozpadania sie czastek
def calculate_sim_ratio(absolute_ratio, r, n):
    return absolute_ratio*(r/config.AU)**n

#dodanie czastek na podstawie kolejki
def add_particles(v, x, y, z, v_x, v_y, v_z):
    global particles
    global queue_H_2O
    n = int((queue_H_2O - queue_H_2O % scale)/scale)
    queue_H_2O -= n*scale
    for i in range(n):
        particles = np.vstack([particles, create_particle(v, x, y, z, v_x, v_y, v_z)])

def dissect(dissection_rate, dt):
    global particles
    chance = 1 - np.exp(-dissection_rate * dt)
    mask = np.random.rand(particles.shape[0]) < chance
    particles[mask, 0] = 1
    particles[mask, 7] = np.array(config.mu)[particles[mask, 0].astype(int)]