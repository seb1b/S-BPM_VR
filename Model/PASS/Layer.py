from PASSProcessModelElement import *
from Subject import *
from Behavior import *
from ExternalSubject import *
from ActiveProcessComponent import *
from MessageExchange import *
from Actor import *
from MessageType import *
from PASSProcessModel import *
from AttributeMultiplicity import *
from ListenerList import *
from ActiveProcessComponent import *

import math

class Layer(PASSProcessModelElement):

	"""
	A superclass for all layers in a PASS process model. A layer is an abstract definition of a model.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	""" ATTRIBUTES

	 See definition in ontology. Exactly one reference is given!

	belongsTo  (public)

	 See definition in ontology

	hasModelComponent  (public)

	 Is a property - Returns all message exchanges that are assigned by has model
	 component. See documentation MessageExchange.

	messageExchanges  (public)

	 Is a property - Returns all ActiveProcessComponents that are assigned to this
	 layer by hasModelComponent. See ActiveProcessDocumentation documentation for
	 further information.

	activeComponents  (public)

	 Is a property - Returns all the Behavior classes that are assigned to this lyer
	 via hasModelComponent. For further information see the Behavior documentation.

	behaviors  (public)

	 Is a property - Returns all Subjects that are assigned to this layer by
	 hasModelComponent. See Subject documentation for further information.

	subjects  (public)

	 Is a property - Returns all ExternalSubjects that are assigned to this layer by
	 hasModelComponent. See ExternalSubject documentation for further information.

	externalSubjects  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None, parentModel = None):
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
		
		if((parentModel is not None) and (not isinstance(parentModel, PASSProcessModel))):
			raise Exception("ParentModel parameter must be of type PASSProcessModel!")
		self.belongsTo = parentModel
		self.hasModelComponent = ListenerList([], self)
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "belongsTo"):
			AttributeMultiplicity.UNIQUE
		else:
			return PASSProcessModelElement.getAttrMultiplicity(self, attributeName)
		
	@property
	def messageExchanges(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, MessageExchange)):
				result.append(c)
		return result
		
	@property
	def activeComponents(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, ActiveProcessComponent)):
				result.append(c)
		return result
		
	@property
	def behaviors(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, Behavior)):
				result.append(c)
		return result
		
	@property
	def subjects(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, Subject)):
				result.append(c)
		return result
		
	@property
	def externalSubjects(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, ExternalSubject)):
				result.append(c)
		return result
		
	@property
	def activeProcessComponents(self):
		result = []
		for c in self.hasModelComponent:
			if (isinstance(c, ActiveProcessComponent)):
				result.append(c)
		return result

	def addSubject(self, behaviorToAssign = None):
		"""
		 Adds a new subject to this layer.

		@param Behavior behaviorToAssign : The behavior that should be assigned to the subject.
		@return Subject :
		@author
		"""
		if((behaviorToAssign is not None) and (not isinstance(behaviorToAssign, Behavior))):
			raise Exception("'BehaviorToAssign' must be of type Behavior!")
		if(behaviorToAssign is None):
			behaviorToAssign = self.addBehavior()
		newSubject = Subject(self.modelManager, behavior=behaviorToAssign)
		self.hasModelComponent.append(newSubject)
		return newSubject
		
	def addExternalSubject(self, uri):
		"""


		@param short uri : Uri where this process modell is stored.
		@return ExternalSubject :
		@author
		"""
		if(not isinstance(uri, str)):
			raise Exception("'Uri' must be of type string!")
		newExSub = ExternalSubject(self.modelManager, referenceUri = uri)
		self.hasModelComponent.append(newExSub)
		return newExSub

	def removeActiveComponent(self, componentToRemove, removeBehavior = True):
		"""


		@param ActiveProcessComponent componentToRemove : The subject, external subject, ... to remove from this layer
		@param bool removeBehavior : Tries to also delete the behavior of this active component, if it is of type subject.
		@return  :
		@author
		"""
		if(not isinstance(componentToRemove, ActiveProcessComponent)):
			raise Exception("'Uri' must be of type Behavior!")	
		if(not isinstance(removeBehavior, bool)):
			raise Exception("'removeBehavior' must be of type bool!")
		#Remove incident message exchanges
		for e in self.messageExchanges:
			if((e.sender is componentToRemove) or (e.receiver is componentToRemove)):
				self.removeMessageExchange(e)
		#Remove behavior if requested
		if((removeBehavior) and isinstance(componentToRemove, Actor)):
			behaviorToRemove = componentToRemove.hasBehavior
			self.removeBehavior(behaviorToRemove)
		#Remove process element
		self.hasModelComponent.remove(componentToRemove)

	def addMessageExchange(self, sender, receiver, messageType = None):
		"""
		 Adds a new message exchange to this layer.

		@param Actor sender : The sender of the message exchange
		@param Actor receiver : The receiver of this message exchange
		@param MessageType messageType : The type of the message this message exchanges should be of. If none is given a new message type is created.
		@return MessageExchange :
		@author
		"""
		if(not isinstance(sender, ActiveProcessComponent)):
			raise Exception("'Sender' must be of type Actor!")	
		if(not isinstance(receiver, ActiveProcessComponent)):
			raise Exception("'Receiver' must be of type Actor!")	
		if((messageType is not None) and (not isinstance(messageType, MessageType))):
			raise Exception("'MessageType' must be of type MessageType!")	
		if(messageType is None):
			messageType = MessageType(self.modelManager)
		newExchange = MessageExchange(self.modelManager, sender = sender, receiver = receiver, messageType = messageType)
		self.hasModelComponent.append(newExchange)
		return newExchange

	def removeMessageExchange(self, messageExchange):
		"""
		 Invers function of addMessageExchange - Removes a message exchange from this
		 layer.

		@param MessageExchange messageExchange : The messageExchange to remove from this layer
		@return  :
		@author
		"""
		if(not isinstance(messageExchange, MessageExchange)):
			raise Exception("'MessageExchange' must be of type MessageExchange!")	
		self.hasModelComponent.remove(messageExchange)

	def addBehavior(self):
		"""
		 Function to add a new Behavior to this layer and to directly assign it to an
		 actor, if needed.

		@param Actor asignToActor : The actor that should have this behavior.
		@return Behavior :
		@author
		"""
		newBehavior = Behavior(self.modelManager)
		self.hasModelComponent.append(newBehavior)
		return newBehavior

	def removeBehavior(self, behaviorToRemove):
		"""
		 Invers function of addBehavior. Removes a behavior from this layer and (if it
		 was assigned to one) also from the actor.

		@param Behavior behaviorToRemove : The behavior that should be removed from this layer.
		@return  :
		@author
		"""
		if(not isinstance(behaviorToRemove, Behavior)):
			raise Exception("BehaviorToRemove must be of type Behavior!")
		for a in self.activeComponents:
			if(isinstance(a, Actor) and (a.hasBehavior is behaviorToRemove)):
				a.hasBehavior = None
				print("WARNING! Behavior was removed that belonged to a subject!")
		self.hasModelComponent.remove(behaviorToRemove)
		
	def getBoundingBox2D(self):
		#Helper variables
		maxX = float("-inf")
		maxY = float("-inf")
		minX = float("inf")
		minY = float("inf")
		#Now iterate over all active process components
		for active in self.activeProcessComponents:
			if(hasattr(active, "hasAbstractVisualRepresentation")):
				point = active.hasAbstractVisualRepresentation.getPoint2D()
				#Max tests
				if(maxX < point[0]):
					maxX = point[0]
				if(maxY < point[1]):
					maxY = point[1]
				#Min tests
				if(minX > point[0]):
					minX = point[0]
				if(minY > point[1]):
					minY = point[1]
		#inf tests
		if(math.isinf(maxX)):
			maxX = 0
			minX = 0
		if(math.isinf(maxY)):
			maxY = 0
			minY = 0
		return [[minX, minY], [maxX, maxY]]
					
	def getBoundingBox3D(self):
		#Helper variables
		maxX = float("-inf")
		maxY = float("-inf")
		maxZ = float("-inf")
		minX = float("inf")
		minY = float("inf")
		minZ = float("inf")
		#Now iterate over all active process components
		for active in self.activeProcessComponents:
			if(hasattr(active, "hasAbstractVisualRepresentation")):
				point = active.hasAbstractVisualRepresentation.getPoint3D()
				#Max tests
				if(maxX < point[0]):
					maxX = point[0]
				if(maxY < point[1]):
					maxY = point[1]
				if(maxZ < point[2]):
					maxZ = point[2]
				#Min tests
				if(minX > point[0]):
					minX = point[0]
				if(minY > point[1]):
					minY = point[1]
				if(minZ > point[2]):
					minZ = point[2]
		#inf tests
		if(math.isinf(maxX)):
			maxX = 0
			minX = 0
		if(math.isinf(maxY)):
			maxY = 0
			minY = 0
		if(math.isinf(maxZ)):
			maxZ = 0
			minZ = 0
		return [[minX, minY, minZ], [maxX, maxY, maxZ]]



