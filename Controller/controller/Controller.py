#!/usr/bin/env python2
import math
import sys
import logging
import PASS

from view import View
from hardware_main_config import VRHardware


class Controller:

	def __init__(self):
		#logging.basicConfig(filename='controller.log', level=logging.INFO)
		self.log = logging.getLogger()
		self.log.setLevel(logging.WARNING)
		ch = logging.StreamHandler(sys.stdout)
		ch.setLevel(logging.WARNING)
		#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		ch.setFormatter(formatter)
		self.log.addHandler(ch)

		self.log.info("Starting controller")

		self.MAX_ACTIVE_USERS = 2  # ROFL!!

		# dictionaries of model and view, file path is key
		self.models = {}
		self.current_model = None
		self.view = None

		self.active_users = []

		self.press_position = {}
		self.drag_position = None
		self.release_position = {}

		self.selected_objects = []
		self.pressed_object = None
		self.pressed_menu_bar = None
		self.pressed_menu_bar_item = None
		self.released_object = None
		self.pressed_is_left = False
		self.pressed_user_id = None
		self.point_pos = None
		self.highlighted_pos = None

		self.hw_main = VRHardware(self)

	def _check_active_users(self, user_id):
		if user_id in self.active_users:
			return True
		if user_id not in self.active_users and len(self.active_users) < self.MAX_ACTIVE_USERS:
			self.log.info("Adding new active user with ID {}".format(user_id))
			self.active_users.append(user_id)
			return True
		return False

	def process_menu_bar(self, message):
		assert message is not None, "Message is None"
		if not isinstance(self.pressed_object, View.MenuBar):
			return

		self.log.info("process_menu_bar({})".format(message))
		if self.pressed_object.name == "layer_add":
			if message == "subject":
				if self.point_pos is not None:
					new_obj = self.view.get_cur_scene().addSubject()
					new_obj.hasAbstractVisualRepresentation.setPoint2D(self.point_pos[0], self.point_pos[1])
					self.point_pos = None
				else:
					new_obj = self.view.get_cur_scene().addSubject()
					new_obj.hasAbstractVisualRepresentation.setPoint2D(self.drag_position[0], self.drag_position[1])
				new_obj.label.append("New Subject")
				self.selected_objects.append(new_obj)
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
				self.pressed_object = new_obj
			elif message == "exsubject":
				# TODO: implement
				pass
			elif message == "message":
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
				self.view.set_message_line(self.pressed_user_id, True)
				pass
			#elif message == "delete":
				## only the latest selected subject will be deleted
				#assert self.selected_objects is not None, "Nothing to delete"
				#self.pressed_menu_bar = self.pressed_object
				#self.pressed_menu_bar_item = message
				#latest_obj = self.selected_objects[len(self.selected_objects) - 1]
				#self.view.get_cur_scene().removeActiveComponent(latest_obj, True)
				#self.selected_objects.pop()
			else:
				self.log.warning("invalid mesage: {}".format(message))
		# TODO: implement rest
		elif self.pressed_object.name == "...":
			pass
		else:
			self.log.warning("invalid pressed_object: {}".format(self.pressed_object))

	def process(self):
		self.hw_main.process()

	def press(self, pos, user_id, is_left=False):
		"""This function handles a push or press event

		Press handles user input similar to a pressing a mouse button but not
		releasing it yet, i.e. this function should only be called for pushing
		the button, not for releasing it.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param user_id: the id of the user causing this event
		:type user_id: integer
		:param is_left: Whether or not this event was caused by the left
			hand(default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), \
				"Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), \
			"Left/Right hand parameter must be a boolean value"

		self.log.info(("press({}, {}, {})".format(pos, user_id, is_left)))

		if self.view is not None:
			assert self.current_model is not None
			#obj = self.view.get_object(pos[:2])  # old version
			# TODO: maybe update cursor position with pos
			obj = self.view.get_object(user_id, is_left)
			if obj is not None and self.pressed_user_id is None:
				# CASE: press on existing obj(subject/message/menu bar item)
				self.log.info("press(): got object")
				if isinstance(obj, PASS.Subject):
					# CASE: click on Subject
					self.log.info("press(): got Subject")
					pass
				elif isinstance(obj, PASS.MessageExchange):
					# CASE: click on MessageExchange
					self.log.info("press(): got MessageExchange")
					pass
				elif isinstance(obj, PASS.State):
					# CASE: click on State
					self.log.info("press(): got State")
					pass
				elif isinstance(obj, PASS.TransitionEdge):
					# CASE: click on TransitionEdge
					self.log.info("press(): got TransitionEdge")
					pass
				elif isinstance(obj, View.MenuBar):
					# CASE: should be MenuBar
					self.log.info(("Press on MenuBar: {}".format(obj.name)))
					if obj.name == "layer_add":
						pass
					elif obj.name == "edit":
						# TODO: implement rest
						pass
				else:
					self.log.info("Unknown object returned on press()")

				if obj not in self.selected_objects:
					self.log.debug("Adding new selected object {}".format(obj))
					self.selected_objects.append(obj)
					self.log.debug("Going to hightlight object")
					if not isinstance(obj, View.MenuBar):
						if not self.view.set_highlight(obj, True):
							self.log.warning("view.set_highlight(True) failed")
				if self._check_active_users(user_id):
					self.log.debug("Setting new pressed_object: {}".format(obj))
					self.pressed_object = obj
					self.drag_position = pos
				else:
					self.log.debug("User {} is no active user - do not set pressed_object".format(user_id))

			else:
				# CASE: press on object but already pressed OR press on empty field or empty menu bar
				if obj is not None:
					self.log.debug("Got {} - press on object but already pressed".format(obj))
				else:
					self.log.debug("Got no object - press on empty field or empty menu bar?")
				pass
		self.press_position[user_id] = pos
		self.pressed_is_left = is_left
		self.pressed_user_id = user_id  # TODO: double check

		return None

	def release(self, pos, user_id, is_left=False):
		"""This function handles a release event

		Release handles user input similar to a releasing a mouse button after
		pushing it, i.e. this function should only be called for releasing the
		button, not for pushing it.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param user_id: the id of the user causing this event
		:type user_id: integer
		:param is_left: Whether or not this event was caused by the left
			hand (default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), \
				"Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), \
			"User ID must be an integer"
		assert isinstance(is_left, bool), \
			"Left/Right hand parameter must be a boolean value"

		self.log.info(("release({}, {}, {})".format(pos, user_id, is_left)))

		if self.view is not None:
			assert self.current_model is not None
			if self.pressed_object is not None \
				and self.pressed_is_left == is_left \
				and self.pressed_user_id == user_id:
				# CASE: some object was released -> drag or select?
				assert self.pressed_object in self.selected_objects
				self.released_object = self.pressed_object
				self.pressed_object = None
				if isinstance(self.pressed_menu_bar, View.MenuBar):
					# CASE: menu bar item was released on field
					new_obj = None
					#if isinstance(self.released_object, PASS.Subject):
					if self.pressed_menu_bar_item == "subject":
						assert isinstance(self.released_object, PASS.Subject), "Inconsistency between pressed_menu_bar_item and released_object"
						# CASE: add subject was released on field
						if not self.view.set_highlight(self.released_object, True):
							self.log.warning("view.set_highlight(False) failed")
						# TODO: start edit mode
					#elif isinstance(self.released_object, PASS.ExternalSubject):
					elif self.pressed_menu_bar_item == "exsubject":
						assert isinstance(self.released_object, PASS.ExternalSubject), "Inconsistency between pressed_menu_bar_item and released_object"
						# CASE: add external subject was released on field
						if not self.view.set_highlight(self.released_object, True):
							self.log.warning("view.set_highlight(False) failed")
						# TODO: start edit mode
					elif self.pressed_menu_bar_item == "message":
						assert isinstance(self.released_object, View.MenuBar), "Inconsistency between pressed_menu_bar_item and released_object"
						# CASE: add message was released on field
						lo = self.view.get_object(user_id, True)
						ro = self.view.get_object(user_id, False)
						if isinstance(lo, PASS.Subject) and isinstance(ro, PASS.Subject):
							# CASE: adding message only possible if two subjects are selected
							new_obj = self.view.get_cur_scene().addMessageExchange(lo, ro)
							x1 = lo.hasAbstractVisualRepresentation.hasPos2D.hasXValue
							y1 = lo.hasAbstractVisualRepresentation.hasPos2D.hasYValue
							x2 = ro.hasAbstractVisualRepresentation.hasPos2D.hasXValue
							y2 = ro.hasAbstractVisualRepresentation.hasPos2D.hasYValue
							new_obj.hasAbstractVisualRepresentation.setPos2D([x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2])
							new_obj.label.append("New Message")
						else:
							self.log.info("User {} trying to create message on invalid targets".format(user_id))
						self.view.set_message_line(user_id, False)
					else:
						self.log.warning("Invalid MenuBar type")
					self.selected_objects.remove(self.released_object)
					assert self.released_object not in self.selected_objects
					if new_obj is not None:
						self.selected_objects.append(new_obj)
					self.released_object = new_obj
					self.pressed_menu_bar = None
					self.pressed_menu_bar_item = None
				elif sum([x ** 2 for x in [a - b for a, b in zip(
					self.press_position[user_id], pos)]]) < 10.0:
					# CASE: some field object was selected
					# nothing to do
					pass
				else:
					# CASE: some field object was dragged/moved
					# nothing to do
					pass
			elif self.pressed_object is None and self.pressed_is_left == is_left:
				# CASE: release on field without object -> deselect everything
				for obj in self.selected_objects:
					if not isinstance(obj, View.MenuBar):
						if not self.view.set_highlight(obj, False):
							self.log.warning("view.set_highlight(False) failed")
				self.selected_objects = []
				# TODO: set highlight on empty field (for creating new object from menubar combo-command)
				self.view.remove_highlighted_pos(self.highlighted_pos)
				self.point_pos = pos
				self.highlighted_pos = pos
				self.view.highlight_pos(self.highlighted_pos)
				self.log.info("deselect")
			else:
				self.log.warning("case: x")
		self.release_position[user_id] = pos
		self.pressed_user_id = None

		return None

	def move(self, pos, user_id, is_left=False):
		"""This function handles a move event

		Move handles movement of an input device similar to mouse movement. It should
		be called continuously to update the virtual pointing device, e.g. a mouse
		pointer. Calling this function after press() will be interpreted as dragging.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param user_id: the id of the user causing this event
		:type user_id: integer
		:param is_left: Whether or not this event was caused by the left hand
			(default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), \
				"Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), \
			"Left/Right hand parameter must be a boolean value"

		self.log.debug(("move({}, {}, {})".format(pos, user_id, is_left)))

		if self.view is not None:
			assert self.current_model is not None
			if self.pressed_object is not None and self.pressed_user_id == user_id \
				and self.pressed_is_left == is_left:
				assert self.pressed_object in self.selected_objects
				if not isinstance(self.pressed_object, View.MenuBar):
					assert hasattr(self.pressed_object, "hasAbstractVisualRepresentation")
					self.log.info("Moving object to {}".format(pos))
					bb = self.view.get_cur_scene().getBoundingBox2D()
					assert bb is not None and len(bb) == 2 and len(bb[0]) == 2 and len(bb[1]) == 2, \
						"Invalid bounding box: {}".format(bb)
					pos_norm_2d = [bb[0][0] + pos[0] * (bb[1][0] - bb[0][0]), bb[0][1] + pos[1] * (bb[1][1] - bb[0][1])]
					self.pressed_object.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
					#self.view.move_object(self.pressed_object, pos[:2])
			self.view.move_cursor(pos, user_id, is_left)

		return None

	def zoom(self, level, user_id):
		"""This function handles a zoom event

		This function zooms the view by the giving parameter level, zooms out if -1,
		zooms in if 1, changes s-bpm level if the current level is 0

		:param level: the relative zoom level: -1 zoom out, +1 zoom in
		:type level: integer or float

		:return: None
		"""
		assert isinstance(level, (float, int)), "Level must be a number"
		self.log.info(("zoom({})".format(level)))

		if self.view is not None:
			assert self.current_model is not None
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to zoom".format(user_id))
				return None
			if level < 0:
				if self.view.current_zoom_level() == 0:
					layer = self.view.get_cur_scene()
					if layer is not None:
						parent_layer = self.current_model.getParent(layer, PASS.Layer)
						if parent_layer is not None:
							assert isinstance(parent_layer, PASS.Layer), "Got invalid parent from Model"
							self.view.set_cur_scene(parent_layer)
				else:
					self.view.zoom(-1)
			elif level > 0:
				self.view.zoom(1)
		return None

	def fade_away(self):
		"""This function fades the view away

		This fades the view away in one step (full zoom out) to give an broad
		overview over the entire scene. It should be called if the user wants to
		zoom out from a close up view and directly jump to the lowest zoom level.

		:return: None
		"""
		self.log.info("fade_away()")

		if self.view is not None:
			assert self.current_model is not None
			print(("Controller level: {}".format(self.view.current_zoom_level())))
			i = 1000
			while self.view.current_zoom_level() > 10 and i > 0:
				print(("Controller level: {}".format(self.view.current_zoom_level())))
				self.view.zoom(-10)  # TODO: check if value is okay
				i = i - 1
		return None

	def fade_in(self, pos, user_id, is_left):
		"""This function enters the inner sub-level of the object at the given
		position

		This function enters the inner sub-level of the object at the given
		position.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param user_id: the id of the user causing this event
		:type user_id: integer
		:param is_left: Whether or not this event was caused by the left hand
			(default: false)
		:type is_left: boolean

		:return: None
		"""

		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), \
				"Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), \
			"Left/Right hand parameter must be a boolean value"

		self.log.info(("fade_in({})".format(pos)))

		if self.view is not None:
			assert self.current_model is not None
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to fade_in".format(user_id))
				return None
			obj = self.view.get_object(user_id, is_left)
			if obj is not None and self.pressed_user_id is None:
				assert self.pressed_object is None, "Inconsistent pressed_* variables"
				if isinstance(obj, PASS.Subject):
					self.log.info("fade_in: got subject")
					behavior = obj.hasBehavior
					assert behavior is not None, "Invalid Subject, Behavior is none"
					self.view.set_cur_scene(behavior)
				else:
					self.log.debug("fade_in: invalid object: {}".format(obj))
		return None

	def move_model(self, pos, user_id):
		"""This function moves the entire model or scene

		Moves the entire model or scene regardless of selected objects. This
		function should be called continuously to ensure a smooth animation of
		movement. The position parameter should be a directional vector with a
		length that corresponds to the moved distance. The third value (Z-direction)
		should probably be 0.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param user_id: the id of the user causing this event
		:type user_id: integer

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), \
				"Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"

		self.log.info(("move_model({}, {})".format(pos, user_id)))

		if self.view is not None:
			assert self.current_model is not None
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to move_model".format(user_id))
				return None
			# normalize to [-1,1]
			self.view.move_scene([pos[0] * 2.0 - 1.0, (1 - pos[2]) * 2.0 - 1.0])

		return None

	def rotate(self, degrees):
		"""This function rotates the entire scene for the given number of degrees

		:param degrees: The number of degrees to rotate
		:type degrees: integer or float

		:return: None
		"""
		assert isinstance(degrees, (float, int)), "Degrees must be a number"

		self.log.info(("rotate({})".format(degrees)))
		return None

	def move_head(self, pos, degrees, user_id):
		"""This function updates a user's head position for head tracking

		Updates the given user's head position and rotation. This function should
		be called continuously to ensure smooth movement representation. The
		position parameter should be a directional vector with a length that
		corresponds to the moved distance. The degrees parameter should be a
		relative value in degrees.

		:param pos: the 3D position in normalized screen space coordinates
		:type pos: float array of length 3
		:param degrees: The number of degrees to rotate
		:type degrees: integer or float
		:param user_id: the id of the user causing this event
		:type user_id: integer

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), \
				"Position must contain three floating point numbers"
		assert isinstance(degrees, (float, int)), "Degrees must be a number"
		assert isinstance(user_id, int), "User ID must be an integer"

		self.log.info(("move_head({}, {}, {})".format(pos, degrees, user_id)))
		return None

	def test(self):
		self.log.info("Test run")
		self.press([1, 1, 0], 2, True)
		self.move([0.3, 0.2, 0.9], 123, False)
		self.move([0.3, 0.2, 0.8], 123, False)
		self.release([0.1, 0.2, 0.3], 2, True)
		self.zoom(123)
		self.fade_away()
		self.rotate(90)
		self.move_model([4.3, 0.4, 0.5], 33)
		self.move_head([1.4, 0.0, -1.2], 180.2, 4)

	def test_bsp_prozess(self):
		file_path = "../../Model/tests/Beispielprozess.owl"
		self.models[file_path] = PASS.ModelManager(file_path)
		self.view = View()
		self.current_model = self.models[file_path]

		self.view.set_cur_scene(self.current_model.model.hasModelComponent[0])
		self.current_model.addChangeListener(self.view.on_change)

		#self.view.on_change(self.current_model.model.hasModelComponent[0])
		#self.view.on_change(
		#	self.current_model.model.hasModelComponent[0].subjects[0])
		#self.view.on_change(
		#	self.current_model.model.hasModelComponent[0].subjects[1])
		#self.current_model.model.hasModelComponent[0].addMessageExchange(
		#	self.current_model.model.hasModelComponent[0].subjects[0],
		#	self.current_model.model.hasModelComponent[0].subjects[1])

	def init_empty(self):
		file_path = "/tmp/temp_model.owl"
		self.models[file_path] = PASS.ModelManager()
		self.view = View()
		self.current_model = self.models[file_path]
		self.current_model.addChangeListener(self.view.on_change)
		# TODO: init model


if __name__ == "__main__":
	c = Controller()
	c.test()

