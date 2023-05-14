import gmsh
import numpy as np

gmsh.initialize()

gmsh.model.add("x7")

gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMin", 2.0)
gmsh.model.mesh.generate(3)
order = 2
interpolationOrder = 1
gmsh.model.mesh.setOrder(order)

elementType = gmsh.model.mesh.getElementType("tetrahedron", order)
edgeNodes = gmsh.model.mesh.getElementEdgeNodes(elementType).reshape(-1, order + 1)

# generate Edge Tagas
gmsh.model.mesh.createEdges()
edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(edgeNodes[:, :2].flatten())

localCoords, weights = gmsh.model.mesh.getIntegrationPoints(
    elementType, "Gauss" + str(interpolationOrder)
)

numComponents, basisFunctions, numOrientations = gmsh.model.mesh.getBasisFunctions(
    elementType, localCoords, "Lagrange"
)

print(basisFunctions.shape)
print(basisFunctions)

jacobians, determinants, coords = gmsh.model.mesh.getJacobians(elementType, localCoords)

elementTags, _ = gmsh.model.mesh.getElementsByType(elementType)

print(localCoords)
print(len(elementTags))
print(len(determinants))
print(jacobians.reshape(24, -1).shape)

# Launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()

gmsh.finalize()
