#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
import numpy as np
from fem.field import Element, Edge, Node
from fem.field.model import make_model
from fem.calc import set_nodes, set_edges, set_element


def calc_K(elements):
    determinants = 1
    K = np.zeros()
    for e in elements:
        for edge_i, edge_j in itertools.product(e.edges, e.edges):
            grad_N_i = edge_i.grad_N
            grad_N_j = edge_j.grad_N
        K[i][j] += np.dot(grad_N_i, grad_N_j) * determinants

    return K


if __name__ == '__main__':
    from pprint import pprint

    gmsh.initialize()
    gmsh.model.add("fem")
    make_model()
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.createEdges()

    elementType = gmsh.model.mesh.getElementType("tetrahedron", 1)
    elements = set_element(elementType)
    pprint(elements)
    # gmsh.fltk.run()

