import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# import pygtk
# pygtk.require('2.0')
# import gtk as Gtk

import datetime
import time

class MyDateEntry(Gtk.HBox):
    def __init__(self, parent, initial_date):
        Gtk.HBox.__init__(self)
        self.set_spacing(5)
        self.set_homogeneous(False)
        date_entry = DateEntry(parent)
        date_entry.set_hexpand(False)
        date_entry.set_halign(Gtk.Align.CENTER)
        date_entry.set_text(initial_date)

        self.add(date_entry)

        self.date_entry = date_entry

        cal_btn = Gtk.Button()
        img = Gtk.Image.new_from_file('./images/calendar.png')
        cal_btn.set_image(img)
        cal_btn.set_hexpand(False)
        cal_btn.set_halign(False)
        self.add(cal_btn)
        cal_btn.connect("clicked", date_entry.popup_calendar)

        # Stop external packing options from influencing our layout
        self.set_hexpand(False)
        self.set_halign(Gtk.Align.START)

    def get_text(self):
        return self.date_entry.get_text()
        pass


class DateEntry(Gtk.Entry):
        
    def __init__(self, parent):
        Gtk.Entry.__init__(self)
        self.set_max_length(8)
        self.set_width_chars(8)
        self.set_max_width_chars(8)

        self.cal_dlg = Gtk.Dialog("Choose date", None, Gtk.DialogFlags.MODAL, None)
        self.cal_dlg.set_transient_for(parent)

        self.cal = Gtk.Calendar()
        self.cal_dlg.vbox.add(self.cal)
        try:
            dt = datetime.datetime.strptime(self.get_text(), "%d/%m/%y")
        except:
            dt = datetime.date.today()

        print(datetime.date.today().year)
        self.cal.select_month(dt.month-1, dt.year)
        self.cal.select_day(dt.day)
        self.cal.connect("day-selected-double-click", self.click_on_calendar)
        self.cal_dlg.connect("delete-event", self.click_on_calendar)

       

    def popup_calendar(self, widget):
        self.cal.show()
        self.cal_dlg.run()
        
        year, month, day = self.cal.get_date()
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        self.set_text(time.strftime("%x", time.localtime(mytime)))

        self.activate()


    def click_on_calendar(self, calendar, event=None):
        # just close the cal_dlg. Code in popup_calendar will
        # then copy the selected date into the text entry field
        self.cal_dlg.hide()


if __name__ == "__main__":
    window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    v = Gtk.VBox()

    today = datetime.date.today()
    d = MyDateEntry(window, today.strftime("%d/%m/%Y"))
    v.pack_start(d, False, False, 0)

    window.add(v)
    window.show_all()

    Gtk.main()
