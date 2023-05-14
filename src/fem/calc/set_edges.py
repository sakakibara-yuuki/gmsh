#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import numpy as np

from fem.field import Edge


def set_edges(edge_tags, edge_nodes, nodes):
    edges = []
    for edge_tag, nodes_pair_tag in zip(edge_tags, edge_nodes.reshape(-1, 2)):
        nodes_pair = set_nodes_pair(nodes_pair_tag, nodes)

        edge = Edge(tag=edge_tag, nodes=nodes_pair)

        edges.append(edge)

    return edges


def set_nodes_pair(nodes_pair_tag, nodes):
    nodes_pair = []
    for node in nodes:
        if node.tag in nodes_pair_tag:
            nodes_pair.append(node)
    return nodes_pair
