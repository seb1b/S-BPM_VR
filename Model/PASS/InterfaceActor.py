from ActiveProcessComponent import *
from Resource import *
from AttributeMultiplicity import *

class InterfaceActor(ActiveProcessComponent):

	"""
	An interface actor is the superclass for all external subject like elements in a PASS model.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	""" ATTRIBUTES

	 The PASSProcessModel this Interface Actor references. Returns exactly the URI
	 (or a sameAs) of the model that should be referenced!

	references  (public)

	 Property that shows the uri, that is also stored in the references resource.

	referenceUri  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, referenceUri = None):
		"""


		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		ActiveProcessComponent.__init__(self, manager, isBlank, blankNodeId)
		self.references = Resource(self.modelManager, uri = referenceUri)

	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "references"):
			AttributeMultiplicity.UNIQUE
		else:
			return PASSProcessModelElement.getAttrMultiplicity(attributeName)

	@property
	def referenceUri(self):
		return self.references.uri
