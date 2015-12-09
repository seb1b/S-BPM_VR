from PASSProcessModelElement import *

class PASSProcessModel(PASSProcessModelElement):
	
	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		self.hasModelComponent = []