# textview_demo.py

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="TextView Example")

        self.set_default_size(500, 350)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        toolbar = Gtk.Toolbar()
        open_btn = Gtk.ToolButton()
        open_btn.set_icon_name("document-open-symbolic")
        open_btn.connect("clicked", self.on_open_clicked)
        toolbar.insert(open_btn, 0)
        save_btn = Gtk.ToolButton()
        save_btn.set_icon_name("document-save-symbolic")
        save_btn.connect("clicked", self.on_save_clicked)
        toolbar.insert(save_btn, 1)
        self.box.pack_start(toolbar, False, True, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)
        self.box.pack_start(scrolledwindow, True, True, 0)

    def on_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=self,
            action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Open", Gtk.ResponseType.OK,
                           "Cancel", Gtk.ResponseType.CANCEL)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_file = dialog.get_filename()
            with open(selected_file, 'r') as f:
                data = f.read()
                self.textbuffer.set_text(data)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Save file",
            parent=self,
            action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons("Save", Gtk.ResponseType.OK,
                           "Cancel", Gtk.ResponseType.CANCEL)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            save_file = dialog.get_filename()
            start_iter = self.textbuffer.get_start_iter()
            end_iter = self.textbuffer.get_end_iter()
            text = self.textbuffer.get_text(start_iter, end_iter, True)
            with open(save_file, 'w') as f:
                f.write(text)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()