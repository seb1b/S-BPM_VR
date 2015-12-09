import os.path
import RDF
import weakref
from AttributeMapper import *
from ClassMapper import *
from Resource import *
from AttributeMultiplicity import *


class ModelManager(object):
	

	"""
	 Class to manage the process model. Is responsible for holding the line to the
	 rdfs ontology and (de)serializing all the stuff.

	:version: 2012-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The base uri where models that are locally stored should be appended to.

	DEFAULT_BASE_URI  (public)

	 The possible extensions like *.owl or *.xml for the file format

	POSSIBLE_EXTENSIONS  (public)

	 The default extension for saving and reading from file

	DEFAULT_EXTENSION  (public)

	 Representing the file path the pass process model was loaded from or last saved
	 to. If model manager was initialized using the default constructor this
	 attribute is empty. (Is a property - only get allowed.)

	filePath  (public)



	_filePath  (private)

	 The name of this file (the filename without extension). Is a property - only get
	 is allowed.

	name  (public)

	 Reference to the pass process model this manager is responsible for. Property -
	 Only get is allowed

	model  (public)



	_model  (private)

	 Link to the attribute mapper. For further information see documentation of class
	 AttributeMapper. Is a property - Only get is allowed.

	attrMapper  (public)



	_attrMapper  (private)

	 Instance to the class mapper of this manager. See ClassMapper documentation for
	 further information. Is a property - onyl get is allowed.

	classMapper  (public)



	_classMapper  (private)

	 Containing all resources that are attachted to this controller and should be
	 serialized when storing.

	_resources  (private)

	 The array of listener functions to be called whenever a value of a
	 PASSProcessModelElement changes.

	_changeListeners  (private)

	"""
	
	#ToDo: Complete list
	POSSIBLE_EXTENSIONS = [".owl", ".nt"]
	DEFAULT_EXTENSION = ".owl"
	DEFAULT_BASE_URI = "http://www.imi.kit.edu/passModelInstances/"

	def __init__(self, filePath = None):
		"""
		 Constructor - Reads the pass process model from the file. The filePath can
		 either be a local path or an absolute path in the internet, specifing the uri
		 where the model to load is defined. In the current Implementation the namespace
		 is cut off for certain namespaces and a local search is performed!
		 If no filePath is given a new model is created

		@param string filePath : (Absolute) path to the file to read the pass process model from
		@return  :
		@author
		"""
		self._resources = []
		self._classMapper = ClassMapper()
		self._attrMapper = AttributeMapper()
		self._filePath = None
		self._changeListeners = []
		self._currentlyLoading = False
		self._model = None
		#Now decide whether to load a model or create a new one
		if(filePath is None):
			#Import here because is only needed here (to prevent loops)
			from PASSProcessModel import *
			from BaseLayer import *
			self._model = PASSProcessModel(self)
			layer = BaseLayer(self)
			self._model.hasModelComponent.append(layer)
		else:
			#Load a model
			#ToDo: Find model in the loaded file
			#Check the type of the path and whether the path exists
			hasWriteAccess = os.access(os.path.dirname(filePath), os.W_OK)
			isString = isinstance(filePath, str)
			validExtension = os.path.splitext(filePath)[-1] in ModelManager.POSSIBLE_EXTENSIONS
			#Raise exceptions if above restrictions are not valid
			if(not isString):
				raise Exception("Parameter \"filePath\" must be of type str!")
			elif(not hasWriteAccess):
				raise Exception("Parameter \"filePath\" must point to a valid file address!")
			elif(not validExtension):
				raise Exception("Parameter \"filePath\" must have a valid extension!")
			else:
				#ToDo: Pack all this functionality into subfunctions
				
				#Set the variable to not fire change events currently
				self._currentlyLoading = True
				
				#Set the file path
				self._filePath = filePath
				#========= Now load the model =========
				storage = RDF.MemoryStorage()
				if storage is None:
					raise Exception("Failed to create storage for reading from the file!")
				model = RDF.Model(storage)
				if(model is None):
					raise Exception("Faile to create model for reading from the file!")
				#========= Now start parsing =========
				#Select parser by file type
				if(os.path.splitext(filePath)[-1] == ".nt"):
					parser = RDF.NTriplesParser()
				else:
					parser = RDF.Parser("raptor")
				#Read from file
				uri = RDF.Uri(string="file:" + filePath)
				for statement in parser.parse_as_stream(uri, uri):
					model.add_statement(statement)
				#Get all class types of each subject node by rdf:type and store them all in the classTypes dict
				typeQuery = RDF.Query("SELECT ?s ?o WHERE { ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o }")
				classTypes = {}
				for result in typeQuery.execute(model):
					#Check the type of s
					if(result["s"].is_resource()):
						subjectString = str(result["s"].uri)
					elif(result["s"].is_blank()):
						subjectString = str(result["s"].blank_identifier)
					else:
						raise Exception("Received a RDFNode that is a subject and neither of type normal nor blank!")
					#Now insert it into dict if not and append type
					if (not (subjectString in classTypes)):
						classTypes[subjectString] = []
					classTypes[subjectString].append(str(result["o"]))
				#Now generate the instances depending on their rdf:type links stored in the classTypes dict
				ownClasses = {}
				for (key, value) in list(classTypes.items()):
					className = self._classMapper.getClassName(value)
					#Do a dynamic import of the missing class
					exec(str("from " + className + " import *"), globals())
					classConstructor = globals()[className]
					if(key.startswith("http://")):
						newClass = classConstructor(self, uri = key)
					else:
						newClass = classConstructor(self, isBlank = True, blankNodeId = key)
					#Set the PASSProcessModel-Reference
					if(className == "PASSProcessModel"):
						if(self._model is not None):
							print("WARNING! Two Process Models were read from the file while only one can be instanciated!")
						self._model = newClass
					ownClasses[key] = newClass
				#Go through all triples with the component id and perform them before the others to set the right ids on the PASSProcessModelElements
				tripleQuery = RDF.Query("SELECT ?s ?o WHERE { ?s <http://www.imi.kit.edu/abstract-pass-ont#hasModelComponentID> ?o }")
				for result in tripleQuery.execute(model):
					self._convertTriples(result, ownClasses, "http://www.imi.kit.edu/abstract-pass-ont#hasModelComponentID")
				#Go through all triples and include them - Eventually generate additional class instances or literals if this object has not been created yet
				tripleQuery = RDF.Query("SELECT ?s ?a ?o WHERE { ?s ?a ?o }")
				for result in tripleQuery.execute(model):
					self._convertTriples(result, ownClasses)
				#Finished loading
				self._currentlyLoading = False
				#ToDo: Validity check at the end

	def _convertTriples(self, result, ownClasses, alternativeAttrUri = None):
		#Rest subject string
		subjectString = None
		
		#Attribute is always a node with uris => Automatically get the attribute name
		if(("a" in result) and (result["a"] is not None)):
			attrName = self.attrMapper.getAttributeName(str(result["a"].uri))
		else:
			attrName = self.attrMapper.getAttributeName(alternativeAttrUri)
		
		#Now check of what type the subject is
		if(result["s"].is_resource()):
			subjectString = str(result["s"].uri)
		elif(result["s"].is_blank()):
			subjectString = str(result["s"].blank_identifier)
		else:
			raise Exception("Received a RDFNode that is a subject and neither of type normal nor blank!")
		
		#Insert the subject if not already in class list
		if (not (subjectString in ownClasses)):
			#Do a dynamic import of the missing class
			exec(str("from " + ClassMapper.DEFAULT_CLASS + " import *"))
			classConstructor = globals()[ClassMapper.DEFAULT_CLASS]
			if(subjectString.startswith("http://")):
				ownClasses[subjectString] = classConstructor(self, uri = subjectString)
			else:
				ownClasses[subjectString] = classConstructor(self, isBlank = True, blankNodeId = subjectString)
		#Get the subject class
		subjectClass = ownClasses[subjectString]
		
		#Now check of what type the object is
		objectIsLiteral = False
		if(result["o"].is_resource()):
			objectString = str(result["o"].uri)
		elif(result["o"].is_blank()):
			objectString = str(result["o"].blank_identifier)
		else:
			#It is a literal
			objectIsLiteral = True
			literalValues = result["o"].literal_value
			if(literalValues["datatype"] is not None):
				dt = str(literalValues["datatype"])
			else:
				dt = None
			objectClass = Resource.castLiteralToType(literalValues["string"], dt)
		#No go on depending the object type
		if(not objectIsLiteral):
			#Insert the object if not already in class list
			if (not (objectString in ownClasses)):
				#Do a dynamic import of the missing class
				exec(str("from " + ClassMapper.DEFAULT_CLASS + " import *"))
				classConstructor = globals()[ClassMapper.DEFAULT_CLASS]
				if(objectString.startswith("http://")):
					ownClasses[objectString] = classConstructor(self, uri = objectString)
				else:
					ownClasses[objectString] = classConstructor(self, isBlank = True, blankNodeId = objectString)
			#Get the object class
			objectClass = ownClasses[objectString]
		
		#Now take the classes and reference the object in the subjects attribute depending on the multiplicity
		multiplicity = subjectClass.getAttrMultiplicity(attrName)
		if(multiplicity == AttributeMultiplicity.UNKNOWN):
			if (not hasattr(subjectClass, attrName)):
				setattr(subjectClass, attrName, [])
			getattr(subjectClass, attrName).append(objectClass)
		elif(multiplicity == AttributeMultiplicity.UNIQUE):
			setattr(subjectClass, attrName, objectClass)
		else:
			raise Exception("Unknown attribute multiplicity set to attribute " + attrName)

	@property
	def model(self):
		return self._model

	@property
	def filePath(self):
		return self._filePath

	@property
	def attrMapper(self):
		return self._attrMapper

	@property
	def classMapper(self):
		return self._classMapper

	@property
	def name(self):
		if(self._filePath is not None):
			return os.path.basename(self._filePath)
		else:
			return "Unnamed Model"
			
	@property
	def resources(self):
		#Clean up list of dead references
		self._resources[:] = [x for x in self._resources if not ((type(x) is weakref.ref) and (x() is None))]
		
		result = []
		for r in self._resources:
			if(type(r) is weakref.ref):
				#It is a weak reference
				o = r()
				if(o is not None):
					#The object is still alive, append it
					result.append(o)
			else:
				result.append(r)
		
		return result

	def save(self):
		"""
		 Saves the pass process modell to a file using the given file path. If no file
		 path is given, an error is thrown.

		@return  :
		@author
		"""
		if(self._filePath is not None):
			#Create the needed datatypes (storage and model) for rdf
			storage = RDF.MemoryStorage()
			if(storage is None):
				raise Exception("Failed to create storage for saving the model!")
			#The model
			model = RDF.Model(storage)
			if(model is None):
				raise Exception("Failed to creat a new RDF model for saving!")
			
			#Now request all statements from the resources and add them to the model
			for resource in self.resources:
				for statement in resource.serialize():
					model.add_statement(statement)
			
			#Now serialize to file
			#Get right type of serializer depending on the ending
			fileExtension = os.path.splitext(self._filePath)[-1]
			name = None
			mimeType = None
			if(fileExtension == ".nt"):
				name = "ntriples"
			else:
				#By default use the default serialize
				pass
			serializer = RDF.Serializer(name=name, mime_type=mimeType)
			#ToDo: Maybe use namespaces?
			serializer.serialize_model_to_file(self.filePath, model)
			print(("INFO! Saving model to file \"" + self.filePath + "\" was successfull!"))
		else:
			#No file path is currently set
			raise Exception("Cannot save a file directly that has never been saved before. Use \"saveAs(self, filePath)\" instead ")


	def saveAs(self, filePath):
		"""
		 Saves the current model to the given filepath and/or to the given type.

		@param string filePath : The (absolute) path to the file where this model should be stored. The extension must fit to one of the possible extensions. Serialization to the right format is done automatically.
		@return  :
		@author
		"""
		#Check the type of the path and whether the path exists
		hasWriteAccess = os.access(os.path.dirname(filePath), os.W_OK)
		isString = isinstance(filePath, str)
		validExtension = os.path.splitext(filePath)[-1] in ModelManager.POSSIBLE_EXTENSIONS
		#Raise exceptions if above restrictions are not valid
		if(not isString):
			raise Exception("Parameter \"filePath\" must be of type str!")
		elif(not hasWriteAccess):
			raise Exception("Parameter \"filePath\" must point to a valid file address!")
		elif(not validExtension):
			raise Exception("Parameter \"filePath\" must have a valid extension!")
		else:
			#Otherwise set the filepath and save
			self._filePath = filePath
			self.save()

	def registerResource(self, resource):
		"""
		 The model manager only takes care of all resources that are registered to it.
		 E.g. the model manager only saves the resources that are registered.

		@param Resource resource : The resource that should be registered so that the model manager can take care of it.
		@return  :
		@author
		"""
		if(isinstance(resource, Resource)):
			if(type(resource) is not Resource):
				#It is a subclass of resource that is managed by this model. Only keep it alive it is needed elsewhere
				r = weakref.ref(resource)
				self._resources.append(r)
			else:
				#It is a normal Resource class that should be appended
				self._resources.append(resource)
		else:
			raise Exception("Only instances of type \"Resource\" can be registered at the ModelManager!")

	def releaseResource(self, resource):
		"""
		 Invers function of registerResource.

		@param Resource resource : The resource that should be released from the model manager.
		@return  :
		@author
		"""
		if(isinstance(resource, Resource)):
			#ToDo: Check if that works...
			#Check whether resource is stored as a weak ref
			for value in self._resources:
				if((type(value) is weakref.ref) and ((value() is resource))):
					isWeakRef = True
					break
				elif(value is resource):
					isWeakRef = False
					break
			
			#Now delete it depending on the type
			if(not isWeakRef):
				self._resources.remove(resource)
			else:
				self._resources[:] = [x for x in self._resources if not ((type(x) is weakref.ref) and (x() is resource))]
		else:
			raise Exception("Only instances of type \"Resource\" can be registered at the ModelManager!")

	def getBaseUri(self):
		"""
		 Function to return the base uri this file represents. Takes the DEFAULT_BASE_URI
		 attribute and appends the filename to it. All other process model elements
		 should use the return value of this uri to create their uri by appending "#" +
		 componentId.

		@return string :
		@author
		"""
		if(self._filePath is None):
			raise Exception("Cannot return a base uri because this model is currently not saved to any file!")
		else:
			return (ModelManager.DEFAULT_BASE_URI + self.name)

	def addChangeListener(self, listenerFunction):
		"""
		 Adds a change listener to this model. Whenever a PASSProcessModelElement
		 changes, the given function is called.

		@param undef listenerFunction : A function with exactly one parameter representing the PASSProcessModelElement that has changed.
		@return  :
		@author
		"""
		self._changeListeners.append(listenerFunction)

	def removeChangeListener(self, listenerFunction):
		"""
		 Removes a already registered listener from this model.

		@param undef listenerFunction : The function to remove from listening.
		@return  :
		@author
		"""
		self._changeListeners.remove(listenerFunction)

	def fireChangeEvent(self, changedElement):
		"""
		 Fires a change event to all registered change listeners.

		@param PASSProcessModelElement changedElement : The element that has changed.
		@return  :
		@author
		"""
		#Only fire if we are not loading anything currently
		if(not self._currentlyLoading):
			for func in self._changeListeners:
				func(changedElement)
			
	def getParent(self, childElement, classType = None, recursionDepth = 5):
		#Iterate over all avaiable resources
		for resource in self.resources:
			if(resource is not None):
					#Check if it is in the child resource
					if (childElement in resource.childResources):
						#Check if resource if of right type
						if((classType is None) or isinstance(resource, classType)):
							return resource
						elif(recursionDepth > 0):
							#Otherwise search for the parent of this resource to receive the variable
							self.getParent(resource, classType, recursionDepth-1)
		#We reached here we are not able to find anything
		return None

