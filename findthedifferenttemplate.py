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

class FindTheDifferentTemplate():
	
	def changeBackgroundColour(self, eventBox, colour):
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
	
		
	def modalWindowReturn(self, item, itemType, args):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
                self.mainWindows.getLogger().debug(item)
		copyMethod = None	
		
		indexCurrentEventBox = self.currentHBoxItems.child_get_property(self.currentEventBoxSelected, "position")
		
		if indexCurrentEventBox == self.currentDifferentIndex and self.isFirstClick() == False:
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
		response = True
		for theEventBox in self.currentHBoxItems.get_children():
			if theEventBox.filled == True:
				response = False
				break
		return response			
	
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
		
	def selectionCallBack(self,eventBox, *args):
		
		self.mainWindows.getLogger().debug(args)
		
		dialogInsertNewItem = ModalWindowSelectItem(self.mainWindows, self)
                dialogInsertNewItem.show()
		self.currentEventBoxSelected = eventBox
		self.currentDifferentIndex = args[1]
		self.currentHBoxItems = args[2]

	
	def createEventBox(self):
		eventBox = gtk.EventBox()
		
		label = gtk.Label("")
		label.modify_font(pango.FontDescription("Courier Bold 40"))
		eventBox.add(label)
		self.changeBackgroundColour(eventBox, 'white')		

		return eventBox
		
	def getWindow(self, mainWindows):
		
		self.mainWindows = mainWindows
			
		windowFindTheDifferent = gtk.ScrolledWindow()
		windowFindTheDifferent.exerciseName = "FindTheDifferentTemplate"
		windowFindTheDifferent.exerciseInstance = self		
			
		frameExercises = gtk.Frame() 
		
		vBoxWindows = gtk.VBox(False, 5)
		self.vBoxExercises = gtk.VBox(False, 5)
		
		frameExercises.add(self.vBoxExercises)
		
		indexs = [0,1,2,3,4]
		for index in indexs:
			
			frame = gtk.Frame()
			hBox = gtk.HBox(True, 10)
			frame.add(hBox)
			
			count = 0
			until = 3
			different = random.randint(0,until)
			
			while count <= until:	
			
				eventBox = self.createEventBox()	
				eventBox.connect("button-press-event", self.selectionCallBack, different, hBox)
				if count == different:
					eventBox.different = True
				else:
					eventBox.different = False				
				eventBox.filled = False
				hBox.pack_start(eventBox, False,True,0)
				count = count + 1
			
			
			frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
			self.vBoxExercises.pack_start(frame, True,True,10)
		
		
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
	
	def validateFilled(self, hBox):
		eventBoxEqual = None
		eventBoxDifferent = None
		foundEqualFilled = False
		foundDifferentFilled = False
		response = False
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
		return (response, eventBoxEqual, eventBoxDifferent)			

	def parseToJson(self):
        	theExerciseJson = {}
                theExerciseJson['codeType'] = 2
                theExerciseJson['items'] = []
                itemsToCopy = []
                for hFrame in self.vBoxExercises.get_children():
			self.mainWindows.getLogger().debug("Hframe child: ")
			self.mainWindows.getLogger().debug(hFrame.get_children()[0])
			response, eventBoxEqual, eventBoxDifferent = self.validateFilled(hFrame.get_children()[0])			
			if response is True:				                         
                                payloadEqual = eventBoxEqual.get_children()[0]
                                payloadDifferent = eventBoxDifferent.get_children()[0]
                                item = {}
                                item['equal'] = self.parsePayloadToJson(payloadEqual, itemsToCopy)
                                item['different'] = self.parsePayloadToJson(payloadDifferent, itemsToCopy)
                                theExerciseJson['items'].append(item)
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
