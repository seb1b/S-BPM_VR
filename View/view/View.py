import VR
import math

class View():

	def __init__(self):
		self.ZOOM_STEP = 0.1
		self.MAX_USERS = 5
		
		self.camera_from = [1, 0.5, 2]
		self.camera_at = [1, 0.5, -1.0]
		self.camera_dir =[0, 0, -1]
		
		# setup root
		VR.view_root = VR.getRoot().find('Headlight')
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(self.camera_from)
		VR.cam.setAt(self.camera_at)
		VR.cam.setDir(self.camera_dir)
	
		# set colors
		self.colors = {}
		self.colors['menu_subject'] = [[0.56, 0.78, 0.95]]
		self.colors['subject'] = [[0.56, 0.78, 0.95]]
		self.colors['menu_message'] = [[0.95, 0.85, 0.56]]
		self.colors['message'] = [[0.95, 0.85, 0.56]]
		self.colors['highlight'] = [[1, 0, 0]]
		
		#HACK create 3 clickable and movable objects
		self.objects = []
		obj1 = VR.Geometry('cube')
		obj1.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj1.setMaterial(VR.Material('sample material'))
		obj1.setColors(self.colors['subject'])
		obj1.setFrom(0.3, 0.3, 0)
		obj1.setPickable(True)
		obj1.addTag('subject')
		VR.view_root.addChild(obj1)
		self.objects.append(obj1)
		obj2 = VR.Geometry('cube')
		obj2.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj2.setMaterial(VR.Material('sample material'))
		obj2.setColors(self.colors['subject'])
		obj2.setFrom(0.6, 0.3, 0)
		obj2.setPickable(True)
		obj2.addTag('subject')
		VR.view_root.addChild(obj2)
		self.objects.append(obj2)
		obj3 = VR.Geometry('cube')
		obj3.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj3.setMaterial(VR.Material('sample material'))
		obj3.setColors(self.colors['subject'])
		obj3.setFrom(0.5, 0.7, 0)
		obj3.setPickable(True)
		obj3.addTag('subject')
		VR.view_root.addChild(obj3)
		self.objects.append(obj3)
	
		# setup menu bar
		# add subject
		#menu_subject = VR.Geometry('cube')
		#menu_subject.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		#menu_subject.setMaterial(VR.Material('sample material'))
		#menu_subject.setFrom(0.4, 0.2, 0)
		#menu_subject.setPickable(False)
		#menu_subject.addTag('menu_subject')
		#VR.view_root.addChild(menu_subject)
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
		ll.setColors([[0,1,0]])
		ll.setFrom(0,0,0)
		ll.setPickable(False)
		VR.view_root.addChild(ll)
		# right lower
		rl = VR.Geometry('cube')
		rl.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		rl.setMaterial(VR.Material('sample material'))
		rl.setColors([[0,1,0]])
		rl.setFrom(2,0,0)
		rl.setPickable(False)
		VR.view_root.addChild(rl)
		#right upper
		ru = VR.Geometry('cube')
		ru.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		ru.setMaterial(VR.Material('sample material'))
		ru.setColors([[0,1,0]])
		ru.setFrom(2,1,0)
		ru.setPickable(False)
		VR.view_root.addChild(ru)
		#left upper
		lu = VR.Geometry('cube')
		lu.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		lu.setMaterial(VR.Material('sample material'))
		lu.setColors([[0, 1, 0]])
		lu.setFrom(0,1,0)
		lu.setPickable(False)
		VR.view_root.addChild(lu)		

	def zoom(self, level):
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p,d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] < 2:
			VR.cam.setFrom(new_cam_pos)
		
	def move_cursor(self, pos_ws, user_id, is_left):
		colors = [1]

		assert isinstance(is_left, bool)
		assert isinstance(user_id, int)
		pos_ws = [pos_ws[0] * 2, pos_ws[1]]

		if not hasattr(VR, 'view_user_cursors'):
			VR.view_user_cursors = {}
		if not hasattr(VR, 'view_user_colors'):
			VR.view_user_colors = {}
		if not hasattr(VR, 'view_user_positions'):
			VR.view_user_positions = {}

		if user_id not in VR.view_user_cursors:
			assert len(VR.view_user_cursors) < self.MAX_USERS
			cursor_left = VR.Geometry('sphere')
			cursor_left.setPrimitive('Sphere 0.05 5')
			cursor_left.setMaterial(VR.Material('sample material'))
			cursor_left.setFrom(-1, 0, -3)
			cursor_left.addTag(str([user_id, True]))
			VR.view_root.addChild(cursor_left)
			cursor_right = VR.Geometry('sphere')
			cursor_right.setPrimitive('Sphere 0.05 5')
			cursor_right.setMaterial(VR.Material('sample material'))
			cursor_right.setFrom(1, 0, -3)
			cursor_right.addTag(str([user_id, False]))
			VR.view_root.addChild(cursor_right)
			VR.view_user_cursors[user_id] = {}
			VR.view_user_cursors[user_id][True] = cursor_left
			VR.view_user_cursors[user_id][False] = cursor_right
			VR.view_user_colors[user_id] = colors[len(VR.view_user_cursors) - 1]
			VR.view_user_positions[user_id] = {}
			VR.view_user_positions[user_id][True] = [0, 0, 0]
			VR.view_user_positions[user_id][False] = [0, 0, 0]
			print 'init new user done'

		delta = [p_new - p_old for p_new, p_old in zip(pos_ws, VR.view_user_positions[user_id][is_left])]
		length = math.sqrt(sum(d * d for d in delta))
		if length > 0:
			direction = [d / length for d in delta]
		else:
			direction = [0, 1, 0]

		cursor = next((c for c in VR.view_root.getChildren() if c.hasTag(str([user_id, is_left]))), None)
		assert cursor is not None
		path = VR.Path()
		path.set(VR.view_user_positions[user_id][is_left], direction, pos_ws, direction, 2)
		# VR.view_user_cursors[user_id][is_left].animate(path, 2, 0, False)
		cursor.animate(path, 2, 0, False)
		VR.view_user_positions[user_id][is_left] = pos_ws
		#print 'done'
		
	def move_scene(self, translation):
		cam_pos = VR.cam.getFrom()
		assert len(cam_pos) == 3
		assert len(translation) == 2
		new_cam_pos = [cam_pos[0] + translation[0], cam_pos[1] + translation[1], cam_pos[2]]
		VR.cam.setFrom(new_cam_pos)
		
	def set_highlight(self, obj, highlight):
		assert isinstance(highlight, bool)
		if highlight:
			obj.setColors([[1, 0 , 0]])
			return True
		else:
			if obj.hasTag('subject'):
				obj.setColors(self.colors['subject'])
				return True
			elif obj.hasTag('message'):
				obj.setColors(self.colors['message'])
				return True
			else:
				print "Error: no valid object tag"
				return False
		return False
	
	def get_object(self, pos_ws):
		return get_intersected_obj(pos_ws)
		
	def rotate(self, degrees):
		pass
		
	#HACK
	def get_intersected_obj(self, pos):
		assert len(pos) == 2
		pos = [pos[0] * 2, pos[1]]
		for o in self.objects:
			o_pos = o.getFrom
			if pos[0] < o_pos[0] + 0.2 and pos[0] > o_pos[0] - 0.2 and pos[1] < o_pos[1] + 0.2 and pos[1] > o_pos[1] - 0.2:
				return o
		return None
		
	def move_object(self, obj, ws_pos):
		path = VR.Path()
		ws_pos.append(0)
		direction = ws_pos - obj.getFrom()
		path.set(obj.getFrom(), direction, pos_ws, direction, 2)
		# VR.view_user_cursors[user_id][is_left].animate(path, 2, 0, False)
		cursor.animate(path, 2, 0, False)
			
		
	