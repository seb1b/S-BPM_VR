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
		self.BLENDER_PATHS['subject_meta'] = '../../View/Blender/Prozess/Subjekt_Hashtag.dae'
		self.BLENDER_PATHS['subject_highlight'] = '../../View/Blender/Prozess/Subjekt_Highlight.dae'
		self.BLENDER_PATHS['subject_meta_highlight'] = '../../View/Blender/Prozess/Subjekt_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['message'] = '../../View/Blender/Prozess/Message.dae'
		self.BLENDER_PATHS['message_meta'] = '../../View/Blender/Prozess/Message_Hashtag.dae'
		self.BLENDER_PATHS['message_highlight'] = '../../View/Blender/Prozess/Message_Highlight.dae'
		self.BLENDER_PATHS['message_meta_highlight'] = '../../View/Blender/Prozess/Message_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['external_subject'] = '../../View/Blender/Prozess/Sub.dae'
		self.BLENDER_PATHS['external_subject_meta'] = '../../View/Blender/Prozess/Sub_Hashtag.dae'
		self.BLENDER_PATHS['external_subject_highlight'] = '../../View/Blender/Prozess/Sub_Highlight.dae'
		self.BLENDER_PATHS['external_subject_meta_highlight'] = '../../View/Blender/Prozess/Sub_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['f_state'] = '../../View/Blender/Behavior/FState.dae'
		self.BLENDER_PATHS['f_state_meta'] = '../../View/Blender/Behavior/FState_Hashtag.dae'
		self.BLENDER_PATHS['f_state_highlight'] = '../../View/Blender/Behavior/FState_Highlight.dae'
		self.BLENDER_PATHS['f_state_meta_highlight'] = '../../View/Blender/Behavior/FState_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['s_state'] = '../../View/Blender/Behavior/SState.dae'
		self.BLENDER_PATHS['s_state_meta'] = '../../View/Blender/Behavior/SState_Hashtag.dae'
		self.BLENDER_PATHS['s_state_highlight'] = '../../View/Blender/Behavior/SState_Highlight.dae'
		self.BLENDER_PATHS['s_state_meta_highlight'] = '../../View/Blender/Behavior/SState_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['r_state'] = '../../View/Blender/Behavior/RState.dae'
		self.BLENDER_PATHS['r_state_meta'] = '../../View/Blender/Behavior/RState_Hashtag.dae'
		self.BLENDER_PATHS['r_state_highlight'] = '../../View/Blender/Behavior/RState_Highlight.dae'
		self.BLENDER_PATHS['r_state_meta_highlight'] = '../../View/Blender/Behavior/RState_Highlight_Hashtag.dae'
		self.BLENDER_PATHS['transition'] = '../../View/Blender/Behavior/Trans.dae'
		self.BLENDER_PATHS['transition_meta'] = '../../View/Blender/Behavior/Trans_Hashtag.dae'
		self.BLENDER_PATHS['transition_highlight'] = '../../View/Blender/Behavior/Trans_Highlight.dae'
		self.BLENDER_PATHS['transition_meta_highlight'] = '../../View/Blender/Behavior/Trans_Highlight_Hashtag.dae'

		self.HANDLE = VR.Geometry('handle')
		self.HANDLE.setPrimitive('Box 0.03 0.03 0.03 1 1 1')
		self.HANDLE.setMaterial(VR.Material('sample material'))

		#TODO add path for missing elements

		self.menubar_entries = {
			'edit': self.MenuBarItem('edit'),
			'meta': self.MenuBarItem('meta'),
			'layer_add': self.MenuBarItem('layer_add'),
			'behavior_add': self.MenuBarItem('behavior_add')
		}

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dict = {}
		self.message_dict = {}  # key: poly_mess 1. entry: poly_sender, 2. entry: poly_receiver, 3. entry: path

		#stores user_id and corresponding color
		self.user_colors = {}

		#setup camera parameter
		self.camera_from = [0, 0, self.MAX_DIST]
		self.camera_at = [0, 0, -1.0]
		self.camera_dir = [0, 0, -1]
		self.camera_fov = 0.2

		self.paths = []  # list of paths

		self.cur_scene = None
		self.active_gui_element = None  # edit plane, layer_add plane or behavior_add plane

		#setup root
		root = VR.getRoot().find('Headlight')
		VR.view_root = VR.Transform('world')
		root.addChild(VR.view_root)
		VR.cam = VR.getRoot().find('Default')
		VR.cam.setFrom(self.camera_from)
		VR.cam.setAt(self.camera_at)
		VR.cam.setDir(self.camera_dir)
		VR.cam.setFov(self.camera_fov)
		
		#setup pathtool
		self.ptool = VR.Pathtool()
		self.ptool.setHandleGeometry(self.HANDLE)

		#setup offsets
		#screen
		win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(win_size) == 2
		self.scale_y = 2 * self.camera_from[2] * math.tan(self.camera_fov * 0.5)
		self.scale_x = self.scale_y * win_size[0] / win_size[1]
		self.scale_cursor_y = 2 * abs(self.CURSOR_DIST) * math.tan(self.camera_fov * 0.5)
		self.scale_cursor_x = self.scale_cursor_y * win_size[0] / win_size[1]
		#model
		self.model_offset_x = 0
		self.model_offset_y = 0
		self.model_width = 0
		self.model_hight = 0

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
		s += str(self.scale_x - (self.scale_x / 4))
		s += ' 0.4 1 1'
		self.layer_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.layer_add_plane.setMaterial(material)
		self.layer_add_plane.setFrom(-(self.scale_x / 4) / 2, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

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
		s += str(self.scale_x - (self.scale_x / 4))
		s += ' 0.4 1 1'
		self.behavior_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.behavior_add_plane.setMaterial(material)
		self.behavior_add_plane.setFrom(-(self.scale_x / 4) / 2, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

		self.behavior_add_plane.setUp(0, -1, 0)
		self.behavior_add_plane.setAt(0, 0, 1)
		self.behavior_add_plane.setDir(0, 0, 1)
		self.behavior_add_plane.setPickable(False)
		self.behavior_add_plane.addTag('behavior_add')

		self.behavior_add_site = VR.CEF()
		self.behavior_add_site.setMaterial(self.layer_add_plane.getMaterial())
		self.behavior_add_site.open('http://localhost:5500/behaviorAdd')
		self.behavior_add_site.setResolution(512)
		self.behavior_add_site.setAspectRatio(4)

		#self.active_gui_element = self.behavior_add_plane
	
		#setup menu bar navigation
		self.navigation_plane = VR.Geometry('navigation')
		s = 'Plane '
		s += str(self.scale_x / 4)
		s += ' 0.4 1 1'
		self.navigation_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.navigation_plane.setMaterial(material)
		self.navigation_plane.setFrom((self.scale_x * 3 / 8), -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

		self.navigation_plane.setUp(0, -1, 0)
		self.navigation_plane.setAt(0, 0, 1)
		self.navigation_plane.setDir(0, 0, 1)
		self.navigation_plane.setPickable(False)
		self.navigation_plane.addTag('navigation')


		#setup menu bar edit
		self.edit_plane = VR.Geometry('edit')
		s = 'Plane '
		s += str(self.scale_x / 4)
		s += ' 0.4 1 1'
		self.edit_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.edit_plane.setMaterial(material)
		self.edit_plane.setFrom(-(self.scale_x / 4) / 2, -0.5 * self.scale_y + 0.2, -self.MAX_DIST)

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
		VR.cam.addChild(self.navigation_plane)

		VR.site = {self.edit_site, self.meta_site, self.layer_add_site, self.behavior_add_site}
		VR.cam.addChild(self.active_gui_element)

	def set_cur_scene(self, cur_scene):
		assert  isinstance(cur_scene, PASS.Layer) or isinstance(cur_scene, PASS.Behavior)
		self.cur_scene = cur_scene
		#self.cam.remChild(self.active_gui_element) #TODO

		if isinstance(cur_scene, PASS.Layer):
			self.active_gui_element = self.layer_add_plane
		else:  # is instance of Pass.Behavior
			self.active_gui_element = self.behavior_add_plane

		#set offsets
		self.model_offset_x = self.cur_scene.getBoundingBox2D()[0][0]
		self.model_offset_y = self.cur_scene.getBoundingBox2D()[0][1]
		self.model_width = self.cur_scene.getBoundingBox2D()[1][0] - self.model_offset_x
		self.model_hight = self.cur_scene.getBoundingBox2D()[1][1] - self.model_offset_y

		#VR.cam.addChild(self.active_gui_element) #TODO
		#self.update_all()

	def get_cur_scene(self):
		return self.cur_scene

	# update entire scene based on given scene self.cur_scene
	def update_all(self):
		#delete current scene
		scene_children = VR.view_root.getChildren()
		for child in scene_children:
			child.destroy()
		self.object_dict.clear()
		self.message_dict.clear()
		self.ptool = VR.Pathtool()
		self.ptool.setHandleGeometry(self.HANDLE)

		#todo sizes
		#todo replace with blender models
		if isinstance(self.cur_scene, PASS.Layer):
			subjects = self.cur_scene.subjects
			message_exchanges = self.cur_scene.messageExchanges
			external_subjects = self.cur_scene.externalSubjects

			for subject in subjects:
				assert isinstance(subject, PASS.Subject)
				pos = subject.hasAbstractVisualRepresentation.hasPoint2D
				if len(subject.hasMetaContent) == 0:
					poly_sub = VR.loadGeometry(self.BLENDER_PATHS['subject'])
				else:
					poly_sub = VR.loadGeometry(self.BLENDER_PATHS['subject_meta'])
				poly_sub.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
				poly_sub.setPickable(True)
				poly_sub.addTag('subject')
				poly_sub.addTag('obj')
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
				poly_mes.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
				poly_mes.setPickable(True)
				poly_mes.addTag('message')
				poly_mes.addTag('obj')
				poly_mes.setColors(self.colors['message'])
				poly_mes.setPlaneConstraints([0, 0, 1])
				poly_mes.setRotationConstraints([1, 1, 1])
				self.object_dict[message] = poly_mes
				self.object_dict[poly_mes] = message
				s = None
				r = None
				if message.sender in self.object_dict:
					s = self.object_dict[message.sender]
				if message.receiver in self.object_dict:
					r = self.object_dict[message.sender]
				self.message_dict[message] = [s, r, None]
				VR.view_root.addChild(poly_mes)
				self.connect(message)

			for subject in external_subjects:
				assert isinstance(subject, PASS.ExternalSubject)
				pos = subject.hasAbstractVisualRepresentation.hasPoint2D
				if len(subject.hasMetaContent) == 0:
					poly_sub = VR.loadGeometry(self.BLENDER_PATHS['external_subject'])
				else:
					poly_sub = VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta'])
				poly_sub.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
				poly_sub.setPickable(True)
				poly_sub.addTag('external_subject')
				poly_sub.addTag('obj')
				poly_sub.setPlaneConstraints([0, 0, 1])
				poly_sub.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_sub)
				self.object_dict[subject] = poly_sub
				self.object_dict[poly_sub] = subject

		elif isinstance(self.cur_scene, PASS.Behavior):
			states = self.cur_scene.hasState
			edges = self.cur_scene.hasEdge

			for state in states:
				assert isinstance(state, PASS.State)
				pos = state.hasAbstractVisualRepresentation.hasPoint2D
				if isinstance(state, PASS.FunctionState):
					if len(state.hasMetaContent) == 0:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['f_state'])
					else:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['f_state_meta'])
					poly_state..setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
					poly_state.setPickable(True)
					poly_state.addTag('functional_state')
					poly_state.addTag('obj')
					poly_state.setPlaneConstraints([0, 0, 1])
					poly_state.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(poly_state)
					self.object_dict[state] = poly_state
					self.object_dict[poly_state] = state
				elif isinstance(state, PASS.SendState):
					if len(state.hasMetaContent) == 0:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['s_state'])
					else:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['s_state_meta'])
					poly_state..setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
					poly_state.setPickable(True)
					poly_state.addTag('send_state')
					poly_state.addTag('obj')
					poly_state.setPlaneConstraints([0, 0, 1])
					poly_state.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(poly_state)
					self.object_dict[state] = poly_state
					self.object_dict[poly_state] = state
				elif isinstance(state, PASS.ReceiveState):
					if len(state.hasMetaContent) == 0:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['r_state'])
					else:
						poly_state = VR.loadGeometry(self.BLENDER_PATHS['r_state_meta'])
					poly_state..setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
								 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
					poly_state.setPickable(True)
					poly_state.addTag('receive_state')
					poly_state.addTag('obj')
					poly_state.setPlaneConstraints([0, 0, 1])
					poly_state.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(poly_state)
					self.object_dict[state] = poly_state
					self.object_dict[poly_state] = state

			for edge in edges:
				assert isinstance(edge, PASS.TransitionEdge)
				pos = edge.hasAbstractVisualRepresentation.hasPoint2D
				if len(edge.hasMetaContent) == 0:
					poly_edge = VR.loadGeometry(self.BLENDER_PATHS['transition'])
				else:
					poly_edge = VR.loadGeometry(self.BLENDER_PATHS['transition_meta'])
				poly_edge..setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
							 ((pos.hasYValue - self.model_offset_y) / self.model_hight -0.5) * self.scale_y, 0)
				poly_edge.setPickable(True)
				poly_edge.addTag('receive_state')
				poly_edge.addTag('obj')
				poly_edge.setPlaneConstraints([0, 0, 1])
				poly_edge.setRotationConstraints([1, 1, 1])
				VR.view_root.addChild(poly_edge)
				self.object_dict[edge] = poly_edge
				self.object_dict[poly_edge] = edge
				self.connect(poly_edge)
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
			#mydev_l.addIntersection(VR.view_root)
			mydev_l.addIntersection(self.meta_plane)
			mydev_l.addIntersection(self.edit_plane)  #TODO replace by layer_add_plane
			mydev_r = VR.Device('mydev')
			mydev_r.setBeacon(cursor_right)
			#mydev_r.addIntersection(VR.view_root)
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
		print 'pass obj', obj
		o = self.object_dict[obj]
		print 'vr obj', o
		assert isinstance(o, VR.Object)

		if highlight:
			pass
			#TODO set edit gui element
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
			if highlight:  #TODO change message exchange line
				if len(obj.hasMetaContent) == 0:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['subject_highlight'], parent='world')
					new_o.setScale(0.1, 0.1, 0.1)
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				else:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['subject_meta_highlight'], parent='world')
					new_o.setScale(0.1, 0.1, 0.1)
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				#set metaContent on gui element meta to parent
				params = self.create_url_params_from_metacontent(self.object_dict[obj])
				self.meta_site.open('http://localhost:5500/meta' + '?' + params)
			else:
				if len(obj.hasMetaContent) == 0:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['subject'], parent='world')
					new_o.setScale(0.1, 0.1, 0.1)
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				else:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['subject_meta'], parent='world')
					new_o.setScale(0.1, 0.1, 0.1)
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				#set metaContent on gui element meta to parent
				params = self.create_url_params_from_metacontent(self.cur_scene)
				self.meta_site.open('http://localhost:5500/meta' + '?' + params)
		elif isinstance(obj, PASS.MessageExchange):
			if highlight:  #TODO change message exchange line
				if len(obj.hasMetaContent) == 0:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['message_highlight'], parent='world')
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				else:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['message_meta_highlight'], parent='world')
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				#set metaContent on gui element meta to parent
				params = self.create_url_params_from_metacontent(self.object_dict[obj])
				self.meta_site.open('http://localhost:5500/meta' + '?' + params)
			else:
				if len(obj.hasMetaContent) == 0:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['message'], parent='world')
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				else:
					del self.object_dict[obj]
					del self.object_dict[o]
					new_o = VR.loadGeometry(self.BLENDER_PATHS['message_meta'], parent='world')
					new_o.setFrom(o.getFrom())
					new_o.setPickable(True)
					new_o.addTag('subject')
					new_o.addTag('obj')
					new_o.setPlaneConstraints([0, 0, 1])
					new_o.setRotationConstraints([1, 1, 1])
					VR.view_root.addChild(new_o)
					o.distroy()
					self.object_dict[obj] = new_o
					self.object_dict[new_o] = obj
					return True
				#set metaContent on gui element meta to parent
				params = self.create_url_params_from_metacontent(self.cur_scene)
				self.meta_site.open('http://localhost:5500/meta' + '?' + params)
		elif isinstance(obj, PASS.SendState):  #TODO blender
			o.setColors(self.colors['send_state'])
			return True
		elif isinstance(obj, PASS.ReceiveState):  #TODO blender
			o.setColors(self.colors['receive_state'])
			return True
		elif isinstance(obj, PASS.FunctionState):  #TODO blender
			o.setColors(self.colors['function_state'])
			return True
		elif isinstance(obj, PASS.TransitionEdge):  #TODO blender
			o.setColors(self.colors['state_message'])
			return True
		else:
			print "View Error: no valid object tag"
			return False
		return False

	def create_url_params_from_metacontent(self, obj):
		o = self.object_dict[obj]
		assert isinstance(o, VR.Object)

		params = ''
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
		highlighted_point.setFrom((pos[0] - 0.5) * self.scale_x, (pos[1] - 0.5) * self.scale_y, 0.0)
		highlighted_point.setPlaneConstraints([0, 0, 1])
		highlighted_point.setRotationConstraints([1, 1, 1])
		highlighted_point.setColors([1, 0, 0]) #TODO change color?!
		highlighted_point.setPickable(False)
		highlighted_point.addTag('highlight')
		VR.view_root.addChild(highlighted_point)

		return highlighted_point

	def remove_highlight_pos(self, highlight_pos):  # remove the given highlighted object from scene
		VR.view_root.remChild(highlight_pos)

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
				#TODO check if intersection with handle or object
				p = i.getParent().getParent()
				if p.hasTag('obj'):
					print 'Object found', p
					return self.object_dict[p]
				elif i.hasTag('obj'):
					print 'Object found', i
					return self.object_dict[i]
				else:
					print 'No valid intersected object in get_object'
		else:
			print 'No intersection. Empty space clicked.'
		return None

	def rotate(self, degrees):
		pass

	def on_change(self, object):
		if isinstance(self.cur_scene, PASS.Layer):
			if isinstance(object, PASS.Subject):
				print "View on_change: Subject"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new subject
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('subject')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					#TODO set Handle if this subject is connected
					#if poly_obj.getParent() is Handle: change handle position
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					#TODO reset name
					#TODO meta content
			elif isinstance(object, PASS.MessageExchange):
				print "View on_change: MessageExchange"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['message'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['message_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('message')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
					s = None
					r = None
					if object.sender in self.object_dict:
						s = self.object_dict[object.sender]
					if object.receiver in self.object_dict:
						r = self.object_dict[object.sender]
					self.message_dict[object] = [s, r, None]
					self.connect(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					#TODO set Handle if existing
					#if poly_obj.getParent() is Handle: change handle position
					#poly_obj.getParent().setFrom((pos_x - self.model_offset_x) / self.model_width * self.scale_x,
					#				 (pos_y - self.model_offset_y) / self.model_hight * self.scale_y, 0.0)
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#TODO reset name
					#TODO meta content
					#TODO sender changed
					#TODO receiver changed
			elif isinstance(object, PASS.ExternalSubject):
				print "View on_change: External Message"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('external_subject')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					#TODO set Handle if existing
					#if poly_obj.getParent() is Handle: change handle position
					#poly_obj.getParent().setFrom((pos_x - self.model_offset_x) / self.model_width * self.scale_x,
					#				 (pos_y - self.model_offset_y) / self.model_hight * self.scale_y, 0.0)
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#TODO reset name
					#TODO meta content
			else:
				pass
		elif isinstance(self.cur_scene, PASS.Behavior):
			if isinstance(object, PASS.SendState):
				print "View on_change: Send State"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new subject
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['s_state'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['s_state_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('send_state')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					#TODO set Handle if this subject is connected
					#if poly_obj.getParent() is Handle: change handle position
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					#TODO reset name
					#TODO meta content
			elif isinstance(object, PASS.ReceiveState):
				print "View on_change: Receive State"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['r_state'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['subject_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('receive_state')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
					self.connect(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					#TODO set Handle if existing
					#if poly_obj.getParent() is Handle: change handle position
					#poly_obj.getParent().setFrom((pos_x - self.model_offset_x) / self.model_width * self.scale_x,
					#				 (pos_y - self.model_offset_y) / self.model_hight * self.scale_y, 0.0)
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#TODO reset name
			elif isinstance(object, PASS.FunctionState):
				print "View on_change: Function State"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['f_state'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['f_state_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('function_state')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					#TODO set Handle if existing
					#if poly_obj.getParent() is Handle: change handle position
					#poly_obj.getParent().setFrom((pos_x - self.model_offset_x) / self.model_width * self.scale_x,
					#				 (pos_y - self.model_offset_y) / self.model_hight * self.scale_y, 0.0)
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#TODO reset name
					#TODO meta content
			elif isinstance(object, PASS.TransitionEdge):
				print "View on_change: Transition Edge"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					if len(object.hasMetaConten) == 0:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['transition'], parent='world')
					else:
						poly_obj = VR.loadGeometry(self.BLENDER_PATHS['transition_meta'], parent='world')
					poly_obj.setScale(0.1, 0.1, 0.1)
					poly_obj.addTag('transition')
					poly_obj.addTag('obj')
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					poly_obj.setPickable(True)
					poly_obj.setPlaneConstraints([0, 0, 1])
					poly_obj.setRotationConstraints([1, 1, 1])
					#TODO set name
					self.object_dict[object] = poly_obj
					self.object_dict[poly_obj] = object
					VR.view_root.addChild(poly_obj)
					s = None
					r = None
					if object.hasSourceState in self.object_dict:
						s = self.object_dict[object.sender]
					if object.hasTargetState in self.object_dict:
						r = self.object_dict[object.sender]
					self.message_dict[object] = [s, r, None]
					self.connect(poly_obj)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					#TODO set Handle if existing
					#if poly_obj.getParent() is Handle: change handle position
					#poly_obj.getParent().setFrom((pos_x - self.model_offset_x) / self.model_width * self.scale_x,
					#				 (pos_y - self.model_offset_y) / self.model_hight * self.scale_y, 0.0)
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
									 ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#TODO reset name
					#TODO meta content
					#TODO sender changed
					#TODO receiver changed
		else:
			print 'VIEW ERROR: self.cur_scene must be of type Layer or Behavior'
		#TODO move to right place
		print 'on_change: Name tagging '
		ae = VR.AnnotationEngine('ae_')
		VR.view_root.addChild(ae)
		ae.setColor([0,1,0,1])
		ae.setBackground([1,0,0,0.5])
		ae.setSize(0.02)
		text = ''
		for t in object.label:
			text = str(text) + str(t)
		ae.set(1, [pos_x, pos_y, 0.0], 'test -' + text)

	def connect(self, message):
		assert isinstance(message, VR.Transform), "parameter must be of VR.Transform type"
		assert message in self.message_dict, "parameter must be in message_dict"

		s = self.message_dict[message][0]
		r = self.message_dict[message][1]
		assert s is not None and r is not None, "sender and receiver must not be None"
		start_pos = s.getFrom()
		mid_pos = message.getFrom()
		end_pos = r.getFrom()

		#calc directions
		start_dir = [0.0, 0.0]
		mid_dir = [1.0, 0.0]
		end_dir = [0.0, 0.0]
		if start_pos[0] > mid_pos[1]:
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

		message.setPickable(False)
		s.setPickable(False)
		s.setPickable(False)

		print "draw_line: ", s, " => ", r
		self.paths.append(self.ptool.newPath(None, VR.view_root))
		self.message_dict[message][2] = self.paths[-1]
		self.ptool.extrude(None, self.paths[-1])
		handles = self.ptool.getHandles(self.paths[-1])
		assert len(handles) == 3, "invalid number of handles"
		handles[0].setFrom(s.getFrom())
		print 'handle 1 vor:', handles[0].getFrom()
		handles[0].setAt(s.getAt())
		handles[0].setDir(start_dir[0], start_dir[1], 0.0)
		handles[0].addChild(s)
		s.setFrom(0, 0, 0)
		print 'handle 1 nach:', handles[0].getFrom()
		handles[1].setFrom(message.getFrom())
		print 'handle 2 vor:', handles[1].getFrom()
		handles[1].setAt(message.getAt())
		handles[1].setDir(1.0, 0.0, 0.0)
		handles[1].addChild(message)
		message.setFrom(0, 0, 0)
		print 'handle 2 nach:', handles[1].getFrom()
		handles[2].setFrom(r.getFrom())
		print 'handle 3 vor:', handles[2].getFrom()
		handles[2].setAt(r.getAt())
		handles[2].setDir(end_dir[0], end_dir[1], 0.0)
		handles[2].addChild(r)
		r.setFrom(0, 0, 0)
		print 'handle 3 nach:', handles[2].getFrom()
		self.ptool.update()

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
