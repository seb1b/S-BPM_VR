#!/usr/bin/env python

import collections, pika, sys
import untangle  #for config file read in
if sys.path[0] != '../Controller': sys.path.insert(0, '../Controller')

# Uncomment for standalone use
# import controller

# from controller import Controller
import threading
import itertools

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
		# if is_left:
		# 	print("move with left at", pos)
		# else:
		# 	print("move with right at", pos)
	def zoom(self, level):
		print "zoom"
	def fade_away(self):
		print "fade_away"
	def rotate(self, degrees):
		print "rotate"
	def move_model(self, pos, user_id):
		print("move_model at", pos)
	def move_head(self, pos, degrees, user_id):
		print "move_head"


class VRHardware():

	def __init__(self, controller):
		self.controller = controller


		config = untangle.parse('config.xml')


		# TODO Any way to make this constant?
		self.LEAP_ID = config.node.inputMethods.leap['id']
		self.MYO_ID = config.node.inputMethods.myo['id']
		self.KINECT_ID = config.node.inputMethods.kinect['id']
		self.TABLET_ID = config.node.inputMethods.tablet['id']

		print self.LEAP_ID + " " + self.MYO_ID + " " + self.KINECT_ID + " " + self.TABLET_ID

		# set leap control
		self.leap_press = config.node.leapGestures.press['id']
		self.leap_move = config.node.leapGestures.move['id']
		self.leap_zoom_in = config.node.leapGestures.zoom_in['id']
		self.leap_zoom_out = config.node.leapGestures.zoom_out['id']

		# set myo control
		self.leap_press = config.node.leapGestures.press['id']
		self.leap_move = config.node.leapGestures.move['id']
		self.leap_zoom_in = config.node.leapGestures.zoom_in['id']
		self.leap_zoom_out = config.node.leapGestures.zoom_out['id']

		#set kinect control

		# Variables used for Leap control
		self.cache_left = collections.deque(list(), 200)
		self.cache_right = collections.deque(list(), 200)
		self.called_press_left_leap = False
		self.called_press_right_leap = False

		# Variables used for Myo control
		self.called_press_myo = False

		# Initialize RabbitMq communication
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.node.rabbitMq.host_name["id"]))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=config.node.rabbitMq.queue_name["id"])

		self.channel.basic_consume(self.callback, queue=config.node.rabbitMq.queue_name["id"], no_ack=True)

		print 'VRHardware init done'

	def process(self):
		self.connection.process_data_events()

	def callback(self, ch, method, properties, body):
		if body:
			# Split the body string
			bodyParts = body.split(':')
			user_id = int(bodyParts[0])
			pos = bodyParts[1]
			hand_type = bodyParts[2]
			gesture = bodyParts[3]

			is_left = False
			if hand_type == 'L':
				is_left = True

			# LEAP
			if user_id >= self.LEAP_ID and user_id < self.MYO_ID:
				xyz = [float(x) for x in pos.split(",")]

				# MOVE_MODEL
				if gesture == "hands_aligned":
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
					if self.called_press_left_leap and is_left and not self.last_gestures(5, "grab", is_left):
						self.controller.release(xyz, user_id, is_left)
						self.called_press_left_leap = False

					if self.called_press_right_leap and not is_left and not self.last_gestures(5, "grab", is_left):
						self.controller.release(xyz, user_id, is_left)
						self.called_press_right_leap = False

					# GRAB
					if gesture == "grab":

						# n = 25
						if is_left and self.last_gestures(25, "grab", is_left):
							self.controller.press(xyz, user_id, is_left)
							self.called_press_left_leap = True

						if not is_left and self.last_gestures(25, "grab", is_left):
							self.controller.press(xyz, user_id, is_left)
							self.called_press_right_leap = True

					# ZOOM
					elif gesture == "circle_clockwise" or gesture == "circle_counterclockwise":

						# n = 15
						if is_left:
							if self.last_gestures(15, "circle_clockwise", is_left):
								self.controller.zoom(1)
							elif self.last_gestures(15, "circle_counterclockwise", is_left):
								self.controller.zoom(-1)

						else:
							if self.last_gestures(15, "circle_clockwise", is_left):
								self.controller.zoom(1)
							elif self.last_gestures(15, "circle_counterclockwise", is_left):
								self.controller.zoom(-1)

			# MYO
			elif user_id >= self.MYO_ID and user_id < self.KINECT_ID:
				xyz = [float(x) for x in pos.split(";")[0].split(",")]
				rot = [float(x) for x in pos.split(";")[2].split(",")]

				# Myo has some additional info
				gesture_split = gesture.split(";")
				edge = gesture_split[1]
				gesture = gesture_split[0]

				# MOVE
				# TODO Normalize position on 0, 1 -> in myo client
				self.controller.move(xyz, user_id, is_left)

				# PRESS
				if gesture == "fist":
					self.called_press_myo = True
					print("Myo press")
					self.controller.press(xyz, user_id, is_left)

				elif gesture == "rest" and self.called_press_myo == True:
					print("Myo release")
					self.controller.release(xyz, user_id, is_left)
					self.called_press_myo = False

				# ZOOM
				elif gesture == "fingersSpread":
					print("Myo zoom: " + str(rot[0]))
					# TODO For left arm different
					if rot[0] > 0.2:
						self.controller.zoom(1)
					elif rot[0] < -0.5:
						self.controller.zoom(-1)

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

def test():
	c = Controller()
	vr = VRHardware(c)

	while True:
		vr.process()

if __name__ == "__main__":
	test()