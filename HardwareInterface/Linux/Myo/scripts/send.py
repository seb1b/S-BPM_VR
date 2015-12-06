#!/usr/bin/env python
import pika


def getChange():
	# initial definitions
	# userID:posXYZ:L/R:Geste
	stringToSend = ""

	# myo = 2, number of users = 1
	userID = "21" #TODO extend for more myos

	# position on the screen:
	# 8 | 1 | 2
	# 7 | 0 | 3
	# 6 | 5 | 4
	position = myo.getBox()

	hand = ""
	h = myo.getArm() # TODO assuming the arm won't change?
	if (h == "left"): #for some reason shows wrong
		hand = "R"
	elif (h == "right"):
		hand = "L"
	else:
		hand = "unknown"

	gesture = myo.getPose()
	stringToSend = userID + ":" + str(position) + ":" + hand + ":" + gesture
	
	return stringToSend	

# Center is set when you first double tap to unlock.
# It is kept unlocked forever
def onUnlock():
	myo.rotSetCenter()
	myo.unlock("hold")


def onPoseEdge(pose, edge):
	# in case you end up pointing to weird directions,
	# just point to where you want the center to be and double tap again
	if (pose == 'doubleTap') and (edge == "on"):
		myo.rotSetCenter()

	stringToSend = getChange()
	channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=stringToSend)
	print("Pose: "+stringToSend)
	#connection.close()


def onBoxChange(box, edge):	
	stringToSend = getChange()
	channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=stringToSend)
	print("Box: "+stringToSend)



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


