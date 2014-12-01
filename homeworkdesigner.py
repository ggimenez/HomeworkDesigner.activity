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



import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

from simpleassociationtemplate import SimpleAssociationTemplate
from findthedifferent import FindTheDifferent
from searchthesame import SearchTheSame


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

		self.modalWindow.set_default_size(600,600)
		self.modalWindow.set_decorated(False)
	
		
		self.vBoxModalWindow = gtk.VBox(False, 0)
		
		self.vBoxExercises =  gtk.VBox(True, 5)
		
		exercisesTypes = ( [{"code":1, "imagePath":"./images/code1.png", "label":"Asociacion Simple"},
                                    {"code":2, "imagePath":"./images/code2.png", "label":"Encuentra el Diferente"},
                                    {"code":3, "imagePath":"./images/code3.png", "label":"Busca los iguales"} ]
                                 )
		
		for exerciseType in exercisesTypes:
			hBox = gtk.HBox(True, 0)
			eventBox = gtk.EventBox()
			eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("gray"))
		
			eventBox.connect("enter-notify-event", self.enterNotifyEventBoxCallBack)
			eventBox.connect("leave_notify_event", self.leaveNotifyEventBoxCallBack)
			eventBox.connect("button-press-event", self.exerciseTypeSelectedCallBack, exerciseType)
			image = gtk.Image()
			image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(exerciseType['imagePath']).scale_simple(200, 200, 2))
			label = gtk.Label(exerciseType['label'])
			hBox.pack_start(image, False,False,0)
			hBox.pack_start(label, False,False,0)
			eventBox.add(hBox)
			self.vBoxExercises.pack_start(eventBox, False,False,0)
		
		imageButtonIcon = gtk.Image()
		imageButtonIcon.set_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)	
		buttonOk = gtk.Button()
		buttonOk.set_image(imageButtonIcon)
		buttonOk.set_label("Cancelar")
		buttonOk.connect ("clicked", self.cancelButtonCallBack)
		buttonOk.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False	,0)
		
		self.scrolledWindow.add_with_viewport(self.vBoxExercises)
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
		#self.newButton.connect("clicked", self.newExerciseCallBack)
		toolbar_box.toolbar.insert(self.deleteButton, 6)
		
		self.exportButton = ToolButton('document-save')
		self.exportButton.set_tooltip(_('Exportar Ejercicio'))
		#self.newButton.connect("clicked", self.newExerciseCallBack)
		toolbar_box.toolbar.insert(self.exportButton, 7)
	
		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()

		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()

		vBoxGeneral = gtk.VBox(False, 2)
		self.set_canvas(vBoxGeneral)
		self.show_all()
		
	
	def exerciseCompletedCallBack(self):
			self.modalDoneWindow = ModalWindowDone(self)
			self.modalDoneWindow.show()	
	
	def manageBackNextButtons(self):
		if self.currentIndexExercise == 0:
			self.buttonBefore.set_sensitive(False) 
			self.buttonNext.set_sensitive(True) 
		elif self.currentIndexExercise > 0 and self.currentIndexExercise < (self.amountExercises-1):
			
			self.buttonBefore.set_sensitive(True) 
			self.buttonNext.set_sensitive(True)
		else:
			
			self.buttonBefore.set_sensitive(True) 
			self.buttonNext.set_sensitive(False) 

	
	def newExerciseCallBack(self, button, *args):
		dialogExercise = ModalWindowSelectExercise(self)
		dialogExercise.show()
		
	def nextButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise + 1
		self.createNewWindowExercise()
		
	def getLogger(self):
		return self._logger
	
	def backButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise - 1
		self.createNewWindowExercise()
	
	def createNewExerciseType(self, codeExerciseType):
		newExerciseTemplate = None
		newWindowExerciseTemplate = None
		if codeExerciseType == 1:
			self._logger.debug("Inside : if codeExerciseType == 1")
			newExerciseTemplate = SimpleAssociationTemplate()
			newWindowExerciseTemplate = newExerciseTemplate.getWindow(self)
			self._logger.debug("After : ewWindowExerciseTemplate = newExerciseTemplate.getWindow(self)")
			
		vBoxMain = self.get_children()[0]
		if len(vBoxMain.get_children()) > 1 :
			oldWindowExerciseTemplate = vBoxMain.get_children()[1]
			vBoxMain.remove(oldWindowExerciseTemplate)
		
		self._logger.debug("After : if len(vBoxMain.get_children()) > 1")
			
		vBoxMain.pack_start(newWindowExerciseTemplate, True, True, 0)
		self.show_all()	
		self._logger.debug("After : self.show_all()")
			
	def createNewWindowExercise(self):
		
		'''newExercise = None
		newWindowExercise = None
		if self.activity.exercises[self.currentIndexExercise].codeType == 1:
			newExercise = SimpleAssociation()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 2:
			newExercise = FindTheDifferent()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 3:
			newExercise = SearchTheSame()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
			
		vBoxMain = self.get_children()[0]
		if len(vBoxMain.get_children()) > 1 :
			oldWindowExercise = vBoxMain.get_children()[1]
			vBoxMain.remove(oldWindowExercise)
			
		vBoxMain.pack_start(newWindowExercise, True, True, 0)
		
		self.manageBackNextButtons()
		self.show_all()'''
	
	def read_file(self, tmp_file):
		pass

	def write_file(self, tmp_file):
		pass

