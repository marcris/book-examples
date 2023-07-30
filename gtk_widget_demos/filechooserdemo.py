# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FileChooserWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="FileChooser Example")

        vbox = Gtk.VBox()
        vbox.set_halign(Gtk.Align.CENTER)
        self.hbox = Gtk.HBox()
        self.hbox.set_valign(Gtk.Align.CENTER)
        vbox.add(self.hbox)
        self.add(vbox)

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.set_title("FileChooser Example")
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

        button1 = Gtk.RadioButton.new_with_label(None, label="FileChooserWidget Demo")
        button1.set_mode(draw_indicator=True)
        button1.connect("clicked", self.on_button1_clicked)
        self.buttonbox.add(button1)
        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, label="FileChooserButton Demo")
        button2.set_mode(draw_indicator=True)
        button2.connect("clicked", self.on_button2_clicked)
        self.buttonbox.add(button2)
        button3 = Gtk.RadioButton.new_with_label_from_widget(button1, label="FileChooserDialog Demo")
        button3.set_mode(draw_indicator=True)
        button3.connect("clicked", self.on_button3_clicked)
        self.buttonbox.add(button3)
        self.hbox.add(self.buttonbox)
        self.show_all()

    def on_button1_clicked(self, button):
        if button.get_active():
            self.buttonbox.destroy()

            box = Gtk.Box(spacing=6)

            file_chooser_widget = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.OPEN)
            box.pack_start(file_chooser_widget, False, False, 0)
            self.add_filters(file_chooser_widget)

            file_chooser_widget = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.SELECT_FOLDER)
            box.pack_start(file_chooser_widget, False, False, 0)
            file_chooser_widget.connect("file_activated", self.on_file_activated)

            self.hbox.add(box)
            self.show_all()

    def on_file_activated(self, file_chooser_widget):
        print(file_chooser_widget.get_filename())

    def on_button2_clicked(self, button):
        if button.get_active():
            self.buttonbox.destroy()

            box = Gtk.Box(spacing=6)

            file_chooser_button = Gtk.FileChooserButton(title="Please choose a file", action=Gtk.FileChooserAction.OPEN)
            box.pack_start(file_chooser_button, False, False, 0)
            file_chooser_button.set_width_chars(15)
            file_chooser_button.connect("file-set", self.on_filechooserbutton_clicked)
            self.add_filters(file_chooser_button)

            folder_chooser_button = Gtk.FileChooserButton(title="Please choose a folder", action=Gtk.FileChooserAction.SELECT_FOLDER)
            box.pack_start(folder_chooser_button, False, False, 0)
            folder_chooser_button.set_width_chars(15)
            folder_chooser_button.connect("file-set", self.on_folderchooserbutton_clicked)

            self.hbox.add(box)
            self.show_all()

    def on_filechooserbutton_clicked(self, widget):
        print(f"File selected: {widget.get_filename()}")


    def on_folderchooserbutton_clicked(self, widget):
        print(f"Folder selected: {widget.get_filename()}")


    def on_button3_clicked(self, button):
        self.buttonbox.destroy()

        box = Gtk.Box(spacing=6)
        button1 = Gtk.Button(label="Choose File")
        button1.connect("clicked", self.on_file_clicked)
        box.add(button1)

        button2 = Gtk.Button(label="Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)
        box.add(button2)

        self.hbox.add(box)
        self.show_all()


    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print(f"File selected: {dialog.get_filename()}")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            "Select", Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        )
        dialog.set_default_size(400, 200)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print(f"Folder selected: {dialog.get_filename()}")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

win = FileChooserWindow()
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
