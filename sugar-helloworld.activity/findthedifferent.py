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

class FindTheDifferent():
	
	def changeBackgroundColour(self, eventBox, colour):
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
	
	def checkCompletedExercise(self):
		
		checkFlag = True
		for selectionState in self.selectionsState:
			if selectionState['selectedIndex'] != selectionState['differentInex']:
				checkFlag = False
				break
	
		if checkFlag:
			self.mainWindows.exerciseCompletedCallBack()
			
		
	def selectionCallBack(self,eventBox, *args):
		
		hVox = args[1]
		vBoxExercises = args[2]
		frame = args[3]
		
		indexHBox = vBoxExercises.child_get_property(frame, "position")
		lastIndexSelected = self.selectionsState[indexHBox]['selectedIndex']
		if lastIndexSelected != -1:
			lastEventBoxSelected = hVox.get_children()[lastIndexSelected]
			self.changeBackgroundColour(lastEventBoxSelected, "white")	
		
		currentIndexEventBox = hVox.child_get_property(eventBox, "position")
		self.changeBackgroundColour(eventBox, "orange")
		self.selectionsState[indexHBox]['selectedIndex'] = currentIndexEventBox
		
		self.checkCompletedExercise();
	
	def createEventBox(self, itemElement):
		eventBox = gtk.EventBox()
		
		if itemElement.type == "letter":
			label = gtk.Label(itemElement.value)
			label.modify_font(pango.FontDescription("Courier Bold 40"))
			eventBox.add(label)
			
		return eventBox
		
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
			
		windowFindTheDifferent = gtk.ScrolledWindow()
		
		frameExercises = gtk.Frame() 
		
		vBoxWindows = gtk.VBox(False, 5)
		vBoxExercises = gtk.VBox(False, 5)
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		self.selectionsState = [None]*len(items)
		for index, item in enumerate(items):
			
			frame = gtk.Frame()
			
			hVox = gtk.HBox(True, 10)
			frame.add(hVox)
			
			count = 0
			until = 3
			different = random.randint(0,until)
			self.selectionsState[index] = {"selectedIndex": -1,"differentInex":different}
			while count <= until:
				
				eventBox = gtk.EventBox()
				if count == different:
					eventBox = self.createEventBox(item.different)
				else:
					eventBox = self.createEventBox(item.equal)
					
				self.changeBackgroundColour(eventBox, 'white')
				eventBox.connect("button-press-event", self.selectionCallBack, hVox, vBoxExercises, frame)
				hVox.pack_start(eventBox, False,True,0)
				count = count + 1
			
			
			frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
			vBoxExercises.pack_start(frame, True,True,10)
		
		
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
		
	
		
