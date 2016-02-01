from PASSProcessModelElement import *
from State import *
from StandardTransition import *
from FunctionState import *
from ReceiveTransition import *
from ReceiveState import *
from MessageExchange import *
from SendTransition import *
from SendState import *
from TransitionEdge import *
from ListenerList import *
from ActiveProcessComponent import *

import math

class Behavior(PASSProcessModelElement):

	"""
	A behavior is a state diagram that defines how an subject reacts when it receives or sends messages.

	:version: 2015-12-07
	:author: Kai Hartung & Lukas Block
	"""

	""" ATTRIBUTES

	 All edges of this behavior description. Variable is defined by ontology.

	hasEdge  (public)

	 All states of this behavior description. Variable is defined by ontology.

	hasState  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
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
		self.hasEdge = ListenerList([], self, "hasEdge")
		self.hasState = ListenerList([], self, "hasState")
		
		self._fireChangeEvents = True
		self.fireChangeEvent()

	def addFunctionState(self):
		"""
		 Adds a state of type function to this Behavior.

		@return  :
		@author
		"""
		newFunc = FunctionState(self.modelManager)
		self.hasState.append(newFunc)
		#Check if we should set the initial state
		if(len(self.hasState) == 1):
			self.setInitialState(newFunc)
		return newFunc

	def addReceiveState(self):
		"""
		 Adds a state of type receive to this Behavior.

		@return  :
		@author
		"""
		newS = ReceiveState(self.modelManager)
		self.hasState.append(newS)
		#Check if we should set the initial state
		if(len(self.hasState) == 1):
			self.setInitialState(newS)
		return newS

	def addSendState(self):
		"""
		 Adds a state of type send to this Behavior.

		@return  :
		@author
		"""
		newS = SendState(self.modelManager)
		self.hasState.append(newS)
		#Check if we should set the initial state
		if(len(self.hasState) == 1):
			self.setInitialState(newS)
		return newS

	def removeState(self, state):
		"""
		 Removes a state from the current behavior.

		@param State state : The state to remove.
		@return  :
		@author
		"""
		if(not isinstance(state, State)):
			raise Exception("The state must be of type State!")
		#Delete incident edges
		self.hasEdge[:] = [t for t in self.hasEdge if not ((t.hasSourceState is state) or (t.hasTargetState is state))]
		#Delete state
		self.hasState.remove(state)
		#Check if it was the initial state - if yes set another initial state if there are other states
		if(state.isInitialState and (len(self.hasState) > 0)):
			self.setInitialState(self.hasState[0])

	def addStandardTransition(self, from_, to):
		"""
		 Adds a standard transtition to the behavior.

		@param FunctionState from : The function state the transition should start at.
		@param State to : The target state of the transition
		@return StandardTransition :
		@author
		"""
		if(not isinstance(from_, FunctionState)):
			raise Exception("'From' must be of type FunctionState!")
		if(not isinstance(to, State)):
			raise Exception("'To' must be of type State!")
		newT = StandardTransition(self.modelManager, sourceState = from_, targetState = to)
		self.hasEdge.append(newT)
		return newT
		

	def addReceiveTransition(self, from_, to, refersTo):
		"""
		 Adds a receiving transition to the receive state.

		@param ReceiveState from : The start state of the transition
		@param State to : The target state of the transition.
		@param MessageExchange refersTo : The message exchange this transition should refer to.
		@return ReceiveTransition :
		@author
		"""
		if(not isinstance(from_, ReceiveState)):
			raise Exception("'From' must be of type ReceiveState!")
		if(not isinstance(to, State)):
			raise Exception("'To' must be of type State!")
		if(not isinstance(refersTo, MessageExchange)):
			raise Exception("'RefersTo' must be of type MessageExchange!")
		if(self.getParent(ActiveProcessComponent) != refersTo.receiver):
			raise Exception("The MessageExchange that should be done must be start at the subject assigned to this Behavior!")
		#Now create the transition
		newT = ReceiveTransition(self.modelManager, sourceState = from_, targetState = to, refersTo = refersTo)
		self.hasEdge.append(newT)
		return newT

	def addSendTransition(self, from_, to, refersTo):
		"""
		 Adds a sending transition between the given states.

		@param SendState from : The send state the transition starts at.
		@param State to : The target state of the transition.
		@param MessageExchange refersTo : The message exchange this transition should refer to.
		@return SendTransition :
		@author
		"""
		if(not isinstance(from_, SendState)):
			raise Exception("'From' must be of type ReceiveState!")
		if(not isinstance(to, State)):
			raise Exception("'To' must be of type State!")
		if(not isinstance(refersTo, MessageExchange)):
			raise Exception("'RefersTos' must be of type MessageExchange!")
		if(self.getParent(ActiveProcessComponent) != refersTo.sender):
			raise Exception("The MessageExchange that should be done must be start at the subject assigned to this Behavior!")
		#Now create the transition
		newT = SendTransition(self.modelManager, sourceState = from_, targetState = to, refersTo = refersTo)
		self.hasEdge.append(newT)
		return newT
		

	def removeTransition(self, transitionToRemove):
		"""
		 Removes an existing transition.

		@param TransitionEdge transitionToRemove : The transition edge to remove.
		@return  :
		@author
		"""
		if(not isinstance(transitionToRemove, TransitionEdge)):
			raise Exception("The transitionToRemove must be of type TransitionEdge!")
		self.hasEdge.remove(transitionToRemove)

	def setInitialState(self, state):
		"""
		 Sets the initail state (= the state where the behavior automata starts). Only
		 one state can be of type initial state. A state is set to an initial state by
		 manipulating the rdfs:type variable.

		@param State state : The state that should be used to start the actor's behavior.
		@return  :
		@author
		"""
		#Variable for the initial state
		initState = "http://www.purl.org/s-scm-ont#InitialState"
		for eState in self.hasState:
			if(eState.isInitialState):
				#Remove current inital state
				eState.type.remove(initState)
			if(eState is state):
				#Set to initial state
				eState.type.append(initState)
				
	def getBoundingBox2D(self):
		"""
		 Returns the bounding box of all state elements in their 2D coordinate system.

		@return  :
		@author
		"""
		#Helper variables
		maxX = float("-inf")
		maxY = float("-inf")
		minX = float("inf")
		minY = float("inf")
		#Now iterate over all active process components
		for active in (self.hasState + self.hasEdge):
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
		"""
		 Returns the bounding box of all state elements in their 3D coordinate system.

		@return  :
		@author
		"""
		#Helper variables
		maxX = float("-inf")
		maxY = float("-inf")
		maxZ = float("-inf")
		minX = float("inf")
		minY = float("inf")
		minZ = float("inf")
		#Now iterate over all active process components
		for active in (self.hasState + self.hasEdge):
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



