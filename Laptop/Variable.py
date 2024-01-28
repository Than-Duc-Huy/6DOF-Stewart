import numpy as np
from spatialmath import *
import roboticstoolbox as rtb
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



pyplot = rtb.backends.PyPlot.PyPlot()
pyplot.launch()


center_to_joint = 67.63 #mm
min_joint_length = 210 #mm
max_joint_length = 300 #mm
angle = 12.82 #deg

angle_base_to_joint = np.array([-angle, angle, 120 - angle,120 + angle, 240 - angle, 240 + angle])
angle_base_to_joint_rad = angle_base_to_joint * np.pi/180


angle_platform_to_joint = np.array([-60+angle, 60-angle,60+angle,180-angle,180+angle,-60-angle])
angle_platform_to_joint_rad = angle_platform_to_joint*np.pi/180


pose_base_to_joint = []
pose_platform_to_joint = []

# Original
for i in range(6):
	pose_base_to_joint.append(SE3.Rz(angle_base_to_joint_rad[i])*SE3.Tx(center_to_joint))
	pose_platform_to_joint.append(SE3.Rz(angle_platform_to_joint_rad[i])*SE3.Tx(center_to_joint))
	# pose_base_to_joint[i].plot()
	# pose_platform_to_joint[i].plot()


base_coord = []
base_coord_x = np.ndarray(6)
base_coord_y = np.ndarray(6)
base_coord_z = np.ndarray(6)
for i in range(6):
	base_coord.append(pose_base_to_joint[i].t)
	base_coord_x[i], base_coord_y[i], base_coord_z[i] = (pose_base_to_joint[i].t)

print(base_coord)
print(base_coord_x)
print(base_coord_y)
print(base_coord_z)

base_vert = [list(zip(base_coord_x,base_coord_y,base_coord_z))]
base_shape = Poly3DCollection(base_vert)
base_shape.set_facecolor('r')
base_shape.set_edgecolor('black')
pyplot.ax.add_collection3d(base_shape)





translation = SE3(0,0,206)
rotation = SE3.RPY([0,1,0], order = 'xyz')


platform_center = translation*rotation
platform_center.plot()

new_platform_to_joint = []
for i in range(6):
	new_platform_to_joint.append(platform_center*pose_platform_to_joint[i])
	# new_platform_to_joint[i].plot()


plat_coord = []
plat_coord_x = np.ndarray(6)
plat_coord_y = np.ndarray(6)
plat_coord_z = np.ndarray(6)
for i in range(6):
	plat_coord.append(new_platform_to_joint[i].t)
	plat_coord_x[i], plat_coord_y[i], plat_coord_z[i] = (new_platform_to_joint[i].t)


plat_vert = [list(zip(plat_coord_x,plat_coord_y,plat_coord_z))]
platform_shape = Poly3DCollection(plat_vert)
platform_shape.set_facecolor('blue')
platform_shape.set_edgecolor('black')

pyplot.ax.add_collection3d(platform_shape)

for i in range(6):
	xs = [base_coord[i][0], plat_coord[i][0]]
	ys = [base_coord[i][1], plat_coord[i][1]]
	zs = [base_coord[i][2], plat_coord[i][2]]
	pyplot.ax.plot(xs,ys,zs)

pyplot.ax.xaxis.set_ticks(np.arange(-70, 80,20))
pyplot.ax.yaxis.set_ticks(np.arange(-70, 80,20))
pyplot.ax.zaxis.set_ticks(np.arange(0, 300,20))
pyplot.ax.view_init(30, -42) #Elevation, Azimuth

joint_length = []
for i in range(6):
	joint_length.append(np.linalg.norm((new_platform_to_joint[i].t - pose_base_to_joint[i].t)).round(0))   # Find Length, find milimeter
print(joint_length)


b = input()


