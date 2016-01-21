import VR
import math
import PASS


class View():

	class MenuBarItem():
		def __init__(self, name):
			self.name = name

	menubar_entries = {
		"subject": MenuBarItem("subject"),
		"message": MenuBarItem("message"),
		"copy": MenuBarItem("copy"),
		"edit": MenuBarItem("edit")
		# TODO: finish
	}

	def __init__(self):
		self.ZOOM_STEP = 0.01
		self.MAX_USERS = 5
		self.MAX_DIST = 10
		self.MIN_DIST = 2
		self.offset_x = 0
		self.offset_y = 0
		self.VALID_USER_COLORS = []
		#setup valid user colors
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])
		self.VALID_USER_COLORS.append([0.81, 0.77, 0.66])
		self.VALID_USER_COLORS.append([0.25, 0.19, 0.47])
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])  #TODO
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])  #TODO

		self.BLENDER_PATHS = {}
		self.BLENDER_PATHS['subject'] = '../../View/Blender/Archiv/Subjekt.dae'
		#TODO add path for missing elements

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dic = {}

		#stores user_id and corresponding color
		self.user_colors = {}

		#setup camera parameter
		self.camera_from = [0, 0, self.MAX_DIST]
		self.camera_at = [0, 0, -1.0]
		self.camera_dir = [0, 0, -1]
		self.camera_fov = 0.2

		self.objects = []  # list of objects : PASSProcessModelElement
		self.paths = []  # list of paths

		self.cur_scene = None

		# setup root
		VR.view_root = VR.getRoot().find('Headlight')
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(self.camera_from)
		VR.cam.setAt(self.camera_at)
		VR.cam.setDir(self.camera_dir)
		VR.cam.setFov(self.camera_fov)

		# setup offset
		win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(win_size) == 2
		self.offset_x = win_size[0]  #TODO delete
		self.offset_y = win_size[1]  #TODO delete
		self.scale_y = 2 * self.camera_from[2] * math.tan(self.camera_fov * 0.5)
		self.scale_x = self.scale_y * win_size[0] / win_size[1]

		# set colors
		self.colors = {}
		self.colors['menu_subject'] = [[0.56, 0.78, 0.95]]  # not needed?
		self.colors['menu_message'] = [[0.95, 0.85, 0.56]]  # not needed?
		self.colors['subject'] = [[0.56, 0.78, 0.95]]  # blue
		self.colors['message'] = [[0.95, 0.85, 0.56]]  # orange
		self.colors['send_state'] = [[0.98, 0.69, 0.81]]  # green
		self.colors['receive_state'] = [[0.85, 0.59, 0.98]]  # purple
		self.colors['function_state'] = [[0.74, 0.95, 0.80]]  # rose
		self.colors['state_message'] = [[0.98, 0.98, 0.62]]  # yellow
		self.colors['highlight'] = [[1, 0, 0]]
		
		self.setup_menu_bar()

		#HACK create 3 clickable and movable objects
		self.poly_objects = []
		"""
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
		"""

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

	def set_cur_scene(self, cur_scene):
		self.cur_scene = cur_scene
		self.update_all()

	def get_cur_scene(self):
		return self.cur_scene
		
	def setup_menu_bar(self):
		# setup menu bar edit	
		editPlane = VR.Geometry('edit')
		s = 'Plane '
		s += str(self.scale_x)
		s += ' 0.4 1 1'
		editPlane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		editPlane.setMaterial(material)
		#editPlane.setFrom(1.1, 1, 0)
		editPlane.setFrom(0, -0.5 * self.scale_y + 0.2, 0)
	
		editPlane.setUp(0, -1, 0)
		editPlane.setAt(0, 0, 1)
		editPlane.setDir(0, 0, 1)
		editPlane.setPickable(False)
		editPlane.addTag('edit')	
	
		self.editSite = VR.CEF()
		self.editSite.setMaterial(editPlane.getMaterial())
		self.editSite.open('http://localhost:5500/edit')	
	
		VR.view_root.addChild(editPlane)
		#editSite.addMouse(VR.mydev, editPlane, 0, 2, 3, 4)
		#editSite.addKeyboard(keyboard)
		VR.site = self.editSite	
	
		# setup menu bar metadata
		dataPlane = VR.Geometry('data')
		s = 'Plane '
		s += '0.4 '
		s += str(self.scale_y)
		s += ' 1 1'
		dataPlane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		dataPlane.setMaterial(material)
		dataPlane.setFrom(0.5 * self.scale_x - 0.2, 0, 0)
		dataPlane.setUp(0, -1, 0)
		dataPlane.setAt(0, 0, 1)
		dataPlane.setDir(0, 0, 1)
		dataPlane.setPickable(False)
		dataPlane.addTag('data')	
	
		self.metaSite = VR.CEF()
		self.metaSite.setMaterial(dataPlane.getMaterial())
		# refresh URI with new params depending on highlighted component
		# TODO: create method to convert metacontent array from selected object into URI params
		params = '?' + 'm1_k=key1&m1_v=value1&m2_k=key2&m2_v=value2'
		self.metaSite.open('http://localhost:5500/meta' + params)
	
		VR.view_root.addChild(dataPlane)
		#dataSite.addMouse(mouse, dataPlane, 0, 2, 3, 4)
		#dataSite.addKeyboard(keyboard)
	
		VR.site = {self.editSite, self.metaSite}

	# update entire scene based on given scene self.cur_scene
	def update_all(self):
		#delete current scene
		scene_children = VR.view_root.getChildren()
		for child in scene_children:
			print child
			#VR.view_root.remChild(child)
			child.destroy()
		self.object_dic.clear()
		#todo positions and sizes
		#todo replace with blender models
		if isinstance(self.cur_scene, PASS.Layer):
			subjects = self.cur_scene.subjects
			message_exchanges = self.cur_scene.messageExchanges

			for subject in subjects:
				assert isinstance(subject, PASS.Subject)
				pos = subject.hasAbstractVisualRepresentation.hasPoint2D
				poly_sub = VR.loadGeometry(self.BLENDER_PATHS['subject'])
				#poly_sub = VR.Geometry('cube')
				#poly_sub.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
				#poly_sub.setMaterial(VR.Material('sample material'))
				poly_sub.setFrom(pos.hasXValue, pos.hasYValue, 0)
				poly_sub.setPickable(True)
				poly_sub.addTag('subject')
				poly_sub.addTag('obj')
				#poly_sub.setColors(self.colors['subject'])
				poly_sub.setPlaneConstraints([0, 0, 1])
				poly_sub.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_sub)
				self.poly_objects.append(poly_sub)
				self.object_dic[subject] = poly_sub
				self.object_dic[poly_sub] = subject
			for message in message_exchanges:
				assert isinstance(message, PASS.MessageExchange)
				pos = message.hasAbstractVisualRepresentation.hasPoint2D
				poly_mes = VR.Geometry('cube')
				poly_mes.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
				poly_mes.setMaterial(VR.Material('sample material'))
				poly_mes.setFrom(pos.hasXValue, pos.hasYValue, 0)
				poly_mes.setPickable(True)
				poly_mes.addTag('message')
				poly_mes.addTag('obj')
				poly_mes.setColors(self.colors['message'])
				poly_mes.setPlaneConstraints([0, 0, 1])
				poly_mes.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_mes)
				self.poly_objects.append(poly_mes)
				self.draw_line(message)
				self.object_dic[message] = poly_mes
				self.object_dic[poly_mes] = message

		elif isinstance(self.cur_scene, PASS.Behavior):
			states = self.cur_scene.hasState
			edges = self.cur_scene.hasEdge

			for state in states:
				assert isinstance(state, PASS.State)
				pos = state.hasAbstractVisualRepresentation.hasPoint2D
				poly_state = VR.Geometry('cube')
				poly_state.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
				poly_state.setMaterial(VR.Material('sample material'))
				poly_state.setFrom(pos.hasXValue, pos.hasYValue, 0)
				poly_state.setPickable(True)
				if isinstance(state, PASS.FunctionState):
					poly_state.addTag('function_state')
					poly_state.setColors(self.colors['function_state'])
				elif isinstance(state, PASS.SendState):
					poly_state.addTag('send_state')
					poly_state.setColors(self.colors['send_state'])
				elif isinstance(state, PASS.ReceiveState):
					poly_state.addTag('receive_state')
					poly_state.setColors(self.colors['receive_state'])
				else:
					print 'Failed setting state color.'
				poly_state.addTag('obj')
				poly_state.setPlaneConstraints([0, 0, 1])
				poly_state.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_state)
				self.poly_objects.append(poly_state)
				self.object_dic[state] = poly_state
				self.object_dic[poly_state] = state

			for edge in edges:
				assert isinstance(edge, PASS.TransitionEdge)
				pos = edge.hasAbstractVisualRepresentation.hasPoint2D
				poly_edge = VR.Geometry('cube')
				poly_edge.setPrimitive('Box 0.2 0.2 0.2 1 1 1')
				poly_edge.setMaterial(VR.Material('sample material'))
				poly_edge.setFrom(pos.hasXValue, pos.hasYValue, 0)
				poly_edge.setPickable(True)
				poly_edge.addTag('state_message')
				poly_edge.addTag('obj')
				poly_edge.setColors(self.colors['state_message'])
				poly_edge.setPlaneConstraints([0, 0, 1])
				poly_edge.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_edge)
				self.poly_objects.append(poly_edge)
				self.draw_line(edge)
				self.object_dic[edge] = poly_edge
				self.object_dic[poly_edge] = edge
		else:
			print 'Failed to load current scene: has to be level or behavior'

	def zoom(self, level):
		print(("Zoom level: {}".format(self.current_zoom_level())))
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p, d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] >= self.MAX_DIST and not new_cam_pos[2] <= self.MIN_DIST:
			VR.cam.setFrom(new_cam_pos)
		#TODO add image

	def current_zoom_level(self):
		level = int(float(self.MAX_DIST - VR.cam.getFrom()[2]) / self.ZOOM_STEP)
		assert(level >= 0)
		return level

	def move_cursor(self, pos_ws, user_id, is_left):
		colors = [1]

		assert isinstance(is_left, bool)
		assert isinstance(user_id, int)
		pos_ws = [(pos_ws[0] - 0.5) * self.scale_x, (pos_ws[1] - 0.5) * self.scale_y]
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
			cursor_left.setPrimitive('Sphere 0.03 5')
			cursor_left.setMaterial(VR.Material('sample material'))
			cursor_left.setFrom(0.3, 0, 0.3)
			cursor_left.setPlaneConstraints([0, 0, 1])
			cursor_left.setRotationConstraints([1, 1, 1])
			cursor_left.addTag(str([user_id, True]))
			VR.cam.addChild(cursor_left)
			cursor_right = VR.Geometry('sphere')
			cursor_right.setPrimitive('Sphere 0.03 5')
			cursor_right.setMaterial(VR.Material('sample material'))
			cursor_right.setFrom(1.5, 0, 0.3)
			cursor_right.setPlaneConstraints([0, 0, 1])
			cursor_right.setRotationConstraints([1, 1, 1])
			cursor_right.addTag(str([user_id, False]))
			VR.cam.addChild(cursor_right)
			VR.view_user_cursors[user_id] = {}
			#VR.view_user_cursors[user_id][True] = cursor_left
			#VR.view_user_cursors[user_id][False] = cursor_right
			mydev_l = VR.Device('mydev')
			mydev_l.setBeacon(cursor_left)
			mydev_l.addIntersection(VR.view_root)
			mydev_r = VR.Device('mydev')
			mydev_r.setBeacon(cursor_right)
			mydev_r.addIntersection(VR.view_root)
			self.editSite.addMouse(mydev_l, editPlane, 0, 2, 3, 4)
			self.editSite.addMouse(mydev_r, editPlane, 0, 2, 3, 4)
			self.metaSite.addMouse(mydev_l, editPlane, 0, 2, 3, 4)
			self.metaSite.addMouse(mydev_l, editPlane, 0, 2, 3, 4)
			VR.view_user_cursors[user_id][True] = mydev_l
			VR.view_user_cursors[user_id][False] = mydev_r		
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
		o = self.object_dic[obj]
		assert isinstance(o, VR.Object)
		if highlight:
			o.setColors([[1, 0, 0]])
			return True
		else:
			if isinstance(obj, PASS.Subject):
				o.setColors(self.colors['subject'])
				return True
			elif isinstance(obj, PASS.MessageExchange):
				o.setColors(self.colors['message'])
				return True
			elif isinstance(obj, PASS.SendState):
				o.setColors(self.colors['send_state'])
				return True
			elif isinstance(obj, PASS.ReceiveState):
				o.setColors(self.colors['receive_state'])
				return True
			elif isinstance(obj, PASS.FunctionState):
				o.setColors(self.colors['function_state'])
				return True
			elif isinstance(obj, PASS.TransitionEdge):
				o.setColors(self.colors['state_message'])
				return True
			else:
				print "View Error: no valid object tag"
				return False
		return False

	def highlight_pos(self, pos):  # returns the added highlight
		assert len(pos) == 2

		highlighted_point = VR.Geometry('sphere')
		highlighted_point.setPrimitive('Sphere 0.05 5')
		highlighted_point.setMaterial(VR.Material('sample material'))
		highlighted_point.setFrom(pos[0], pos[1], 0.0) #TODO scaling factor
		highlighted_point.setPlaneConstraints([0, 0, 1])
		highlighted_point.setRotationConstraints([1, 1, 1])
		highlighted_point.setColors([1, 0, 0]) #TODO change color?!
		highlighted_point.setPickable(False)
		highlighted_point.addTag('highlight')
		VR.view_root.addChild(highlighted_point)

		return highlighted_point

	def remove_highlight_pos(self, highlight_pos):  # remove the given highlighted object from scene
		VR.view_root.remChild(highlight_pos)

	def get_scene_object(self, pos_ws):
		vr_pos = [(p - 0.5) for p in pos_ws]
		#print(("View: intersect at {}".format(vr_pos)))
		obj = self.get_intersected_obj(vr_pos)
		if isinstance(obj, VR.Object):
			#print("View: VR object")
			return self.object_dic[obj]  # TODO: return PASS object
		elif obj is not None:
			# MenuBarItem?!
			print("View: MenuBarItem")
			return self.menubar_entries["subject"]  # TODO: return correct item!
		#print(("View: No object at {}".format(pos_ws)))
		return None
		#TODO update when victor finished implementing missing function
		
	def get_object(self, user_id, is_left):
		mydev = VR.view_user_cursors[user_id][is_left].trigger(0, 1)
		if VR.mydev.intersect():
			i = mydev.getIntersected()
			tags = i.getTags()
			if 'edit' in tags:
				mydev.trigger(0,dev.getState())
			elif 'data' in tags:
				pass
			elif 'obj' in tags:
				pass
			else:
				print 'No valid intersected object in get_object'
			print i, i.getName()
			print i, i.getTags()
			#print VR.mydev.getIntersected().getTags()
			#print VR.mydev.getIntersected().getName()
			#print VR.mydev.getIntersected().getID()
		else:
			print 'No intersection. Empty space clicked.'
		return None
		
	def rotate(self, degrees):
		pass

	#HACK
	def get_intersected_obj(self, pos):
		assert len(pos) == 2
		pos = [pos[0] * self.scale_x, pos[1] * self.scale_y]
		for o in self.poly_objects:
			o_pos = o.getFrom()
			if pos[0] < o_pos[0] + 0.2 and pos[0] > o_pos[0] - 0.2 and pos[1] < o_pos[1] + 0.2 and pos[1] > o_pos[1] - 0.2:
				return o
		return None

	def on_change(self, object):
		#  TODO Hack
		if isinstance(object, PASS.Subject) or isinstance(object, PASS.MessageExchange):
			pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
			pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
			
			print pos_x, pos_y
			"""
			bb_min_x = object.getParent(PASS.Layer).getBoundingBox2D()[0][0]
			bb_min_y = object.getParent(PASS.Layer).getBoundingBox2D()[0][1]
			bb_max_x = object.getParent(PASS.Layer).getBoundingBox2D()[1][0]
			bb_max_y = object.getParent(PASS.Layer).getBoundingBox2D()[1][1]
			bb_x_dist = bb_max_x - bb_min_x
			bb_y_dist = bb_max_y - bb_min_y
			"""

			rel_size = 1  # TODO getRelativeSize()
			# find given object
			if not object in self.objects:  # add given object to scene
				self.objects.append(object)
				#create polyVR object and add it to scene #TODO
				poly_obj = VR.Geometry('cube')  #TODO replace with blender model
				primitive_str = 'Box'
				#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
				primitive_str += (' 0.2') * 3
				primitive_str += ' 1' * 3
				poly_obj.setPrimitive(primitive_str)
				poly_obj.setMaterial(VR.Material('sample material'))
				if isinstance(object, PASS.Subject):
					poly_obj.setColors(self.colors['subject'])
					poly_obj.addTag('subject')
				elif isinstance(object, PASS.MessageExchange):
					poly_obj.setColors(self.colors['message'])
					poly_obj.addTag('message')
					self.draw_line(object)
				elif isinstance(object, PASS.SendState):
					poly_obj.setColors(self.colors['send_state'])
					poly_obj.addTag('send_state')
				elif isinstance(object, PASS.ReceiveState):
					poly_obj.setColors(self.colors['receive_state'])
					poly_obj.addTag('receive_state')
				elif isinstance(object, PASS.FunctionState):
					poly_obj.setColors(self.colors['function_state'])
					poly_obj.addTag('function_state')
				elif isinstance(object, PASS.TransitionEdge):
					poly_obj.setColors(self.colors['state_message'])
					poly_obj.addTag('state_message')
					self.draw_line(object)
				#poly_obj.setFrom((pos_x / bb_x_dist) * self.offset_x - self.offset_x / 2.0, (pos_y / bb_y_dist) * self.offset_y - self.offset_y / 2.0, 0.0 )
				#print (pos_x / bb_x_dist) * self.offset_x - self.offset_x / 2.0
				print self.offset_x
				poly_obj.setFrom(pos_x, pos_y, 0.0)
				poly_obj.setPickable(True)
				poly_obj.setPlaneConstraints([0, 0, 1])
				poly_obj.setRotationConstraints([1, 1, 1])

				VR.view_root.addChild(poly_obj)
				self.poly_objects.append(poly_obj)
				self.object_dic[poly_obj] = object
				self.object_dic[object] = poly_obj
			else:  # update given object
				#TODO if object is of type *message: change line
				idx = self.objects.index(object)
				obj = self.poly_objects[idx]  # poly_objects should have the same idx as objects

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
			if start_pos.hasXValue > mid_pos.hasYValue:
				start_dir[1] = -1.0
			elif start_pos.hasYValue < mid_pos.hasYValue:
				start_dir[1] = 1.0
			else:
				if start_pos.hasXValue > mid_pos.hasXValue:
					start_dir[0] = 1.0
				else:
					start_dir[0] = -1.0

			if mid_pos.hasYValue > end_pos.hasYValue:
				end_dir[1] = 1.0
			elif mid_pos.hasYValue < mid_pos.hasYValue:
				end_dir[1] = -1.0
			else:
				if end_pos.hasXValue > mid_pos.hasXValue:
					end_dir[0] = -1.0
				else:
					end_dir[0] = 1.0

			if mid_pos.hasXValue == start_pos.hasXValue or mid_pos.hasXValue == end_pos.hasXValue:
				if mid_pos.hasYValue < start_pos.hasYValue:
					mid_dir[1] = -1.0
				else:
					mid_dir[1] = 1.0
			elif mid_pos.hasXValue > start_pos.hasXValue:
				mid_dir[0] = 1.0
			else:
				mid_dir[0] = -1.0

			ptool = VR.Pathtool()
			self.paths.append(ptool.newPath(None, VR.getRoot().find('Headlight')))
			ptool.extrude(None, self.paths[-1])
			handles = ptool.getHandles(self.paths[-1])
			handles[0].setFrom(start_pos.hasXValue, start_pos.hasYValue, 0.0)
			handles[0].setDir(start_dir[0], start_dir[1], 0.0)
			handles[1].setFrom(mid_pos.hasXValue, mid_pos.hasYValue, 0.0)
			handles[1].setDir(1.0, 0.0, 0.0)
			handles[2].setFrom(end_pos.hasXValue, end_pos.hasYValue, 0.0)
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
		o = self.object_dic[obj]
		assert isinstance(o, VR.Object)
		o.setFrom((pos_ws[0] - 0.5) * self.scale_x, (pos_ws[1] - 0.5) * self.scale_y, 0.0)
