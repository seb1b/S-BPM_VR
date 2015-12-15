#!/usr/bin/env python

import collections, pika, sys
if sys.path[0] != '../Controller': sys.path.insert(0, '../Controller')
import controller
#from controller import Controller
import threading
import itertools

'''
class Controller:
	def press(self, pos, user_id, is_left=False):
		print "press"
	def release(self, pos, user_id, is_left=False):
		print "release"
	def move(self, pos, user_id, is_left=False):
		print "move"
	def zoom(self, level):
		print "zoom"
	def fade_away(self):
		print "faed_away"
	def rotate(self, degrees):
		print "rotate"
	def move_model(self, pos, user_id):
		print "move_model"
	def move_head(self, pos, degrees, user_id):
		print "move_head"
'''

class VRHardware():
	
	def __init__(self, controller):	
		self.controller = controller
	
		#TODO any way to make this constant?	
		self.LEAP_ID = 10
		self.MYO_ID = 20
		self.KINECT_ID = 30
		self.TABLET_ID = 40
	
		# variables used for Leap control		
		self.cache = collections.deque(list(), 200)
		self.called_press = False	

		# initialize RabbitMq communication
		# NOTE: we changed stop_ioloop_on_close=True
		#self.connection = pika.SelectConnection(pika.ConnectionParameters(host='localhost'), self.on_connection_open, stop_ioloop_on_close=True) 
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		#self.channel = None
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='hello')
		
		#print ' [*] Waiting for messages. To exit please press CTRL+C'
		# user_id:position_x,position_y,position_z:hand_type:gesture

		self.channel.basic_consume(self.callback, queue='hello', no_ack=True)
		#self.channel.start_consuming()
		#t1 = threading.Thread(target=self.channel.start_consuming)
		#t1.start()
		#self.connection.ioloop.start()
		#t1 = threading.Thread(target=self.connection.ioloop.start)
		#t1.start()
		#print help(self.connection)
		#t1 = threading.Thread(target=self.process)
		#t1.start()
		print 'VRHardware init done'

	def process(self):
		self.connection.process_data_events()

'''
	def on_connection_open(self, unused_connection):
		self.connection.channel(on_open_callback=self.on_channel_open)

	def on_channel_open(self, channel):
		self.channel = channel
		self.channel.exchange_declare(self.on_exchange_declareok, "message", "topic")

	def on_exchange_declareok(self, unused_frame):
		print "on_exchange_declareok(self, unused_frame)"
		self.channel.queue_bind(self.on_bindok, "hello2", "message", "hello2")

	def on_bindok(self, unused_frame):
		#self._consumer_tag = 
		self.channel.basic_consume(self.callback, "hello2")
'''

	def callback(self, ch, method, properties, body):
		if body:
			#split the body string
			bodyParts = body.split(':')
			user_id = int(bodyParts[0])
			pos = bodyParts[1]
			hand_type = bodyParts[2]
			gesture = bodyParts[3]
			
			try:
				xyz = [float(x) for x in pos.split(",")]
			except:
				print pos
				raise ValueError("invalid literal for float(): bla")
			
			is_left = False
			if hand_type == 'L':
				is_left = True
	
			# LEAP
			if user_id >= self.LEAP_ID and user_id < self.MYO_ID:
				
				# MOVE
				self.controller.move(xyz, user_id, is_left)
	
				# Store the last 200 frames
				self.cache.append(gesture)
	
				# PRESS
				if gesture == "grab":
					self.called_press = True
					self.controller.press(xyz, user_id, is_left)
	
				# RELEASE
				# If press() has been called but released() has not been called yet and the current gesture does not equal 	grab
				elif self.called_press:
					self.controller.release(xyz, user_id, is_left)
					self.called_press = False
	
	
				# ZOOM
				elif gesture == "circle_clockwise" or gesture == "circle_counterclockwise":
					# Iterate over last n gestures
					false_alarm = False
					n = 10 #TODO probably too small for leap
					#for element in self.cache[-n:]:
					if len(self.cache) >= n:
						for element in list(itertools.islice(self.cache, len(self.cache) - n, len(self.cache))):
							# If the circle does not occur at least n times in a row, it will be interpreted as false 	alarm
							if element != gesture:
								false_alarm = True
	
					if not false_alarm:
						if gesture == "circle_clockwise":
							self.controller.zoom(1)
						elif gesture == "circle_counterclockwise":
							self.controller.zoom(-1)
	
			# MYO
			elif user_id >= self.MYO_ID and user_id < self.KINECT_ID:
				# myo has some additional info
				posSplit = pos.split(";")
				box = posSplit[1]
				rot = posSplit[2]			
				pos = posSplit[0] #x,y,z
				
				
				gesSplit = gesture.split(";")
				edge = gesSplit[1]
				gesture = gesSplit[0]
	
				# MOVE
				#TODO normalize position on 0, 1 -> in myo client
				self.controller.move(pos, user_id, is_left)
	
				#PRESS
				if gesture == "fist" and edge == "on":
					self.controller.press(pos, user_id, is_left)
	
				elif gesture == "fist" and edge == "off":
					self.controller.release(pos, user_id, is_left)
				
				#ZOOM
				elif gesture == "fingersSpread":
					#TODO figure out how quaternions work on myo
					if rotX > 0:
						rot(1)
					else:
						rot(-1)

		#self.channel.basic_ack(method.delivery_tag)

def test():
	c = Controller()
	vr = VRHardware(c)

if __name__ == "__main__":
	test()


