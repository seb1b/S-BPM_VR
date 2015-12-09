# -*- coding: utf-8 -*-
import PASS

def buildHelper(manager, model):
	# SID
	baseLayer = model.hasModelComponent[0]
	# SID -> Subjects
	sKonstrukteur = baseLayer.addSubject()
	sKonstrukteur.label.append("Konstrukteur")
	sPruefer = baseLayer.addSubject()
	sPruefer.label.append("Prüfer")
	sEntwicklungsleiter = baseLayer.addSubject()
	sEntwicklungsleiter.label.append("Entwicklungsleiter")
	sPrototypenbau = baseLayer.addSubject()
	sPrototypenbau.label.append("Prototypenbau")
	sSerienfertigung = baseLayer.addSubject()
	sSerienfertigung.label.append("Serienfertigung")
	# SID -> MessageExchanges
	meKonstrukteurPruefer = baseLayer.addMessageExchange(sKonstrukteur, sPruefer)
	meKonstrukteurPruefer.label.append("Änderungsantrag")
	mePrueferKonstrukteur = baseLayer.addMessageExchange(sPruefer, sKonstrukteur)
	mePrueferKonstrukteur.label.append("Antrag überarbeiten")
	mePrueferEntwicklungsleiter = baseLayer.addMessageExchange(sPruefer, sEntwicklungsleiter)
	mePrueferEntwicklungsleiter.label.append("Änderungsantrag in Ordnung")
	meEntwicklungsleiterPrototypenbau = baseLayer.addMessageExchange(sEntwicklungsleiter, sPrototypenbau)
	meEntwicklungsleiterPrototypenbau.label.append("Freigabe Prototypenbau")
	meEntwicklungsleiterSerienfertigung = baseLayer.addMessageExchange(sEntwicklungsleiter, sPrototypenbau)
	meEntwicklungsleiterSerienfertigung.label.append("Freigabe der Serienfertigung")
	mePrototypenbauEntwicklungsleiter = baseLayer.addMessageExchange(sPrototypenbau, sEntwicklungsleiter)
	mePrototypenbauEntwicklungsleiter.label.append("Prototyp funktional")
	mePrototypenbauKonstrukteur = baseLayer.addMessageExchange(sPrototypenbau, sPruefer)
	mePrototypenbauKonstrukteur.label.append("Prototyp nicht funktional")
	
	# SBD (Pruefer)
	behaviorPruefer = sPruefer.hasBehavior
	# SBD -> States
	state1 = behaviorPruefer.addReceiveState()
	state1.label.append("Warten auf Antrag")
	behaviorPruefer.setInitialState(state1)
	state2 = behaviorPruefer.addFunctionState()
	state2.label.append("Prüfe Antrag")
	state3 = behaviorPruefer.addSendState()
	state3.label.append("Bitte um Freigabe")
	state4 = behaviorPruefer.addReceiveState()
	state4.label.append("Ende")
	state4.isFinalState = True
	state5 = behaviorPruefer.addSendState()
	state5.label.append("Informiere Konstrukteur")
	
	# SBD -> TransitionEdges
	edge12 = behaviorPruefer.addReceiveTransition(state1, state2, meKonstrukteurPruefer)
	edge12.label.append("Änderungsantrag")
	edge23 = behaviorPruefer.addStandardTransition(state2, state3)
	edge23.label.append("Antrag OK")
	edge25 = behaviorPruefer.addStandardTransition(state2, state5)
	edge25.label.append("Antrag nicht OK")
	edge34 = behaviorPruefer.addSendTransition(state3, state4, mePrueferKonstrukteur)
	edge34.label.append("Änderungsantrag in Ordnung")
	edge42 = behaviorPruefer.addReceiveTransition(state4, state2, meKonstrukteurPruefer)
	edge42.label.append("Änderungsantrag")

#Create manager
manager = PASS.ModelManager()
#Now build the model
buildHelper(manager, manager.model)

#Save
manager.saveAs("./tests/Beispielprozess.owl")