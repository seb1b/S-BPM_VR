#!/usr/bin/env python2

from PASS import ModelManager
from view import View
from hardware_main import VRHardware

class Controller:

	def __init__(self):
		# dictionaries of model and view, file path is key
		self.models = {}
		self.views = {}
		self.current_model = None
		self.current_view = None

		self.press_position = None
		self.drag_position = None
		self.release_position = None

		self.selected_objects = []
		self.pressed_object = None
		self.released_object = None
		self.pressed_is_left = False

		self.hw_main = VRHardware(self)

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
		:param is_left: Whether or not this event was caused by the left hand(default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), "Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), "Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), "Left/Right hand parameter must be a boolean value"

		print("press({}, {}, {})".format(pos, user_id, is_left))

		# TODO: check quick and dirty implementation

		if self.current_view is not None:
			assert self.current_model is not None
			obj = self.current_view.get_object(pos[:2])
			if obj is not None:
				if obj not in self.selected_objects:
					self.selected_objects.append(obj)
				self.pressed_object = obj
				self.pressed_is_left = is_left
				self.current_view.set_highlight(obj, True)
		self.press_position = pos

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
		:param is_left: Whether or not this event was caused by the left hand (default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), "Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), "Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), "Left/Right hand parameter must be a boolean value"

		print("release({}, {}, {})".format(pos, user_id, is_left))

		if self.current_view is not None:
			assert self.current_model is not None
			if self.pressed_object is not None and self.pressed_is_left == is_left:
				assert self.pressed_object in self.selected_objects
				self.released_object = self.pressed_object
				self.pressed_object = None
				self.current_view.set_highlight(self.released_object, False)
		self.release_position = pos

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
		:param is_left: Whether or not this event was caused by the left hand (default: false)
		:type is_left: boolean

		:return: None
		"""
		assert len(pos) == 3, "Position argument must be of length 3 (x,y,z)"
		for p in pos:
			assert isinstance(p, (float, int)), "Position must contain three floating point numbers"
			assert (p >= 0.0 and p <= 1.0), "Position must be in normalized screen space coordinates [0.0,1.0]"
		assert isinstance(user_id, int), "User ID must be an integer"
		assert isinstance(is_left, bool), "Left/Right hand parameter must be a boolean value"

		print("move({}, {}, {})".format(pos, user_id, is_left))

		if self.current_view is not None:
			assert self.current_model is not None
			if self.pressed_object is not None and self.pressed_is_left == is_left:
				assert self.pressed_object in self.selected_objects
				# TODO: self.pressed_object.hasVisualPresentation().setPoint3D(pos[0], pos[1], pos[2])
				# TODO: check and fix quick and dirty implementation
				self.current_view.move_object(self.pressed_object, pos[:2])
			self.current_view.move_cursor(pos, user_id, is_left)

		return None

	def zoom(self, level):
		"""TODO

		:param level: the relative zoom level: -1 zoom out, +1 zoom in
		:type level: integer or float

		:return: None
		"""
		assert isinstance(level, (float, int)), "Level must be a number"
		if self.current_view is not None:
			assert self.current_model is not None
			if level < 0:
				# TODO: if self.current_view.get_current_zoom_level() == 0:
					# TODO: go back one s-bpm level
					# pass
				# else:
				self.current_view.zoom(-1)
			elif level > 0:
				self.current_view.zoom(+1)

		print("zoom({})".format(level))
		return None

	def fade_away(self):
		"""This function fades the view away

		This fades the view away in one step (full zoom out) to give an broad
		overview over the entire scene. It should be called if the user wants to
		zoom out from a close up view and directly jump to the lowest zoom level.

		:return: None
		"""
		print("fade_away()")
		return None

	def rotate(self, degrees):
		"""This function rotates the entire scene for the given number of degrees

		:param degrees: The number of degrees to rotate
		:type degrees: integer or float

		:return: None
		"""
		assert isinstance(degrees, (float, int)), "Degrees must be a number"

		print("rotate({})".format(degrees))
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
			assert isinstance(p, (float, int)), "Position must contain three floating point numbers"
		assert isinstance(user_id, int), "User ID must be an integer"

		print("move_model({}, {})".format(pos, user_id))

		if self.current_view is not None:
			assert self.current_model is not None
			self.current_view.move_scene(pos[:2])

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
			assert isinstance(p, (float, int)), "Position must contain three floating point numbers"
		assert isinstance(degrees, (float, int)), "Degrees must be a number"
		assert isinstance(user_id, int), "User ID must be an integer"

		print("move_head({}, {}, {})".format(pos, degrees, user_id))
		return None

	def test(self):
		print("Test run")
		self.press([1, 1, 0], 2, True)
		self.move([0.3, 0.2, 0.9], 123, False)
		self.move([0.3, 0.2, 0.8], 123, False)
		self.release([0.1, 0.2, 0.3], 2, True)
		self.zoom(123)
		self.fade_away()
		self.rotate(90)
		self.move_model([4.3, 0.4, 0.5], 33)
		self.move_head([1.4, 0.0, -1.2], 180.2, 4)

	def init_debug_setup(self):
		print("Initializing debug/testing model and view")
		file_path = "/var/temp/temp_model"
		self.models[file_path] = ModelManager(None)
		# TODO: init model
		self.views[file_path] = View()
		self.current_model = self.models[file_path]
		self.current_view = self.views[file_path]


if __name__ == "__main__":
	c = Controller()
	c.test()

