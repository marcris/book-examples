import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class ImageDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Image Demo")
        self.set_size_request(250, 100)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        hbox = Gtk.HBox()
        hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(hbox)

        image = Gtk.Image.new_from_file ("images/gtk-logo-rgb.gif");
        #pixbuf = GdkPixbuf.new_from_file("images/gtk-logo-rgb.gif")
        # transparent = image.add_alpha(True, 0xff, 0xff, 0xff)
        # image = Gtk.Image.new_from_pixbuf(transparent)

        hbox.add(image)

        self.add(vbox)



window = ImageDemo()
window.show_all()

Gtk.main()

