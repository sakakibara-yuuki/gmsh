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

from fem.field.edge import Edge, Node


@dataclasses.dataclass
class Element:
    tag: int
    edges: list[Edge]
    nodes: list[Node]
    # transform to gauss-Legendre system
    jacobian: np.array
    determinant: float

    elementType = None
    localCoords = None
    weights = None
    grad = None

    def __str__(self):
        return str(self.tag)

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.tag == other.tag
        return False

    def __hash__(self):
        return hash(self.tag)

    def set_basis(self):
        nodal_func_space = "Lagrange"
        Ls = self.get_basis(
            self.tag, self.elementType, self.localCoords, nodal_func_space
        )
        print(Ls)

        scalar_func_space = "H1Legendre"
        grad_func_space = "GradH1Legendre1"
        rot_func_space = "HcurlLegendre"
        rotrot_func_space = "CurlHcurlLegendre"

        Ns = (
            self.get_basis(self.tag, self.elementType, self.localCoords, rot_func_space)
            @ self.jacobian
        )
        rots = (
            self.get_basis(
                self.tag, self.elementType, self.localCoords, rotrot_func_space
            )
            @ self.jacobian
        )

        for edge, N, rot in zip(self.edges, Ns, rots):
            edge.N = N
            edge.rot = rot

        grads = (
            self.get_basis(
                self.tag, self.elementType, self.localCoords, grad_func_space
            )
            @ self.jacobian
        )

        for node, grad in zip(self.nodes, grads):
            node.grad = grad

    def type_str(self):
        if self.elementType != None:
            return "error"
        type_map = {
            1: "2-node-line",
            2: "3-node-triangle",
            3: "4-node-quadrangle",
            4: "4-node-tetrahedron",
            5: "8-node-hexahedron",
            6: "6-node-prism",
            7: "5-node-pyramid",
        }
        return type_map[self.elementType]

    @staticmethod
    def get_basis(elementTag, elementType, localCoords, function_space_type):
        basisOrientation = gmsh.model.mesh.getBasisFunctionsOrientationForElement(
            elementTag, function_space_type
        )
        numComponents, basis_func, numOrientations = gmsh.model.mesh.getBasisFunctions(
            elementType, localCoords, function_space_type, [basisOrientation]
        )
        return basis_func.reshape(-1, numComponents)
