import pygame
import math
import urllib.request
#import random
import threading
url = "http://192.168.20.108/"  # "http://192.168.20.131/", "http://192.168.20.130/"
angle = 0
x_speed = 0
y_speed = 0
speed = 0
data = ""
curve_track_opacity = True
player_angle = 180
datatup= (0, 0)
BG_COL = (30, 110, 35, 0)
L_COL = (70, 50, 10, 0)
track_dist = 10  #  0 for no track, -1 for infinite track, 1 or more for track that fades  the larger the number the less it fades
s_size = (0, 0)
prev_s_size = (0, 0)
TRACK_COLOUR = (60, 42, 5)
prev_wheel_poses = [(0, 0), (0, 0), (0, 0), (0, 0)]
wheel_poses = [(0, 0), (0, 0), (0, 0), (0, 0)]

def draw_bg(op):
	surf = pygame.Surface(pygame.display.get_window_size())
	surf = surf.convert_alpha()
	surf.fill((BG_COL[0], BG_COL[1], BG_COL[2], op))
	draw_rounded_line(surf, (L_COL[0], L_COL[1], L_COL[2], op), (100, 100), (400, 400), width2=100)
	return surf

def draw_rounded_line(surface, colour, p1, p2, width2=1):
	for i in range(round(math.dist(p1, p2))):
		pygame.draw.circle(surface, colour, ((((p2[0]-p1[0])/math.dist(p1, p2))*i)+p1[0], (((p2[1]-p1[1])/math.dist(p1, p2))*i)+p1[1]), width2//2)

def get_angle(tup):
	a = 100-(tup[1])
	b = 100
	ba = tup[0]+180
	aa = math.degrees(math.asin((a*math.sin(math.radians(ba)))/b))
	ca = (180-aa)-ba
	return ca

def get_data():
	global datatup, done
	while not done
		n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
		n = n.decode("utf-8") # convert raw html bytes format to string

		data = n
		datalist = data.split(", ")
		datatup = tuple(float(i) for i in datalist)
		datatup = (datatup[0] / 1.25, datatup[1])
	# data = n.split() 			#<optional> split datas we got. (if you programmed it to send more than one value) It splits them into seperate list elements.
	# data = list(map(int, data)) #<optional> turn datas to integers, now all list elements are integers.

# Example usage
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), flags=pygame.RESIZABLE)
pygame.display.set_caption("")
done = False
backgroundandtrack = draw_bg(255)
if track_dist>=0:
	backgroundoverlay = draw_bg(255//(track_dist+1))
else:
	backgroundoverlay = draw_bg(0)
x = pygame.display.get_window_size()[0]//2
y = pygame.display.get_window_size()[1]//2
wheel_poses = [(x+(math.sin(math.radians(player_angle-90))*20), y+(math.cos(math.radians(player_angle-90))*20)), (x+(math.sin(math.radians(player_angle+90))*20), y+(math.cos(math.radians(player_angle+90))*20)), (x+(math.sin(math.radians(player_angle-10))*90), y+(math.cos(math.radians(player_angle-10))*90)), (x+(math.sin(math.radians(player_angle+10))*90), y+(math.cos(math.radians(player_angle+10))*90))]
prev_wheel_poses = [listn[:] for listn in wheel_poses]
threading.Thread(target=get_data, daemon=True).start()
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			
	screen.fill((0, 0, 0))
	#datatup = (10, 100)
	clock.tick(60)
	speed += (datatup[1]/18)
	x_speed = (math.sin(math.radians(player_angle))*speed)
	y_speed = (math.cos(math.radians(player_angle))*speed)
	datatup = (datatup[0] / 1.25, datatup[1])
	angle = get_angle((datatup[0], speed))
#	screen.blit(text, (0, 0))
	if not(x<0 or 
	       x>pygame.display.get_window_size()[0] or 
		   y<0 or 
	       y>pygame.display.get_window_size()[1] or 
		   x+(math.sin(math.radians(player_angle+angle))*100)<0 or 
	       x+(math.sin(math.radians(player_angle+angle))*100)>pygame.display.get_window_size()[0] or 
		   y+(math.cos(math.radians(player_angle+angle))*100)<0 or 
	       y+(math.cos(math.radians(player_angle+angle))*100)>pygame.display.get_window_size()[1]):
		player_angle += angle
	if not(x+x_speed<0 or 
	       x+x_speed>pygame.display.get_window_size()[0] or 
		   y+y_speed<0 or 
	       y+y_speed>pygame.display.get_window_size()[1] or 
		   x+x_speed+(math.sin(math.radians(player_angle))*100)<0 or 
	       x+x_speed+(math.sin(math.radians(player_angle))*100)>pygame.display.get_window_size()[0] or 
		   y+y_speed+(math.cos(math.radians(player_angle))*100)<0 or 
	       y+y_speed+(math.cos(math.radians(player_angle))*100)>pygame.display.get_window_size()[1]):
		x += x_speed
		y += y_speed
	s_size = pygame.display.get_window_size()
	if s_size != prev_s_size:
		backgroundandtrack = draw_bg(255)
		if track_dist>=0:
			backgroundoverlay = draw_bg(255//(track_dist+1))
		else:
			backgroundoverlay = draw_bg(0)
	prev_s_size = s_size
	backgroundandtrack.blit(backgroundoverlay, (0, 0))
	screen.blit(backgroundandtrack, (0, 0))
	wheel_poses = [(x+(math.sin(math.radians(player_angle-90))*20), y+(math.cos(math.radians(player_angle-90))*20)), (x+(math.sin(math.radians(player_angle+90))*20), y+(math.cos(math.radians(player_angle+90))*20)), (x+(math.sin(math.radians(player_angle-10))*90), y+(math.cos(math.radians(player_angle-10))*90)), (x+(math.sin(math.radians(player_angle+10))*90), y+(math.cos(math.radians(player_angle+10))*90))]
	pygame.draw.line(screen, (255, 255, 255), (x, y), (x+(math.sin(math.radians(player_angle))*100), y+(math.cos(math.radians(player_angle))*100)), width = 3)# central line
	pygame.draw.line(screen, (255, 255, 255), wheel_poses[0], wheel_poses[1], width = 3)#back wheel axel
	pygame.draw.line(screen, (255, 255, 255), wheel_poses[2], wheel_poses[3], width = 3)#front wheel axel
	pygame.draw.line(screen, (255, 255, 255), (wheel_poses[2][0]+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*-10), wheel_poses[2][1]+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*-10)), (wheel_poses[2][0]+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*10), wheel_poses[2][1]+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (wheel_poses[3][0]+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*-10), wheel_poses[3][1]+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*-10)), (wheel_poses[3][0]+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*10), wheel_poses[3][1]+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (wheel_poses[0][0]+(math.sin(math.radians(player_angle))*-10), wheel_poses[0][1]+(math.cos(math.radians(player_angle))*-10)), (wheel_poses[0][0]+(math.sin(math.radians(player_angle))*10), wheel_poses[0][1]+(math.cos(math.radians(player_angle))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (wheel_poses[1][0]+(math.sin(math.radians(player_angle))*-10), wheel_poses[1][1]+(math.cos(math.radians(player_angle))*-10)), (wheel_poses[1][0]+(math.sin(math.radians(player_angle))*10), wheel_poses[1][1]+(math.cos(math.radians(player_angle))*10)), width = 3)
	pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poses[0], prev_wheel_poses[0], width = 3)
	pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poses[1], prev_wheel_poses[1], width = 3)
	pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poses[2], prev_wheel_poses[2], width = 3)
	pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poses[3], prev_wheel_poses[3], width = 3)
	pygame.draw.polygon(screen, (255, 0, 0), [(x+(math.sin(math.radians(player_angle-90))*15), y+(math.cos(math.radians(player_angle-90))*15)), (x+(math.sin(math.radians(player_angle+90))*15), y+(math.cos(math.radians(player_angle+90))*15)), (x+(math.sin(math.radians(player_angle))*100), y+(math.cos(math.radians(player_angle))*100))])#bonnet
	pygame.display.flip()
	speed *= 0.7
	if player_angle >= 360:
		player_angle -= 360
	if player_angle <= 0:
		player_angle += 360
	prev_wheel_poses = [listn[:] for listn in wheel_poses]
pygame.quit()
