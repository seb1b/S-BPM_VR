import VR
import math
import PASS
import sys
import logging
import copy


class View():

	class MenuBar():
		def __init__(self, name):
			self.name = name

	class InitScreenEntry():
		def __init__(self, display_name, file_name, image_file_name, model_id):
			self.display_name = display_name
			self.file_name = file_name
			self.image_file_name = image_file_name
			self.model_id = model_id

		def __str__(self):
			return "InitScreenEntry: {}, {}, {}".format(self.display_name, self.file_name, self.image_file_name)

	def __init__(self):
		self.log = logging.getLogger()
		#self.log.setLevel(logging.DEBUG)  # DEBUG INFO WARNING ...
		#ch = logging.StreamHandler(sys.stdout)
		#ch.setLevel(logging.DEBUG)
		#formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		#ch.setFormatter(formatter)
		#self.log.addHandler(ch)
		self.log.info("Starting view")

		self.ZOOM_STEP = 0.05
		self.MOVE_STEP = 0.01
		self.MAX_USERS = 5
		self.MAX_DIST = 100
		self.CURSOR_DIST = -2
		self.MIN_DIST = 2
		self.CAM_INIT_DIST = 10
		self.VALID_USER_COLORS = []
		#setup valid user colors
		self.VALID_USER_COLORS.append([1, 0, 0])
		self.VALID_USER_COLORS.append([0.91, 0.54, 0.05])
		self.VALID_USER_COLORS.append([0.45, 0.05, 0.91])
		self.VALID_USER_COLORS.append([1, 0.98, 0.05])
		self.VALID_USER_COLORS.append([0, 0.7, 0.2])
		self.PATH_COLOR = 0.27

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
		self.BLENDER_PATHS['open_hand_left'] = '../../View/Blender/Cursor/Open_Hand_Left.dae'
		self.BLENDER_PATHS['closed_hand_left'] = '../../View/Blender/Cursor/Closed_Hand_Left.dae'
		self.BLENDER_PATHS['open_hand_right'] = '../../View/Blender/Cursor/Open_Hand_Right.dae'
		self.BLENDER_PATHS['closed_hand_right'] = '../../View/Blender/Cursor/Closed_Hand_Right.dae'
		self.BLENDER_PATHS['open_pointer_left'] = '../../View/Blender/Cursor/Pointer_Hand_Left.dae'
		self.BLENDER_PATHS['closed_pointer_left'] = '../../View/Blender/Cursor/Pointer_Hand_Left_Click.dae'
		self.BLENDER_PATHS['open_pointer_right'] = '../../View/Blender/Cursor/Pointer_Hand_Right.dae'
		self.BLENDER_PATHS['closed_pointer_right'] = '../../View/Blender/Cursor/Pointer_Hand_Right_Click.dae'
		self.BLENDER_PATHS['arrow_tip'] = '../../View/Blender/Pfeil/Pfeil.dae'

		self.PLANE_SIZE = 0.4
		self.OBJECT_SCALE = [0.4, 0.4, 0.4]
		self.TEXT_SIZE = 0.5
		self.BORDER_ANGLE = 0.005

		self.HANDLE = VR.Geometry('handle')
		self.HANDLE.setPrimitive('Box 0.001 0.001 0.001 1 1 1')
		self.HANDLE.setMaterial(VR.Material('sample material'))

		self.HANDLE_ARROW = VR.loadGeometry(self.BLENDER_PATHS['arrow_tip'])
		self.HANDLE_ARROW.setScale([0.7, 0.7, 0.7])

		self.menubar_entries = {
			'edit': self.MenuBar('edit'),
			'meta': self.MenuBar('meta'),
			'layer_add': self.MenuBar('layer_add'),
			'behavior_add': self.MenuBar('behavior_add')
		}

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dict = {}
		self.message_dict = {}  # key: poly_mess, 1. entry: poly_sender, 2. entry: poly_receiver, 3. entry: path
		self.elements = []

		#stores user_id and corresponding color
		self.user_colors = {}

		#setup camera parameter
		self.camera_from = [0, 0, self.CAM_INIT_DIST]
		self.camera_at = [0, 0, -1.0]
		self.camera_dir = [0, 0, -1]
		self.camera_fov = 0.2

		self.paths = []  # list of paths
		self.new_message_path = None  # for creating a new message

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
		self.cam_navigation = VR.Camera('cam_navigation')
		self.cam_navigation.setFrom(self.camera_from[0], self.camera_from[1], self.camera_from[2] + 2.5)
		self.cam_navigation.setAt(self.camera_at)
		self.cam_navigation.setDir(self.camera_dir)
		self.cam_navigation.setFov(self.camera_fov)
		
		#setup cursors
		if not hasattr(VR, 'view_user_cursors'):
			VR.view_user_cursors = {}
		if not hasattr(VR, 'view_user_colors'):
			VR.view_user_colors = {}
		if not hasattr(VR, 'view_user_positions'):
			VR.view_user_positions = {}

		#setup pathtool
		VR.ptool = VR.Pathtool()
		#VR.ptool.setHandleGeometry(self.HANDLE_ARROW)
		VR.ptool.setHandleGeometry(self.HANDLE)

		#setup offsets
		#screen
		self.win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(self.win_size) == 2
		self.scale_y = 2 *self.CAM_INIT_DIST * math.tan(self.camera_fov * 0.5)
		self.scale_x = self.scale_y * self.win_size[0] / self.win_size[1]
		self.scale_cursor_y = 2 * abs(self.CURSOR_DIST) * math.tan(self.camera_fov * 0.5)
		self.scale_cursor_x = self.scale_cursor_y * self.win_size[0] / self.win_size[1]
		self.scale_plane_y = 2 * 11 * math.tan(self.camera_fov * 0.5)
		self.scale_plane_x = self.scale_plane_y * self.win_size[0] / self.win_size[1]
		#model
		self.model_offset_x = 0
		self.model_offset_y = 0
		self.model_width = 0
		self.model_height = 0

		# gui elements
		#node for all edit planes
		self.edit_node = VR.Transform('edit_node')
		self.edit_node.setFrom(-(self.scale_plane_x / 4) / 2, -0.5 * self.scale_plane_y + 0.2, -11)
		self.setup_menu_bar()

		# start page
		self.setup_start_page()

	def setup_start_page(self):
		#setup menu bar behaviorAdd
		self.start_page_plane = VR.Geometry('startPage')
		s = 'Plane '
		#s += str(self.scale_x) + str(self.scale_y)
		s += str(self.scale_x)
		s += ' 2 1 1'
		self.start_page_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.start_page_plane.setMaterial(material)
		self.start_page_plane.setFrom(0, 0, 0)

		self.start_page_plane.setUp(0, -1, 0)
		self.start_page_plane.setAt(0, 0, 1)
		self.start_page_plane.setDir(0, 0, 1)
		self.start_page_plane.setPickable(False)		
		self.start_page_plane.addTag('start_page')

		self.start_page_site = VR.CEF()
		self.start_page_site.setMaterial(self.start_page_plane.getMaterial())
		self.start_page_site.open('http://localhost:5500/start')
		self.start_page_site.setResolution(1024)
		self.start_page_site.setAspectRatio(1)

		self.start_page_plane.setVisible(False)
		VR.view_root.addChild(self.start_page_plane)

	def setup_menu_bar(self):
		self.log.info('setup_menu_bar')
		self.edit_plane = None
		self.edit_site = None
		self.meta_plane = None
		self.meta_site = None
		self.layer_add_plane = None
		self.layer_add_site = None
		self.behavior_add_plane = None
		self.behavior_add_site = None

		#setup menu bar layerAdd -> add in process layer
		self.layer_add_plane = VR.Geometry('layerAdd')
		s = 'Plane '
		s += str(self.scale_plane_x - (self.scale_plane_x / 4))
		s += ' ' + str(self.PLANE_SIZE)
		s += ' 1 1'
		self.layer_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.layer_add_plane.setMaterial(material)
		self.layer_add_plane.setFrom(0, 0, 0)

		self.layer_add_plane.setUp(0, -1, 0)
		self.layer_add_plane.setAt(0, 0, 1)
		self.layer_add_plane.setDir(0, 0, 1)
		self.layer_add_plane.setPickable(False)
		self.layer_add_plane.addTag('layer_add')

		self.layer_add_site = VR.CEF()
		self.layer_add_site.setMaterial(self.layer_add_plane.getMaterial())
		self.layer_add_site.open('http://localhost:5500/layerAdd')
		self.layer_add_site.setResolution(1024)
		self.layer_add_site.setAspectRatio(6)

		self.layer_add_plane.setVisible(False)
		self.edit_node.addChild(self.layer_add_plane)

		#setup menu bar behaviorAdd
		self.behavior_add_plane = VR.Geometry('behaviorAdd')
		s = 'Plane '
		s += str(self.scale_plane_x - (self.scale_plane_x / 4))
		s += ' ' + str(self.PLANE_SIZE)
		s += ' 1 1'
		self.behavior_add_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.behavior_add_plane.setMaterial(material)
		self.behavior_add_plane.setFrom(0, 0, 0)

		self.behavior_add_plane.setUp(0, -1, 0)
		self.behavior_add_plane.setAt(0, 0, 1)
		self.behavior_add_plane.setDir(0, 0, 1)
		self.behavior_add_plane.setPickable(False)
		self.behavior_add_plane.addTag('behavior_add')

		self.behavior_add_site = VR.CEF()
		self.behavior_add_site.setMaterial(self.behavior_add_plane.getMaterial())
		self.behavior_add_site.open('http://localhost:5500/behaviorAdd')
		self.behavior_add_site.setResolution(512)
		self.behavior_add_site.setAspectRatio(4)

		self.behavior_add_plane.setVisible(False)
		self.edit_node.addChild(self.behavior_add_plane)

		#setup menu bar edit
		self.edit_plane = VR.Geometry('edit')
		s = 'Plane '
		s += str(self.scale_plane_x - (self.scale_plane_x / 4))
		s += ' 0.4 1 1'
		self.edit_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.edit_plane.setMaterial(material)
		self.edit_plane.setFrom(0, 0, 0)

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

		self.edit_plane.setVisible(False)
		self.edit_node.addChild(self.edit_plane)

		#setup menu bar navigation
		#background
		self.navigation_plane_back = VR.Geometry('navigation_back')
		s = 'Plane '
		s += str(self.scale_x / 4)
		s += ' ' + str(self.PLANE_SIZE)
		s += ' 1 1'
		self.navigation_plane_back.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.navigation_plane_back.setMaterial(material)
		self.navigation_plane_back.setFrom((self.scale_x * 3 / 8), -0.5 * self.scale_y + 0.2, -self.camera_from[2])
		self.navigation_plane_back.setUp(0, -1, 0)
		self.navigation_plane_back.setAt(0, 0, 1)
		self.navigation_plane_back.setDir(0, 0, 1)
		self.navigation_plane_back.setScale(1, -1, 1)
		self.navigation_plane_back.setPickable(False)
		self.navigation_plane_back.setVisible(False)
		self.navigation_plane_back.addTag('navigationBack')

		self.navigation_plane = VR.Geometry('navigation')
		s = 'Plane '
		s += str(self.scale_x / 4 - (self.scale_x / 4 / 150))
		s += ' ' + str(self.PLANE_SIZE - (self.PLANE_SIZE / 150))
		s += ' 1 1'
		self.navigation_plane.setPrimitive(s)
		material = VR.Material('gui')
		material.setLit(False)
		self.navigation_plane.setMaterial(material)
		self.navigation_plane.setFrom((self.scale_x * 3 / 8), -0.5 * self.scale_y + 0.2, -self.camera_from[2] + 0.1)
		self.navigation_plane.setUp(0, -1, 0)
		self.navigation_plane.setAt(0, 0, 1)
		self.navigation_plane.setDir(0, 0, 1)
		self.navigation_plane.setScale(1, -1, 1)
		self.navigation_plane.setPickable(False)
		self.navigation_plane.addTag('navigation')

		texture = VR.TextureRenderer('navigation_texture')
		root = VR.getRoot().find('Headlight')
		#root = VR.cam
		VR.getRoot().addChild(texture)

		VR.rcam = self.cam_navigation
		li = VR.Light('sun')
		lib = VR.LightBeacon('sun_b')
		li.setBeacon(lib)
		texture.setup(self.cam_navigation, int(self.scale_x / 4 * 1024), int(self.PLANE_SIZE * 1024))
		li.addChild(self.cam_navigation)
		texture.addChild(li)
		self.cam_navigation.addChild(lib)
		texture.addLink(root)

		m = texture.getMaterial()
		self.navigation_plane.setMaterial(m)

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
		self.meta_plane.setFrom(0.5 * self.scale_x - 0.2, 0.2, -self.camera_from[2])
		self.meta_plane.setUp(0, -1, 0)
		self.meta_plane.setAt(0, 0, 1)
		self.meta_plane.setDir(0, 0, 1)
		self.meta_plane.setPickable(False)
		self.meta_plane.addTag('meta')

		self.meta_site = VR.CEF()
		self.meta_site.setMaterial(self.meta_plane.getMaterial())
		params = '?' + 'key1=value1&key2=value2'
		self.meta_site.open('http://localhost:5500/meta' + params)
		self.meta_site.setResolution(200)
		self.meta_site.setAspectRatio(0.4)
		self.meta_site.addKeyboard(VR.keyboard)

		self.meta_plane.setVisible(False)
		self.navigation_plane.setVisible(False)
		VR.cam.addChild(self.meta_plane)
		VR.cam.addChild(self.navigation_plane_back)
		VR.cam.addChild(self.navigation_plane)

		VR.site = {self.edit_site, self.meta_site, self.behavior_add_site, self.layer_add_site}
		VR.cam.addChild(self.edit_node)

	def set_cur_scene(self, cur_scene):
		self.log.info('set_cur_scene')
		assert isinstance(cur_scene, PASS.Layer) or isinstance(cur_scene, PASS.Behavior), cur_scene
		self.cur_scene = cur_scene
		#set offsets
		#print 'bb: ', self.cur_scene.getBoundingBox2D()
		bb = self.cur_scene.getBoundingBox2D()
		self.model_offset_x = bb[0][0]
		self.model_offset_y = bb[0][1]
		self.model_width = bb[1][0] - self.model_offset_x
		self.model_height = bb[1][1] - self.model_offset_y
		#print 'x min ', self.model_offset_x
		#print 'y min ', self.model_offset_y
		#print 'x dist ', self.model_width
		#print 'y dist ', self.model_height
		dist = 0.5 * self.model_width / math.tan((self.camera_fov - self.BORDER_ANGLE) * 0.5)
		VR.cam.setFrom(self.model_offset_x + 0.5 * self.model_width, self.model_offset_y + 0.5 * self.model_height, dist)
		self.scale_y = dist * math.tan(self.camera_fov * 0.5) * 2
		self.scale_x = self.scale_y / self.win_size[1] * self.win_size[0]

		dist_overview = 0.5 * self.model_width / math.tan(self.camera_fov * 0.5)
		self.cam_navigation.setFrom(self.model_offset_x + 0.5 * self.model_width, self.model_offset_y + 0.5 * self.model_height, dist_overview)

		# hide start view
		self.start_page_plane.setVisible(False)
		# show menus
		self.meta_plane.setVisible(True)
		params = self._create_url_params_from_object(self.cur_scene)
		self.meta_site.open('http://localhost:5500/meta' + '?' + params)
		self.navigation_plane.setVisible(True)
		self.navigation_plane_back.setVisible(True)
		for c in self.edit_node.getChildren():
			c.setVisible(False)
		if isinstance(cur_scene, PASS.Layer):
			self.edit_node.getChildren()[0].setVisible(True)
		elif isinstance(cur_scene, PASS.Behavior):  # is instance of Pass.Behavior
			self.edit_node.getChildren()[1].setVisible(True)
		else:
			self.log.info('set_cur_scene neither layer nor behavior')

		##VR.cam.addChild(self.active_gui_element) #TODO
		#self.scale_y = 2 *self.CAM_INIT_DIST * math.tan(self.camera_fov * 0.5)
		#self.scale_x = self.scale_y * self.win_size[0] / self.win_size[1]
		self.update_all()
		#VR.cam.setFrom(self.camera_from[0], self.camera_from[1], self.CAM_INIT_DIST + 10)


	def get_cur_scene(self):
		self.log.info('get_cur_scene')
		return self.cur_scene

	# update entire scene based on given scene self.cur_scene
	def update_all(self):
		self.log.info('update_all')
		#delete current scene
		scene_children = VR.view_root.getChildren()
		for child in scene_children:
			child.destroy()
		self.object_dict.clear()
		self.message_dict.clear()
		self.elements = []
		#setup path tool
		VR.ptool = VR.Pathtool()
		VR.ptool.setHandleGeometry(self.HANDLE)
		VR.ptool.getPathMaterial().setDiffuse(self.PATH_COLOR, self.PATH_COLOR, self.PATH_COLOR)
		VR.ptool.getPathMaterial().setTransparency(0.8)

		if isinstance(self.cur_scene, PASS.Layer):
			subjects = self.cur_scene.subjects
			message_exchanges = self.cur_scene.messageExchanges
			external_subjects = self.cur_scene.externalSubjects

			for subject in subjects:
				self._create_subject(subject)
			for message in message_exchanges:
				self._create_message(message)
			for subject in external_subjects:
				self._create_external_subject(subject)

		elif isinstance(self.cur_scene, PASS.Behavior):
			states = self.cur_scene.hasState
			edges = self.cur_scene.hasEdge

			for state in states:
				if isinstance(state, PASS.FunctionState):
					self._create_function_state(state)
				elif isinstance(state, PASS.SendState):
					self._create_send_state(state)
				elif isinstance(state, PASS.ReceiveState):
					self._create_receive_state(state)

			for edge in edges:
				self._create_transition_edge(edge)
		else:
			self.log.info('Failed to load current scene: has to be level or behavior')

	def zoom(self, level):
		self.log.info('zoom')
		print(("Zoom level: {}".format(self.current_zoom_level())))
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p, d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] >= self.MAX_DIST and not new_cam_pos[2] <= self.MIN_DIST:
			VR.cam.setFrom(new_cam_pos)
		self.scale_y = new_cam_pos[2] * math.tan(self.camera_fov * 0.5) * 2
		self.scale_x = self.scale_y / self.win_size[1] * self.win_size[0]

	def current_zoom_level(self):
		self.log.info('current_zoom_level')
		level = int(float(self.MAX_DIST - VR.cam.getFrom()[2]) / self.ZOOM_STEP)
		assert(level >= 0)
		return level
		
	def add_new_user(self, user_id, is_active):
		self.log.info('add_new_user({}, {})'.format(user_id, is_active))
		assert len(VR.view_user_cursors) < self.MAX_USERS
		
		VR.view_user_colors[user_id] = self.VALID_USER_COLORS[len(VR.view_user_cursors)]
		mat = VR.Material('cursor')
		mat.setDiffuse([VR.view_user_colors[user_id]])
		cursor_container_left = VR.Transform('Cursor_Container_Left')
		cursor_container_left.addTag(str([user_id, True]))
		cursor_container_left.setFrom(0.3, 0, self.CURSOR_DIST)
		if is_active:
			cursor_left_open = VR.loadGeometry(self.BLENDER_PATHS['open_hand_left'])
			cursor_left_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_hand_left'])
			cursor_right_open = VR.loadGeometry(self.BLENDER_PATHS['open_hand_right'])
			cursor_right_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_hand_right'])
		else:
			cursor_left_open = VR.loadGeometry(self.BLENDER_PATHS['open_pointer_left'])
			cursor_left_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_pointer_left'])
			cursor_right_open = VR.loadGeometry(self.BLENDER_PATHS['open_pointer_right'])
			cursor_right_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_pointer_right'])
		cursor_left_open.setFrom(0, 0, 0)
		cursor_left_open.setVisible(True)
		cursor_left_open.getChildren()[0].getChildren()[0].setColors([VR.view_user_colors[user_id]])	
		#cursor_left_open.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_left_closed.setFrom(0, 0, 0)
		cursor_left_closed.setVisible(False)
		cursor_left_closed.getChildren()[0].getChildren()[0].setColors([VR.view_user_colors[user_id]])
		#cursor_left_closed.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_container_left.addChild(cursor_left_open)
		cursor_container_left.addChild(cursor_left_closed)
		VR.cam.addChild(cursor_container_left)
		cursor_container_right = VR.Transform('Cursor_Container_Right')
		cursor_container_right.addTag(str([user_id, False]))
		cursor_container_right.setFrom(1.5, 0, self.CURSOR_DIST)		
		cursor_right_open.setFrom(0, 0, 0)
		cursor_right_open.setVisible(True)
		cursor_right_open.getChildren()[0].getChildren()[0].setColors([VR.view_user_colors[user_id]])
		#cursor_right_open.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_right_closed.setFrom(0, 0, 0)
		cursor_right_closed.setVisible(False)
		cursor_right_closed.getChildren()[0].getChildren()[0].setColors([VR.view_user_colors[user_id]])
		#cursor_right_closed.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_container_right.addChild(cursor_right_open)
		cursor_container_right.addChild(cursor_right_closed)
		#print "cursor container right", cursor_container_right.getChildren()
		#print "cursor container left", cursor_container_left.getChildren()
		VR.cam.addChild(cursor_container_right)
		
		VR.view_user_cursors[user_id] = {}
		mydev_l = VR.Device('mydev')
		mydev_l.setBeacon(cursor_container_left)
		mydev_l.addIntersection(self.edit_node)
		mydev_l.addIntersection(self.meta_plane)
		mydev_l.addIntersection(VR.view_root)
		mydev_r = VR.Device('mydev')
		mydev_r.setBeacon(cursor_container_right)
		#print "cursor container right", mydev_r.getBeacon().getChildren()
		#print "cursor container left", mydev_l.getBeacon().getChildren()
		mydev_r.addIntersection(self.edit_node)
		mydev_r.addIntersection(self.meta_plane)
		mydev_r.addIntersection(VR.view_root)
		self.edit_site.addMouse(mydev_l, self.edit_plane, 0, 2, 3, 4)
		self.edit_site.addMouse(mydev_r, self.edit_plane, 0, 2, 3, 4)
		self.meta_site.addMouse(mydev_l, self.meta_plane, 0, 2, 3, 4)
		self.meta_site.addMouse(mydev_r, self.meta_plane, 0, 2, 3, 4)
		self.layer_add_site.addMouse(mydev_l, self.layer_add_plane, 0, 2, 3, 4)
		self.layer_add_site.addMouse(mydev_r, self.layer_add_plane, 0, 2, 3, 4)
		self.behavior_add_site.addMouse(mydev_l, self.behavior_add_plane, 0, 2, 3, 4)
		self.behavior_add_site.addMouse(mydev_r, self.behavior_add_plane, 0, 2, 3, 4)
		VR.view_user_cursors[user_id][True] = mydev_l
		VR.view_user_cursors[user_id][False] = mydev_r
		VR.view_user_positions[user_id] = {}
		VR.view_user_positions[user_id][True] = [0, 0, 0]
		VR.view_user_positions[user_id][False] = [0, 0, 0]
		self.log.info('init new user done')

	def move_cursor(self, pos_ws, user_id, is_left):
		self.log.debug('move_cursor')
		
		assert isinstance(is_left, bool)
		assert isinstance(user_id, int)
		pos_ws = [(pos_ws[0] - 0.5) * self.scale_cursor_x, (pos_ws[1] - 0.5) * self.scale_cursor_y, self.CURSOR_DIST]
		#print 'View: pos_ws: ', pos_ws

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
		self.log.info('move_scene')
		cam_pos = VR.cam.getFrom()
		assert len(cam_pos) == 3
		assert len(translation) == 2
		new_cam_pos = [cam_pos[0] + translation[0] * self.MOVE_STEP, cam_pos[1] + translation[1] * self.MOVE_STEP, cam_pos[2]]
		VR.cam.setFrom(new_cam_pos)

	def set_highlight(self, obj, highlight):
		self.log.info('set_highlight')

		assert isinstance(highlight, bool)
		pass_obj = self.object_dict[obj]
		assert isinstance(pass_obj, VR.Object)
		children = pass_obj.getChildren()

		if highlight:
			for c in self.edit_node.getChildren():
				c.setVisible(False)
			self.edit_node.getChildren()[2].setVisible(True)
			pass
			# set edit gui element
			params = self._create_url_params_from_object(obj)
			self.meta_site.open('http://localhost:5500/meta' + '?' + params)

			if children[0].isVisible() is True:
				children[0].setVisible(False)
				children[2].setVisible(True)
				return True
			elif children[1].isVisible() is True:
				children[1].setVisible(False)
				children[3].setVisible(True)
				return True
		else:
			for c in self.edit_node.getChildren():
				c.setVisible(False)
			if isinstance(self.cur_scene, PASS.Layer):
				self.edit_node.getChildren()[0].setVisible(True)
			elif isinstance(self.cur_scene, PASS.Behavior):
				self.edit_node.getChildren()[1].setVisible(True)
			else:
				self.log.error('ERROR (view): Current scene neither of type Layer nor Behavior')

			#set metaContent on gui element meta to parent
			params = self._create_url_params_from_object(self.cur_scene)
			self.meta_site.open('http://localhost:5500/meta' + '?' + params)

			if children[2].isVisible() is True:
				children[2].setVisible(False)
				children[0].setVisible(True)
				return True
			elif children[3].isVisible() is True:
				children[3].setVisible(False)
				children[1].setVisible(True)
				return True
		return False

	def _create_url_params_from_object(self, obj):
		self.log.info('create_url_params_from_metacontent')
		
		label_key = 'sbpm_label'
		label_value = ''
		if isinstance(obj, PASS.Layer):
			label_value = 'Layer'
			label_key = 'sbpm_noEditLabel'
		elif isinstance(obj, PASS.Behavior):				
			label_value = 'Behavior'
			label_key = 'sbpm_noEditLabel'
		elif len(obj.label) > 0:
			label_value = obj.label[0]
		
		params = label_key + '=' + label_value + '&'
		metaKeys = obj.getMetaKeys()
		i = 0
		while i < len(metaKeys):
			params = params + str(metaKeys[i]) + '=' + str(obj.getMetaContent(metaKeys[i])[0])
			i = i + 1
			if(i != len(metaKeys)):
				params = params + '&'
		self.log.info('parameter website {}'.format(params))
		return params

	def highlight_pos(self, pos):  # returns the added highlight
		self.log.info('highlight_pos')
		assert len(pos) == 2

		highlighted_point = VR.Geometry('sphere')
		highlighted_point.setPrimitive('Sphere 0.1 5')
		highlighted_point.setMaterial(VR.Material('sample material'))
		w_pos = self.local_to_world_2d(pos)
		highlighted_point.setFrom(w_pos[0], w_pos[1], 0.0)
		highlighted_point.setPlaneConstraints([0, 0, 1])
		highlighted_point.setRotationConstraints([1, 1, 1])
		highlighted_point.setColors([[0.21, 0.57, 0.83]])
		highlighted_point.setPickable(False)
		highlighted_point.addTag('highlight')
		VR.view_root.addChild(highlighted_point)

		return highlighted_point

	def remove_highlight_point(self, highlight_point):  # remove the given highlighted object from scene
		self.log.info('remove_highlight_pos')
		if isinstance(highlight_point, VR.Object):
			highlight_point.destroy()

	def trigger_down(self, user_id, is_left):
		self.log.warning('trigger_down({}, {})'.format(user_id, is_left))
		mydev = VR.view_user_cursors[user_id][is_left]
		assert mydev is not None, 'user {} has no VR device (is_left={})'.format(user_id, is_left)
		mydev.trigger(0, 1)

	def trigger_up(self, user_id, is_left):
		self.log.warning('trigger_up({}, {})'.format(user_id, is_left))
		mydev = VR.view_user_cursors[user_id][is_left]
		assert mydev is not None, 'user {} has no VR device (is_left={})'.format(user_id, is_left)
		mydev.trigger(0, 0)

	def release(self, user_id, is_left):
		mydev = VR.view_user_cursors[user_id][is_left]
		beacon_children = mydev.getBeacon().getChildren()
		assert len(beacon_children) > 1, "Beacon must have at least two children"
		beacon_children[0].setVisible(True)
		beacon_children[1].setVisible(False)

	def press(self, user_id, is_left):
		mydev = VR.view_user_cursors[user_id][is_left]
		beacon_children = mydev.getBeacon().getChildren()
		assert len(beacon_children) > 1, "Beacon must have at least two children"
		beacon_children[0].setVisible(False)
		beacon_children[1].setVisible(True)

	def get_object(self, user_id, is_left):
		self.log.info('get_object')
		mydev = VR.view_user_cursors[user_id][is_left]
		if mydev.intersect():
			i = mydev.getIntersected()
			tags = i.getTags()
			self.log.info( 'View tags: {} name: {} id {} {}'.format(tags, i.getName(), i.getID(), i))
			if i.hasTag('edit'):
				self.log.info('view: edit')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['edit']
			elif i.hasTag('meta'):
				self.log.info('view: meta')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['meta']
			elif i.hasTag('layer_add'):
				self.log.info('view: layer_add')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['layer_add']
			elif i.hasTag('behavior_add'):
				self.log.info('view: behavior_add')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['behavior_add']
			#elif 'obj' in tags:
			else:
				#print 'view: object'
				
				p = i.getParent().getParent().getParent()
				if p.hasTag('obj'):
					return self.object_dict[p]
				elif i.hasTag('obj'):
					return self.object_dict[i]
				else:
					self.log.info('No valid intersected object in get_object')
		else:
			self.log.info('No intersection. Empty space clicked.')
		return None

	def rotate(self, degrees):
		self.log.info('rotate')
		pass

	def _create_subject(self, pass_sub):
		assert isinstance(pass_sub, PASS.Subject)
		self.elements.append(pass_sub)
		pos = pass_sub.hasAbstractVisualRepresentation.hasPoint2D
		subject_node = VR.Transform('Subject_Container')
		subject_node.addTag('obj')
		subject_node.addTag('subject')
		subject_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		subject_node.setPlaneConstraints([0, 0, 1])
		subject_node.setRotationConstraints([1, 1, 1])
		poly_subjects = []
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['subject']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['subject_meta']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['subject_highlight']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['subject_meta_highlight']))
		for poly_sub in poly_subjects:
			poly_sub.setFrom(0, 0, 0)
			poly_sub.setPickable(True)
			poly_sub.setScale(self.OBJECT_SCALE)
			poly_sub.setVisible(False)
			subject_node.addChild(poly_sub)
		if len(pass_sub.hasMetaContent) == 0:
			subject_node.getChildren()[0].setVisible(True)
		else:
			subject_node.getChildren()[1].setVisible(True)
		
		# create label
		if len(pass_sub.label) == 0:
			label = ''
		else:
			label = pass_sub.label[0]
		label_split = str.split(label)
		for l in label_split:
			sprite = VR.Sprite('label')
			sprite.setFrom(self.TEXT_SIZE / 2, label_split.index(l), self.TEXT_SIZE)
			sprite.setSize(0.1 * len(l), 0.1)
			#print 'label', l
			sprite.setText(l)
			subject_node.addChild(sprite)	
		
		self.object_dict[pass_sub] = subject_node
		self.object_dict[subject_node] = pass_sub
		VR.view_root.addChild(subject_node) 
		#VR.view_root.addChild(sprite)

	def _create_message(self, pass_mes):
		assert isinstance(pass_mes, PASS.MessageExchange)
		self.elements.append(pass_mes)
		pos = pass_mes.hasAbstractVisualRepresentation.hasPoint2D
		message_node = VR.Transform('Message_Container')
		message_node.addTag('obj')
		message_node.addTag('message')
		message_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		message_node.setPlaneConstraints([0, 0, 1])
		message_node.setRotationConstraints([1, 1, 1])
		poly_mesages = []
		poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message']))
		poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta']))
		poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_highlight']))
		poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta_highlight']))
		for poly_mes in poly_mesages:
			poly_mes.setPickable(True)
			poly_mes.setScale(self.OBJECT_SCALE)
			poly_mes.setVisible(False)
			message_node.addChild(poly_mes)
		if len(pass_mes.hasMetaContent) == 0:
			message_node.getChildren()[0].setVisible(True)
		else:
			message_node.getChildren()[1].setVisible(True)
			
		# create label		
		if len(pass_mes.label) == 0:
			label = ''
		else:
			label = pass_mes.label[0]
		label_split = str.split(label)
		for l in label_split:
			sprite = VR.Sprite('label')
			sprite.setFrom(self.TEXT_SIZE / 2, label_split.index(l) * 10, self.TEXT_SIZE)
			sprite.setSize(0.1 * len(l), 0.1)
			#print 'label', l
			sprite.setText(l)
			message_node.addChild(sprite)		
		self.object_dict[pass_mes] = message_node
		self.object_dict[message_node] = pass_mes
		self.message_dict[message_node] = [self.object_dict[pass_mes.sender], self.object_dict[pass_mes.receiver], None, None, None]
		self.connect(message_node)
		VR.view_root.addChild(message_node)

	def _create_external_subject(self, pass_exsub):
		pos = pass_exsub.hasAbstractVisualRepresentation.hasPoint2D
		self.elements.append(pass_exsub)
		subject_node = VR.Transform('External_Subject_Container')
		subject_node.addTag('obj')
		subject_node.addTag('external_subject')
		subject_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		subject_node.setPlaneConstraints([0, 0, 1])
		subject_node.setRotationConstraints([1, 1, 1])
		poly_subjects = []
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_highlight']))
		poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta_highlight']))
		for poly_sub in poly_subjects:
			poly_sub.setPickable(True)
			poly_sub.setScale(self.OBJECT_SCALE)
			poly_sub.setVisible(False)
			subject_node.addChild(poly_sub)
		if len(pass_exsub.hasMetaContent) == 0:
			subject_node.getChildren()[0].setVisible(True)
		else:
			subject_node.getChildren()[1].setVisible(True)
			
		# create label
		sprite = VR.Sprite('label')
		sprite.setFrom(self.TEXT_SIZE / 2, 0, self.TEXT_SIZE)
		if len(pass_exsub.label) == 0:
			label = ''
		else:
			label = pass_exsub.label[0]
		sprite.setSize(0.1 * len(label), 0.1)
		#print 'label', label
		sprite.setText(label)
		subject_node.addChild(sprite)
		
		self.object_dict[pass_exsub] = subject_node
		self.object_dict[subject_node] = pass_exsub
		VR.view_root.addChild(subject_node)

	def _create_function_state(self, state):
		assert isinstance(state, PASS.State)
		self.elements.append(state)
		pos = state.hasAbstractVisualRepresentation.hasPoint2D
		state_node = VR.Transform('State_Container')
		state_node.addTag('obj')
		state_node.addTag('function_state')
		state_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		state_node.setPlaneConstraints([0, 0, 1])
		state_node.setRotationConstraints([1, 1, 1])
		poly_states = []
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_meta']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_highlight']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_meta_highlight']))
		for poly_sub in poly_states:
			poly_sub.setPickable(True)
			poly_sub.setScale(self.OBJECT_SCALE)
			poly_sub.setVisible(False)
			state_node.addChild(poly_sub)
		if len(state.hasMetaContent) == 0:
			state_node.getChildren()[0].setVisible(True)
		else:
			state_node.getChildren()[1].setVisible(True)
			
		# create label
		sprite = VR.Sprite('label')
		sprite.setFrom(self.TEXT_SIZE / 2, 0, self.TEXT_SIZE)
		if len(state.label) == 0:
			label = ''
		else:
			label = state.label[0]
		sprite.setSize(0.1 * len(label), 0.1)
		#print 'label', label
		sprite.setText(label)
		state_node.addChild(sprite)
		
		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

	def _create_send_state(self, state):
		assert isinstance(state, PASS.State)
		self.elements.append(state)
		pos = state.hasAbstractVisualRepresentation.hasPoint2D
		state_node = VR.Transform('State_Container')
		state_node.addTag('send_state')
		state_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		state_node.setPlaneConstraints([0, 0, 1])
		state_node.setRotationConstraints([1, 1, 1])
		poly_states = []
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_meta']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_highlight']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_meta_highlight']))
		for poly_sub in poly_states:
			poly_sub.setPickable(True)
			poly_sub.setScale(self.OBJECT_SCALE)
			poly_sub.setVisible(False)
			state_node.addChild(poly_sub)
		if len(state.hasMetaContent) == 0:
			state_node.getChildren()[0].setVisible(True)
		else:
			state_node.getChildren()[1].setVisible(True)
			
		# create label
		sprite = VR.Sprite('label')
		sprite.setFrom(self.TEXT_SIZE / 2, 0, self.TEXT_SIZE)
		if len(state.label) == 0:
			label = ''
		else:
			label = state.label[0]
		sprite.setSize(0.1 * len(label), 0.1)
		#print 'label', label
		sprite.setText(label)
		state_node.addChild(sprite)
		
		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

	def _create_receive_state(self, state):
		assert isinstance(state, PASS.State)
		self.elements.append(state)
		pos = state.hasAbstractVisualRepresentation.hasPoint2D
		state_node = VR.Transform('State_Container')
		state_node.addTag('receive_state')
		state_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		state_node.setPlaneConstraints([0, 0, 1])
		state_node.setRotationConstraints([1, 1, 1])
		poly_states = []
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_meta']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_highlight']))
		poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_meta_highlight']))
		for poly_sub in poly_states:
			poly_sub.setPickable(True)
			poly_sub.setScale(self.OBJECT_SCALE)
			poly_sub.setVisible(False)
			state_node.addChild(poly_sub)
		if len(state.hasMetaContent) == 0:
			state_node.getChildren()[0].setVisible(True)
		else:
			state_node.getChildren()[1].setVisible(True)
			
		# create label
		sprite = VR.Sprite('label')
		sprite.setFrom(self.TEXT_SIZE / 2, 0, self.TEXT_SIZE)
		if len(state.label) == 0:
			label = ''
		else:
			label = state.label[0]
		sprite.setSize(0.1 * len(label), 0.1)
		#print 'label', label
		sprite.setText(label)
		state_node.addChild(sprite)
		
		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

	def _create_transition_edge(self, edge):
		assert isinstance(edge, PASS.TransitionEdge)
		self.elements.append(edge)
		pos = edge.hasAbstractVisualRepresentation.hasPoint2D
		transition_node = VR.Transform('Transition_Container')
		transition_node.addTag('obj')
		transition_node.addTag('transition')
		transition_node.setFrom(pos.hasXValue, pos.hasYValue, 0)
		transition_node.setPlaneConstraints([0, 0, 1])
		transition_node.setRotationConstraints([1, 1, 1])
		poly_trans = []
		poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition']))
		poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta']))
		poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_highlight']))
		poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta_highlight']))
		for poly_mes in poly_trans:
			poly_mes.setPickable(True)
			poly_mes.setScale(self.OBJECT_SCALE)
			poly_mes.setVisible(False)
			transition_node.addChild(poly_mes)
		if len(edge.hasMetaContent) == 0:
			transition_node.getChildren()[0].setVisible(True)
		else:
			transition_node.getChildren()[1].setVisible(True)
			
		# create label
		sprite = VR.Sprite('label')
		sprite.setFrom(self.TEXT_SIZE / 2, 0, self.TEXT_SIZE)
		if len(edge.label) == 0:
			label = ''
		else:
			label = edge.label[0]
		sprite.setSize(0.1 * len(label), 0.1)
		#print 'label', label
		sprite.setText(label)
		transition_node.addChild(sprite)
		
		self.object_dict[edge] = transition_node
		self.object_dict[transition_node] = edge
		self.message_dict[transition_node] = [self.object_dict[edge.hasSourceState], self.object_dict[edge.hasTargetState], None, None, None]
		self.connect(transition_node)
		VR.view_root.addChild(transition_node)

	def on_change(self, object, attr):
		self.log.info('on_change: obj: {} attr: {}'.format(object, attr))
		if isinstance(self.cur_scene, PASS.Layer) and (isinstance(object, PASS.Layer) or isinstance(object, PASS.Subject) \
				or isinstance(object, PASS.ExternalSubject) or isinstance(object, PASS.MessageExchange)):
			if not isinstance(object, PASS.Layer) and not object in self.object_dict:  # create new layer object
				if isinstance(object, PASS.Subject):
					self._create_subject(object)
				elif isinstance(object, PASS.MessageExchange):
					self._create_message(object)
				elif isinstance(object, PASS.ExternalSubject):
					self._create_external_subject(object)
			elif isinstance(object, PASS.Layer):
				self.log.info('onchange layer')
				if attr == "hasModelComponent":
					list_of_elements = object.hasModelComponent
					list_of_elements = [x for x in list_of_elements if isinstance(x, PASS.Subject) or isinstance(x, PASS.MessageExchange) or isinstance(x, PASS.ExternalSubject)]
					element_to_delete = set(self.elements) - set(list_of_elements)
					element_to_delete = list(element_to_delete)
					assert len(element_to_delete) < 2, "More than one element to delete"
					if len(element_to_delete) == 1:
						if isinstance(element_to_delete[0], PASS.Subject) or isinstance(element_to_delete[0], PASS.ExternalSubject):
							poly_mes = self._get_attached_message(element_to_delete[0])
							if poly_mes is not None:  # delete attached message
								mes = self.object_dict[poly_mes]
								paths_to_delete = self.message_dict[poly_mes][2]
								for p in paths_to_delete:
									VR.ptool.remPath(p)
								del self.object_dict[mes]
								del self.object_dict[poly_mes]
								del self.message_dict[poly_mes]
								self.elements.remove[mes]
								poly_mes.destroy()
							poly_obj = self.object_dict[element_to_delete[0]]
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							self.elements.remove(element_to_delete[0])
							poly_obj.destroy()
						elif isinstance(element_to_delete[0], PASS.MessageExchange):
							poly_obj = self.object_dict[element_to_delete[0]]
							paths_to_delete = self.message_dict[poly_obj][2]
							for p in paths_to_delete:
								VR.ptool.remPath(p)
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							del self.message_dict[poly_obj]
							self.elements.remove(element_to_delete[0])
							poly_obj.destroy()
					else:
						self.log.info('Skip, Element added.')
			else:
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				poly_obj = self.object_dict[object]
				if attr == 'hasAbstractVisualRepresentation':  # position changed
					self.log.debug("moving subject to {}, {}, {}".format(((pos.hasXValue - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x, ((pos.hasYValue - self.model_offset_y) / self.model_height - 0.5) * self.scale_y, 0.0))
					poly_obj.setFrom(pos.hasXValue, pos.hasYValue, 0)
				elif attr == 'label':  # name changed
					if len(object.label) == 0:
						label = ''
					else:
						label = object.label[0]
					poly_obj.getChildren()[4].setText(label)
				elif attr == 'hasMetaContent':
					#TODO meta data changed
					children = poly_obj.getChildren()
					
					for i, c in enumerate(children):
						if c.isVisible():
							if i == 0 or i == 1:
								c.setVisible(False)
								if len(object.hasMetaContent) == 0:
									children[0].setVisible(True)
								else:
									children[1].setVisible(True)
							elif i == 2 or i == 3:
								c.setVisible(False)
								if len(object.hasMetaContent) == 0:
									children[2].setVisible(True)
								else:
									children[3].setVisible(True)
							break
				else:
					self.log.info('Invalid attribute in on_change')

		elif isinstance(self.cur_scene, PASS.Behavior) and (isinstance(object, PASS.State) or isinstance(object, PASS.TransitionEdge)):
			if not isinstance(object, PASS.Behavior) and not object in self.object_dict:  # create new layer object
				if isinstance(object, PASS.SendState):
					self._create_send_state(object)
				elif isinstance(object, PASS.FunctionState):
					self._create_function_state(object)
				elif isinstance(object, PASS.ReceiveState):
					self._create_receive_state(object)
				elif isinstance(object, PASS.TransitionEdge):
					self._create_transition_edge(object)
			elif isinstance(object, PASS.Behavior):
				self.log.info('onchange behavior')
				if attr == "hasModelComponent":
					list_of_elements = object.hasModelComponent
					list_of_elements = [x for x in list_of_elements if isinstance(x, PASS.Subject) or isinstance(x, PASS.MessageExchange) or isinstance(x, PASS.ExternalSubject)]
					element_to_delete = set(self.elements) - set(list_of_elements)
					assert len(element_to_delete) < 2, "More than one element to delete"
					if len(element_to_delete) == 1:
						if isinstance(element_to_delete[0], PASS.Subject) or isinstance(element_to_delete[0], PASS.ExternalSubject):
							poly_obj = self.object_dict[element_to_delete[0]]
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							poly_obj.destroy()
						elif isinstance(element_to_delete[0], PASS.MessageExchange):
							poly_obj = self.object_dict[element_to_delete[0]]
							paths_to_delete = self.message_dict[poly_obj][2]
							for p in paths_to_delete:
								VR.ptool.remPath(p)
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							del self.message_dict[poly_obj]
							poly_obj.destroy()
					else:
						self.log.info('Skip, Element added.')
			else:
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				poly_obj = self.object_dict[object]
				if attr == 'hasAbstractVisualRepresentation':  # position changed
					self.log.debug("moving subject to {}, {}, {}".format(((pos.hasXValue - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x, ((pos.hasYValue - self.model_offset_y) / self.model_height - 0.5) * self.scale_y, 0.0))
					poly_obj.setFrom(pos.hasXValue, pos.hasYValue, 0)
				elif attr == 'label':  # name changed
					if len(object.label) == 0:
						label = ''
					else:
						label = object.label[0]
					poly_obj.getChildren()[4].setText(label)
				elif attr == 'hasMetaContent':
					#TODO meta data changed
					children = poly_obj.getChildren()
					
					for i, c in enumerate(children):
						if c.isVisible():
							if i == 0 or i == 1:
								c.setVisible(False)
								if len(object.hasMetaContent) == 0:
									children[0].setVisible(True)
								else:
									children[1].setVisible(True)
							elif i == 2 or i == 3:
								c.setVisible(False)
								if len(object.hasMetaContent) == 0:
									children[2].setVisible(True)
								else:
									children[3].setVisible(True)
							break
				else:
					self.log.info('Invalid attribute in on_change')
		elif isinstance(self.cur_scene, PASS.Layer) or isinstance(self.cur_scene, PASS.Behavior):
			self.log.info("Ignoring weird on_change object: {}".format(object))
		else:
			self.log.warning('VIEW ERROR: self.cur_scene must be of type Layer or Behavior but is: {}'.format(self.cur_scene))

	def _get_attached_message(self, subject):
		self.log.info('object {}'.format(subject))
		poly_sub = self.object_dict[subject]
		for i in self.message_dict:
			if self.message_dict[i][0] is poly_sub or self.message_dict[i][1] is poly_sub:
				self.log.info('attached message {}'.format(i))
				return i
		return None

	def connect(self, message):
		self.log.info('connect({})'.format(message))
		assert isinstance(message, VR.Transform), "parameter must be of VR.Transform type"
		assert message in self.message_dict, "parameter must be in message_dict"

		s = self.message_dict[message][0]
		r = self.message_dict[message][1]
		assert s is not None and r is not None, "sender and receiver must not be None"
		s_pos = s.getFrom()
		m_pos = message.getFrom()
		r_pos = r.getFrom()

		#calc directions
		s_dir = [0, 0]
		m_dir_1 = [0, 0]
		m_dir_2 = [0, 0]
		r_dir = [0, 0]
		#calc handel start_pos and mid_pos
		if s_pos[0] < m_pos[0]:
			#start_pos handle right
			s_dir = [-1, 0]
			if s_pos[1] < m_pos[1]:
				#mes_pos handle bottom
				m_dir_1 = [0, 1]
			elif s_pos[1] == m_pos[1]:
				#mes_pos handle left
				m_dir_1 = [1, 0]
			else:
				#mes_pos handle top
				m_dir_1 = [0, -1]
		elif s_pos[0] == m_pos[0]:
			#start_pos handle middle
			if s_pos[1] < m_pos[1]:
				#start_pos middle top
				m_dir_1 = [0, 1]
				s_dir = [0, -1]
			else:
				#start_pos middle bottom
				m_dir_1 = [0, -1]
				s_dir = [0, 1]
		else:
			#start_pos handle left
			s_dir = [1, 0]
			if s_pos[1] < m_pos[1]:
				#mes_pos handle bottom
				m_dir_1 = [0, 1]
			elif s_pos[1] == m_pos[1]:
				#mes_pos handle right
				m_dir_1 = [-1, 0]
			else:
				#mes_pos handle top
				m_dir_1 = [0, -1]
		#calc handel end_pos and mid_pos
		if r_pos[0] < m_pos[0]:
			#end_pos handle right
			r_dir = [-1, 0]
			if r_pos[1] < m_pos[1]:
				#mes_pos handle bottom
				m_dir_2 = [0, 1]
			elif r_pos[1] == m_pos[1]:
				#mes_pos handle left
				m_dir_2 = [1, 0]
			else:
				#mes_pos handle top
				m_dir_2 = [0, -1]
		elif r_pos[0] == m_pos[0]:
			#end_pos handle middle
			if r_pos[1] < m_pos[1]:
				#end_pos middle top
				m_dir_2 = [0, 1]
				r_dir = [0, -1]
			else:
				#start_pos middle bottom
				m_dir_2 = [0, -1]
				r_dir = [0, 1]
		else:
			#end_pos handle left
			r_dir = [1, 0]
			if r_pos[1] < m_pos[1]:
				#mes_pos handle bottom
				m_dir_2 = [0, 1]
			elif r_pos[1] == m_pos[1]:
				#mes_pos handle right
				m_dir_2 = [-1, 0]
			else:
				#mes_pos handle top
				m_dir_2 = [0, -1]
				
		self.log.debug("View:", 's_pos', s_pos, 'm_pos', m_pos, 'r_pos', r_pos)
		self.log.debug("View:", 's_dir', s_dir, 'm_dir_1', m_dir_1, 'm_dir_2', m_dir_2, 'r_dir', r_dir)
		self.log.debug("View:", "draw_line: ", s, " => ", message, " => ", r)

		#set path from sender
		m_paths = []
		self.paths.append(VR.ptool.newPath(None, VR.view_root))
		m_paths.append(self.paths[-1])
		handles = VR.ptool.getHandles(self.paths[-1])
		assert len(handles) == 2, "invalid number of handles"
		handles[0].setFrom(-s_dir[0] * self.OBJECT_SCALE[0] * 1.3, -s_dir[1] * self.OBJECT_SCALE[0] * 1.3, 0)
		handles[0].setUp(-20 * s_dir[1], s_dir[0], 0.0)
		handles[0].setPickable(False)
		s.addChild(handles[0])
		handles[1].setFrom(-m_dir_1[0] * self.OBJECT_SCALE[0] * 0.6, -m_dir_1[1] * self.OBJECT_SCALE[1] * 0.6, 0)
		handles[1].setUp(-20 * m_dir_1[1], m_dir_1[0], 0.0)
		handles[1].setPickable(False)
		message.addChild(handles[1])

		#set path to receiver
		self.paths.append(VR.ptool.newPath(None, VR.view_root))
		m_paths.append(self.paths[-1])
		VR.ptool.extrude(None, self.paths[-1])
		handles = VR.ptool.getHandles(self.paths[-1])
		assert len(handles) == 3, "invalid number of handles"
		handles[0].setFrom(-m_dir_2[0] * self.OBJECT_SCALE[0] * 0.6, -m_dir_2[1] * self.OBJECT_SCALE[0] * 0.6, 0)
		handles[0].setUp(-20 * m_dir_2[1], m_dir_2[0], 0.0)
		handles[0].setPickable(False)
		message.addChild(handles[0])
		handles[1].setFrom(-r_dir[0] * self.OBJECT_SCALE[0] * 2, -r_dir[1] * self.OBJECT_SCALE[1] * 2, 0)
		handles[1].setUp(-20 * r_dir[1], r_dir[0], 0.0)
		handles[1].setPickable(False)
		handles[2].setFrom(-r_dir[0] * self.OBJECT_SCALE[0] * 1.3, -r_dir[1] * self.OBJECT_SCALE[1] * 1.3, 0)
		handles[2].setUp(-20 * r_dir[1], r_dir[0], 0.0)
		handles[2].setPickable(False)
		handle_arrow = VR.loadGeometry(self.BLENDER_PATHS['arrow_tip'])
		handle_arrow.setScale(0.7, 0.7, 0.7)
		#handle_arrow = copy.deepcopy(self.HANDLE_ARROW)
		#handle_arrow.getParent().setColors(195, 100, 20)
		handles[2].addChild(handle_arrow)
		r.addChild(handles[1])
		r.addChild(handles[2])
		
		self.message_dict[message][2] = m_paths
		VR.ptool.update()

	def set_message_line(self, user_id, set_line):
		self.log.info("drawing line")
		if set_line:
			if self.new_message_path is not None:
				return
			self.paths.append(VR.ptool.newPath(None, VR.view_root))
			handles = VR.ptool.getHandles(self.paths[-1])
			assert len(handles) == 2, "invalid number of handles"
			handles[0].setPickable(False)
			handles[0].setFrom(0, 0, 0)
			VR.view_user_cursors[user_id][0].getBeacon().addChild(handles[0])
			handles[1].setFrom(0, 0, 0)
			handles[1].setPickable(False)
			VR.view_user_cursors[user_id][1].getBeacon().addChild(handles[1])
			self.new_message_path = self.paths[-1]
			VR.ptool.update()
		else:
			if self.new_message_path is not None:
				self.log.info('delete')
				VR.ptool.remPath(self.new_message_path)
				self.new_message_path = None
			else:
				self.log.info("Warning: no message path to be deleted...")

	def local_to_world_2d(self, local_pos):
		#transformation
		assert len(local_pos) == 2, "local_pos must have a length of 2"
		return [(local_pos[0] - 0.5) * self.scale_x + VR.cam.getFrom()[0], (local_pos[1] - 0.5) * self.scale_y + VR.cam.getFrom()[1]]

	def show_init_screen(self, init_list):
		self.log.info("show_init_screen({})".format(init_list))
		params = ''
		for i in init_list:
			assert isinstance(i, self.InitScreenEntry)
			params = params + str(i.display_name) + '=' + str(i.image_file_name) + '=' + str(i.model_id)
			if(init_list.index(i) != len(init_list) - 1):
				params = params + '&'

		self.log.info('parameter website {}'.format(params))
		self.start_page_site.open('http://localhost:5500/start' + '?' + params)
		self.start_page_plane.setVisible(True)
