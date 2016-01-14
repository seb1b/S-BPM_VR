from Resource import *
from Tools import *
from AttributeMultiplicity import *

class Point2D(Resource):

	"""
	A point in 2D space.

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The x value of the 2d point.

	hasXValue  (public)

	 The y value of the 2d point.

	hasYValue  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, x=0.0, y=0.0):
		"""
		 Constructor

		@return  :
		@author
		"""
		Resource.__init__(self, manager, isBlank = True, blankNodeId = str(randomXMLName()))
		x = float(x)
		y = float(y)
		self.hasXValue = x
		self.hasYValue = y
		
		self._fireChangeEvents = True
		self.fireChangeEvent()
		
	def getAttrMultiplicity(self, attributeName):
		if((attributeName == "hasXValue") or (attributeName == "hasYValue")):
			return AttributeMultiplicity.UNIQUE
		else:
			return Resource.getAttrMultiplicity(self, attributeName)
			
	def fireChangeEvent(self):
		#Also fire a change event for the class that owns the abstract visual representation to make the use for the view more easy
		abstractVisualRepresentation = self.getParent(None, 1)
		if(abstractVisualRepresentation is not None):
			owner = abstractVisualRepresentation.getParent(None, 1)
			if(owner is not None):
				owner.fireChangeEvent()
		Resource.fireChangeEvent(self)



