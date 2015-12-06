# Center is set when you first double tap to unlock.
# It is kept unlocked forever
def onUnlock():
	myo.rotSetCenter()
	myo.unlock("hold")

# in case you end up pointing to weird directions,
# just point to where you want the center to be and double tap again
def onPoseEdge(pose, edge):
	if (pose == 'doubleTap') and (edge == "on"):
		myo.rotSetCenter()

def onBoxChange(box, edge):
	if myo.getVBox() == 1: myo.keyboard("up_arrow","down","")
	else: myo.keyboard("up_arrow","up","")
	
	if myo.getVBox() == -1: myo.keyboard("down_arrow","down","")
	else: myo.keyboard("down_arrow","up","")
	
	if myo.getHBox() == 1: myo.keyboard("right_arrow","down","")
	else: myo.keyboard("right_arrow","up","")
	
	if myo.getHBox() == -1: myo.keyboard("left_arrow","down","")
	else: myo.keyboard("left_arrow","up","")

	# this debug message will help you understand the logic:
	if edge == "on": print("VBox=",myo.getVBox()," HBox=",myo.getHBox())
