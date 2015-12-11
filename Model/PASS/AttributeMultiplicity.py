class AttributeMultiplicity():
	"""
	Enum to represent how often a certain attribute is allowed to occur in a class.
	:version: 2015-12-01
	:author: Lukas Block
	"""

	""" Enum Literals
	
	The information about multiplicity is not given in the ontology. This is resolved by representing the attribute as an array that might also be empty.
	UNKNOW
	
	Exactly one instance is allowed.
	UNIQUE
	
	"""
	
	UNKNOWN = 0
	UNIQUE = 1