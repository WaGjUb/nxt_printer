import nxt
from time import sleep
import threading

MAX_SPEED = 127
PAPER = nxt.PORT_A
RAIL = nxt.PORT_B
PEN = nxt.PORT_C
TOUCH = nxt.PORT_1
RGB = nxt.PORT_3
MOVE_PEN = 53
ERROR = 4
SPEED_PEN = 5
PRINT_SPEED = 40
MIN_MOVE = 20
X_BOUND = 1300
Y_BOUND = 1600
X_POSITIVE = 1
Y_POSITIVE = -1
X_NEGATIVE = -1
Y_NEGATIVE = 1

def initialize(brick, paper, rail, rgb, touch, pen):
	t1 = threading.Thread(target=init_paper, args=(paper, rgb))
	t2 = threading.Thread(target=init_rail, args=(rail, touch))
	try:
		pen.turn(MAX_SPEED/5, MOVE_PEN)
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
	def __init__(self):
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
	#	self.draw_square()
		#self.draw_utf()

	def draw_file(self):
		f = open("without2.utf", 'r')
		thread = False
		for l in f:
			l = l.strip().split(' ')
			print l	
			if len(l) == 1:
				l = l[0]
				if l == "M":
					self.up_pen()
				elif l == "L":
					self.down_pen()
				elif l == "T":
					thread = True
			elif len(l) == 2:
				if thread:
					self.set_position(int(float(l[0])), int(float(l[1])))#, True)
					thread = False
				else:
					self.set_position(int(float(l[0])), int(float(l[1])))
					
		

	def can_move(self, x=0, y=0):
		if ((self.x_pos + x < X_BOUND) and (self.y_pos + Y_BOUND)):
			return True
		else:
			return False

	def set_position(self, x, y, thread=False):
		to_move_x = x - self.x_pos
		to_move_y = y - self.y_pos
		t1 = None
		t2 = None
		threading.Thread(target=self.move, args=(1, 300,self.rail))
		if thread:	
			# move to negative way
			if to_move_x < 0:
				t1 = threading.Thread(target=self.move, args=(X_NEGATIVE, abs(to_move_x), self.rail))
			#move to positive way
			else:
				t1 = threading.Thread(target=self.move, args=(X_POSITIVE, abs(to_move_x), self.rail))
			# move to negative way
			if to_move_y < 0:
				t2 = threading.Thread(target=self.move, args=(Y_NEGATIVE, abs(to_move_y), self.paper))
			#move to positive way
			else:
				t2 = threading.Thread(target=self.move, args=(Y_POSITIVE, abs(to_move_y), self.paper))
		
			t1.start()
			t2.start()
			t1.join()
			t2.join()
		else:
			# move to negative way
			if to_move_x < 0:
				self.move(X_NEGATIVE, abs(to_move_x), self.rail)	
			#move to positive way
			else:
				self.move(X_POSITIVE, abs(to_move_x), self.rail)	
				
			# move to negative way
			if to_move_y < 0:
				self.move(Y_NEGATIVE, abs(to_move_y), self.paper)	
			#move to positive way
			else:
				self.move(Y_POSITIVE, abs(to_move_y), self.paper)	

	def move(self, direction, size, motor):
		motor.reset_position(0)
		if motor == self.paper:
			self.y_pos -= size*direction
		elif motor == self.rail:
			self.x_pos -= size*-direction
		
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
			try:
				self.pen.turn(-SPEED_PEN, MOVE_PEN)
			except:
				pass
			self.pen_is_down = True
			#while True:
			#	self.pen.turn(-SPEED_PEN, MOVE_PEN)
			#	walked = abs(self.pen.get_tacho().rotation_count)
			#	print (walked)
			#	self.pen_is_down = True
			#	if walked >= MOVE_PEN and walked < MOVE_PEN + ERROR:
			#		break
			#	else:
			#		self.up_pen()


	def up_pen(self):
		if self.pen_is_down:
			try:
				self.pen.turn(SPEED_PEN, MOVE_PEN+100)
			except Exception as e:
				print(e)
				self.pen.reset_position(0)
			self.pen.weak_turn(0,0)
			self.pen_is_down = False

	def draw_square(self):
		print("sobe caneta")
		self.up_pen()
		self.set_position(600, 600)
		self.down_pen()
		self.set_position(600, 900)
		self.set_position(900, 900)
		self.set_position(900, 600)
		self.set_position(600, 600)
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


	def draw_utf(self):
		#draw U 
		self.set_position(100,900)
		self.down_pen()
		self.set_position(100,600)
		self.set_position(300,600)
		self.set_position(300,900)
		self.up_pen()

		#draw T
		self.set_position(450,900)
		self.down_pen()
		self.set_position(650,900)
		self.up_pen()
		self.set_position(550,900)
		self.down_pen()
		self.set_position(550,600)
		self.up_pen()
		
		#draw F
		self.set_position(800,600)
		self.down_pen()
		self.set_position(800,900)
		self.set_position(1000,900)
		self.up_pen()
		self.set_position(1000,800)
		self.down_pen()
		self.set_position(800,800)
		self.up_pen()
		
	def draw_logo(self):
		#print U and T
		self.set_position(265,1135)
		self.down_pen()
		self.set_position(265,870)
		self.set_position(470,870)
		self.set_position(470,1090)
		self.set_position(530,1090)
		self.set_position(530,870)
		self.set_position(580,870)
		self.set_position(580,1090)
		self.set_position(785,1090)
		self.set_position(785,1135)
		self.set_position(420,1135)
		self.set_position(420,910)
		self.set_position(315,910)
		self.set_position(315,1135)
		self.set_position(265,1135)
		self.up_pen()

p =	print_file()
try:	
	p.draw_file()	
except KeyboardInterrupt as e:
	p.up_pen()
#print_file.draw_square()
