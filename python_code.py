from __future__ import division
import random
import pygame
import math
import urllib.request
import colorsys
import threading
urls = ["http://192.168.0.40/"]#, "http://192.168.0.40/", "http://192.168.0.40/"]  # any set urls you want
cars = len(urls)
nauty_wheel = False
lines = []
angles = []
x_speeds = []
y_speeds = []
speeds = []
wheel_angles = []
data = ""
xs = []
ys = []
size_of_car = 100
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
wheel_poseses2 = []
for i in range(cars):
	wheel_angles.append(0)
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
	wheel_poseses2.append([(0, 0), (0, 0), (0, 0), (0, 0)])

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
def do_crash(line, line2, i):
	global collide_car, crasheds, crashchannels, lines_in_my_car, lines
	if (calculateIntersectPoint(line[0], line[1], line2[0], line2[1]) != None):
		collide_car = True
		if crasheds[i] >= (cars*len(lines_in_my_car))+200:
			crashchannels[i].play(pygame.mixer.Sound("car_crash_sound.ogg"))
		crasheds[i] = 0
	else:
		crasheds[i] += 1
def draw_bg(op):
	global lines
	lines = [((pygame.display.get_window_size()[0]/6, pygame.display.get_window_size()[1]/2), ((pygame.display.get_window_size()[0]/6)*5, pygame.display.get_window_size()[1]/2))]
	surf = pygame.Surface(pygame.display.get_window_size())
	surf = surf.convert_alpha()
	surf.fill((BG_COL[0], BG_COL[1], BG_COL[2], op))
	for linetodraw in lines:
		draw_rounded_line(surf, (L_COL[0], L_COL[1], L_COL[2], op), linetodraw[0], linetodraw[1], width2=4)
	return surf

def draw_rounded_line(surface, colour, p1, p2, width2=1):
	for i in range(round(math.dist(p1, p2))):
		pygame.draw.circle(surface, colour, ((((p2[0]-p1[0])/math.dist(p1, p2))*i)+p1[0], (((p2[1]-p1[1])/math.dist(p1, p2))*i)+p1[1]), width2//2)

def get_angle(tup):
	global size_of_car
	a = size_of_car-(tup[1])
	b = size_of_car
	ba = tup[0]+180
	aa = math.degrees(math.asin((a*math.sin(math.radians(ba)))/b))
	ca = (180-aa)-ba
	return ca

def get_data(index):
	global datatups, done, urls
	while not done:
		try:
			n = urllib.request.urlopen(urls[index], timeout = 1).read() # get the raw html data in bytes (sends request and warn our esp8266)
			n = n.decode("utf-8") # convert raw html bytes format to stringprint("here")
			data = n
			datalist = data.split(", ")
			datatups[index] = tuple(float(i) for i in datalist)
			datatups[index] = (datatups[index][0] / 1.25, datatups[index][1])
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
crasheds = []
backgroundandtrack = draw_bg(255)
if track_dist>=0:
	backgroundoverlay = draw_bg(255//(track_dist+1))
else:
	backgroundoverlay = draw_bg(0)
crashchannels = []
for i in range(cars):
	crasheds.append(cars-1)
	crashchannels.append(pygame.mixer.Channel(i))
	xs[i] = ((i+0.75)*(size_of_car/100)*70)
	ys[i] = pygame.display.get_window_size()[1]-(size_of_car*0.35) 
	wheel_poseses[i] = [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*(size_of_car/100)*20), ys[i]+(math.cos(math.radians(player_angles[i]-90))*(size_of_car/100)*20)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*(size_of_car/100)*20), ys[i]+(math.cos(math.radians(player_angles[i]+90))*(size_of_car/100)*20)), (xs[i]+(math.sin(math.radians(player_angles[i]-10))*(size_of_car/100)*90), ys[i]+(math.cos(math.radians(player_angles[i]-10))*(size_of_car/100)*90)), (xs[i]+(math.sin(math.radians(player_angles[i]+10))*(size_of_car/100)*90), ys[i]+(math.cos(math.radians(player_angles[i]+10))*(size_of_car/100)*90))]
	prev_wheel_poseses[i] = [listn[:] for listn in wheel_poseses[i]]
	threading.Thread(target=get_data, daemon=True, args=[i]).start()
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	screen.fill((0, 0, 0))

	#datatups = list((random.randint(-90, 90), random.randint(20, 30)) for i in range(cars)) # Random for when not using the MMU input
	clock.tick(60)
	for i in range(cars):
		speeds[i] += (size_of_car/100)*(datatups[i][1]/45)
		x_speeds[i] = (math.sin(math.radians(player_angles[i]))*speeds[i])
		y_speeds[i] = (math.cos(math.radians(player_angles[i]))*speeds[i])
		angles[i] = get_angle((datatups[i][0], speeds[i]))
		wheel_poseses2[i] = [(xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]-90))*(size_of_car/100)*20), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]-90))*(size_of_car/100)*20)), (xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]+90))*(size_of_car/100)*20), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]+90))*(size_of_car/100)*20)), (xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]-10))*(size_of_car/100)*90), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]-10))*(size_of_car/100)*90)), (xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]+10))*(size_of_car/100)*90), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]+10))*(size_of_car/100)*90))]
#	screen.blit(text, (0, 0))
		collide_car = False
		lines_in_my_car = [((wheel_poseses2[i][2][0]+(math.sin(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*-10), wheel_poseses2[i][2][1]+(math.cos(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*-10)), (wheel_poseses2[i][2][0]+(math.sin(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*10), wheel_poseses2[i][2][1]+(math.cos(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*10))), 
						   ((wheel_poseses2[i][3][0]+(math.sin(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*-10), wheel_poseses2[i][3][1]+(math.cos(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*-10)), (wheel_poseses2[i][3][0]+(math.sin(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*10), wheel_poseses2[i][3][1]+(math.cos(math.radians(player_angles[i]+angles[i]+(datatups[i][0]*-1)))*(size_of_car/100)*10))), 
						   	(wheel_poseses2[i][2], wheel_poseses2[i][3]), 
							(wheel_poseses2[i][0], wheel_poseses2[i][1]), 
						   ((xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]+90))*(size_of_car/100)*15), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]+90))*(size_of_car/100)*15)), (xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*size_of_car), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*size_of_car))), 
						   ((xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]-90))*(size_of_car/100)*15), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]-90))*(size_of_car/100)*15)), (xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*size_of_car), ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*size_of_car))), 
						   ((wheel_poseses2[i][0][0]+(math.sin(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*-10), wheel_poseses2[i][0][1]+(math.cos(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*-10)), (wheel_poseses2[i][0][0]+(math.sin(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*10), wheel_poseses2[i][0][1]+(math.cos(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*10))), 
						   ((wheel_poseses2[i][1][0]+(math.sin(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*-10), wheel_poseses2[i][1][1]+(math.cos(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*-10)), (wheel_poseses2[i][1][0]+(math.sin(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*10), wheel_poseses2[i][1][1]+(math.cos(math.radians(player_angles[i]+angles[i]))*(size_of_car/100)*10)))]
		for linecollide in lines:
			for (index, line) in enumerate(lines_in_my_car):
				do_crash(line, linecollide, i)
				if index == 1:
					nauty_wheel = collide_car
		for j in range(cars):
			lines_in_their_car = [(wheel_poseses[j][2], wheel_poseses[j][3]), (wheel_poseses[j][0], wheel_poseses[j][1]), ((xs[j]+(math.sin(math.radians(player_angles[j]+90))*(size_of_car/100)*15), ys[j]+(math.cos(math.radians(player_angles[j]+90))*(size_of_car/100)*15)), (xs[j]+(math.sin(math.radians(player_angles[j]))*size_of_car), ys[j]+(math.cos(math.radians(player_angles[j]))*size_of_car))), ((xs[j]+(math.sin(math.radians(player_angles[j]-90))*(size_of_car/100)*15), ys[j]+(math.cos(math.radians(player_angles[j]-90))*(size_of_car/100)*15)), (xs[j]+(math.sin(math.radians(player_angles[j]))*size_of_car), ys[j]+(math.cos(math.radians(player_angles[j]))*size_of_car))),  ((wheel_poseses[j][2][0]+(math.sin(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*-10), wheel_poseses[j][2][1]+(math.cos(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*-10)), (wheel_poseses[j][2][0]+(math.sin(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*10), wheel_poseses[j][2][1]+(math.cos(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*10))), ((wheel_poseses[j][3][0]+(math.sin(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*-10), wheel_poseses[j][3][1]+(math.cos(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*-10)), (wheel_poseses[j][3][0]+(math.sin(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*10), wheel_poseses[j][3][1]+(math.cos(math.radians(player_angles[j]+(datatups[j][0]*-1)))*(size_of_car/100)*10))), ((wheel_poseses[j][1][0]+(math.sin(math.radians(player_angles[j]))*(size_of_car/100)*-10), wheel_poseses[j][1][1]+(math.cos(math.radians(player_angles[j]))*(size_of_car/100)*-10)), (wheel_poseses[j][1][0]+(math.sin(math.radians(player_angles[j]))*(size_of_car/100)*10), wheel_poseses[j][1][1]+(math.cos(math.radians(player_angles[j]))*(size_of_car/100)*10)))]
			if not i==j:
				for (index, line) in enumerate(lines_in_my_car):
					for line2 in lines_in_their_car:
						do_crash(line, line2, i)
						if index == 1 and collide_car:
							nauty_wheel = True
		if not nauty_wheel:
			wheel_angles[i] = datatups[i][0]
		if not(xs[i]+x_speeds[i]<0 or 
				xs[i]+x_speeds[i]>pygame.display.get_window_size()[0] or 
				ys[i]+y_speeds[i]<0 or 
				ys[i]+y_speeds[i]>pygame.display.get_window_size()[1] or 
				xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*size_of_car)<0 or 
				xs[i]+x_speeds[i]+(math.sin(math.radians(player_angles[i]+angles[i]))*size_of_car)>pygame.display.get_window_size()[0] or 
				ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*size_of_car)<0 or 
				ys[i]+y_speeds[i]+(math.cos(math.radians(player_angles[i]+angles[i]))*size_of_car)>pygame.display.get_window_size()[1] or 
				collide_car ):
			xs[i] += x_speeds[i]
			ys[i] += y_speeds[i]
			player_angles[i] += angles[i]
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
		wheel_poseses[i] = [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*(size_of_car/100)*20), ys[i]+(math.cos(math.radians(player_angles[i]-90))*(size_of_car/100)*20)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*(size_of_car/100)*20), ys[i]+(math.cos(math.radians(player_angles[i]+90))*(size_of_car/100)*20)), (xs[i]+(math.sin(math.radians(player_angles[i]-10))*(size_of_car/100)*90), ys[i]+(math.cos(math.radians(player_angles[i]-10))*(size_of_car/100)*90)), (xs[i]+(math.sin(math.radians(player_angles[i]+10))*(size_of_car/100)*90), ys[i]+(math.cos(math.radians(player_angles[i]+10))*(size_of_car/100)*90))]
		pygame.draw.line(screen, (255, 255, 255), (xs[i], ys[i]), (xs[i]+(math.sin(math.radians(player_angles[i]))*size_of_car), ys[i]+(math.cos(math.radians(player_angles[i]))*size_of_car)), width = round((size_of_car/100)*3))# central line
		pygame.draw.line(screen, (255, 255, 255), wheel_poseses[i][0], wheel_poseses[i][1], width = round((size_of_car/100)*3))#back wheel axel
		pygame.draw.line(screen, (255, 255, 255), wheel_poseses[i][2], wheel_poseses[i][3], width = round((size_of_car/100)*3))#front wheel axel
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][2][0]+(math.sin(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*-10), wheel_poseses[i][2][1]+(math.cos(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*-10)), (wheel_poseses[i][2][0]+(math.sin(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*10), wheel_poseses[i][2][1]+(math.cos(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*10)), width = round((size_of_car/100)*3))#wheels
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][3][0]+(math.sin(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*-10), wheel_poseses[i][3][1]+(math.cos(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*-10)), (wheel_poseses[i][3][0]+(math.sin(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*10), wheel_poseses[i][3][1]+(math.cos(math.radians(player_angles[i]+(wheel_angles[i]*-1)))*(size_of_car/100)*10)), width = round((size_of_car/100)*3))#wheels
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][0][0]+(math.sin(math.radians(player_angles[i]))*(size_of_car/100)*-10), wheel_poseses[i][0][1]+(math.cos(math.radians(player_angles[i]))*(size_of_car/100)*-10)), (wheel_poseses[i][0][0]+(math.sin(math.radians(player_angles[i]))*(size_of_car/100)*10), wheel_poseses[i][0][1]+(math.cos(math.radians(player_angles[i]))*(size_of_car/100)*10)), width=round((size_of_car/100)*3))#wheels
		pygame.draw.line(screen, (255, 255, 255), (wheel_poseses[i][1][0]+(math.sin(math.radians(player_angles[i]))*(size_of_car/100)*-10), wheel_poseses[i][1][1]+(math.cos(math.radians(player_angles[i]))*(size_of_car/100)*-10)), (wheel_poseses[i][1][0]+(math.sin(math.radians(player_angles[i]))*(size_of_car/100)*10), wheel_poseses[i][1][1]+(math.cos(math.radians(player_angles[i]))*(size_of_car/100)*10)), width=round((size_of_car/100)*3))#wheels
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][0], prev_wheel_poseses[i][0], width = round((size_of_car/100)*3))
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][1], prev_wheel_poseses[i][1], width = round((size_of_car/100)*3))
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][2], prev_wheel_poseses[i][2], width = round((size_of_car/100)*3))
		pygame.draw.line(backgroundandtrack, TRACK_COLOUR, wheel_poseses[i][3], prev_wheel_poseses[i][3], width = round((size_of_car/100)*3))
		pygame.draw.polygon(screen, tuple(round(i*255) for i in colorsys.hsv_to_rgb(1-(1/cars)*i, 1, 1)), [(xs[i]+(math.sin(math.radians(player_angles[i]-90))*(size_of_car/100)*15), ys[i]+(math.cos(math.radians(player_angles[i]-90))*(size_of_car/100)*15)), (xs[i]+(math.sin(math.radians(player_angles[i]+90))*(size_of_car/100)*15), ys[i]+(math.cos(math.radians(player_angles[i]+90))*(size_of_car/100)*15)), (xs[i]+(math.sin(math.radians(player_angles[i]))*size_of_car), ys[i]+(math.cos(math.radians(player_angles[i]))*size_of_car))])#bonnet
		speeds[i] *= 0.7
		if player_angles[i] >= 360:
			player_angles[i] -= 360
		if player_angles[i] <= 0:
			player_angles[i] += 360
		prev_wheel_poseses[i] = [listn[:] for listn in wheel_poseses[i]]
	pygame.display.flip()
pygame.quit()
