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
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.combobox import ComboBox

from sugar.graphics.alert import Alert

import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

from simpleassociationtemplate import SimpleAssociationTemplate
from findthedifferenttemplate import FindTheDifferentTemplate
from searchthesametemplate import SearchTheSameTemplate

import os
import zipfile
from sugar.datastore import datastore
import glob

from sugar.graphics.alert import ConfirmationAlert
from sugar.graphics.alert import NotifyAlert


FONT_DESCRIPTION = 'DejaVu Bold 40'
FONT_DESCRIPTION_MODAL = "DejaVu Bold 10"


class ModalWindowSelectExercise:

	def __init__ (self, parent):
		self.parent = parent
		self.modalWindow = gtk.Window()
		
		self.frameWindowScrolled = gtk.Frame()
		self.frameWindowScrolled.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		
		self.frameHBoxButton = gtk.Frame()
		self.frameHBoxButton.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
			
		self.scrolledWindow = gtk.ScrolledWindow()
		
		'''Disable interaction with parent'''
		self.modalWindow.set_modal (True)

		# Tell WM this is a dialog
		self.modalWindow.set_type_hint (gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

		# Tell WM this window belongs to parent
		self.modalWindow.set_transient_for (parent)

		self.modalWindow.set_default_size(1000,500)
		self.modalWindow.set_decorated(False)
	
		
		self.vBoxModalWindow = gtk.VBox(False, 0)
		
		self.hBoxExercises =  gtk.HBox(True, 1)
		
		exercisesTypes = ( [{"code":1, "imagePath":"./images/code1.png", "label":"Asociacion Simple"},
                                    {"code":2, "imagePath":"./images/code2.png", "label":"Encuentra el Diferente"},
                                    {"code":3, "imagePath":"./images/code3.png", "label":"Busca los iguales"} ]
                                 )
		
		for exerciseType in exercisesTypes:
			vBox = gtk.VBox(True, 0)
			eventBox = gtk.EventBox()
			eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("gray"))
		
			eventBox.connect("enter-notify-event", self.enterNotifyEventBoxCallBack)
			eventBox.connect("leave_notify_event", self.leaveNotifyEventBoxCallBack)
			eventBox.connect("button-press-event", self.exerciseTypeSelectedCallBack, exerciseType)
			image = gtk.Image()
			image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(exerciseType['imagePath']).scale_simple(300, 200, 2))
			label = gtk.Label(exerciseType['label'])
			label.modify_font(pango.FontDescription(FONT_DESCRIPTION_MODAL))
			frameImage = gtk.Frame()			
			frameImage.add(image)
			vBox.pack_start(label, False,False,0)
			vBox.pack_start(frameImage, False,False,0)
			eventBox.add(vBox)
			self.hBoxExercises.pack_start(eventBox, False,False,0)
		
		imageButtonIcon = gtk.Image()
		imageButtonIcon.set_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)	
		buttonOk = gtk.Button()
		buttonOk.set_image(imageButtonIcon)
		buttonOk.set_label(_("Cancel"))
		buttonOk.connect ("clicked", self.cancelButtonCallBack)
		buttonOk.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False,0)
		
		self.scrolledWindow.add_with_viewport(self.hBoxExercises)
		self.frameWindowScrolled.add(self.scrolledWindow)
		self.vBoxModalWindow.pack_start(self.frameWindowScrolled, True,True,0)
		
		self.frameHBoxButton.add(hBoxButton)
		self.vBoxModalWindow.pack_start(self.frameHBoxButton, False,False,0)
		
		self.modalWindow.add(self.vBoxModalWindow)
	
	def enterNotifyEventBoxCallBack(self, eventBox, *args):
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
	def leaveNotifyEventBoxCallBack(self, eventBox, *args):
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("gray")) 
		
	def cancelButtonCallBack(self, button,*args):
		self.modalWindow.destroy()
		
	def exerciseTypeSelectedCallBack(self, eventBox, *args):
		#self.parent._logger.debug(args)
		codeExerciseType = args[1]['code']
		self.modalWindow.destroy()
		self.parent.createNewExerciseType(codeExerciseType, None, None)
		
		
	def show(self):
		self.modalWindow.show_all ()
		

class HomeWorkDesigner(activity.Activity):
	"""HelloWorldActivity class as specified in activity.info"""
	def __init__(self, handle):
		
		self._logger = logging.getLogger('home-work-designer-activity')
		self._logger.setLevel(logging.DEBUG)
		
		self._logger.debug("Inside to HomeWorkViewer, __init__ method")	
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

		self.title_entry = TitleEntry(self)
		toolbar_box.toolbar.insert(self.title_entry, 1)
		self.title_entry.show()

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
	
		labelItem = gtk.ToolItem() 
		self.labelExercisePosition = gtk.Label("")
		labelItem.add(self.labelExercisePosition)
		toolbar_box.toolbar.insert(labelItem, 4)
		
		separatorBeforeLevels = gtk.SeparatorToolItem()
		separatorBeforeLevels.props.draw = False
		separatorBeforeLevels.set_expand(True)
		toolbar_box.toolbar.insert(separatorBeforeLevels, 5)	

		self.comboBoxLevels = ComboBox()
		#self.comboBoxLevels.append_item(0, "--")
		self.comboBoxLevels.append_item(1, 'One')
		self.comboBoxLevels.append_item(2, 'Two')	
		self.comboBoxLevels.connect('changed', self.comboBoxChanged)
			
		toolComboBoxLevels = ToolComboBox(self.comboBoxLevels)
		toolComboBoxLevels.label.set_text("Level: ")	
		toolbar_box.toolbar.insert(toolComboBoxLevels, 6)		
	
		separator2 = gtk.SeparatorToolItem()
                separator2.props.draw = False
                separator2.set_expand(True)
                toolbar_box.toolbar.insert(separator2, 7)
                separator2.show()
	
		self.newButton = ToolButton('add')
		self.newButton.set_tooltip(_('New Exercise'))
		self.newButton.connect("clicked", self.newExerciseCallBack)
		toolbar_box.toolbar.insert(self.newButton, 8)
	
		self.deleteButton = ToolButton('edit-delete')
		self.deleteButton.set_tooltip(_('Delete Exercise'))
		self.deleteButton.connect("clicked", self.buttonDeleteExerciseCallBack)
		toolbar_box.toolbar.insert(self.deleteButton, 9)
		
		self.exportButton = ToolButton('document-save')
		self.exportButton.set_tooltip(_('Export Exercise'))
		self.exportButton.connect("clicked", self.exportExerciseCallBack)
		toolbar_box.toolbar.insert(self.exportButton, 10)
	
		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()

		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()

		self.vBoxMain = gtk.VBox(False, 2)
		self.set_canvas(self.vBoxMain)
		
		self.amountExercises = 0		
		self.currentExerciseIndex = -1		
		self.manageNevegationButtons()
		self.manageComboBoxDisplay()
		
		self.show_all()
	
	
	def comboBoxChanged(self, combo, *args):
		self.getLogger().debug("Inside to comboBoxChanged method:")
		self.getLogger().debug(args)
		self.getLogger().debug(self.comboBoxLevels.get_value())
		self.getLogger().debug(self.comboBoxLevels.get_active_item())
		newLevel = self.comboBoxLevels.get_value()
		if self.currentExerciseIndex is not -1:
			currentWindow = self.vBoxMain.get_children()[self.currentExerciseIndex]
			self.getLogger().debug( currentWindow.exerciseInstance.level )
			if currentWindow.exerciseInstance.level is not newLevel:
				newWindow = currentWindow.exerciseInstance.changeLevel(newLevel)
				self.deleteExerciseCallBack()
				self.createNewExerciseType(None, None, newWindow)
				

	def manageComboBoxDisplay(self):
		self.getLogger().debug("Inside to manageComboBoxDisplay")
		if self.amountExercises > 0:
			self.comboBoxLevels.set_sensitive(True)
			currentWindow = self.vBoxMain.get_children()[self.currentExerciseIndex]
			self.getLogger().debug(currentWindow.exerciseInstance.level)
			self.comboBoxLevels.set_active(currentWindow.exerciseInstance.level - 1)
		else:
			self.comboBoxLevels.set_sensitive(False)
			self.comboBoxLevels.set_active(-1)	

	def manageNevegationButtons(self):
		self.getLogger().debug("inside to manageNevegationButtons ")
		self.getLogger().debug("self.amountExercises : %s "  % self.amountExercises)
		self.getLogger().debug("self.currentExerciseIndex %s : " % self.currentExerciseIndex)

		if self.amountExercises == 0 :
			self.buttonBefore.set_sensitive(False)				
			self.buttonNext.set_sensitive(False)
			self.deleteButton.set_sensitive(False)
			self.exportButton.set_sensitive(False)
		else:
			self.deleteButton.set_sensitive(True)
			self.exportButton.set_sensitive(True)	
			if self.currentExerciseIndex == 0:
				self.buttonBefore.set_sensitive(False)
			else:
				self.buttonBefore.set_sensitive(True)

			if self.currentExerciseIndex == (self.amountExercises-1):
                        	self.buttonNext.set_sensitive(False)
                        else:
                                self.buttonNext.set_sensitive(True)
		if self.amountExercises > 0 :
			self.labelExercisePosition.set_text( str(self.currentExerciseIndex + 1) + " of " + str(self.amountExercises) )
		else:					
			self.labelExercisePosition.set_text("")
	def newExerciseCallBack(self, button, *args):
		self.getLogger().debug("inside to newExerciseCallBack")
		dialogExercise = ModalWindowSelectExercise(self)
		dialogExercise.show()
		self.getLogger().debug("exit from newExerciseCallBack")
		
	def nextButtonCallBack(self, button, *args):
		self.vBoxMain.get_children()[self.currentExerciseIndex].hide()
                self.currentExerciseIndex = self.currentExerciseIndex + 1
                self.vBoxMain.get_children()[self.currentExerciseIndex].show()
                self.manageNevegationButtons()
		self.manageComboBoxDisplay()

		
	def getLogger(self):
		return self._logger
	
	def backButtonCallBack(self, button, *args):
		self.vBoxMain.get_children()[self.currentExerciseIndex].hide()
		self.currentExerciseIndex = self.currentExerciseIndex - 1
		self.vBoxMain.get_children()[self.currentExerciseIndex].show()
		self.manageNevegationButtons()
	
	def moveToExerciseIndex(self, indexExercise):
		vBoxMain = self.vBoxMain
                allWindowsExercises = vBoxMain.get_children()
                for index, windowExercise in enumerate(allWindowsExercises):
                        if index != indexExercise:
				windowExercise.hide()
			else:
				windowExercise.show_all()
		self.currentExerciseIndex = indexExercise
		self.manageNevegationButtons()
		self.manageComboBoxDisplay()	
	
	def buttonDeleteExerciseCallBack(self, button, *args):
		self._alert_confirmation(self.deleteExerciseCallBack, _("Remove exercise"), _("Are you sure ?"))		
	
	def deleteExerciseCallBack(self):
		self.getLogger().debug("inside to buttonDeleteExercise")
		self.getLogger().debug(self.amountExercises)
		self.getLogger().debug(self.currentExerciseIndex)
		self.getLogger().debug(self.vBoxMain.get_children())	
				

		windowToDelete = self.vBoxMain.get_children()[self.currentExerciseIndex]
                self.vBoxMain.remove(windowToDelete)
		if self.currentExerciseIndex == (self.amountExercises - 1):
			self.currentExerciseIndex = self.currentExerciseIndex - 1				
		self.amountExercises = self.amountExercises - 1
		

		if self.amountExercises > 0:
			self.vBoxMain.get_children()[self.currentExerciseIndex].show_all()

		self.manageNevegationButtons()
		self.manageComboBoxDisplay()
		self.getLogger().debug("exit from buttonDeleteExercise")		

	def zipdir(self,path, zip):
    		for root, dirs, files in os.walk(path):
        		for file in files:
            			zip.write(os.path.join(root, file))	

	def exportExerciseCallBack(self, *args):
		self.getLogger().debug("Inside to exportExerciseCallBack")
		allExerciseWindows = self.vBoxMain.get_children()
		theJson = {}
		theJson["name"] = "JSON de prueba"
		theJson["exercises"] = []
		itemsToCopy = []
		for index, exerciseWindow in enumerate( allExerciseWindows ):
				exerciseJson, itemsToCopyAux, validExercise , errorMessage = exerciseWindow.exerciseInstance.parseToJson(False, None)
				if validExercise == False:
					self._alert_notify(_("Export as activity"), _("Error in the exercise Number ") + str(index + 1) + " : " + errorMessage)
					return 
				itemsToCopy = itemsToCopy + itemsToCopyAux
				theJson['exercises'].append(exerciseJson)

		with open('./template.activity/json.txt', 'w') as outfile:
				outfile.truncate()
				json.dump(theJson, outfile)
				outfile.close()

		imagesToDelete = glob.glob('./template.activity/images/*')
		for imageToDelete in imagesToDelete:
				os.remove(imageToDelete)

		for itemToAdd in itemsToCopy:
				if itemToAdd['type'] == "image":
						pixbuf = itemToAdd['value'].get_pixbuf()
						pixbuf.save('./template.activity/images/' + itemToAdd['fileName'], itemToAdd['fileType'])
		activityName = self.title_entry.entry.get_text()

		#write activity info
		activityInfoData = []
		#tag
		activityInfoData.append("[Activity]")
		#name
		activityInfoData.append("name = " + activityName)
		#version
		activityInfoData.append("activity_version = 1")
		#bundel_id
		activityNameSpacesLess = activityName.replace(" ", "")
		self.getLogger().debug(activityNameSpacesLess)
		activityInfoData.append("bundle_id = org.sugarlabs." + activityNameSpacesLess)
		#exec
		activityInfoData.append("exec = sugar-activity homeworkviewer.HomeWorkViewer")
		#icon
		activityInfoData.append("icon = homework-viewer")
		#lincense
		activityInfoData.append("license = GPLv2+")
		with open('./template.activity/activity/activity.info', 'w') as infofile:
				infofile.truncate()
				for infoEntry in activityInfoData:
						infofile.write(infoEntry + "\n")
				infofile.close()
	
		zipf = zipfile.ZipFile(self.get_activity_root() + '/instance/' + activityNameSpacesLess + '.activity.xo', 'w')                                             
		os.rename("./template.activity/", activityNameSpacesLess + '.activity')
		self.zipdir(activityNameSpacesLess + '.activity', zipf)
		zipf.close()
		os.rename( activityNameSpacesLess + '.activity',"./template.activity/")

		file_dsobject = datastore.create()
		file_dsobject.metadata['title'] = activityNameSpacesLess + '.activity.xo'
		file_dsobject.metadata['mime_type'] = "application/vnd.olpc-sugar"
		file_path = os.path.join(self.get_activity_root(), 'instance', activityNameSpacesLess + '.activity.xo')
		file_dsobject.set_file_path(file_path)
		datastore.write(file_dsobject)
		
		self._alert_notify(_("Export as activity"), _("It has been exported successfully"))
		
		#delete the .xo created when is saved in the datastore
		os.remove(self.get_activity_root() + '/instance/' + activityNameSpacesLess + '.activity.xo')			

		self.getLogger().debug(theJson)
		self.getLogger().debug(itemsToCopy)

	def createNewExerciseType(self, codeExerciseType, jsonResume, newWindow):
		self.getLogger().debug("inside to createNewExerciseType")
			
		newExerciseTemplate = None
		newWindowExerciseTemplate = None
		if newWindow is None:
			if codeExerciseType == 1:
				self._logger.debug("Inside : if codeExerciseType == 1")
				newExerciseTemplate = SimpleAssociationTemplate()
				newWindowExerciseTemplate = newExerciseTemplate.getWindow(self, jsonResume, 1)
				self._logger.debug("After : ewWindowExerciseTemplate = newExerciseTemplate.getWindow(self)")
			elif codeExerciseType == 2:
				newExerciseTemplate = FindTheDifferentTemplate()
				newWindowExerciseTemplate = newExerciseTemplate.getWindow(self, jsonResume, 1)		
			elif codeExerciseType == 3:
				newExerciseTemplate = SearchTheSameTemplate()
				newWindowExerciseTemplate = newExerciseTemplate.getWindow(self, jsonResume, 1)
		else:
			newWindowExerciseTemplate = newWindow
	
		vBoxMain = self.vBoxMain
		allWindowsExercises = vBoxMain.get_children()
                for windowExercise in allWindowsExercises:
                        windowExercise.hide() 
		
	
		vBoxMain.pack_start(newWindowExerciseTemplate, True, True, 0)
		self.amountExercises = self.amountExercises + 1
		self.currentExerciseIndex = self.currentExerciseIndex + 1
		
		self.getLogger().debug(self.amountExercises)
                self.getLogger().debug(self.currentExerciseIndex)
		self.getLogger().debug("update after createNewExerciseType")		

		self.manageNevegationButtons()
		self.manageComboBoxDisplay()
		newWindowExerciseTemplate.show_all()
		self.getLogger().debug("exit from buttonDeleteExercise")
		
		
	def _alert_confirmation(self, callback, title, message):
        	alert = ConfirmationAlert()
        	alert.props.title= title
        	alert.props.msg = message
        	alert.connect('response', self._alert_response_cb, callback)
        	self.add_alert(alert)

	def _alert_response_cb(self, alert, *args):
        	self.getLogger().debug(args)
		#remove the alert from the screen, since either a response button
        	#was clicked or there was a timeout
        	self.remove_alert(alert)
		response_id = args[0]
		callback = args[1]		
		
        	#Do any work that is specific to the type of button clicked.
        	if response_id is gtk.RESPONSE_OK:
        		callback()	

	def _alert_notify(self, title, message):
        	#Notice that for a NotifyAlert, you pass the number of seconds in
        	#which to notify. By default, this is 5.
        	alert = NotifyAlert(10)
        	alert.props.title= title
        	alert.props.msg = message
        	alert.connect('response', self._alert_response_cb, self.alert_notify_callback)
        	self.add_alert(alert)
	
 	def alert_notify_callback(self):
		pass
			
	def read_file(self, tmp_file_path):
		self.getLogger().debug("Inside to read_file")
		self.getLogger().debug(tmp_file_path)
		tmpFile = open(tmp_file_path, 'r')
        	theJsonState = json.load(tmpFile)
               	self.getLogger().debug(theJsonState) 
		
		self.resumeActivity(theJsonState)
		tmpFile.close()


	def write_file(self, tmp_file_path):
		self.getLogger().debug("Inside to write_file")
		self.getLogger().debug(tmp_file_path)	
		tmpFile = open(tmp_file_path, 'w')
		self.saveActivityState(tmpFile)
		tmpFile.close()
	
	def saveActivityState(self, tmpFile):
		self.getLogger().debug("inside to saveActivityState")
		allExerciseWindows = self.vBoxMain.get_children()
                theJson = {}
                theJson["name"] = "JSON de prueba"
                theJson['currentExerciseIndex'] = self.currentExerciseIndex
		theJson["exercises"] = []
                itemsToCopy = []
		activityName = self.metadata.get('title')
                for index, exerciseWindow in enumerate( allExerciseWindows ):
                                exerciseJson, itemsToCopyAux = exerciseWindow.exerciseInstance.parseToJson(True, \
								self.get_activity_root() + '/data/' + activityName)                
                                
				itemsToCopy = itemsToCopy + itemsToCopyAux
                                theJson['exercises'].append(exerciseJson)

		if not os.path.exists(self.get_activity_root() + '/data/' + activityName):
    			os.makedirs(self.get_activity_root() + '/data/' + activityName)
		
		for itemToAdd in itemsToCopy:
                	if itemToAdd['type'] == "image":
                        	pixbuf = itemToAdd['value'].get_pixbuf()
                                pixbuf.save(self.get_activity_root() + '/data/' + activityName + '/' + itemToAdd['fileName'], itemToAdd['fileType'])
		self.getLogger().debug(theJson)
		json.dump(theJson, tmpFile)

	def resumeActivity(self, jsonState):
		for exerciseJson in jsonState['exercises']:
			self.createNewExerciseType(exerciseJson['codeType'], exerciseJson, None)
		self.moveToExerciseIndex(jsonState['currentExerciseIndex'])				
		
