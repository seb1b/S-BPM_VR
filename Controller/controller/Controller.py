#!/usr/bin/env python2
import os
import VR
import sys
import math
import PASS
import uuid
import time
import logging
import collections

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
		formatter = logging.Formatter('%(asctime)s.%(msecs)03d - {%(pathname)s:%(lineno)d} %(levelname)s: %(message)s','%H:%M:%S')
		ch.setFormatter(formatter)
		self.log.addHandler(ch)

		self.log.info("Starting controller")

		self.MAX_ACTIVE_USERS = 2  # ROFL!!

		self.model_files = []
		# dictionaries of model and view, file path is key
		self.models = {}
		self.current_model = None
		self.view = None

		self.users = []
		self.active_users = []

		self.press_position = {}
		self.drag_position = None
		self.release_position = {}

		self.selected_object = None
		self.pressed_object = None

		self.pressed_menu_bar = None
		self.pressed_menu_bar_item = None
		self.pressed_menu_bar_user_id = None
		self.pressed_menu_bar_is_left = None

		self.released_object = None
		self.pressed_is_left = False
		self.pressed_user_id = None

		self.highlighted_pos = None
		self.highlighted_pos_obj = None

		self.passive_selected_objects = collections.defaultdict(lambda: None)  # user_id is key

		VR.hw_main = VRHardware(self)

	def _check_active_users(self, user_id):
		assert user_id in self.users
		if user_id in self.active_users:
			return True
		if user_id not in self.active_users and len(self.active_users) < self.MAX_ACTIVE_USERS:
			self.log.info("Adding new active user with ID {}".format(user_id))
			self.active_users.append(user_id)
			return True
		return False

	def _check_user(self, user_id):
		if user_id not in self.users:
			self.users.append(user_id)
			is_active = self._check_active_users(user_id)
			self.view.add_new_user(user_id, is_active)

	def _update_selected_object(self, obj):
		if obj is not None and not isinstance(obj, PASS.PASSProcessModelElement):
			self.log.info("Ignoring select on object {}".format(obj))
			return
		if self.selected_object is not None and isinstance(self.selected_object, PASS.PASSProcessModelElement):
			if not self.view.set_highlight(self.selected_object, False):
				self.log.warning("Deselecting object {} failed".format(self.selected_object))
		self.selected_object = obj
		if self.selected_object is not None and isinstance(self.selected_object, PASS.PASSProcessModelElement):
			if not self.view.set_highlight(self.selected_object, True):
				self.log.warning("Selecting object {} failed".format(self.selected_object))

	def _update_passive_highlight(self, obj, user_id):
		if isinstance(obj, PASS.PASSProcessModelElement):
			if self.passive_selected_objects[user_id] is not None and isinstance(self.passive_selected_objects[user_id], PASS.PASSProcessModelElement):
				if not self.view.set_highlight(self.passive_selected_objects[user_id], False):
					self.log.warning("Deselecting passive object {} failed".format(self.passive_selected_objects[user_id]))
			self.passive_selected_objects[user_id] = obj
			if self.passive_selected_objects[user_id] is not None and isinstance(self.passive_selected_objects[user_id], PASS.PASSProcessModelElement):
				if not self.view.set_highlight(self.passive_selected_objects[user_id], True):
					self.log.warning("Selecting passive object {} failed".format(self.passive_selected_objects[user_id]))

	def _load_model(self, file_path, new=False):
		self.log.info("open_model({}, {})".format(file_path, new))
		assert self.view is not None

		if new:
			self.current_model = PASS.ModelManager()
			self.current_model.saveAs(file_path)
		elif file_path in self.models:
			self.current_model = self.models[file_path]
		else:
			self.current_model = PASS.ModelManager(file_path)

		self.models[file_path] = self.current_model
		self.models[self.models[file_path]] = file_path

		self.view.set_cur_scene(self.current_model.model.hasModelComponent[0])
		self.current_model.addChangeListener(self.view.on_change)

	def _save_model(self):
		self.log.info("_save_model()")
		if self.view is not None:
			assert self.current_model is not None
			file_path = self.models[self.current_model]
			assert isinstance(file_path, basestring)
			screenshot = VR.getSetup().getView(0).grab()
			image_file_name = "{}{}".format(os.path.splitext(file_path)[0], ".png")
			self.log.info("Saving screenshot {}".format(image_file_name))
			screenshot.write(image_file_name)
			self.log.info("Saving model file {}".format(file_path))
			self.current_model.saveAs(file_path)

	def process_menu_bar(self, message):
		assert message is not None, "Message is None"
		self.log.info("process_menu_bar({}{}{})".format('"', message, '"'))
		self.log.info("process_menu_bar: self.pressed_menu_bar: {}".format(self.pressed_menu_bar))
		self.log.info("process_menu_bar: self.pressed_object: {}".format(self.pressed_object))
		self.log.info("process_menu_bar: self.selected_object: {}".format(self.selected_object))
		if isinstance(self.pressed_menu_bar, View.MenuBar):
			self.log.info("process_menu_bar: self.pressed_menu_bar.name: {}".format(self.pressed_menu_bar.name))
		if isinstance(self.pressed_object, View.MenuBar):
			self.log.info("process_menu_bar: self.pressed_object.name: {}".format(self.pressed_object.name))

		if ((isinstance(self.pressed_menu_bar, View.MenuBar) and self.pressed_menu_bar.name == "layer_add") or (isinstance(self.pressed_object, View.MenuBar) and self.pressed_object.name == "layer_add")):
			if message == "subject_down":
				if not isinstance(self.pressed_object, View.MenuBar):
					self.log.info("process_menu_bar({}): pressed object is NOT MenuBar - returning".format(message))
					return
				if self.highlighted_pos_obj is None:
					assert self.highlighted_pos is None, "WTF"
					new_obj = self.view.get_cur_scene().addSubject()
					self.pressed_object = new_obj
					pos_norm_2d = self.view.local_to_world_2d(self.drag_position[:2])
					self.log.info("Creating subject at local {} / world {}".format(self.highlighted_pos, pos_norm_2d))
					new_obj.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
					new_obj.setMetaContent("Date", time.strftime("%c"))
					new_obj.label.append("New Subject")
					self._update_selected_object(new_obj)
					self.pressed_menu_bar = None
					self.pressed_menu_bar_item = None
					assert self.pressed_menu_bar_user_id is not None
					assert self.pressed_menu_bar_is_left is not None
					self.view.trigger_up(self.pressed_menu_bar_user_id, self.pressed_menu_bar_is_left)
				else:
					self.log.info("Setting pressed_menu_bar for subject creation")
					self.pressed_menu_bar = self.pressed_object
					self.pressed_menu_bar_item = message
			elif message == "subject_up":
				if self.highlighted_pos_obj is not None and self.pressed_menu_bar is not None:
					assert isinstance(self.pressed_menu_bar, View.MenuBar)
					assert self.highlighted_pos is not None, "WTF"
					new_obj = self.view.get_cur_scene().addSubject()
					self.pressed_object = None
					self.pressed_user_id = None
					pos_norm_2d = self.view.local_to_world_2d(self.highlighted_pos[:2])
					self.log.info("Creating subject at local {} / world {}".format(self.highlighted_pos, pos_norm_2d))
					self.view.remove_highlight_point(self.highlighted_pos_obj)
					self.highlighted_pos = None
					self.highlighted_pos_obj = None
					new_obj.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
					new_obj.setMetaContent("Date", time.strftime("%c"))
					new_obj.label.append("New Subject")
					self._update_selected_object(new_obj)
				self.pressed_menu_bar = None
				self.pressed_menu_bar_item = None
				self.pressed_menu_bar_user_id = None
				self.pressed_menu_bar_is_left = None
			elif message == "exsubject_down":
				# TODO: implement
				pass
			elif message == "exsubject_up":
				# TODO: implement
				pass
			elif message == "message_down":
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
				self.view.set_message_line(self.pressed_user_id, True)
			elif message == "message_up":
				pass
			else:
				self.log.warning("invalid mesage: {}".format(message))
		# TODO: implement rest
		elif ((isinstance(self.pressed_menu_bar, View.MenuBar) and self.pressed_menu_bar.name == "edit") or (isinstance(self.pressed_object, View.MenuBar) and self.pressed_object.name == "edit")):
			assert self.selected_object is not None and isinstance(self.selected_object, PASS.PASSProcessModelElement), "{}".format(self.selected_object)
			self.log.info("process_menu_bar: editing {}".format(self.selected_object))
			if message == "delete_down":
				self.log.info("Setting pressed_menu_bar for subject/state/message/transaction deletion")
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
			elif message == "delete_up":
				self.log.info("Deleting {}".format(self.selected_object))
				old_obj = self.selected_object
				self._update_selected_object(None)
				if isinstance(old_obj, PASS.ActiveProcessComponent):  # subject
					self.view.get_cur_scene().removeActiveComponent(old_obj, True)
				elif isinstance(old_obj, PASS.MessageExchange):
					self.view.get_cur_scene().removeMessageExchange(old_obj)
				elif isinstance(old_obj, PASS.State):
					self.view.get_cur_scene().removeState(old_obj)
				elif isinstance(old_obj, PASS.TransitionEdge):
					self.view.get_cur_scene().removeTransition(old_obj)
				self.pressed_menu_bar = None
				self.pressed_menu_bar_item = None
			elif message == "copy_down" and (isinstance(self.selected_object, PASS.ActiveProcessComponent) or isinstance(self.selected_object, PASS.State)):
				self.log.info("Setting pressed_menu_bar for copy")
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
			elif  message == "copy_up" and (isinstance(self.selected_object, PASS.ActiveProcessComponent) or isinstance(self.selected_object, PASS.State)):
				self.log.info("Copying {}".format(self.selected_object))
				pos = self.selected_object.hasAbstractVisualRepresentation.getPoint2D()
				pos[0] += 0.3
				pos[1] += 0.3
				if isinstance(self.selected_object, PASS.ActiveProcessComponent):
					new_obj = self.view.get_cur_scene().duplicateActiveProcessComponent(self.selected_object)
				else:
					new_obj = self.view.get_cur_scene().duplicateState(self.selected_object)
				new_obj.hasAbstractVisualRepresentation.setPoint2D(pos[0], pos[1])
				self._update_selected_object(new_obj)
				self.pressed_menu_bar = None
				self.pressed_menu_bar_item = None
			elif message == "cancel_down" and (isinstance(self.selected_object, PASS.ActiveProcessComponent)
				or isinstance(self.selected_object, PASS.MessageExchange)
				or isinstance(self.selected_object, PASS.State)
				or isinstance(self.selected_object, PASS.TransitionEdge)):
				self.log.info("Setting pressed_menu_bar for cancel")
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
			elif message == "cancel_up" and (isinstance(self.selected_object, PASS.ActiveProcessComponent)
				or isinstance(self.selected_object, PASS.MessageExchange)
				or isinstance(self.selected_object, PASS.State)
				or isinstance(self.selected_object, PASS.TransitionEdge)):
				self.log.info("Canceling {}".format(self.selected_object))
				self._update_selected_object(None)
				self.pressed_menu_bar = None
				self.pressed_menu_bar_item = None
		elif ((isinstance(self.pressed_menu_bar, View.MenuBar) and self.pressed_menu_bar.name == "behavior_add") or (isinstance(self.pressed_object, View.MenuBar) and self.pressed_object.name == "behavior_add")):
			if message in ["functionState_down", "receiveState_down", "sendState_down"]:
				if not isinstance(self.pressed_object, View.MenuBar):
					self.log.info("process_menu_bar({}): pressed object is NOT MenuBar - returning".format(message))
					return
				if self.highlighted_pos_obj is None:
					assert self.highlighted_pos_obj is None, "WTF"
					if message == "functionState_down":
						new_obj = self.view.get_cur_scene().addFunctionState()
					elif message == "receiveState_down":
						new_obj = self.view.get_cur_scene().addReceiveState()
					elif message == "sendState_down":
						new_obj = self.view.get_cur_scene().addSendState()
					else:
						assert False, "I think you forgot to add the new state above!!!!!!!"
					self.pressed_object = None
					self.pressed_user_id = None
					pos_norm_2d = self.view.local_to_world_2d(self.drag_position[:2])
					self.log.info("Creating {} at local {} / world {}".format(message, self.highlighted_pos, pos_norm_2d))
					new_obj.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
					new_obj.setMetaContent("Date", time.strftime("%c"))
					label = message.split("_")[0]  # remove _up/_down
					label = "New {}{}".format(label[0].upper(), label[1:])  # change first letter to upper case
					new_obj.label.append(label)
					self._update_selected_object(new_obj)
					self.pressed_menu_bar = None
					self.pressed_menu_bar_item = None
					assert self.pressed_menu_bar_user_id is not None
					assert self.pressed_menu_bar_is_left is not None
					self.view.trigger_up(self.pressed_menu_bar_user_id, self.pressed_menu_bar_is_left)
				else:
					self.log.info("Setting pressed_menu_bar for {} creation".format(message))
					self.pressed_menu_bar = self.pressed_object
					self.pressed_menu_bar_item = message
			elif message in ["functionState_up", "receiveState_up", "sendState_up"]:
				if self.highlighted_pos_obj is not None and self.pressed_menu_bar is not None:
					assert isinstance(self.pressed_menu_bar, View.MenuBar)
					assert self.highlighted_pos is not None, "WTF"
					if message == "functionState_up":
						new_obj = self.view.get_cur_scene().addFunctionState()
					elif message == "receiveState_up":
						new_obj = self.view.get_cur_scene().addReceiveState()
					elif message == "sendState_up":
						new_obj = self.view.get_cur_scene().addSendState()
					else:
						assert False, "I think you forgot to add the new state above!!!!!!!"
					self.pressed_object = None
					self.pressed_user_id = None
					pos_norm_2d = self.view.local_to_world_2d(self.highlighted_pos[:2])
					self.log.info("Creating {} at local {} / world {}".format(message, self.highlighted_pos, pos_norm_2d))
					self.view.remove_highlight_point(self.highlighted_pos_obj)
					self.highlighted_pos = None
					self.highlighted_pos_obj = None
					new_obj.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
					label = message.split("_")[0]  # remove _up/_down
					label = "New {}{}".format(label[0].upper(), label[1:])  # change first letter to upper case
					new_obj.label.append(label)
					self._update_selected_object(new_obj)
				self.pressed_menu_bar = None
				self.pressed_menu_bar_item = None
				self.pressed_menu_bar_user_id = None
				self.pressed_menu_bar_is_left = None
			elif message == "transition_down":
				self.pressed_menu_bar = self.pressed_object
				self.pressed_menu_bar_item = message
				self.view.set_message_line(self.pressed_user_id, True)
			elif message == "transition_up":
				pass
			else:
				self.log.warning("invalid message: {}".format(message))
		elif ((isinstance(self.pressed_menu_bar, View.MenuBar) and self.pressed_menu_bar.name == "start_page") or (isinstance(self.pressed_object, View.MenuBar) and self.pressed_object.name == "start_page")):
			# click on start screen -> open item
			# NOTE: start_page will send click only (no mousedown/up)
			self.log.info("Searching start screen object UUID: {} in {}".format(message, self.model_files))
			for entry in self.model_files:
				self.log.info("type({}): {} == type({}): {}".format(type(entry.model_id), entry.model_id, type(message), message))
				if entry.model_id == message:
					self.log.info("Found! - opening start screen object UUID: {}".format(message))
					new_model = False
					if not os.path.isfile(entry.file_name):
						self.log.info("New file - create empty model")
						new_model = True
						new_name = "New Process {}".format(time.strftime("%c"))
						new_image = "imi_logo.png"
						new_entry = View.InitScreenEntry(new_name, "./pass_models/{}.owl".format(new_name), new_image, str(uuid.uuid4()))
						self.log.info("Appending to model files list: {}".format(new_entry.__str__()))
						self.model_files.insert(0, new_entry)  # add new new_file to model_files
					self._load_model(entry.file_name, new_model)
					assert self.current_model is not None
					break
			self.pressed_menu_bar = None
			self.pressed_menu_bar_item = None
		elif ((isinstance(self.pressed_menu_bar, View.MenuBar) and self.pressed_menu_bar.name == "meta") or (isinstance(self.pressed_object, View.MenuBar) and self.pressed_object.name == "meta")):
			if not isinstance(self.selected_object, PASS.PASSProcessModelElement):
				self.log.warning("Got change event from meta, but there is no selected_object to change! message: {}".format(message))
			elif message.startswith("metaContent["):
				key = message.split("[")
				assert len(key) >= 2
				key = key[1].split("]")
				assert len(key) >= 2
				key = key[0]
				self.log.info("Meta key: {}".format(key))
				old_value = message.split("%%%OLDSTART%%%")
				assert len(old_value) >= 2
				old_value = old_value[1].split("%%%OLDEND%%%")
				assert len(old_value) >= 2
				old_value = old_value[0]
				self.log.info("Old value: {}".format(old_value))
				new_value = message.split("%%%NEWSTART%%%")
				assert len(new_value) >= 2
				new_value = new_value[1].split("%%%NEWEND%%%")
				assert len(new_value) >= 2
				new_value = new_value[0]
				self.log.info("New value: {}".format(new_value))
				# check existing meta data
				if key in self.selected_object.getMetaKeys():
					self.log.info("Found existing key {}".format(key))
					self.selected_object.setMetaContent(key, new_value)
					# TODO: enable to save on changing label value
					#self._save_model()
				else:
					self.log.info("Key not found: {}".format(key))
					# TODO: add new entry (probably?)
			else:
				self.log.warning("Received unhandled message from meta: {}".format(message))
		else:
			self.log.warning("invalid pressed_object: {} - message was {}".format(self.pressed_object, message))

	def process_hardware(self):
		VR.hw_main.process()

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
			self._check_user(user_id)
			self.view.press(user_id, is_left)  # show closed hand in view
			obj = self.view.get_object(user_id, is_left)
			if obj is not None and self.pressed_user_id is None and self._check_active_users(user_id):
				# force remove highlight from passive user
				for p_user_id, p_obj in self.passive_selected_objects:
					if p_obj is obj:
						self._update_passive_highlight(None, p_user_id)

				if isinstance(obj, View.MenuBar):
					# CASE: click on menu bar -> trigger cursor click
					self.log.info(("Press on MenuBar: {}".format(obj.name)))
					if self.highlighted_pos_obj is None and (obj.name == "layer_add" or obj.name == "behavior_add"):  # otherwise "edit" or "meta" or "start_page"
						# here, we want to trigger_up in process_menu_bar() to ignore it (e.g., create subject on press),
						# so we need to know the user_id/is_left in process_menu_bar() -> store it
						assert self.current_model is not None
						self.pressed_menu_bar_user_id = user_id
						self.pressed_menu_bar_is_left = is_left
					self.view.press(user_id, is_left)
					self.view.trigger_down(user_id, is_left)
				else:
					self.log.info("Unimportant object returned on press(): {}".format(obj))

				self._update_selected_object(obj)
				self.log.info("Setting new pressed_object: {}".format(obj))
				self.pressed_object = obj
				self.pressed_is_left = is_left
				self.drag_position = pos
				self.pressed_user_id = user_id
			elif obj is not None and obj not in self.passive_selected_objects and obj is not self.selected_object and not self._check_active_users(user_id):
				# CASE: press on object from passive user
				self._update_passive_highlight(obj, user_id)

		self.press_position[user_id] = pos
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
			self._check_user(user_id)
			if self.pressed_object is not None and self.pressed_is_left == is_left and self.pressed_user_id == user_id:
				# CASE: some object was released -> drag or select?
				#assert self.pressed_object is self.selected_object  # this is no longer true, MenuBar is not selected
				self.released_object = self.pressed_object
				self.pressed_object = None
				self.pressed_user_id = None

				obj = self.view.get_object(user_id, is_left)

				if (isinstance(self.pressed_menu_bar, View.MenuBar) or isinstance(obj, View.MenuBar)):  # NOTE: this was set in handle_menu_bar!!!!!!
					# CASE: item was created with highlight point
					# or "delete" was pressed with selected_object
					# or message was created
					if isinstance(self.pressed_menu_bar, View.MenuBar):
						self.log.info("Release previous MenuBar: {}".format(self.pressed_menu_bar.name))
					self.log.info("Release current object: {}".format(obj))
					if isinstance(obj, View.MenuBar):
						self.log.info("Release current object name: {}".format(obj.name))

					if self.pressed_menu_bar_item == "subject_down" or self.pressed_menu_bar_item == "exsubject_down":
						# subject down was pressed before, now released
						if obj is not self.pressed_menu_bar:
							self.log.info("User dragged off from menu bar during click!")
							self.pressed_menu_bar = None
							self.pressed_menu_bar_item = None
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "message_down":
						assert isinstance(self.released_object, View.MenuBar), "Inconsistency between pressed_menu_bar_item and released_object"
						# CASE: add message was released on field
						lo = self.view.get_object(user_id, True)
						ro = self.view.get_object(user_id, False)
						self.log.info("Trying to create new message between {} and {}".format(lo, ro))
						if isinstance(lo, PASS.Subject) and isinstance(ro, PASS.Subject):
							# CASE: adding message only possible if two subjects are selected
							new_obj = self.view.get_cur_scene().addMessageExchange(lo, ro)
							p1 = lo.hasAbstractVisualRepresentation.getPoint2D()
							p2 = ro.hasAbstractVisualRepresentation.getPoint2D()
							min_pos = [min(a, b) for a, b in zip(p1, p2)]
							max_pos = [max(a, b) for a, b in zip(p1, p2)]
							new_obj.hasAbstractVisualRepresentation.setPoint2D(min_pos[0] + (max_pos[0] - min_pos[0]) / 2, min_pos[1] + (max_pos[1] - min_pos[1]) / 2)
							new_obj.label.append("New Message")
							new_obj.setMetaContent("Date", time.strftime("%c"))
							self._update_selected_object(new_obj)
							self.released_object = new_obj
						else:
							self.log.info("User {} trying to create message on invalid targets".format(user_id))
						self.pressed_menu_bar = None
						self.pressed_menu_bar_item = None
						self.view.set_message_line(user_id, False)
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "transition_down":
						assert isinstance(self.released_object, View.MenuBar), "Inconsistency between pressed_menu_bar_item and released_object"
						# CASE: add transition was released on field
						lo = self.view.get_object(user_id, True)
						ro = self.view.get_object(user_id, False)
						self.log.info("Trying to create new transition edge between {} and {}".format(lo, ro))
						if isinstance(lo, PASS.FunctionState) and isinstance(ro, PASS.State):
							new_obj = self.view.get_cur_scene().addStandardTransition(lo, ro)
							p1 = lo.hasAbstractVisualRepresentation.getPoint2D()
							p2 = ro.hasAbstractVisualRepresentation.getPoint2D()
							min_pos = [min(a, b) for a, b in zip(p1, p2)]
							max_pos = [max(a, b) for a, b in zip(p1, p2)]
							new_obj.hasAbstractVisualRepresentation.setPoint2D(min_pos[0] + (max_pos[0] - min_pos[0]) / 2, min_pos[1] + (max_pos[1] - min_pos[1]) / 2)
							new_obj.label.append("New Standard Transition")
							new_obj.setMetaContent("Date", time.strftime("%c"))
							self._update_selected_object(new_obj)
							self.released_object = new_obj
						else:
							self.log.info("User {} trying to create transition edge on invalid targets".format(user_id))
						self.pressed_menu_bar = None
						self.pressed_menu_bar_item = None
						self.view.set_message_line(user_id, False)
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "delete_down":
						# delete was pressed before, now released
						if obj is not self.pressed_menu_bar:
							self.log.info("User dragged off from menu bar during click!")
							self.pressed_menu_bar = None
							self.pressed_menu_bar_item = None
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "copy_down":
						# copy was pressed before, now released
						if obj is not self.pressed_menu_bar:
							self.log.info("User dragged off from menu bar during click!")
							self.pressed_menu_bar = None
							self.pressed_menu_bar_item = None
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "cancel_down":
						# cancel was pressed before, now released
						if obj is not self.pressed_menu_bar:
							self.log.info("User dragged off from menu bar during click!")
							self.pressed_menu_bar = None
							self.pressed_menu_bar_item = None
						self.view.trigger_up(user_id, is_left)
					elif self.pressed_menu_bar_item == "functionState_down" or self.pressed_menu_bar_item == "receiveState_down" or self.pressed_menu_bar_item == "sendState_down":
						# *state down was pressed before, now released
						if obj is not self.pressed_menu_bar:
							self.log.info("User dragged off from menu bar during click!")
							self.pressed_menu_bar = None
							self.pressed_menu_bar_item = None
						self.view.trigger_up(user_id, is_left)
					elif obj.name == "start_page":
						# click on start page (no mouseup/down here, handle a click (up/down at once)
						self.pressed_menu_bar = obj
						self.pressed_menu_bar_item = obj.name
						self.view.trigger_up(user_id, is_left)
					else:
						self.log.warning("Invalid MenuBar type or so")
					#self.pressed_menu_bar = None
					#self.pressed_menu_bar_item = None
				#elif sum([x ** 2 for x in [a - b for a, b in zip(self.press_position[user_id], pos)]]) < 10.0:
				#	# CASE: some field object was selected
				#	# nothing to do LOL
				#	pass
				else:
					# CASE: some field object was dragged/moved
					# nothing to do
					assert self.current_model is not None, "Why is this happending? O_o double check"
					pass
			elif self.pressed_object is None and self._check_active_users(user_id):
				assert self.current_model is not None
				# CASE: release on field without object -> deselect everything and whatnot
				if self.selected_object is None and self.highlighted_pos_obj is None:
					# set highlight on empty field (for creating new object from menubar combo-command)
					self.highlighted_pos_obj = self.view.highlight_pos(pos[:2])
					self.highlighted_pos = pos
				elif self.selected_object is None:
					# remove highlight on empty field
					self.view.remove_highlight_point(self.highlighted_pos_obj)
					self.highlighted_pos_obj = None
					self.highlighted_pos = None
				else:
					# remove highlight from object
					self._update_selected_object(None)
			else:
				#assert self.current_model is not None
				# passive user release -> remove passive highlight from user
				self._update_passive_highlight(None, user_id)

		self.release_position[user_id] = pos
		self.view.release(user_id, is_left)

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
			self._check_user(user_id)
			if self.pressed_object is not None and self.pressed_user_id == user_id and self.pressed_is_left == is_left:
				#assert self.pressed_object is self.selected_object  # this is no longer true, MenuBar is not selected
				#if not isinstance(self.pressed_object, View.MenuBar):
				# TODO: the drag position is not set here. WTF?
				if isinstance(self.pressed_object, PASS.PASSProcessModelElement):
					assert self.current_model is not None
					assert hasattr(self.pressed_object, "hasAbstractVisualRepresentation")
					self.log.info("Moving object to {}".format(pos))
					pos_norm_2d = self.view.local_to_world_2d(pos[:2])
					old_pos = self.pressed_object.hasAbstractVisualRepresentation.getPoint2D()
					self.log.info("Moving object from {} to {} in model".format(old_pos, pos_norm_2d))
					self.pressed_object.hasAbstractVisualRepresentation.setPoint2D(pos_norm_2d[0], pos_norm_2d[1])
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
			self._check_user(user_id)
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to zoom".format(user_id))
				return None
			if self.current_model is None:
				self.log.debug("No current model, ignore zoom")
				return None
			if level < 0:
				if self.view.current_zoom_level() == 0:
					behavior = self.view.get_cur_scene()
					if isinstance(behavior, PASS.Behavior):
						layer = self.current_model.getParent(behavior, PASS.Layer)
						if layer is not None:
							assert isinstance(layer, PASS.Layer), "Got invalid parent from Model"
							# remove all highlights
							for u in self.users:
								self._update_passive_highlight(None, u)
							self._update_selected_object(None)
							self.view.set_cur_scene(layer)
				else:
					self.view.zoom(-1)
			elif level > 0:
				self.view.zoom(1)
		return None

	def fade_away(self, user_id):
		"""This function fades the view away

		This fades the view away in one step (full zoom out) to give an broad
		overview over the entire scene. It should be called if the user wants to
		zoom out from a close up view and directly jump to the lowest zoom level.

		:return: None
		"""
		self.log.info("fade_away()")

		if self.view is not None:
			assert self.current_model is not None
			self._check_user(user_id)
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
			self._check_user(user_id)
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to fade_in".format(user_id))
				return None
			obj = self.view.get_object(user_id, is_left)
			if obj is not None and self.pressed_user_id is None:
				assert self.pressed_object is None, "Inconsistent pressed_* variables"
				if isinstance(obj, PASS.Subject):
					# remove all highlights
					for u in self.users:
						self._update_passive_highlight(None, u)
					self._update_selected_object(None)
					assert self.current_model is not None
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
			self._check_user(user_id)
			if not self._check_active_users(user_id):
				self.log.debug("Inactive user {} trying to move_model".format(user_id))
				return None
			# normalize to [-1,1]
			self.view.move_scene([pos[0] * 2.0 - 1.0, pos[1] * 2.0 - 1.0])

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
		self.models[self.models[file_path]] = file_path
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
		self.view = View()
		self.current_model = None

		# Format: [InitScreenEntry, InitScreenEntry, ...]

		new_name = "New Process {}".format(time.strftime("%c"))
		new_image = "imi_logo.png"
		new_entry = View.InitScreenEntry(new_name, "./pass_models/{}.owl".format(new_name), new_image, str(uuid.uuid4()))
		self.log.info("Appending to model files list: {}".format(new_entry.__str__()))
		self.model_files = [new_entry]
		files = []

		for dirpath, _, filenames in os.walk("./pass_models/"):
			for f in filenames:
				files.append(os.path.join(dirpath, f))

		self.log.info("Files: {}".format(files))

		for fi in [f for f in files if f.endswith(".owl")]:
			basename = os.path.basename(fi)
			dispname = os.path.splitext(basename)[0]
			image_file_name = "{}{}".format(os.path.splitext(fi)[0], ".png")
			self.log.info("Searching for logo file {}".format(image_file_name))
			if image_file_name not in files:
				image_file_name = new_image
			t = View.InitScreenEntry(dispname, fi, image_file_name, str(uuid.uuid4()))
			self.log.info("Appending to model files list: {}".format(t.__str__()))
			self.model_files.append(t)

		self.view.show_init_screen(self.model_files)


if __name__ == "__main__":
	c = Controller()
	c.test()

