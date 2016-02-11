import PASS
import gc

def buildHelper(manager, model):
	#SID
	layer = model.hasModelComponent[0]
	#behavior1 = layer.addBehavior()
	subject1 = layer.addSubject()
	subject2 = layer.addSubject()
	#messageExchange = layer.addMessageExchange(subject2, subject1)
	messageExchange2 = layer.addMessageExchange(subject1, subject2)

	#Indicator that weakref does not work... Or there is a reference somewhere else still active
	#print "Size: ", len(manager.resources)
	#print(layer.hasModelComponent)
	#layer.removeActiveComponent(subject1)
	#print(layer.hasModelComponent)
	#SBD
	#behavior2 = subject2.hasBehavior
	#newState1 = behavior2.addFunctionState()
	#newState1.isFinalState = True
	#newState2 = behavior2.addSendState()
	#newState2.isFinalState = True
	#behavior2.setInitialState(newState2)
	#behavior2.addStandardTransition(newState1, newState2)
	#newState3 = behavior2.addReceiveState()
	#behavior2.addSendTransition(newState2, newState3, messageExchange)
	#behavior2.addReceiveTransition(newState3, newState1, messageExchange2)
	

print("Enabled: " + str(gc.isenabled()))
#Create manager
manager = PASS.ModelManager()
#Now build the model
print("==")
buildHelper(manager, manager.model)
gc.collect()
print "Size: ", len(manager.resources)
print("==")
#Save
manager.saveAs("./tests/test8_1.owl")

print("====================== Model 2 ================================")

#Load again
manager2 = PASS.ModelManager("./tests/test8_1.owl")
manager2.saveAs("./tests/test8_2.owl")

#Load again
manager3 = PASS.ModelManager("./tests/test8_2.owl")
manager3.saveAs("./tests/test8_3.owl")
