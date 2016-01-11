from collections import OrderedDict

class ClassMapper(object):

	"""
	The class mapper is responsible for mapping the rdf:type attribute to the python classes and vice versa.

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 The default class that is returned if no class is specified for a given
	 resource. (Value = "Resource")

	DEFAULT_CLASS  (public)



	_classMapping  (private)

	"""
	
	DEFAULT_CLASS = "Resource"

	def __init__(self):
		"""
		 Constructor

		@return  :
		@author
		"""
		#Class mapping is an ordered dictionary => Order sepcifies specificy => First one is most specific
		self._classMapping = OrderedDict()
		#Be carefull with the order: Might lead to mistakes
		self._classMapping["Resource"] = "http://www.w3.org/2000/01/rdf-schema#Class"
		
		self._classMapping["SendState"] = "http://www.imi.kit.edu/abstract-pass-ont#SendState"
		self._classMapping["FunctionState"] = "http://www.imi.kit.edu/abstract-pass-ont#FunctionState"
		self._classMapping["ReceiveState"] = "http://www.imi.kit.edu/abstract-pass-ont#ReceiveState"
		self._classMapping["State"] = "http://www.imi.kit.edu/abstract-pass-ont#State"
		
		self._classMapping["ReceiveTransition"] = "http://www.imi.kit.edu/abstract-pass-ont#ReceiveTransition"
		self._classMapping["SendTransition"] = "http://www.imi.kit.edu/abstract-pass-ont#SendTransition"
		self._classMapping["StandardTransition"] = "http://www.imi.kit.edu/abstract-pass-ont#StandardTransition"
		self._classMapping["CommunicationActTransition"] = "http://www.imi.kit.edu/abstract-pass-ont#CommunicationActTransition"
		
		self._classMapping["BaseLayer"] = "http://www.imi.kit.edu/abstract-pass-ont#BaseLayer"
		self._classMapping["Layer"] = "http://www.imi.kit.edu/abstract-pass-ont#Layer"
		
		self._classMapping["ExternalSubject"] = "http://www.imi.kit.edu/abstract-pass-ont#ExternalSubject"
		self._classMapping["InterfaceActor"] = "http://www.imi.kit.edu/abstract-pass-ont#InterfaceActor"
		self._classMapping["Subject"] = "http://www.imi.kit.edu/abstract-pass-ont#Subject"
		self._classMapping["Actor"] = "http://www.imi.kit.edu/abstract-pass-ont#Actor"
		self._classMapping["ActiveProcessComponent"] = "http://www.imi.kit.edu/abstract-pass-ont#ActiveProcessComponent"
		
		self._classMapping["Behavior"] = "http://www.imi.kit.edu/abstract-pass-ont#Behavior"
		self._classMapping["MessageType"] = "http://www.imi.kit.edu/abstract-pass-ont#MessageType"
		self._classMapping["MessageExchange"] = "http://www.imi.kit.edu/abstract-pass-ont#MessageExchange"
		self._classMapping["PASSProcessModel"] = "http://www.imi.kit.edu/abstract-pass-ont#PASSProcessModel"
		
		self._classMapping["PASSProcessModelElement"] = "http://www.imi.kit.edu/abstract-pass-ont#PASSProcessModelElement"
		self._classMapping["AbstractVisualRepresentation"] = "http://www.imi.kit.edu/abstract-pass-ont#AbstractVisualRepresentation"
		self._classMapping["VisualRepresentation"] = "http://www.imi.kit.edu/abstract-pass-ont#VisualRepresentation"
		self._classMapping["MetaContent"] = "http://www.imi.kit.edu/abstract-pass-ont#MetaContent"
		self._classMapping["Point2D"] = "http://www.imi.kit.edu/abstract-pass-ont#Point2D"
		self._classMapping["Point3D"] = "http://www.imi.kit.edu/abstract-pass-ont#Point3D"

	def getClassName(self, uris):
		"""
		 Returns the class name that should be associated with the given rdfs class which
		 is specified by the uri strings. The string with the highest specificy
		 (regarding this class model - not the ontology) is used to dertmine the class
		 name. If no class name is attachted to this uri array the DEFAULT_CLASS is
		 returned.

		@param string[] uris : The uri the for whicht the class name is requested
		@return string :
		@author
		"""
		#Iterate over the class mapping. As the uris are stored in the value they have to be checked against the given uris parameter
		#Class mapping is an ordered dictionary => Order sepcifies specificy
		for (key, value) in list(self._classMapping.items()):
			if(value in uris):
				return key
		#If nothing was found the Resource class is the right one
		return ClassMapper.DEFAULT_CLASS
		
	def getClassResource(self, className):
		#To prevent resources from having another type
		if(className == "Resource"):
			return None
		#Now check if we have a mapping in here
		if(className in self._classMapping):
			return self._classMapping[className]
		else:
			raise Exception("Given class name \"" + className + "\"is not associated with a uri!")



