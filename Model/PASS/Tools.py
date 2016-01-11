# -*- coding: utf-8 -*-

import string
import random

def randomXMLName(length = 12):
	"""
	Helper function to create random valid xml names.
	
	@param in length : Defines the length that the xml name should have. 12 by default.
	@return The xml name as a string:
	@author Lukas Block
	"""
	name = "".join(random.choice(string.ascii_letters))
	name = name + "".join(random.choice(string.ascii_letters + string.digits) for i in range(11))
	return name