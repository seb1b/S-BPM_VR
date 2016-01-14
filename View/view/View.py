import VR
import math
import PASS

class View():

	def __init__(self):
		self.ZOOM_STEP = 0.01
		self.MAX_USERS = 5
		self.offset_x = 0
		self.offset_y = 0
		self.VALID_USER_COLORS = []
		#setup valid user colors
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])
		self.VALID_USER_COLORS.append([0.81, 0.77, 0.66])
		self.VALID_USER_COLORS.append([0.25, 0.19, 0.47])
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49]) #TODO
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49]) #TODO

		#stores user_id and corresponding color
		self.user_colors = {}
		
		self.camera_from = [1, 0.5, 2]
		self.camera_at = [1, 0.5, -1.0]
		self.camera_dir =[0, 0, -1]

		self.objects = [] #list of objects : PASSProcessModelElement
		self.paths = [] #list of paths
		
		# setup root
		VR.view_root = VR.getRoot().find('Headlight')
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(self.camera_from)
		VR.cam.setAt(self.camera_at)
		VR.cam.setDir(self.camera_dir)

		# setup offset
		win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(win_size) == 2
		self.offset_x = win_size.getSize()[0]
		self.offset_y = win_size.getSize()[1]
	
		# set colors
		self.colors = {}
		self.colors['menu_subject'] = [[0.56, 0.78, 0.95]] #not needed?
		self.colors['menu_message'] = [[0.95, 0.85, 0.56]] #not needed?
		self.colors['subject'] = [[0.56, 0.78, 0.95]] #blue
		self.colors['message'] = [[0.95, 0.85, 0.56]] #orange
		self.colors['send_state'] = [[0.98, 0.69, 0.81]] #green
		self.colors['receive_state'] = [[0.85, 0.59, 0.98]] #purple
		self.colors['function_state'] = [[0.74, 0.95, 0.80]] #rose
		self.colors['state_message'] = [[0.98, 0.98, 0.62]] #yellow
		self.colors['highlight'] = [[1, 0, 0]]
		
		#HACK create 3 clickable and movable objects
		self.poly_objects = []
		obj1 = VR.Geometry('cube')
		obj1.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj1.setMaterial(VR.Material('sample material'))
		obj1.setColors(self.colors['subject'])
		obj1.setFrom(0.3, 0.3, 0.0)
		obj1.setPickable(True)
		obj1.setPlaneConstraints([0, 0, 1])
		obj1.setRotationConstraints([1, 1, 1])
		obj1.addTag('subject')
		VR.view_root.addChild(obj1)
		self.poly_objects.append(obj1)
		obj2 = VR.Geometry('cube')
		obj2.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj2.setMaterial(VR.Material('sample material'))
		obj2.setColors(self.colors['subject'])
		obj2.setFrom(1.5, 0.3, 0.0)
		obj2.setPickable(True)
		obj2.setPlaneConstraints([0, 0, 1])
		obj2.setRotationConstraints([1, 1, 1])
		obj2.addTag('subject')
		VR.view_root.addChild(obj2)
		self.poly_objects.append(obj2)
		obj3 = VR.Geometry('cube')
		obj3.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
		obj3.setMaterial(VR.Material('sample material'))
		obj3.setColors(self.colors['subject'])
		obj3.setFrom(1.0, 0.7, 0.0)
		obj3.setPickable(True)
		obj3.setPlaneConstraints([0, 0, 1])
		obj3.setRotationConstraints([1, 1, 1])
		obj3.addTag('subject')
		VR.view_root.addChild(obj3)
		self.poly_objects.append(obj3)
	
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

		# # add origin and borders
		# # origin: left loser
		# ll = VR.Geometry('cube')
		# ll.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		# ll.setMaterial(VR.Material('sample material'))
		# ll.setColors([[0,1,0]])
		# ll.setFrom(0,0,0)
		# ll.setPickable(False)
		# VR.view_root.addChild(ll)
		# # right lower
		# rl = VR.Geometry('cube')
		# rl.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		# rl.setMaterial(VR.Material('sample material'))
		# rl.setColors([[0,1,0]])
		# rl.setFrom(2,0,0)
		# rl.setPickable(False)
		# VR.view_root.addChild(rl)
		# #right upper
		# ru = VR.Geometry('cube')
		# ru.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		# ru.setMaterial(VR.Material('sample material'))
		# ru.setColors([[0,1,0]])
		# ru.setFrom(2,1,0)
		# ru.setPickable(False)
		# VR.view_root.addChild(ru)
		# #left upper
		# lu = VR.Geometry('cube')
		# lu.setPrimitive('Box 0.05 0.05 0.05 1 1 1')
		# lu.setMaterial(VR.Material('sample material'))
		# lu.setColors([[0, 1, 0]])
		# lu.setFrom(0,1,0)
		# lu.setPickable(False)
		# VR.view_root.addChild(lu)

	def zoom(self, level):
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p,d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] > 2:
			VR.cam.setFrom(new_cam_pos)
		#TODO add image
		
	def move_cursor(self, pos_ws, user_id, is_left):
		colors = [1]

		assert isinstance(is_left, bool)
		assert isinstance(user_id, int)
		pos_ws = [(pos_ws[0] - 0.5) * 2, pos_ws[1] - 0.5]
		pos_ws.append(0)

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
			cursor_left.setFrom(0.5, 0, 0.3)
			cursor_left.setPlaneConstraints([0, 0, 1])
			cursor_left.setRotationConstraints([1, 1, 1])
			cursor_left.addTag(str([user_id, True]))
			VR.cam.addChild(cursor_left)
			cursor_right = VR.Geometry('sphere')
			cursor_right.setPrimitive('Sphere 0.05 5')
			cursor_right.setMaterial(VR.Material('sample material'))
			cursor_right.setFrom(1.5, 0, 0.3)
			cursor_right.setPlaneConstraints([0, 0, 1])
			cursor_right.setRotationConstraints([1, 1, 1])
			cursor_right.addTag(str([user_id, False]))
			VR.cam.addChild(cursor_right)
			VR.view_user_cursors[user_id] = {}
			VR.view_user_cursors[user_id][True] = cursor_left
			VR.view_user_cursors[user_id][False] = cursor_right
			VR.view_user_colors[user_id] = colors[len(VR.view_user_cursors) - 1]
			VR.view_user_positions[user_id] = {}
			VR.view_user_positions[user_id][True] = [0, 0, 0]
			VR.view_user_positions[user_id][False] = [0, 0, 0]
			print 'init new user done'

		#delta = [p_new - p_old for p_new, p_old in zip(pos_ws, VR.view_user_positions[user_id][is_left])]
		#length = math.sqrt(sum(d * d for d in delta))
		#if length > 0:
		#	direction = [d / length for d in delta]
		#else:
		#	direction = [0, 1, 0]

		cursor = next((c for c in VR.cam.getChildren() if c.hasTag(str([user_id, is_left]))), None)
		assert cursor is not None
		#path = VR.Path()
		#path.set(VR.view_user_positions[user_id][is_left], direction, pos_ws, direction, 2)
		# VR.view_user_cursors[user_id][is_left].animate(path, 2, 0, False)
		#cursor.animate(path, 0.01, 0, False)
		cursor.setFrom(pos_ws)
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
			if isinstance(object, PASS.Subject):
				obj.setColors(self.colors['subject'])
				return True
			elif isinstance(object, PASS.MessageExchange):
				obj.setColors(self.colors['message'])
				return True
			elif isinstance(object, PASS.SendState):
				pobj.setColors(self.colors['send_state'])
				return True
			elif isinstance(object, PASS.ReceiveState):
				obj.setColors(self.colors['receive_state'])
				return True
			elif isinstance(object, PASS.FunctionState):
				obj.setColors(self.colors['function_state'])
				return True
			elif isinstance(object, PASS.TransitionEdge):
				obj.setColors(self.colors['state_message'])
				return True
			else:
				print "Error: no valid object tag"
				return False
		return False
	
	def get_object(self, pos_ws):
		return self.get_intersected_obj(pos_ws)
		#TODO update when victor finished implementing missing function
		
	def rotate(self, degrees):
		pass

	#HACK
	def get_intersected_obj(self, pos):
		assert len(pos) == 2
		pos = [pos[0] * 2, pos[1]]
		for o in self.poly_objects:
			o_pos = o.getFrom()
			if pos[0] < o_pos[0] + 0.2 and pos[0] > o_pos[0] - 0.2 and pos[1] < o_pos[1] + 0.2 and pos[1] > o_pos[1] - 0.2:
				return o
		return None

	def on_change(self, object):
		#TODO Hack
		if isinstance(object, PASS.Subject):
			pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
			pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
			
			bb_min_x = object.getParent(PASS.Layer).getBoundingBox2D()[0][0]
			bb_min_y = object.getParent(PASS.Layer).getBoundingBox2D()[0][1]
			bb_max_x = object.getParent(PASS.Layer).getBoundingBox2D()[1][0]
			bb_max_y = object.getParent(PASS.Layer).getBoundingBox2D()[1][1]
			bb_x_dist = bb_max_x - bb_min_x
			bb_y_dist = bb_max_y - bb_min_y
		
		
			rel_size = 1 #TODO getRelativeSize()
			# find given object
			if not object in self.objects: #add given object to scene
				self.objects.append(object)
				#create polyVR object and add it to scene #TODO
				poly_obj = VR.Geometry('cube') #TODO replace with blender model
				primitive_str = 'box'
				#primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
				primitive_str += (' 0.2') * 3
				primitive_str += ' 1' * 3
				poly_obj.setPrimitive(primitive_str)
				poly_obj.setMaterial(VR.Material('sample material'))
				if isinstance(object, PASS.Subject):
					poly_obj.setColor(self.colors['subject'])
					poly_obj.addTag('subject')
				elif isinstance(object, PASS.MessageExchange):
					poly_obj.setColor(self.colors['message'])
					poly_obj.addTag('message')
					self.draw_line(object)
				elif isinstance(object, PASS.SendState):
					poly_obj.setColor(self.colors['send_state'])
					poly_obj.addTag('send_state')
				elif isinstance(object, PASS.ReceiveState):
					poly_obj.setColor(self.colors['receive_state'])
					poly_obj.addTag('receive_state')
				elif isinstance(object, PASS.FunctionState):
					poly_obj.setColor(self.colors['function_state'])
					poly_obj.addTag('function_state')
				elif isinstance(object, PASS.TransitionEdge):
					poly_obj.setColor(self.colors['state_message'])
					poly_obj.addTag('state_message')
					self.draw_line(object)
				poly_obj.setFrom((pos_x / bb_x_dist) * self.offset_x - self.offset_x / 2.0, (pos_y / bb_y_dist) * self.offset_y - self.offset_y / 2.0, 0.0 )
				poly_obj.setPickable(True)
				poly_obj.setPlaneConstraints([0, 0, 1])
				poly_obj.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_obj)
				self.poly_objects.append(poly_obj)
			else: #update given object
				#TODO if object is of type *message: change line
				idx = self.objects.index(object)
				obj = self.poly_objects[idx] #poly_objects should have the same idx as objects

				#set position and size
				primitive_str = 'box'
				primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
				primitive_str += ' 1' * 3
				obj.setPrimitive(primitive_str)
				self.move_object(obj, [pos_x, pos_y])
				#TODO label, parent, hasMetaContent

	def draw_line(self, object):
		assert isinstance(object, PASS.MessageExchange) or isinstance(object, PASS.TransitionEdge)
		start_pos = None
		mid_pos = None
		end_pos = None
		if isinstance(object, PASS.MessageExchange):
			start_pos = object.sender.hasAbstractVisualRepresentation.hasPoint2D
			mid_pos = object.hasAbstractVisualRepresentation.hasPoint2D
			end_pos = object.receiver.hasAbstractVisualRepresentation.hasPoint2D
		elif isinstance(object, PASS.TransitionEdge):
			start_pos = object.hasSourceState.hasAbstractVisualRepresentation.hasPoint2D
			mid_pos = object.hasAbstractVisualRepresentation.hasPoint2D
			end_pos = object.hasTargetState.hasAbstractVisualRepresentation.hasPoint2D

		if start_pos and end_pos:
			#calc directions
			start_dir = [0.0, 0.0]
			mid_dir = [1.0, 0.0]
			end_dir = [0.0, 0.0]
			if start_pos[1] > mid_pos[1]:
				start_dir[1] = -1.0
			elif start_pos[1] < mid_pos[1]:
				start_dir[1] = 1.0
			else:
				if start_pos[0] > mid_pos[0]:
					start_dir[0] = 1.0
				else:
					start_dir[0] = -1.0

			if mid_pos[1] > end_pos[1]:
				end_dir[1] = 1.0
			elif mid_pos[1] < mid_pos[1]:
				end_dir[1] = -1.0
			else:
				if end_pos[0] > mid_pos[0]:
					end_dir[0] = -1.0
				else:
					end_dir[0] = 1.0

			if mid_pos[0] == start_pos[0] or mid_pos[0] == end_pos[0]:
				if mid_pos[1] < start_pos[1]:
					mid_dir[1] = -1.0
				else:
					mid_dir[1] = 1.0
			elif mid_pos[0] > start_pos[0]:
				mid_dir[0] = 1.0
			else:
				mid_dir[0] = -1.0

			ptool = VR.Pathtool()
			ptool.extrude(None, self.paths[-1])
			self.paths.append(ptool.newPath(None, VR.getRoot().find('Headlight')))
			handles = ptool.getHandles(self.paths[-1])
			handles[0].setFrom(start_pos[0], start_pos[1], 0.0)
			handles[0].setDir(start_dir[0], start_dir[1], 0.0)
			handles[1].setFrom(mid_pos[0], mid_pos[1], 0.0)
			handles[1].setDir(1.0, 0.0, 0.0)
			handles[2].setFrom(end_pos[0], end_pos[1], 0.0)
			handles[2].setDir(end_dir[0], end_dir[1], 0.0)
			ptool.update()
		else:
			print "Error getting start and/or end position to draw transition edge"

	def move_object(self, obj, pos_ws):
		assert len(pos_ws) == 2
		#path = VR.Path()
		#pos_ws.append(0)
		#pos_ws[0] = pos_ws[0] * 2
		#direction = [wp - op for wp, op in zip(pos_ws, obj.getFrom())]
		#path.set(obj.getFrom(), direction, pos_ws, direction, 2)
		# VR.view_user_cursors[user_id][is_left].animate(path, 2, 0, False)
		#obj.animate(path, 2, 0, False)
		#obj.setFrom(pos_ws)
		obj.setFrom(pos_ws[0] * self.offset_x - self.offset_x / 2.0, pos_ws[1] * self.offset_y - self.offset_y / 2.0, 0.0)
