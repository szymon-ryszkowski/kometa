#plik odpowiadający za cząsteczki

import numpy as np
from math import *

particles = np.zeros((0, 7))

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
    particle = np.zeros(1, 7)
    particle[0] = "H_2O"
    particle[1] = x # x
    particle[2] = y # y
    particle[3] = z # z
    particle[4] = velocity[0] # v_x
    particle[5] = velocity[1] # v_y
    particle[6] = velocity[2] # v_z
    return particle