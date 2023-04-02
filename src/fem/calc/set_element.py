#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh
from fem.field import Element
from fem.calc import set_nodes, set_edges


def set_element(elementType):

    # all-element node
    elementTags, elementNodeTags =\
        gmsh.model.mesh.getElementsByType(elementType)

    # all-element edge
    edgeNodes = gmsh.model.mesh.getElementEdgeNodes(elementType)
    edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(edgeNodes)

    # all-element jacobian, determinants, coords, basisFunctions
    localCoords, weights =\
        gmsh.model.mesh.getIntegrationPoints(elementType, "Gauss1")

    jacobians, determinants, coords =\
        gmsh.model.mesh.getJacobians(elementType, localCoords)

    numComponents, basisFunctions_L, numOrientations =\
        gmsh.model.mesh.getBasisFunctions(elementType,
                                          localCoords,
                                          "Lagrange")

    numComponents, basisFunctions_grad, numOrientations =\
        gmsh.model.mesh.getBasisFunctions(elementType,
                                          localCoords,
                                          "GradLagrange")

    e_num = len(elementTags)

    elements_edges = []
    for element_nodes, grads, edge_tags, edge_nodes in zip(
            elementNodeTags.reshape(e_num, -1),
            basisFunctions_grad.reshape(4, 3) @ jacobians.reshape(e_num, 3, 3),
            edgeTags.reshape(e_num, -1),
            edgeNodes.reshape(e_num, -1)):

            nodes = set_nodes(element_nodes, basisFunctions_L, grads)
            edges = set_edges(edge_tags, edge_nodes, nodes)
            elements_edges.append(edges)

    elements = []
    for elemnt_tag, edges, jacobian, determinant, coord in zip(
                elementTags,
                elements_edges,
                jacobians.reshape(e_num, 3, 3),
                determinants,
                coords.reshape(e_num, -1)):

        e = Element(tag = elemnt_tag,
                    type_num = elementType,
                    edges = edges,
                    jacobian = jacobian,
                    determinant = determinant,
                    coord = coord)

        elements.append(e)


    return elements

