from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
scene.set_background_color((0, 0, 0))

@ti.func
def rotate(alpha):
    return ti.Matrix([[ti.cos(alpha), -ti.sin(alpha)], [ti.sin(alpha), ti.cos(alpha)]])

@ti.func
def in_magatama(i, j, origin, radius, alpha):
    ans = 0
    X = rotate(-alpha) @ (vec2(i, j) - origin) / radius 
    if X.norm() > 1 or (X - (-0.5, 0)).norm() <= 0.5: 
        pass
    elif X[1] > 0 or (X - (0.5, 0)).norm() <= 0.5:
        # scene.set_voxel(vec3(i + int(origin[0]), 0, j + int(origin[1])), 2, vec3(0.8, 0.1, 0.8))
        ans = 1
    return ans

@ti.func
def magatama(origin, radius, alpha):
    for i in range(-radius - 1, radius + 1):
        for j in range(-radius - 1, radius + 1):
            X = rotate(-alpha) @ vec2(i, j) / radius 
            if X.norm() > 1 or (X - (-0.5, 0)).norm() <= 0.5: 
                continue
            if X[1] > 0 or (X - (0.5, 0)).norm() <= 0.5:
                scene.set_voxel(vec3(i + int(origin[0]), 0, j + int(origin[1])), 2, vec3(0.8, 0.1, 0.8))

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    # scene.set_voxel(vec3 0, 0, 0), 2, vec3(0.9, 0.1, 0.1))
    # for i in range(3):
    #     alpha = 2 * pi / 3 * i
    #     origin = rotate(alpha) @ vec2(12, 0)
    #     magatama(origin, 16, alpha + pi * (1 + 0.5))
    m_radius = 32
    c_radius = 20
    all_radius = m_radius + c_radius - 2
    for i in range(-64, 64):
        for j in range(-64, 64):
            if vec2(i, j).norm() > all_radius: continue
            flag = 1
            for k in range(3):
                alpha = 2 * pi / 3 * k + 0.6
                origin = rotate(alpha) @ vec2(c_radius, 0)
                if in_magatama(i, j, origin, m_radius, alpha + pi * (1 + 0.37)):
                    flag = 0
            if flag:
                scene.set_voxel(vec3(i, 0, j), 2, vec3(0.8, 0.1, 0.8))



initialize_voxels()

scene.finish()
