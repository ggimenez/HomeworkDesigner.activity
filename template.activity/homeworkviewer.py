# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""

import gtk
import logging

from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton


from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton


import pygtk
pygtk.require('2.0')
import json
from collections import namedtuple
from array import *
import pango

from simpleassociation import SimpleAssociation
from findthedifferent import FindTheDifferent
from searchthesame import SearchTheSame
import os


class ModalWindowDone:

	def __init__ (self, parent):
		self.parent = parent
		self.modalWindow = gtk.Window ()

		'''Disable interaction with parent'''
		self.modalWindow.set_modal (True)

		# Tell WM this is a dialog
		self.modalWindow.set_type_hint (gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

		# Tell WM this window belongs to parent
		self.modalWindow.set_transient_for (parent)

		self.modalWindow.set_default_size(350,350)
	
		self.modalWindow.set_skip_pager_hint(True)
		self.modalWindow.set_keep_below(True)
		self.modalWindow.set_decorated(False)
		
		frame = gtk.Frame()
		eventBox = gtk.EventBox()
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("white"))
		
		frame.add(eventBox)
		
		vBox = gtk.VBox (False, 10)
		eventBox.add(vBox)
		
		doneImageContainer =  gtk.Image()
		buttonImageContainer =  gtk.Image()
		buttonImageContainer.set_from_stock(gtk.STOCK_OK, gtk.ICON_SIZE_BUTTON)		
	
		if self.parent.exercisesMatches < self.parent.amountExercises:
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./activity-images/party.png").scale_simple(200, 200, 2))		
		else:
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./activity-images/prize.png").scale_simple(200, 200, 2))
				
		buttonOk = gtk.Button(_("OK"))	
		buttonOk.connect ("clicked", self.goBackButtonCallBack)
		
		vBox.pack_start(doneImageContainer, True,True,10)
		
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False,0)
		
		vBox.pack_start(hBoxButton, True,False,0)
		
		self.modalWindow.add (frame)

		
	def goBackButtonCallBack(self, button,*args):
		self.modalWindow.destroy()
		
	def show (self):
		self.modalWindow.show_all ()
		


class HomeWorkViewer(activity.Activity):
	

	def __init__(self, handle):

		self._logger = logging.getLogger('home-work-viewer')
                self._logger.setLevel(logging.DEBUG)
		

		'''Obtenemos el JSON de la Actividad'''
		json_data=open('json.txt')
		self.activity = json.load(json_data, object_hook=lambda d: namedtuple('Activity', d.keys())(*d.values()))
		json_data.close()

		"""Set up the HelloWorld activity."""
		activity.Activity.__init__(self, handle)

		# we do not have collaboration features
		# make the share option insensitive
		self.max_participants = 1

		# toolbar with the new toolbar redesign
		toolbar_box = ToolbarBox()

		activity_button = ActivityButton(self)
		toolbar_box.toolbar.insert(activity_button, 0)
		activity_button.show()

		title_entry = TitleEntry(self)
		toolbar_box.toolbar.insert(title_entry, 1)
		title_entry.show()

		
		separator = gtk.SeparatorToolItem()
		separator.props.draw = False
		separator.set_expand(True)
		toolbar_box.toolbar.insert(separator, -1)
		separator.show()

		self.buttonBefore = ToolButton('go-previous')
		self.buttonBefore.set_tooltip(_('Back'))
		self.buttonBefore.connect("clicked", self.backButtonCallBack)
		toolbar_box.toolbar.insert(self.buttonBefore, 2)

		self.buttonNext = ToolButton('go-next')
		self.buttonNext.set_tooltip(_('Next'))
		self.buttonNext.connect("clicked", self.nextButtonCallBack)
		toolbar_box.toolbar.insert(self.buttonNext, 3)

		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()

		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()

		self.vBoxMain = gtk.VBox(True, 2)
		self.set_canvas(self.vBoxMain)
		self.show_all()
	
		self._logger.debug(self.metadata.keys())
		self._logger.debug(self.metadata['activity_id'])	
			
		jsonState = None
		activityName = self.metadata.get('title')		
		if (self.metadata.get('custom_activity_id') is not None):		
			with open(self.get_activity_root() + '/data/'  + \
					  str(self.metadata['custom_activity_id']) + '/exerciseState.txt', 'r') as stateFile:
				jsonState = json.load(stateFile)			
			stateFile.close()
		self.createWindowExercises(jsonState)
			
			
	def exerciseCompletedCallBack(self):
		if self.amountExercises > self.exercisesMatches:
			self.exercisesMatches = self.exercisesMatches + 1	
		
		self.modalDoneWindow = ModalWindowDone(self)
		self.modalDoneWindow.show()
		self.freezeExerciseWindow()	
	
	def manageBackNextButtons(self):
		self.getLogger().debug("Inside to manageBackNextButtons")
		self.getLogger().debug(self.currentIndexExercise)
		self.getLogger().debug(self.amountExercises)
		if self.currentIndexExercise == 0:
			self.buttonBefore.set_sensitive(False) 
			if self.amountExercises != 1:
				self.buttonNext.set_sensitive(True)
			else:
				self.buttonNext.set_sensitive(False) 
		elif self.currentIndexExercise > 0 and self.currentIndexExercise < (self.amountExercises-1):
			
			self.buttonBefore.set_sensitive(True) 
			self.buttonNext.set_sensitive(True)
		else:
			
			self.buttonBefore.set_sensitive(True) 
			self.buttonNext.set_sensitive(False) 


	def nextButtonCallBack(self, button, *args):
	
		self.vBoxMain.get_children()[self.currentIndexExercise].hide()
                self.currentIndexExercise = self.currentIndexExercise + 1
		
                self.vBoxMain.get_children()[self.currentIndexExercise].show_all()
                self.manageBackNextButtons()

		
	
	def backButtonCallBack(self, button, *args):
		self.vBoxMain.get_children()[self.currentIndexExercise].hide()
                self.currentIndexExercise = self.currentIndexExercise - 1
                self.vBoxMain.get_children()[self.currentIndexExercise].show_all()
                self.manageBackNextButtons()

	
	def createWindowExercises(self, stateJson):
		
		self._logger.debug("inside to createNewWindowExercise")		
             
		self.amountExercises = len(self.activity.exercises)
		self.currentIndexExercise = 0
		self.exercisesMatches = 0		
	
                index = 0
		while index < self.amountExercises:
                        newExercise = None
                	newWindowExercise = None
			stateExercise = None
			if stateJson is not None:
				stateExercise = stateJson['exercises'][index]
                	if self.activity.exercises[index].codeType  == 1:
                        	newExercise = SimpleAssociation()
                        	newWindowExercise = newExercise.getWindow(self.activity.exercises[index], self, stateExercise)  
                	elif self.activity.exercises[index].codeType  == 2:
                        	newExercise = FindTheDifferent()
                        	newWindowExercise = newExercise.getWindow(self.activity.exercises[index] ,self, stateExercise)
                	elif self.activity.exercises[index].codeType  == 3:
                        	newExercise = SearchTheSame()
                        	newWindowExercise = newExercise.getWindow(self.activity.exercises[index] ,self, stateExercise)

			newWindowExercise.hide()
                	self.vBoxMain.pack_start(newWindowExercise, True, True, 0)
               		index = index + 1
		if stateJson is None:
			self.vBoxMain.get_children()[self.currentIndexExercise].show_all()		
		else:
			self.exercisesMatches = stateJson['exercisesMatches']
			self.moveToExerciseIndex(stateJson['currentIndexExercise'])
		self.manageBackNextButtons()		

	def read_file(self, tmp_file):
		pass
		
	def write_file(self, tmp_file):
		self.getLogger().debug("Inside to write_file")
                self.saveActivityState()
                
		
	def getLogger(self):
                return self._logger
	
	def saveActivityState(self):
                self.getLogger().debug("inside to saveActivityState")
                allExerciseWindows = self.vBoxMain.get_children()
                theJson = {}
                theJson["name"] = "JSON de prueba"
                theJson['currentIndexExercise'] = self.currentIndexExercise
                theJson['exercisesMatches'] = self.exercisesMatches
		theJson["exercises"] = []
                itemsToCopy = []
                activityName = self.metadata.get('title')
                
		metadataKeys = self.metadata.keys()
		self.getLogger().debug(metadataKeys)
		for key in metadataKeys:
			self.getLogger().debug(key)
			self.getLogger().debug(self.metadata.get(key))

		for index, exerciseWindow in enumerate( allExerciseWindows ):
                                exerciseJson = exerciseWindow.exerciseInstance.saveExerciseState()
                                theJson['exercises'].append(exerciseJson)


		'''if not os.path.exists(self.get_activity_root() + '/data/' + activityName):
                        os.makedirs(self.get_activity_root() + '/data/' + activityName)'''

		if self.metadata.get('custom_activity_id') is None:
			self.metadata['custom_activity_id'] = len(os.walk(self.get_activity_root() + '/data').next()[1]) + 1	
			if not os.path.exists(self.get_activity_root() + '/data/' + str(self.metadata['custom_activity_id'])):
                        	os.makedirs( self.get_activity_root() + '/data/' + str(self.metadata['custom_activity_id']))	
	
                self.getLogger().debug(theJson)
                with open( self.get_activity_root() + '/data/' + str(self.metadata['custom_activity_id'])  + '/exerciseState.txt', 'w+') as stateFile:
			json.dump(theJson,stateFile )
		stateFile.close()

	def freezeExerciseWindow(self):
		currentWindowsExercise = self.vBoxMain.get_children()[self.currentIndexExercise] 
		currentWindowsExercise.exerciseInstance.disconnectEventBoxs()	
	
	def moveToExerciseIndex(self, indexExercise):
                self.getLogger().debug("Inside to moveToExerciseIndex")
		vBoxMain = self.vBoxMain
                allWindowsExercises = vBoxMain.get_children()
                for index, windowExercise in enumerate(allWindowsExercises):
                        self.getLogger().debug(index)
			self.getLogger().debug(indexExercise)
			if index != indexExercise:
                                windowExercise.hide()
                        else:
                                windowExercise.show_all()
                self.currentIndexExercise = indexExercise
                self.manageBackNextButtons()

