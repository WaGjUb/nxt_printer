import nxt
from time import sleep
import threading

MAX_SPEED = 127
PAPER = nxt.PORT_A
RAIL = nxt.PORT_B
PEN = nxt.PORT_C
TOUCH = nxt.PORT_1
RGB = nxt.PORT_3
MOVE_PEN = 32
SPEED_PEN = 5
PRINT_SPEED = 50
MIN_MOVE = 15
X_BOUND = 1300
Y_BOUND = 1600

def initialize(brick, paper, rail, rgb, touch, pen):
	t1 = threading.Thread(target=init_paper, args=(paper, rgb))
	t2 = threading.Thread(target=init_rail, args=(rail, touch))
	try:
		pen.turn(MAX_SPEED/5, 30)
	except Exception as e:
		print(e)
	#stop to force motor
	pen.weak_turn(0,0)
	pen.reset_position(0)

	try:
		t1.start()
		t2.start()
	except Exception as e:
		print(e)
		
	t1.join()
	t2.join()

def init_paper(p_motor, rgb_sensor):
	# if does not work, set 6 to different of 1
	while(rgb_sensor.get_color() != 6):
		try:
			p_motor.turn(MAX_SPEED/2, 5)
		except Exception as e:
			print(e)

def init_rail(r_motor, t_sensor):
	i = 0
	while(not t_sensor.get_sample()):
		try:
			r_motor.turn(-MAX_SPEED, 15)
			i += 15
		except Exception as e:
			print(e)

#	print(i)
		
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
		self.pen_is_down = False
		self.x_pos = 0
		self.y_pos = Y_BOUND
		initialize(self.brick, self.paper, self.rail, self.rgb, self.touch, self.pen)
		self.t_draw_square()

	def can_move(self, x=0, y=0):
		if ((self.x_pos + x < X_BOUND) and (self.y_pos + Y_BOUND)):
			return True
		else:
			return False

	def set_position(x, y):
		
		

	def move(self, direction, size, motor):
		motor.reset_position(0)
		if motor == self.paper:
			self.y_pos -= size*direction
		while size > 30:
			#TODO verificar se pode mexer
			motor.turn(PRINT_SPEED*direction, size)
			walked = abs(motor.get_tacho().rotation_count)
			size -= walked
			if size < MIN_MOVE:
				size = 0

	def f_move(self, direction, size, motor):
		motor.reset_position(0)
		while size > 30:
			#TODO verificar se pode mexer
			motor.turn(MAX_SPEED*direction, size)
			walked = abs(motor.get_tacho().rotation_count)
			size -= walked
			if size < MIN_MOVE:
				size = 0

	def down_pen(self):
		if not self.pen_is_down:
			self.pen.turn(-SPEED_PEN, MOVE_PEN)
			self.pen_is_down = True
		
	def up_pen(self):
		if self.pen_is_down:
			self.pen.turn(SPEED_PEN, MOVE_PEN)
			self.pen.weak_turn(0,0)
			self.pen_is_down = False

	def draw_square(self):
		print("sobe caneta")
		self.up_pen()
		print("movendo trilho")
		self.move(1, 300, self.rail)
		print("movendo papel")
		self.move(1, 600, self.paper)
		print("desce caneta")
		self.down_pen()
		print("movendo trilho")
		self.move(1, 300, self.rail)
		print("movendo papel")
		self.move(1, 300, self.paper)
		print("movendo trilho")
		self.move(-1, 300, self.rail)
		print("movendo papel")
		self.move(-1, 300, self.paper)
		print("sobe caneta")
		self.up_pen()
		
	def t_draw_square(self):
		print("sobe caneta")
		self.up_pen()
		print("movendo trilho")
		t1 = threading.Thread(target=self.move, args=(1, 300,self.rail))
		print("movendo papel")
		t2 = threading.Thread(target=self.f_move, args=(1, 600,self.paper))
	
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		print("desce caneta")
		self.down_pen()
		print("movendo trilho")
		t1 = threading.Thread(target=self.move, args=(1, 300,self.rail))
		print("movendo papel")
		t2 = threading.Thread(target=self.f_move, args=(1, 300,self.paper))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		print("movendo trilho")
		t1 = threading.Thread(target=self.f_move, args=(1, 300,self.rail))
		print("movendo papel")
		t2 = threading.Thread(target=self.move, args=(-1, 300,self.paper))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		print("sobe caneta")
		self.up_pen()


print_file("daniel")
#print_file.draw_square()
