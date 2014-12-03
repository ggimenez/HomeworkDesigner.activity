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
	
		
	def modalWindowReturn(self, item, itemType):
                self.mainWindows.getLogger().debug("Inside a modalWindowReturn")
                self.mainWindows.getLogger().debug(item)
		copyMethod = None	
		
		indexCurrentEventBox = self.currentHBoxItems.child_get_property(self.currentEventBoxSelected, "position")
		
		if indexCurrentEventBox == self.currentDifferentIndex:
			itemCopy = self.copyItem(item, itemType)
			oldItem = self.currentEventBoxSelected.get_children()[0]
                        self.currentEventBoxSelected.remove(oldItem)
                        self.currentEventBoxSelected.add(itemCopy)
                        self.currentEventBoxSelected.show_all()			
		else:
	
			for index,eventBox in enumerate(self.currentHBoxItems.get_children()):
                		if index != self.currentDifferentIndex:
					itemCopy = self.copyItem(item, itemType)
					oldItem = eventBox.get_children()[0]
                			eventBox.remove(oldItem)
					eventBox.add(itemCopy)
                			eventBox.show_all()
	
	def copyItem(self, item, itemType):
		self.mainWindows.getLogger().debug("Inside to copyItem:")
		self.mainWindows.getLogger().debug(itemType)
		itemCopy = None
		if itemType == "text":
			itemCopy = gtk.Label(item.get_text())
			itemCopy.modify_font(pango.FontDescription("Courier Bold 40"))
		elif itemType == "image":		
			itemCopy = gtk.image_new_from_pixbuf(item.get_pixbuf())
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
		
		frameExercises = gtk.Frame() 
		
		vBoxWindows = gtk.VBox(False, 5)
		vBoxExercises = gtk.VBox(False, 5)
		
		frameExercises.add(vBoxExercises)
		
		indexs = [0,1,2,3,4]
		for index in indexs:
			
			frame = gtk.Frame()
			hBox = gtk.HBox(True, 10)
			frame.add(hBox)
			
			count = 0
			until = 3
			different = random.randint(0,until)
			
			while count <= until:
				
				eventBox = gtk.EventBox()
				if count == different:
					eventBox = self.createEventBox()
				else:
					eventBox = self.createEventBox()
					
				eventBox.connect("button-press-event", self.selectionCallBack, different, hBox)
				hBox.pack_start(eventBox, False,True,0)
				count = count + 1
			
			
			frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
			vBoxExercises.pack_start(frame, True,True,10)
		
		
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
		
	
		
