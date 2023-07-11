#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
import numpy as np


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


def calc_C(elements, edge_num, node_num, elementType):
    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
        elementType, "Gauss"
    )

    grad = basis_grad(localCoords)
    N = basis_N(localCoords)

    C = np.zeros((edge_num + node_num, edge_num + node_num))

    for e in elements:

        g = e.jacobian.T @ e.jacobian
        g_inv = np.linalg.inv(g)

        row = np.array([[edge.tag] for edge in e.edges]) - 1
        col = np.array([edge.tag for edge in e.edges]) - 1
        C[row, col] += N @ g_inv @ N.T * e.determinant[0]

        row = np.array([[edge.tag] for edge in e.edges]) - 1
        col = np.array([node.tag for node in e.nodes]) - 1 + edge_num
        C[row, col] += N @ g_inv @ grad.T * e.determinant[0]
        C[col, row] = C[row, col]

        row = np.array([[node.tag] for node in e.nodes]) - 1 + edge_num
        col = np.array([node.tag for node in e.nodes]) - 1 + edge_num
        C[row, col] += grad @ g_inv @ grad.T * e.determinant[0]

    return C


def calc_K(elements, edge_num, node_num, elementType):
    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
        elementType, "Gauss"
    )
    rot = basis_rot(localCoords)

    K = np.zeros((edge_num + node_num, edge_num + node_num))

    for e in elements:
        g = e.jacobian @ e.jacobian.T
        row = np.array([[edge.tag] for edge in e.edges]) - 1
        col = np.array([edge.tag for edge in e.edges]) - 1
        K[row, col] += rot @ g @ rot.T / e.determinant[0]
    return K
