#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import dataclasses
import numpy as np
from fem.field.node import Node


@dataclasses.dataclass
class Edge:
    tag: int
    nodes: list[Node]
    N: np.array = None
    rot: np.array = None

    def __post_init__(self):
        self.rot = self.set_rot()
        self.N = self.set_N()

    def __str__(self):
        return str(self.tag)

    def set_rot(self):
        node_i, node_j = self.nodes
        rot = 2 * np.cross(node_i.grad, node_j.grad)
        return rot

    def set_N(self):
        node_i, node_j = self.nodes
        L_i, L_j, grad_i, grad_j = \
            node_i.L, node_j.L, node_i.grad, node_j.grad
        N = L_i * grad_j - L_j * grad_i
        return N
