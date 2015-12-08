#!/usr/bin/env python3

def press(pos, user_id, is_left=False):
	"""This function handles a push or press event

	Press handles user input similar to a pressing a mouse button but not
	releasing it yet, i.e. this function should only be called for pushing
	the button, not for releasing it.

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

	print("press({}, {}, {})".format(pos, user_id, is_left))
	return None


def release(pos, user_id, is_left=False):
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
	return None


def move(pos, user_id, is_left=False):
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
	return None


def zoom(level):
	"""TODO

	:param level: the zoom level
	:type level: integer or float

	:return: None
	"""
	assert isinstance(level, (float, int)), "Level must be a number"
	#TODO check what level actually means (absolute or relative value)

	print("zoom({})".format(level))
	return None


def fade_away():
	"""This function fades the view away

	This fades the view away in one step (full zoom out) to give an broad
	overview over the entire scene. It should be called if the user wants to
	zoom out from a close up view and directly jump to the lowest zoom level.

	:return: None
	"""
	print("fade_away()")
	return None


def rotate(degrees):
	"""This function rotates the entire scene for the given number of degrees

	:param degrees: The number of degrees to rotate
	:type degrees: integer or float

	:return: None
	"""
	assert isinstance(degrees, (float, int)), "Degrees must be a number"

	print("rotate({})".format(degrees))
	return None


def move_model(pos, user_id):
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
	return None


def move_head(pos, degrees, user_id):
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


def test():
	print("Test run")
	press([1, 1, 0], 2, True)
	move([0.3,0.2,0.9], 123, False)
	move([0.3,0.2,0.8], 123, False)
	release([0.1, 0.2, 0.3], 2, True)
	zoom(123)
	fade_away()
	rotate(90)
	move_model([4.3, 0.4, 0.5], 33)
	move_head([1.4, 0.0, -1.2], 180.2, 4)


if __name__ == "__main__":
	test()

