# DateEntry_plain.py
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, GObject

import datetime


class MyDateEntry(gtk.Box):
    """
    MyDateEntry is a composite widget containing a Gtk.Entry and a Gtk.Button.
    Entry of a date into the Gtk.Entry is possible by
        * direct typing by the user
        * clicking the button to display a Gtk.Dialog containing a Gtk.Calendar
          and then double-clicking the desired day in the Calendar.

    The cursor is positioned after the entered date to simulate typing. If
    Return is pressed the 'activate' signal is emitted, as in a Gtk.Entry.

    The composite widget implements grab_focus (in order to receive the input
    focus transferred from any preceding widget).
    """
    __gsignals__ = {
        'activate': (GObject.SignalFlags.RUN_LAST,
                      GObject.TYPE_NONE,
                      (GObject.TYPE_STRING,))
    }

    def __init__(self, parent, initial_date):
        super(self.__class__, self).__init__()
        self.set_spacing(5)
        self.set_homogeneous(False)

        self.date_entry = DateEntry(parent)
        self.date_entry.set_text(initial_date)

        self.date_entry.connect('activate', self.activate_handler)

        self.add(self.date_entry)

    def activate_handler(self, widget):
        self.emit("activate", widget.get_text())

    def grab_focus(self):
        self.date_entry.grab_focus()


class DateEntry(gtk.Box):   # orientation defaults to HORIZONTAL

    def __init__(self, parent):
        super(self.__class__, self).__init__()
        self.set_spacing(5)

        self.entry = gtk.Entry()
        self.entry.set_max_length(8)
        self.entry.set_width_chars(8)
        self.entry.set_max_width_chars(8)

        self.add(self.entry)

        btn = gtk.Button()
        img = gtk.Image.new_from_file('calendar.png')
        btn.set_image(img)
        self.add(btn)
        btn.connect("clicked", self.popup_calendar)

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
        try: # set the Calendar to the date currently in the Entry ...
            dt = datetime.datetime.strptime(self.entry.get_text(), "%d/%m/%y")
        except Exception: # ... or to today's date if that was invalid
            dt = datetime.date.today()

        self.cal.select_month(dt.month - 1, dt.year)
        self.cal.select_day(dt.day)
        self.cal.show()
        self.cal_dlg.run()

    def day_selected_double_click(self, widget):
        year, month, day = self.cal.get_date()
        self.entry.grab_focus_without_selecting()
        self.set_text(f"{day:02}/{month + 1:02}/{year - 2000:02}")
        self.cal_dlg.hide()

    def get_text(self):
        return self.entry.get_text()

    def set_text(self, text):
        self.entry.set_text(text)
        self.entry.set_position(len(text))  # set cursor to the right

    def grab_focus(self):
        self.entry.grab_focus_without_selecting()

    def connect(self, detailed_signal, handler):
        self.entry.connect('activate', handler)


if __name__ == "__main__":
    window = gtk.Window(type=gtk.WindowType.TOPLEVEL)
    window.connect('delete-event', gtk.main_quit)

    widget = MyDateEntry(window, '25/08/22')
    window.add(widget)

    window.show_all()

    gtk.main()
