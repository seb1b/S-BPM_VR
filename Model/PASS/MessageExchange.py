from PASSProcessModelElement import *
from ActiveProcessComponent import *
from MessageType import *

class MessageExchange(PASSProcessModelElement):

	"""
	This is a class that describes a message exchange between two active process components.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	""" ATTRIBUTES

	 The receiver of this message exchange. Defined by the ontology.

	receiver  (public)

	 The sender of this message exchange. Defined by the ontology.

	sender  (public)

	 The type this message has.

	hasType  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, sender = None, receiver = None, messageType = None):
		"""
		 Constructor - Should never be called directly from outside the model framwork.

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@return  :
		@author
		"""
		PASSProcessModelElement.__init__(self, manager, uri, isBlank, blankNodeId)
		
		if((sender is not None) and (not isinstance(sender, ActiveProcessComponent))):
			raise Exception("Sender type definition must be of type ActiveProcessComponent!")
		if((receiver is not None) and (not isinstance(receiver, ActiveProcessComponent))):
			raise Exception("Receiver type definition must be of type ActiveProcessComponent!")
		if((messageType is not None) and (not isinstance(messageType, MessageType))):
			raise Exception("MessageType parameter must be of type MessageType!")
		self.receiver = receiver
		self.sender = sender
		self.hasType = messageType
		
		self.hasAbstractVisualRepresentation = AbstractVisualRepresentation(self.modelManager)
		
		self._fireChangeEvents = True
		self.fireChangeEvent()
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "receiver"):
			return AttributeMultiplicity.UNIQUE
		elif(attributeName == "sender"):
			return AttributeMultiplicity.UNIQUE
		elif(attributeName == "hasType"):
			return AttributeMultiplicity.UNIQUE
		else:
			return PASSProcessModelElement.getAttrMultiplicity(self, attributeName)
