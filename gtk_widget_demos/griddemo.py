# !/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import MyDateEntry
import datetime

DATE = 1
ELECMETER = 2
ELECPERDAY = 3
GASMETER = 4
GASPERDAY = 5
NOTES = 6


class enter_8(Gtk.Entry):
    # Modify an Entry widget to accept a maximum of 8 characters,
    # to have a sufficient width to display them and to be aligned to
    # the left of its cell in the Grid.
    #
    # The "sensitive" attribute determines whether the Entry is able to
    # accept input (True) or not (False).
    def __init__(self, sensitive=True):
        Gtk.Entry.__init__(self)
        self.set_max_length(8)
        self.set_width_chars(8)
        self.set_max_width_chars(8)
        self.set_halign(Gtk.Align.START)
        self.set_sensitive(sensitive)


class GridDemo(Gtk.Window):
    # Fake some "readings" to be displayed in the Entry widgets
    readings = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Grid Demo")
        self.set_size_request(250, 100)
        self.set_border_width(5)
        self.connect("destroy", Gtk.main_quit)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_column_homogeneous(False)
        self.add(grid)

        label = Gtk.Label(label='Date')
        label.set_halign(Gtk.Align.START)
        grid.add(label)
        # Note the use of MyDateEntry, a composite widget discussed in a later section.
        self.date_entry = MyDateEntry.MyDateEntry(self, datetime.date.today().strftime("%d/%m/%y"))
        grid.attach(self.date_entry, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label='ElecMeter'), 0, 1, 1, 1)
        self.elecmeter_entry = enter_8()
        self.elecmeter_entry.set_text(str(self.readings[ELECMETER]))
        grid.attach(self.elecmeter_entry, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label='ElecPerDay'), 2, 1, 1, 1)
        self.elec_per_day_entry = enter_8(sensitive=False)
        self.elec_per_day_entry.set_text(str(self.readings[ELECPERDAY]))
        grid.attach(self.elec_per_day_entry, 3, 1, 1, 1)

        grid.attach(Gtk.Label(label='GasMeter'), 0, 2, 1, 1)
        self.gasmeter_entry = enter_8()
        self.gasmeter_entry.set_text(str(self.readings[GASMETER]))
        grid.attach(self.gasmeter_entry, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label='GasPerDay'), 2, 2, 1, 1)
        self.gas_per_day_entry = enter_8(sensitive=False)
        self.gas_per_day_entry.set_text(str(self.readings[GASPERDAY]))
        grid.attach(self.gas_per_day_entry, 3, 2, 1, 1)

        label = Gtk.Label(label='Notes')
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        self.notes_entry = Gtk.Entry()
        self.notes_entry.set_text(str(self.readings[NOTES]))
        grid.attach(self.notes_entry, 1, 3, 3, 1)

window = GridDemo()
window.show_all()

Gtk.main()
