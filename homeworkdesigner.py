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
			label.modify_font(pango.FontDescription("Courier Bold 12"))
			
			vBox.pack_start(label, False,False,0)
			vBox.pack_start(image, False,False,0)
			eventBox.add(vBox)
			self.hBoxExercises.pack_start(eventBox, False,False,0)
		
		imageButtonIcon = gtk.Image()
		imageButtonIcon.set_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)	
		buttonOk = gtk.Button()
		buttonOk.set_image(imageButtonIcon)
		buttonOk.set_label("Cancelar")
		buttonOk.connect ("clicked", self.cancelButtonCallBack)
		buttonOk.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False	,0)
		
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
		self.parent.createNewExerciseType(codeExerciseType)
		
		
	def show(self):
		self.modalWindow.show_all ()
		

class HomeWorkDesigner(activity.Activity):
	"""HelloWorldActivity class as specified in activity.info"""
	def __init__(self, handle):
		
		self._logger = logging.getLogger('home-work-designer-activity')
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
		self.buttonBefore.set_tooltip(_('Anterior'))
		self.buttonBefore.connect("clicked", self.backButtonCallBack)
		toolbar_box.toolbar.insert(self.buttonBefore, 2)

		self.buttonNext = ToolButton('go-next')
		self.buttonNext.set_tooltip(_('Siguiente'))
		self.buttonNext.connect("clicked", self.nextButtonCallBack)
		toolbar_box.toolbar.insert(self.buttonNext, 3)

		toolbar_box.toolbar.insert_space(4)

		
		self.newButton = ToolButton('add')
		self.newButton.set_tooltip(_('Nuevo Ejercicio'))
		self.newButton.connect("clicked", self.newExerciseCallBack)
		toolbar_box.toolbar.insert(self.newButton, 5)
	
		self.deleteButton = ToolButton('edit-delete')
		self.deleteButton.set_tooltip(_('Borrar Ejercicio'))
		self.deleteButton.connect("clicked", self.buttonDeleteExerciseCallBack)
		toolbar_box.toolbar.insert(self.deleteButton, 6)
		
		self.exportButton = ToolButton('document-save')
		self.exportButton.set_tooltip(_('Exportar Ejercicio'))
		self.exportButton.connect("clicked", self.exportExerciseCallBack)
		toolbar_box.toolbar.insert(self.exportButton, 7)
	
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
		
		self.show_all()

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

		
	def getLogger(self):
		return self._logger
	
	def backButtonCallBack(self, button, *args):
		self.vBoxMain.get_children()[self.currentExerciseIndex].hide()
		self.currentExerciseIndex = self.currentExerciseIndex - 1
		self.vBoxMain.get_children()[self.currentExerciseIndex].show()
		self.manageNevegationButtons()
	
	def buttonDeleteExerciseCallBack(self, button, *args):
		self.getLogger().debug("inside to buttonDeleteExercise")
		self.getLogger().debug(self.amountExercises)
		self.getLogger().debug(self.currentExerciseIndex)
		self.getLogger().debug(self.vBoxMain.get_children())	

		windowToDelete = self.vBoxMain.get_children()[self.currentExerciseIndex]
                self.vBoxMain.remove(windowToDelete)
		if self.currentExerciseIndex == (self.amountExercises - 1):
			self.currentExerciseIndex = self.currentExerciseIndex - 1				
		self.amountExercises = self.amountExercises - 1
		

		if self.amountExercises != 1:
			
			if self.currentExerciseIndex == (self.amountExercises - 1):
				self.getLogger().debug("Inside to: if self.currentExerciseIndex == (self.amountExercises - 1):")
				self.vBoxMain.get_children()[self.currentExerciseIndex - 1].show_all()
			else:
				self.getLogger().debug("inside to: Else")
				self.vBoxMain.get_children()[self.currentExerciseIndex + 1].show_all()
		
		self.manageNevegationButtons()
		self.getLogger().debug("exit from buttonDeleteExercise")		

	def exportExerciseCallBack(self, *args):
		self.getLogger().debug("Inside to exportExerciseCallBack")
		allExerciseWindows = self.vBoxMain.get_children()
		theJson = {}
		theJson["name"] = "JSON de prueba"
		theJson["exercises"] = []
		itemsToCopy = []
		for exerciseWindow in allExerciseWindows:
			if exerciseWindow.exerciseName == "SimpleAssociationTemplate":
				exerciseJson, itemsToCopyAux = exerciseWindow.exerciseInstance.parseToJson() 
				itemsToCopy = itemsToCopy + itemsToCopyAux
				theJson['exercises'].append(exerciseJson)	
				
				

		self.getLogger().debug(theJson)
		self.getLogger().debug(itemsToCopy)

	def createNewExerciseType(self, codeExerciseType):
		self.getLogger().debug("inside to createNewExerciseType")
		newExerciseTemplate = None
		newWindowExerciseTemplate = None
		if codeExerciseType == 1:
			self._logger.debug("Inside : if codeExerciseType == 1")
			newExerciseTemplate = SimpleAssociationTemplate()
			newWindowExerciseTemplate = newExerciseTemplate.getWindow(self)
			self._logger.debug("After : ewWindowExerciseTemplate = newExerciseTemplate.getWindow(self)")
		elif codeExerciseType == 2:
			newExerciseTemplate = FindTheDifferentTemplate()
			newWindowExerciseTemplate = newExerciseTemplate.getWindow(self)		
		elif codeExerciseType == 3:
			newExerciseTemplate = SearchTheSameTemplate()
			newWindowExerciseTemplate = newExerciseTemplate.getWindow(self)
		
	
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
		newWindowExerciseTemplate.show_all()
		self.getLogger().debug("exit from buttonDeleteExercise")
 	
			
	def read_file(self, tmp_file):
		pass

	def write_file(self, tmp_file):
		pass
