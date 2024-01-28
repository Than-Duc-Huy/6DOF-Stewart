import time
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from spatialmath import *
from spatialmath.base.transforms3d import trplot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pygame
import inspect
from IPython.display import display, clear_output





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
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0
        self.p  = 0
        self.yaw = 0
        self.r1 = 0
        self.p1 = 0
        self.yaw1 = 0

        # self.fig , self.ax = plt.subplots(figsize = (10,10),subplot_kw = dict(projection = '3d'))
        # self.ax.set_xlim3d(0,10)
        # self.ax.set_ylim3d(0,10)
        # self.ax.set_zlim3d(0,20)
        # self.ax.set_xlabel("X")
        # self.ax.set_ylabel("Y")
        # self.ax.set_zlabel("Z")



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
            self.z = 0.1
        elif (self.button_data.get(0)): # DOWN Z-
            self.z = -0.1
        else:
            self.z = 0 


        if (self.button_data.get(13)):# LEFT Y+
            self.y = 0.1
        elif (self.button_data.get(14)): # RIGHT Y-
            self.y = -0.1
        else:
            self.y = 0     

        if (self.button_data.get(11)): # FORWARD X+
            self.x = 0.1
        elif (self.button_data.get(12)): # BACKWARD X-
            self.x = -0.1
        else:
            self.x = 0 
    
        self.Matrix = SE3(self.x,self.y,self.z)*self.Matrix

        # RPY
        if (self.axis_data.get(0) == -1): # ROLL LEFT X-
            self.r = -0.1
        elif (self.axis_data.get(0) == 1): # ROLL RIGHT X+
            self.r = 0.1
        else:
            self.r = 0
        self.Matrix = SE3(self.Matrix.t)*SE3.Rx(self.r)*SE3(SO3(self.Matrix))


        
        if (self.axis_data.get(3) == -1):# PITCH DOWN Y+
            self.p = 0.1
        elif (self.axis_data.get(3) == 1): # PITCH UP Y-
            self.p = -0.1
        else: self.p = 0

        self.Matrix = SE3(self.Matrix.t)*SE3.Ry(self.p)*SE3(SO3(self.Matrix))

        if (self.axis_data.get(4) == 1): # YAW LEFT Z+
            self.yaw = 0.1
        elif (self.axis_data.get(5) == 1): # YAW RIGHT Z-
            self.yaw = -0.1
        else: self.yaw = 0

        self.Matrix = SE3(self.Matrix.t)*SE3.Rz(self.yaw)*SE3(SO3(self.Matrix))

        # RESET
        if (self.button_data.get(15)):  # Middle
            self.Matrix = SE3(0,0,0)
        if (self.button_data.get(9)):   # L1
            self.Matrix = SE3(self.Matrix.t)

    def render(self):

        # pyplot.ax.clear()
        # pyplot.ax.set_xlim3d(-5, 5)
        # pyplot.ax.set_ylim3d(-5, 5)
        # pyplot.ax.set_zlim3d(-5, 5)
        # self.Matrix.norm().plot() # Normalize before plotting



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
        plt.ion()
        plt.show()
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
    pyplot = rtb.backends.PyPlot.PyPlot()
    ps4 = PS4Controller()
    ps4.init()
    ps4.run()
    

