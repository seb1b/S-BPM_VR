from Resource import *
from PlainLiteral import *
from Tools import *

class VisualRepresentation(Resource):

	"""
	A wrapper class to include data of different formats into the PASS process model.

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The mime type in which the data is represeneted (e.g. application/xml). Refere
	 to the official MIME-Type documentation for further information.

	hasMIMEType  (public)

	 The data as a plain literal. It must be encoded in the type given in
	 hasMIMEType-Variable

	hasData  (public)

	"""

	def __init__(self, manager, mimeType, data, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor

		@param string mimeType :
		@param undef data :
		@return  :
		@author
		"""
		Resource.__init__(self, manager, isBlank = True, blankNodeId = str(Tools.randomXMLName()))
		
		if(not isinstance(mimeType, str)):
			raise Exception("Mime type definition must be of type string!")
		if(not isinstance(data, PlainLiteral)):
			raise Exception("Data set must be of type PlainLiteral!")
		self.hasMIMEType = mimeType
		self.hasData = data
		
		self._fireChangeEvents = True
		self.fireChangeEvent()



