# -*- coding: utf-8 -*-

import PASS
from copy import deepcopy

i = 0

def buildHelper(manager, model):
	#SID
	layer = PASS.BaseLayer(manager)
	model.hasModelComponent.append(layer)
	behavior1 = layer.addBehavior()
	subject1 = layer.addSubject(behavior1)
	subject2 = layer.addSubject()
	subject1.hasAbstractVisualRepresentation.setPoint2D(0, 1)
	subject2.hasAbstractVisualRepresentation.setPoint3D(1, 2, 3)
	subject2.hasAbstractVisualRepresentation.setPoint2D(-13, 5)
	messageExchange = layer.addMessageExchange(subject2, subject1)
	messageExchange2 = layer.addMessageExchange(subject1, subject2)
	#SBD
	behavior2 = subject2.hasBehavior
	newState1 = behavior2.addFunctionState()
	newState1.isFinalState = True
	newState2 = behavior2.addSendState()
	newState2.isFinalState = True
	behavior2.setInitialState(newState2)
	behavior2.addStandardTransition(newState1, newState2)
	newState3 = behavior2.addReceiveState()
	behavior2.addSendTransition(newState2, newState3, messageExchange)
	behavior2.addReceiveTransition(newState3, newState1, messageExchange2)

	newState3.hasAbstractVisualRepresentation.setPoint2D(13, 15)

	newState2.label.append("Hallo")

	print("==================================")
	test = deepcopy(subject2)
	subject2.hasBehavior.hasState[0].setMetaContent("test", 1)
	test.hasBehavior.hasState[0].setMetaContent("test", 2)
	#print(subject2.hasBehavior.hasState[0].getMetaContent("test"))
	#print(test.hasBehavior.hasState[0].getMetaContent("test"))
	print("==================================")

	#print("==================================")
	#test = layer.duplicateActiveProcessComponent(subject2)
	#subject2.hasBehavior.hasState[0].label.append("Test1")
	#test.hasBehavior.hasState[0].label.append("Test2")
	#print(subject2.hasBehavior.hasState[0].label)
	#print(test.hasBehavior.hasState[0].label)
	#print("==================================")
	#print(test.hasBehavior)

	test2 = test.hasBehavior.duplicateState(test.hasBehavior.hasState[0])


def changeListener(obj, attrName):
	global i
	#print(("==> Object changed: " + str(obj) + " with attribute " + str(attrName) + "!"))
	#print(("==> Parent: " + str(obj.getParent()) + "!"))
	i += 1



print("========= Loading: =============")
manager = PASS.ModelManager()
manager.addChangeListener(changeListener)
buildHelper(manager, manager.model)

print(i)
