from PASSProcessModelElement import *
from AbstractVisualRepresentation import *

class ActiveProcessComponent(PASSProcessModelElement):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
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



