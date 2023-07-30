# TreeViewCsvExample
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

import os
import sys
print(f'module os imported from {os.__file__}')
import csv
print(f'module csv imported from {csv.__file__}')

import datetime
print(f'module datetime imported from {datetime.__file__}')

import ActiveList
from ActiveList import TVColumn, ActiveList
#print(f'module ActiveList imported from {ActiveList.__file__}')

# TreeModel column ID's
COL_SEQ = 0
COL_LAST = 1  # LastName
COL_FIRST = 2  # FirstName
COL_TITLE = 3  # Title
COL_BOSS = 4  # ReportsTo
COL_BORN = 5  # Birth Date
COL_HIRED = 6  # Hire Date
COL_KEY = 7  # Database Key - not used

# ...or (easier to modify correctly)
COL_SEQ, \
COL_LAST, \
COL_FIRST, \
COL_TITLE, \
COL_BOSS, \
COL_BORN, \
COL_HIRED, \
COL_KEY = range(8)


class TV(ActiveList):
    # The ActiveList defines the columns for the treeview
    _columns = [
        # We'll use column 0 of each row to specify a background colour for
        # the row. This is not compulsory but I found it a useful convention.
        # This column is not displayed.
        TVColumn(COL_SEQ, str)

        # The following columns are obtained from the data source
        # and displayed in the treeview.

        # column 1 (LastName)
        , TVColumn(COL_LAST, str, "LastName", 75, COL_SEQ, gtk.CellRendererText)
        # column 2 (FirstName)
        , TVColumn(COL_FIRST, str, "FirstName", 75, COL_SEQ, gtk.CellRendererText)
        # column 3 (Title)
        , TVColumn(COL_TITLE, str, "Title", 93, COL_SEQ, gtk.CellRendererText)
        # column 4 (Reports To)
        , TVColumn(COL_BOSS, str, "ReportsTo", 75, COL_SEQ, gtk.CellRendererText)
        # column 5 (BirthDate)
        , TVColumn(COL_BORN, str, "Born", 70, COL_SEQ, gtk.CellRendererText)
        # column 6 (HireDate)
        , TVColumn(COL_HIRED, str, "Hired", 70, COL_SEQ, gtk.CellRendererText)

        # The following column is used but not displayed
        # KEY - e.g. database key to identify a record for UPDATE etc
        , TVColumn(COL_KEY, int)
    ]


class MyWindow(gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(title="TreeView Example", application=app)
        self.set_default_size(250, 100)

        self.treeview = gtk.TreeView()
        self.create_model_and_view_columns(f'{os.path.dirname(__file__)}/employees.csv')
        self.add(self.treeview)

    def create_model_and_view_columns(self, filepath):
        my_TV = TV(self.treeview)  # an instance of our descendant of ActiveList which
        # defines the model and the columns of the treeview
        self.treeview.set_model(my_TV.model)

        # The following code gets the data from some source (a .CSV file but could be
        # (e.g) a database), and loads it into the treeview's model (storage).

        # Put the name of the source (CSV file) as the window title
        self.set_title('Employee table')

        # Use csv.DictReader() to create an object for reading data from a CSV file.
        # The DictReader translates each line of the file to a dictionary using the
        # field names from the first line as keys.

        with open(filepath, 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # The BirthDate and HireDate fields are in YY-MM-DD format.
                year_s, mon_s, day_s = row['BirthDate'].split(' ')[0].split('-')
                bd = datetime.date(int(year_s), int(mon_s), int(day_s))
                year_s, mon_s, day_s = row['HireDate'].split(' ')[0].split('-')
                hd = datetime.date(int(year_s), int(mon_s), int(day_s))

                my_TV.model.append([
                    "white" if reader.line_num % 2 else "lightgreen",
                    row['LastName'],
                    row['FirstName'],
                    row['Title'],
                    row['ReportsTo'],
                    bd.strftime("%d/%m/%y"),
                    hd.strftime("%d/%m/%y"),

                    float(reader.line_num)])



class MyApplication(gtk.Application):

    def __init__(self):
        super().__init__()

    def do_activate(self):
        self.window = MyWindow(self)
        self.window.show_all()

    def do_startup(self):
        # start the application
        gtk.Application.do_startup(self)

import platform
print("Using Python %s on %s" % (platform.python_version(), platform.platform()))
#import about
#about.whence(ActiveList.whence(), 'ActiveList')

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
