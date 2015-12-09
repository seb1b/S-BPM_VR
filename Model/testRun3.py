import PASS

def buildHelper(manager, model):
	#SID
	layer = PASS.BaseLayer(manager)
	model.hasModelComponent.append(layer)
	behavior1 = layer.addBehavior()
	subject1 = layer.addSubject(behavior1)
	subject2 = layer.addSubject()
	messageExchange = layer.addMessageExchange(subject1, subject2)
	
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
	e31 = behavior2.addReceiveTransition(newState3, newState1, messageExchange)
	
	#behavior2.removeState(newState2)
	#behavior2.removeTransition(e31)
	#behavior2.removeState(newState1)
	
	#layer.removeMessageExchange(messageExchange)
	#layer.removeActiveComponent(subject1)
	#layer.removeBehavior(behavior2)

#Create manager
manager = PASS.ModelManager("./tests/in001.nt")
#Now build the model
model = PASS.PASSProcessModel(manager)
buildHelper(manager, model)

#Save
manager.saveAs("./tests/out001-3.owl")


manager2 = PASS.ModelManager("./tests/out001-3.owl")
manager2.saveAs("./tests/out001-4.owl")