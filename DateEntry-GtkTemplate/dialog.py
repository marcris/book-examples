# Dialog.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

# from DateEntry_gtkTemplate import MyDateEntry
from DateEntry_plain import MyDateEntry

class DialogExample(gtk.Dialog):

    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent)
        self.add_buttons(
            gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, gtk.STOCK_OK, gtk.ResponseType.OK)
        self.set_default_size(200, 200)
        self.set_border_width(15)

        box = self.get_content_area()
        vbox = gtk.VBox()
        box.add(vbox)

        # add a plain Entry to demonstrate moving the focus to
        # the composite when this Entry is activated
        self.prev_entry = gtk.Entry()
        self.prev_entry.set_vexpand(True)
        self.prev_entry.set_valign(gtk.Align.CENTER)
        vbox.add(self.prev_entry)
        self.prev_entry.grab_focus()
        self.prev_entry.connect('activate', self.prev_entry_activated)

        hbox = gtk.HBox()
        hbox.set_valign(gtk.Align.CENTER)
        hbox.set_spacing(5)
        hbox.add(gtk.Label(label="Date:"))

        # add an instance of the composite 'MyDateEntry' with 'initial_date' set to '25/08/22'
        self.date_entry = MyDateEntry(self, "25/08/22")
        hbox.add(self.date_entry)
        vbox.add(hbox)

        # add a plain Entry to demonstrate moving the focus there
        # when the composite is activated
        self.next_entry = gtk.Entry()
        self.next_entry.set_vexpand(True)
        self.next_entry.set_valign(gtk.Align.CENTER)
        vbox.add(self.next_entry)

        self.show_all()

    def prev_entry_activated(self, widget):
        # user pressed Enter in prev_entry
        self.date_entry.grab_focus()
        self.date_entry.connect("activate", self.date_entry_activated)

    def date_entry_activated(self, widget, text):
        # user pressed Enter in the composite's Entry child
        print(f'date_entry_activated\t{text}')
        self.next_entry.grab_focus()
        self.next_entry.connect('activate', self.next_entry_activated)

    def next_entry_activated(self, widget):
        # user pressed Enter in next_entry
        self.response(gtk.ResponseType.OK)

class DialogWindow(gtk.Window):
    # a class for a main window to contain just a button to run
    # the dialog example
    def __init__(self):
        gtk.Window.__init__(self, title="Dialog Example")
        self.set_default_size(200, 200)
        self.set_border_width(6)

        button = gtk.Button(label="Open dialog")
        button.connect("clicked", self.on_button_clicked)

        self.add(button)

    def on_button_clicked(self, widget):
        # Create an instance of the DialogExample, run it
        # and print out what the response was.
        dialog = DialogExample(self)
        response = dialog.run()

        if response == gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()


win = DialogWindow()
win.connect("destroy", gtk.main_quit)
win.show_all()
gtk.main()