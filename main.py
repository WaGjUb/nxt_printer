import nxt
import threading

MAX_SPEED = 127
PAPER = nxt.PORT_A
RAIL = nxt.PORT_B
PEN = nxt.PORT_C
TOUCH = nxt.PORT_1
RGB = nxt.PORT_3

def initialize(brick, paper, rail, rgb, touch):
	try:
		threading.Thread(target=init_paper, args=(paper, rgb)).start()
		threading.Thread(target=init_rail, args=(rail, touch)).start()
		
	except:
		pass

def init_paper(p_motor, rgb_sensor):
	# if does not work, set 6 to different of 1
	while(rgb_sensor.get_color() != 6):
		try:
			p_motor.turn(MAX_SPEED/2, 5)
		except e:
			print(e)

def init_rail(r_motor, t_sensor):
	while(not t_sensor.get_sample()):
		try:
			r_motor.turn(-MAX_SPEED, 15)
		except e:
			print(e)
		
class print_file(object):
 	# img is an group of coordinates to draw
	def __init__(self, img):
		self.img = img
		# get NXT USB information
		self.brick = nxt.locator.find_one_brick()
		# define motors
		self.paper = nxt.Motor(self.brick, PAPER)	
		self.rail = nxt.Motor(self.brick, RAIL)	
		self.pen = nxt.Motor(self.brick, PEN)	
		# define sensors
		self.touch = nxt.sensor.Touch(self.brick, TOUCH)	
		self.rgb = nxt.sensor.Color20(self.brick, RGB)	
		##init_paper(self.paper, self.rgb)
		#init_rail(self.rail, self.touch)
		initialize(self.brick, self.paper, self.rail, self.rgb, self.touch)

print_file("daniel")
