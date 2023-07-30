# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class ColorChooserWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ColorChooser Example")

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        self.hbox = Gtk.HBox()
        self.hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(self.hbox)
        self.add(vbox)

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.set_title("ColorChooser Example")
        self.back_button = Gtk.Button.new_from_icon_name("pan-start-symbolic", Gtk.IconSize.BUTTON)
        self.back_button.connect('clicked', self.show_choices)

        headerbar.pack_start(self.back_button)
        self.set_titlebar(headerbar)

        self.show_choices()

    def show_choices(self, *args):
        def remove_children(widget, container):
            container.remove(widget)

        self.hbox.foreach(remove_children, self.hbox)

        self.buttonbox = Gtk.VBox()

        button1 = Gtk.RadioButton.new_with_label(None, label="ColorChooserWidget Demo")
        button1.set_mode(draw_indicator=True)
        button1.connect("clicked", self.on_button1_clicked)
        self.buttonbox.add(button1)
        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, label="ColorChooserButton Demo")
        button2.set_mode(draw_indicator=True)
        button2.connect("clicked", self.on_button2_clicked)
        self.buttonbox.add(button2)
        button3 = Gtk.RadioButton.new_with_label_from_widget(button1, label="ColorChooserDialog Demo")
        button3.set_mode(draw_indicator=True)
        button3.connect("clicked", self.on_button3_clicked)
        self.buttonbox.add(button3)
        self.hbox.add(self.buttonbox)
        self.show_all()

    def on_button1_clicked(self, button):
        if button.get_active():
            self.buttonbox.destroy()

            box = Gtk.Box(spacing=6)

            color_chooser_widget = Gtk.ColorChooserWidget()
            color = Gdk.RGBA()
            color.parse("MediumSlateBlue")
            color_chooser_widget.set_rgba(color)
            box.pack_start(color_chooser_widget, False, False, 0)
            color_chooser_widget.connect("color_activated", self.on_color_activated)

            self.hbox.add(box)
            self.show_all()

    def on_color_activated(self, color_chooser_widget, color):
        print(f"color selected: {color.to_string()}")

    def on_button2_clicked(self, button):
        if button.get_active():
            self.buttonbox.destroy()

            box = Gtk.Box(spacing=6)

            color = Gdk.RGBA()
            color.parse("MediumSlateBlue")
            color_chooser_button = Gtk.ColorButton.new_with_rgba(color)
            color_chooser_button.set_title("Please choose a color")
            box.pack_start(color_chooser_button, False, False, 0)
            color_chooser_button.connect("color-set", self.on_colorchooserbutton_clicked)

            self.hbox.add(box)
            self.show_all()

    def on_colorchooserbutton_clicked(self, widget):
        print(f"color selected: {widget.get_rgba()}")


    def on_button3_clicked(self, button):
        self.buttonbox.destroy()

        box = Gtk.Box(spacing=6)
        button1 = Gtk.Button(label="Choose color")
        button1.connect("clicked", self.on_color_clicked)
        box.add(button1)

        button2 = Gtk.Button(label="Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)
        box.add(button2)

        self.hbox.add(box)
        self.show_all()


    def on_color_clicked(self, widget):
        dialog = Gtk.ColorChooserDialog(
            title="Please choose a color", parent=self
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(f"color selected: {dialog.get_rgba()}")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


    def on_folder_clicked(self, widget):
        dialog = Gtk.ColorChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.ColorChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            "Select", Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        )
        dialog.set_default_size(400, 200)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print(f"Folder selected: {dialog.get_colorname()}")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

win = ColorChooserWindow()
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
