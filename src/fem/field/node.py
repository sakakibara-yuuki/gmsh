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
    L: float
    grad: np.array

    def __str__(self):
        return str(self.tag)

