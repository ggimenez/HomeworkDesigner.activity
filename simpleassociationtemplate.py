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

from sugar.graphics.objectchooser import ObjectChooser
from sugar.graphics.entry import CanvasEntry
from modalwindowselectItem import ModalWindowSelectItem
''' Scales '''
IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]

'''Curren item selection association'''
SELECTED_COLOUR = gtk.gdk.Color("#FFFF00")



class SimpleAssociationTemplate():
	
	def getWindow(self, mainWindows):
		
		self.mainWindows = mainWindows
		windowSimpleAssociation = gtk.ScrolledWindow()
		windowSimpleAssociation.exerciseName =  "SimpleAssociationTemplate"		
				
	
		vBoxWindows = gtk.VBox(False, 5)
		hBoxExercises = gtk.HBox(True, 50)
		self.vBoxOptions = gtk.VBox(True, 5)
		self.vBoxCorrespondences = gtk.VBox(True, 5)
		
		frameExercises = gtk.Frame() 
		frameExercises.add(hBoxExercises)
	
		windowSimpleAssociation.exerciseInstance = self

	
		itemCount = 1
		while itemCount <= 5:
			
			'''Options'''
			eventBoxOption = self.createEventBox()
			eventBoxOption.connect("button-press-event", self.itemSelectedCallBack)
			self.addEventBoxToVBox(eventBoxOption, self.vBoxOptions)			
			
			'''Correspondences'''
			eventBoxCorrespondence = self.createEventBox()
			eventBoxCorrespondence.connect("button_press_event", self.itemSelectedCallBack)
			self.addEventBoxToVBox(eventBoxCorrespondence, self.vBoxCorrespondences)
			#self.correspondencesSelectionState[index] = {"selected": -1, "pair": correspondencesList[index]['indexPair'], "colour": None}	
			itemCount = itemCount + 1
			
		hBoxExercises.pack_start(self.vBoxOptions, False,True,50)
		hBoxExercises.pack_start(self.vBoxCorrespondences, False,True,50)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		
		windowSimpleAssociation.add_with_viewport(vBoxWindows)
				
		return windowSimpleAssociation
	
	def itemSelectedCallBack(self, eventBox, *args):
		self.mainWindows.getLogger().debug("Inside: itemSelectedCallBack")
		dialogInsertNewItem = ModalWindowSelectItem(self.mainWindows, self)
		dialogInsertNewItem.show()
		self.currentEventBoxSelected = eventBox
      		self.mainWindows.getLogger().debug("after of show() in itemSelectedCallBack")	

        def modalWindowReturn(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
		self.mainWindows.getLogger().debug(item)
		oldItem = self.currentEventBoxSelected.get_children()[0]
		self.currentEventBoxSelected.remove(oldItem)
		self.currentEventBoxSelected.filled = True 		

		if itemType == "text":
			item.modify_font(pango.FontDescription("Courier Bold 60"))

		
		self.currentEventBoxSelected.add(item)
		self.currentEventBoxSelected.show_all()


	def addEventBoxToVBox(self, eventBox, vBox):
		frameEventBox = gtk.Frame() 
		frameEventBox.add(eventBox)
		vBox.pack_start(frameEventBox, False,False,0)
		
	def createEventBox(self):
		eventBox = gtk.EventBox()
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription("Courier Bold 70"))
		eventBox.add(blankLabel)
		eventBox.set_size_request(LETTERS_SCALE[0], LETTERS_SCALE[1])	        
		eventBox.filled = False
			
		return eventBox
				
	def parseToJson(self):
		theExerciseJson = {}
                theExerciseJson['codeType'] = 1
                theExerciseJson['name'] = "Asociacion Simple" 
		theExerciseJson['items'] = []
		itemsToCopy = []
		for index, option in enumerate(self.vBoxOptions.get_children()):

			theEventBoxOption = option.get_children()[0]			
			theEventBoxCorrespondence = self.vBoxCorrespondences.get_children()[index].get_children()[0]
			if theEventBoxOption.filled == True and theEventBoxCorrespondence.filled == True:
				payloadOption = theEventBoxOption.get_children()[0]
				payloadCorrespondence = theEventBoxCorrespondence.get_children()[0]
				item = {}
				item['option'] = self.parsePayloadToJson(payloadOption, itemsToCopy)
				item['correspondence'] = self.parsePayloadToJson(payloadCorrespondence, itemsToCopy)
				theExerciseJson['items'].append(item)
		return (theExerciseJson, itemsToCopy, True, None)				
								
	def parsePayloadToJson(self, payload, itemsToCopy):
		self.mainWindows.getLogger().debug(" Inside to parseToJson")
		theJson = {}
		self.mainWindows.getLogger().debug(payload.__class__.__name__)
		if payload.__class__.__name__ == "Label":
			theJson['type']	= "letter"
			theJson["value"] = payload.get_text()
		if payload.__class__.__name__ == "Image":
			theJson['type'] = "image"
			theJson['value'] = "./images/" + payload.imageName
			itemsToCopy.append({"type":"image", "value":payload, "fileName":payload.imageName, "fileType":payload.imageType})
		return theJson							

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
	
	
	def fakeSelection(self, frame):
		frame.modify_bg(gtk.STATE_NORMAL, SELECTED_COLOUR)
	
	def fakeUnselection(self, frame)	:
		frame.modify_bg(gtk.STATE_NORMAL, frame.get_colormap().alloc_color('white'))
	
	def changeBackgroundColour(self, eventBox, colour):
		eventBox.modify_bg(gtk.STATE_NORMAL, colour)
		
	def setSelectionStateColour(self,selectionState, index, colour):
		selectionState[index]['colour'] = colour
	
