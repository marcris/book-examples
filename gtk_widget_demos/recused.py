#!/usr/bin/python3
# recused.py
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class RecentChooserMenu(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('RecentChooser Demo')
        self.set_size_request(250, 100)
        self.connect('destroy', Gtk.main_quit)

        vbox = Gtk.VBox()
        self.add(vbox)
        hbox = Gtk.HBox()
        hbox.set_size_request(300, 200)


        menubar = Gtk.MenuBar()
        vbox.add(menubar)




        project_directory = '/home/chris/MDProject/Code/programming-python-with-gtk-and-sqlite'
        recent_mgr = Gtk.RecentManager.get_default()

        recentchooserwidget = Gtk.RecentChooserWidget()
        recentchooserwidget.connect('item-activated', self.on_item_activated)
        hbox.add(recentchooserwidget)


        menuitem = Gtk.MenuItem(label = 'Recent Items')
        menubar.append(menuitem)

        recentchoosermenu = Gtk.RecentChooserMenu.new_for_manager(recent_mgr)
        recentchoosermenu.connect('item-activated', self.on_item_activated)
        menuitem.set_submenu(recentchoosermenu)
        # add an hbox to contain window(s)
        vbox.add(hbox)

        button = Gtk.Button(label = 'Gtk.RecentChooserDialog Demo')
        button.connect('clicked', self.on_button_clicked)
        vbox.add(button)

        # recent_data = Gtk.RecentData()
        # recent_data.app_exec = "bm"
        # recent_data.app_name = "BookMaker"
        # recent_data.mime_type = "inode/directory"
        # recent_mgr.add_full(Gio.File.new_for_path(project_directory).get_uri(), recent_data)
        recent_data = Gtk.RecentData()
        recent_data.app_exec = "bm"
        recent_data.app_name = "BookMaker"
        recent_data.mime_type = "inode/directory"
        recent_data.description = "A Book Authoring Application in Python"
        recent_data.display_name = "programming-python-with-gtk-and-sqlite"
        recent_data.short_name = "programming-python-with-gtk-and-sqlite"
        recent_data.is_private = False
        recent_mgr.add_full(Gio.File.new_for_path(project_directory).get_uri(), recent_data)

        # A Gtk.RecentInfo contains all the meta-data associated with an entry in the recently used files list.
        for recent_info in recent_mgr.get_items():  # one from a list of Gtk.RecentInfo objects
            if "BookMaker" in recent_info.get_applications():
                if info := recent_info.get_application_info("BookMaker"):  # parameter is app_name
                    # a tuple of app_exec, count, timestamp, e.g  ('recused demo', 5, 1658594295)
                    print("\nApplication info for 'BookMaker'\n", info)

                print("Description for 'BookMaker': ", recent_info.get_description())
                print("The file's display name:             ", recent_info.get_display_name())
                print("The file's short name:               ", recent_info.get_short_name())
                print("Applications which registered file: ", recent_info.get_applications())
                print("The file's MIME type:               ", recent_info.get_mime_type())
                print("The file's URI:                     ", recent_info.get_uri())
                print("Displayable version of its URI:     ", recent_info.get_uri_display())
                print("Registration is_private to app:     ", recent_info.get_private_hint())
                print("Registration is_local:              ", recent_info.is_local())


    def on_item_activated(self, recentchoosermenu):
        if item := recentchoosermenu.get_current_item():
            print("Item selected:")
            print("Name:\t %s" % (item.get_display_name()))
            print("URI:\t %s" % (item.get_uri()))

    def on_button_clicked(self, button):
        class RecentChooserDialog(Gtk.RecentChooserDialog):
            def __init__(self):
                Gtk.RecentChooserDialog.__init__(self)
                self.set_title('RecentChooserDialog')
                self.set_default_size(250, -1)
                self.add_button('Cancel', Gtk.ResponseType.CANCEL)
                self.add_button('OK', Gtk.ResponseType.OK)
                self.set_default_response(Gtk.ResponseType.OK)
                self.connect('response', self.on_response)

            def on_response(self, recentchooserdialog, response):
                if response == Gtk.ResponseType.OK:
                    item = recentchooserdialog.get_current_item()

                    if item:
                        print('Item selected:')
                        print('Name:\t %s' % (item.get_display_name()))
                        print('URI:\t %s' % (item.get_uri()))

        dialog = RecentChooserDialog()
        dialog.run()
        dialog.destroy()


window = RecentChooserMenu()
window.show_all()

# GLib.idle_add(Gtk.main_quit)
Gtk.main()
