from PASSProcessModelElement import *

class State(PASSProcessModelElement):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	""" ATTRIBUTES

	 Property - Only get is allowed here. Checks the initial state property by taking
	 into account the rdfs::type variable.

	isInitialState  (public)

	 Property - Get and set is allowed. There's no shadow variable behind it, but
	 final state is managed through manipulating rdfs:type. A behavior might have
	 more than one final state (instead of a unique initial state).

	isFinalState  (public)

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
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasAbstractVisualRepresentation = AbstractVisualRepresentation(self.modelManager)
		
	@property
	def isInitialState(self):
		return ("http://www.purl.org/s-scm-ont#InitialState" in self.type)

	@property
	def isFinalState(self):
		return ("http://www.purl.org/s-scm-ont#FinalState" in self.type)
		
	@isFinalState.setter
	def isFinalState(self, value):
		if(not isinstance(value, bool)):
			raise Exception("isFinalState must be of type bool!")
		elif("http://www.purl.org/s-scm-ont#FinalState" not in self.type):
				self.type.append("http://www.purl.org/s-scm-ont#FinalState")

