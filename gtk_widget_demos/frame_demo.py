import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Frame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Box demo")
        self.set_default_size(200, 200)
        self.set_border_width(5)
        self.connect("destroy", Gtk.main_quit)

        hframe = Gtk.Frame()
        self.add(hframe)

        hbox = Gtk.Box()
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(5)
        hbox.set_spacing(5)

        button = Gtk.Button(label="Button 1")
        hbox.pack_start(button, True, True, 0)
        button = Gtk.Button(label="Button 2")
        hbox.pack_start(button, True, True, 0)

        hframe.add(hbox)

        vframe = Gtk.Frame()
        hbox.add(vframe)

        vbox = Gtk.Box()
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        vbox.set_border_width(5)
        vbox.set_spacing(5)

        button = Gtk.Button(label="Button 3")
        vbox.pack_start(button, True, True, 0)
        button = Gtk.Button(label="Button 4")
        vbox.pack_start(button, True, True, 0)

        vframe.add(vbox)


window = Frame()
window.show_all()

Gtk.main()


