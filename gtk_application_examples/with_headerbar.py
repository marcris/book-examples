#!/usr/bin/python3
# with_headerbar.py

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="example_with_headerbar")
        self.set_border_width(10)
        self.set_default_size(400, 400)

        # Create HeaderBar.
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Geeks for Geeks"
        self.set_titlebar(hb)

        # Create Button
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        # Create Box
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        self.add(Gtk.TextView())


win = HeaderBarWindow()
win.connect("destroy", Gtk.main_quit)
# Display the window.
win.show_all()
# Start the GTK + processing loop
Gtk.main()