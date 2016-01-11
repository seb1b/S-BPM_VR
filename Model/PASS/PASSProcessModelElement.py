from Resource import *
from AbstractVisualRepresentation import *
from AttributeMultiplicity import *
from Tools import *
from MetaContent import *
from ListenerList import *

class PASSProcessModelElement(Resource):

	"""
	This class is the superclass for all Elements in a PASS process. It is responsible for their
	representation, their meta data and their linking.

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 Is a property so in fact returns the type of PASSProcessElement-subclass as a
	 string. Uses ClassMapper and rdfs:type property to determine own class type or
	 python's instance of.

	classType  (public)

	 See definition of hasComponentID in ontologie

	hasComponentID  (public)

	 Property - onyl get is allowed here. Returns the parent instance of this object.
	 The parent instance is the instance that is the next upper class in the visual
	 hierachy. Might be null!

	parent  (public)

	 The label should be uses to display itself to the outside. Might contain
	 different languages. For all ActiveProcessComponents, MessageTypes and all
	 states this label is also the words displayed on it.

	label  (public)

	 Represents all meta content this element has. The array contains the different
	 MetaContent instances with their keys and values. A key isn't secured to be
	 unique. Better use the getMetaContent or setMetaContant function.

	hasMetaContent  (public)

	 Links to a Visual Reperesentation object. See documentation of visual
	 representation for further reference.

	hasVisualRepresentation  (public)

	 Reference to an abstract visual representation that only shows the positions of
	 the elements. See AbstractVisualRepresentation for further reference.

	hasAbstractVisualRepresentation  (public)

	"""
	
	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor including the parent element

		@param ModelManager manger : The parent element (if one exists).
		@param string uri :
		@param bool isBlank :
		@param string blankNodeId :
		@param PASSProcessModelElement : The hierarchical parent of this process element.
		@return  :
		@author
		"""
		
		#Call super constructor
		Resource.__init__(self, manager, uri, isBlank, blankNodeId)
		
		#Generate the component id and the empty array for the meta content
		self.hasComponentID = randomXMLName()
		self.hasMetaContent = ListenerList([], self)
		self.hasAbstractVisualRepresentation = None
		self.hasVisualRepresentation = None
		self.label = ListenerList([], self)
		
	@property
	def uri(self):
		#ToDo: Nachher rausnehmen
		return self.modelManager.getBaseUri() + "#" + type(self).__name__ + "-" + self.hasComponentID
		
	@uri.setter
	def uri(self, value):
		print("WARNING! URI cannot be set for a PASSProcessModelElement!")
		
	@property
	def classType(self):
		type(self).__name__
	
	@property
	def parent(self):
		return self.getParent()
		
	def getAttrMultiplicity(self, attributeName):
		if(attributeName == "hasComponentID"):
			return AttributeMultiplicity.UNIQUE
		if(attributeName == "hasAbstractVisualRepresentation"):
			return AttributeMultiplicity.UNIQUE
		else:
			return Resource.getAttrMultiplicity(self, attributeName)

	def setMetaContent(self, key, value, override = True):
		"""
		 Sets a new meta content object or updates a given one.

		@param string key : The key of the meta content to set. If the key exists the override parameter specifies what to do. Otherwise a new MetaContent instance will be created and appended to hasMetaContent.
		@param undef value : The value of the meta content. Can be of any type that is specified in XMLLiteral.
		@param bool override : Determines if the current value should be overriden by the given one, if a MetaContent instance with the given key already exists (default behavior). If set to false a new isntance will be created and two meta content objects will exist now.
		@return  :
		@author
		"""
		for element in self.hasMetaContent:
			if(element.hasKey == key):
				if (override):
					element.hasValue = value
					#Now terminate
					return
				else:
					#Otherwise stop iterating, because we for sure must create a new one
					break
		#If not already terminated, we have to insert a new one
		self.hasMetaContent.append(MetaContent(self.modelManager, key, value))
		#No need to fire a change event beacause it is automatically fired by the newly created or the changed one.
				

	def getMetaContent(self, key):
		"""
		 Returns an array of XMLLiterals containing all values that belong to MetaContent
		 instances with this key. As Meta Content keys do not need to be unique, but
		 should be, the array normally has the size 1.

		@param string key : The key for which the MetaContent should be returned.
		@return  :
		@author
		"""
		results = []
		
		#Iterate over all meta content and add it to the list
		for value in self.hasMetaContent:
			if(value.hasKey == key):
				results.append(value.hasValue)
		
		return results
		
	def getMetaKeys(self):
		"""
		Function that returns all registered meta content keys.
		
		@return  :
		@author
		"""
		results = []
		
		for value in self.hasMetaContent:
			if(not value.hasKey in results):
				results.append(value.hasKey)
		
		return results
		
	def removeMetaContent(self, key, onlyFirst = False):
		"""
		Function that removes all registered meta content with that key.
		
		@return  :
		@author
		"""
		
		for content in self.hasMetaContent:
			if(content.hasKey == key):
				self.hasMetaContent.remove(content)
				#Stop deleting if we only want to delete the first occurence
				if(onlyFirst):
					break
		#Now fire a change event because we removed a meta content - Important: This time it is fired by the element itself
		self.fireChangeEvent()

		
	def getParent(self, classType = None, recursionDepth = 5):
		"""
		Returns the parent of this PASSProcessModelElement by using ModelManager.getParent(...). Refer to this function for further information.
		
		@return  :
		@author
		"""
		
		return self.modelManager.getParent(self, classType, recursionDepth)



