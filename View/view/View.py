import VR
import math
import PASS
import sys
import logging


class View():

	class MenuBar():
		def __init__(self, name):
			self.name = name

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
		self.VALID_USER_COLORS = []
		#setup valid user colors
		self.VALID_USER_COLORS.append([0.65, 0.09, 0.49])
		self.VALID_USER_COLORS.append([0.81, 0.77, 0.66])
		self.VALID_USER_COLORS.append([0.25, 0.19, 0.47])
		self.VALID_USER_COLORS.append([0.98, 0.98, 0.62])
		self.VALID_USER_COLORS.append([0.85, 0.59, 0.98])

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
		self.HANDLE.setPrimitive('Box 0.001 0.001 0.001 1 1 1')
		self.HANDLE.setMaterial(VR.Material('sample material'))

		self.PLANE_SIZE = 0.4

		#TODO add path for missing elements

		self.menubar_entries = {
			'edit': self.MenuBar('edit'),
			'meta': self.MenuBar('meta'),
			'layer_add': self.MenuBar('layer_add'),
			'behavior_add': self.MenuBar('behavior_add')
		}

		#stores polyVR objects and related PASS objects and vise versa
		self.object_dict = {}
		self.message_dict = {}  # key: poly_mess, 1. entry: poly_sender, 2. entry: poly_receiver, 3. entry: path
		self.annotation_dict = {}  # key: object, 1. entry: list(index)

		#stores user_id and corresponding color
		self.user_colors = {}

		#setup camera parameter
		self.camera_from = [0, 0, 10]
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

		#setup annotation engine
		self.annotation_index = 0
		self.annotation_engine = VR.AnnotationEngine('ae')
		self.annotation_engine.setColor([0, 1, 0, 1])
		self.annotation_engine.setPickable(False)
		#self.annotation_engine.setBackground([1,0,0,0.5])
		self.annotation_engine.setSize(0.2)
		self.annotation_engine.setScale([1, 1, 1])
		VR.view_root.addChild(self.annotation_engine)
		
		#setup pathtool
		VR.ptool = VR.Pathtool()
		VR.ptool.setHandleGeometry(self.HANDLE)

		#setup offsets
		#screen
		self.win_size = VR.getSetup().getWindow('screen').getSize()
		assert len(self.win_size) == 2
		self.scale_y = 2 * self.camera_from[2] * math.tan(self.camera_fov * 0.5)
		self.scale_x = self.scale_y * self.win_size[0] / self.win_size[1]
		self.scale_cursor_y = 2 * abs(self.CURSOR_DIST) * math.tan(self.camera_fov * 0.5)
		self.scale_cursor_x = self.scale_cursor_y * self.win_size[0] / self.win_size[1]
		self.scale_plane_y = 2 * 11 * math.tan(self.camera_fov * 0.5)
		self.scale_plane_x = self.scale_plane_y  * self.win_size[0] / self.win_size[1]
		#model
		self.model_offset_x = 0
		self.model_offset_y = 0
		self.model_width = 0
		self.model_hight = 0

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
		self.start_page_site.setAspectRatio(2)

		self.start_page_plane.setVisible(True)
		self.start_page_site.setMaterial(self.behavior_add_plane.getMaterial())
		self.start_page_site.open('http://localhost:5500/behaviorAdd')
		self.start_page_site.setResolution(512)
		self.start_page_site.setAspectRatio(4)

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
		self.layer_add_site.setResolution(512)
		self.layer_add_site.setAspectRatio(4)

		self.layer_add_plane.setVisible(False)
		self.edit_node.addChild(self.layer_add_plane)

		#setup menu bar behaviorAdd
		self.behavior_add_plane = VR.Geometry('behaviorAdd')
		s = 'Plane '
		s += str(self.scale_x - (self.scale_x / 4))
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
		s += str(self.scale_x - (self.scale_x / 4))
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
		VR.cam.setFrom(self.camera_from)

		# hide start view
		self.start_page_plane.setVisible(False)
		# show menus
		self.meta_plane.setVisible(True)
		self.navigation_plane.setVisible(True)
		for c in self.edit_node.getChildren():
			c.setVisible(False)
		if isinstance(cur_scene, PASS.Layer):
			self.edit_node.getChildren()[0].setVisible(True)
		elif isinstance(cur_scene, PASS.Behavior):  # is instance of Pass.Behavior
			self.edit_node.getChildren()[1].setVisible(True)
		else:
			print 'set_cur_scene neither layer nor behavior'

		#set offsets
		print 'bb: ', self.cur_scene.getBoundingBox2D()
		self.model_offset_x = self.cur_scene.getBoundingBox2D()[0][0]
		self.model_offset_y = self.cur_scene.getBoundingBox2D()[0][1]
		self.model_width = self.cur_scene.getBoundingBox2D()[1][0] - self.model_offset_x
		self.model_hight = self.cur_scene.getBoundingBox2D()[1][1] - self.model_offset_y
		print 'x min ', self.model_offset_x
		print 'y min ', self.model_offset_y
		print 'x dist ', self.model_width
		print 'y dist ', self.model_hight

		#VR.cam.addChild(self.active_gui_element) #TODO
		self.update_all()
		VR.cam.setFrom(self.camera_from[0], self.camera_from[1], self.camera_from[2] + 10)

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
		VR.ptool = VR.Pathtool()
		VR.ptool.setHandleGeometry(self.HANDLE)

		#todo sizes
		if isinstance(self.cur_scene, PASS.Layer):
			subjects = self.cur_scene.subjects
			message_exchanges = self.cur_scene.messageExchanges
			external_subjects = self.cur_scene.externalSubjects

			for subject in subjects:
				assert isinstance(subject, PASS.Subject)
				pos = subject.hasAbstractVisualRepresentation.hasPoint2D
				assert pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width, '{} is not in x bounding range'.format(pos.hasXValue)
				assert pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight, '{} is not in y bounding range'.format(pos.hasYValue)
				subject_node = VR.Transform('Subject_Container')
				subject_node.addTag('obj')
				subject_node.addTag('subject')
				subject_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
					((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
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
					poly_sub.setScale(0.1, 0.1, 0.1)
					poly_sub.setVisible(False)
					subject_node.addChild(poly_sub)
				if len(subject.hasMetaContent) == 0:
					subject_node.getChildren()[0].setVisible(True)
				else:
					subject_node.getChildren()[1].setVisible(True)
				self.object_dict[subject] = subject_node
				self.object_dict[subject_node] = subject
				VR.view_root.addChild(subject_node)
				self.create_annotation_engine(subject)

			for message in message_exchanges:
				assert isinstance(message, PASS.MessageExchange)
				pos = message.hasAbstractVisualRepresentation.hasPoint2D
				#assert pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width, '{} is not in x bounding range'.format(pos.hasXValue)
				#assert pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight, '{} is not in y bounding range'.format(pos.hasYValue)
				message_node = VR.Transform('Message_Container')
				message_node.addTag('obj')
				message_node.addTag('message')
				message_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
					((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
#				message_node.setPlaneConstraints([0, 0, 1])
#				message_node.setRotationConstraints([1, 1, 1])
				poly_mesages = []
				poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message']))
				poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta']))
				poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_highlight']))
				poly_mesages.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta_highlight']))
				for poly_mes in poly_mesages:
					poly_mes.setPickable(True)
					poly_mes.setScale(0.1, 0.1, 0.1)
					poly_mes.setVisible(False)
					poly_mes.setUp(0, 0, 1)
					poly_mes.rotate(90, 0, 0, 0)
					message_node.addChild(poly_mes)
				if len(message.hasMetaContent) == 0:
					message_node.getChildren()[0].setVisible(True)
				else:
					message_node.getChildren()[1].setVisible(True)
				self.object_dict[message] = message_node
				self.object_dict[message_node] = message
				self.message_dict[message_node] = [self.object_dict[message.sender], self.object_dict[message.receiver], None]				
				self.create_annotation_engine(message)
				self.connect(message_node)
				VR.view_root.addChild(message_node)

			for subject in external_subjects:
				pos = subject.hasAbstractVisualRepresentation.hasPoint2D
				assert pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width, '{} is not in x bounding range'.format(pos.hasXValue)
				assert pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight, '{} is not in y bounding range'.format(pos.hasYValue)
				subject_node = VR.Transform('External_Subject_Container')
				subject_node.addTag('obj')
				subject_node.addTag('external_subject')
				subject_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
					((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
				subject_node.setPlaneConstraints([0, 0, 1])
				subject_node.setRotationConstraints([1, 1, 1])
				poly_subjects = []
				poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject']))
				poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta']))
				poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_highlight']))
				poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta_highlight']))
				for poly_sub in poly_subjects:
					poly_sub.setPickable(True)
					poly_sub.setScale(0.1, 0.1, 0.1)
					poly_sub.setVisible(False)
					subject_node.addChild(poly_sub)
				if len(subject.hasMetaContent) == 0:
					subject_node.getChildren()[0].setVisible(True)
				else:
					subject_node.getChildren()[1].setVisible(True)
				self.object_dict[subject] = subject_node
				self.object_dict[subject_node] = subject				
				VR.view_root.addChild(subject_node)
				self.create_annotation_engine(subject)

		elif isinstance(self.cur_scene, PASS.Behavior):
			states = self.cur_scene.hasState
			edges = self.cur_scene.hasEdge

			for state in states:
				assert isinstance(state, PASS.State)
				pos = state.hasAbstractVisualRepresentation.hasPoint2D
				assert pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width, '{} is not in x bounding range'.format(pos.hasXValue)
				assert pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight, '{} is not in y bounding range'.format(pos.hasYValue)
				state_node = VR.Transform('State_Container')
				state_node.addTag('obj')
				if isinstance(state, PASS.FunctionState):
					state_node.addTag('function_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['function_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['function_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['function_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['function_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(state.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					self.object_dict[state] = state_node
					self.object_dict[state_node] = state
					self.create_annotation_engine(state)
					VR.view_root.addChild(state_node)
				elif isinstance(state, PASS.SendState):
					state_node.addTag('send_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['send_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['send_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['send_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['send_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(state.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					self.object_dict[state] = state_node
					self.object_dict[state_node] = state
					self.create_annotation_engine(state)
					state_node.addChild(ae)
					VR.view_root.addChild(state_node)
				elif isinstance(state, PASS.ReceiveState):
					state_node.addTag('receive_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['receive_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['receive_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['receive_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['receive_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(state.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					self.object_dict[state] = state_node
					self.object_dict[state_node] = state
					self.create_annotation_engine(state)
					VR.view_root.addChild(state_node)

			for edge in edges:
				assert isinstance(message, PASS.MessageExchange)
				pos = edge.hasAbstractVisualRepresentation.hasPoint2D
				assert pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width, '{} is not in x bounding range'.format(pos.hasXValue)
				assert pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight, '{} is not in y bounding range'.format(pos.hasYValue)
				transition_node = VR.Transform('Transition_Container')
				transition_node.addTag('obj')
				transition_node.addTag('transition')
				transition_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
					((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
				transition_node.setPlaneConstraints([0, 0, 1])
				transition_node.setRotationConstraints([1, 1, 1])
				poly_trans = []
				poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition']))
				poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta']))
				poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_highlight']))
				poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta_highlight']))
				for poly_mes in poly_trans:
					poly_mes.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5),  # * self.scale_x,
								((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5), 0)  # * self.scale_y, 0)
					poly_mes.setPickable(True)
					poly_mes.setScale(0.1, 0.1, 0.1)
					poly_mes.setVisible(False)
					transition_node.addChild(poly_mes)
				if len(edge.hasMetaContent) == 0:
					transition_node.getChildren()[0].setVisible(True)
				else:
					transition_node.getChildren()[1].setVisible(True)
				self.object_dict[message] = transition_node
				self.object_dict[transition_node] = message
				self.message_dict[poly_mes] = [self.object_dict[edge.hasSourceState], self.object_dict[edge.hasTargetState], None]
				#self.connect(transition_node)
				VR.view_root.addChild(transition_node)
				self.create_annotation_engine(edge, 0.02)
		else:
			print 'Failed to load current scene: has to be level or behavior'

	def create_annotation_engine(self, subject):
		# text label
		assert subject is not None, "create_annotation_engine given subject has not to be None"
		text = ''
		for t in subject.label:
			text = text + t
		split = text.split(' ')
		print 'split', split
		index_list = []
		for s in split:
			index_list.append(split.index(s) + self.annotation_index)
		print 'indexlist', index_list
		self.annotation_dict[subject] = index_list
		for i in index_list:
			#print 'teschd', int(i), split[int(i)- self.annotation_index]
			self.annotation_engine.set(int(i), [self.object_dict[subject].getFrom()[0] - (0.01*len(split[int(i - self.annotation_index)])), self.object_dict[subject].getFrom()[1], self.object_dict[subject].getFrom()[2] + 0.1], split[int(i - self.annotation_index)] + 'test')
		self.annotation_index = self.annotation_index + len(index_list)
	
	def refresh_annotation_engine(self, subject, size):
		# text label
		assert subject is not None, "refresh_annotation_engine given subject has not to be None"
		text = ''
		for t in subject.label:
			text = text + t		
		for c in subject.getChildren():
			if c.hasTag('AnnotationEngine'):
				ae = c
		assert ae is not None, "refresh_annotation_engine given subject has no AnnotationEngine"
		ae.set(1, [-size, 0, 0.1], text)

	def zoom(self, level):
		self.log.info('zoom')
		print(("Zoom level: {}".format(self.current_zoom_level())))
		new_cam_pos = [p + d * self.ZOOM_STEP * level for p, d in zip(VR.cam.getFrom(), VR.cam.getDir())]
		if not new_cam_pos[2] >= self.MAX_DIST and not new_cam_pos[2] <= self.MIN_DIST:
			VR.cam.setFrom(new_cam_pos)

	def current_zoom_level(self):
		self.log.info('current_zoom_level')
		level = int(float(self.MAX_DIST - VR.cam.getFrom()[2]) / self.ZOOM_STEP)
		assert(level >= 0)
		return level

	def move_cursor(self, pos_ws, user_id, is_left):
		self.log.info('move_cursor')

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
			VR.view_user_colors[user_id] = self.VALID_USER_COLORS[len(VR.view_user_cursors)]
			cursor_left = VR.Geometry('dev_l')
			cursor_left.setPrimitive('Sphere 0.008 5')
			cursor_left.setMaterial(VR.Material('sample material'))
			cursor_left.setFrom(0.3, 0, self.CURSOR_DIST)
			cursor_left.addTag(str([user_id, True]))
			cursor_left.setColors([VR.view_user_colors[user_id]])
			VR.cam.addChild(cursor_left)
			cursor_right = VR.Geometry('dev_r')
			cursor_right.setPrimitive('Sphere 0.008 5')
			cursor_right.setMaterial(VR.Material('sample material'))
			cursor_right.setFrom(1.5, 0, self.CURSOR_DIST)
			cursor_right.addTag(str([user_id, False]))
			cursor_right.setColors([VR.view_user_colors[user_id]])
			VR.cam.addChild(cursor_right)
			VR.view_user_cursors[user_id] = {}
			mydev_l = VR.Device('mydev')
			mydev_l.setBeacon(cursor_left)
			mydev_l.addIntersection(self.edit_node)
			mydev_l.addIntersection(self.meta_plane)
			mydev_l.addIntersection(VR.view_root)
			mydev_r = VR.Device('mydev')
			mydev_r.setBeacon(cursor_right)
			mydev_r.addIntersection(self.edit_node)
			mydev_r.addIntersection(self.meta_plane)
			mydev_r.addIntersection(VR.view_root)
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
			#params = self.create_url_params_from_metacontent(obj)
			#self.meta_site.open('http://localhost:5500/meta' + '?' + params)

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
				print 'ERROR (view): Current scene neither of type Layer nor Behavior'

			#set metaContent on gui element meta to parent
			#params = self.create_url_params_from_metacontent(self.cur_scene)
			#self.meta_site.open('http://localhost:5500/meta' + '?' + params)

			if children[2].isVisible() is True:
				children[2].setVisible(False)
				children[0].setVisible(True)
				return True
			elif children[3].isVisible() is True:
				children[3].setVisible(False)
				children[1].setVisible(True)
				return True
		return False

	def create_url_params_from_metacontent(self, obj):
		self.log.info('create_url_params_from_metacontent')
		#o = self.object_dict[obj]
		#assert isinstance(o, VR.Object)

		label = ''
		for l in obj.label:
			label = label + l
		params = 'label=' + str(label) + '&'
		metaKeys = obj.getMetaKeys()
		i = 0
		while i < len(metaKeys):
			print obj.getMetaContent(metaKeys[i])
			#params = params + 'k' + str(i) + '=' + str(metaKeys[i]) + '&' + 'v' + str(i) + '=' + str(o.getMetaContent(metaKeys[i]))
			params = params + str(metaKeys[i]) + '=' + str(obj.getMetaContent(metaKeys[i]))
			if(i != len(metaKeys)):
				params = params + '&'

		return params

	def highlight_pos(self, pos):  # returns the added highlight
		self.log.info('highlight_pos')
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

	def remove_highlight_point(self, highlight_point):  # remove the given highlighted object from scene
		self.log.info('remove_highlight_pos')
		VR.view_root.remChild(highlight_pos)

	def get_object(self, user_id, is_left):
		self.log.info('get_object')
		mydev = VR.view_user_cursors[user_id][is_left]
		if mydev.intersect():
			i = mydev.getIntersected()
			#tags = i.getTags()
			#print 'View tags: ', tags, 'name: ', i.getName(), 'id:', i.getID(), i
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
				#print 'view: object'
				p = i.getParent().getParent().getParent()
				if p.hasTag('obj'):
					#print 'Object found', p
					return self.object_dict[p]
				elif i.hasTag('obj'):
					#print 'Object found', i
					return self.object_dict[i]
				else:
					print 'No valid intersected object in get_object'
		else:
			print 'No intersection. Empty space clicked.'
		return None

	def rotate(self, degrees):
		self.log.info('rotate')
		pass

	def on_change(self, object, attr):
		self.log.info('on_change')
		if isinstance(self.cur_scene, PASS.Layer):
			if isinstance(object, PASS.Subject):
				print "View on_change: Subject"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new subject
					pos = object.hasAbstractVisualRepresentation.hasPoint2D
					if not pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width:
						return
					if pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight:
						return
					subject_node = VR.Transform('Subject_Container')
					subject_node.addTag('obj')
					subject_node.addTag('subject')
					subject_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
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
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						subject_node.getChildren()[0].setVisible(True)
					else:
						subject_node.getChildren()[1].setVisible(True)
					self.object_dict[object] = subject_node
					self.object_dict[subject_node] = object
					self.create_annotation_engine(object)
					VR.view_root.addChild(subject_node)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					self.log.debug("moving subject to {}, {}, {}".format(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x, ((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0))
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					# name changed
					'''
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					ae = self.create_annotation_engine(object, 0.02)
					ae.addTag('AnnotationEngine')
					poly_obj.addChild(ae)
					'''
			elif isinstance(object, PASS.MessageExchange):
				print "View on_change: MessageExchange"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					pos = object.hasAbstractVisualRepresentation.hasPoint2D
					if not pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width:
						return
					if pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight:
						return
					message_node = VR.Transform('Subject_Container')
					message_node.addTag('obj')
					message_node.addTag('subject')
					message_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					message_node.setPlaneConstraints([0, 0, 1])
					message_node.setRotationConstraints([1, 1, 1])
					poly_subjects = []
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['message']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['message_highlight']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['message_meta_highlight']))
					for poly_sub in poly_subjects:
						poly_sub.setFrom(0, 0, 0)
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						message_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						message_node.getChildren()[0].setVisible(True)
					else:
						message_node.getChildren()[1].setVisible(True)
					self.create_annotation_engine(object)
					self.object_dict[object] = message_node
					self.object_dict[message_node] = object
					self.create_annotation_engine(object)
					VR.view_root.addChild(message_node)
					self.connect(message_node)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x ) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.ExternalSubject):
				print "View on_change: External Message"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					pos = object.hasAbstractVisualRepresentation.hasPoint2D
					if not pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width:
						return
					if pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight:
						return
					subject_node = VR.Transform('External_Subject_Container')
					subject_node.addTag('obj')
					subject_node.addTag('external_subject')
					subject_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					subject_node.setPlaneConstraints([0, 0, 1])
					subject_node.setRotationConstraints([1, 1, 1])
					poly_subjects = []
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_highlight']))
					poly_subjects.append(VR.loadGeometry(self.BLENDER_PATHS['external_subject_meta_highlight']))
					for poly_sub in poly_subjects:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						subject_node.getChildren()[0].setVisible(True)
					else:
						subject_node.getChildren()[1].setVisible(True)
					#set name
					self.create_annotation_engine(object)
					self.object_dict[object] = subject_node
					self.object_dict[subject_node] = object
					ae = self.create_annotation_engine(object)
					VR.view_root.addChild(subject_node)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.Layer):
				self.update_all()
			else:
				pass
		elif isinstance(self.cur_scene, PASS.Behavior):
			if isinstance(object, PASS.SendState):
				print "View on_change: Send State"
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				if not pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width:
					return
				if pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight:
					return
				if not object in self.object_dict:  # create new subject
					state_node = VR.Transform('State_Container')
					state_node.addTag('obj')
					state_node.addTag('send_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['s_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					#set name
					self.create_annotation_engine(object)
					self.object_dict[object] = state_node
					self.object_dict[state_node] = object
					VR.view_root.addChild(state_node)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.ReceiveState):
				print "View on_change: Receive State"
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				if not object in self.object_dict:  # create new subject
					state_node = VR.Transform('State_Container')
					state_node.addTag('obj')
					state_node.addTag('send_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['r_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					#set name
					self.create_annotation_engine(object)
					self.object_dict[object] = state_node
					self.object_dict[state_node] = object
					VR.view_root.addChild(state_node)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.FunctionState):
				print "View on_change: Function State"
				pos = object.hasAbstractVisualRepresentation.hasPoint2D
				if not object in self.object_dict:  # create new subject
					state_node = VR.Transform('State_Container')
					state_node.addTag('obj')
					state_node.addTag('send_state')
					state_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					state_node.setPlaneConstraints([0, 0, 1])
					state_node.setRotationConstraints([1, 1, 1])
					poly_states = []
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_meta']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_highlight']))
					poly_states.append(VR.loadGeometry(self.BLENDER_PATHS['f_state_meta_highlight']))
					for poly_sub in poly_states:
						poly_sub.setPickable(True)
						poly_sub.setScale(0.1, 0.1, 0.1)
						poly_sub.setVisible(False)
						subject_node.addChild(poly_sub)
					if len(object.hasMetaContent) == 0:
						state_node.getChildren()[0].setVisible(True)
					else:
						state_node.getChildren()[1].setVisible(True)
					#set name
					self.create_annotation_engine(object)
					self.object_dict[object] = state_node
					self.object_dict[state_node] = object
					VR.view_root.addChild(state_node)
				else:
					poly_obj = self.object_dict[object]
					#position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.TransitionEdge):
				print "View on_change: Transition Edge"
				pos_x = object.hasAbstractVisualRepresentation.hasPoint2D.hasXValue
				pos_y = object.hasAbstractVisualRepresentation.hasPoint2D.hasYValue
				if not object in self.object_dict:  # create new message
					pos = object.hasAbstractVisualRepresentation.hasPoint2D
					if not pos.hasXValue >= self.model_offset_x and pos.hasXValue <= self.model_offset_x + self.model_width:
						return
					if pos.hasYValue >= self.model_offset_y and pos.hasYValue <= self.model_offset_y + self.model_hight:
						return
					transition_node = VR.Transform('Transition_Container')
					transition_node.addTag('obj')
					transition_node.addTag('transition')
					transition_node.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0)
					transition_node.setPlaneConstraints([0, 0, 1])
					transition_node.setRotationConstraints([1, 1, 1])
					poly_trans = []
					poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition']))
					poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta']))
					poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_highlight']))
					poly_trans.append(VR.loadGeometry(self.BLENDER_PATHS['transition_meta_highlight']))
					for poly_mes in poly_trans:
						poly_mes.setFrom(((pos.hasXValue - self.model_offset_x) / self.model_width - 0.5),  # * self.scale_x,
									((pos.hasYValue - self.model_offset_y) / self.model_hight - 0.5), 0)  # * self.scale_y, 0)
						poly_mes.setPickable(True)
						poly_mes.setScale(0.1, 0.1, 0.1)
						poly_mes.setVisible(False)
						transition_node.addChild(poly_mes)
					if len(object.hasMetaContent) == 0:
						transition_node.getChildren()[0].setVisible(True)
					else:
						transition_node.getChildren()[1].setVisible(True)
					#set name
					self.create_annotation_engine(object)
					self.object_dict[object] = transition_node
					self.object_dict[transition_node] = object
					self.message_dict[poly_mes] = [self.object_dict[object.hasSourceState], self.object_dict[object.hasTargetState], None]
					self.connect(poly_trans)
					VR.view_root.addChild(transition_node)
				else:
					poly_obj = self.object_dict[object]
					# position changed
					poly_obj.setFrom(((pos_x - self.model_offset_x) / self.model_width - 0.5) * self.scale_x,
						((pos_y - self.model_offset_y) / self.model_hight - 0.5) * self.scale_y, 0.0)
					#name changed
					for c in poly_obj.getChildren():
						if c.hasTag('AnnotationEngine'):
							c.destroy()
					self.create_annotation_engine(object)
			elif isinstance(object, PASS.Behavior):
				self.update_all()
			else:
				pass
		else:
			print 'VIEW ERROR: self.cur_scene must be of type Layer or Behavior'

	def connect(self, message):
		self.log.info('connect')
		assert isinstance(message, VR.Transform), "parameter must be of VR.Transform type"
		assert message in self.message_dict, "parameter must be in message_dict"

		s = self.message_dict[message][0]
		r = self.message_dict[message][1]
		assert s is not None and r is not None, "sender and receiver must not be None"
		print 'sender :', self.object_dict[s].label, 'receiver: ', self.object_dict[r].label
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

		print "draw_line: ", s, " => ", r
				
		#set path to sender
		self.paths.append(VR.ptool.newPath(None, VR.view_root))
		handles = VR.ptool.getHandles(self.paths[-1])
		assert len(handles) == 2, "invalid number of handles"
		handles[0].setDir(start_dir[0], start_dir[1], 0.0)
		handles[0].setPickable(False)
		handles[0].setFrom(0, 0, 0)
		s.addChild(handles[0])
		handles[1].setFrom(0, 0, 0)
		handles[1].setPickable(False)
		handles[1].setDir(1.0, 0.0, 0.0)
		message.addChild(handles[1])
		
		#set path to receiver
		self.paths.append(VR.ptool.newPath(None, VR.view_root))
		handles = VR.ptool.getHandles(self.paths[-1])
		assert len(handles) == 2, "invalid number of handles"
		handles[0].setFrom(0, 0, 0)
		handles[0].setPickable(False)
		handles[0].setDir(1.0, 0.0, 0.0)
		message.addChild(handles[0])
		handles[1].setFrom(0, 0, 0)
		handles[1].setDir(end_dir[0], end_dir[1], 0.0)
		handles[1].setPickable(False)
		r.addChild(handles[1])

		VR.ptool.update()

	#def move_object(self, obj, pos_ws):
		#self.log.info('move_object')
		#assert len(pos_ws) == 2
		#o = self.object_dict[obj]
		#assert isinstance(o, VR.Object)
		#o.setFrom((pos_ws[0] - 0.5) * self.scale_x, (pos_ws[1] - 0.5) * self.scale_y, 0.0)

	def set_message_line(self, user_id, set_line):
		print "drawing line"
		if set_line:
			if self.new_message_path is not None:
				return
			print "test"
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
			print 'else'
			if self.new_message_path is not None:
				print 'delete'
				h1 = VR.view_user_cursors[user_id][0].getBeacon().getChildren()[0]
				h2 = VR.view_user_cursors[user_id][1].getBeacon().getChildren()[0]
				print h1,h2
				h1.destroy()
				h2.destroy()
				#VR.ptool.remPath(self.new_message_path)
				self.new_message_path = None
			else:
				print "Warning: no message path to be deleted..."
