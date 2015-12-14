import VR

class View():

	def __init__(self):    
		# setup root
		VR.view_root = VR.getRoot().find('Headlight')
		
		# set colors
		VR.view_colors = {}
		VR.view_colors['menu_subject'] = [[0.56, 0.78, 0.95]]
		VR.view_colors['subject'] = [[0.56, 0.78, 0.95]]
		VR.view_colors['menu_message'] = [[0.95, 0.85, 0.56]]
		VR.view_colors['message'] = [[0.95, 0.85, 0.56]]
		
		# setup menu bar
		# add subject
		VR.view_subject = VR.Geometry('cube')
		VR.view_subject.setPrimitive('Box 0.5 0.5 0.3 1 1 1')
		VR.view_subject.setMaterial(VR.Material('sample material'))
		VR.view_subject.setFrom(-1.8, 0, -3)
		VR.view_subject.setPickable(False)
		VR.view_subject.addTag('menu_subject')
		VR.view_root.addChild(VR.view_subject)
		# add message
		VR.view_message = VR.Geometry('cube')
		VR.view_message.setPrimitive('Box 0.4 0.2 0.01 1 1 1')
		VR.view_message.setMaterial(VR.Material('sample material'))
		VR.view_message.setFrom(-2, -1, -3)
		VR.view_message.setPickable(False)
		VR.view_message.addTag('menu_message')
		VR.view_root.addChild(VR.view_message) 

	def zoom(level):
		new_cam_pos = [p + d * level for p,d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		VR.cam.setFrom(new_cam_pos)
		
	def move_cursor(pos_ws, user_id, is_left):
		pass
		
	def move_scene(translation):
		pass
		
	