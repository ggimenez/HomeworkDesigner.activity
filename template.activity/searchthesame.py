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
#royal blue
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#4169E1"), "available":True, "id":0})
#medium sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#3CB371"), "available":True, "id":1})
#teal
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#008080"), "available":True, "id":2})
#sienna
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#A0522D"), "available":True, "id":3})
#dark sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#BA55D3"), "available":True, "id":4})
#wheat
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#F5DEB3"), "available":True, "id":5})
#chocolate
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#D2691E"), "available":True, "id":6})
#Gray
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#808080"), "available":True, "id":7})


IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]

FONT_DESCRIPTION_BIG = 'DejaVu Bold 40'
FONT_DESCRIPTION_MEDIUM = 'DejaVu Bold 20'

EVENTBOX_SCALE = [100,100]


class SearchTheSame():
		
	def blankEventBox(self):
		eventBox = gtk.EventBox()
		eventBox.set_size_request(EVENTBOX_SCALE[0], EVENTBOX_SCALE[1])
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
		blankLabel = gtk.Label("")
		eventBox.add(blankLabel)
		return eventBox	
		
	def setAllAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			colour['available'] = True
			
	def getAvailableSelectionColour(self):
		for colour in COLOURS_ASSOCIATION:
			if colour['available']:
				return colour
	def getColourByID(self, id):
		for colour in COLOURS_ASSOCIATION:
			if colour['id'] == id:
				return colour
	
	def setUnavailableColourByID(self,id):
		for colour in COLOURS_ASSOCIATION:
			if colour['id'] == id:
				colour['available'] = False
				break

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
		eventBox.add(blankLabel)
		eventBox.show_all()
		
	def changeEventBoxPayload(self, rowIndex, columnIndex, eventBox):
		oldPayload = eventBox.get_children()[0]
		eventBox.remove(oldPayload)
		payload = self.payloads[self.mapTable[rowIndex][columnIndex][2]]
		if payload.type == "letter":
			letterLabel = gtk.Label(payload.value)
			if len(payload.value) <= 8:
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))

			eventBox.add(letterLabel)
			eventBox.show_all()
		elif payload.type == "image":
			image = gtk.Image()
			pixbuf = gtk.gdk.pixbuf_new_from_file(payload.value)
                        image.set_from_pixbuf(pixbuf)
			eventBox.add(image)
			eventBox.show_all()
        def repaintTable(self):
		for itemIndexes in self.itemsIndexMatches:
			self.mainWindows.getLogger().debug(self.mapTable)
			firstEventBox = self.vBox.get_children()[itemIndexes[0]].get_children()[itemIndexes[1]]
			self.changeEventBoxPayload(itemIndexes[0], itemIndexes[1], firstEventBox)
			firstEventBox.disconnect( self.mapTable[itemIndexes[0]][itemIndexes[1]][3])
			colour = self.getColourByID(itemIndexes[2])
			firstEventBox.modify_bg(gtk.STATE_NORMAL, colour['colour'])
			self.setUnavailableColourByID(itemIndexes[2])	

			
			rowPairEventBox = self.mapTable[itemIndexes[0]][itemIndexes[1]][0]
			columnPairEventBox =  self.mapTable[itemIndexes[0]][itemIndexes[1]][1]
			handlerIdPairEventBox =  self.mapTable[rowPairEventBox][columnPairEventBox][3]
			pairEventBox = self.vBox.get_children()[rowPairEventBox].get_children()[columnPairEventBox]
		        self.changeEventBoxPayload(rowPairEventBox, columnPairEventBox, pairEventBox)
			pairEventBox.disconnect(handlerIdPairEventBox)
			pairEventBox.modify_bg(gtk.STATE_NORMAL, colour['colour'])
        
	
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
				self.lastCellSelected =[rowIndex,columnIndex]
			
			else :
				handlerId = self.mapTable[rowIndex][columnIndex][3]
				lastEventBoxHandlerId = self.mapTable[lastEventBoxSelectedRow][lastEventBoxSelectedColumn][3]
				self.matches = self.matches + 1
				self.itemsIndexMatches.append([rowIndex, columnIndex, colour["id"]])
				eventBox.disconnect(handlerId)
				lastEventBoxSelected.disconnect(lastEventBoxHandlerId)
				self.lastCellSelected = None
				self.setUnavailableColour(colour)
				
		if self.matches == self.matchesToDo:
			self.mainWindows.exerciseCompletedCallBack()
			
	def saveExerciseState(self):
                self.mainWindows.getLogger().debug("Inside to saveExerciseState")
                stateJson = {}
                stateJson['itemsIndexMatches'] = self.itemsIndexMatches
		stateJson['matchesToDo'] = self.matchesToDo
		stateJson['matches'] = self.matches
                stateJson['lastCellSelected'] = self.lastCellSelected
		return stateJson

	def disconnectEventBoxs(self):
		pass	
	
	def getWindow(self, exercise, mainWindows, stateJson):
				
		self.mainWindows = mainWindows
		self.mainWindows.getLogger().debug("Inside to getWindow()")
		self.mainWindows.getLogger().debug(exercise)		
		
	
		windowSearchTheSame= gtk.ScrolledWindow()
		windowSearchTheSame.exerciseInstance = self
				
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(True, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		
		self.vBox = gtk.VBox(True, 0)
		self.level = exercise.level
		
		if self.level is 1:
			rows = 4
			columns = 2
			self.matchesToDo = 4
		elif self.level is 2:
			rows = 4
			columns = 4
			self.matchesToDo = 8		
		rowsCount = 0	
		self.mapTable = exercise.mapTable
		
		self.setAllAvailableSelectionColour()
		self.payloads = exercise.items
		self.lastCellSelected = None
		self.matches = 0
		self.itemsIndexMatches = []
		if stateJson is not None:
			self.lastCellSelected = stateJson['lastCellSelected']
			self.matches = stateJson['matches']
			self.itemsIndexMatches = stateJson['itemsIndexMatches']
		while rowsCount < (rows):
			
			hBox = gtk.HBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				
				eventBox = self.blankEventBox()
				handlerId  = eventBox.connect("button-press-event", self.cellSelectedCallBack)
				self.mapTable[rowsCount][countColumns].append(handlerId)

				hBox.pack_start(eventBox, True,True,5)
				countColumns = countColumns + 1
			
			self.vBox.pack_start(hBox, True,True,5)
			rowsCount = rowsCount + 1
		if stateJson is not None:
			self.repaintTable()	

	
		vBoxExercises.pack_start(self.vBox, True,False,0)
		vBoxWindows.pack_start(frameExercises, True,False,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
	
