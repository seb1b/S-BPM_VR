from ActiveProcessComponent import *
from AttributeMultiplicity import *

class Actor(ActiveProcessComponent):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	""" ATTRIBUTES

	 Variable defined by the ontology. Must only link to behaviors that are also
	 registered to the layer the actor belongs to.

	hasBehavior  (public)

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
		ActiveProcessComponent.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasBehavior = behavior
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "hasBehavior"):
			return AttributeMultiplicity.UNIQUE
		else:
			return PASSProcessModelElement.getAttrMultiplicity(self, attributeName)