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
import gtk
import json
from collections import namedtuple
from array import *
import pango

from simpleassociation import SimpleAssociation
from findthedifferent import FindTheDifferent
from searchthesame import SearchTheSame


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
		
		if self.parent.currentIndexExercise < (self.parent.amountExercises - 1):
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/party.png").scale_simple(200, 200, 2))	
			buttonImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/left.png").scale_simple(50, 50, 2))
		else:
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/prize.png").scale_simple(200, 200, 2))
			buttonImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/left.png").scale_simple(50, 50, 2))
		
		
		
		buttonOk = gtk.Button()
		buttonOk.set_image(buttonImageContainer)
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
	"""HelloWorldActivity class as specified in activity.info"""

	def __init__(self, handle):

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

		'''share_button = ShareButton(self)
		toolbar_box.toolbar.insert(share_button, -1)
		share_button.show()'''

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

		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()

		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()

		self.amountExercises = len(self.activity.exercises)
		self.currentIndexExercise = -1
		
		self.nextButtonCallBack(None, None)


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


	def nextButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise + 1
		self.createNewWindowExercise()
		
	
	def backButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise - 1
		self.createNewWindowExercise()
	
	def createNewWindowExercise(self):
		newExercise = None
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
		self.show_all()
	
	def read_file(self, tmp_file):
		""" datastore high-level interaction to read """
		logging.debug("The tmp_file is at %s, for reading", tmp_file)

		# resume metadata
		try:
			self.entry.set_text(self.metadata['entry'])
		except KeyError:
			logging.error("No entry metadata")

		# resume data
		data = open(tmp_file, "r")
		buffer = self.text.get_buffer()
		buffer.set_text(data.read())
		data.close()

	def write_file(self, tmp_file):
		""" datastore high-level interaction to write """
		logging.debug("The tmp_file is at %s, for writing", tmp_file)

		# save metadata
		self.metadata['entry'] = self.entry.get_text()

		# save data
		data = open(tmp_file, "w")
		buffer = self.text.get_buffer()
		data.write(buffer.get_text(*buffer.get_bounds()))
		data.close()

