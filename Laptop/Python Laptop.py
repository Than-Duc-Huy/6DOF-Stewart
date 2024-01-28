import serial

import os
import pprint
import pygame

import numpy as np







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

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        # Variable
        a = 0
        b = 0
        c = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.

                if( self.button_data.get(11) == True ): # UP
                    a += 100
                    if (a > 9000): a = 9000
                if (self.button_data.get(12) == True ): # DOWN
                    a -= 100
                    if (a < 100): a = 0
                if (self.button_data.get(2) == True): # READ
                    c = -1
                    ESP.write(bytes(str(c)+",","ascii"))
                    print(ESP.readline().decode())	
                if (self.button_data.get(1) == True): # ZERO
                    c = -2
                    ESP.write(bytes(str(c)+",","ascii"))
                    print(ESP.readline().decode())	
                    a = 0
                # 
                if (b != a):
                    print("Input: ",a)
                    ESP.write(bytes(str(a)+",","ascii"))
                    # print(ESP.readline().decode())	
                b = a
	



if __name__ == "__main__":
    ESP = serial.Serial("COM12")
    print(ESP.name)
    print(ESP.is_open)

    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
