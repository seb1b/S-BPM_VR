# -*- coding: utf-8 -*-
#!/usr/bin/env_python

import sys, thread, time, pika
if sys.path[0] != './Leap': sys.path.insert(0, './Leap')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Vector, Bone, Finger

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    # ID
    # 10: Leap1, 11: Leap2
    # 20: Myo1, 21: Myo2
    # 30: Kinect1, 31: Kinect2
    # 40: Tablet1

    # Connection init 
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

        # The current InteractionBox for the frame.
        box = frame.interaction_box

        # ID:current_handpalm_position_x,current_handpalm_position_y,current_handpalm_position_z:hand_type:current_gesture
        string_to_send = ""

        ID = 10
        current_gesture = ""
        current_handpalm_position_x = ""
        current_handpalm_position_y = ""
        current_handpalm_position_z = ""
        hand_type = ""

        positions_fingertips = [Vector]*5
        distance_fingers = 0.0
        positions_distal_phalanges = [Vector]*5
        distance_distal_phalanges = 0.0


        # Get hands
        for hand in frame.hands:

            hand_type = "L" if hand.is_left else "R"

            # Coordinates from the Leap Motion frame of reference (millimeters) are converted to a range of [0..1] such that
            # the minimum value of the InteractionBox maps to 0 and the maximum value of the InteractionBox maps to 1.
            # The coordinates for normalized points outside the InteractionBox boundaries can be negative or greater than one
            # (unless the clamp parameter is True, which is the default).
            # normalized_point = box.normalize_point(vector, True)

            # Use handpalm
            # current_handpalm_position_x += str(hand.palm_position.x)
            # current_handpalm_position_y += str(hand.palm_position.y)
            # current_handpalm_position_z += str(hand.palm_position.z)

            # Use frontmost finger
            current_handpalm_position_x = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).x)
            current_handpalm_position_y = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).y)
            current_handpalm_position_z = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).z)

            fingers = hand.fingers
            for finger in fingers:
                if finger.is_valid:
                    positions_fingertips[finger.type] = finger.joint_position(Finger.JOINT_TIP)
                    positions_distal_phalanges[finger.type] = finger.bone(Bone.TYPE_DISTAL).next_joint

            # Leave pinky and ring finger out
            for i in range(1, Finger.TYPE_MIDDLE + 1):
                distance_fingers += positions_fingertips[0].distance_to(positions_fingertips[i])
                distance_distal_phalanges += positions_distal_phalanges[0].distance_to(positions_distal_phalanges[i])

            # An open hand has a grab strength of zero. As a hand closes into a fist, its grab strength increases to one.
            # if hand.grab_strength >= 0.8 and 
            if distance_fingers <= 100 and distance_distal_phalanges <= 100:
                current_gesture = "grab"       

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"
                current_gesture = "circle_" + clockwiseness

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                current_gesture = "swipe"

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                current_gesture = "keytap"

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                current_gesture = "screentap"

            # Recognized movements occur over time and have a beginning, a middle, and an end. The state attribute reports where in that sequence this Gesture object falls.

        string_to_send += str(ID) + ":" + str(current_handpalm_position_x) + "," + str(current_handpalm_position_y) + "," + str(current_handpalm_position_z) + ":" + hand_type + ":" + current_gesture
        print "string_to_send: " + string_to_send
		
        if current_handpalm_position_x:
            channel.basic_publish(exchange='',routing_key='hello',body=string_to_send)

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
