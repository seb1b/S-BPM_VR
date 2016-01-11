from TransitionEdge import *
from MessageExchange import *

class CommunicationActTransition(TransitionEdge):

	"""
	The communication act transition is a superclass transition from a receive state or a transition to a send state.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	""" ATTRIBUTES

	 The message exchange type this communication transition belongs to.

	refersTo  (public)

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
		TransitionEdge.__init__(self, manager, uri, isBlank, blankNodeId, sourceState, targetState)
		if((refersTo is not None) and (not isinstance(refersTo, MessageExchange))):
			raise Exception("'RefersTo' must be of type MessageExchange!")
		self.refersTo = refersTo
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "refersTo"):
			return AttributeMultiplicity.UNIQUE
		else:
			return TransitionEdge.getAttrMultiplicity(self, attributeName)

