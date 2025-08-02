import config
import particle as pt
import celestial_body as cb

kometa = cb.celestial_body(2*config.AU, 0.2, 0, 0, 90, 90, 2*config.AU, -1, config.M, config.G)

for i in range(config.n_steps):
    #utwórz cząstki
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, kometa.r, 2)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(4, kometa.x, kometa.y, kometa.z)

    #przesun komete i zmien predkosc
    kometa.x += kometa.v_x*config.dt
    kometa.y += kometa.v_y*config.dt
    kometa.z += kometa.v_z*config.dt
    acceleration_x = -kometa.x*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_y = -kometa.y*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    acceleration_z = -kometa.z*config.G*config.M/(kometa.x**2 + kometa.y**2 + kometa.z**2)**1.5
    kometa.v_x += acceleration_x*config.dt
    kometa.v_y += acceleration_y*config.dt
    kometa.v_z += acceleration_z*config.dt
