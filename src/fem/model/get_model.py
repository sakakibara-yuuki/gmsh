#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sakakibara <sakakibara@skk.local>
#
# Distributed under terms of the MIT license.
# ------------------------------------------------------------------------------
#
#  Gmsh Python tutorial 14
#
#  Homology and cohomology computation
#
# ------------------------------------------------------------------------------

# Homology computation in Gmsh finds representative chains of (relative)
# (co)homology space bases using a mesh of a model.  The representative basis
# chains are stored in the mesh as physical groups of Gmsh, one for each chain.

import sys

import gmsh

gmsh.initialize(sys.argv)

# Create an example geometry
gmsh.model.add("t14")


# DefineConstant[
#   lc = {TotalMemory <= 2048 ? 0.1 : 0.02, Name "Mesh size"}
# ];
# lc2 = lc;
# lc3 = 0;
# front3d = 0; // Set to 1 if Frontal 3D mesh algorithm is used
# nn = (1./lc)/4.; // Mesh subdivisions per turn, used with Frontal 3D

# If(front3d == 1)
#   Mesh.Algorithm3D = 4; // Frontal 3D
# EndIf
# Mesh.Optimize = 1;


# lc = 0.1 if TotalMemory <= 2048 else 0.02 #Mesh size
lc = 0.1
turns = 5 #Geometry/Number of coil turns
r = 0.11 # Geometry/Coil radius
rc = 0.01 # Geometry/Coil wire radius
hc = 0.2 # Geometry/Coil height
ht = 0.3 # Geometry/Tube height
rt1 = 0.081 # Geometry/Tube internal radius
rt2 = 0.092 # Geometry/Tube external radius
lb = 1 # Geometry/Infinit box width
left = 1 # Geometry/Terminals on the left?

# tube
p = 0
Point(p) = {0, 0, -ht/2, lc2};
Point(p+1) = {rt1, 0, -ht/2, lc2};
Point(p+2) = {0, rt1, -ht/2, lc2};
Point(p+3) = {-rt1, 0, -ht/2, lc2};
Point(p+4) = {0, -rt1, -ht/2, lc2};
Point(p+5) = {rt2, 0, -ht/2, lc2};
Point(p+6) = {0, rt2, -ht/2, lc2};
Point(p+7) = {-rt2, 0, -ht/2, lc2};
Point(p+8) = {0, -rt2, -ht/2, lc2};
c = newc;
Circle(c) = {p+1, p, p+2};
Circle(c+1) = {p+2, p, p+3};
Circle(c+2) = {p+3, p, p+4};
Circle(c+3) = {p+4, p, p+1};
Circle(c+4) = {p+5, p, p+6};
Circle(c+5) = {p+6, p, p+7};
Circle(c+6) = {p+7, p, p+8};
Circle(c+7) = {p+8, p, p+5};
ll = newll;
Line Loop(ll) = {c+4, c+5, c+6, c+7, -c, -(c+1), -(c+2), -(c+3)};
s = news;
Plane Surface(s) = {ll};
If(front3d == 1)
tmp[] = Extrude {0,0,ht}{ Surface{s}; Layers{nn}; };
EndIf
If(front3d == 0)
tmp[] = Extrude {0,0,ht}{ Surface{s}; };
EndIf
vol_tube = tmp[1];

# box
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

# v = 0
# gmsh.model.geo.addVolume(sl, v)

gmsh.model.geo.synchronize()

# # Create physical groups, which are used to define the domain of the
# # (co)homology computation and the subdomain of the relative (co)homology
# # computation.

# # Whole domain
# domain_tag = e[1][1]
# domain_physical_tag = 1001
# gmsh.model.addPhysicalGroup(dim=3, tags=[domain_tag], tag=domain_physical_tag, name="Whole domain")

# # Four "terminals" of the model
# terminal_tags = [e[3][1], e[5][1], e[7][1], e[9][1]]
# terminals_physical_tag = 2001
# gmsh.model.addPhysicalGroup(dim=2,
#                             tags=terminal_tags,
#                             tag=terminals_physical_tag,
#                             name="Terminals")

# # Find domain boundary tags
# boundary_dimtags = gmsh.model.getBoundary(dimTags=[(3, domain_tag)],
#                                           oriented=False)
# boundary_tags = []
# complement_tags = []
# for tag in boundary_dimtags:
#     complement_tags.append(tag[1])
#     boundary_tags.append(tag[1])
# for tag in terminal_tags:
#     complement_tags.remove(tag)

# # Whole domain surface
# boundary_physical_tag = 2002
# gmsh.model.addPhysicalGroup(dim=2,
#                             tags=boundary_tags,
#                             tag=boundary_physical_tag,
#                             name="Boundary")

# # Complement of the domain surface with respect to the four terminals
# complement_physical_tag = 2003
# gmsh.model.addPhysicalGroup(dim=2,
#                             tags=complement_tags,
#                             tag=complement_physical_tag,
#                             name="Complement")

# # Find bases for relative homology spaces of the domain modulo the four
# # terminals.
# gmsh.model.mesh.addHomologyRequest("Homology", domainTags=[domain_physical_tag],
#                                    subdomainTags=[terminals_physical_tag],
#                                    dims=[0, 1, 2, 3])

# # Find homology space bases isomorphic to the previous bases: homology spaces
# # modulo the non-terminal domain surface, a.k.a the thin cuts.
# gmsh.model.mesh.addHomologyRequest("Homology", domainTags=[domain_physical_tag],
#                                    subdomainTags=[complement_physical_tag],
#                                    dims=[0, 1, 2, 3])

# # Find cohomology space bases isomorphic to the previous bases: cohomology
# # spaces of the domain modulo the four terminals, a.k.a the thick cuts.
# gmsh.model.mesh.addHomologyRequest("Cohomology", domainTags=[domain_physical_tag],
#                                    subdomainTags=[terminals_physical_tag],
#                                    dims=[0, 1, 2, 3])

# # more examples
# gmsh.model.mesh.addHomologyRequest()
# gmsh.model.mesh.addHomologyRequest("Homology", domainTags=[domain_physical_tag])
# gmsh.model.mesh.addHomologyRequest("Homology", domainTags=[domain_physical_tag],
#                                    subdomainTags=[boundary_physical_tag],
#                                    dims=[0,1,2,3])

# Generate the mesh and perform the requested homology computations
gmsh.model.mesh.generate(3)

# For more information, see M. Pellikka, S. Suuriniemi, L. Kettunen and
# C. Geuzaine. Homology and cohomology computation in finite element
# modeling. SIAM Journal on Scientific Computing 35(5), pp. 1195-1214, 2013.

gmsh.write("t14.msh")

# Launch the GUI to see the results:
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
