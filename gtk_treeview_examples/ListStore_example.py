#!/usr/bin/python3
# ListStore_example.py

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import sys

import csv
import datetime

from ActiveList import ActiveList

# TreeModel column ID's
# COL_SEQ = 0
# COL_LAST = 1        # LastName
# COL_FIRST = 2       # FirstName
# COL_TITLE = 3       # Title
# COL_BOSS = 4        # ReportsTo
# COL_BORN = 5        # Birth Date
# COL_HIRED = 6       # Hire Date
# COL_KEY = 7         # Database Key - not used


#...or (easier to modify correctly)
#   We'll use column 0 of each row to specify a background colour for
#   the row. this is not compulsory, but I found it a useful convention.
#   This column is not displayed.
COL_SEQ,\
COL_LAST,\
COL_FIRST,\
COL_TITLE,\
COL_BOSS,\
COL_BORN,\
COL_HIRED,\
COL_KEY = range(8)


class MyWindow(Gtk.ApplicationWindow):

    def get_data(self, model):
        # Use csv.DictReader() to create an object for reading data from a CSV file.
        # The DictReader translates each line of the file to a dictionary using the
        # field names from the first line as keys.

        with open(f'{os.path.dirname(__file__)}/employees.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # The BirthDate and HireDate fields are in DATETIME format
                # "YYYY-MM-DD HH:MM:SS". Extract just the date part, and
                # re-format it as "DD/MM/YY".
                year_s, mon_s, day_s = row['BirthDate'].split(' ')[0].split('-')
                bd = datetime.date(int(year_s), int(mon_s), int(day_s))
                year_s, mon_s, day_s = row['HireDate'].split(' ')[0].split('-')
                hd = datetime.date(int(year_s), int(mon_s), int(day_s))
                model.append(["white" if reader.line_num % 2 else "lightgreen",
                            row['LastName'],
                            row['FirstName'],
                            row['Title'],
                            row['ReportsTo'],
                            bd.strftime("%d/%m/%y"),
                            hd.strftime("%d/%m/%y")])

        # Illustrate iterating through the ListStore

        it = model.get_iter_first()

        while it:
            print(model.get(it, 1, 2, 3, 5))

            it = model.iter_next(it)

    def __init__(self, app):
        super().__init__(title="ListStore Example", application=app)
        self.set_default_size(250, 250)

        print(sys.path)

        model = Gtk.ListStore(str, str, str, str, str, str, str)
        self.get_data(model)
        self.tree_view = Gtk.TreeView(model=model)
        totalWidth = 0

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("LastName", renderer)
        # column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_fixed_width(75)  # fixed_width overrides AUTOSIZE if set
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_LAST)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("FirstName", renderer)
        # column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_fixed_width(75)
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_FIRST)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        # column.set_fixed_width(110)
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_TITLE)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("ReportsTo", renderer)
        # column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_fixed_width(75)
        renderer.set_property('xalign', 0.5)    # horiz.centre alignment
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_BOSS)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("BirthDate", renderer)
        # column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_fixed_width(80)
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_BORN)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("HireDate", renderer)
        # column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_fixed_width(80)
        column.add_attribute(renderer, "cell-background", COL_SEQ)
        column.add_attribute(renderer, "text", COL_HIRED)
        self.tree_view.append_column(column)
        totalWidth += column.get_fixed_width()

        self.tree_view.set_size_request(totalWidth, -1)

        self.add(self.tree_view)
        


class MyApplication(Gtk.Application):

    def __init__(self):
        super().__init__()
        

    def do_activate(self):
        self.window = MyWindow(self)
        self.window.show_all()

    def do_startup(self):
        # start the application
        Gtk.Application.do_startup(self)

import platform
print("Using Python %s on %s" % (platform.python_version(), platform.platform()))
# This example doesn't use ActiveList; it's designed to show what we would
# have to do in the absence of ActiveList.


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

