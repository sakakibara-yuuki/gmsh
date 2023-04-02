#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
from fem.field import Node


def set_nodes(element_nodes, basisFunctions_L, grads):
    nodes = []
    for node_tag, L, grad in zip(element_nodes, basisFunctions_L, grads):
        nodes.append(Node(node_tag, L, grad))
    return nodes
