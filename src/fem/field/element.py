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
from fem.field.edge import Edge


@dataclasses.dataclass
class Element:
    tag: int
    type_num: int
    edges: list[Edge]
    jacobian: np.array
    determinant: float
    coord: np.array

    def __str__(self):
        return str(self.tag)

    @property
    def type_str(self):
        type_map = {
            1: '2-node-line',
            2: '3-node-triangle',
            3: '4-node-quadrangle',
            4: '4-node-tetrahedron',
            5: '8-node-hexahedron',
            6: '6-node-prism',
            7: '5-node-pyramid',
            }
        return type_map[self.type_num]


