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
		
		vBoxWindows = gtk.VBox(False, 5)
		hBoxExercises = gtk.HBox(True, 50)
		vBoxOptions = gtk.VBox(True, 5)
		vBoxCorrespondences = gtk.VBox(True, 5)
		
		frameExercises = gtk.Frame() 
		frameExercises.add(hBoxExercises)
		
		itemCount = 1
		while itemCount <= 5:
			
			'''Options'''
			eventBoxOption = self.createEventBox()
			eventBoxOption.connect("button-press-event", self.itemSelectedCallBack)
			self.addEventBoxToVBox(eventBoxOption, vBoxOptions)			
			
			'''Correspondences'''
			eventBoxCorrespondence = self.createEventBox()
			eventBoxCorrespondence.connect("button_press_event", self.itemSelectedCallBack)
			self.addEventBoxToVBox(eventBoxCorrespondence, vBoxCorrespondences)
			#self.correspondencesSelectionState[index] = {"selected": -1, "pair": correspondencesList[index]['indexPair'], "colour": None}	
			itemCount = itemCount + 1
			
		hBoxExercises.pack_start(vBoxOptions, False,True,50)
		hBoxExercises.pack_start(vBoxCorrespondences, False,True,50)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		
		windowSimpleAssociation.add_with_viewport(vBoxWindows)
				
		return windowSimpleAssociation
	
	def itemSelectedCallBack(self, eventBox, *args):
		self.mainWindows.getLogger().debug("Inside: itemSelectedCallBack")
		dialogInsertNewItem = ModalWindowSelectItem(self.mainWindows, self)
		dialogInsertNewItem.show()
		self.currentEventBoxSelected = eventBox
      		self.mainWindows.getLogger().debug("after of show() in itemSelectedCallBack")	

        def modalWindowReturn(self, item):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
		self.mainWindows.getLogger().debug(item)
		oldItem = self.currentEventBoxSelected.get_children()[0]
		self.currentEventBoxSelected.remove(oldItem)
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
		
		return eventBox
				
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
	
