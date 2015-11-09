import VR, sys
if sys.path[0] != './Leap': sys.path.insert(0, './Leap')
import Leap
if not hasattr(VR, 'leap'): VR.leap = Leap.Controller()

frame = VR.leap.frame()
if frame.hands.is_empty: print 'stop'

hand = frame.hands[0]
iL = hand.is_left
iR = hand.is_right

p = hand.palm_position
d = hand.direction
n = hand.palm_normal

pitch = direction.pitch * Leap.RAD_TO_DEG
roll = normal.roll * Leap.RAD_TO_DEG

for gesture in frame.gestures():
        if gesture.type is Leap.Gesture.TYPE_CIRCLE:
            circle = Leap.CircleGesture(gesture)
            print 'Circle radius =', circle.radius
