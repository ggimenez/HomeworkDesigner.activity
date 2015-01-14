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
import copy

from modalwindowselectItem import ModalWindowSelectItem

''' Scales '''
IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]

EVENTBOX_SCALE = [100,100]

FONT_DESCRIPTION_BIG = 'DejaVu Bold 40'
FONT_DESCRIPTION_MEDIUM = 'DejaVu Bold 20'

MAXIMUM_LETTER_LENGTH_BIG = 8

class FindTheDifferentTemplate():
	
	def changeBackgroundColour(self, eventBox, colour):
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
	
		
	def modalWindowReturn(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
                self.mainWindows.getLogger().debug(item)
		
		copyMethod = None	
		
		indexCurrentEventBox = self.currentHBoxItems.child_get_property(self.currentEventBoxSelected, "position")
		
		if indexCurrentEventBox == self.currentDifferentIndex and not self.isFirstClick() :
			itemCopy = self.copyItem(item, itemType, args)
			oldItem = self.currentEventBoxSelected.get_children()[0]
                        self.currentEventBoxSelected.remove(oldItem)
                        self.currentEventBoxSelected.add(itemCopy)
                        self.currentEventBoxSelected.show_all()
			self.currentEventBoxSelected.filled = True			
		else:
	
			for index,eventBox in enumerate(self.currentHBoxItems.get_children()):
                		if index != self.currentDifferentIndex:
					itemCopy = self.copyItem(item, itemType, args)
					oldItem = eventBox.get_children()[0]
                			eventBox.remove(oldItem)
					eventBox.add(itemCopy)
					eventBox.filled = True
                			eventBox.show_all()
	def isFirstClick(self):
		self.mainWindows.getLogger().debug("Inside to isFirstClick")
		response = True
		for theEventBox in self.currentHBoxItems.get_children():
			#self.mainWindows.getLogger().debug(theEventBox.filled)
			if theEventBox.filled == True:
				response = False
				break
		return response			
	
	def copyItem(self, item, itemType, args):
		self.mainWindows.getLogger().debug("Inside to copyItem:")
		#self.mainWindows.getLogger().debug(itemType)
		itemCopy = None
		if itemType == "text":
			itemCopy = gtk.Label(item.get_text())
			if len(item.get_text()) <= MAXIMUM_LETTER_LENGTH_BIG:
				itemCopy.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:				
				itemCopy.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))
		elif itemType == "image":		
			itemCopy = gtk.image_new_from_pixbuf(item.get_pixbuf())
			itemCopy.imageName = args['imageName']
			itemCopy.imageType = args['imageType']
		return itemCopy	
		
	def selectionCallBack(self,eventBox, *args):
		
		self.mainWindows.getLogger().debug("Inside to selectionCallBack")
		

		dialogInsertNewItem = ModalWindowSelectItem(self.mainWindows, self)
                dialogInsertNewItem.show()
		self.currentEventBoxSelected = eventBox
		self.currentDifferentIndex = args[1]
		self.currentHBoxItems = args[2]

	

	def createEventBox(self, payload):
                eventBox = gtk.EventBox()
                eventBox.set_size_request(EVENTBOX_SCALE[0], EVENTBOX_SCALE[1])
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))

                if payload is None:
                        blankLabel = gtk.Label("")
                        blankLabel.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
                        eventBox.add(blankLabel)
                        #eventBox.set_size_request(LETTERS_SCALE[0], LETTERS_SCALE[1])
                        eventBox.filled = False
                else:
                        eventBox.add(payload)
			#eventBox.set_size_request(LETTERS_SCALE[0], LETTERS_SCALE[1])
                        eventBox.filled = True

                return eventBox


	
	def createPayloadFromResume(self, jsonItem):
                self.mainWindows.getLogger().debug("Inside to createPayloadFromResume")
                '''self.mainWindows.getLogger().debug(jsonItem)'''
                payloadResume = None
                if jsonItem["filled"] is True:
                        if jsonItem['type'] == 'letter':
                                payloadResume = gtk.Label( jsonItem['value'] )
                                if len(jsonItem['value']) <= MAXIMUM_LETTER_LENGTH_BIG:
					payloadResume.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
				else:	
					payloadResume.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))

                        elif  jsonItem['type'] == 'image':
                                payloadResume = gtk.Image()
                                payloadResume.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(\
                                        jsonItem['value'] ).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2))
                                payloadResume.imageName = jsonItem['fileName']
                                payloadResume.imageType = jsonItem['fileType']
                return payloadResume
	
	def changeLevel(self, newLevel):
                newWindow = self.getWindow(self.mainWindows, None, newLevel)
                return newWindow
	
	def getWindow(self, mainWindows, jsonState, level):
		
		self.mainWindows = mainWindows
			
		windowFindTheDifferent = gtk.ScrolledWindow()
		windowFindTheDifferent.exerciseName = "FindTheDifferentTemplate"
		windowFindTheDifferent.exerciseInstance = self		
			
		frameExercises = gtk.Frame() 
		
		vBoxWindows = gtk.VBox(False, 5)
		self.vBoxExercises = gtk.VBox(False, 5)
		
		frameExercises.add(self.vBoxExercises)
		self.level = level
		if jsonState is not None:
			self.level = jsonState['level']
		index = None
		if self.level is 1:	
			indexs = [0,1]
		elif self.level is 2:
			indexs = [0,1,2,3,4]

		
		for index in indexs:
			
			frame = gtk.Frame()
			hBox = gtk.HBox(True, 10)
			frame.add(hBox)
			
			count = 0
			until = 3
			different = random.randint(0,until)
			
			while count <= until:	
				payload = None
				if jsonState is not None:
					if count == different:
						payload = self.createPayloadFromResume(jsonState['items'][index]['different'])
					else:			
						payload = self.createPayloadFromResume(jsonState['items'][index]['equal'])
	
				eventBox = self.createEventBox(payload)
				
				eventBox.connect("button-press-event", self.selectionCallBack, different, hBox)
				if count == different:
					eventBox.different = True
				else:
					eventBox.different = False				
			
				hBox.pack_start(eventBox, True,True,0)
				count = count + 1
			
			
			frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
			self.vBoxExercises.pack_start(frame, True,True,10)
		
		
		vBoxWindows.pack_start(frameExercises, False,False,10)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
	
	def validateFilled(self, hBox, isStop):
		eventBoxEqual = None
		eventBoxDifferent = None
		foundEqualFilled = False
		foundDifferentFilled = False
		response = False
		
		if isStop == False:
			for eventBox in hBox.get_children():				
				if eventBox.different == True:
					if eventBox.filled == True:
						eventBoxDifferent = eventBox
						foundDifferentFilled = True
					else:
						break
				else:
					if eventBox.filled == True:
						foundEqualFilled = True
				  		eventBoxEqual = eventBox
			if foundEqualFilled is True and foundDifferentFilled is True:
				response = True
		else:
			for eventBox in hBox.get_children():				
				if eventBox.different == True:
					eventBoxDifferent = eventBox
				else:
				  	eventBoxEqual = eventBox
				

		return (response, eventBoxEqual, eventBoxDifferent)			

	def parseToJson(self, isStop, pathToSaveItemsStop):
        	theExerciseJson = {}
                theExerciseJson['codeType'] = 2
                theExerciseJson['level'] = self.level
		theExerciseJson['items'] = []
                itemsToCopy = []
                for hFrame in self.vBoxExercises.get_children():
			self.mainWindows.getLogger().debug("Hframe child: ")
			self.mainWindows.getLogger().debug(hFrame.get_children()[0])
			response, eventBoxEqual, eventBoxDifferent = self.validateFilled(hFrame.get_children()[0], isStop)			
			if response is True or isStop:				                         
                                payloadEqual = eventBoxEqual.get_children()[0]
                                payloadDifferent = eventBoxDifferent.get_children()[0]
                                item = {}
                                item['equal'] = self.parseItemToJson(payloadEqual, itemsToCopy, isStop, eventBoxEqual.filled, pathToSaveItemsStop)
                                item['different'] = self.parseItemToJson(payloadDifferent, itemsToCopy, isStop, eventBoxDifferent.filled, pathToSaveItemsStop)
                                theExerciseJson['items'].append(item)
                response = (theExerciseJson, itemsToCopy, True, None)
		if isStop == True:
			response = (theExerciseJson, itemsToCopy)

		return response

	def parseItemToJson(self, payload, itemsToCopy, isStop, eventBoxFilled, pathToSaveItemsStop):
                self.mainWindows.getLogger().debug("inside to parseItemToJson")	

                theJson = {} 
                if isStop == True:
                        
                        theJson['filled'] = eventBoxFilled
                        if eventBoxFilled == True:
                                
                                self.parsePayloadToJson(payload, pathToSaveItemsStop, theJson, itemsToCopy, isStop)
                else: 
                        self.parsePayloadToJson(payload, "./images", theJson, itemsToCopy, isStop)
                return theJson

        def parsePayloadToJson(self, payload ,itemsPath, theJson, itemsToCopy, isStop):
                self.mainWindows.getLogger().debug("inside to parsePayloadToJson")
	
		if payload.__class__.__name__ == "Label":
                        theJson['type'] = "letter"
                        theJson["value"] = payload.get_text()
                if payload.__class__.__name__ == "Image":
                        theJson['type'] = "image"
                        theJson['value'] = itemsPath + "/" + payload.imageName
                        if isStop:
                                theJson['fileName'] = payload.imageName
                                theJson['fileType'] = payload.imageType
                        itemsToCopy.append({"type":"image", "value":payload, "fileName":payload.imageName, "fileType":payload.imageType})
	
