from spatialmath import *

# print(SE3(0,0,0))
x = SE3.Rand()
print(x)
print(x.t)
y = SE3(x.t)
print(y)

print(type(x.R))
print(x.R)
print(SO3(x.R))
print(SE3(SO3(x.R)))

print(SO3(x))

