import VR
import math
import PASS
import logging

class View():
	"""
	This class creates the view of the application and handels all interaction with it.
	
	:version: 2016-02-10
	:author: Mirjam Joechner and Kai Hartung
	"""
	
	class MenuBar():
		"""
		TODO
		
		"""
		def __init__(self, name):
			self.name = name

	class InitScreenEntry():
		"""
		TODO
		
		"""
		def __init__(self, display_name, file_name, image_file_name, model_id):
			"""
			Constructor of InitScreenEntry.

			@param str display_name : The name that is displayed in the application.
			@param str file_name : The URI where the file is located.
			@param str image_file_name : The file name of the according image.
			@param str model_id : The unique model id.
			@return  : None
			"""
			self.display_name = display_name
			self.file_name = file_name
			self.image_file_name = image_file_name
			self.model_id = model_id

		def __str__(self):
			"""
			This function returns a str-representation.

			@return str : String representation of InitScreenEntry.
			"""
			return "InitScreenEntry: {}, {}, {}".format(self.display_name, self.file_name, self.image_file_name)

	def __init__(self):
		"""
		Constructor of View.

		@return  : None
		"""
		self.log = logging.getLogger()
		#self.log.setLevel(logging.DEBUG)  # DEBUG INFO WARNING ...
		#ch = logging.StreamHandler(sys.stdout)
		#ch.setLevel(logging.DEBUG)
		#formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		#ch.setFormatter(formatter)
		#self.log.addHandler(ch)
		self.log.info("VIEW: Starting view")

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
		self.TEXT_SIZE = 0.06
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
			'behavior_add': self.MenuBar('behavior_add'),
			'start_page': self.MenuBar('start_page')
		}

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dict = {}
		self.message_dict = {}  # key: poly_mess, 1. entry: poly_sender, 2. entry: poly_receiver, 3. entry: path
		self.annotation_dict = {} # key: pass object, 1. entry: list(index)
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
		self._setup_menu_bar()

		# start page
		self._setup_start_page()

	def _setup_start_page(self):
		"""
		This function creates a start page to select an existing model or to create a new one.

		@return  : None
		"""
		self.log.info('VIEW: setup_start_page')
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

	def _setup_menu_bar(self):
		"""
		This function creates the menu bars when a model is selected.

		@return  : None
		"""
		self.log.info('VIEW: setup_menu_bar')
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
		"""
		This function sets the current scene of the selected model.

		@param PASS.Layer or PASS.Behavior cur_scene : The scene to set.
		@return  : None
		"""
		self.log.info('VIEW: set_cur_scene')
		assert isinstance(cur_scene, PASS.Layer) or isinstance(cur_scene, PASS.Behavior), cur_scene
		self.cur_scene = cur_scene
		#set offsets
		#print 'boundingbox: ', self.cur_scene.getBoundingBox2D()
		bb = self.cur_scene.getBoundingBox2D()
		self.model_offset_x = bb[0][0]
		self.model_offset_y = bb[0][1]
		self.model_width = bb[1][0] - self.model_offset_x
		self.model_height = bb[1][1] - self.model_offset_y
		if self.model_height == 0:
			self.model_height = 10
		if self.model_width == 0:
			self.model_width = 10

		#print 'x min ', self.model_offset_x
		#print 'y min ', self.model_offset_y
		#print 'x dist ', self.model_width
		#print 'y dist ', self.model_height
		dist = 0.5 * self.model_width / math.tan((self.camera_fov - self.BORDER_ANGLE) * 0.5)
		if dist <= self.MAX_DIST and dist >= self.MIN_DIST:
			VR.cam.setFrom(self.model_offset_x + 0.5 * self.model_width, self.model_offset_y + 0.5 * self.model_height, dist)
		else:
			VR.cam.setFrom(self.model_offset_x + 0.5 * self.model_width, self.model_offset_y + 0.5 * self.model_height, self.MAX_DIST)
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
			self.log.info('VIEW: set_cur_scene neither layer nor behavior')
		self._update_all()

	def get_cur_scene(self):
		"""
		This function returns the current scene.

		@return PASS.Layer or PASS.Behavior : The current scene.
		"""
		self.log.info('VIEW: get_cur_scene')
		return self.cur_scene

	def _update_all(self):
		"""
		This function updates the entire scene based on the given self.cur_scene.

		@return  : None
		"""
		self.log.info('VIEW: update_all')
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
		
		#setup annotation engine
		self.annotation_index = 1
		self.annotation_engine = VR.AnnotationEngine('annotation_engine')
		VR.view_root.addChild(self.annotation_engine)
		self.annotation_engine.setColor([0, 0, 0, 1])
		self.annotation_engine.setPickable(False)
		#self.annotation_engine.setBackground([255, 255, 255, 1])
		self.annotation_engine.setSize(self.TEXT_SIZE)
		self.annotation_engine.setScale([1, 1, 1])

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
			self.log.info('VIEW: Failed to load current scene: has to be level or behavior')

	def zoom(self, level):
		"""
		This function moves the camera to create a zoom effect.

		@param int level : The level to zoom.
		@return  : None
		"""
		self.log.info('VIEW: zoom')
		self.log.info("VIEW: Zoom level: {}".format(self.current_zoom_level()))
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p, d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] >= self.MAX_DIST and not new_cam_pos[2] <= self.MIN_DIST:
			VR.cam.setFrom(new_cam_pos)
		self.scale_y = new_cam_pos[2] * math.tan(self.camera_fov * 0.5) * 2
		self.scale_x = self.scale_y / self.win_size[1] * self.win_size[0]

	def current_zoom_level(self):
		"""
		This function return the current zoom level.

		@return int : The current zoom level
		"""
		self.log.info('VIEW: current_zoom_level')
		level = int(float(self.MAX_DIST - VR.cam.getFrom()[2]) / self.ZOOM_STEP)
		assert(level >= 0)
		return level
		
	def add_new_user(self, user_id, is_active):
		"""
		This function adds a new user to the view.

		@param int user_id : The user id of the new user.
		@param bool is_active : Indication if new user is active or passive.
		@return  : None
		"""
		self.log.info('VIEW: add_new_user({}, {})'.format(user_id, is_active))
		assert len(VR.view_user_cursors) < self.MAX_USERS
		
		VR.view_user_colors[user_id] = self.VALID_USER_COLORS[len(VR.view_user_cursors)]
		cursor_container_left = VR.Transform('Cursor_Container_Left')
		cursor_container_left.addTag(str([user_id, True]))
		cursor_container_left.setFrom(0.3, 0, self.CURSOR_DIST)
		if is_active:
			cursor_left_open = VR.loadGeometry(self.BLENDER_PATHS['open_hand_left'], 1)
			cursor_left_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_hand_left'], 1)
			cursor_right_open = VR.loadGeometry(self.BLENDER_PATHS['open_hand_right'], 1)
			cursor_right_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_hand_right'], 1)
		else:
			cursor_left_open = VR.loadGeometry(self.BLENDER_PATHS['open_pointer_left'], 1)
			cursor_left_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_pointer_left'], 1)
			cursor_right_open = VR.loadGeometry(self.BLENDER_PATHS['open_pointer_right'], 1)
			cursor_right_closed = VR.loadGeometry(self.BLENDER_PATHS['closed_pointer_right'], 1)
		cursor_left_open.setFrom(0, 0, 0)
		cursor_left_open.setVisible(True)
		
		mat = VR.Material('cursorMaterial'+str(user_id))
		mat.setDiffuse(VR.view_user_colors[user_id])
		
		cursor_left_open.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_left_closed.setFrom(0, 0, 0)
		cursor_left_closed.setVisible(False)
		cursor_left_closed.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_container_left.addChild(cursor_left_open)
		cursor_container_left.addChild(cursor_left_closed)
		VR.cam.addChild(cursor_container_left)
		cursor_container_right = VR.Transform('Cursor_Container_Right')
		cursor_container_right.addTag(str([user_id, False]))
		cursor_container_right.setFrom(1.5, 0, self.CURSOR_DIST)		
		cursor_right_open.setFrom(0, 0, 0)
		cursor_right_open.setVisible(True)
		cursor_right_open.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_right_closed.setFrom(0, 0, 0)
		cursor_right_closed.setVisible(False)
		cursor_right_closed.getChildren()[0].getChildren()[0].setMaterial(mat)
		cursor_container_right.addChild(cursor_right_open)
		cursor_container_right.addChild(cursor_right_closed)
		VR.cam.addChild(cursor_container_right)
		
		VR.view_user_cursors[user_id] = {}
		mydev_l = VR.Device('mydev')
		mydev_l.setBeacon(cursor_container_left)
		mydev_l.addIntersection(self.edit_node)
		mydev_l.addIntersection(self.meta_plane)
		mydev_l.addIntersection(self.start_page_plane)
		mydev_l.addIntersection(VR.view_root)
		mydev_r = VR.Device('mydev')
		mydev_r.setBeacon(cursor_container_right)
		#print "cursor container right", mydev_r.getBeacon().getChildren()
		#print "cursor container left", mydev_l.getBeacon().getChildren()
		mydev_r.addIntersection(self.edit_node)
		mydev_r.addIntersection(self.meta_plane)
		mydev_r.addIntersection(self.start_page_plane)
		mydev_r.addIntersection(VR.view_root)
		self.edit_site.addMouse(mydev_l, self.edit_plane, 0, 2, 3, 4)
		self.edit_site.addMouse(mydev_r, self.edit_plane, 0, 2, 3, 4)
		self.meta_site.addMouse(mydev_l, self.meta_plane, 0, 2, 3, 4)
		self.meta_site.addMouse(mydev_r, self.meta_plane, 0, 2, 3, 4)
		self.layer_add_site.addMouse(mydev_l, self.layer_add_plane, 0, 2, 3, 4)
		self.layer_add_site.addMouse(mydev_r, self.layer_add_plane, 0, 2, 3, 4)
		self.behavior_add_site.addMouse(mydev_l, self.behavior_add_plane, 0, 2, 3, 4)
		self.behavior_add_site.addMouse(mydev_r, self.behavior_add_plane, 0, 2, 3, 4)
		self.start_page_site.addMouse(mydev_l, self.start_page_plane, 0, 2, 3, 4)
		self.start_page_site.addMouse(mydev_r, self.start_page_plane, 0, 2, 3, 4)
		VR.view_user_cursors[user_id][True] = mydev_l
		VR.view_user_cursors[user_id][False] = mydev_r
		VR.view_user_positions[user_id] = {}
		VR.view_user_positions[user_id][True] = [0, 0, 0]
		VR.view_user_positions[user_id][False] = [0, 0, 0]
		self.log.info('VIEW: init new user done')

	def move_cursor(self, pos_ws, user_id, is_left):
		"""
		This function moves a cursor of a user to a  new position.

		@param float[] pos_ws : The new position to set.
		@param int user_id : The user id of the user.
		@param bool is_left : Indication if cursor is the left or right one of the given user.
		@return  : None
		"""
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
		"""
		This function moves the camera to create a shifting effect of the entire scene.

		@param float[] translation : The x- and y-translation by which the scene should be moved.
		@return  : None
		"""
		self.log.info('VIEW: move_scene')
		cam_pos = VR.cam.getFrom()
		assert len(cam_pos) == 3
		assert len(translation) == 2
		new_cam_pos = [cam_pos[0] + translation[0] * self.MOVE_STEP, cam_pos[1] + translation[1] * self.MOVE_STEP, cam_pos[2]]
		VR.cam.setFrom(new_cam_pos)

	def set_highlight(self, obj, highlight):
		"""
		This function sets a highlight effect to the given object.

		@param object obj : The object which should be highlighted.
		@param bool highlight : Indication if the given object should be highlighted or not.
		@return bool : Indication of success of the highlight action.
		"""
		self.log.info('VIEW: set_highlight')

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
		"""
		This function creates the params for the URL for passing data to the meta menu bar.

		@param object obj : The object to create a URL for.
		@return str : The parmas for the meta menu bar URL.
		"""
		self.log.info('VIEW: create_url_params_from_metacontent')
		
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
		self.log.info('VIEW: parameter website {}'.format(params))
		return params

	def highlight_pos(self, pos):  # returns the added highlight
		"""
		This function highlights a position on the scene.

		@param float[] pos : The position that should be highlighted.
		@return object : The added highlight object.
		"""
		self.log.info('VIEW: highlight_pos')
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

	def remove_highlight_point(self, highlight_point):
		"""
		This function removes a given highlight object from the scene.

		@param object highlight_point : The highlight object to remove.
		@return  : None
		"""
		self.log.info('VIEW: remove_highlight_pos')
		if isinstance(highlight_point, VR.Object):
			highlight_point.destroy()

	def trigger_down(self, user_id, is_left):
		"""
		This function simulates a trigger down on the current position of the given cursor.

		@param int user_id : The user id of the user.
		@param bool is_left : Indication which cursor of the given user to trigger.
		@return  : None
		"""
		self.log.warning('trigger_down({}, {})'.format(user_id, is_left))
		mydev = VR.view_user_cursors[user_id][is_left]
		assert mydev is not None, 'user {} has no VR device (is_left={})'.format(user_id, is_left)
		mydev.trigger(0, 1)

	def trigger_up(self, user_id, is_left):
		"""
		This function simulates a trigger up on the current position of the given cursor.

		@param int user_id : The user id of the user.
		@param bool is_left : Indication which cursor of the given user to trigger.
		@return  : None
		"""
		self.log.warning('trigger_up({}, {})'.format(user_id, is_left))
		mydev = VR.view_user_cursors[user_id][is_left]
		assert mydev is not None, 'user {} has no VR device (is_left={})'.format(user_id, is_left)
		mydev.trigger(0, 0)

	def release(self, user_id, is_left):
		"""
		This function simulates a release on the current position of the given cursor.

		@param int user_id : The user id of the user.
		@param bool is_left : Indication which cursor of the given user to release.
		@return  : None
		"""
		mydev = VR.view_user_cursors[user_id][is_left]
		beacon_children = mydev.getBeacon().getChildren()
		assert len(beacon_children) > 1, "Beacon must have at least two children"
		beacon_children[0].setVisible(True)
		beacon_children[1].setVisible(False)

	def press(self, user_id, is_left):
		"""
		This function simulates a press down on the current position of the given cursor.

		@param int user_id : The user id of the user.
		@param bool is_left : Indication which cursor of the given user to press.
		@return  : None
		"""
		mydev = VR.view_user_cursors[user_id][is_left]
		beacon_children = mydev.getBeacon().getChildren()
		assert len(beacon_children) > 1, "Beacon must have at least two children"
		beacon_children[0].setVisible(False)
		beacon_children[1].setVisible(True)

	def get_object(self, user_id, is_left):
		"""
		This function returns the intersected object of the given cursor.

		@param int user_id : The user id of the user.
		@param bool is_left : Indication which cursor of the given user to to intersect.
		@return object : The intersected object.
		"""
		self.log.info('VIEW: get_object')
		mydev = VR.view_user_cursors[user_id][is_left]
		if mydev.intersect():
			i = mydev.getIntersected()
			tags = i.getTags()
			self.log.info( 'View tags: {} name: {} id {} {}'.format(tags, i.getName(), i.getID(), i))
			if i.hasTag('edit'):
				self.log.info('View: edit')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['edit']
			elif i.hasTag('meta'):
				self.log.info('View: meta')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['meta']
			elif i.hasTag('layer_add'):
				self.log.info('View: layer_add')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['layer_add']
			elif i.hasTag('behavior_add'):
				self.log.info('View: behavior_add')
				#mydev.trigger(0, 0)
				#mydev.trigger(0, 1)
				return self.menubar_entries['behavior_add']
			elif i.hasTag('start_page'):
				self.log.info('View: start_page')
				return self.menubar_entries['start_page']
			#elif 'obj' in tags:
			else:
				#print 'view: object'
				
				p = i.getParent().getParent().getParent()
				if p.hasTag('obj'):
					return self.object_dict[p]
				elif i.hasTag('obj'):
					return self.object_dict[i]
				else:
					self.log.info('VIEW: No valid intersected object in get_object')
		else:
			self.log.info('VIEW: No intersection. Empty space clicked.')
		return None

	def rotate(self, degrees):
		self.log.info('VIEW: rotate')
		pass

	def _create_subject(self, pass_sub):
		"""
		This function creates a VR object based on a pass subject.

		@param PASS.Subject : The PASS.Subject to create in the scene.
		@return  : None
		"""
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

		self.object_dict[pass_sub] = subject_node
		self.object_dict[subject_node] = pass_sub
		VR.view_root.addChild(subject_node)

		# create label
		self._create_label_for_object(pass_sub)

	def _create_message(self, pass_mes):
		"""
		This function creates a VR object based on a pass message exchange.

		@param PASS.MessageExchange : The PASS.MessageExchange to create in the scene.
		@return  : None
		"""
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

		self.object_dict[pass_mes] = message_node
		self.object_dict[message_node] = pass_mes
		self.message_dict[message_node] = [self.object_dict[pass_mes.sender], self.object_dict[pass_mes.receiver], None, None, None]
		self._connect(message_node)
		VR.view_root.addChild(message_node)

		# create label
		self._create_label_for_object(pass_mes)

	def _create_external_subject(self, pass_exsub):
		"""
		This function creates a VR object based on a pass external subject.

		@param PASS.ExternalSubject : The PASS.ExternalSubject to create in the scene.
		@return  : None
		"""
		assert isinstance(pass_exsub, PASS.ExternalSubject)
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

		self.object_dict[pass_exsub] = subject_node
		self.object_dict[subject_node] = pass_exsub
		VR.view_root.addChild(subject_node)

		# create label
		self._create_label_for_object(pass_exsub)

	def _create_function_state(self, state):
		"""
		This function creates a VR object based on a pass function state.

		@param PASS.State : The PASS.State to create in the scene.
		@return  : None
		"""
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

		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

		# create label
		self._create_label_for_object(state)

	def _create_send_state(self, state):
		"""
		This function creates a VR object based on a pass send sate.

		@param PASS.State : The PASS.State to create in the scene.
		@return  : None
		"""
		assert isinstance(state, PASS.State)
		self.elements.append(state)
		pos = state.hasAbstractVisualRepresentation.hasPoint2D
		state_node = VR.Transform('State_Container')
		state_node.addTag('send_state')
		state_node.addTag('obj')
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

		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

		# create label
		self._create_label_for_object(state)

	def _create_receive_state(self, state):
		"""
		This function creates a VR object based on a pass receive state.

		@param PASS.State : The PASS.State to create in the scene.
		@return  : None
		"""
		assert isinstance(state, PASS.State)
		self.elements.append(state)
		pos = state.hasAbstractVisualRepresentation.hasPoint2D
		state_node = VR.Transform('State_Container')
		state_node.addTag('receive_state')
		state_node.addTag('obj')
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

		self.object_dict[state] = state_node
		self.object_dict[state_node] = state
		VR.view_root.addChild(state_node)

		#create label
		self._create_label_for_object(state)

	def _create_transition_edge(self, edge):
		"""
		This function creates a VR object based on a pass transition edge.

		@param PASS.TransitionEdge : The PASS.TransitionEdge to create in the scene.
		@return  : None
		"""
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

		self.object_dict[edge] = transition_node
		self.object_dict[transition_node] = edge
		self.message_dict[transition_node] = [self.object_dict[edge.hasSourceState], self.object_dict[edge.hasTargetState], None, None, None]
		self._connect(transition_node)
		VR.view_root.addChild(transition_node)

		# create label
		self._create_label_for_object(edge)

	def _create_label_for_object(self, pass_obj):
		"""
		This function creates a label based on the pass object.

		@param object pass_obj : The pass object which contains the label information.
		@return  : None
		"""
		assert pass_obj is not None, "_create_label_for_object given pass_obj has not to be None"
		poly_obj = self.object_dict[pass_obj]
		text = ''
		for t in pass_obj.label:
			text = text + t
		split = text.split(' ')
		index_list = []
		for s in split:
			index_list.append(split.index(s) + self.annotation_index)
		self.annotation_dict[pass_obj] = index_list
		#print 'annotation: index_list create', index_list, split
		for i in index_list:
			self.annotation_engine.set(int(i), [poly_obj.getFrom()[0] - (0.455*self.TEXT_SIZE*len(split[index_list.index(int(i))])), poly_obj.getFrom()[1] - ((index_list.index(int(i)) - int(len(index_list) / 2)) * 2 * self.TEXT_SIZE), 10 * self.TEXT_SIZE], split[index_list.index(int(i))])
		self.annotation_index = self.annotation_index + len(index_list)

	def _refresh_label_for_object(self, poly_obj):
		"""
		This function refreshs a label based on the poly object.

		@param object poly_obj : The poly object which was changed.
		@return  : None
		"""
		'''
		if len(pass_obj.label) == 0:
			label_split = ['']
		else:
			label_split = str.split(pass_obj.label[0])
		for l in label_split:
			sprite = VR.Sprite('label')
			sprite.setFrom(self.TEXT_SIZE / 2, label_split.index(l) * 0.5, self.TEXT_SIZE)
			sprite.setSize(0.1 * len(l), 0.1)
			print 'label', l
			sprite.setText(l)
			vr_obj.addChild(sprite)
		'''
		self.log.info('VIEW: _create_label_for_object')
		assert poly_obj is not None, "_create_label_for_object given pass_obj has not to be None"
		pass_obj = self.object_dict[poly_obj]
		text = ''
		for t in pass_obj.label:
			text = text + t
		split = text.split(' ')
		index_list = self.annotation_dict[pass_obj]
		#print 'annotation: index_list before', index_list, split
		if len(index_list) < len(split):
			for i in xrange(0, (len(split) - len(index_list))):
				index_list.append(self.annotation_index + 1)
				self.annotation_index = self.annotation_index +1
		elif len(index_list) > len(split):
			for i in xrange(0, (len(index_list) - len(split))):
				index_list.remove(self.annotation_index + 1)
		self.annotation_dict[pass_obj] = index_list
		#print 'annotation: index_list after', index_list
		for i in index_list:
			self.annotation_engine.set(int(i), [poly_obj.getFrom()[0] - (0.455*self.TEXT_SIZE*len(split[index_list.index(int(i))])), poly_obj.getFrom()[1] - ((index_list.index(int(i)) - int(len(index_list) / 2)) * 2 * self.TEXT_SIZE), 10 * self.TEXT_SIZE], split[index_list.index(int(i))])

	def on_change(self, object, attr):
		"""
		This function processes all changes to a object in the current scene.

		@param object object : The object which changed.
		@param str attr : The attribute of the object which changed.
		@return  : None
		"""
		self.log.info('VIEW: on_change: obj: {} attr: {}'.format(object, attr))
		if isinstance(self.cur_scene, PASS.Layer) and (isinstance(object, PASS.Layer) or isinstance(object, PASS.Subject) \
				or isinstance(object, PASS.ExternalSubject) or isinstance(object, PASS.MessageExchange)):
			if not isinstance(object, PASS.Layer) and not object in self.object_dict:  # create new layer object
				if isinstance(object, PASS.Subject):
					self._create_subject(object)
				elif isinstance(object, PASS.MessageExchange):
					self._create_message(object)
				elif isinstance(object, PASS.ExternalSubject):
					self._create_external_subject(object)
			elif isinstance(object, PASS.Layer):  # delete element
				self.log.info('VIEW: onchange layer')
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
								# delete annotation engine entry/ set text to ''
								ae_idx_list = self.annotation_dict[self.object_dict[poly_mes]]
								for ae_idx in ae_idx_list:
									self.annotation_engine.set(int(ae_idx), [0, 0, 0], '')
								paths_to_delete = self.message_dict[poly_mes][2]
								for p in paths_to_delete:
									VR.ptool.remPath(p)
								del self.object_dict[mes]
								del self.object_dict[poly_mes]
								del self.message_dict[poly_mes]
								self.elements.remove[mes]
								poly_mes.destroy()
							poly_obj = self.object_dict[element_to_delete[0]]
							# delete annotation engine entry/ set text to ''
							ae_idx_list = self.annotation_dict[element_to_delete[0]]
							for ae_idx in ae_idx_list:
								self.annotation_engine.set(int(ae_idx), [0, 0, 0], '')
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							self.elements.remove(element_to_delete[0])
							poly_obj.destroy()
						elif isinstance(element_to_delete[0], PASS.MessageExchange):
							poly_obj = self.object_dict[element_to_delete[0]]
							# delete annotation engine entry/ set text to ''
							ae_idx_list = self.annotation_dict[element_to_delete[0]]
							for ae_idx in ae_idx_list:
								self.annotation_engine.set(int(ae_idx), [0, 0, 0], '')
							paths_to_delete = self.message_dict[poly_obj][2]
							for p in paths_to_delete:
								VR.ptool.remPath(p)
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							del self.message_dict[poly_obj]
							self.elements.remove(element_to_delete[0])
							poly_obj.destroy()
					else:
						self.log.info('VIEW: Skip, Element added.')
			else:
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				poly_obj = self.object_dict[object]
				if attr == 'hasAbstractVisualRepresentation':  # position changed
					self.log.debug("moving subject to {}, {}, {}".format(pos.hasXValue, pos.hasYValue, 0.0))
					poly_obj.setFrom(pos.hasXValue, pos.hasYValue, 0)
					self._refresh_label_for_object(poly_obj)
				elif attr == 'label':  # name changed
					self._refresh_label_for_object(poly_obj)
				elif attr == 'hasMetaContent':  # meta data changed
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
					self.log.info('VIEW: Invalid attribute in on_change')

		elif isinstance(self.cur_scene, PASS.Behavior) and (isinstance(object, PASS.Behavior) or isinstance(object, PASS.State) or isinstance(object, PASS.TransitionEdge)):
			if not isinstance(object, PASS.Behavior) and not object in self.object_dict:  # create new layer object
				if isinstance(object, PASS.SendState):
					self._create_send_state(object)
				elif isinstance(object, PASS.FunctionState):
					self._create_function_state(object)
				elif isinstance(object, PASS.ReceiveState):
					self._create_receive_state(object)
				elif isinstance(object, PASS.TransitionEdge):
					self._create_transition_edge(object)
			elif isinstance(object, PASS.Behavior):  # delete State or TransitionEdge
				self.log.info('VIEW: onchange behavior')
				if attr == "hasEdge" or attr == "hasState":
					list_of_elements = object.hasEdge + object.hasState
					print 'list of elements for filter', list_of_elements
					list_of_elements = [x for x in list_of_elements if isinstance(x, PASS.State) or isinstance(x, PASS.TransitionEdge)]
					element_to_delete = set(self.elements) - set(list_of_elements)
					element_to_delete = list(element_to_delete)
					assert len(element_to_delete) < 2, "More than one element to delete"
					if len(element_to_delete) == 1:
						if isinstance(element_to_delete[0], PASS.TransitionEdge) or isinstance(element_to_delete[0], PASS.State):							
							poly_obj = self.object_dict[element_to_delete[0]]
							# delete annotation engine entry/ set text to ''
							ae_idx_list = self.annotation_dict[element_to_delete[0]]
							for ae_idx in ae_idx_list:
								self.annotation_engine.set(int(ae_idx), [0, 0, 0], '')
							if isinstance(element_to_delete[0], PASS.TransitionEdge):
								paths_to_delete = self.message_dict[poly_obj][2]
								for p in paths_to_delete:
									VR.ptool.remPath(p)
							del self.object_dict[poly_obj]
							del self.object_dict[element_to_delete[0]]
							self.elements.remove(element_to_delete[0])
							poly_obj.destroy()
					else:
						self.log.info('VIEW: Skip, Element added.')
			else:
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				poly_obj = self.object_dict[object]
				if attr == 'hasAbstractVisualRepresentation':  # position changed
					self.log.debug("moving subject to {}, {}, {}".format(pos.hasXValue, pos.hasYValue, 0.0))
					poly_obj.setFrom(pos.hasXValue, pos.hasYValue, 0)
					self._refresh_label_for_object(poly_obj)
				elif attr == 'label':  # name changed
					self._refresh_label_for_object(poly_obj)
				elif attr == 'hasMetaContent':  # meta data changed
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
					self.log.info('VIEW: Invalid attribute in on_change')
		elif isinstance(self.cur_scene, PASS.Layer) or isinstance(self.cur_scene, PASS.Behavior):
			self.log.info("Ignoring weird on_change object: {}".format(object))
		else:
			self.log.warning('VIEW ERROR: self.cur_scene must be of type Layer or Behavior but is: {}'.format(self.cur_scene))

	def _get_attached_message(self, subject):
		"""
		This function returns the attached message exchange of a subject.

		@param object subject : The subject to which the attached messsage exchangewill be returned.
		@return object : The attached message exchange of the given subject.
		"""
		self.log.info('VIEW: object {}'.format(subject))
		poly_sub = self.object_dict[subject]
		for i in self.message_dict:
			if self.message_dict[i][0] is poly_sub or self.message_dict[i][1] is poly_sub:
				self.log.info('VIEW: attached message {}'.format(i))
				return i
		return None

	def _connect(self, message):
		"""
		This function adds paths between the objects belonging to the given message.

		@param object message : The object in the middle of the path to create.
		@return  : None
		"""
		self.log.info('VIEW: connect({})'.format(message))
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
		"""
		This function displayes a direkt path between the left and right cursor of a given user.

		@param int user_id : The user id of the given user.
		@param bool set_line : Indication if the line should be set or not.
		@return  : None
		"""
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
				self.log.info('VIEW: delete')
				VR.ptool.remPath(self.new_message_path)
				self.new_message_path = None
			else:
				self.log.info("Warning: no message path to be deleted...")

	def local_to_world_2d(self, local_pos):
		"""
		This function translates 2D local positions into world coordinates.

		@param float[] local_pos : The 2D local position to translate.
		@return float[] : The calculated world position.
		"""
		#transformation
		assert len(local_pos) == 2, "local_pos must have a length of 2"
		return [(local_pos[0] - 0.5) * self.scale_x + VR.cam.getFrom()[0], (local_pos[1] - 0.5) * self.scale_y + VR.cam.getFrom()[1]]

	def show_init_screen(self, init_list):
		"""
		This function shows the initial start screen.

		@param InitScreenEntry[] init_list : List of InitScreenEntries to show on the start screen.
		@return  : None
		"""
		self.log.info("show_init_screen({})".format(init_list))
		params = ''
		for i in init_list:
			assert isinstance(i, self.InitScreenEntry)
			params = params + str(i.display_name) + '=' + str(i.image_file_name) + '=' + str(i.model_id)
			if(init_list.index(i) != len(init_list) - 1):
				params = params + '&'

		self.log.info('VIEW: parameter website {}'.format(params))
		self.start_page_site.open('http://localhost:5500/start' + '?' + params)
		self.start_page_plane.setVisible(True)
