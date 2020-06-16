import matplotlib.pyplot as plt
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d

figure = plt.figure()
axes = mplot3d.Axes3D(figure)
your_mesh = mesh.Mesh.from_file('Mini650_HULL.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)
plt.show()



