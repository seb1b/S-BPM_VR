from CommunicationActTransition import *
from SendState import *

class SendTransition(CommunicationActTransition):

	"""
	A transition with a send state as its resource.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, sourceState = None, targetState = None, refersTo = None):
		"""
		 Constructor - Should never be called from outside the model framework.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		if((sourceState is not None) and (not isinstance(sourceState, SendState))):
			raise Exception("SourceState parameter must be of type SendState!")
		CommunicationActTransition.__init__(self, manager, uri, isBlank, blankNodeId, sourceState, targetState, refersTo)

		self._fireChangeEvents = True
		self.fireChangeEvent()



