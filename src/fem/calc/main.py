#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import dataclasses

import gmsh
import numpy as np


@dataclasses.dataclass
class Node:
    tag: int
    # nodal: np.ndarray
    grad: np.ndarray


@dataclasses.dataclass
class Edge:
    tag: int
    nodes: list[Node]
    orientation: int
    edge_shape: list
    curl_edge_shape: list


@dataclasses.dataclass
class Element:
    tag: int
    edges: list[Edge]


if __name__ == "__main__":
    gmsh.initialize()

    gmsh.model.add("x7")

    # gmsh.option.setNumber("Mesh.MeshSizeMin", 1)
    gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)

    order = 1
    interpolationOrder = 1
    gmsh.model.mesh.setOrder(order)

    elementType = gmsh.model.mesh.getElementType("tetrahedron", order)
    elementTags, _ = gmsh.model.mesh.getElementsByType(elementType)
    elementEdgeNodes = gmsh.model.mesh.getElementEdgeNodes(elementType).reshape(
        -1, 6, order + 1
    )

    # generate Edge Tagas
    gmsh.model.mesh.createEdges()

    # integral
    localCoords, weights = gmsh.model.mesh.getIntegrationPoints(elementType, "Gauss")

    # affine transform
    jacobians, determinants, coords = gmsh.model.mesh.getJacobians(
        elementType, localCoords
    )

    element_list = []

    for elementTag, edgeNodes, jacobian in zip(
        elementTags, elementEdgeNodes, jacobians.reshape(-1, 3, 3)
    ):
        _, nodeTags, _, _ = gmsh.model.mesh.getElement(elementTag)
        edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(
            edgeNodes[:, :2].flatten()
        )

        # function_space_type = "H1Legendre1"
        # nodal_basises = get_basis(elementTag, elementType, localCoords, function_space_type)
        function_space_type = "GradH1Legendre1"
        grad_basises = get_basis(
            elementTag, elementType, localCoords, function_space_type
        )
        function_space_type = "HcurlLegendre1"
        edge_basises = get_basis(
            elementTag, elementType, localCoords, function_space_type
        )
        function_space_type = "CurlHcurlLegendre"
        curl_basises = get_basis(
            elementTag, elementType, localCoords, function_space_type
        )

        edge_list = []
        for edgeTag, edge_nodes, edgeOrientation, edge_basis, curl_basis in zip(
            edgeTags,
            edgeOrientations,
            edge_basises.reshape(-1, 3),
            curl_basises.reshape(-1, 3),
        ):
            node_list = []
            grad = 0
            for edgeNode in edgeNodes[:, :2]:
                node = Node(edgeNode, grad)
                node_list.append(node)

            # how to create node tag
            edge = Edge(edgeTag, node_list, edgeOrientation, edge_basis, curl_basis)
            edge_list.append(edge)

        element = Element(elementTag, edge_list)
        element_list.append(element)

        print(element_list)

        # for edgeTag, edgeOrientation, edgeij, edge_shape, curl_edge_shape in \
        #         zip(edgeTags, edgeOrientations, edgeAB, edge_basis.reshape(-1, 3), curl_edge_basis.reshape(-1, 3)):
        #     if edgeOrientation == -1:
        #         edge = Edge(edgeTag, edgeij[[1, 0]], edgeOrientation, -edge_shape, curl_edge_shape)
        #     else:
        #         edge = Edge(edgeTag, edgeij, edgeOrientation, edge_shape, curl_edge_shape)
        #     edges_list.append(edge)

        # print(edges_list)

    # Launch the GUI to see the results:
    # if '-nopopup' not in sys.argv:
    #     gmsh.fltk.run()

    gmsh.finalize()
