from Resource import *
from Tools import *
from AttributeMultiplicity import *

class MetaContent(Resource):

	"""


	:version: 2012-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The key value of this MetaContent. A key does not need to be unique amongst a
	 PASSProcessModelElement but should be.

	hasKey  (public)

	 The value of this metacontent. Is undefined because it could be of any
	 XMLLiteral type.

	hasValue  (public)

	"""

	def __init__(self, manager, key = None, value = None, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor

		@param string key : The key this meta content type should represent
		@param undef value : The value of this content type
		@return  :
		@author
		"""
		Resource.__init__(self, manager, isBlank = True, blankNodeId = str(randomXMLName()))
		
		if((key is None) or isinstance(key, str)):
			self.hasKey = key
			self.hasValue = value
		else:
			raise Exception("Key definition must be of type string!")
		
		self._fireChangeEvents = True
		self.fireChangeEvent()
		
	def getAttrMultiplicity(self, attributeName):
		if((attributeName == "hasKey") or (attributeName == "hasValue")):
			return AttributeMultiplicity.UNIQUE
		else:
			return Resource.getAttrMultiplicity(self, attributeName)



