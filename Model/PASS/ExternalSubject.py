from InterfaceActor import *

class ExternalSubject(InterfaceActor):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, referenceUri = None):
		"""
		 Constructor - Never call directly

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		InterfaceActor.__init__(self, manager, uri, isBlank, blankNodeId, referenceUri)

		self._fireChangeEvents = True
		self.fireChangeEvent()

