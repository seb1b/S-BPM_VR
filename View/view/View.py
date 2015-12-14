import VR

class View():

	def __init__(self):
		self.ZOOM_STEP = 0.1
		import VR
	
		VR.view_cam_from = [1, 0.5, -2]
		VR.view_cam_at = [1, 0.5, -1.0]
		VR.view_cam_dir = [0, 0, 1]
		VR.view_cam_world_from = [1, 0.5, -2]
		
		# setup root
		VR.view_root = VR.getRoot().find('Headlight')
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(VR.view_cam_from)
		VR.cam.setAt(VR.view_cam_at)
		VR.cam.setDir(VR.view_cam_dir)
		VR.cam.setWorldFrom(VR.view_cam_world_from)
	
		# set colors
		VR.view_colors = {}
		VR.view_colors['menu_subject'] = [[0.56, 0.78, 0.95]]
		VR.view_colors['subject'] = [[0.56, 0.78, 0.95]]
		VR.view_colors['menu_message'] = [[0.95, 0.85, 0.56]]
		VR.view_colors['message'] = [[0.95, 0.85, 0.56]]
	
		# setup menu bar
		# add subject
		VR.view_subject = VR.Geometry('cube')
		VR.view_subject.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		VR.view_subject.setMaterial(VR.Material('sample material'))
		VR.view_subject.setFrom(0.4, 0.2, 0)
		VR.view_subject.setPickable(False)
		VR.view_subject.addTag('menu_subject')
		VR.view_root.addChild(VR.view_subject)
		# add message
		#VR.view_message = VR.Geometry('cube')
		#VR.view_message.setPrimitive('Box 0.4 0.2 0.01 1 1 1')
		#VR.view_message.setMaterial(VR.Material('sample material'))
		#VR.view_message.setFrom(0.4, 0.4, 0)
		#VR.view_message.setPickable(False)
		#VR.view_message.addTag('menu_message')
		#VR.view_root.addChild(VR.view_message)

		# add origin and borders
		# origin: left loser
		ll = VR.Geometry('cube')
		ll.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		ll.setMaterial(VR.Material('sample material'))
		ll.setColors([[1,0,1]])
		ll.setFrom(0,0,0)
		ll.setPickable(False)
		VR.view_root.addChild(ll)
		# right lower
		rl = VR.Geometry('cube')
		rl.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		rl.setMaterial(VR.Material('sample material'))
		rl.setColors([[1,0,0]])
		rl.setFrom(2,0,0)
		rl.setPickable(False)
		VR.view_root.addChild(rl)
		#right upper
		ru = VR.Geometry('cube')
		ru.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		ru.setMaterial(VR.Material('sample material'))
		ru.setColors([[1,0,0]])
		ru.setFrom(2,1,0)
		ru.setPickable(False)
		VR.view_root.addChild(ru)
		#left upper
		lu = VR.Geometry('cube')
		lu.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		lu.setMaterial(VR.Material('sample material'))
		lu.setColors([[1,0,0]])
		lu.setFrom(0,1,0)
		lu.setPickable(False)
		VR.view_root.addChild(lu)		

	def zoom(level):
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p,d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		VR.cam.setFrom(new_cam_pos)
		
	def move_cursor(pos_ws, user_id, is_left):
		pass
		
	def move_scene(translation):
		pass
		
	