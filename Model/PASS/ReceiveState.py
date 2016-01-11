from State import *

class ReceiveState(State):

	"""
	A state that represents that the actor waits for an incoming message.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor - Should never be called from outside the model framework.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		State.__init__(self, manager, uri, isBlank, blankNodeId)

		self._fireChangeEvents = True
		self.fireChangeEvent()



