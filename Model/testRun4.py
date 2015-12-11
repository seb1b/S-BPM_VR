import PASS

def buildHelper(manager, model):
	#SID
	layer = model.hasModelComponent[0]
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
manager = PASS.ModelManager()
#Now build the model
buildHelper(manager, manager.model)

#Save
manager.saveAs("./tests/out004.owl")


manager2 = PASS.ModelManager("./tests/out004.owl")
print(manager2.model.hasModelComponent[0].activeComponents[1].hasBehavior.hasState[0].hasComponentID)