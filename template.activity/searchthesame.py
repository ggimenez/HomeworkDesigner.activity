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



class SearchTheSame():
	
		
	
	def createStoreSelection(self, exercise):
		
		items = exercise.items
		indexsCountUse = [0]*8
		pairTracker = [None]*8
		
		storeSelectionState = [[None for i in range(4)] for j in range(4)]
		
		rows = 4
		rowsCount = 0
		columns = 4
		
		self.lastCellSelected = None
		self.matches = 0
		
		while rowsCount < rows :
			columnsCount = 0
			while columnsCount < columns:
				indexFound = False
				while indexFound == False:
					indexToUse = random.randint(0,7)
					
					if indexsCountUse[indexToUse] < 2:
						
						if indexsCountUse[indexToUse] == 0 :
							pairTracker[indexToUse] = [rowsCount,columnsCount]
						else: 					
							storeSelectionState[rowsCount][columnsCount] = {"type": items[indexToUse].type, "value": items[indexToUse].value, "pair":pairTracker[indexToUse]}
							storeSelectionState[pairTracker[indexToUse][0]][pairTracker[indexToUse][1]] = {"type": items[indexToUse].type,"value": items[indexToUse].value, "pair":[rowsCount,columnsCount]}
							
						indexFound = True
						indexsCountUse[indexToUse] = indexsCountUse[indexToUse] + 1
						
				columnsCount = columnsCount + 1
			
			rowsCount = rowsCount + 1
		
		return storeSelectionState
	
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
		
	def fakeUnselection(self, eventBox)	:
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
		if self.storeSelectionState[rowIndex][columnIndex]['type'] == "letter":
			letterLabel = gtk.Label(self.storeSelectionState[rowIndex][columnIndex]['value'])
			letterLabel.modify_font(pango.FontDescription("Courier Bold 50"))
			eventBox.add(letterLabel)
			eventBox.show_all()
	
	def cellSelectedCallBack(self, eventBox, *args):
		
		vBox = eventBox.get_parent()
		rowIndex = vBox.child_get_property(eventBox, "position")
		
		hBox = vBox.get_parent()
		columnIndex = hBox.child_get_property(vBox, "position")
		
		self.changeEventBoxPayload(rowIndex, columnIndex, eventBox)
		colour = self.fakeSelection(eventBox)
		
		if self.lastCellSelected == None:
			self.lastCellSelected = [rowIndex,columnIndex]
		elif self.lastCellSelected != [rowIndex,columnIndex]:
			lastEventBoxSelectedRow = self.lastCellSelected[0]
			lastEventBoxSelectedColumn = self.lastCellSelected[1]
			lastEventBoxSelectedVBox = hBox.get_children()[lastEventBoxSelectedColumn]
			lastEventBoxSelected = lastEventBoxSelectedVBox.get_children()[lastEventBoxSelectedRow]
			if self.lastCellSelected != self.storeSelectionState[rowIndex][columnIndex]['pair']:
				
				self.fakeUnselection(lastEventBoxSelected)
				#lastEventBoxSelected.get_children()[0].set_text("")
				self.lastCellSelected =[rowIndex,columnIndex]
			
			else :
				handlerId = self.storeSelectionState[rowIndex][columnIndex]['handlerId']
				lastEventBoxHandlerId = self.storeSelectionState[lastEventBoxSelectedRow][lastEventBoxSelectedColumn]['handlerId']
				self.matches = self.matches + 1
				eventBox.disconnect(handlerId)
				lastEventBoxSelected.disconnect(lastEventBoxHandlerId)
				self.lastCellSelected = None
				self.setUnavailableColour(colour)
				
		if self.matches == 8:
			self.mainWindows.exerciseCompletedCallBack()
				
	
	
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
			
		windowSearchTheSame= gtk.ScrolledWindow()
		
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(False, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		
		hBox = gtk.HBox(True, 0)
		columns = 4
		rows = 4
		
		rowsCount = 0
		self.storeSelectionState = self.createStoreSelection(exercise)
		self.setAllAvailableSelectionColour()
		while rowsCount < (rows):
			
			vBox = gtk.VBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				
				eventBox = self.blankEventBox()
				handlerId  = eventBox.connect("button-press-event", self.cellSelectedCallBack)
				self.storeSelectionState[countColumns][rowsCount]['handlerId'] = handlerId
				vBox.pack_start(eventBox, False,False,5)
				countColumns = countColumns + 1
			
			hBox.pack_start(vBox, True,True,5)
			rowsCount = rowsCount + 1
		
		vBoxExercises.pack_start(hBox, False,False,0)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
	
