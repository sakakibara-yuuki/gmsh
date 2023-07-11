#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh


def make_model_1():
    # モデルを作成
    model = gmsh.model
    model.add("cube")

    # 立方体の座標を定義
    lc = 1.0
    x0, y0, z0 = 0.0, 0.0, 0.0
    x1, y1, z1 = 1.0, 1.0, 1.0

    # 立方体を作成
    p1 = model.geo.addPoint(x0, y0, z0, lc)
    p2 = model.geo.addPoint(x1, y0, z0, lc)
    p3 = model.geo.addPoint(x1, y1, z0, lc)
    p4 = model.geo.addPoint(x0, y1, z0, lc)
    p5 = model.geo.addPoint(x0, y0, z1, lc)
    p6 = model.geo.addPoint(x1, y0, z1, lc)
    p7 = model.geo.addPoint(x1, y1, z1, lc)
    p8 = model.geo.addPoint(x0, y1, z1, lc)

    l1 = model.geo.addLine(p1, p2)
    l2 = model.geo.addLine(p2, p3)
    l3 = model.geo.addLine(p3, p4)
    l4 = model.geo.addLine(p4, p1)
    l5 = model.geo.addLine(p1, p5)
    l6 = model.geo.addLine(p2, p6)
    l7 = model.geo.addLine(p3, p7)
    l8 = model.geo.addLine(p4, p8)
    l9 = model.geo.addLine(p5, p6)
    l10 = model.geo.addLine(p6, p7)
    l11 = model.geo.addLine(p7, p8)
    l12 = model.geo.addLine(p8, p5)

    c1 = model.geo.addCurveLoop([l1, l2, l3, l4])
    c2 = model.geo.addCurveLoop([l5, l6, l2, l1])
    c3 = model.geo.addCurveLoop([l6, l7, l3, l2])
    c4 = model.geo.addCurveLoop([l7, l8, l4, l3])
    c5 = model.geo.addCurveLoop([l8, l5, l1, l4])
    c6 = model.geo.addCurveLoop([l6, l10, l9, l5])
    c7 = model.geo.addCurveLoop([l10, l7, l11, l9])
    c8 = model.geo.addCurveLoop([l8, l11, l10, l6])
    c9 = model.geo.addCurveLoop([l11, l12, l9, l10])
    c10 = model.geo.addCurveLoop([l12, l8, l7, l9])
    model.geo.addSurfaceFilling([c1, c2, c3, c4, c5], 1)
    model.geo.addSurfaceFilling([c6, c7, c8, c9, c10], 2)
    gmsh.model.geo.addVolume([v])


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
