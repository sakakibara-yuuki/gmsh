#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
import numpy as np
import itertools
from fem.field import Element, Edge, Node
from fem.field.model import make_model
from fem.calc import set_nodes, set_edges, set_element


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


def calc_K(elements):

    edge_num, node_num = get_edge_node_num(elements)

    determinants = 1
    K = np.zeros((edge_num + node_num, edge_num + node_num))
    for e in elements:
        for edge_i, edge_j in itertools.product(e.edges, e.edges):
            i = int(edge_i.tag - 1)
            j = int(edge_j.tag - 1)
            K[i][j] += np.dot(edge_i.rot, edge_j.rot) * determinants
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
    K = calc_K(elements)
    print(K)
    # pprint(elements)
    # gmsh.fltk.run()

