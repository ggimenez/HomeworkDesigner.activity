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

from modalwindowselectItem import ModalWindowSelectItem


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



class SearchTheSameTemplate():	
		
	
		
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
	
	
	def fakeSelection(self, eventBox, colour):
		
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
	
	def givemeMapTable(self, rows, columns):
		theMatrix = [[None] * columns for i in range(rows)]
		
		row = 0
		while row < rows :
			column = 0
			#self.mainWindows.getLogger().debug("row: %s" % row)
			while column < columns: 
				#self.mainWindows.getLogger().debug("column: %s" % column)
				isFoundMap = False				
				
				self.mainWindows.getLogger().debug(theMatrix)
				if theMatrix[row][column] == None :				
					while (isFoundMap is False):
						rowMap = random.randint(0, 3)
						columnMap = random.randint(0,3)					
					
						self.mainWindows.getLogger().debug("-------------------------------")
						self.mainWindows.getLogger().debug(row)
						self.mainWindows.getLogger().debug(column)	
						self.mainWindows.getLogger().debug(rowMap)
						self.mainWindows.getLogger().debug(columnMap)

						if (rowMap != row or columnMap != column) and theMatrix[rowMap][columnMap] is None:
							theMatrix[row][column] = [rowMap,columnMap]			
							theMatrix[rowMap][columnMap] = [row,column]
							isFoundMap = True
				column = column + 1
			row = row + 1
		self.mainWindows.getLogger().debug(theMatrix)
		self.mainWindows.getLogger().debug("exit from givemeMapTable")
		return theMatrix

	def modalWindowReturn(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
                self.mainWindows.getLogger().debug(item)
                copyMethod = None

                #indexCurrentEventBox = self.currentHBoxItems.child_get_property(self.currentEventBoxSelected, "position")

		itemCopy = self.copyItem(item, itemType, args)
                oldItem = self.currentEventBoxSelected.get_children()[0]
                self.currentEventBoxSelected.remove(oldItem)
                self.currentEventBoxSelected.add(itemCopy)
                self.currentEventBoxSelected.show_all()
		colour = self.getAvailableSelectionColour()
		self.setUnavailableColour(colour)
		self.fakeSelection(self.currentEventBoxSelected, colour)	
	
		self.payloads.append(itemCopy)

		hBox = self.currentEventBoxSelected.get_parent()
		vBox  = hBox.get_parent()
		
		self.mainWindows.getLogger().debug(self.currentColumnPairIndex)
		self.mainWindows.getLogger().debug(self.currentRowPairIndex)
		#self.mainWindows.getLogger().debug(hBox.get_children()[self.currentColumnPairIndex])

		pairEventBox = vBox.get_children()[self.currentRowPairIndex].get_children()[self.currentColumnPairIndex]
		itemCopyPair = self.copyItem(item, itemType, args)
                oldItemPair = pairEventBox.get_children()[0]
                pairEventBox.remove(oldItemPair)
                pairEventBox.add(itemCopyPair)
		self.fakeSelection(pairEventBox, colour)
                pairEventBox.show_all()
		
	


	def copyItem(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside to copyItem:")
                self.mainWindows.getLogger().debug(itemType)
                itemCopy = None
                if itemType == "text":
                        itemCopy = gtk.Label(item.get_text())
                        itemCopy.modify_font(pango.FontDescription("Courier Bold 40"))
                elif itemType == "image":
                        itemCopy = gtk.image_new_from_pixbuf(item.get_pixbuf())
			itemCopy.imageName = args['imageName']
			itemCopy.imageType = args['imageType']
                return itemCopy


	def cellSelectedCallBack(self, eventBox, *args):
		self.mainWindows.getLogger().debug("inside to cellSelectedCallBack")
		self.mainWindows.getLogger().debug(args)
		dialogInsertNewItem = ModalWindowSelectItem(self.mainWindows, self)
                dialogInsertNewItem.show()
		self.currentEventBoxSelected = eventBox
		self.currentRowPairIndex = self.mapTable[args[1]][args[2]][0]
		self.currentColumnPairIndex = self.mapTable[args[1]][args[2]][1]

		
			
	
	
	def getWindow(self, mainWindows):
		
		self.mainWindows = mainWindows
			
		windowSearchTheSame= gtk.ScrolledWindow()
		windowSearchTheSame.exerciseName = "SearchTheSameTemplate"		
		windowSearchTheSame.exerciseInstance = self		
	
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(False, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		
		frameExercises.add(vBoxExercises)
		
		
		vBox = gtk.VBox(True, 0)
		columns = 4
		rows = 4
		
		rowsCount = 0
		self.setAllAvailableSelectionColour()
		self.mapTable = self.givemeMapTable(rows, columns)
		self.payloads = []
		while rowsCount < (rows):
			
			hBox = gtk.HBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				
				eventBox = self.blankEventBox()
				
				eventBox.connect("button-press-event", self.cellSelectedCallBack, rowsCount, countColumns)
				hBox.pack_start(eventBox, True,True,5)
				countColumns = countColumns + 1
			
			vBox.pack_start(hBox, True,True,5)
			rowsCount = rowsCount + 1
		
		vBoxExercises.pack_start(vBox, False,False,0)
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
	
	
	def parseToJson(self):
                theExerciseJson = {}
                theExerciseJson['codeType'] = 3
                theExerciseJson['items'] = []
                itemsToCopy = []
                if len(self.payloads) < 8:
			return (None, None, False, "All items must be filled")
		for payload in self.payloads:
                        self.mainWindows.getLogger().debug("Hframe child: ")
                        theExerciseJson['items'].append(self.parsePayloadToJson(payload, itemsToCopy))
                return (theExerciseJson, itemsToCopy, True, None)

        def parsePayloadToJson(self, payload, itemsToCopy):
                self.mainWindows.getLogger().debug(" Inside to parseToJson")
                theJson = {}
                self.mainWindows.getLogger().debug(payload.__class__.__name__)
                if payload.__class__.__name__ == "Label":
                        theJson['type'] = "letter"
                        theJson["value"] = payload.get_text()
                if payload.__class__.__name__ == "Image":
                        theJson['type'] = "image"
                        theJson['value'] = "./images/" + payload.imageName
                        itemsToCopy.append({"type":"image", "value":payload, "fileName":payload.imageName, "fileType":payload.imageType})
                return theJson	
