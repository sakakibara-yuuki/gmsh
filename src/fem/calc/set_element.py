#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
import numpy as np

from fem.calc import set_edges, set_nodes
from fem.field import Edge, Element, Node


def set_element(elementType, element_order, interpolate_order):

    # all-element node
    elementTags, elementNodeTags = gmsh.model.mesh.getElementsByType(elementType)

    # all-element edge
    edgeNodes = gmsh.model.mesh.getElementEdgeNodes(elementType).reshape(
        -1, element_order + 1
    )

    # this is Nessesary
    gmsh.model.mesh.createEdges()
    edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(edgeNodes[:, :2].flatten())

    # gauss-Legendre localCoords
    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
        elementType, "Gauss" + str(interpolate_order)
    )

    # affine transform
    jacobians, determinants, coords = gmsh.model.mesh.getJacobians(
        elementType, localCoords
    )

    # edgeTag と　自作N, rotを対応させる.
    # edgeTag　の並び順を確認する.
    # print(jacobians.reshape(-1, 3, 3)[:2])
    # print(weights)
    # print(localCoords)
    # print("elementTags")
    # print(elementTags[:3])
    # print(elementTags.shape)
    # print("elementNodeTags")
    # print(elementNodeTags[: 3 * 4])
    # print(elementNodeTags.shape)
    # print('edgeNodes')
    # print(edgeNodes[:3*6, :])
    # print(edgeNodes.shape)
    # print('edgeTags')
    # print(edgeTags[:3*6])
    # print(edgeTags.shape)

    node_list = []
    for node_tag in elementNodeTags:
        node = Node(node_tag)
        node_list.append(node)
    node_list = np.array(node_list, dtype=object)

    edge_list = []
    for edge_tag, edge_nodes in zip(edgeTags, edgeNodes[:, :2]):
        edge_nodes = [Node(node_tag) for node_tag in edge_nodes]
        edge = Edge(edge_tag, edge_nodes)
        edge_list.append(edge)
    edge_list = np.array(edge_list, dtype=object)

    element_list = []
    for element_tag, edges, nodes, jacobian, determinant in zip(
        elementTags,
        edge_list.reshape(-1, 6),
        node_list.reshape(-1, 4),
        jacobians.reshape(-1, 3, 3),
        determinants.reshape(-1, 1),
    ):

        e = Element(element_tag, edges, nodes, jacobian, determinant)

        element_list.append(e)

        # e.elementType = elementType
        # e.localCoords = localCoords
        # e.weights = weights
        # create basis
        # e.set_basis()

    element_list = np.array(element_list, dtype=object)

    return element_list
