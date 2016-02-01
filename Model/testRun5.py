# -*- coding: utf-8 -*-

import PASS

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

	print behavior2.getBoundingBox2D()
	print behavior2.getBoundingBox3D()
	print behavior1.getBoundingBox2D()
	print behavior1.getBoundingBox3D()

	print layer.getBoundingBox2D()
	print layer.getBoundingBox3D()


def changeListener(object, attrName):
	global i
	print(("==> Object changed: " + str(object) + " with attribute " + str(attrName) + "!"))
	print(("==> Parent: " + str(object.getParent(PASS.BaseLayer)) + "!"))
	i += 1



print("========= Loading: =============")
manager = PASS.ModelManager()
manager.addChangeListener(changeListener)
buildHelper(manager, manager.model)

print(i)
