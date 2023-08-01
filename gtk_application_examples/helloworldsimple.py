#!/usr/bin/python3
# helloworldsimple.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys
import my_useful_module
print(f'imported from {my_useful_module.__file__}')
print(sys.path)

window = Gtk.Window(title="Hello World")
window.show()

Gtk.main()
