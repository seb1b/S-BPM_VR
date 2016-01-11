from PASSProcessModelElement import *
from ListenerList import *

class PASSProcessModel(PASSProcessModelElement):
	"""
	This class represents a PASS Process model.
	
	:version: 2015-12-04
	:author: Lukas Block
	"""
	
	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasModelComponent = ListenerList([], self)
		
		self._fireChangeEvents = True
		self.fireChangeEvent()