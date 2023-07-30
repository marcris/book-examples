# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class ButtonDemo(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("Button Demo")
        self.set_size_request(250, 100)
        self.connect("destroy", gtk.main_quit)

        vbox = gtk.VBox()
        vbox.set_halign(gtk.Align.CENTER)
        hbox = gtk.HBox()
        hbox.set_valign(gtk.Align.CENTER)
        vbox.add(hbox)

        button = gtk.Button(label="Button")
        button.connect("clicked", self.on_button_clicked)
        hbox.add(button)

        self.add(vbox)

    def on_button_clicked(self, button):
        print("Button was clicked!")


window = ButtonDemo()
window.show_all()

gtk.main()


