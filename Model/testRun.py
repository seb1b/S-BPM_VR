# -*- coding: utf-8 -*-

import PASS


def changeListener(object, attrName):
	print(("==> Object changed: " + str(object) + " with attribute " + str(attrName) + "!"))

print("========= Loading: =============")
manager = PASS.ModelManager("./tests/in001.nt")
manager.addChangeListener(changeListener)
print("========= Adding elements ==========")
element = PASS.PASSProcessModelElement(manager)
element._fireChangeEvents = True
element.hasAbstractVisualRepresentation = PASS.AbstractVisualRepresentation(manager)
element.hasAbstractVisualRepresentation.setPoint2D(1.0, 1.0)
element.hasAbstractVisualRepresentation = PASS.AbstractVisualRepresentation(manager)
element.hasAbstractVisualRepresentation.setPoint2D(2.0, 2.0)
element.setMetaContent("Hallo", "Hallo Lukas")
element.setMetaContent("Test", "Ein Test")
element.setMetaContent("Hallo", "Hallo Svenya")
element.setMetaContent("Hallo", "Hallo Lukas", False)
element.removeMetaContent("Hallo")
print(element.getMetaKeys())
print(element.getMetaContent("Test"))
print(element.getMetaContent("Hallo"))
print("========= Saving 1: =============")
manager.saveAs("./tests/out001.nt")
print("========= Loading and Saving 2: =============")
manager2 = PASS.ModelManager("./tests/out001.nt")
manager2.saveAs("./tests/out001-2.owl")
