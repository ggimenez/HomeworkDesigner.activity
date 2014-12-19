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


''' Scales '''
IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]


'''Color Selection association
Reference of colours codes :http://www.rapidtables.com/web/color/RGB_Color.htm
'''
COLOURS_ASSOCIATION = []
#medium sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#3CB371"), "available":True})
#teal
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#008080"), "available":True})
#thistle
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#D8BFD8"), "available":True})
#dark sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#8FBC8F"), "available":True})
#forest green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#228B22"), "available":True})


'''Curren item selection association'''
SELECTED_COLOUR = gtk.gdk.Color("#FFFF00")



class SimpleAssociation():
	
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
			
		windowSimpleAssociation = gtk.ScrolledWindow()
		
		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription("Sans 10"))
		
		vBoxWindows = gtk.VBox(False, 5)
		hBoxExercises = gtk.HBox(True, 50)
		vBoxOptions = gtk.VBox(True, 5)
		vBoxCorrespondences = gtk.VBox(True, 5)
		
		frameExercises = gtk.Frame() 
		
		frameExercises.add(hBoxExercises)
		
		
		self.optionsSelectionState = {}
		self.correspondencesSelectionState = {}
		
		self.currentOptionSelected = -1
		self.lastOptionSelected = -1
		
		self.currentCorrespondenceSelected = -1
		self.lastCorrespondenceSelected = -1
		
		self.setAllAvailableSelectionColour()
		
		optionsList, correspondencesList = self.disorderCorrespondences(exercise.items)
		firstOptionEventBox = None
		for index,  option in enumerate(optionsList):
			'''Options'''
			eventBoxOption = self.createEventBox(option['option'].value, option['option'].type)
			eventBoxOption.connect("button-press-event", self.imageSelectedCallBack, vBoxCorrespondences)
			self.addEventBoxToVBox(eventBoxOption, vBoxOptions)			
			if index == 0:
				firstOptionEventBox = eventBoxOption
			self.optionsSelectionState[index] = {"selected": -1, "pair": option['indexPair'], "colour": None}
			
			'''Correspondences'''
			eventBoxCorrespondence = self.createEventBox(correspondencesList[index]['correspondence'].value, correspondencesList[index]['correspondence'].type)
			eventBoxCorrespondence.connect("button_press_event", self.pairSelectedCallBack, vBoxOptions)
			self.addEventBoxToVBox(eventBoxCorrespondence, vBoxCorrespondences)
			self.correspondencesSelectionState[index] = {"selected": -1, "pair": correspondencesList[index]['indexPair'], "colour": None}	
			
			
		hBoxExercises.pack_start(vBoxOptions, False,True,50)
		hBoxExercises.pack_start(vBoxCorrespondences, False,True,50)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		
		windowSimpleAssociation.add_with_viewport(vBoxWindows)
		
		self.selectFirtImage(firstOptionEventBox)
		
		return windowSimpleAssociation
	
	def addEventBoxToVBox(self, eventBox, vBox):
		frameEventBox = gtk.Frame() 
		frameEventBox.add(eventBox)
		vBox.pack_start(frameEventBox, False,False,0)
		
	def createEventBox(self, payload, typePayload):
		eventBox = gtk.EventBox()
		if typePayload == "image":
			imageContainer =  gtk.Image()
			imageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(payload).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2))
			eventBox.add(imageContainer)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
		if typePayload == "letter":
			letterLabel = gtk.Label(payload)
			letterLabel.modify_font(pango.FontDescription("Courier Bold 60"))
			eventBox.add(letterLabel)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
			eventBox.set_size_request(LETTERS_SCALE[0], LETTERS_SCALE[1])
		if typePayload == "word":
			letterLabel = gtk.Label(payload)
			letterLabel.modify_font(pango.FontDescription("Courier Bold 30"))
			eventBox.add(letterLabel)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
			eventBox.set_size_request(LETTERS_SCALE[0], LETTERS_SCALE[1])
			
		return eventBox
			
		
	def selectFirtImage(self, firstEvenBox):
		availableColour =  self.getAvailableSelectionColour()
		self.changeBackgroundColour(firstEvenBox, availableColour['colour'])
		self.setSelectionStateColour(self.optionsSelectionState, 0, availableColour)
		self.currentOptionSelected = 0
		frameImageSelected = firstEvenBox.get_parent()
		self.fakeSelection(frameImageSelected)
		
	def disorderCorrespondences(self, items):
		
		optionsList = [None]*len(items)
		correspondencesList = [None]*len(items)
		
		indexsList = range(len(items))
		random.shuffle(indexsList)
	
		for index, item in enumerate(items):
			optionsList[index] = {"option":item.option, "indexPair": indexsList[index]}
			correspondencesList[indexsList[index]] = {"correspondence":item.correspondence, "indexPair": index}
		
		return (optionsList, correspondencesList)
	
	def checkCompletedExercise(self):
		result = True
		for key,imageSelectionState in self.optionsSelectionState.items():
			if (imageSelectionState['selected'] != imageSelectionState['pair']) or (self.correspondencesSelectionState[key]['selected'] != self.correspondencesSelectionState[key]['pair']) :
				result = False
				break
		if result:
			self.mainWindows.exerciseCompletedCallBack()
	
	def setAllAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			colour['available'] = True
			
	def getAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			if colour['available']:
				return colour
	
	def setAvailableColour(self, colour):
		COLOURS_ASSOCIATION[COLOURS_ASSOCIATION.index(colour)]['available'] = True
	
	def setUnavailableColour(self, colour):
		COLOURS_ASSOCIATION[COLOURS_ASSOCIATION.index(colour)]['available'] = False
		
	
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
			self.changeBackgroundColour(lastImageEvenBoxSelected, gtk.gdk.Color("white"))
			self.setSelectionStateColour(self.optionsSelectionState, self.lastOptionSelected, None)
			
			
		# Revisamos si ya existe una asociacion'''
		if self.optionsSelectionState[indexImageSelected]['selected'] == -1:
			# Aun no existe una asociación
			colorAvailable = self.getAvailableSelectionColour()
			self.changeBackgroundColour(imageEventBox, colorAvailable['colour'])
			self.setSelectionStateColour(self.optionsSelectionState, indexImageSelected, colorAvailable)
			
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		self.fakeSelection(frameImageSelected)
		lastFrameImageSelected = allImagesFrames[self.lastOptionSelected]
		self.fakeUnselection(lastFrameImageSelected)
		self.fakeUnselection
		
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
		if self.lastCorrespondenceSelected != -1:
			lastPairSelectionState = self.correspondencesSelectionState[self.lastCorrespondenceSelected]
		
		pairIndexCurrentImageSelected = -1
		imageEventBoxCurremtSelected = None
		if self.currentOptionSelected != -1:
			pairIndexCurrentImageSelected = self.optionsSelectionState[self.currentOptionSelected]['selected']
			imageEventBoxCurremtSelected = self.optionsSelectionState[self.currentOptionSelected]['colour']
		
		pairEventBoxCurrentImageSelected = None
		if self.currentOptionSelected != -1 and pairIndexCurrentImageSelected != -1:
			pairEventBoxCurrentImageSelected = allPairFrames[self.optionsSelectionState[self.currentOptionSelected]['selected']].get_children()[0]
		
		
		# Verificamos que el ultimo par seleccionado no tenga una asocicion
		if self.lastCorrespondenceSelected != -1 and lastPairSelectionState['selected'] == -1:
			lastPairEventBoxSelected = allPairFrames[self.lastCorrespondenceSelected].get_children()[0]
			self.changeBackgroundColour(self, lastPairEventBoxSelected, gtk.gdk.Color("white"))
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
				self.changeBackgroundColour(currentPairEventBoxSelected, gtk.gdk.Color("white"))
				self.setAvailableColour(self.correspondencesSelectionState[pairIndexCurrentImageSelected]['colour'])
				self.setSelectionStateColour(self.correspondencesSelectionState, pairIndexCurrentImageSelected, None )
				self.correspondencesSelectionState[pairIndexCurrentImageSelected]['selected'] = -1
				
				
			#El par seleccionado ya fue asociado por otra imagen, la cual no es la actualmente seleccionada
			if self.correspondencesSelectionState[indexPairSelected]['selected'] != -1 and self.correspondencesSelectionState[indexPairSelected]['selected'] != self.currentOptionSelected:
				#des-asociamos la imagen anterior asociada al par
				imagePairSelectedEventBox= allFramesImages[self.correspondencesSelectionState[indexPairSelected]['selected']].get_children()[0]
				self.changeBackgroundColour(imagePairSelectedEventBox,gtk.gdk.Color("white"))
				self.setAvailableColour(self.optionsSelectionState[self.correspondencesSelectionState[indexPairSelected]['selected']]['colour'])
				self.setSelectionStateColour(self.optionsSelectionState, self.correspondencesSelectionState[indexPairSelected]['selected'], None )
				self.optionsSelectionState[self.correspondencesSelectionState[indexPairSelected]['selected']]['selected'] = -1
			
			#guardamos los datos de la asociacion actuales de ambos lados
			self.correspondencesSelectionState[indexPairSelected]['selected'] = self.currentOptionSelected
			self.optionsSelectionState[self.currentOptionSelected]['selected'] = indexPairSelected
			self.setUnavailableColour(colourImageSelected)	
		else:
			# TODO: No hay imagen seleccionada, re-ver!
			'''colourAvailable =  self.getAvailableSelectionColour()
			pairEventBox.modify_bg(gtk.STATE_NORMAL, pairEventBox.get_colormap().alloc_color(colourAvailable['colour']))
			self.correspondencesSelectionState[indexPairSelected]['colour'] = colourAvailable'''
			
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		self.fakeSelection(framePairSelected)
		lastFramePairSelected = allPairFrames[self.lastCorrespondenceSelected]
		self.fakeUnselection(lastFramePairSelected)
		
		#Comprabamos la finalización del ejercicio
		self.checkCompletedExercise()
	
	def fakeSelection(self, frame):
		frame.modify_bg(gtk.STATE_NORMAL, SELECTED_COLOUR)
	
	def fakeUnselection(self, frame)	:
		frame.modify_bg(gtk.STATE_NORMAL, frame.get_colormap().alloc_color('white'))
	
	def changeBackgroundColour(self, eventBox, colour):
		eventBox.modify_bg(gtk.STATE_NORMAL, colour)
		
	def setSelectionStateColour(self,selectionState, index, colour):
		selectionState[index]['colour'] = colour
	

	
