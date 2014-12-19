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


'''Color Selection association
Reference of colours codes :http://www.rapidtables.com/web/color/RGB_Color.htm
'''
COLOURS_ASSOCIATION = []
#Marron
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#800000"), "available":True})
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
#chocolate
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#D2691E"), "available":True})
#Gray
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#808080"), "available":True})


IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]



class SearchTheSame():
	
		
	def blankEventBox(self):
		eventBox = gtk.EventBox()
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription("Courier Bold 50"))
		eventBox.add(blankLabel)
		return eventBox
	
	
		
	def setAllAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			colour['available'] = True
			
	def getAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			if colour['available']:
					return colour

	def setUnavailableColour(self, colour):
		COLOURS_ASSOCIATION[COLOURS_ASSOCIATION.index(colour)]['available'] = False
	
	
	def fakeSelection(self, eventBox):
		
		colour = self.getAvailableSelectionColour()
		eventBox.modify_bg(gtk.STATE_NORMAL, colour['colour'])
		return colour
		
	def fakeUnselection(self, eventBox):
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
		oldPayload = eventBox.get_children()[0]
		eventBox.remove(oldPayload)
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription("Courier Bold 50"))
		eventBox.add(blankLabel)
		eventBox.show_all()
		
	def changeEventBoxPayload(self, rowIndex, columnIndex, eventBox):
		oldPayload = eventBox.get_children()[0]
		eventBox.remove(oldPayload)
		payload = self.payloads[self.mapTable[rowIndex][columnIndex][2]]
		if payload.type == "letter":
			letterLabel = gtk.Label(payload.value)
			letterLabel.modify_font(pango.FontDescription("Courier Bold 50"))
			eventBox.add(letterLabel)
			eventBox.show_all()
		elif payload.type == "image":
			image = gtk.Image()
                        image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(\
                                payload.value ).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2))
			eventBox.add(image)
			eventBox.show_all()
                        '''payloadResume.imageName = jsonItem['fileName']
                        payloadResume.imageType = jsonItem['fileType
                        args = {"imageName": jsonItem['fileName'],"imageType": jsonItem['fileType']}'''
	

	
	def cellSelectedCallBack(self, eventBox, *args):
		
		self.mainWindows.getLogger().debug("Inside to cellSelectedCallBack")	
		hBox = eventBox.get_parent()
		columnIndex = hBox.child_get_property(eventBox, "position")
		
		vBox = hBox.get_parent()
		rowIndex = vBox.child_get_property(hBox, "position")
		
		self.changeEventBoxPayload(rowIndex, columnIndex, eventBox)
		colour = self.fakeSelection(eventBox)
		
		if self.lastCellSelected == None:
			self.lastCellSelected = [rowIndex,columnIndex]
		elif self.lastCellSelected != [rowIndex,columnIndex]:
			lastEventBoxSelectedRow = self.lastCellSelected[0]
			lastEventBoxSelectedColumn = self.lastCellSelected[1]
			lastEventBoxSelectedHBox = vBox.get_children()[lastEventBoxSelectedRow]
			lastEventBoxSelected = lastEventBoxSelectedHBox.get_children()[lastEventBoxSelectedColumn]
			pairSelected = []
			pairSelected.append(self.mapTable[rowIndex][columnIndex][0])
			pairSelected.append(self.mapTable[rowIndex][columnIndex][1])

			self.mainWindows.getLogger().debug(self.lastCellSelected)
			self.mainWindows.getLogger().debug(pairSelected)
			if self.lastCellSelected != pairSelected:
				
				self.fakeUnselection(lastEventBoxSelected)
				#lastEventBoxSelected.get_children()[0].set_text("")
				self.lastCellSelected =[rowIndex,columnIndex]
			
			else :
				handlerId = self.mapTable[rowIndex][columnIndex][3]
				lastEventBoxHandlerId = self.mapTable[lastEventBoxSelectedRow][lastEventBoxSelectedColumn][3]
				self.matches = self.matches + 1
				eventBox.disconnect(handlerId)
				lastEventBoxSelected.disconnect(lastEventBoxHandlerId)
				self.lastCellSelected = None
				self.setUnavailableColour(colour)
				
		if self.matches == 8:
			self.mainWindows.exerciseCompletedCallBack()
				
		
	
	def getWindow(self, exercise, mainWindows):
	
				
			
		self.mainWindows = mainWindows
		self.mainWindows.getLogger().debug("Inside to getWindow()")
		self.mainWindows.getLogger().debug(exercise)		
	
		windowSearchTheSame= gtk.ScrolledWindow()
		
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(False, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		
		vBox = gtk.VBox(True, 0)
		columns = 4
		rows = 4
		
		rowsCount = 0
		#self.storeSelectionState = self.createStoreSelection(exercise)
		self.mapTable = exercise.mapTable
		#self.addPayloadToMapTable(exercise['items'])
		self.setAllAvailableSelectionColour()
		self.payloads = exercise.items
		self.lastCellSelected = None
		self.matches = 0
		while rowsCount < (rows):
			
			hBox = gtk.HBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				
				eventBox = self.blankEventBox()
				handlerId  = eventBox.connect("button-press-event", self.cellSelectedCallBack)
				self.mapTable[rowsCount][countColumns].append(handlerId)
				
				hBox.pack_start(eventBox, True,True,5)
				countColumns = countColumns + 1
			
			vBox.pack_start(hBox, True,True,5)
			rowsCount = rowsCount + 1
		
		vBoxExercises.pack_start(vBox, False,False,0)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
	
