#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh


def make_model():
    lc = 3

    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(2, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(0, 3, 0, lc)
    p4 = gmsh.model.geo.addPoint(1, 1, 2, lc)

    l12 = gmsh.model.geo.addLine(p1, p2)
    l24 = gmsh.model.geo.addLine(p2, p4)
    l41 = gmsh.model.geo.addLine(p4, p1)
    l13 = gmsh.model.geo.addLine(p1, p3)
    l34 = gmsh.model.geo.addLine(p3, p4)
    l23 = gmsh.model.geo.addLine(p2, p3)

    s124 = gmsh.model.geo.addCurveLoop([l12, l24, l41])
    s143 = gmsh.model.geo.addCurveLoop([-l41, -l34, -l13])
    s234 = gmsh.model.geo.addCurveLoop([l23, l34, -l24])
    s213 = gmsh.model.geo.addCurveLoop([-l23, -l12, l13])

    S1 = gmsh.model.geo.addPlaneSurface([s124])
    S2 = gmsh.model.geo.addPlaneSurface([s143])
    S3 = gmsh.model.geo.addPlaneSurface([s234])
    S4 = gmsh.model.geo.addPlaneSurface([s213])

    v = gmsh.model.geo.addSurfaceLoop([S1, S2, S3, S4])
    gmsh.model.geo.addVolume([v])
