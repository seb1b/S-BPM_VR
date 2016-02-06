from Resource import *

class AttributeMapper(object):

	"""
	 Class that is responsible to represent a mapping between the attribute names an
	 instance might have and their representation in rdfs (= their resource name).

	:version: 2015-12-04
	:author: Lukas Block
	"""

	""" ATTRIBUTES

	 Dictionary of resources mapping the attributes name as a string to the resource
	 representing the attribute.

	_attributeMapping  (private)

	"""

	def __init__(self):
		"""
		 Construcotr

		@return  :
		@author
		"""
		self._attributeMapping = {}
		self._attributeMapping["hasComponentID"] = "http://www.imi.kit.edu/abstract-pass-ont#hasModelComponentID"
		self._attributeMapping["hasAbstractVisualRepresentation"] = "http://www.imi.kit.edu/abstract-pass-ont#hasAbstractVisualRepresentation"
		self._attributeMapping["label"] = "http://www.w3.org/2000/01/rdf-schema#label"
		self._attributeMapping["type"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
		self._attributeMapping["hasVisualRepresentation"] = "http://www.imi.kit.edu/abstract-pass-ont#hasVisualRepresentation"
		self._attributeMapping["hasMetaContent"] = "http://www.imi.kit.edu/abstract-pass-ont#hasMetaContent"
		self._attributeMapping["hasMIMEType"] = "http://www.imi.kit.edu/abstract-pass-ont#hasMIMEType"
		self._attributeMapping["hasData"] = "http://www.imi.kit.edu/abstract-pass-ont#hasData"
		self._attributeMapping["hasRelativeSize"] = "http://www.imi.kit.edu/abstract-pass-ont#hasRelativeSize"
		self._attributeMapping["hasPoint2D"] = "http://www.imi.kit.edu/abstract-pass-ont#hasPoint2D"
		self._attributeMapping["hasPoint3D"] = "http://www.imi.kit.edu/abstract-pass-ont#hasPoint3D"
		self._attributeMapping["hasXValue"] = "http://www.imi.kit.edu/abstract-pass-ont#hasXValue"
		self._attributeMapping["hasYValue"] = "http://www.imi.kit.edu/abstract-pass-ont#hasYValue"
		self._attributeMapping["hasZValue"] = "http://www.imi.kit.edu/abstract-pass-ont#hasZValue"
		self._attributeMapping["hasValue"] = "http://www.imi.kit.edu/abstract-pass-ont#hasValue"
		self._attributeMapping["hasKey"] = "http://www.imi.kit.edu/abstract-pass-ont#hasKey"
		self._attributeMapping["belongsTo"] = "http://www.imi.kit.edu/abstract-pass-ont#belongsTo"
		self._attributeMapping["hasModelComponent"] = "http://www.imi.kit.edu/abstract-pass-ont#hasModelComponent"
		self._attributeMapping["references"] = "http://www.imi.kit.edu/abstract-pass-ont#references"
		self._attributeMapping["hasBehavior"] = "http://www.imi.kit.edu/abstract-pass-ont#hasBehavior"
		self._attributeMapping["receiver"] = "http://www.imi.kit.edu/abstract-pass-ont#receiver"
		self._attributeMapping["sender"] = "http://www.imi.kit.edu/abstract-pass-ont#sender"
		self._attributeMapping["hasType"] = "http://www.imi.kit.edu/abstract-pass-ont#hasType"
		self._attributeMapping["hasEdge"] = "http://www.imi.kit.edu/abstract-pass-ont#hasEdge"
		self._attributeMapping["hasState"] = "http://www.imi.kit.edu/abstract-pass-ont#hasState"
		self._attributeMapping["hasSourceState"] = "http://www.imi.kit.edu/abstract-pass-ont#hasSourceState"
		self._attributeMapping["hasTargetState"] = "http://www.imi.kit.edu/abstract-pass-ont#hasTargetState"
		self._attributeMapping["refersTo"] = "http://www.imi.kit.edu/abstract-pass-ont#refersTo"

	def getAttributeName(self, uri):
		"""
		 Returns the name of an attribute for a given uri (representing an attribute in
		 rdfs). If this attribute uri is currently unknwon a new resource object is
		 created, linking to this resource. If this attribute is already registered as an
		 resource nothing happens.

		@param string uri : The uri representing the attribute in rdfs
		@return string :
		@author
		"""
		#Search for the right key in the array
		for (key, value) in list(self._attributeMapping.items()):
			if(value == uri):
				return key
		#If nothing was found, create new attribute mapping and add it to the dict
		#First check the format
		if((not isinstance(uri, str)) or (not uri.startswith("http://"))):
			raise Exception("The given uri parameter is not of type string or does not start with \"http://\" !")
		else:
			#Get the appendix of the attribute mapping
			newAttrName = uri.split("/")[-1]
			#Mayber better to use regex here?
			newAttrName = newAttrName.split("#")[-1]
			#Now check if the attribute already exists in the mapping set
			while(newAttrName in self._attributeMapping):
				newAttrName = newAttrName + "x"
			self._attributeMapping[newAttrName] = uri
			print(("INFO! Added \"" + uri + "\" with attribute name \"" + newAttrName + "\" to the attribute mapping!"))
			return newAttrName

	def getAttributeUri(self, attributeName):
		"""
		 Returns the rdfs resource object belonging to/representing this attribute. If
		 the attribute name is unknwon an error is thrown.

		@param string attributeName : The name of the attribute the resource should be obtained from.
		@return Resource :
		@author
		"""
		if(attributeName in self._attributeMapping):
			return self._attributeMapping[attributeName]
		else:
			raise Exception("Given attribute " + attributeName + " name is not registered to the attribute mapping!")



