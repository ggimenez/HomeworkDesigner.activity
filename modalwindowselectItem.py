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

from sugar.graphics.objectchooser import ObjectChooser
from sugar.graphics.entry import CanvasEntry
''' Scales '''
IMAGES_SCALE = [100, 100]
LETTERS_SCALE = [100, 100]


class ModalWindowSelectItem:

	def __init__ (self, parent, exerciseWindow):
		self.parent = parent
		self.exerciseWindow = exerciseWindow
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
		
		self.hBoxItem =  gtk.HBox(True, 10)
		
		entry = gtk.Entry()
                eventBoxImageItem = gtk.EventBox()



		entry.connect("changed", self.textEnterCallBack, eventBoxImageItem)
		self.hBoxItem.pack_start(entry, False,False,0)
		
		imagePlaceHolder = gtk.Image()
		imagePlaceHolder.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/img_place_holder.gif").scale_simple(300, 200, 2))
		
		
		vBoxImageItem = gtk.VBox(True, 0)
		
		frameEventBoxImageItem = gtk.Frame()
		frameEventBoxImageItem.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
		
		eventBoxImageItem.connect("button-press-event", self.imageItemSelected, entry)
		eventBoxImageItem.add(imagePlaceHolder)
		
		frameEventBoxImageItem.add(eventBoxImageItem)
		
		vBoxImageItem.pack_start(frameEventBoxImageItem, False,False,0)
		self.hBoxItem.pack_start(vBoxImageItem, False,False	,0)
		
		imageButtonIcon = gtk.Image()
		imageButtonIcon.set_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)	
		buttonCancel = gtk.Button()
		buttonCancel.set_image(imageButtonIcon)
		buttonCancel.set_label("Cancelar")
		buttonCancel.connect ("clicked", self.cancelButtonCallBack)
		buttonCancel.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		
		buttonOkIcon = gtk.Image()
		buttonOkIcon.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)	
		buttonOk = gtk.Button()
		buttonOk.set_image(buttonOkIcon)
		buttonOk.set_label("Aceptar")
		buttonOk.connect ("clicked", self.okButtonCallBack)
		buttonOk.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		
		
		
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False	,0)
		hBoxButton.pack_start(buttonCancel, False,False	,0)
		
		self.scrolledWindow.add_with_viewport(self.hBoxItem)
		self.frameWindowScrolled.add(self.scrolledWindow)
		self.vBoxModalWindow.pack_start(self.frameWindowScrolled, True,True,0)
		
		self.frameHBoxButton.add(hBoxButton)
		self.vBoxModalWindow.pack_start(self.frameHBoxButton, False,False,0)
		
		self.modalWindow.add(self.vBoxModalWindow)
	
	def textEnterCallBack(self, entry, *args):
		
		imageEventBox = args[0]
		oldImage = imageEventBox.get_children()[0]
		imageEventBox.remove(oldImage)
		imagePlaceHolder = gtk.Image()
                imagePlaceHolder.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/img_place_holder.gif").scale_simple(300, 200, 2))
		imageEventBox.add(imagePlaceHolder)		
		imageEventBox.show_all()
		
		self.parent.getLogger().debug("Inside in textEnterCallBack : ")
		self.parent.getLogger().debug(args)
		self.parent.getLogger().debug(entry.get_text())
		self.itemHandler = self.manageTextSelected		
		self.itemSelected = entry.get_text()		
	


	def manageTextSelected(self):
		labelText = gtk.Label(self.itemSelected)
		#labelText.modify_font(pango.FontDescription("Courier Bold 60"))
		self.exerciseWindow.modalWindowReturn(labelText, "text", {})
		
	def manageImageSelected(self):
		self.parent.getLogger().debug("Inside to manageImageSelected")
		self.exerciseWindow.modalWindowReturn(self.itemSelected, "image", {"imageName":self.itemSelected.imageName, "imageType":self.itemSelected.imageType})		
	
	def imageItemSelected(self, eventBox, *args):
                self.parent.getLogger().debug("Inside a imageItemSelected, args: ")
		self.parent.getLogger().debug(args)
		
		entryText = args[1]
		entryText.set_text("")
		
		chooser = ObjectChooser(parent=self.modalWindow, what_filter='Image')
		result = chooser.run()
		self.parent.getLogger().debug("chooser result :")
		self.parent.getLogger().debug(result)
		self.jobject = None		
		self.path = None
		if result == gtk.RESPONSE_ACCEPT:
			self.jobject = chooser.get_selected_object()
			self.path = str(self.jobject.get_file_path())
			self.parent.getLogger().debug(self.jobject)	
			self.parent.getLogger().debug(self.path)
			self.parent.getLogger().debug(self.jobject.get_metadata().keys())
			self.parent.getLogger().debug(self.jobject.get_metadata().get('title'))			
			self.parent.getLogger().debug(self.jobject.get_metadata().get('mtime'))				
			self.parent.getLogger().debug(self.jobject.get_metadata().get('mime_type'))			
		if self.path != None:
			imageSelected = gtk.Image()
			imageSelected.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self.path).scale_simple(300, 300, 2))
			
			imageSelectedCopy = gtk.Image()
			imageSelectedCopy.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(self.path).scale_simple(IMAGES_SCALE[0], IMAGES_SCALE[1], 2))
			imageSelectedCopy.imageName = self.jobject.get_metadata().get('title')			
			
			imageMimeType = self.jobject.get_metadata().get('mime_type').split("/")
	
			imageSelectedCopy.imageType = imageMimeType[1]	
			
	
   			self.itemSelected = imageSelectedCopy
						
			oldImage = eventBox.get_children()[0]
			eventBox.remove(oldImage)
			eventBox.add(imageSelected)
			eventBox.show_all()
			self.itemHandler = self.manageImageSelected 
		
	def enterNotifyEventBoxCallBack(self, eventBox, *args):
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("orange"))
	def leaveNotifyEventBoxCallBack(self, eventBox, *args):
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("gray")) 
	
        def okButtonCallBack(self, eventBox, *args):
		self.itemHandler()	
		self.modalWindow.destroy()
	
        def cancelButtonCallBack(self, button,*args):
		self.modalWindow.destroy()
		
	def exerciseTypeSelectedCallBack(self, eventBox, *args):
		#self.parent._logger.debug(args)
		codeExerciseType = args[1]['code']
		self.modalWindow.destroy()
		self.parent.createNewExerciseType(codeExerciseType)
		
	def show(self):
		self.modalWindow.show_all ()
