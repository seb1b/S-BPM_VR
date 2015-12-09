from Layer import *

class BaseLayer(Layer):

	"""


	:version: 2015-12-07
	:author: Kai Hartung
	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor - Should never be used directly from outside the model framework.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		Layer.__init__(self, manager, uri, isBlank, blankNodeId)

		self._fireChangeEvents = True
		self.fireChangeEvent()

