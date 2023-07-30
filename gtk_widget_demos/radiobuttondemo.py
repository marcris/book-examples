# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class RadioButtonDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("RadioButton Demo")
        self.set_size_request(250, 100)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        hbox = Gtk.HBox()
        hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(hbox)
        self.add(vbox)

        buttonbox = Gtk.VBox()
        button1 = Gtk.RadioButton.new_with_label(None, label="RadioButton1")
        button1.set_mode(draw_indicator=True)
        button1.connect("clicked", self.on_button_clicked)
        buttonbox.add(button1)
        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, label="RadioButton2")
        button2.set_mode(draw_indicator=True)
        button2.connect("clicked", self.on_button_clicked)
        buttonbox.add(button2)
        button3 = Gtk.RadioButton.new_with_label_from_widget(button1, label="RadioButton3")
        button3.set_mode(draw_indicator=True)
        button3.connect("clicked", self.on_button_clicked)
        buttonbox.add(button3)
        hbox.add(buttonbox)


    def on_button_clicked(self, button):
        print(f"{button.get_label()} was clicked!")


window = RadioButtonDemo()
window.show_all()

Gtk.main()


