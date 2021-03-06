from Resource import *
from Point2D import *
from Point3D import *
from Tools import *
from AttributeMultiplicity import *

class AbstractVisualRepresentation(Resource):

	"""
	This class represents the position of a PASSProcessModelElement in 2D and 3D space. As it does only
	provide some coordinates and no real visual representation it is called an abstract visual representation. The
	coordinate system of the abstract visual representation is a kartesian coordinate system mit y up, x right and z
	to front. The coordinate system is infinite in positive and negative direction.
	
	:version: 2012-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 Reference from the ontology. Represents the size of this pass process model
	 element. - You are allowed to directly manipulate this value with !only! double
	 values!

	hasRelativeSize  (public)

	 Reference from the ontology. Do not update them directly - Better use the
	 provided methods of this class.

	hasPoint2D  (public)

	 Reference from the ontology. Do not update them directly - Better use the
	 provided methods of this class.

	hasPoint3D  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor

		@param double relativeSize :
		@return  :
		@author
		"""
		Resource.__init__(self, manager, isBlank = True, blankNodeId = str(randomXMLName()))
		
		self.hasPoint2D = Point2D(manager)
		self.hasPoint3D = Point3D(manager)
		
		self._fireChangeEvents = True
		self.fireChangeEvent()


	def setPoint2D(self, xCoordinate, yCoordinate):
		"""
		 Manipulate the 2D point representation.

		@param double xCoordinate :
		@param double yCoordinate :
		@return  :
		@author
		"""
		xCoordinate = float(xCoordinate)
		yCoordinate = float(yCoordinate)
		self.hasPoint2D.hasXValue = xCoordinate
		self.hasPoint2D.hasYValue = yCoordinate

	def setPoint3D(self, xCoordinate, yCoordinate, zCoordinate):
		"""
		 Manipulate the coordinates of the 3D point.

		@param double xCoordinate :
		@param double yCoordinate :
		@param double zCoordinate :
		@return  :
		@author
		"""
		xCoordinate = float(xCoordinate)
		yCoordinate = float(yCoordinate)
		zCoordinate = float(zCoordinate)
		self.hasPoint3D.hasXValue = xCoordinate
		self.hasPoint3D.hasYValue = yCoordinate
		self.hasPoint3D.hasZValue = zCoordinate

	def getPoint2D(self):
		"""
		 Returns a two dimensional array [x, y] containing the coordinates of the point.

		@return double[] :
		@author
		"""
		result = []
		result.append(self.hasPoint2D.hasXValue)
		result.append(self.hasPoint2D.hasYValue)
		return result

	def getPoint3D(self):
		"""
		 Returns a 3d array [x, y, z] of the coordinates of the 3d point.

		@return double[] :
		@author
		"""
		result = []
		result.append(self.hasPoint3D.hasXValue)
		result.append(self.hasPoint3D.hasYValue)
		result.append(self.hasPoint3D.hasZValue)
		return result
		
	def getAttrMultiplicity(self, attributeName):
		if((attributeName == "hasPoint3D") or (attributeName == "hasPoint2D") or (attributeName == "hasRelativeSize")):
			return AttributeMultiplicity.UNIQUE
		else:
			return Resource.getAttrMultiplicity(self, attributeName)



