from InterfaceActor import *

class ExternalSubject(InterfaceActor):

	"""
	An external subject is a subject that links to another PASS process model that itself defines this PASS model as an
	external subject. This class is not fully specified in the ontology as this class is also not finished yet.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, referenceUri = None):
		"""
		 Constructor - Never call directly

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		InterfaceActor.__init__(self, manager, uri, isBlank, blankNodeId, referenceUri)

		self._fireChangeEvents = True
		self.fireChangeEvent()

