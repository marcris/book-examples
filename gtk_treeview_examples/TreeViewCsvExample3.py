# TreeViewCsvExample3 - using a Gtk.ListStore and Gtk.TreeModelSort
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

from typing import Optional

import os
import sys
import csv

from datetime import datetime

from ActiveList import TVColumn, ActiveList

# TreeModel column ID's

COL_LAST,\
COL_FIRST,\
COL_TITLE,\
COL_BOSS,\
COL_BORN,\
COL_HIRED,\
COL_KEY,\
COL_SEQ = range(8)


class TV(ActiveList):
    # The ActiveList defines the columns for the treeview
    _columns = [
        # The following columns are obtained from the source
        # and displayed in the treeview.

        # column 0 (LastName)
        TVColumn(COL_LAST, str, "LastName", 75, COL_SEQ, gtk.CellRendererText)
        # column 1 (FirstName)
        , TVColumn(COL_FIRST, str, "FirstName", 75, COL_SEQ, gtk.CellRendererText)
        # column 2 (Title)
        , TVColumn(COL_TITLE, str, "Title", 135, COL_SEQ, gtk.CellRendererText)
        # column 3 (Reports To)
        , TVColumn(COL_BOSS, str, "ReportsTo", 80, COL_SEQ, gtk.CellRendererText, 0.5)
        # column 4 (BirthDate)
        , TVColumn(COL_BORN, str, "Born", 70, COL_SEQ, gtk.CellRendererText)
        # column 5 (HireDate)
        , TVColumn(COL_HIRED, str, "Hired", 70, COL_SEQ, gtk.CellRendererText)

        # column 6 (KEY) - e.g. database key to identify a record for UPDATE etc
        # Would not normally be displayed but useful in this example
        , TVColumn(COL_KEY, int, "Key", 50, COL_SEQ, gtk.CellRendererText, 0.5)

        # The following source fields are used but not displayed

        # The following column (column 7) contains a string representing a
        # background colour to be used for the whole row.
        , TVColumn(COL_SEQ, str)

    ]


def parse_ddmmyy(s):
    day_s, mon_s, year_s = s.split('/')
    return datetime(1900+int(year_s), int(mon_s), int(day_s))


def sort_on_date(model, a, b, userdata):
    # Return a negative integer, zero, or a positive integer
    # if a sorts before b, a sorts with b, or a sorts after b respectively.

    # userdata is a tuple of column id's; here we only specify one column.

    # Get the data from first column (format dd/mm/yy)
    first = model.get_value(a, COL_BORN)
    second = model.get_value(b, COL_BORN)
    print (first, second)

    # Convert to datetime format. If we use datetime.strptime to parse the dates
    # which are in %d/%m/%y format,
    #     first = datetime.strptime(first, '%d/%m/%y')
    #     second = datetime.strptime(second, '%d/%m/%y')
    # there is a question over the %y format specifier.
    # According to the Python interpreter source code (From cpython/_strptime.py)
    #   "Open Group specification for strptime() states that a %y value in the range
    #   of [00, 68] is in the century 2000, while [69,99] is in the century 1900"
    # and datetime.strptime is implemented accordingly. Since we have a group of
    # random dates which we know are all in the range 1900-1999, some of these will
    # be moved into 2000-2068 and others will stay in 1969-1999. Our only choice is
    # to let this happen and then correct for it.
    # Alternatively (as I have chosen to do here) we provide a simple parsing function
    # incorporating the knowledge that the dates are all in 1900-1999.
    # This also has the advantage of being far more efficient than the generalized
    # datetime.strptime.
    first = parse_ddmmyy(first)
    second = parse_ddmmyy(second)
    print (first, second)

    # Correction that would be necessary if we used datetime.strptime
    # first = first if datetime.now() > first else first.replace(year=first.year - 100)
    # second = second if datetime.now() > second else second.replace(year=second.year - 100)
    print (first, second)

    return 0 if first == second else 1 if first > second else -1


class MyWindow(gtk.ApplicationWindow):

    from typing import Optional, Union
    sorted_model: Optional[gtk.TreeModelSort]

    def __init__(self, app):
        super().__init__(title="TreeView Example 3", application=app)

        self.vbox = gtk.Box.new(gtk.Orientation.VERTICAL, 0)

        self.builder = gtk.Builder()
        self.builder.add_from_file("ui_statusbar.xml")
        self.builder.connect_signals(self)
        self.statusbar = self.builder.get_object("statusbar")

        self.set_default_size(250, 100)

        self.treeview = gtk.TreeView()
        self.sorted_model = None
        self.create_model_and_view_columns(f'{os.path.dirname(__file__)}/employees.csv')
        self.vbox.add(self.treeview)

        self.message_1 = "Initially sorted in ASCENDING order on column 'Born'\n"   # fields in statusbar
        self.message_2 = "(Sort on column 'Key' to restore original order)\n"   #
        self.message_3: Optional[str] = ""   #
        self.vbox.add(self.statusbar)
        self.add(self.vbox)

        # Quoting from cpython/_strptime.py
        # "Open Group specification for strptime() states that a %y
        # value in the range of [00, 68] is in the century 2000, while
        # [69,99] is in the century 1900"

        # The following is just to illustrate the quote above and has no
        # other part in the program.

        first = datetime.strptime('25/08/68', '%d/%m/%y')
        second = datetime.strptime('25/08/69', '%d/%m/%y')
        print(first, second)
        first = parse_ddmmyy('25/08/68')
        second = parse_ddmmyy('25/08/69')
        print(first, second)

    def create_model_and_view_columns(self, filepath):
        my_TV = TV(self.treeview)   # an instance of our descendant of ActiveList which
                                    # defines the model and columns of the treeview

        # The following code gets the data from some source (a .CSV file but could be
        # (e.g) a database), and loads it into the treeview's model (storage).

        # Put the name of the source (CSV file) as the window title
        self.set_title('Sorted Employee table from employees.csv')

        # Not interested in the message stacking facility of statusbar.
        # Get access to the label used for display; parent-child relationships are
        # gtk.Statusbar.message_area (a gtk.Box) -> gtk.Label
        self.statusbar_label = self.statusbar.get_message_area().get_children()[0]
        self.statusbar_label.set_single_line_mode(False)
        self.message_1 = "Click a column heading to sort on that column\n"
        self.message_2 = "(Sort on column 'Key' to restore original order)\n"
        self.message_3 = ""
        self.statusbar_label.set_text(self.message_1 + self.message_2 + self.message_3)

        # Use csv.DictReader() to create an object for reading data from a CSV file.
        # The DictReader translates each line of the file to a dictionary using the
        # field names from the first line as keys.

        with open(filepath, 'rt') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # The BirthDate and HireDate fields are in YY-MM-DD format (ISO format).
                bd = datetime.fromisoformat(row['BirthDate'])
                hd = datetime.fromisoformat(row['HireDate'])

                my_TV.model.append([
                    row['LastName'],
                    row['FirstName'],
                    row['Title'],
                    row['ReportsTo'],
                    bd.strftime("%d/%m/%y"),
                    hd.strftime("%d/%m/%y"),
                    # line number used as value for Key field
                    int(reader.line_num),
                    # alternate background colouring
                    "white" if reader.line_num % 2 else "lightgreen",
                ])

        self.sorted_model = gtk.TreeModelSort.new_with_model(my_TV.model)
        self.sorted_model.set_sort_func(COL_BORN, sort_on_date, [COL_BORN,])
        self.sorted_model.set_sort_column_id(COL_BORN, gtk.SortType.ASCENDING)
        self.treeview.set_model(self.sorted_model)

        self.shade_alternate_rows(self.sorted_model, 0)
        self.treeview.get_selection().connect('changed', self.on_selection_changed)

        for col_id in range(7):
            # Set each column header to sort on its own column
            sort_column = self.treeview.get_column(col_id)
            print(f'{col_id} {sort_column.get_title()}')
            sort_column.set_sort_column_id(col_id)
            sort_column.connect('clicked', self.on_column_clicked)

    def on_selection_changed(self, selection):
        print('selection changed')
        self.sorted_model, treeiter = self.treeview.get_selection().get_selected()
        sorted_path = self.sorted_model.get_path(treeiter)

        self.shade_alternate_rows(self.sorted_model, 0)

        self.message_3 = f"Selected row is row {self.sorted_model.convert_path_to_child_path(sorted_path)} of unsorted view"
        self.statusbar_label.set_text(self.message_1 + self.message_2 + self.message_3)

    def on_column_clicked(self, column: gtk.TreeViewColumn):
        self.shade_alternate_rows(self.sorted_model, 0)
        # Assumes the sorting takes place before this routine gets called

        sort_order = ['ASCENDING', 'DESCENDING']
        self.message_1 = f"Sorted in {sort_order[column.get_sort_order()]} order on column '{column.get_title()}'\n"
        self.statusbar_label.set_text(self.message_1 + self.message_2 + self.message_3)



    def shade_alternate_rows(self, model, start_from_row, color1="white", color2="lightgreen"):
        row_number = start_from_row
        while row_iter := model.iter_nth_child(None, row_number):
            child_iter = model.convert_iter_to_child_iter(row_iter)

            if row_number % 2 == 0:
                model.get_model().set(child_iter, COL_SEQ, color2)
            else:
                model.get_model().set(child_iter, COL_SEQ, color1)

            row_number += 1
            row_iter = model.iter_nth_child(None, row_number)


class MyApplication(gtk.Application):

    def __init__(self):
        super().__init__()
        self.window = None

    def do_activate(self):
        self.window = MyWindow(self)
        self.window.show_all()

    def do_startup(self):
        # start the application
        gtk.Application.do_startup(self)


import platform
print("Using Python %s on %s" % (platform.python_version(), platform.platform()))

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
