import VR
import math
import PASS


class View():

	class MenuBarItem():
		def __init__(self, name):
			self.name = name

	def __init__(self):
		self.ZOOM_STEP = 0.01
		self.MAX_USERS = 5
		self.MAX_DIST = 10
		self.CURSOR_DIST = -2
		self.MIN_DIST = 2
		self.VALID_USER_COLORS = []
		#setup valid user colors
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])
		self.VALID_USER_COLORS.append([0.81, 0.77, 0.66])
		self.VALID_USER_COLORS.append([0.25, 0.19, 0.47])
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])  #TODO
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])  #TODO

		self.BLENDER_PATHS = {}
		self.BLENDER_PATHS['subject'] = '../../View/Blender/Prozess/Subjekt.dae'
		#TODO add path for missing elements

		self.menubar_entries = {
			'edit': self.MenuBarItem('edit'),
			'meta': self.MenuBarItem('meta'),
			'layer_add': self.MenuBarItem('layer_add'),
			'behavior_add': self.MenuBarItem('behavior_add')
		}

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dict = {}

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
		self.active_gui_element = None  # edit plane, layer_add plane or behavior_add plane

		# setup root
		root = VR.getRoot().find('Headlight')
		VR.view_root = VR.Transform('world')
		root.addChild(VR.view_root)
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(self.camera_from)
		VR.cam.setAt(self.camera_at)
		VR.cam.setDir(self.camera_dir)
		VR.cam.setFov(self.camera_fov)

		# setup offset
		win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(win_size) == 2
		self.scale_y = 2 * self.camera_from[2] * math.tan(self.camera_fov * 0.5)
		self.scale_x = self.scale_y * win_size[0] / win_size[1]
		self.scale_cursor_y = 2 * abs(self.CURSOR_DIST) * math.tan(self.camera_fov * 0.5)
		self.scale_cursor_x = self.scale_cursor_y * win_size[0] / win_size[1]

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

		# gui elements
		self.setup_menu_bar()

		#test tags
		poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject'], parent='world')
		poly_obj.setScale(0.1, 0.1, 0.1)
		poly_obj.addTag('subject')
		poly_obj.addTag('obj')
		poly_obj.setFrom(0, 0, 0.0)
		poly_obj.setPickable(True)
		poly_obj.setPlaneConstraints([0, 0, 1])
		poly_obj.setRotationConstraints([1, 1, 1])
		VR.view_root.addChild(poly_obj)
		self.object_dict[poly_obj] = 'obj'
		self.object_dict['obj'] = poly_obj

	def setup_menu_bar(self):
		print 'setup_menu_bar'
		self.edit_plane = None
		self.edit_site = None
		self.meta_plane = None
		self.meta_site = None
		self.layer_add_plane = None
		self.layer_add_site = None
		self.behavior_add_plane = None
		self.behavior_add_site = None

		#setup menu bar layerAdd
		self.layer_add_plane = VR.Geometry('layerAdd')
		s = 'Plane '
		s += str(self.scale_x)
		s += ' 0.4 1 1'
		self.layer_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.layer_add_plane.setMaterial(material)
		self.layer_add_plane.setFrom(0, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

		self.layer_add_plane.setUp(0, -1, 0)
		self.layer_add_plane.setAt(0, 0, 1)
		self.layer_add_plane.setDir(0, 0, 1)
		self.layer_add_plane.setPickable(False)
		self.layer_add_plane.addTag('layer_add')

		self.layer_add_site = VR.CEF()
		self.layer_add_site.setMaterial(self.layer_add_plane.getMaterial())
		self.layer_add_site.open('http://localhost:5500/layerAdd')
		self.layer_add_site.setResolution(512)
		self.layer_add_site.setAspectRatio(4)

		self.active_gui_element = self.layer_add_plane

		#setup menu bar behaviorAdd
		self.behavior_add_plane = VR.Geometry('behaviorAdd')
		s = 'Plane '
		s += str(self.scale_x)
		s += ' 0.4 1 1'
		self.behavior_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.behavior_add_plane.setMaterial(material)
		self.behavior_add_plane.setFrom(0, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

		self.behavior_add_plane.setUp(0, -1, 0)
		self.behavior_add_plane.setAt(0, 0, 1)
		self.behavior_add_plane.setDir(0, 0, 1)
		self.behavior_add_plane.setPickable(False)
		self.behavior_add_plane.addTag('layer_add')

		self.behavior_add_site = VR.CEF()
		self.behavior_add_site.setMaterial(self.layer_add_plane.getMaterial())
		self.behavior_add_site.open('http://localhost:5500/behaviorAdd')
		self.behavior_add_site.setResolution(512)
		self.behavior_add_site.setAspectRatio(4)

		#self.active_gui_element = self.behavior_add_plane

		#setup menu bar edit
		self.edit_plane = VR.Geometry('edit')
		s = 'Plane '
		s += str(self.scale_x)
		s += ' 0.4 1 1'
		self.edit_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.edit_plane.setMaterial(material)
		self.edit_plane.setFrom(0, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

		self.edit_plane.setUp(0, -1, 0)
		self.edit_plane.setAt(0, 0, 1)
		self.edit_plane.setDir(0, 0, 1)
		self.edit_plane.setPickable(False)
		self.edit_plane.addTag('edit')

		self.edit_site = VR.CEF()
		self.edit_site.setMaterial(self.edit_plane.getMaterial())
		self.edit_site.open('http://localhost:5500/edit')
		self.edit_site.setResolution(512)
		self.edit_site.setAspectRatio(4)
		
		#self.active_gui_element = self.edit_plane

		# setup menu bar metadata
		self.meta_plane = VR.Geometry('meta')
		s = 'Plane '
		s += '0.4 '
		s += str(self.scale_y - 0.4)
		s += ' 1 1'
		self.meta_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.meta_plane.setMaterial(material)
		self.meta_plane.setFrom(0.5 * self.scale_x - 0.2, 0.2, -self.MAX_DIST)
		self.meta_plane.setUp(0, -1, 0)
		self.meta_plane.setAt(0, 0, 1)
		self.meta_plane.setDir(0, 0, 1)
		self.meta_plane.setPickable(False)
		self.meta_plane.addTag('meta')

		self.meta_site = VR.CEF()
		self.meta_site.setMaterial(self.meta_plane.getMaterial())
		params = '?' + 'm1_k=key1&m1_v=value1&m2_k=key2&m2_v=value2'
		self.meta_site.open('http://localhost:5500/meta' + params)
		self.meta_site.setResolution(200)
		self.meta_site.setAspectRatio(0.4)

		VR.cam.addChild(self.meta_plane)

		VR.site = {self.edit_site, self.meta_site, self.layer_add_site, self.behavior_add_site}
		VR.cam.addChild(self.active_gui_element)

	def set_cur_scene(self, cur_scene):
		print 'set_cur_scene'
		self.cur_scene = cur_scene
		self.cam.remChild(self.active_gui_element)

		if isinstance(cur_scene, PASS.Layer):
			self.active_gui_element = self.layer_add_plane
		elif isinstance(cur_scene, PASS.Behavior):
			self.active_gui_element = self.behavior_add_plane
		else:
			print 'View: ERROR in set_cur_scene: no valid active scene'

		VR.cam.addChild(self.active_gui_element)
		self.update_all()

	def get_cur_scene(self):
		return self.cur_scene

	# update entire scene based on given scene self.cur_scene
	def update_all(self):
		#delete current scene
		scene_children = VR.view_root.getChildren()
		for child in scene_children:
			print child
			#VR.view_root.remChild(child)
			child.destroy()
		self.object_dict.clear()
		#todo sizes
		#todo replace with blender models
		if isinstance(self.cur_scene, PASS.Layer):
			subjects = self.cur_scene.subjects
			message_exchanges = self.cur_scene.messageExchanges
			#TODO set right gui element

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
				self.object_dict[subject] = poly_sub
				self.object_dict[poly_sub] = subject
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
				self.draw_line(message)
				self.object_dict[message] = poly_mes
				self.object_dict[poly_mes] = message

		elif isinstance(self.cur_scene, PASS.Behavior):
			states = self.cur_scene.hasState
			edges = self.cur_scene.hasEdge
			#TODO set right gui element

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
				self.object_dict[state] = poly_state
				self.object_dict[poly_state] = state

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
				self.draw_line(edge)
				self.object_dict[edge] = poly_edge
				self.object_dict[poly_edge] = edge
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
		pos_ws = [(pos_ws[0] - 0.5) * self.scale_cursor_x, (pos_ws[1] - 0.5) * self.scale_cursor_y, self.CURSOR_DIST]
		#print 'View: pos_ws: ', pos_ws
		if not hasattr(VR, 'view_user_cursors'):
			VR.view_user_cursors = {}
		if not hasattr(VR, 'view_user_colors'):
			VR.view_user_colors = {}
		if not hasattr(VR, 'view_user_positions'):
			VR.view_user_positions = {}

		if user_id not in VR.view_user_cursors:
			assert len(VR.view_user_cursors) < self.MAX_USERS
			cursor_left = VR.Geometry('dev_l')
			cursor_left.setPrimitive('Sphere 0.008 5')
			cursor_left.setMaterial(VR.Material('sample material'))
			cursor_left.setFrom(0.3, 0, self.CURSOR_DIST)
			cursor_left.addTag(str([user_id, True]))
			VR.cam.addChild(cursor_left)
			cursor_right = VR.Geometry('dev_r')
			cursor_right.setPrimitive('Sphere 0.008 5')
			cursor_right.setMaterial(VR.Material('sample material'))
			cursor_right.setFrom(1.5, 0, self.CURSOR_DIST)
			cursor_right.addTag(str([user_id, False]))
			VR.cam.addChild(cursor_right)
			VR.view_user_cursors[user_id] = {}
			mydev_l = VR.Device('mydev')
			mydev_l.setBeacon(cursor_left)
			mydev_l.addIntersection(VR.view_root)
			mydev_l.addIntersection(self.meta_plane)
			mydev_l.addIntersection(self.edit_plane)  #TODO replace by layer_add_plane
			mydev_r = VR.Device('mydev')
			mydev_r.setBeacon(cursor_right)
			mydev_r.addIntersection(VR.view_root)
			mydev_r.addIntersection(self.meta_plane)
			mydev_r.addIntersection(self.edit_plane)   #TODO replace by layer_add_plane
			self.edit_site.addMouse(mydev_l, self.edit_plane, 0, 2, 3, 4)
			self.edit_site.addMouse(mydev_r, self.edit_plane, 0, 2, 3, 4)
			self.meta_site.addMouse(mydev_l, self.meta_plane, 0, 2, 3, 4)
			self.meta_site.addMouse(mydev_l, self.meta_plane, 0, 2, 3, 4)
			self.layer_add_site.addMouse(mydev_l, self.layer_add_plane, 0, 2, 3, 4)
			self.layer_add_site.addMouse(mydev_r, self.layer_add_plane, 0, 2, 3, 4)
			#self.behavior_add_site.addMouse(mydev_l, self.behavior_add_plane, 0, 2, 3, 4)
			#self.behavior_add_site.addMouse(mydev_r, self.behavior_add_plane, 0, 2, 3, 4)
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
		cursor.setDir(pos_ws)
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
		o = self.object_dict[obj]
		assert isinstance(o, VR.Object)
		if highlight:
			o.setColors([[1, 0, 0]])
			#set gui element: edit

			#set metaContent on gui element meta
			params = self.create_url_params_from_metacontent(o)
			self.meta_site.open('http://localhost:5500/meta' + '?' + params)			
			return True
		else:
			if isinstance(self.cur_scene, PASS.Layer):
				#TODO set gui element for layer (subject, message)
				pass
			elif isinstance(self.cur_scene, PASS.Behavior):
				#TODO set gui element for layer (fstate, sstate, rstate, tedge)
				pass
			else:
				print 'ERROR (view): Current scene neither of type Layer nor Behavior'

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
			#set metaContent on gui element meta to parent
			params = self.create_url_params_from_metacontent(o.getParent())
			self.meta_site.open('http://localhost:5500/meta' + '?' + params)
		return False

	def create_url_params_from_metacontent(self, obj):
		o = self.object_dict[obj]
		assert isinstance(o, VR.Object)
		
		params = '';		
		metaKeys = o.getMetaKeys()
		i = 0
		while i < len(metaKeys):
			print o.getMetaContent(metaKeys[i])
			params = params + 'k' + str(i) + '=' + str(metaKeys[i]) + '&' + 'v' + str(i) + '=' + str(o.getMetaContent(metaKeys[i]))
			if(i != len(metaKeys)):
				params = params + '&'
			
		return params


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
			return self.object_dict[obj]  # TODO: return PASS object
		elif obj is not None:
			# MenuBarItem?!
			print("View: MenuBarItem")
			return self.menubar_entries["subject"]  # TODO: return correct item!
		#print(("View: No object at {}".format(pos_ws)))
		return None
		#TODO update when victor finished implementing missing function

	def get_object(self, user_id, is_left):
		mydev = VR.view_user_cursors[user_id][is_left]
		if mydev.intersect():
			i = mydev.getIntersected()
			tags = i.getTags()
			print 'View tags: ', tags, 'name: ', i.getName(), 'id:', i.getID()
			if i.hasTag('edit'):
				print 'view: edit'
				mydev.trigger(0, 0)
				mydev.trigger(0, 1)
				return self.menubar_entries['edit']
			elif i.hasTag('meta'):
				print 'view: meta'
				mydev.trigger(0, 0)
				mydev.trigger(0, 1)
				return self.menubar_entries['meta']
			elif i.hasTag('layer_add'):
				print 'view: layer_add'
				mydev.trigger(0, 0)
				mydev.trigger(0, 1)
				return self.menubar_entries['layer_add']
			elif i.hasTag('behavior_add'):
				print 'view: behavior_add'
				mydev.trigger(0, 0)
				mydev.trigger(0, 1)
				return self.menubar_entries['behavior_add']
			#elif 'obj' in tags:
			else:
				print 'view: object'
				p = i.getParent().getParent()
				if p.hasTag('obj') or i.hasTag('obj'):
					print 'Object found'
					return i
				else:
					print 'No valid intersected object in get_object'
		else:
			print 'No intersection. Empty space clicked.'
		return None

	def rotate(self, degrees):
		pass

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
				if isinstance(object, PASS.Subject):
					poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject'], parent = 'world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('subject')
				elif isinstance(object, PASS.MessageExchange):
					poly_obj = VR.Geometry('cube')  #TODO replace with blender model
					primitive_str = 'Box'
					#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
					primitive_str += (' 0.2') * 3
					primitive_str += ' 1' * 3
					poly_obj.setPrimitive(primitive_str)
					poly_obj.setMaterial(VR.Material('sample material'))
					poly_obj.setColors(self.colors['message'])
					poly_obj.addTag('message')
					self.draw_line(object)
				elif isinstance(object, PASS.SendState):
					poly_obj = VR.Geometry('cube')  #TODO replace with blender model
					primitive_str = 'Box'
					#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
					primitive_str += (' 0.2') * 3
					primitive_str += ' 1' * 3
					poly_obj.setPrimitive(primitive_str)
					poly_obj.setMaterial(VR.Material('sample material'))
					poly_obj.setColors(self.colors['send_state'])
					poly_obj.addTag('send_state')
				elif isinstance(object, PASS.ReceiveState):
					poly_obj = VR.Geometry('cube')  #TODO replace with blender model
					primitive_str = 'Box'
					#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
					primitive_str += (' 0.2') * 3
					primitive_str += ' 1' * 3
					poly_obj.setPrimitive(primitive_str)
					poly_obj.setMaterial(VR.Material('sample material'))
					poly_obj.setColors(self.colors['receive_state'])
					poly_obj.addTag('receive_state')
				elif isinstance(object, PASS.FunctionState):
					poly_obj = VR.Geometry('cube')  #TODO replace with blender model
					primitive_str = 'Box'
					#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
					primitive_str += (' 0.2') * 3
					primitive_str += ' 1' * 3
					poly_obj.setPrimitive(primitive_str)
					poly_obj.setMaterial(VR.Material('sample material'))
					poly_obj.setColors(self.colors['function_state'])
					poly_obj.addTag('function_state')
				elif isinstance(object, PASS.TransitionEdge):
					poly_obj = VR.Geometry('cube')  #TODO replace with blender model
					primitive_str = 'Box'
					#  primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
					primitive_str += (' 0.2') * 3
					primitive_str += ' 1' * 3
					poly_obj.setPrimitive(primitive_str)
					poly_obj.setMaterial(VR.Material('sample material'))
					poly_obj.setColors(self.colors['state_message'])
					poly_obj.addTag('state_message')
					self.draw_line(object)
				#poly_obj.setFrom((pos_x / bb_x_dist) * self.offset_x - self.offset_x / 2.0, (pos_y / bb_y_dist) * self.offset_y - self.offset_y / 2.0, 0.0 )
				#print (pos_x / bb_x_dist) * self.offset_x - self.offset_x / 2.0
				poly_obj.addTag('obj')
				poly_obj.setFrom(pos_x, pos_y, 0.0)
				poly_obj.setPickable(True)
				poly_obj.setPlaneConstraints([0, 0, 1])
				poly_obj.setRotationConstraints([1, 1, 1])

				VR.view_root.addChild(poly_obj)
				self.object_dict[poly_obj] = object
				self.object_dict[object] = poly_obj
			else:  # update given object
				#TODO if object is of type *message: change line

				#set position and size
				primitive_str = 'box'
				primitive_str += (' ' + str(rel_size * max(self.offset_x, self.offset_y))) * 3
				primitive_str += ' 1' * 3
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
		o = self.object_dict[obj]
		assert isinstance(o, VR.Object)
		o.setFrom((pos_ws[0] - 0.5) * self.scale_x, (pos_ws[1] - 0.5) * self.scale_y, 0.0)
