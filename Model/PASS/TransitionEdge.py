from PASSProcessModelElement import *
from State import *

class TransitionEdge(PASSProcessModelElement):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	""" ATTRIBUTES

	 The state where this transition starts. Defined by the onology.

	hasSourceState  (public)

	 The state where this transition ends. Defined by the onology.

	hasTargetState  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, sourceState = None, targetState = None):
		"""
		 Constructor

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		if((sourceState is not None) and (not isinstance(sourceState, State))):
			raise Exception("SourceState parameter must be of type State!")
		if((targetState is not None) and (not isinstance(targetState, State))):
			raise Exception("TargetState parameter must be of type State")
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasSourceState = sourceState
		self.hasTargetState = targetState
		
		self.hasAbstractVisualRepresentation = AbstractVisualRepresentation(self.modelManager)
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "hasSourceState"):
			return AttributeMultiplicity.UNIQUE
		elif(attributeName == "hasTargetState"):
			return AttributeMultiplicity.UNIQUE
		else:
			return PASSProcessModelElement.getAttrMultiplicity(self, attributeName)
