from __future__ import division
import pygame
import math
import urllib.request
import colorsys
import threading
def calculateGradient(p1, p2):
   if (p1[0] != p2[0]):
       m = (p1[1] - p2[1]) / (p1[0] - p2[0])
       return m
   else:
       return None
def calculateYAxisIntersect(p, m):
   return  p[1] - (m * p[0])
def getIntersectPoint(p1, p2, p3, p4):
   m1 = calculateGradient(p1, p2)
   m2 = calculateGradient(p3, p4)
   if (m1 != m2):
       if (m1 is not None and m2 is not None):
           b1 = calculateYAxisIntersect(p1, m1)
           b2 = calculateYAxisIntersect(p3, m2)   
           x = (b2 - b1) / (m1 - m2)       
           y = (m1 * x) + b1           
       else:
           if (m1 is None):
               b2 = calculateYAxisIntersect(p3, m2)   
               x = p1[0]
               y = (m2 * x) + b2
           elif (m2 is None):
               b1 = calculateYAxisIntersect(p1, m1)
               x = p3[0]
               y = (m1 * x) + b1           
           else:
               assert False
       return ((x,y),)
   else:
       b1, b2 = None, None
       if m1 is not None:
           b1 = calculateYAxisIntersect(p1, m1)
       if m2 is not None:   
           b2 = calculateYAxisIntersect(p3, m2)
       if b1 == b2:
           return p1,p2,p3,p4
       else:
           return None
def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)
    if p is not None:               
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]       
        r1 = pygame.Rect(p1, (width , height))
        r1.normalize()
        width = p4[0] - p3[0]
        height = p4[1] - p3[1]
        r2 = pygame.Rect(p3, (width, height))
        r2.normalize()  
        tolerance = 1
        if r1.width < tolerance:
            r1.width = tolerance   
        if r1.height < tolerance:
            r1.height = tolerance
        if r2.width < tolerance:
            r2.width = tolerance
        if r2.height < tolerance:
            r2.height = tolerance
        for point in p:                 
            try:    
                res1 = r1.collidepoint(point)
                res2 = r2.collidepoint(point)
                if res1 and res2:
                    point = [int(pp) for pp in point]                                
                    return point
            except:
                str = "point was invalid  ", point                
                print(str)
        return None            
    else:
        return None

urls = ["http://192.168.20.108/", "http://192.168.20.104/", "http://192.168.20.114/"]  # any set urls you want
cars = len(urls)
angles = []
x_speeds = []
y_speeds = []
speeds = []
data = ""
xs = []
ys = []
curve_track_opacity = True
player_angles = []
datatups = []
BG_COL = (30, 110, 35, 0)
L_COL = (70, 50, 10, 0)
track_dist = 10
s_size = (0, 0)
prev_s_size = (0, 0)
TRACK_COLOUR = (60, 42, 5)
prev_wheel_poseses = []
wheel_poseses = []
for i in range(cars):
	xs.append(0)
	ys.append(0)
	x_speeds.append(0)
	speeds.append(0)
	y_speeds.append(0)
	angles.append(0)
	player_angles.append(180)
	datatups.append((0, 0))
	prev_wheel_poseses.append([(0, 0), (0, 0), (0, 0), (0, 0)])
	wheel_poseses.append([(0, 0), (0, 0), (0, 0), (0, 0)])
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
	global datatups, done, cars, urls
	while not done:
		for numb in range(cars):
			try:
				n = urllib.request.urlopen(urls[numb], timeout = 1).read() # get the raw html data in bytes (sends request and warn our esp8266)
				n = n.decode("utf-8") # convert raw html bytes format to string
				
				data = n
				datalist = data.split(", ")
				datatups[numb] = tuple(float(i) for i in datalist)
				datatups[numb] = (datatups[numb][0] / 1.25, datatups[numb][1])
			except:
				pass
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
for i in range(cars):
	xs[i] = ((i+0.75)*(size_of_car/100)*70)
	ys[i] = pygame.display.get_window_size()[1]-(size_of_car*0.35) 
	wheel_poseses[i] = [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*20), ys[i]+(math.cos(math.radians(player_angles[i]-90))*20)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*20), ys[i]+(math.cos(math.radians(player_angles[i]+90))*20)), (xs[i]+(math.sin(math.radians(player_angles[i]-10))*90), ys[i]+(math.cos(math.radians(player_angles[i]-10))*90)), (xs[i]+(math.sin(math.radians(player_angles[i]+10))*90), ys[i]+(math.cos(math.radians(player_angles[i]+10))*90))]
	prev_wheel_poseses[i] = [listn[:] for listn in wheel_poseses[i]]
threading.Thread(target=get_data, daemon=True).start()
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			
	screen.fill((0, 0, 0))
	#datatup = (10, 100)
	clock.tick(6000)
	for i in range(cars):
		speeds[i] += (datatups[i][1]/50)
		x_speeds[i] = (math.sin(math.radians(player_angles[i]))*speeds[i])
		y_speeds[i] = (math.cos(math.radians(player_angles[i]))*speeds[i])
		angles[i] = get_angle((datatups[i][0], speeds[i]))
#	screen.blit(text, (0, 0))
		if not(xs[i]<0 or 
			xs[i]>pygame.display.get_window_size()[0] or 
			ys[i]<0 or 
			ys[i]>pygame.display.get_window_size()[1] or 
			xs[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*100)<0 or 
			xs[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*100)>pygame.display.get_window_size()[0] or 
			ys[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*100)<0 or 
			ys[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*100)>pygame.display.get_window_size()[1]):
			player_angles[i] += angles[i]
		if not(xs[i]+x_speeds[i]<0 or 
			xs[i]+x_speeds[i]>pygame.display.get_window_size()[0] or 
			ys[i]+y_speeds[i]<0 or 
			ys[i]+y_speeds[i]>pygame.display.get_window_size()[1] or 
			xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]))*100)<0 or 
			xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]))*100)>pygame.display.get_window_size()[0] or 
			ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]))*100)<0 or 
			ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]))*100)>pygame.display.get_window_size()[1]):
			xs[i] += x_speeds[i]
			ys[i] += y_speeds[i]
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
	for i in range(cars):
		wheel_poseses[i] = [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*20), ys[i]+(math.cos(math.radians(player_angles[i]-90))*20)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*20), ys[i]+(math.cos(math.radians(player_angles[i]+90))*20)), (xs[i]+(math.sin(math.radians(player_angles[i]-10))*90), ys[i]+(math.cos(math.radians(player_angles[i]-10))*90)), (xs[i]+(math.sin(math.radians(player_angles[i]+10))*90), ys[i]+(math.cos(math.radians(player_angles[i]+10))*90))]
		pygame.draw.line(screen, (255, 255, 255), (xs[i], ys[i]), (xs[i]+(math.sin(math.radians(player_angles[i]))*100), ys[i]+(math.cos(math.radians(player_angles[i]))*100)), width = 3)# central line
		pygame.draw.line(screen, (255, 255, 255), wheel_poseses[i][0], wheel_poseses[i][1], width = 3)#back wheel axel
		pygame.draw.line(screen, (255, 255, 255), wheel_poseses[i][2], wheel_poseses[i][3], width = 3)#front wheel axel
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][2][0]+(math.sin(math.radians(player_angles[i]+(datatups[i][0]*-1)))*-10), wheel_poseses[i][2][1]+(math.cos(math.radians(player_angles[i]+(datatups[i][0]*-1)))*-10)), (wheel_poseses[i][2][0]+(math.sin(math.radians(player_angles[i]+(datatups[i][0]*-1)))*10), wheel_poseses[i][2][1]+(math.cos(math.radians(player_angles[i]+(datatups[i][0]*-1)))*10)), width = 3)
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][3][0]+(math.sin(math.radians(player_angles[i]+(datatups[i][0]*-1)))*-10), wheel_poseses[i][3][1]+(math.cos(math.radians(player_angles[i]+(datatups[i][0]*-1)))*-10)), (wheel_poseses[i][3][0]+(math.sin(math.radians(player_angles[i]+(datatups[i][0]*-1)))*10), wheel_poseses[i][3][1]+(math.cos(math.radians(player_angles[i]+(datatups[i][0]*-1)))*10)), width = 3)
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][0][0]+(math.sin(math.radians(player_angles[i]))*-10), wheel_poseses[i][0][1]+(math.cos(math.radians(player_angles[i]))*-10)), (wheel_poseses[i][0][0]+(math.sin(math.radians(player_angles[i]))*10), wheel_poseses[i][0][1]+(math.cos(math.radians(player_angles[i]))*10)), width = 3)
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][1][0]+(math.sin(math.radians(player_angles[i]))*-10), wheel_poseses[i][1][1]+(math.cos(math.radians(player_angles[i]))*-10)), (wheel_poseses[i][1][0]+(math.sin(math.radians(player_angles[i]))*10), wheel_poseses[i][1][1]+(math.cos(math.radians(player_angles[i]))*10)), width = 3)
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][0], prev_wheel_poseses[i][0], width = 3)
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][1], prev_wheel_poseses[i][1], width = 3)
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][2], prev_wheel_poseses[i][2], width = 3)
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][3], prev_wheel_poseses[i][3], width = 3)
		pygame.draw.polygon(screen, tuple(round(i*255) for i in colorsys.hsv_to_rgb(1-(1/cars)*i, 1, 1)), [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*15), ys[i]+(math.cos(math.radians(player_angles[i]-90))*15)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*15), ys[i]+(math.cos(math.radians(player_angles[i]+90))*15)), (xs[i]+(math.sin(math.radians(player_angles[i]))*100), ys[i]+(math.cos(math.radians(player_angles[i]))*100))])#bonnet
		speeds[i] *= 0.7
		if player_angles[i] >= 360:
			player_angles[i] -= 360
		if player_angles[i] <= 0:
			player_angles[i] += 360
		prev_wheel_poseses[i] = [listn[:] for listn in wheel_poseses[i]]
	pygame.display.flip()
pygame.quit()
