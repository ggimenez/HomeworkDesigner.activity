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

from gettext import gettext as _

'''Color Selection association
Reference of colours codes :http://www.rapidtables.com/web/color/RGB_Color.htm
'''
COLOURS_ASSOCIATION = []
#royal blue
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#4169E1"), "available":True})
#medium sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#3CB371"), "available":True})
#teal
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#008080"), "available":True})
#sienna
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#A0522D"), "available":True})
#dark sea green
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#BA55D3"), "available":True})
#wheat
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#F5DEB3"), "available":True})
#chocolate
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#D2691E"), "available":True})
#Gray
COLOURS_ASSOCIATION.append({"colour":gtk.gdk.Color("#808080"), "available":True})

IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]

EVENTBOX_SCALE = [100,100]

FONT_DESCRIPTION_BIG = 'DejaVu Bold 40'
FONT_DESCRIPTION_MEDIUM = 'DejaVu Bold 20'

MAXIMUM_LETTER_LENGTH_BIG = 8

class SearchTheSameTemplate():	
			
		
	def blankEventBox(self):
		eventBox = gtk.EventBox()
		eventBox.set_size_request(EVENTBOX_SCALE[0], EVENTBOX_SCALE[1])
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
		eventBox.add(blankLabel)
		eventBox.isBlank = True
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
		
	def fakeUnselection(self, eventBox):
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
		oldPayload = eventBox.get_children()[0]
		eventBox.remove(oldPayload)
		blankLabel = gtk.Label("")
		blankLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
		eventBox.add(blankLabel)
		eventBox.show_all()
		
	def changeEventBoxPayload(self, rowIndex, columnIndex, eventBox):
		oldPayload = eventBox.get_children()[0]
		eventBox.remove(oldPayload)
		if self.storeSelectionState[rowIndex][columnIndex]['type'] == "letter":
			letterLabel = gtk.Label(self.storeSelectionState[rowIndex][columnIndex]['value'])
			if len(self.storeSelectionState[rowIndex][columnIndex]['value']) <= MAXIMUM_LETTER_LENGTH_BIG:
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:
				letterLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))
	
			eventBox.add(letterLabel)
			eventBox.show_all()
	
	def givemeMapTable(self, rows, columns):
		theMatrix = [[None] * columns for i in range(rows)]
		
		row = 0
		itemIndex = None
		if self.level is 1:
			itemIndex = [0,1,2,3]
		elif self.level is 2:		
			itemIndex = [0,1,2,3,4,5,6,7]

		currentItemIndex = 0
		while row < rows :
			column = 0
			#self.mainWindows.getLogger().debug("row: %s" % row)
			while column < columns: 
				#self.mainWindows.getLogger().debug("column: %s" % column)
				isFoundMap = False				
				
				self.mainWindows.getLogger().debug(theMatrix)
				if theMatrix[row][column] == None :				
					while (isFoundMap is False):
						rowMap = random.randint(0, (rows - 1))
						columnMap = random.randint(0,(columns - 1))					
						
						if (rowMap != row or columnMap != column) and theMatrix[rowMap][columnMap] is None:
							theMatrix[row][column] = [rowMap,columnMap, itemIndex[currentItemIndex]]			
							theMatrix[rowMap][columnMap] = [row,column, itemIndex[currentItemIndex]]
							currentItemIndex = currentItemIndex + 1
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

		itemCopy = self.copyItem(item, itemType, args)
        	oldItem = self.currentEventBoxSelected.get_children()[0]
                self.currentEventBoxSelected.remove(oldItem)
                self.currentEventBoxSelected.add(itemCopy)
                self.currentEventBoxSelected.show_all()
		

		itemIndex = self.mapTable[self.currentRowPairIndex][self.currentColumnPairIndex][2]
		self.payloads[str(itemIndex)] = [itemCopy, self.currentRowPairIndex, self.currentColumnPairIndex]

		hBox = self.currentEventBoxSelected.get_parent()
		vBox  = hBox.get_parent()
		
		self.mainWindows.getLogger().debug(self.currentColumnPairIndex)
		self.mainWindows.getLogger().debug(self.currentRowPairIndex)	

		pairEventBox = vBox.get_children()[self.currentRowPairIndex].get_children()[self.currentColumnPairIndex]
		itemCopyPair = self.copyItem(item, itemType, args)
                oldItemPair = pairEventBox.get_children()[0]
                pairEventBox.remove(oldItemPair)
                pairEventBox.add(itemCopyPair)
		pairEventBox.show_all()		

		if self.currentEventBoxSelected.isBlank is True:	        
			colour = self.getAvailableSelectionColour()
			self.setUnavailableColour(colour)
			self.fakeSelection(self.currentEventBoxSelected, colour)	
			self.currentEventBoxSelected.isBlank = False
			self.fakeSelection(pairEventBox, colour)
               		pairEventBox.isBlank = False
			

	def copyItem(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside to copyItem:")
                self.mainWindows.getLogger().debug(itemType)
                itemCopy = None
                if itemType == "text" or itemType == "letter":
                        itemCopy = gtk.Label(item.get_text())
	                if len(item.get_text()) <= MAXIMUM_LETTER_LENGTH_BIG:
				itemCopy.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
        		else:	
				itemCopy.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))
	        elif itemType == "image":
                        itemCopy = gtk.image_new_from_pixbuf(item.get_pixbuf().scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2)) 			
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
	
	def changeLevel(self, newLevel):
                newWindow = self.getWindow(self.mainWindows, None, newLevel)
                return newWindow

	def getWindow(self, mainWindows, jsonState, level):
		
		self.mainWindows = mainWindows
			
		windowSearchTheSame= gtk.ScrolledWindow()
		windowSearchTheSame.exerciseName = "SearchTheSameTemplate"		
		windowSearchTheSame.exerciseInstance = self		
	
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(True, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		
		frameExercises.add(vBoxExercises)
		
		
		vBox = gtk.VBox(True, 0)
		
		rowsCount = 0
		self.setAllAvailableSelectionColour()
		self.level = level	
		self.mapTable = None
		if jsonState is not None:
			self.level = jsonState['level']
		
		rows = -1
		columns = -1
		if self.level is 1:
			columns = 2
			rows = 4
		elif self.level is 2:
			columns =  4
			rows = 4	
	
		self.payloads = {}
		while rowsCount < (rows):
			
			hBox = gtk.HBox(False, 0)
			countColumns = 0
			while countColumns < (columns):
								
				eventBox = self.blankEventBox()	
				eventBox.connect("button-press-event", self.cellSelectedCallBack, rowsCount, countColumns)
				hBox.pack_start(eventBox, True,True,5)
				countColumns = countColumns + 1
			
			vBox.pack_start(hBox, True,True,5)
			rowsCount = rowsCount + 1
		
		if jsonState is not None:
                        self.mapTable = jsonState['mapTable']
              		rowsCount = 0
			columnsCount = 0
			for index, jsonItem in enumerate(jsonState['items']): 
 				eventBox = vBox.get_children()[jsonItem['rowPosition']].get_children()[jsonItem['columnPosition']]
				payload, args = self.resumePayload(jsonItem)
				self.currentEventBoxSelected = eventBox
                		self.currentRowPairIndex = self.mapTable[jsonItem['rowPosition']][jsonItem['columnPosition']][0]
                		self.currentColumnPairIndex = self.mapTable[jsonItem['rowPosition']][jsonItem['columnPosition']][1]
				self.modalWindowReturn(payload, jsonItem['type'], args)
		else:
                        self.mapTable = self.givemeMapTable(rows, columns)
		

	
		vBoxExercises.pack_start(vBox, True, False,0)
		vBoxWindows.pack_start(frameExercises, True,False,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
	
	def resumePayload(self, jsonItem):
                
		self.mainWindows.getLogger().debug("Inside to resumeEventBox")
                self.mainWindows.getLogger().debug(jsonItem)
                
                args = {}
                if jsonItem['type'] == 'letter':
                	payloadResume = gtk.Label( jsonItem['value'] )
                        if len(jsonItem['value']) <= MAXIMUM_LETTER_LENGTH_BIG:
				payloadResume.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:
				payloadResume.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))

                elif  jsonItem['type'] == 'image':
                	payloadResume = gtk.Image()
               		payloadResume.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(\
                        	jsonItem['value']).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2) )
                        payloadResume.imageName = jsonItem['fileName']
                        payloadResume.imageType = jsonItem['fileType']
			args = {"imageName": jsonItem['fileName'],"imageType": jsonItem['fileType']}
               
		return (payloadResume, args)
	
	
	def parseToJson(self, isStop, pathToSaveItemsStop):
                self.mainWindows.getLogger().debug("Inside to parseToJson method")
		
		theExerciseJson = {}
                theExerciseJson['codeType'] = 3
		theExerciseJson['mapTable'] = self.mapTable
		theExerciseJson['level'] =  self.level	
                theExerciseJson['items'] = []
                itemsToCopy = []
                elementsToFill = None
		if self.level is 1:
			elementsToFill = 4
		elif self.level is 2:
			elementsToFill = 8
		if len(self.payloads) < elementsToFill and not isStop:
			return (None, None, False, _("All items must be filled"))
		for key, payload in self.payloads.iteritems():
                        theExerciseJson['items'].append(self.parseItemToJson(payload, itemsToCopy, isStop, pathToSaveItemsStop))
                
		response = (theExerciseJson, itemsToCopy, True, None)
		if isStop:	
			response = (theExerciseJson, itemsToCopy)

		return response
	
	
	def parseItemToJson(self, payload, itemsToCopy, isStop, pathToSaveItemsStop):
                self.mainWindows.getLogger().debug(" Inside to parseToJson")
                theJson = {}
        
                if isStop == True:
                        
                      	self.parsePayloadToJson(payload, pathToSaveItemsStop, theJson, itemsToCopy, isStop)
                else:
                        
                        self.parsePayloadToJson(payload, "./images", theJson, itemsToCopy, isStop)
                return theJson

      	def parsePayloadToJson(self, payload ,itemsPath, theJson, itemsToCopy, isStop):
                if payload[0].__class__.__name__ == "Label":
                        theJson['type'] = "letter"
                        theJson["value"] = payload[0].get_text()
                if payload[0].__class__.__name__ == "Image":
                        theJson['type'] = "image"
                        theJson['value'] = itemsPath + "/" + payload[0].imageName
                        if isStop:
                                theJson['fileName'] = payload[0].imageName
                                theJson['fileType'] = payload[0].imageType
			itemsToCopy.append({"type":"image", "value":payload[0], "fileName":payload[0].imageName, \
				"fileType":payload[0].imageType})
		if isStop:
			theJson['rowPosition'] = payload[1]
			theJson['columnPosition'] = payload[2]

			
