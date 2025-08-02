import config
import particle as pt
import celestial_body as cb

kometa = cb.celestial_body(2*config.AU, 0.2, 0, 0, 90, 90, 2*config.AU, -1, config.M, config.G)

for i in range(config.n_steps):
    ratio = pt.calculate_sim_ratio(config.absolute_ratio_H_2O, kometa.r, 2)
    pt.queue_H_2O += ratio*config.dt
    pt.add_particles(4, kometa.x, kometa.y, kometa.z)
print(pt.queue_H_2O)
print(400000000000.0 % 10**6)