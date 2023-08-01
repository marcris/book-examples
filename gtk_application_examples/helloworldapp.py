#!/usr/bin/python3
# helloworldapp.py
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
