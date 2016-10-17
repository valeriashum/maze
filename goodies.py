'''
	goodies.py

	Definitions for some example goodies
'''

import random
import numpy as np

import maze
from maze import Goody, UP, DOWN, LEFT, RIGHT, STAY, PING

NOOP = maze.Move("nothing")

class StaticGoody(Goody):
	''' A static goody - does not move from its initial position '''

	def take_turn(self, _obstruction, _ping_response):
		''' Stay where we are '''
		return STAY

		
class RandomGoody(Goody):
	''' A random-walking goody '''

	def take_turn(self, obstruction, _ping_response):
		''' Ignore any ping information, just choose a random direction to walk in, or ping '''
		possibilities = filter(lambda direction: not obstruction[direction], [UP, DOWN, LEFT, RIGHT]) + [PING]
		return random.choice(possibilities)		
			
class OurGoody(Goody):
	''' A random-walking goody '''
	def __init__(self):
		self.ping_loc = 0
		self.ping_mod = 9
		self.direction = NOOP
		self.approach = True
		self.pos_goody, self.pos_baddy = [0,0],[0,0]
		self.abs_goody, self.abs_baddy = 0,0
		self.coord = [[0,0]]
	
	def take_turn(self, obstruction, _ping_response):		
		if self.ping_loc%self.ping_mod == 0: 
			#print(self.ping_loc)
			self.ping_loc = 1
			return PING
		self.ping_loc += 1
		
		if _ping_response is not None:
			for player, position in _ping_response.items():
				if isinstance(player, Goody):
					self.pos_goody = [position.x, position.y]
					self.abs_goody = abs(position.x) + abs(position.y)
					#print("goody", position.x, position.y)
				else:
					#print("baddy", position.x, position.y)
					self.pos_baddy= [position.x,position.y]	
					self.abs_baddy =abs(position.x) + abs(position.y)
			
		quad_goody = np.sign(self.pos_goody) 
		quad_baddy = np.sign(self.pos_baddy) 			
		
		if min(self.abs_baddy,self.abs_goody) < 5 : self.ping_mod = 3
		elif min(self.abs_baddy,self.abs_goody) < 10 : self.ping_mod = 5
		else: self.ping_mod = 10
		
		if (quad_goody == quad_baddy).all == True: 
			if self.abs_baddy<abs_goody: self.approach = False
			else: self.approach = True
		elif self.abs_baddy<5: self.approach = False
		else: self.approach = True
			
		num = len(filter(lambda direction: not obstruction[direction], [UP, DOWN, LEFT, RIGHT]))
		
		def is_good(direction):
			return not obstruction[direction]
			
			
		possibilities = filter(is_good, [UP, DOWN, LEFT, RIGHT])
		
		if self.approach: pos = self.pos_goody
		else: pos = [-x for x in self.pos_baddy]
		rem_list = []
		if pos[0]<0: rem_list.append(RIGHT)
		else: rem_list.append(LEFT)
		
		if pos[1]<0: rem_list.append(UP)
		else: rem_list.append(DOWN)
		
		previous_direction = self.previous(self.direction)
		
		#print("possibilities", possibilities)
		
		
				
		if self.ping_loc >1 and len(possibilities) >1:
			if previous_direction in possibilities:
				possibilities.remove(previous_direction)
				#print("it deleted")
		#print("rem_list", rem_list)
		if random.randint(0,100)<80:
			for thingy in rem_list:
				if thingy in possibilities and len(possibilities)>1:
					possibilities.remove(thingy)
		
		random.shuffle(rem_list)
		#print(rem_list)
		
		#if rem_list in possibilities:
		#	possibilities.remove(rem_list)	

		#print("possibilities", possibilities)	
		
		if num==1: 
			self.direction = random.choice(possibilities)
		#	self.coord.append(coord_change(self, self.coord,self.direction))
			return self.direction
			
		elif num==2: 
			self.direction = random.choice(possibilities)
		#	self.coord.append(self.coord_change(self, self.coord,self.direction))
			return self.direction
			
		elif num==3: 
			self.direction=random.choice(possibilities)
		#	self.coord.append(self.coord_change(self, self.coord,self.direction))
			return self.direction
			
		elif num==4: 
			#print("asdf")
			if self.direction == NOOP: 
				self.direction = random.choice(filter(is_good, [UP, DOWN, LEFT, RIGHT]))
				
			else: pass
			if random.randint(0,100)<80: 
				#self.coord.append(self.coord_change(self, self.coord,self.direction))
				return self.direction
			else: 
				self.direction = random.choice(filter(is_good, [UP, DOWN, LEFT, RIGHT]))
				#self.coord.append(self.coord_change(self, self.coord,self.direction))
				return self.direction

	def previous(self, direction):
		if direction==LEFT: return RIGHT
		elif direction==RIGHT: return LEFT
		elif direction==DOWN: return UP
		elif direction==UP: return DOWN
		print("No previous operation")
		return NOOP
	
	#def coord_change(self, *coord,*direction):
	#	if direction==LEFT: return coord[-1] +[-1,0]
		#elif direction==RIGHT: return coord[-1] +[1,0]
	#	elif direction==DOWN: return coord[-1] +[0,-1]
	#	elif direction==UP: return coord[-1] +[0,1]
	#	print("No previous operation")
	#	return NOOP