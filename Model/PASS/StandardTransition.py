from TransitionEdge import *
from FunctionState import *

class StandardTransition(TransitionEdge):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, sourceState = None, targetState = None):
		"""
		 Constructor - Should never be called from outside the model framework.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		if((sourceState is not None) and (not isinstance(sourceState, FunctionState))):
			raise Exception("SourceState parameter must be of type FunctionState!")
		TransitionEdge.__init__(self, manager, uri, isBlank, blankNodeId, sourceState, targetState)

		self._fireChangeEvents = True
		self.fireChangeEvent()



