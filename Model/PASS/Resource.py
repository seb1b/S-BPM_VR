import RDF

from ListenerList import *

class Resource(object):

	"""
	Resource is a class to represent the idea of a rdf resource in our object model. It is superclass
	for all model classes that contain persitent data.

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The uri for this resource - is a property, thus the input is checked against a
	 start with "http://". Can only be set if this resource is not blank.

	uri  (public)

	 Reference to the model manager
	 Is a property - only get is allowed

	modelManager  (public)



	_modelManager  (private)



	_uri  (private)



	_blankIdentifier  (private)

	 Property for _blankIdentifier - Only get is allowed!

	blankIdentifier  (public)

	 Property - Only get is allowed here

	isBlank  (public)

	"""

	def __init__(self, manager, uri = None, isBlank = False, blankNodeId = None):
		"""
		 Constructor - defines whether this instance represents a blank node or not. -
		 This cannot be changed later on!

		@param ModelManager manager : The manager that is responsible for this resource.
		@param string uri : The uri this Resource should represent.
		@param bool isBlank : Boolean to dertermine whether the node is a blank node
		@param string blankNodeId : The identifier for the blank node if this resource is a blank node.
		@return  :
		@author
		"""
		#By default a resource does not fire change events
		self._fireChangeEvents = False
		
		#Import it just here because it is not needed before
		from ModelManager import *
		#Check the type of the manager object
		if(not isinstance(manager, ModelManager)):
			raise Exception("Paramter \"manager\" has to be of type ModelManager!")
		self._modelManager = manager
		self._modelManager.registerResource(self)
		self.type = ListenerList([], self)
		#Now check whether to create a normal or a blank resource
		self._isBlank = isBlank
		if(not self._isBlank):
			#Create a normal resource
			if(uri is not None):
				self.uri = uri
			else:
				self._uri = None
		else:
			#Create a blank resource
			if(blankNodeId is not None):
				self._blankIdentifier = blankNodeId
			else:
				raise Exception("If a Resource is defined as a blank node it must also define the \"blankNodeId\" parameter")
		
	@property
	def modelManager(self):
		return self._modelManager
		
	@property
	def uri(self):
		return self._uri

	@uri.setter
	def uri(self, value):
		if(self.isBlank):
			raise Exception("Cannot set a URI to a blank resource!")
		elif((not isinstance(value, str)) or (not value.startswith("http://"))):
			raise Exception("The uri must be of type str and start with \"http://\" !")
		else:
			self._uri = value
	
	@property
	def isBlank(self):
		return self._isBlank
		
	@property
	def blankIdentifier(self):
		return self._blankIdentifier

	def serialize(self):
		"""
		 Serializes the given resource to triple statements from the Redland RDF library.
		 This is done by using the model manager and its attribute wrapper.

		@return  :
		@author
		"""
		#First set yourself the class type if it is not Resource or already set
		if(type(self).__name__ != "Resource"):
			if(not hasattr(self, "type")):
				self.type = ListenerList([], self)
			ownClassUri = self.modelManager.classMapper.getClassResource(type(self).__name__)
			#Does not work because they are of type resource
			found = False
			for r in self.type:
				try:
					if(r.uri == ownClassUri):
						found = True
						break
				except:
					#Do nothing
					pass
			if(not found):
				#Add your own class type
				self.type.append(Resource(self.modelManager, uri = ownClassUri))
		
		#Initialize an array to store the results in
		results = []
		
		#Iterate over all variables and store the values
		for (key, value) in list(self.__dict__.items()):
			#Only store the values of "public" variables
			if(not key.startswith("_")):
				#Subject and attribute are always the of normal type resource
				if(not self.isBlank):
					subjectNode = RDF.Uri(self.uri)
				else:
					subjectNode = RDF.Node(blank=self.blankIdentifier)
				attributeNode = RDF.Uri(self.modelManager.attrMapper.getAttributeUri(key))
				#Object node might be a list or a skalar
				if(value is None):
					#Do nothing
					pass
				elif(isinstance(value, list)):
					for subValue in value:
						results.append(self._generateStatement(subjectNode, attributeNode, subValue))
				else:
					results.append(Resource._generateStatement(subjectNode, attributeNode, value))
		
		#Now return the results
		return results

	def getAttrMultiplicity(self, attributeName):
		"""
		 Function to determine what attribute multiplicity should be used for a special
		 attribute. Uses _attrMultiplicity variable for that.

		@param string attributeName : The name of the attribute to obtain the multiplicity from.
		@return AttributeMultiplicity :
		@author
		"""
		#Import it just here because it is not needed before
		from AttributeMultiplicity import *
		return AttributeMultiplicity.UNKNOWN

	def isValid(self):
		"""
		 Checks whether the element is in a valid state (all required variables are set
		 and of right type).

		@return bool :
		@author
		"""
		#A resource is always valid even if no uri has been set
		return True

	@staticmethod
	def castLiteralToType(literalString, datatypeUri):
		#Possible extension: Take care of language tags
		"""
		 Cast a given literal to a python value using the specificed type uri. Currently
		 implemented are the XMLSchema-Types double, float, int, string, boolean.

		@param string literalString : The literal containg the specific value to cast to a python type.
		@param string datatypeUri : The uri of the datatype the literal string is from.
		@return undef :
		@author
		"""
		#Import it just here because it is not needed before
		from PlainLiteral import *
		#Now check for type
		if(datatypeUri == "http://www.w3.org/2001/XMLSchema#int"):
			#Int
			return int(literalString.encode('utf-8'))
		elif(datatypeUri == "http://www.w3.org/2001/XMLSchema#long"):
			#Long
			return long(literalString.encode('utf-8'))
		elif((datatypeUri == "http://www.w3.org/2001/XMLSchema#double") or (datatypeUri == "http://www.w3.org/2001/XMLSchema#float")):
			#Double or float
			return float(literalString.encode('utf-8'))
		elif(datatypeUri == "http://www.w3.org/2001/XMLSchema#string"):
			return str(literalString.encode('utf-8'))
		elif(datatypeUri == "http://www.w3.org/2001/XMLSchema#boolean"):
			return bool(literalString.encode('utf-8'))
		else:
			return PlainLiteral(literalString.encode('utf-8'))

	@staticmethod
	def castTypeToLiteral(pythonVar):
		#Possible extension: Take care of language tags
		"""
		 Converts a python variable to a RDF literal. The return value is an array of
		 type [literalString, datatypeUri].  Currently implemented are the
		 XMLSchema-Types double, float, int, string, boolean.

		@param undef pythonVar : The variable that should be typed to a literal including the literals string and literal uri.
		@return string[] :
		@author
		"""
		#The resulting array (first index = string representation, second index = uri to xml schema type)
		result = []
		
		#Import it just here because it is not needed before
		from PlainLiteral import *
		
		#Check of which type the variable is and return the information
		if(isinstance(pythonVar, int)):
			#Int
			result.append(str(pythonVar))
			result.append("http://www.w3.org/2001/XMLSchema#int")
		elif(isinstance(pythonVar, long)):
			#Long
			result.append(str(pythonVar))
			result.append("http://www.w3.org/2001/XMLSchema#long")
		elif(isinstance(pythonVar, float)):
			#Float
			result.append(str(pythonVar))
			result.append("http://www.w3.org/2001/XMLSchema#double")
		elif(isinstance(pythonVar, str)):
			#String
			result.append(pythonVar)
			result.append("http://www.w3.org/2001/XMLSchema#string")
		elif(isinstance(pythonVar, bool)):
			#Boolean
			result.append(str(pythonVar).lower())
			result.append("http://www.w3.org/2001/XMLSchema#boolean")
		elif(isinstance(pythonVar, PlainLiteral)):
			#Plain literal
			result.append(str(pythonVar.content.encode('utf-8')))
			result.append(None)
		else:
			raise Exception("Unknown literal \"" + type(pythonVar).__name__ + "\" type that cannot be deserialized!")
			
		#Retrun the result
		return result
			

	@staticmethod
	def _generateStatement(subjectNode, attributeNode, objectValue):
		"""
		 Internal function to generate a statement from its own attributes!

		@param RDFNode subjectNode : The subject node for this statement.
		@param RDFNode attributeNode : The attribute node for this statement.
		@param undef object : The object where the type should be determined!
		@return Statement :
		@author
		"""
		#Object node might be another resource or a literal
		if(isinstance(objectValue, Resource)):
			if(objectValue.isBlank):
				#It is a blank resource
				objectNode = RDF.Node(blank = objectValue.blankIdentifier)
			else:
				#It is a normal resource with uri
				objectNode = RDF.Uri(objectValue.uri)
		else:
			#It is a literal - Get info about it
			literalValues = Resource.castTypeToLiteral(objectValue)
			#Check what the datatype is (might be None for plain literals)
			if(literalValues[1] is not None):
				dt = RDF.Uri(literalValues[1])
				objectNode = RDF.Node(literal = literalValues[0], datatype = dt)
			else:
				objectNode = RDF.Node(literal = literalValues[0])
			
		#Now return the newly created statement
		return RDF.Statement(subjectNode, attributeNode, objectNode)
		
	def __setattr__(self, name, value):
		"""
		 Override to fire change events

		@param undef name : Override
		@param undef value : Override
		@return undef :
		@author
		"""
		#Fire the event change event if try to set any variable (Except the one setting whether we should fire the change events or not!)
		if(name != "_fireChangeEvents"):
			object.__setattr__(self, name, value)
			self.fireChangeEvent()
		else:
			object.__setattr__(self, name, value)
		
	def fireChangeEvent(self):
		if(self._fireChangeEvents):
			self.modelManager.fireChangeEvent(self)
			
	@property
	def childResources(self):
		#Result array
		results = []
		
		#Iterate over all variables and store the values if they are of type Resource
		for (key, value) in list(self.__dict__.items()):
			#Only store the values of "public" variables
			if(not key.startswith("_")):
				if(isinstance(value, list)):
					for subValue in value:
						if(isinstance(subValue, Resource)):
							results.append(subValue)
				elif(isinstance(value, Resource)):
					results.append(value)
					
		return results
		
	def getParent(self, classType = None, recursionDepth = 1):
		"""
		Returns the parent of this Resource by using ModelManager.getParent(...). Refer to this function for further information.
		
		@return  :
		@author
		"""
		
		return self.modelManager.getParent(self, classType, recursionDepth)



