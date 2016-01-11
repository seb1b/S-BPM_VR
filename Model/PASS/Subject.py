from Actor import *

class Subject(Actor):

	"""
	A special kind of actor which's behavior is described through a behavior.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, behavior = None):
		"""
		 Constructor - Should never be used directly from outside the model framework.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		Actor.__init__(self, manager, uri, isBlank, blankNodeId, behavior)

		self._fireChangeEvents = True
		self.fireChangeEvent()



