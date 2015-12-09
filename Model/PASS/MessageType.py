from PASSProcessModelElement import *

class MessageType(PASSProcessModelElement):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)

		self._fireChangeEvents = True
		self.fireChangeEvent()
		

