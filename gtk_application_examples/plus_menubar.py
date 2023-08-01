#!/usr/bin/python3
# plus_menubar.py
import os
import sys
import pathlib


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vbox = Gtk.VBox()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui_menu.xml")
        self.vbox.add(self.builder.get_object("menubar"))

        hbox = Gtk.HBox()
        hbox.set_size_request(300, 200)

        # add an hbox to contain window(s)
        self.vbox.add(hbox)

        scrollbox = Gtk.ScrolledWindow()
        self.editor = Gtk.TextView()
        scrollbox.add(self.editor)
        hbox.add(scrollbox)

        self.add(self.vbox)  # add the assembled vbox to the window


class MyApplication(Gtk.Application):

    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = MyWindow(application=self, title="Hello World")
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


app = MyApplication()
app.run(sys.argv)
