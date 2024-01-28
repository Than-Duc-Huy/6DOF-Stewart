import pygame
import sys
from time import *
pygame.init()

WIDTH, HEIGHT = 500,600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
speed = [2,1.5]

ball = pygame.image.load("a.jpg")
ballrect = ball.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	ballrect = ballrect.move(speed)

	if ballrect.left < 0 or ballrect.right > WIDTH:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > HEIGHT:
		speed[1] = -speed[1]

	# screen.fill((0,0,0))
	screen.blit(ball, ballrect)
	pygame.display.flip()
	sleep(0.002)	

# xyzrpy = [0,0,0,0,0,0]
# matrix1 = np.zeros((3,3))

# print(matrix1)