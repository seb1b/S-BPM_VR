import PASS

def changeListener(object, attrName):
	print(("==> Object changed: " + str(object) + " with attribute " + str(attrName) + "!"))
	if attrName is not None:
		test = getattr(object, attrName)
		if isinstance(test, list):
			print test;
			for e in test:
				if hasattr(e, "label"):
					print e.label

modelManager = PASS.ModelManager("./tests/Beispielprozess.owl")
modelManager.addChangeListener(changeListener)
konstr = modelManager.model.hasModelComponent[0].hasModelComponent[0]
for e in konstr.hasEdge:
	print e.label
print "================"
for s in konstr.hasState:
	print s.label
print "================"
konstr.removeState(konstr.hasState[0])
print "================"
for e in konstr.hasEdge:
	print e.label
print "================"
for s in konstr.hasState:
	print s.label
