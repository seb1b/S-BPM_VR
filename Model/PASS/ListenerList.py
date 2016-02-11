# -*- coding: utf-8 -*-

import weakref


class ListenerList(list):
	"""
	List that calls its superclass' fireChangeEvent function (if it exists) whenever something changes.
	
	@author Lukas Block
	@version 2015-01-11
	"""

	def __init__(self, value, parent, attrName):
		list.__init__(self, value)
		self._parent = weakref.ref(parent)
		self._attrName = attrName

	def _callParent(self):
		parent = self._parent()
		if(parent is not None):
			operation = getattr(parent, "fireChangeEvent", None)
			if(callable(operation)):
				parent.fireChangeEvent(self._attrName)

	def __setitem__(self, key, value):
		list.__setitem__(self, key, value)
		self._callParent()

	def __delitem__(self, key):
		list.__delitem__(self, key)
		self._callParent()

	def __setslice__(self, i, j, sequence):
		list.__setslice__(self, i, j, sequence)
		self._callParent()

	def __delslice__(self, i, j):
		list.__delslice__(self, i, j)
		self._callParent()

	def append(self, value):
		list.append(self, value)
		self._callParent()

	def pop(self):
		result = list.pop(self)
		self._callParent()
		return result

	def extend(self, newvalue):
		list.extend(self, newvalue)
		self._callParent()

	def insert(self, i, element):
		list.insert(self, i, element)
		self._callParent()

	def remove(self, element):
		list.remove(self, element)
		self._callParent()

	def reverse(self):
		list.reverse(self)
		self._callParent()

	def sort(self, cmpfunc=None):
		list.sort(self, cmpfunc)
		self._callParent()
