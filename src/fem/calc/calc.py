#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import itertools
import pprint

import gmsh
import matplotlib.pyplot as plt
import numpy as np

from fem.calc import set_element
from fem.field import Edge, Element, Node
from fem.field.model import make_model


def get_edge_node_num(elements):
    edge_tag_list = []
    node_tag_list = []
    for e in elements:
        for edge in e.edges:
            edge_tag_list.append(edge.tag)
            for node in edge.nodes:
                node_tag_list.append(node.tag)
    edge_num = len(set(edge_tag_list))
    node_num = len(set(node_tag_list))
    return edge_num, node_num


def calc_C(elements, edge_num, node_num, elementType):

    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
        elementType, "Gauss"
    )

    grad = basis_grad(localCoords)
    N = basis_N(localCoords)

    C = np.zeros((edge_num + node_num, edge_num + node_num))

    for e in elements:

        g = e.jacobian.T @ e.jacobian

        row = np.array([[int(edge.tag) - 1] for edge in e.edges])
        col = np.array([int(edge.tag) - 1 for edge in e.edges])
        C[row, col] += e.determinant * np.dot(N @ g, N.T)

        row = np.array([[int(edge.tag) - 1] for edge in e.edges])
        col = np.array([int(node.tag) - 1 for node in e.nodes]) + edge_num
        C[row, col] += e.determinant * np.dot(N @ g, grad.T)
        C[col, row] = C[row, col]

        row = np.array([[int(node.tag) - 1] for node in e.nodes]) + edge_num
        col = np.array([int(node.tag) - 1 for node in e.nodes]) + edge_num
        C[row, col] += e.determinant * np.dot(grad @ g, grad.T)

    return C


def calc_K(elements, edge_num, node_num, elementType):

    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
        elementType, "Gauss"
    )
    rot = basis_rot(localCoords)

    K = np.zeros((edge_num + node_num, edge_num + node_num))

    for e in elements:
        g = e.jacobian.T @ e.jacobian
        row = np.array([[int(edge.tag) - 1] for edge in e.edges])
        col = np.array([int(edge.tag) - 1 for edge in e.edges])
        K[row, col] += rot @ np.linalg.inv(g) @ rot.T * e.determinant[0] ** 3
    return K

def basis_grad(localCoords):
    if not isinstance(localCoords, np.ndarray):
        localCoords = np.array(localCoords)
    if localCoords.shape[0] != 3:
        raise Exception("dim is not matched")
    u, v, w = localCoords
    grad = np.array([[-1, -1, -1],
                     [1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])
    return grad

def basis_N(localCoords):
    if not isinstance(localCoords, np.ndarray):
        localCoords = np.array(localCoords)
    if localCoords.shape[0] != 3:
        raise Exception("dim is not matched")
    u, v, w = localCoords
    N = np.array([[1-u-w, u, u],
                  [v, 1-u-w, v],
                  [w, w, 1-u-v],
                  [-w, u, 0],
                  [-w, 0, u],
                  [0, -w, v]])
    return N

def basis_rot(localCoords):
    if not isinstance(localCoords, np.ndarray):
        localCoords = np.array(localCoords)
    if localCoords.shape[0] != 3:
        raise Exception("dim is not matched")
    u, v, w = localCoords
    rot = np.array([[0, -2, 2],
                    [2, 0, -2],
                    [-2, 2, 0],
                    [0,  0, 2],
                    [0, -2, 0],
                    [2, 0, 0]])
    return rot

def _calc_C(elements, edge_num, node_num):
    C = np.zeros((edge_num + node_num, edge_num + node_num))

    for e in elements:
        for edge_i, edge_j in itertools.product(e.edges, e.edges):
            i = int(edge_i.tag - 1)
            j = int(edge_j.tag - 1)
            C[i][j] += np.dot(edge_i.N, edge_j.N) * e.determinant

        for edge, node in itertools.product(e.edges, e.nodes):
            i = int(edge.tag - 1)
            j = int(edge_num + node.tag - 1)
            C[i][j] += np.dot(edge.N, node.grad) * e.determinant
            C[j][i] = C[i][j]

        for node_i, node_j in itertools.product(e.nodes, e.nodes):
            i = int(edge_num + node_i.tag - 1)
            j = int(edge_num + node_j.tag - 1)
            C[i][j] += np.dot(node_i.grad, node_j.grad) * e.determinant

    return C


def _calc_K(elements, edge_num, node_num):
    K = np.zeros((edge_num + node_num, edge_num + node_num))
    for e in elements:
        for edge_i, edge_j in itertools.product(e.edges, e.edges):
            i = int(edge_i.tag - 1)
            j = int(edge_j.tag - 1)
            K[i][j] += np.dot(edge_i.rot, edge_j.rot) * e.determinant
    return K


def show_heat_matrix(X):
    fig, ax = plt.subplots()
    heat = ax.pcolor(X, cmap=plt.cm.Blues)
    ax.invert_yaxis()
    plt.show()


def p(X):
    for x in X:
        for _x in x:
            print(f"{_x:2.1f} ", end="")
        print()


def createGeometryAndMesh():
    gmsh.clear()
    # gmsh.merge('titled.stl')

    # s = gmsh.model.getEntities(2)
    # l = gmsh.model.geo.addSurfaceLoop([e[1] for e in s])
    # gmsh.model.geo.addVolume([l])
    # gmsh.model.geo.synchronize()

    gmsh.model.add("sample model")
    gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)
    gmsh.model.occ.synchronize()

    gmsh.model.mesh.generate(3)
    # gmsh.write('titled.msh')


if __name__ == "__main__":
    gmsh.initialize()
    gmsh.model.add("fem")
    # gmsh.option.setNumber("Mesh.MeshSizeMin", 12)

    createGeometryAndMesh()

    element_order = 1
    interpolate_order = 1
    elementType = gmsh.model.mesh.getElementType("tetrahedron", element_order)

    # get element info
    gmsh.model.mesh.setOrder(element_order)
    elements = set_element(elementType, element_order, interpolate_order)

    edge_num, node_num = get_edge_node_num(elements)
    K = calc_K(elements, edge_num, node_num, elementType)
    C = calc_C(elements, edge_num, node_num, elementType)

    # show_heat_matrix(K)
    # show_heat_matrix(C)

    # gmsh.fltk.run()
    gmsh.finalize()
