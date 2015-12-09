# -*- coding: utf-8 -*-

import string
import random

def randomXMLName(length = 12):
	name = "".join(random.choice(string.ascii_letters))
	name = name + "".join(random.choice(string.ascii_letters + string.digits) for i in range(11))
	return name