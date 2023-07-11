#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
import math
import matplotlib.pyplot as plt
import seaborn as sn

from fem.calc import set_element
from fem.calc import get_edge_node_num
from fem.calc import calc_K, calc_C
import fem.model.geo


def show_heat_matrix(X):
    fig, ax = plt.subplots()
    sn.heatmap(data=X, annot=False)
    plt.show()


def p(X):
    for x in X:
        for _x in x:
            print(f"{_x:2.1f} ", end="")
        print()

# def air_box(s):
#     z = 0.63
#     lc2 = 0.3*1e-3

#     # 'naca_boundary_layer_2d.py'.
#     N = 10 # number of layers
#     r = 2 # ra7io
#     d = [1.7e-3] # thickness of first layer
#     for i in range(1, N): d.append(d[-1] + d[0] * r**i)
#     extbl = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2),
#                                                 [1] * N, d, True)

#     # get "top" surfaces of the boundary layer
#     top = []
#     for i in range(1, len(extbl)):
#         if extbl[i][0] == 3:
#             top.append(extbl[i-1])

#     print('++'*31)
#     gmsh.model.mesh.classifySurfaces(10 * math.pi / 180, True, False)
#     gmsh.model.mesh.removeDuplicateNodes()
#     gmsh.model.geo.synchronize()
#     gmsh.model.mesh.removeDuplicateNodes()
#     gmsh.model.mesh.classifySurfaces(10 * math.pi / 180, True, False)
#     # bnd = gmsh.model.getBoundary(top)
#     # cl2 = gmsh.model.geo.addCurveLoop([c[1] for c in bnd])
#     p1 = gmsh.model.geo.addPoint(-1, -1, 0, lc2)
#     p2 = gmsh.model.geo.addPoint(2, -1, 0, lc2)
#     p3 = gmsh.model.geo.addPoint(2, 1, 0, lc2)
#     p4 = gmsh.model.geo.addPoint(-1, 1, 0, lc2)
#     l1 = gmsh.model.geo.addLine(p1, p2)
#     l2 = gmsh.model.geo.addLine(p2, p3)
#     l3 = gmsh.model.geo.addLine(p3, p4)
#     l4 = gmsh.model.geo.addLine(p4, p1)
#     cl3 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
#     # s2 = gmsh.model.geo.addPlaneSurface([cl3, cl2])
#     print('**'*31)
#     gmsh.fltk.run()
#     # -------------------------- comment out til -----------------------
#     # create 3D air box
#     # -------------------------- comment out to -----------------------
#     p11 = gmsh.model.geo.addPoint(-1, -1, 2*z, lc2)
#     p12 = gmsh.model.geo.addPoint(2, -1, 2*z, lc2)
#     p13 = gmsh.model.geo.addPoint(2, 1, 2*z, lc2)
#     p14 = gmsh.model.geo.addPoint(-1, 1, 2*z, lc2)
#     l11 = gmsh.model.geo.addLine(p11, p12)
#     l12 = gmsh.model.geo.addLine(p12, p13)
#     l13 = gmsh.model.geo.addLine(p13, p14)
#     l14 = gmsh.model.geo.addLine(p14, p11)
#     l_1_11 = gmsh.model.geo.addLine(p1, p11)
#     l_2_12 = gmsh.model.geo.addLine(p2, p12)
#     l_3_13 = gmsh.model.geo.addLine(p3, p13)
#     l_4_14 = gmsh.model.geo.addLine(p4, p14)
#     cl3 = gmsh.model.geo.addCurveLoop([l11, l12, l13, l14])
#     s3 = gmsh.model.geo.addPlaneSurface([cl3])
#     cl4 = gmsh.model.geo.addCurveLoop([l1, l_2_12, -l11, -l_1_11])
#     s4 = gmsh.model.geo.addPlaneSurface([cl4])
#     cl5 = gmsh.model.geo.addCurveLoop([l2, l_3_13, -l12, -l_2_12])
#     s5 = gmsh.model.geo.addPlaneSurface([cl5])
#     cl6 = gmsh.model.geo.addCurveLoop([l3, l_4_14, -l13, -l_3_13])
#     s6 = gmsh.model.geo.addPlaneSurface([cl6])
#     cl7 = gmsh.model.geo.addCurveLoop([l4, l_1_11, -l14, -l_4_14])
#     s7 = gmsh.model.geo.addPlaneSurface([cl7])

#     b = [s[1] for s in top]
#     b.extend([s2, s3, s4, s5, s6, s7])
#     sl = gmsh.model.geo.addSurfaceLoop(b)
#     v = gmsh.model.geo.addVolume([sl])
#     # -------------------------- comment out till -----------------------
#     gmsh.model.geo.synchronize()

# def create_air_box(s):
#     mm = 1e-3
#     lc2 = 0.05*mm

#     bnd = gmsh.model.getBoundary(s)
#     # bnd = gmsh.model.getBoundary([(2, 35)])
#     cl2 = gmsh.model.geo.addCurveLoop([c[1] for c in bnd])
#     p1 = gmsh.model.geo.addPoint(-1*mm, -10*mm, 0, lc2)
#     p2 = gmsh.model.geo.addPoint(2*mm, -10*mm, 0, lc2)
#     p3 = gmsh.model.geo.addPoint(2*mm, 10*mm, 0, lc2)
#     p4 = gmsh.model.geo.addPoint(-1*mm, 10*mm, 0, lc2)
#     l1 = gmsh.model.geo.addLine(p1, p2)
#     l2 = gmsh.model.geo.addLine(p2, p3)
#     l3 = gmsh.model.geo.addLine(p3, p4)
#     l4 = gmsh.model.geo.addLine(p4, p1)
#     cl3 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
#     s2 = gmsh.model.geo.addPlaneSurface([cl3, cl2])
#     gmsh.model.geo.synchronize()


#     z = 4*mm
#     p11 = gmsh.model.geo.addPoint(-1*mm, -10*mm, 2*z, lc2)
#     p12 = gmsh.model.geo.addPoint(2*mm, -10*mm, 2*z, lc2)
#     p13 = gmsh.model.geo.addPoint(2*mm, 10*mm, 2*z, lc2)
#     p14 = gmsh.model.geo.addPoint(-1*mm, 10*mm, 2*z, lc2)
#     l11 = gmsh.model.geo.addLine(p11, p12)
#     l12 = gmsh.model.geo.addLine(p12, p13)
#     l13 = gmsh.model.geo.addLine(p13, p14)
#     l14 = gmsh.model.geo.addLine(p14, p11)
#     l_1_11 = gmsh.model.geo.addLine(p1, p11)
#     l_2_12 = gmsh.model.geo.addLine(p2, p12)
#     l_3_13 = gmsh.model.geo.addLine(p3, p13)
#     l_4_14 = gmsh.model.geo.addLine(p4, p14)
#     cl3 = gmsh.model.geo.addCurveLoop([l11, l12, l13, l14])
#     s3 = gmsh.model.geo.addPlaneSurface([cl3])
#     cl4 = gmsh.model.geo.addCurveLoop([l1, l_2_12, -l11, -l_1_11])
#     s4 = gmsh.model.geo.addPlaneSurface([cl4])
#     cl5 = gmsh.model.geo.addCurveLoop([l2, l_3_13, -l12, -l_2_12])
#     s5 = gmsh.model.geo.addPlaneSurface([cl5])
#     cl6 = gmsh.model.geo.addCurveLoop([l3, l_4_14, -l13, -l_3_13])
#     s6 = gmsh.model.geo.addPlaneSurface([cl6])
#     cl7 = gmsh.model.geo.addCurveLoop([l4, l_1_11, -l14, -l_4_14])
#     s7 = gmsh.model.geo.addPlaneSurface([cl7])

#     b = [s[1] for s in top]
#     b.extend([s2, s3, s4, s5, s6, s7])
#     sl = gmsh.model.geo.addSurfaceLoop(b)
#     v = gmsh.model.geo.addVolume([sl])

#     gmsh.model.mesh.createGeometry()
#     gmsh.model.geo.synchronize()


def create_air_box():
    mm = 1e-3
    gmsh.model.add('air_box')
    # gmsh.model.occ.add_box(0.000250, 0.005672, 0.005545, 3*mm, 20*mm, 4*mm)
    gmsh.model.occ.add_box(2, 2, 1, mm, mm, mm)
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)

def createGeometryAndMesh():
    # mm = 1e-3

    # load STL surfaces
    # gmsh.merge('titled.stl')
    gmsh.merge('untitled3.stl')

    # mesh
    # gmsh.option.setNumber('Mesh.Algorithm', 6)
    # gmsh.option.setNumber('Mesh.MeshSizeMin', 0.05*mm)
    # gmsh.option.setNumber('Mesh.MeshSizeMax', 10*mm)

    # merge nodes that are at the same position up to some
    # gmsh.option.setNumber('Geometry.Tolerance', 1e-4)
    # gmsh.model.mesh.removeDuplicateNodes()

    # gmsh.model.mesh.classifySurfaces(40 * 3.14 / 180., True, True)
    # gmsh.model.mesh.classifySurfaces(10 * math.pi / 180, True, False)

    # gmsh.model.mesh.createGeometry()

    # get all the surfaces in the model
    # s = gmsh.model.getEntities(2)
    # create a surface loop and a volumen from these surfaces
    # l = gmsh.model.geo.addSurfaceLoop([e[1] for e in s])
    # gmsh.model.geo.addVolume([l])

    # synchronize the new volume with the model
    gmsh.model.geo.synchronize()

    create_air_box()
    # create_air_box(s)
    # air_box(s)

    gmsh.model.mesh.generate(3)

if __name__ == "__main__":
    gmsh.initialize()
    gmsh.model.add("fem")
    # gmsh.option.setNumber("Mesh.MeshSizeMin", 1)

    createGeometryAndMesh()

    element_order = 1
    interpolate_order = 1
    elementType = gmsh.model.mesh.getElementType("tetrahedron", element_order)

    # get element info
    gmsh.model.mesh.setOrder(element_order)
    elements = set_element(elementType, element_order, interpolate_order)

    edge_num, node_num = get_edge_node_num(elements)
    # K = calc_K(elements, edge_num, node_num, elementType)
    # C = calc_C(elements, edge_num, node_num, elementType)

    # show_heat_matrix(K)
    # show_heat_matrix(C)

    gmsh.fltk.run()
    gmsh.finalize()
