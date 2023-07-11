#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
import gmsh


def addBox(x, y, z, lx, ly, lz):
    p = 0;
    lc3 = 0
    lb = 1 # Infinit box width
    Point = {
        p  : (-lb/2,-lb/2,-lb/2, lc3),
        p+1: (lb/2,-lb/2,-lb/2, lc3),
        p+2: (lb/2,lb/2,-lb/2, lc3),
        p+3: (-lb/2,lb/2,-lb/2, lc3),
        p+4: (-lb/2,-lb/2,lb/2, lc3),
        p+5: (lb/2,-lb/2,lb/2, lc3),
        p+6: (lb/2,lb/2,lb/2, lc3),
        p+7: (-lb/2,lb/2,lb/2, lc3)
        }
    for tag, point in Point.items():
        gmsh.model.geo.addPoint(*point, tag)

    l = 0;
    Line = {
        l   : [p,p+1],
        l+1 : [p+1,p+2],
        l+2 : [p+2,p+3],
        l+3 : [p+3,p],
        l+4 : [p+4,p+5],
        l+5 : [p+5,p+6],
        l+6 : [p+6,p+7],
        l+7 : [p+7,p+4],
        l+8 : [p, p+4],
        l+9 : [p+1, p+5],
        l+10: [p+2, p+6],
        l+11: [p+3, p+7]
        }
    for tag, line in Line.items():
        gmsh.model.geo.addLine(*line, tag)

    ll = 0;
    Line_Loop = {
        ll+1: [l+8, -(l+7), -(l+11), l+3],
        ll+3: [l+9, l+5, -(l+10), -(l+1)],
        ll+4: [l,l+1,l+2,l+3],
        ll+5: [l+4,l+5,l+6,l+7],
        ll+6: [l+2, l+11, -(l+6), -(l+10)],
        ll+7: [l, l+9, -(l+4), -(l+8)]
        }
    for tag, loop in Line_Loop.items():
        gmsh.model.geo.addCurveLoop(loop, tag)

    s = 0
    # tmp = [ll+1, ll]
    # if left:
    #     tmp.append(ll+2)
    # gmsh.model.geo.addPlaneSurface(tmp, s)

    tmp = [ll+3]
    if not left:
        tmp.append(ll+2)

    gmsh.model.geo.addPlaneSurface(tmp, s)

    Plane_Surface = {
        s+1: tmp,
        s+2: [ll+4],
        s+3: [ll+5],
        s+4: [ll+6],
        s+5: [ll+7]
        }
    for tag, surface in Plane_Surface.items():
        gmsh.model.geo.addPlaneSurface(surface, tag)

    sl = 0
    Surface_Loop = {
            sl : [s, s+2, s+3, s+4, s+5]
        }
    for tag, loop in Surface_Loop.items():
        gmsh.model.geo.addSurfaceLoop(loop, tag)
