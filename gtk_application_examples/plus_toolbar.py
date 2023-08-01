#!/usr/bin/python3
# plus_toolbar.py
import sys


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf

import about

# The following declaration allows the application to be invoked from anywhere
# and access its database and .glade files etc. relative to its source directory.
from os.path import dirname

def where_am_i():  # use to find ancillary files e.g. .glade files
    return dirname(__file__)


# Information for the "Help/About" dialog
MY_LOGO = where_am_i() + '/logo.svg'

NAME = 'Example'
VERSION = 'Not stated'
COPYRIGHT = 'Copyright © 2021 Chris Brown and Marcris Software'
DESCRIPTION = 'An example program skeleton'
AUTHORS = [
    'Chris Brown <chris@marcrisoft.co.uk>'
]

DEFAULT_LOGO_SIZE_WIDTH = 150
DEFAULT_LOGO_SIZE_HEIGHT = 150

LICENSE_FILE = 'https://opensource.org/licenses/MIT'


# noinspection PyTypeChecker
class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, application, title):
        Gtk.Window.__init__(self, application=application, title=title)
        self.app = app
        self.connect('destroy', self.on_destroy)
        self.connect('delete-event', self.on_delete_event)

        self.vbox = Gtk.VBox()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui_menu.xml")
        self.vbox.add(self.builder.get_object("menubar"))

        self.builder.add_from_file("ui_toolbar.xml")
        self.vbox.add(self.builder.get_object("toolbar"))

        hbox = Gtk.HBox()
        hbox.set_size_request(300, 200)

        # add an hbox to contain window(s)
        self.vbox.add(hbox)

        scrollbox = Gtk.ScrolledWindow()
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrollbox.add(self.textview)
        hbox.add(scrollbox)

        # noinspection PyArgumentList
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.add(self.vbox)  # add the assembled vbox to the window

        # The "win.new/open/save/save as" actions
        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.on_new_clicked)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.on_open_clicked)
        self.add_action(open_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.on_save_clicked)
        self.add_action(save_action)

        saveas_action = Gio.SimpleAction.new("saveas", None)
        saveas_action.connect("activate", self.on_saveas_clicked)
        self.add_action(saveas_action)


        # The "win.undo/redo" actions
        undo_action = Gio.SimpleAction.new("undo_sourceview_only", None)
        undo_action.connect("activate", self.on_undo_clicked)
        self.add_action(undo_action)

        redo_action = Gio.SimpleAction.new("redo_sourceview_only", None)
        redo_action.connect("activate", self.on_redo_clicked)
        self.add_action(redo_action)

        # The "win.copy/paste/cut" actions
        cut_action = Gio.SimpleAction.new("cut", None)
        cut_action.connect("activate", self.on_cut_clicked)
        self.add_action(cut_action)

        copy_action = Gio.SimpleAction.new("copy", None)
        copy_action.connect("activate", self.on_copy_clicked)
        self.add_action(copy_action)

        paste_action = Gio.SimpleAction.new("paste", None)
        paste_action.connect("activate", self.on_paste_clicked)
        self.add_action(paste_action)

    # Callbacks for "win" actions

    def on_new_clicked(self, action, parameter):
        print("new clicked")

    def on_open_clicked(self, action, parameter):
        print("open clicked")

    def on_save_clicked(self, action, parameter):
        print("save clicked")

    def on_saveas_clicked(self, action, parameter):
        print("save as clicked")


    def on_undo_clicked(self, action, parameter):
        print("undo clicked")
        if self.textbuffer.can_undo():
            self.textbuffer.undo()
            self.is_dirty = True

    def on_redo_clicked(self, action, parameter):
        print("redo clicked")
        if self.textbuffer.can_redo():
            self.textbuffer.redo()
            self.is_dirty = True

    def on_copy_clicked(self, action, parameter):
        print("copy clicked")
        self.textbuffer.copy_clipboard(self.clipboard)  # Copies the currently-selected text to the clipboard.

    def on_paste_clicked(self, action, parameter):
        print("paste clicked")
        editable = self.textview.get_editable()
        self.textbuffer.paste_clipboard(self.clipboard, None, editable)  # Pastes the contents of the clipboard.
        self.is_dirty = True

    def on_cut_clicked(self, action, parameter):
        print("cut clicked")
        editable = self.textview.get_editable()
        self.textbuffer.cut_clipboard(self.clipboard, editable)
        # Copies the currently-selected text to a clipboard, then deletes the text if it’s editable.
        self.is_dirty = True

    # Code around various methods of closing down
    # Note that quit action is "app.quit" declared in MyApplication;
    # all others are "win.something" declared here.
    def on_destroy(self, widget):
        print("Caught destroy event")
        print("i.e. Main window destroyed; quit application")
        self.app.quit()

    def on_delete_event(self, widget, *data):
        print("Caught main window delete event")
        print("i.e. Main window close button clicked; ask user what to do")

        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Do you really want to close?")
        dialog.format_secondary_text(
            "(Your current changes will be saved automatically)")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
            print("i.e. user really does want to close")
            print("     so save changes as promised and return False")
        else:
            if response == Gtk.ResponseType.NO:
                print("QUESTION dialog closed by clicking NO")
            elif response == Gtk.ResponseType.DELETE_EVENT:
                print("QUESTION dialog closed by clicking X")
            print("i.e. user didn't really want to close; return True")
            return True  # means we have dealt with signal; no action required

        return False  # means go ahead with the Gtk.main_quit action


class MyApplication(Gtk.Application):

    def __init__(self):
        super().__init__()

        # The "about" action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        # The "quit" action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    def about_cb(self, action, parameter):
        # Show a "Help/About" dialog
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(NAME)
        dialog.set_version("%s %s" % ('Version', VERSION))
        dialog.set_copyright(COPYRIGHT)
        dialog.set_comments(DESCRIPTION)
        dialog.set_authors(AUTHORS)
        # dialog.set_website(WEBSITE)

        dialog.set_license_type(Gtk.License.MIT_X11)

        # noinspection PyArgumentList
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            MY_LOGO,
            DEFAULT_LOGO_SIZE_WIDTH, DEFAULT_LOGO_SIZE_HEIGHT,
            True)
        dialog.set_logo(pixbuf)
        dialog.run()
        dialog.destroy()

    def quit_cb(self, action, parameter):
        print("quit clicked")
        # Call on_delete_event directly to get same effect as clicking window 'x'
        if not self.win.on_delete_event(self.win):
            self.quit()

    def do_activate(self):
        self.win = MyWindow(application=self, title="Hello World")
        self.win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


app = MyApplication()
app.run(sys.argv)
