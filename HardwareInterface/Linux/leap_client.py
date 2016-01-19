# -*- coding: utf-8 -*-
#!/usr/bin/env_python

import sys, thread, time, pika
if sys.path[0] != './Leap': sys.path.insert(0, './Leap')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Vector, Bone, Finger

class SampleListener(Leap.Listener):
    # ID
    # 10: Leap1, 11: Leap2
    # 20: Myo1, 21: Myo2
    # 30: Kinect1, 31: Kinect2
    # 40: Tablet1

    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

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
        box = frame.interaction_box

        # Coordinates from the Leap Motion frame of reference (millimeters) are converted to a range of [0..1] such that
        # the minimum value of the InteractionBox maps to 0 and the maximum value of the InteractionBox maps to 1.
        # The coordinates for normalized points outside the InteractionBox boundaries can be negative or greater than one
        # (unless the clamp parameter is True, which is the default).
        # normalized_point = box.normalize_point(vector, True)

        # The current InteractionBox for the frame


        # HANDS_ALIGNED
        if len(frame.hands) == 2 and self.is_hands_aligned(frame.hands):

            # ID:current_handpalm_position_x,current_handpalm_position_y,current_handpalm_position_z:handtype:current_gesture
            string_to_send = ""

            ID = 10
            current_gesture = ""
            current_handpalm_position_x = ""
            current_handpalm_position_y = ""
            current_handpalm_position_z = ""
            handtype = "None"

            current_gesture = "hands_aligned"

            # Use middle of both handpalms

            mean_position_hands = Leap.Vector((frame.hands[0].palm_position.x + frame.hands[1].palm_position.x) / 2, (frame.hands[0].palm_position.y + frame.hands[1].palm_position.y) / 2, (frame.hands[0].palm_position.z + frame.hands[1].palm_position.z) / 2)


            current_handpalm_position_x = str(box.normalize_point(mean_position_hands).x)
            current_handpalm_position_y = str(box.normalize_point(mean_position_hands).y)
            current_handpalm_position_z = str(box.normalize_point(mean_position_hands).z)

            string_to_send += str(ID) + ":" + str(current_handpalm_position_x) + "," + str(current_handpalm_position_y) + "," + str(current_handpalm_position_z) + ":" + handtype + ":" + current_gesture
            print(string_to_send)

            if current_handpalm_position_x:
                channel.basic_publish(exchange='',routing_key='hello',body=string_to_send)

        # All other actions
        else:
            for hand in frame.hands:

                # ID:current_handpalm_position_x,current_handpalm_position_y,current_handpalm_position_z:handtype:current_gesture
                string_to_send = ""

                ID = 10
                current_gesture = ""
                current_handpalm_position_x = ""
                current_handpalm_position_y = ""
                current_handpalm_position_z = ""

                handtype = "L" if hand.is_left else "R"

                # Use handpalm
                current_handpalm_position_x = str(box.normalize_point(hand.palm_position).x)
                current_handpalm_position_y = str(box.normalize_point(hand.palm_position).y)
                current_handpalm_position_z = str(box.normalize_point(hand.palm_position).z)

                # Use frontmost finger
                # current_handpalm_position_x = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).x)
                # current_handpalm_position_y = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).y)
                # current_handpalm_position_z = str(box.normalize_point(frame.fingers.frontmost.joint_position(Finger.JOINT_TIP)).z)

                if self.is_grab(hand):
                    current_gesture = "grab"

                # Get gestures
                for gesture in frame.gestures():

                    # True if gesture is associated with hand of type handtype, False else
                    if self.is_associated_with_handtype(gesture, handtype):

                        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                            circle = CircleGesture(gesture)

                            # Determine clock direction using the angle between the pointable and the circle normal
                            if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                                clockwiseness = "clockwise"
                            else:
                                clockwiseness = "counterclockwise"

                            current_gesture = "circle_" + clockwiseness

                        elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                            current_gesture = "swipe"

                        elif gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                            current_gesture = "keytap"

                        elif gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                            current_gesture = "screentap"

                string_to_send += str(ID) + ":" + str(current_handpalm_position_x) + "," + str(current_handpalm_position_y) + "," + str(current_handpalm_position_z) + ":" + handtype + ":" + current_gesture
                print(string_to_send)

                if current_handpalm_position_x:
                    channel.basic_publish(exchange='',routing_key='hello',body=string_to_send)

    # Returns True if grab is detected and False else
    def is_grab(self, hand):
        positions_fingertips = [Vector]*5
        positions_distal_phalanges = [Vector]*5
        distance_fingers_to_thumb = 0.0
        distance_distal_phalanges_to_thumb = 0.0

        fingers = hand.fingers

        for finger in fingers:
            if finger.is_valid:
                positions_fingertips[finger.type] = finger.joint_position(Finger.JOINT_TIP)
                positions_distal_phalanges[finger.type] = finger.bone(Bone.TYPE_DISTAL).next_joint

        # pinky and ring finger out
        for i in range(Finger.TYPE_INDEX, Finger.TYPE_MIDDLE + 1):
            distance_fingers_to_thumb += positions_fingertips[0].distance_to(positions_fingertips[i])
            distance_distal_phalanges_to_thumb += positions_distal_phalanges[0].distance_to(positions_distal_phalanges[i])

        # An open hand has a grab strength of zero. As a hand closes into a fist, its grab strength increases to one.
        # print('distance_fingers_to_thumb =', distance_fingers_to_thumb, 'distance_distal_phalanges_to_thumb =', distance_distal_phalanges_to_thumb, 'grab_strength =', hand.grab_strength)
        if distance_fingers_to_thumb <= 100 and distance_distal_phalanges_to_thumb <= 100 and hand.grab_strength >= 0.5:
            return True
        else:
            return False

    def is_hands_aligned(self, hands):
        # Calculate the distance of the handpalm positions
        distance_handpalms = hands[0].palm_position.distance_to(hands[1].palm_position)

        # print('distance_handpalms =', distance_handpalms)

        if distance_handpalms <= 100:
            return True
        else:
            return False

    def is_associated_with_handtype(self, gesture, handtype):
        for hand in gesture.hands:
            if hand.is_left and handtype == "L":
                return True
            elif hand.is_right and handtype == "R":
                return True
            else:
                return False

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
