import time
import roboticstoolbox as rtb
from spatialmath import *
import matplotlib.pyplot as plt
import pygame
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import serial


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.Matrix = SE3(0,0,0)*SE3.RPY([0,0,0], order = 'xyz')
        self.prevMatrix = self.Matrix
        self.invalid = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0
        self.p  = 0
        self.yaw = 0

        self.reset = 0

        #Individual Points
        self.center_to_joint = 67.63 #mm
        self.min_joint_length = 210 #mm
        self.max_joint_length = 300 #mm
        self.angle = 12.82 #deg

        ## Angle of the point on the base
        self.angle_base_to_joint = np.array([-self.angle, self.angle, 120 - self.angle,120 + self.angle, 240 - self.angle, 240 + self.angle])
        self.angle_base_to_joint_rad = self.angle_base_to_joint * np.pi/180

        ## Angle of the point on the platform
        self.angle_platform_to_joint = np.array([-60+self.angle, 60-self.angle,60+self.angle,180-self.angle,180+self.angle,-60-self.angle])
        self.angle_platform_to_joint_rad = self.angle_platform_to_joint*np.pi/180

        self.pose_base_to_joint = []
        self.pose_platform_to_joint = []
        self.new_platform_to_joint = []

        self.base_coord = []
        self.base_coord_x = np.ndarray(6)
        self.base_coord_y = np.ndarray(6)
        self.base_coord_z = np.ndarray(6)

        self.plat_coord = []
        self.plat_coord_x = np.ndarray(6)
        self.plat_coord_y = np.ndarray(6)
        self.plat_coord_z = np.ndarray(6)

        self.calculated = []
        self.joint_length = []
        self.platform_center = SE3(0,0,206)  # Init Platform Position
        self.platform_new_center = SE3(0,0,206)

        for i in range(6):
            # Base to Joint
            self.pose_base_to_joint.append(SE3.Rz(self.angle_base_to_joint_rad[i])*SE3.Tx(self.center_to_joint))
            # Platform to Joint
            self.pose_platform_to_joint.append(SE3.Rz(self.angle_platform_to_joint_rad[i])*SE3.Tx(self.center_to_joint))


            # Base Coord
            self.base_coord.append(self.pose_base_to_joint[i].t)
            self.base_coord_x[i], self.base_coord_y[i], self.base_coord_z[i] = (self.pose_base_to_joint[i].t)

            # Plat Coord
            self.new_platform_to_joint.append(self.platform_center*self.pose_platform_to_joint[i])
            self.plat_coord.append(self.new_platform_to_joint[i].t)
            self.plat_coord_x[i], self.plat_coord_y[i], self.plat_coord_z[i] = (self.new_platform_to_joint[i].t)        


            
            # Platform Coord
            self.plat_coord.append(self.pose_platform_to_joint[i].t)
            self.plat_coord_x[i], self.plat_coord_y[i], self.plat_coord_z[i] = (self.new_platform_to_joint[i].t)

            # Joint Lengh
            self.calculated.append(self.min_joint_length)
            self.joint_length.append(self.min_joint_length)
    
        self.base_vert = [list(zip(self.base_coord_x,self.base_coord_y,self.base_coord_z))]
        self.base_shape = Poly3DCollection(self.base_vert)
        self.base_shape.set_facecolor('pink')

        self.plat_vert = [list(zip(self.plat_coord_x,self.plat_coord_y,self.plat_coord_z))]
        self.platform_shape = Poly3DCollection(self.plat_vert)
        self.platform_shape.set_facecolor('green')

        # pyplot.ax.add_collection3d(self.base_shape)
        # pyplot.ax.add_collection3d(self.platform_shape)
        # pyplot.ax.set_xlim3d(-80,80,20)
        # pyplot.ax.set_ylim3d(-80,80,20)
        # pyplot.ax.set_zlim3d(0,300,20)
        # pyplot.ax.view_init(27, 152) #Elevation, Azimuth
        # a = input("Enter to continue")



    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}
            self.prev_axis = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False


        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value,2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False






    def update(self):
        self.listen()
        # TRANSLATION
        if (self.button_data.get(3)): # UP Z+
            self.z = 2
        elif (self.button_data.get(0)): # DOWN Z-
            self.z = -2
        else:
            self.z = 0 


        if (self.button_data.get(13)):# LEFT Y+
            self.y = 2
        elif (self.button_data.get(14)): # RIGHT Y-
            self.y = -2
        else:
            self.y = 0     

        if (self.button_data.get(11)): # FORWARD X+
            self.x = 2
        elif (self.button_data.get(12)): # BACKWARD X-
            self.x = -2
        else:
            self.x = 0 
    
        self.Matrix = SE3(self.x,self.y,self.z)*self.Matrix

        # RPY
        if (self.axis_data.get(0) == -1): # ROLL LEFT X-
            self.r = -0.05
        elif (self.axis_data.get(0) == 1): # ROLL RIGHT X+
            self.r = 0.05
        else:
            self.r = 0
        self.Matrix = SE3(self.Matrix.t)*SE3.Rx(self.r)*SE3(SO3(self.Matrix))


        
        if (self.axis_data.get(3) == -1):# PITCH DOWN Y+
            self.p = 0.05
        elif (self.axis_data.get(3) == 1): # PITCH UP Y-
            self.p = -0.05
        else: self.p = 0

        self.Matrix = SE3(self.Matrix.t)*SE3.Ry(self.p)*SE3(SO3(self.Matrix))

        if (self.axis_data.get(4) == 1): # YAW LEFT Z+
            self.yaw = 0.05
        elif (self.axis_data.get(5) == 1): # YAW RIGHT Z-
            self.yaw = -0.05
        else: self.yaw = 0

        self.Matrix = SE3(self.Matrix.t)*SE3.Rz(self.yaw)*SE3(SO3(self.Matrix))

        # RESET
        if (self.button_data.get(15)):  # Middle
            self.Matrix = SE3(0,0,0)
            self.reset = -2
        elif (self.button_data.get(10)): # R1
            self.reset = -1
        else:
            self.reset = 0
        if (self.button_data.get(9)):   # L1
            self.Matrix = SE3(self.Matrix.t)


        # CALCULATE

        self.platform_new_center = self.platform_center*self.Matrix

        for i in range(6):
            # JOINT LENGTH
            self.new_platform_to_joint[i] = self.platform_new_center*self.pose_platform_to_joint[i]
            self.calculated[i] = np.linalg.norm((self.new_platform_to_joint[i].t - self.pose_base_to_joint[i].t)).round(0)
            if ((self.calculated[i] > self.max_joint_length) or (self.calculated[i] < self.min_joint_length)):
                self.invalid = 1
                print("Invalid")
                break
            else: self.invalid = 0

            # NEW PLATFORM CENTER
            self.plat_coord[i] = self.new_platform_to_joint[i].t
            self.plat_coord_x[i], self.plat_coord_y[i], self.plat_coord_z[i] = (self.new_platform_to_joint[i].t)

        if (self.invalid == 0):
            for i in range(6): self.joint_length[i] = self.calculated[i] - self.min_joint_length
            self.prevMatrix = self.Matrix 
        else:
            self.Matrix = self.prevMatrix
            self.invalid = 0
        print(self.joint_length)
        # print(self.Matrix)

    def render(self):
#         # PLOT
#         pyplot.ax.clear()
#         pyplot.ax.set_xlim3d(-80,80,20)
#         pyplot.ax.set_ylim3d(-80,80,20)
#         pyplot.ax.set_zlim3d(0,300,20)
#         pyplot.ax.view_init(27, 152) #Elevation, Azimuth

#         # self.Matrix.norm().plot() # Normalize before plotting
#         pyplot.ax.add_collection3d(self.base_shape)

#         self.plat_vert = [list(zip(self.plat_coord_x,self.plat_coord_y,self.plat_coord_z))]
#         self.platform_shape = Poly3DCollection(self.plat_vert)
#         self.platform_shape.set_facecolor('green')
#         pyplot.ax.add_collection3d(self.platform_shape)




        ## SEND DATA
        if (self.reset !=0):
            for i in range(6):
                ESP.write(bytes(str(int(self.reset))+",","ascii"))
            ESP.write(bytes("\n","ascii"))
            if (self.reset == -1):
                print("Real Measurement")
                print(ESP.readline().decode())
                ESP.reset_input_buffer()
            if (self.reset == -2):
                print("Reset")
                ESP.reset_input_buffer()
    

        else:
            for i in range(6):
                ESP.write(bytes(str(int(self.joint_length[i]))+",","ascii"))
            ESP.write(bytes("\n","ascii"))
            print("ESP")
            print(ESP.readline().decode())
            ESP.reset_input_buffer()


        # for i in range(6):
        #     xs = [self.base_coord[i][0], self.plat_coord[i][0]]
        #     ys = [self.base_coord[i][1], self.plat_coord[i][1]]
        #     zs = [self.base_coord[i][2], self.plat_coord[i][2]]
        # pyplot.ax.plot(xs,ys,zs)

        pass
        # print(self.button_data)
        # print("x: ", self.x, "y: ", self.y, "z: ", self.z, "roll: ", self.r, "pitch: ", self.p, "yaw: ", self.yaw)
        # print(self.Matrix)
        # self.Matrix.plot()
        # display(self.fig)
        # clear_output(wait = True)

        

    def run(self):
        start_time = time.time()
        counter_time = time.time()
        ups = 0
        fps = 0 
        while(True): # Run the loop
            if (time.time() - start_time > 0.0167):
                self.update()
                start_time = time.time()
                ups +=1            
                self.render()
                fps +=1
            if (time.time() - counter_time >1):
                print("ups: ", ups, "fps: ", fps)
                ups = 0 
                fps = 0
                counter_time = time.time()




if __name__ == "__main__":
    ESP = serial.Serial("COM3")
    print(ESP.name)
    print(ESP.is_open)
    # pyplot = rtb.backends.PyPlot.PyPlot()
    # pyplot.launch()
    ps4 = PS4Controller()
    ps4.init()
    ps4.run()
    

