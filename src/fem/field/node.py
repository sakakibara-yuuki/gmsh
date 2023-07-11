#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import dataclasses

import numpy as np


@dataclasses.dataclass
class Node:
    tag: int

    grad: np.ndarray = None

    def __str__(self):
        return str(self.tag) + ";" + str(self.grad)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.tag == other.tag
        return self.tag == other

    def __hash__(self):
        return hash(self.tag)
