import gmsh

# Gmshを初期化
gmsh.initialize()

# モデルを作成
model = gmsh.model
model.add("box_mesh")

# パラメータ
length = 1.0  # 箱の長さ
width = 1.0  # 箱の幅
height = 1.0  # 箱の高さ

# 箱のジオメトリを作成
lc = 0.1  # 特徴サイズ
box = model.occ.addBox(0, 0, 0, length, width, height)
model.occ.synchronize()

# STLファイルをロードしてジオメトリを追加
stl_file = "path/to/your/stl/file.stl"
gmsh.merge(stl_file)
gmsh.model.occ.synchronize()

# メッシュを生成
gmsh.option.setNumber("Mesh.MeshSizeMax", lc)
gmsh.option.setNumber("Mesh.MeshSizeMin", lc)
gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
gmsh.model.mesh.generate(3)

# メッシュを切断
gmsh.model.mesh.setMeshOrder(1)
gmsh.model.mesh.cut([(3, box)], [(2, -1)], 2)  # surface_loopのtagを-1で指定

# メッシュを保存
output_file = "path/to/your/output/mesh.msh"
gmsh.write(output_file)

# Gmshを終了
gmsh.finalize()
