from PASSProcessModelElement import *
from AbstractVisualRepresentation import *

class ActiveProcessComponent(PASSProcessModelElement):

	"""
	This is an active process component of the PASS model. It is the superclass to a number of different
	self-acting objects like subjects, actors etc.
	
	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor - Never call directly

		@param ModelManager manger : The parent element (if one exists).		
		@return  :
		@author
		"""
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasAbstractVisualRepresentation = AbstractVisualRepresentation(self.modelManager)



