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
		
		#self.selectFirtImage(firstOptionEventBox)
		
		return windowSimpleAssociation
	
	def itemSelectedCallBack(self, eventBox, *args):
		self.mainWindows.getLogger().debug("Inside: itemSelectedCallBack")
		chooser = ObjectChooser(parent=self.mainWindows, what_filter='Image')
		result = chooser.run()
	
	
	def addEventBoxToVBox(self, eventBox, vBox):
		frameEventBox = gtk.Frame() 
		frameEventBox.add(eventBox)
		vBox.pack_start(frameEventBox, False,False,0)
		
	def createEventBox(self):
		eventBox = gtk.EventBox()
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("gray"))
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription("Courier Bold 70"))
		eventBox.add(blankLabel)
			
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
	
