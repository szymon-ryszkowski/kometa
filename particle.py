#plik odpowiadający za cząsteczki

import numpy as np
from math import *
import config as conf
from config import scale, absolute_ratio_H_2O

particles = np.zeros((0, 7))
queue_H_2O = 0

def generate_velocity(v):
    velocity = [0, 0, 0]
    while velocity[0]**2 + velocity[1]**2 + velocity[2]**2 > v**2:
        angle = np.random.rand() * 2*pi #longnitude
        cos_theta = np.random.rand() * 2 - 1 # cos(latitude)
        velocity[2] = v*sqrt(1 - cos_theta**2) # składowa z
        velocity[1] = v*cos_theta*sin(angle) # składowa y
        velocity[0] = v*cos_theta*cos(angle) #składowa x
    return velocity
def create_particle(v, x, y, z):
    velocity = generate_velocity(v)
    particle = np.zeros((1, 7))
    particle[0][0] = 1
    particle[0][1] = x # x
    particle[0][2] = y # y
    particle[0][3] = z # z
    particle[0][4] = velocity[0] # v_x
    particle[0][5] = velocity[1] # v_y
    particle[0][6] = velocity[2] # v_z
    return particle

def calculate_sim_ratio(absolute_ratio, r, n):
    return absolute_ratio*(r/conf.AU)**n

def add_particles(v, x, y, z):
    global particles
    global queue_H_2O
    n = int((queue_H_2O - queue_H_2O % scale)/scale)
    queue_H_2O -= n*scale
    for i in range(n):
        particles = np.vstack([particles, create_particle(v, x, y, z)])