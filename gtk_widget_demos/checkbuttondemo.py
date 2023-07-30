# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class CheckButtonDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("CheckButton Demo")
        self.set_size_request(250, 100)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        hbox = Gtk.HBox()
        hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(hbox)
        self.add(vbox)

        button = Gtk.CheckButton(label="CheckButton")
        button.set_mode(draw_indicator=True)
        button.connect("clicked", self.on_button_clicked)
        hbox.add(button)


    def on_button_clicked(self, button):
        print("CheckButton was clicked!")


window = CheckButtonDemo()
window.show_all()

Gtk.main()


