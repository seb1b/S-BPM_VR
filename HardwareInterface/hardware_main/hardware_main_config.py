#!/usr/bin/env python

import collections, pika, sys
import untangle  #for config file read in
import os.path
if sys.path[0] != '../../Controller': sys.path.insert(0, '../../Controller')

# Uncomment for standalone use
import controller

# from controller import Controller
import threading
import itertools
"""
# Uncomment for standalone use
class Controller:
	def press(self, pos, user_id, is_left=False):
		if is_left:
			print("press with left at", pos)
		else:
			print("press with right at", pos)
	def release(self, pos, user_id, is_left=False):
		if is_left:
			print("release with left at", pos)
		else:
			print("release with right at", pos)
	def move(self, pos, user_id, is_left=False):
		pass
#		#print("move", pos, is_lef)
#		if is_left:
#			print("move with left at", pos)
#		else:
#			print("move with right at", pos)
	def zoom(self, level, user_id):
		print("zoom")
	def fade_away(self, user_id):
		counter = 0
		counter = counter+1
		print("fade_away", counter)
	def fade_in(self, pos, user_id, is_left):
		print("fade_in at", pos)
	def rotate(self, degrees):
		print("rotate")
	def move_model(self, pos, user_id):
		print("move_model at", pos)
	def move_head(self, pos, degrees, user_id):
		print("move_head")
"""

class VRHardware():

	def __init__(self, controller):
		self.controller = controller

		config_file = '../../HardwareInterface/hardware_main/config.xml'
		if not os.path.isfile(config_file):
			config_file = 'config.xml'
		config = untangle.parse(config_file)

		# TODO Any way to make this constant?
		self.LEAP_ID = int(config.node.inputMethods.leap['id'])
		self.MYO_ID = int(config.node.inputMethods.myo['id'])
		self.KINECT_ID = int(config.node.inputMethods.kinect['id'])
		self.TABLET_ID = int(config.node.inputMethods.tablet['id'])



		# set leap control
		self.leap_press = config.node.leapGestures.press['id']
		self.leap_move = config.node.leapGestures.move['id']
		self.leap_zoom_in = config.node.leapGestures.zoom_in['id']
		self.leap_zoom_out = config.node.leapGestures.zoom_out['id']
		self.leap_fade_in = config.node.leapGestures.fade_in['id']

		# leap cache setup
		self.leap_press_cache = int(config.node.leapParameters.press_cache['id'])
		self.leap_release_cache = int(config.node.leapParameters.release_cache['id'])
		self.leap_zoom_in_cache = int(config.node.leapParameters.zoom_in_cache['id'])
		self.leap_zoom_out_cache = int(config.node.leapParameters.zoom_out_cache['id'])

		#leap parameters
		self.zoom_factor = int(config.node.leapParameters.zoom_factor['id'])
		self.leap_offset_hand = float(config.node.leapParameters.offset_hand['id'])
		self.leap_filter_n = float(config.node.leapParameters.filter_n['id'])

		# set myo control
		self.myo_press = config.node.myoGestures.press['id']
		self.myo_release = config.node.myoGestures.release['id']
		self.myo_zoom = config.node.myoGestures.zoom['id']
		self.myo_move_model = config.node.myoGestures.move_model['id']
		self.myo_fade_in = config.node.myoGestures.fade_in['id']
		self.myo_fade_away = config.node.myoGestures.fade_away['id']

		#set kinect control
		self.kinect_press = config.node.kinectGestures.press['id']
		self.kinect_release = config.node.kinectGestures.release['id']

		#set rabbitMq
		self.host_name = config.node.rabbitMq.host_name["id"]
		self.queue_name = config.node.rabbitMq.queue_name["id"]



		# Variables used for Leap control
		self.cache_left = collections.deque(list(), 200)
		self.cache_right = collections.deque(list(), 200)
		self.called_press_left_leap = False
		self.called_press_right_leap = False
		self.leap_filter = collections.deque(list(), self.leap_filter_n)
		self.leap_filter_right = collections.deque(list(), self.leap_filter_n)

		# Variables used for Myo control
		self.called_press_myo = False
		self.fist_counter = 0

		# Variables used for Kinect
		self.called_press_left_kinect = False
		self.called_press_right_kinect = False

		# Initialize RabbitMq communication
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name))
		self.channel = self.connection.channel()

		self.channel.queue_declare(queue=self.queue_name)
		self.channel.queue_purge(queue=self.queue_name)
		self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)

		self.print_settings()


	def process(self):
		self.connection.process_data_events()


	def callback(self, ch, method, properties, body):
		if body:
			# Split the body string
			#print body
			bodyParts = body.split(':')
			user_id = int(bodyParts[0])
			pos = bodyParts[1]
			hand_type = bodyParts[2]
			gesture = bodyParts[3]

			is_left = False
			if hand_type == 'L':
				is_left = True

			# LEAP
		#	print "leap leap id " + self.LEAP_ID
		#	print user_id
			if user_id >= self.LEAP_ID and user_id < self.MYO_ID:
				xyz = [float(x) for x in pos.split(",")]
				# MOVE_MODEL
				#print xyz
				if hand_type == 'L':
					xyz = self.filter(xyz,self.leap_filter)
				else:
					xyz = self.filter(xyz,self.leap_filter_right)
				#print xyz
				if (hand_type == 'L') :
					xyz[0] += self.leap_offset_hand
					if(xyz[0]  > 1.0):
						xyz[0]= 1.0
				else :
					xyz[0] -= self.leap_offset_hand
					if(xyz[0]  < 0.0):
						xyz[0]= 0.0
				if gesture == self.leap_move:
					self.controller.move_model(xyz, user_id)

				# All other actions
				else:
					# MOVE
					self.controller.move(xyz, user_id, is_left)

					if is_left:
						self.cache_left.append(gesture)
					else:
						self.cache_right.append(gesture)

					# RELEASE
					# n = 5
					if self.called_press_left_leap and is_left and not self.last_gestures(self.leap_release_cache, self.leap_press, is_left):
						self.called_press_left_leap = False
						self.controller.release(xyz, user_id, is_left)

					if self.called_press_right_leap and not is_left and not self.last_gestures(self.leap_release_cache, self.leap_press, is_left):
						self.called_press_right_leap = False
						self.controller.release(xyz, user_id, is_left)

					# Press
					if gesture == self.leap_press:

						# n = 25
						if is_left and self.last_gestures(self.leap_press_cache, self.leap_press, is_left):
							self.called_press_left_leap = True
							self.controller.press(xyz, user_id, is_left)

						if not is_left and self.last_gestures(self.leap_press_cache, self.leap_press, is_left):
							self.called_press_right_leap = True
							self.controller.press(xyz, user_id, is_left)

					# ZOOM
					elif gesture == self.leap_zoom_in or gesture == self.leap_zoom_out:

						# n = 15
						if is_left:
							if self.last_gestures(self.leap_zoom_in_cache, self.leap_zoom_in, is_left):
								self.controller.zoom(1*self.zoom_factor, user_id)
							elif self.last_gestures(self.leap_zoom_out_cache, self.leap_zoom_out, is_left):
								self.controller.zoom(-1*self.zoom_factor, user_id)

						else:
							if self.last_gestures(self.leap_zoom_in_cache, self.leap_zoom_in, is_left):
								self.controller.zoom(1*self.zoom_factor, user_id)
							elif self.last_gestures(self.leap_zoom_out_cache, self.leap_zoom_out, is_left):
								self.controller.zoom(-1*self.zoom_factor, user_id)
					elif gesture == self.leap_fade_in:
						# n = 1
						self.controller.fade_in(xyz, user_id, is_left)

			# MYO
			elif user_id >= self.MYO_ID and user_id < self.KINECT_ID:
				xyz = [float(x) for x in pos.split(";")[0].split(",")]
				rot = [float(x) for x in pos.split(";")[2].split(",")]
				#box = pos.split(";")[1] 

				# Myo has some additional info
				gesture_split = gesture.split(";")
				edge = gesture_split[1]
				gesture = gesture_split[0]

				# MOVE
				self.controller.move(xyz, user_id, is_left)

				# PRESS
				if gesture == self.myo_press:						
					self.called_press_myo = True
					#print("Myo press")
					self.controller.press(xyz, user_id, is_left)
				#RELEASE
				elif gesture == self.myo_release and self.called_press_myo == True:
					#print("Myo release")
					self.controller.release(xyz, user_id, is_left)
					self.called_press_myo = False

				# ZOOM
				elif gesture == self.myo_zoom:
					print("Myo zoom: " + str(rot[0]))
					if ~is_left:
						if rot[0] > 0.2:
							self.controller.zoom(100, user_id)
						elif rot[0] < -0.2:
							self.controller.zoom(-100, user_id)
					else:
						if rot[0] > -0.2:
							self.controller.zoom(100, user_id)
						elif rot[0] < 0.2:
							self.controller.zoom(-100, user_id)
				# FADE_IN
				elif gesture == self.myo_fade_in:
					#print("Myo fade_in")
					self.controller.fade_in(xyz, user_id, is_left)

				# FADE_AWAY
				elif gesture == self.myo_fade_away:
					#print("Myo fade_in")
					self.controller.fade_away(user_id)

				# MOVE_MODEL
				elif gesture == self.myo_move_model:
					#print("Myo fade_in")
					self.controller.move_model(xyz, user_id)

			elif user_id >= self.KINECT_ID and user_id < self.TABLET_ID:
				xyz = [float(x) for x in pos.split(";")]
				self.controller.move(xyz, user_id, is_left)
				#print xyz
				if gesture == self.kinect_press:
					if is_left:
						print("Kinect left Press")
						self.called_press_left_kinect = True
						self.controller.press(xyz, user_id, is_left)
					else:
						print("Kinect right Press")
						self.called_press_right_kinect = True
						self.controller.press(xyz, user_id, is_left)

				# #RELEASE
				elif gesture == self.kinect_release:
					if is_left and self.called_press_left_kinect:
						print("Kinect left release")
						self.called_press_left_kinect = False
						self.controller.release(xyz, user_id, is_left)
					elif not(is_left) and self.called_press_right_kinect:
						print ("Kinect right release")
						self.called_press_right_kinect = False
						self.controller.release(xyz, user_id, is_left)






	def filter(self, pos, filter):
		filter.append(pos)
		filtered_pos = [0.0]*3
		for i in range(len(filter)):
			filtered_pos[0] += filter[i][0]
			filtered_pos[1] += filter[i][1]
			filtered_pos[2] += filter[i][2]

		filtered_pos[0] = filtered_pos[0]/self.leap_filter_n
		filtered_pos[1] = filtered_pos[1]/self.leap_filter_n
		filtered_pos[2] = filtered_pos[2]/self.leap_filter_n

		return filtered_pos




	# Returns true if the last n elements in cache_left equal gesture, and False else
	# Also returns false, if cache is too small
	def last_gestures(self, n, gesture, is_left):
			if is_left:
				if len(self.cache_left) >= n:
					# Iterate over the last n gestures
					for element in list(itertools.islice(self.cache_left, len(self.cache_left) - n, len(self.cache_left))):
						# If at least one of the elements does not equal gesture, return False
						if element != gesture:
							return False
					return True
				else:
					return False

			else:
				# Returns true if the last n elements in cache_right equal gesture, and False else
				# Also returns false, if cache is too small
				if len(self.cache_right) >= n:
					# Iterate over the last n gestures
					for element in list(itertools.islice(self.cache_right, len(self.cache_right) - n, len(self.cache_right))):
						# If at least one of the elements does not equal gesture, return False
						if element != gesture:
							return False
					return True
				else:
					return False

	def print_settings(self):
		print "______ID Setup________"
		print "Leap: " + str(self.LEAP_ID) + ", Myo: " + str(self.MYO_ID) + ", Kinect: "+str(self.KINECT_ID)
		print "______Gesture Setting_______"
		print "Leap: press: "+ self.leap_press +" ,zoom in: "+self.leap_zoom_in+" ,zoom out: "+ self.leap_zoom_out \
			  + " ,move: "+self.leap_move
		print "LeapParameters release_cache:" + str(self.leap_release_cache) + " ,press_cache: " + str(self.leap_press_cache)\
			  + " ,zoom_in_cache: " + str(self.leap_zoom_in_cache) + " ,zoom_out_cache: "+ str(self.leap_zoom_out_cache)
		print "Myo: press: "+ self.myo_press +" ,release: "+self.myo_release+" ,zoom: "+ self.myo_zoom
		print "Kinect: press: "+ self.kinect_press +" ,release: "+self.kinect_release
		print "______Connection______"
		print "RabbitMq: Host: " + self.host_name + " Queue: " + self.queue_name
		print "______________________"
		print 'VRHardware init done'


def test():
	c = Controller()
	vr = VRHardware(c)

	while True:
		vr.process()

if __name__ == "__main__":
	test()
