# DateEntry_gtkTemplate
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk as gtk
# Used https://github.com/virtuald/pygi-composite-templates.py
from gi_composites import GtkTemplate

import datetime


@GtkTemplate("DateEntry_gtkTemplate.ui")
class MyDateEntry(gtk.Box):
    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'MyDateEntry'

    entry = GtkTemplate.Child()
    button = GtkTemplate.Child()

    # Alternative way to specify multiple widgets:
    # entry, button = GtkTemplate.Child.widgets(2)

    __gsignals__ = {
        'activate': (GObject.SignalFlags.RUN_LAST,
                     GObject.TYPE_NONE,
                     (GObject.TYPE_STRING,))
    }

    def __init__(self, parent, initial_date):
        super(gtk.Box, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()

        self.set_text(initial_date)

        # create a dialog to show the calendar when the button is clicked
        self.cal_dlg = gtk.Dialog("Choose date (gtkTemplate)")
        self.cal_dlg.set_transient_for(parent)

        self.cal = gtk.Calendar()
        self.cal_dlg.vbox.add(self.cal)
        # user expected to double-click on the day ...
        self.cal.connect("day-selected-double-click", self.day_selected_double_click)
        # ... but if user just clicks the close button that's Ok
        self.cal_dlg.connect("delete-event", self.day_selected_double_click)

    def popup_calendar(self, widget):
        try:  # set the Calendar to the date currently in the Entry ...
            dt = datetime.datetime.strptime(self.entry.get_text(), "%d/%m/%y")
        except Exception:  # ... or to today's date if that was invalid
            dt = datetime.date.today()

        self.cal.select_month(dt.month - 1, dt.year)
        self.cal.select_day(dt.day)
        self.cal.show()
        self.cal_dlg.run()

    def day_selected_double_click(self, widget):
        year, month, day = self.cal.get_date()
        self.grab_focus()
        self.set_text(f"{day:02}/{month + 1:02}/{year - 2000:02}")
        self.cal_dlg.hide()

    def grab_focus(self):
        # pass on the call on the composite to the Entry child
        self.entry.grab_focus_without_selecting()

    def set_text(self, text):
        self.entry.set_text(text)
        self.entry.set_position(len(text))  # set cursor to the right

    @GtkTemplate.Callback
    def activate_handler(self, widget):
        # pass on the Entry child's activate signal to the composite
        self.emit("activate", widget.get_text())


if __name__ == '__main__':
    window = gtk.Window(type=gtk.WindowType.TOPLEVEL)
    window.connect('delete-event', gtk.main_quit)

    widget = MyDateEntry(window, '25/08/22')
    window.add(widget)

    window.show_all()

    gtk.main()
