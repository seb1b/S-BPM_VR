# -*- coding: utf-8 -*-
#!/usr/bin/env_python

import sys, thread, time, pika
if sys.path[0] != './Leap': sys.path.insert(0, './Leap')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    # userID
    # 10: Leap1, 11: Leap2
    # 20: Myo1, 21: Myo2
    # 30: Kinect1, 31: Kinect2

    #connection init 
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        # Each Frame object representing a frame contains lists of tracked entities, such as hands, fingers, and tools, as well as recognized gestures and factors describing the overall motion in the scene.
        frame = controller.frame()

        # userID:currentPositionX,currentPositionY,currentPositionZ:handType:currentGesture
        stringToSend = ""

        userID = 10
        currentGesture = ""
        currentPositionX = ""
        currentPositionY = ""
        currentPositionZ = ""
        handType = ""

        # Get hands
        for hand in frame.hands:

            handType = "L" if hand.is_left else "R"

            # palm_position in mm from the Leap Motion Controller origin as a Vector
            
            # vector.normalized returns a normalized copy of vector.
            # A normalized vector has the same direction as the original vector, but with a length of one.

            # vector.is_valid returns True if all of the vector’s components are finite. If any component is NaN or infinite, then this is False.
            # vector.distance_to(other) returns the distance between the point represented by this Vector object and a point represented by the specified Vector object.

            currentPositionX += str(hand.palm_position.x)
            currentPositionY += str(hand.palm_position.y)
            currentPositionZ += str(hand.palm_position.z)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"
                currentGesture = "circle_" + clockwiseness

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                currentGesture = "swipe"

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                currentGesture = "keytap"

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                currentGesture = "screentap"

            # Recognized movements occur over time and have a beginning, a middle, and an end. The state attribute reports where in that sequence this Gesture object falls.
            # stringToSend += self.state_names[gesture.state]

        stringToSend += str(userID) + ":" + str(currentPositionX) + "," + str(currentPositionY) + "," + str(currentPositionZ) + ":" + handType + ":" + currentGesture
        
        channel.basic_publish(exchange='',routing_key='hello',body=stringToSend)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit ..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    main()