#!/usr/bin/env python
import pika


def getChange(edge):
	# initial definitions
	# userID:posXYZ:L/R:Geste
	stringToSend = ""

	# myo = 2, number of users = 1
	userID = "20" #TODO extend for more myos

	# position on the screen:
	# 8 | 1 | 2
	# 7 | 0 | 3
	# 6 | 5 | 4
	posBox = myo.getBox()
	#600+myo.rotYaw()*2000, 500-myo.rotPitch()*2000
	x = 600+myo.rotYaw()*2000
	y = 500-myo.rotPitch()*2000
	z = 0

	xRot = myo.rotYaw()
	yRot = myo.rotPitch()
	zRot = myo.rotRoll()
	position = str(x) + "," + str(y) + "," + str(z) + ";" + str(posBox) + ";" + str(xRot) + "," + str(yRot) + "," + str(zRot)

	hand = ""
	h = myo.getArm() # TODO assuming the arm won't change?
	if (h == "left"): #for some reason shows wrong
		hand = "R"
	elif (h == "right"):
		hand = "L"
	else:
		hand = "unknown"

	gesture = myo.getPose()
	gest_edge = gesture + ";" + edge
	stringToSend = userID + ":" + str(position) + ":" + hand + ":" + gest_edge
	
	return stringToSend	

# Center is set when you first double tap to unlock.
# It is kept unlocked forever
def onUnlock(): #TODO check if this is enough
	myo.rotSetCenter()
	myo.unlock("hold")


def onPoseEdge(pose, edge):
	# in case you end up pointing to weird directions,
	# just point to where you want the center to be and double tap again
	if (pose == 'doubleTap') and (edge == "on"):
		myo.rotSetCenter()

	stringToSend = getChange(edge)
	channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=stringToSend)
	print("Pose: "+stringToSend)
	#connection.close()


def onBoxChange(box, edge):	
	stringToSend = getChange(edge)
	channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=stringToSend)
	print("Box: "+stringToSend)



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


