import pygame
import math
import urllib.request
url = "http://192.168.0.40/"  # esp prints IP address when started
angle = 0
x = 640
y = 357
x_speed = 0
y_speed = 0
speed = 0
data = ""
player_angle = 180
datatup= (0, 0)
BG_COL = (30, 110, 50)


def get_angle(tup):
	a = 100-(tup[1]/18)
	b = 100
	ba = tup[0]
	aa = 180-math.degrees(math.asin((a*math.sin(math.radians(ba)))/b))
	ca = (180-aa)-ba
	return ca

def get_data():
	global data

	n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
	n = n.decode("utf-8") # convert raw html bytes format to string
	
	data = n
	# data = n.split() 			#<optional> split datas we got. (if you programmed it to send more than one value) It splits them into seperate list elements.
	# data = list(map(int, data)) #<optional> turn datas to integers, now all list elements are integers.

# Example usage
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1281, 756))
done = False
myfont = pygame.font.Font("Orbitron-Regular.ttf",50)
text = myfont.render(str(datatup), True, (255, 255, 255))
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill(BG_COL)
	get_data()
	datalist = data.split(", ")
	datatup = tuple(float(i) for i in datalist)
	#datatup = (30, 40)
	clock.tick(10)
	speed += (datatup[1]/18)
	x_speed = (math.sin(math.radians(player_angle))*speed)
	y_speed = (math.cos(math.radians(player_angle))*speed)
	angle = get_angle((datatup[0]/1.5, speed))*20
	text = myfont.render(str(datatup), True, (255, 255, 255))
	datatup = (datatup[0] / 1.5, datatup[1])
	screen.blit(text, (0, 0))
	player_angle += angle
	if not(x+x_speed<0 or 
	       x+x_speed>1281 or 
		   y+y_speed<0 or 
	       y+y_speed>756 or 
		   x+x_speed+(math.sin(math.radians(player_angle))*100)<0 or 
	       x+x_speed+(math.sin(math.radians(player_angle))*100)>1281 or 
		   y+y_speed+(math.cos(math.radians(player_angle))*100)<0 or 
	       y+y_speed+(math.cos(math.radians(player_angle))*100)>756):
		x += x_speed
		y += y_speed
	pygame.draw.line(screen, (255, 255, 255), (x, y), (x+(math.sin(math.radians(player_angle))*100), y+(math.cos(math.radians(player_angle))*100)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (x+(math.sin(math.radians(player_angle-90))*20), y+(math.cos(math.radians(player_angle-90))*20)), (x+(math.sin(math.radians(player_angle+90))*20), y+(math.cos(math.radians(player_angle+90))*20)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (x+(math.sin(math.radians(player_angle-10))*90), y+(math.cos(math.radians(player_angle-10))*90)), (x+(math.sin(math.radians(player_angle+10))*90), y+(math.cos(math.radians(player_angle+10))*90)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), ((x+(math.sin(math.radians(player_angle-10))*90))+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*-10), (y+(math.cos(math.radians(player_angle-10))*90))+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*-10)), ((x+(math.sin(math.radians(player_angle-10))*90))+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*10), (y+(math.cos(math.radians(player_angle-10))*90))+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), ((x+(math.sin(math.radians(player_angle+10))*90))+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*-10), (y+(math.cos(math.radians(player_angle+10))*90))+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*-10)), ((x+(math.sin(math.radians(player_angle+10))*90))+(math.sin(math.radians(player_angle+(datatup[0]*-1)))*10), (y+(math.cos(math.radians(player_angle+10))*90))+(math.cos(math.radians(player_angle+(datatup[0]*-1)))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (x+(math.sin(math.radians(player_angle-90))*20)+(math.sin(math.radians(player_angle))*-10), y+(math.cos(math.radians(player_angle-90))*20)+(math.cos(math.radians(player_angle))*-10)), (x+(math.sin(math.radians(player_angle-90))*20)+(math.sin(math.radians(player_angle))*10), y+(math.cos(math.radians(player_angle-90))*20)+(math.cos(math.radians(player_angle))*10)), width = 3)
	pygame.draw.line(screen, (255, 255, 255), (x+(math.sin(math.radians(player_angle+90))*20)+(math.sin(math.radians(player_angle))*-10), y+(math.cos(math.radians(player_angle+90))*20)+(math.cos(math.radians(player_angle))*-10)), (x+(math.sin(math.radians(player_angle+90))*20)+(math.sin(math.radians(player_angle))*10), y+(math.cos(math.radians(player_angle+90))*20)+(math.cos(math.radians(player_angle))*10)), width = 3)
	# pygame.draw.polygon(screen, (255, 0, 0), [(x+(math.sin(math.radians(player_angle-90))*15), y+(math.cos(math.radians(player_angle-90))*15)), (x+(math.sin(math.radians(player_angle+90))*15), y+(math.cos(math.radians(player_angle+90))*15)), (x+(math.sin(math.radians(player_angle))*100), y+(math.cos(math.radians(player_angle))*100))])
	pygame.display.flip()
	speed *= 0.7
pygame.quit()
# Ninja666-rgb was 'ere...
