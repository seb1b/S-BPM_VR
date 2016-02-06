from Resource import *
from Tools import *
from AttributeMultiplicity import *

class Point3D(Resource):

	"""


	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The x value of the 3d point.

	hasXValue  (public)

	 The y value of the 3d point.

	hasYValue  (public)

	 The x value of the 3d point.

	hasZValue  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, x=0.0, y=0.0, z=0.0):
		"""
		 Constructor

		@return  :
		@author
		"""
		Resource.__init__(self, manager, isBlank = True, blankNodeId = str(randomXMLName()))
		x = float(x)
		y = float(y)
		z = float(z)
		self.hasXValue = x
		self.hasYValue = y
		self.hasZValue = z
		
		self._fireChangeEvents = True
		self.fireChangeEvent()
		
	def getAttrMultiplicity(self, attributeName):
		if((attributeName == "hasXValue") or (attributeName == "hasYValue") or (attributeName == "hasZValue")):
			return AttributeMultiplicity.UNIQUE
		else:
			return Resource.getAttrMultiplicity(self, attributeName)
		
		
	def fireChangeEvent(self, attrName = None):
		if(self._fireChangeEvents):
			#Also fire a change event for the class that owns the abstract visual representation to make the use for the view more easy
			abstractVisualRepresentation = self.getParent(None, 1)
			if(abstractVisualRepresentation is not None):
				owner = abstractVisualRepresentation.getParent(None, 1)
				if(owner is not None):
					owner.fireChangeEvent("hasAbstractVisualRepresentation")
			Resource.fireChangeEvent(self, attrName)



