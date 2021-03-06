#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

import random

from gettext import gettext as _

import copy

''' Scales '''
IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]


'''Color Selection association
Reference of colours codes :http://www.rapidtables.com/web/color/RGB_Color.htm
'''
COLOURS_ASSOCIATION = []

COLOURS_ASSOCIATION.append({"colour":"#0074DF", "available":True})

COLOURS_ASSOCIATION.append({"colour":"#FF1F68", "available":True})

COLOURS_ASSOCIATION.append({"colour":"#D9E021", "available":True})

COLOURS_ASSOCIATION.append({"colour":"#6FC72B", "available":True})

COLOURS_ASSOCIATION.append({"colour":"#F1C001", "available":True})

EVENTBOX_SCALE = [100,100]


'''Curren item selection association'''
SELECTED_COLOUR = gtk.gdk.Color("#FFFF00")

FONT_DESCRIPTION_BIG = 'DejaVu Bold 30'
FONT_DESCRIPTION_MEDIUM = 'DejaVu Bold 15'

class SimpleAssociation():

	def saveExerciseState(self):
		self.mainWindows.getLogger().debug("Inside to saveExerciseState")	
		stateJson = {}
		stateJson['optionsSelectionState'] = self.optionsSelectionState
		stateJson['correspondencesSelectionState'] = self.correspondencesSelectionState
		stateJson['currentOptionSelected'] = self.currentOptionSelected
		stateJson['lastOptionSelected'] = self.lastOptionSelected
		stateJson['currentCorrespondenceSelected'] = self.currentCorrespondenceSelected
		stateJson['lastCorrespondenceSelected'] = self.lastCorrespondenceSelected
		
		stateJson['optionsList'] = self.optionsList
		stateJson['correspondencesList'] = self.correspondencesList
		stateJson['COLOURS_ASSOCIATION'] = self.COLOURS_ASSOCIATION	
		stateJson['exerciseCompleted'] = self.exerciseCompleted

		return stateJson 
	
	def disconnectEventBoxs(self):
		for index, eventBox in enumerate(self.allEventBoxs):
                 	eventBox.disconnect(self.idHandlers[index])
	
		
	
	def getWindow(self, exercise, mainWindows, stateJson):
		
		
		self.mainWindows = mainWindows
			
		windowSimpleAssociation = gtk.ScrolledWindow()
		windowSimpleAssociation.exerciseInstance = self		

		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription("Sans 10"))
		
		vBoxWindows = gtk.VBox(False, 5)
		hBoxExercises = gtk.HBox(False, 5)
		self.vBoxOptions = gtk.VBox(False, 5)
		self.vBoxOptions.set_border_width(10)
		self.vBoxCorrespondences = gtk.VBox(False, 5)
		self.vBoxCorrespondences.set_border_width(10)
		
		frameExercises = gtk.Frame() 
		
		frameExercises.add(hBoxExercises)
	
		self.idHandlers = []
		self.allEventBoxs = []	
		self.exerciseCompleted = False	
		if stateJson is None:
			self.optionsSelectionState = []
			self.correspondencesSelectionState = []
		
			self.currentOptionSelected = -1
			self.lastOptionSelected = -1
		
			self.currentCorrespondenceSelected = -1
			self.lastCorrespondenceSelected = -1
		
			self.optionsList, self.correspondencesList = self.disorderCorrespondences(exercise.items)
			
			self.COLOURS_ASSOCIATION = COLOURS_ASSOCIATION
			
		else:
			self.optionsSelectionState = stateJson['optionsSelectionState']
			self.correspondencesSelectionState = stateJson['correspondencesSelectionState']
		
			self.currentOptionSelected = stateJson['currentOptionSelected']
			self.lastOptionSelected = stateJson['lastOptionSelected']
		
			self.currentCorrespondenceSelected = stateJson['currentCorrespondenceSelected']
			self.lastCorrespondenceSelected = stateJson['lastCorrespondenceSelected']
			self.optionsList = stateJson['optionsList']
			self.correspondencesList = stateJson['correspondencesList']
			self.COLOURS_ASSOCIATION = stateJson['COLOURS_ASSOCIATION']			
			self.exerciseCompleted = stateJson['exerciseCompleted']	
		self.mainWindows.getLogger().debug( self.COLOURS_ASSOCIATION )

	
		firstOptionEventBox = None
		
		frameVBoxOptions = gtk.Frame()
		frameVBoxOptions.set_border_width(10)
		#dark orange
		frameVBoxOptions.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#FF8C00"))		
		frameVBoxCorrespondences = gtk.Frame()
		frameVBoxCorrespondences.set_border_width(10)
		#dark slate blue
                frameVBoxCorrespondences.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#483D8B'))

		for index,  option in enumerate(self.optionsList):
			'''Options'''
			self.mainWindows.getLogger().debug(option)
			eventBoxOption = self.createEventBox(option['option']['value'], option['option']['type'])
			if not self.exerciseCompleted:
				idHandler = eventBoxOption.connect("button-press-event", self.imageSelectedCallBack, self.vBoxCorrespondences)
				self.allEventBoxs.append(eventBoxOption)
				self.idHandlers.append(idHandler)			

			self.addEventBoxToVBox(eventBoxOption, self.vBoxOptions)			
			if index == 0:
				firstOptionEventBox = eventBoxOption
			if stateJson is None:
				self.optionsSelectionState.append ( {"selected": -1, "pair": option['indexPair'], "colour": None} )
			
			'''Correspondences'''
			eventBoxCorrespondence = ( self.createEventBox(self.correspondencesList[index]['correspondence']['value'],
							self.correspondencesList[index]['correspondence']['type']) )
			
			if not self.exerciseCompleted:
				idHandler = eventBoxCorrespondence.connect("button_press_event", self.pairSelectedCallBack, self.vBoxOptions)
				self.allEventBoxs.append(eventBoxCorrespondence)
				self.idHandlers.append(idHandler)			

			self.addEventBoxToVBox(eventBoxCorrespondence, self.vBoxCorrespondences)
			if stateJson is None:
				( self.correspondencesSelectionState.append( {"selected": -1,
				"pair":self.correspondencesList[index]['indexPair'], "colour": None} ) )	
			
	        frameVBoxOptions.add(self.vBoxOptions)		
		frameVBoxCorrespondences.add(self.vBoxCorrespondences)
		hBoxExercises.pack_start(frameVBoxOptions, True,True,5)
		hBoxExercises.pack_start(frameVBoxCorrespondences, True,True,50)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		
		windowSimpleAssociation.add_with_viewport(vBoxWindows)
		
		if stateJson is not None:
			self.repaintResumeItems()
		else:
			self.setAllAvailableSelectionColour()
			self.selectFirtImage(firstOptionEventBox)	
			
		return windowSimpleAssociation

	def repaintResumeItems(self):
		
		for index, value in enumerate(self.optionsSelectionState):
			eventBoxOption = self.vBoxOptions.get_children()[index].get_children()[0]
			eventBoxCorrespondence = self.vBoxCorrespondences.get_children()[index].get_children()[0]
		
			if value['colour'] is not None:
				self.mainWindows.getLogger().debug(value)
				self.changeBackgroundColour(eventBoxOption,str(value['colour']['colour']))				
				
	
			valueCorresondence = self.correspondencesSelectionState[index]
			self.mainWindows.getLogger().debug(valueCorresondence)
			if valueCorresondence['colour'] is not None:
				self.changeBackgroundColour(eventBoxCorrespondence, str(valueCorresondence['colour']['colour']))
		
		firstFrameOption = self.vBoxOptions.get_children()[self.currentOptionSelected] 
		self.fakeSelection(firstFrameOption)

	def addEventBoxToVBox(self, eventBox, vBox):
		frameEventBox = gtk.EventBox()
		frameEventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("white"))
		eventBox.set_border_width(5)
		frameEventBox.add(eventBox)
		vBox.pack_start(frameEventBox, False,False,0)
		
	def createEventBox(self, payload, typePayload):
		eventBox = gtk.EventBox()
		eventBox.set_size_request(EVENTBOX_SCALE[0], EVENTBOX_SCALE[1])
		if typePayload == "image":
			imageContainer =  gtk.Image()
			pixbuf = gtk.gdk.pixbuf_new_from_file(payload).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2)
			imageContainer.set_from_pixbuf(pixbuf)
			eventBox.add(imageContainer)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
		if typePayload == "letter":
			letterLabel = gtk.Label(payload)
			if len(payload) <= 8:
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:	
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))
			eventBox.add(letterLabel)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
						
		return eventBox
			
		
	def selectFirtImage(self, firstEvenBox):
		availableColour =  self.getAvailableSelectionColour()
		self.changeBackgroundColour(firstEvenBox, availableColour['colour'])
		self.setSelectionStateColour(self.optionsSelectionState, 0, availableColour)
		self.currentOptionSelected = 0
		frameImageSelected = firstEvenBox.get_parent()
		self.fakeSelection(frameImageSelected)
		
		
	def disorderCorrespondences(self, items):
		
		self.mainWindows.getLogger().debug("Inside to disorderCorrespondences")
		optionsList = [None]*len(items)
		correspondencesList = [None]*len(items)
		
		indexsList = range(len(items))
		originalList = copy.copy(indexsList)
		self.mainWindows.getLogger().debug(originalList)
                self.mainWindows.getLogger().debug(indexsList)
		random.shuffle(indexsList)
		while( originalList == indexsList and len(items) > 1):
			self.mainWindows.getLogger().debug("Inside to while...")
			random.shuffle(indexsList)
		self.mainWindows.getLogger().debug(originalList)
		self.mainWindows.getLogger().debug(indexsList)
		

		for index, item in enumerate(items):
			optionsList[index] = {"option":{"type":item.option.type, "value":item.option.value}, \
						"indexPair": indexsList[index]}
			correspondencesList[indexsList[index]] = ( {"correspondence":{"type":item.correspondence.type, 
								"value":item.correspondence.value}, "indexPair": index} )
		
		return (optionsList, correspondencesList)
	
	def checkCompletedExercise(self):
		result = True
		for index,imageSelectionState in enumerate( self.optionsSelectionState ):
			if (imageSelectionState['selected'] != imageSelectionState['pair']) or \
				(self.correspondencesSelectionState[index]['selected'] != self.correspondencesSelectionState[index]['pair']) :
				result = False
				break
		if result:
			self.exerciseCompleted = True
			self.mainWindows.exerciseCompletedCallBack()
	
	def setAllAvailableSelectionColour(self):
		for colour in self.COLOURS_ASSOCIATION:
			colour['available'] = True
			
	def getAvailableSelectionColour(self):
		response = None
		for colour in self.COLOURS_ASSOCIATION:
			if colour['available']:
				response = colour
				break
		return response
	
	def setAvailableColour(self, colour):
			
		for currentColour in self.COLOURS_ASSOCIATION:
			if currentColour['colour'] == colour['colour']:
				currentColour['available'] = True
				break
		
	
	def setUnavailableColour(self, colour):
		
		for currentColour in self.COLOURS_ASSOCIATION:
			if currentColour['colour'] == colour['colour']:
				currentColour['available'] = False
				break

			
	def imageSelectedCallBack(self, imageEventBox, *args):
		
		frameImageSelected = imageEventBox.get_parent()
		vBoxImages = imageEventBox.get_parent().get_parent()
		
		allImagesFrames = vBoxImages.get_children()
		
		indexImageSelected = vBoxImages.child_get_property(frameImageSelected, "position")
		self.lastOptionSelected = self.currentOptionSelected
		self.currentOptionSelected = indexImageSelected
		
		vBoxPairs = args[1]
		'''Se des-selecciona el par selecciondo previamente'''
		if self.currentCorrespondenceSelected != -1:
			framePairSelected = vBoxPairs.get_children()[self.currentCorrespondenceSelected]
			self.fakeUnselection(framePairSelected)
		
		# Revisamos si la ultima imagen seleccionada no fue asociada
		if self.lastOptionSelected != -1 and self.optionsSelectionState[self.lastOptionSelected]['selected'] == -1:
			
			# No se ha asociado nada, volvemos a a poner a blanco el bg colour
			lastImageEvenBoxSelected = allImagesFrames[self.lastOptionSelected].get_children()[0]
			self.changeBackgroundColour(lastImageEvenBoxSelected, "white")
			self.setSelectionStateColour(self.optionsSelectionState, self.lastOptionSelected, None)
			
			
		# Revisamos si ya existe una asociacion'''
		if self.optionsSelectionState[indexImageSelected]['selected'] == -1:
			# Aun no existe una asociación
			colorAvailable = self.getAvailableSelectionColour()
			self.changeBackgroundColour(imageEventBox, colorAvailable['colour'])
			self.setSelectionStateColour(self.optionsSelectionState, indexImageSelected, colorAvailable)
			
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		lastFrameImageSelected = allImagesFrames[self.lastOptionSelected]
		self.fakeUnselection(lastFrameImageSelected)	
		self.fakeSelection(frameImageSelected)
	
		#Comprabamos la finalización del ejercicio
		self.checkCompletedExercise()
			
	def pairSelectedCallBack(self, pairEventBox, *args):

		vBoxImages = args[1]
		allFramesImages = vBoxImages.get_children()
				
		framePairSelected = pairEventBox.get_parent()
		vBoxPairs = framePairSelected.get_parent()
		
		allPairFrames = vBoxPairs.get_children()
		
		indexPairSelected = vBoxPairs.child_get_property(framePairSelected, "position")
		self.lastCorrespondenceSelected = self.currentCorrespondenceSelected
		self.currentCorrespondenceSelected = indexPairSelected
		
		lastPairSelectionState = None
		self.mainWindows.getLogger().debug( self.correspondencesSelectionState )
		if self.lastCorrespondenceSelected != -1:
			lastPairSelectionState = self.correspondencesSelectionState[self.lastCorrespondenceSelected]
		
		pairIndexCurrentImageSelected = -1
		imageEventBoxCurremtSelected = None
		if self.currentOptionSelected != -1:
			pairIndexCurrentImageSelected = self.optionsSelectionState[self.currentOptionSelected]['selected']
			imageEventBoxCurremtSelected = self.optionsSelectionState[self.currentOptionSelected]['colour']
		
		pairEventBoxCurrentImageSelected = None
		if self.currentOptionSelected != -1 and pairIndexCurrentImageSelected != -1:
			pairEventBoxCurrentImageSelected =  allPairFrames[self.optionsSelectionState[self.currentOptionSelected]['selected']].get_children()[0]
		
		
		# Verificamos que el ultimo par seleccionado no tenga una asocicion
		if self.lastCorrespondenceSelected != -1 and lastPairSelectionState['selected'] == -1:
			lastPairEventBoxSelected = allPairFrames[self.lastCorrespondenceSelected].get_children()[0]
			self.changeBackgroundColour(lastPairEventBoxSelected, "white")
			self.mainWindows.getLogger().debug(lastPairSelectionState)
			self.setAvailableColour(lastPairSelectionState['colour'])
			self.setSelectionStateColour(self.correspondencesSelectionState, self.lastCorrespondenceSelected, None)
			
		
		#Comprobamos si hay alguna imagen seleccionada 
		if self.currentOptionSelected != -1:
			#usamos el color de la imagen seleccionada como bg
			colourImageSelected = self.optionsSelectionState[self.currentOptionSelected]['colour']
			self.changeBackgroundColour(pairEventBox, colourImageSelected['colour'])
			self.setSelectionStateColour(self.correspondencesSelectionState, indexPairSelected, colourImageSelected )
			
					
			#La imagen asociada al par poseía otro par asociado anteriormente
			if pairIndexCurrentImageSelected != -1 and pairIndexCurrentImageSelected != self.currentCorrespondenceSelected:
				#des-asociamos el par aterior
				currentPairEventBoxSelected = allPairFrames[pairIndexCurrentImageSelected].get_children()[0]
				self.changeBackgroundColour(currentPairEventBoxSelected, "white")
				self.setAvailableColour(self.correspondencesSelectionState[pairIndexCurrentImageSelected]['colour'])
				self.setSelectionStateColour(self.correspondencesSelectionState, pairIndexCurrentImageSelected, None )
				self.correspondencesSelectionState[pairIndexCurrentImageSelected]['selected'] = -1
				
				
			#El par seleccionado ya fue asociado por otra imagen, la cual no es la actualmente seleccionada
			if ( self.correspondencesSelectionState[indexPairSelected]['selected'] != -1 
				and self.correspondencesSelectionState[indexPairSelected]['selected'] != self.currentOptionSelected):
				
				#des-asociamos la imagen anterior asociada al par
				imagePairSelectedEventBox= allFramesImages[self.correspondencesSelectionState[indexPairSelected]['selected']].get_children()[0]
				self.changeBackgroundColour(imagePairSelectedEventBox,"white")
				self.setAvailableColour(self.optionsSelectionState[self.correspondencesSelectionState[indexPairSelected]['selected']]['colour'])
				self.setSelectionStateColour(self.optionsSelectionState, self.correspondencesSelectionState[indexPairSelected]['selected'], None )
				self.optionsSelectionState[self.correspondencesSelectionState[indexPairSelected]['selected']]['selected'] = -1
			
			#guardamos los datos de la asociacion actuales de ambos lados
			self.correspondencesSelectionState[indexPairSelected]['selected'] = self.currentOptionSelected
			self.optionsSelectionState[self.currentOptionSelected]['selected'] = indexPairSelected
			self.setUnavailableColour(colourImageSelected)	
				
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		self.fakeSelection(framePairSelected)
		lastFramePairSelected = allPairFrames[self.lastCorrespondenceSelected]
		self.mainWindows.getLogger().debug(self.lastCorrespondenceSelected)
		self.mainWindows.getLogger().debug(self.currentCorrespondenceSelected)
		if (self.lastCorrespondenceSelected != self.currentCorrespondenceSelected) and self.lastCorrespondenceSelected != -1:
			self.fakeUnselection(lastFramePairSelected)
		
		#Comprabamos la finalización del ejercicio
		self.checkCompletedExercise()
	
	def fakeSelection(self, frame):
		self.mainWindows.getLogger().debug(frame)
		frame.modify_bg(gtk.STATE_NORMAL, SELECTED_COLOUR)	
		#self.mainWindows.getLogger().debug("get_style() : ")
		#self.mainWindows.getLogger().debug(frame.get_style() )
			
	def fakeUnselection(self, frame):
		frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("white"))	

	def changeBackgroundColour(self, eventBox, colour):
		eventBox.modify_bg(gtk.STATE_NORMAL,  gtk.gdk.Color(colour))		
	
	def setSelectionStateColour(self,selectionState, index, colour):
		selectionState[index]['colour'] = colour
		
