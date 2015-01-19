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


IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]



EVENTBOX_SCALE = [100,100]
FONT_DESCRIPTION_BIG = 'DejaVu Bold 15'
FONT_DESCRIPTION_MEDIUM = 'DejaVu Bold 8'


class FindTheDifferent():
	
	def saveExerciseState(self):
                self.mainWindows.getLogger().debug("Inside to saveExerciseState")
                stateJson = {}
                stateJson['selectionsState'] = self.selectionsState
                stateJson['exerciseCompleted'] = self.exerciseCompleted
		return stateJson


	def changeBackgroundColour(self, eventBox, colour):
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
	
	def checkCompletedExercise(self):
		
		checkFlag = True
		for selectionState in self.selectionsState:
			if selectionState['selectedIndex'] != selectionState['differentInex']:
				checkFlag = False
				break
	
		if checkFlag:
			self.exerciseCompleted = True
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
		eventBox.set_size_request(EVENTBOX_SCALE[0], EVENTBOX_SCALE[1])	
		if itemElement.type == "letter":	
			label = gtk.Label(itemElement.value)
			if len(itemElement.value) <= 8:
				label.modify_font(pango.FontDescription(FONT_DESCRIPTION_BIG))
			else:				
				label.modify_font(pango.FontDescription(FONT_DESCRIPTION_MEDIUM))
			eventBox.add(label)
		elif itemElement.type == "image":
                        image = gtk.Image()
			pixbuf = gtk.gdk.pixbuf_new_from_file(itemElement.value).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2) 
			image.set_from_pixbuf(pixbuf)
                        eventBox.add(image)
                        eventBox.show_all()
	
		return eventBox
	
	def disconnectEventBoxs(self):
		for index, eventBox in enumerate(self.allEventBoxs):
			eventBox.disconnect(self.idHandlers[index])	
	
	def getWindow(self, exercise, mainWindows, stateJson):
		
		self.mainWindows = mainWindows		
		windowFindTheDifferent = gtk.ScrolledWindow()
		windowFindTheDifferent.exerciseInstance = self
		
		frameExercises = gtk.Frame() 
		
		vBoxWindows = gtk.VBox(False, 5)
		vBoxExercises = gtk.VBox(False, 5)
		
		frameExercises.add(vBoxExercises)
		self.exerciseCompleted = False	
		items = exercise.items
		if stateJson is None:
			self.selectionsState = [None]*len(items)
		else:
			self.mainWindows.getLogger().debug("Is a resume of exercises...")
			self.selectionsState = stateJson['selectionsState']
			self.exerciseCompleted = stateJson['exerciseCompleted']
		
		self.allEventBoxs = []
		self.idHandlers = []				
		for index, item in enumerate(items):
			
			frame = gtk.Frame()
			
			hVox = gtk.HBox(True, 10)
			frame.add(hVox)
			
			count = 0
			until = 3
			different = random.randint(0,until)
			if stateJson is None:
				self.selectionsState[index] = {"selectedIndex": -1,"differentInex":different}
			else:
				different = self.selectionsState[index]['differentInex'] 
			while count <= until:
				
				eventBox = gtk.EventBox()
				if count == different:
					eventBox = self.createEventBox(item.different)
				else:
					eventBox = self.createEventBox(item.equal)
				
				self.changeBackgroundColour(eventBox, 'white')
				if not self.exerciseCompleted:
					idHandler = eventBox.connect("button-press-event", self.selectionCallBack, hVox, vBoxExercises, frame)
					self.allEventBoxs.append(eventBox)
					self.idHandlers.append(idHandler)
				
				hVox.pack_start(eventBox, True,True,0)
				count = count + 1
			
			
			frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
			vBoxExercises.pack_start(frame, False,False,10)
	
		if stateJson is not None:
			self.mainWindows.getLogger().debug(self.selectionsState)
			for index, selectionState in enumerate(self.selectionsState):
				if selectionState['selectedIndex'] != -1:
					self.mainWindows.getLogger().debug("Entra para pintar....")
					currentEventBox = vBoxExercises.get_children()[index].get_children()[0].get_children()[selectionState['selectedIndex']]
					self.changeBackgroundColour(currentEventBox, "orange")
		
		vBoxWindows.pack_start(frameExercises, True,True,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
		
	
		
		
