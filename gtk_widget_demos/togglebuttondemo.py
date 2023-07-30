# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ToggleButtonDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("ToggleButton Demo")
        self.set_size_request(250, 100)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        hbox = Gtk.HBox()
        hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(hbox)
        self.add(vbox)

        button = Gtk.ToggleButton(label="ToggleButton")
        button.connect("clicked", self.on_button_clicked)
        hbox.add(button)

    def on_button_clicked(self, button):
        print("ToggleButton was clicked!")


window = ToggleButtonDemo()
window.show_all()

Gtk.main()


