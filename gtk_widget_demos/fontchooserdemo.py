# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk
#
# window = Gtk.Window()
# window.set_title("FontChooserWidget")
# window.connect("destroy", Gtk.main_quit)
#
# def on_font_choice(widget, font):
#     print(f"Font selected: {font}")
#
# fontchooserwidget = Gtk.FontChooserWidget()
# fontchooserwidget.connect("font-activated", on_font_choice)
# window.add(fontchooserwidget)
#
# window.show_all()
#
#
#
#
# fontchooserdialog = Gtk.FontChooserDialog()
# fontchooserdialog.set_title("FontChooserDialog")
#
# response = fontchooserdialog.run()
#
# if response == Gtk.ResponseType.OK:
#     print(f"Font selected: {fontchooserdialog.get_font()}")
#
# fontchooserdialog.destroy()
#
#
#
import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
        <item>
            <attribute name="label">FontChooserWidget Demo</attribute>
            <attribute name="action">app.widget</attribute>
        </item>
        <item>
            <attribute name="label">FontButton Demo</attribute>
            <attribute name="action">app.button</attribute>
        </item>
        <item>
            <attribute name="label">FontChooserDialog Demo</attribute>
            <attribute name="action">app.dialog</attribute>
        </item>
    </section>
  </menu>
</interface>
"""


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(200, 200)

        outerbox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(outerbox)
        outerbox.show()

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        menu = builder.get_object("app-menu")

        self.button = Gtk.MenuButton(menu_model=menu)

        outerbox.pack_start(self.button, False, True, 0)
        self.button.show()
        self.set_border_width(6)

        self.outerbox = outerbox


class FontChooserDemo(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp", **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction(name="widget")
        action.connect("activate", self.on_widget)
        self.add_action(action)

        action = Gio.SimpleAction(name="button")
        action.connect("activate", self.on_button)
        self.add_action(action)

        action = Gio.SimpleAction(name="dialog")
        action.connect("activate", self.on_dialog)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title="FontChooser Demo")

        self.window.show_all()

    def on_font_choice(self, widget, font):
        print(f"Font selected: {font}")

        widget.destroy()

    def on_font_choice2(self, widget):  # for FontButton which doesn't pass the font
        print(f"Font selected: {widget.get_font()}")

        widget.destroy()

    def on_widget(self, action, param):
        fontchooserwidget = Gtk.FontChooserWidget()
        fontchooserwidget.connect("font-activated", self.on_font_choice)
        self.window.outerbox.add(fontchooserwidget)
        self.window.show_all()
        self.window.set_title("FontChooserWidget Demo")
        self.window.button.hide()

    def on_button(self, action, param):
        fontbutton = Gtk.FontButton(title="FontButton")
        fontbutton.set_font("Sans Bold Italic 12")
        fontbutton.connect("font-set", self.on_font_choice2)
        self.window.outerbox.add(fontbutton)
        self.window.show_all()
        self.window.set_title("FontButton Demo")
        self.window.button.hide()

    def on_dialog(self, action, param):
        fontchooserdialog = Gtk.FontChooserDialog()
        fontchooserdialog.set_title("FontChooserDialog")

        response = fontchooserdialog.run()

        if response == Gtk.ResponseType.OK:
            print(f"Font selected: {fontchooserdialog.get_font()}")

        fontchooserdialog.destroy()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = FontChooserDemo()
    app.run(sys.argv)