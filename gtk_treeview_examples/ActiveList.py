import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TVColumn(Gtk.TreeViewColumn):

    def __init__(self, ID, object_type, title="", width=0, background_column=None, renderer_type=None, alignment=0.0):
        self.ID = ID
        self.object_type = object_type
        self.renderer_type = renderer_type
        self.title = title
        self.width = width
        self.background_column = background_column
        self.alignment = alignment


class ActiveList(object):
    _columns = None

    def __init__(self, tree_view):

        column_type_list = [] # for creating the model
        totalWidth = 0

        # Loop through the columns and initialize the TreeView
        for column in self._columns:

            # Save the type for Gtk.TreeStore creation
            column_type_list.append(column.object_type)
            # Is it visible?
            if column.renderer_type:
                # Renderer type is specified, i.e. it's a visible column
                # Create an instance of renderer_type
                _renderer = column.renderer_type()

                # Create the Column and set up suitable attributes
                col = Gtk.TreeViewColumn (
                    column.title
                ,   _renderer
                )
                col.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
                col.set_expand(True)
                col.set_resizable(True)
                col.set_fixed_width(column.width)

                if isinstance(_renderer, Gtk.CellRendererText):
                    col.add_attribute(_renderer, "text", column.ID)
                    # Set right-justified if requested, default is left
                    _renderer.set_property('xalign', column.alignment)
                elif isinstance(_renderer, Gtk.CellRendererToggle):
                    col.add_attribute(_renderer, "active", column.ID)

                # col.add_attribute(_renderer, "cell_background", column.background_column)
                col.add_attribute(_renderer, "cell_background", column.background_column)
                # _renderer.set_property("background", "lightblue")

                tree_view.append_column(col)
                col.queue_resize()
                totalWidth = totalWidth + col.get_fixed_width()

        # Create the Gtk.ListStore model to use with the TreeView
        # (* unpacks the column_type_list into separate column-type arguments)
        self.model = Gtk.ListStore(*column_type_list)

        tree_view.set_size_request(totalWidth, 250)
        self.treeselection = tree_view.get_selection()
        self.treeselection.set_mode(Gtk.SelectionMode.SINGLE)

        self.model.set_sort_column_id(Gtk.TREE_SORTABLE_UNSORTED_SORT_COLUMN_ID, Gtk.SortType.ASCENDING)


class sorted_row(object):

    def __init__(self, sorted_model, sorted_path):
        self.model = sorted_model
        self.path = sorted_path

        self.child_model = self.model.get_model()
        if self.path:
            self.child_path = self.model.convert_path_to_child_path(self.path)
        else:
            self.child_path = self.child_model.get_path(self.child_model.append())

        self.path = self.model.convert_child_path_to_path(self.child_path)

    def append(self):
        self.child_path = self.child_model.get_path(self.child_model.append())

    def remove(self):
        # # The iter for previous row is calculated from path.
        # # As the paths are tuples and they are immutable, we have to convert the tuple to a list.
        # # Then cut out the last member (= position on current tree level), decrement it and convert the
        # # resulting list back to a tuple.
        #
        # position = self.path[-1]
        # prev_path = list(self.path)[:-1]
        # prev_path.append(position - 1)
        # prev_path = tuple(prev_path)
        #
        self.child_model.remove(self.child_model.get_iter(self.child_path))

    def __getitem__(self, item):        # item is column id e.g COL_RECON
        return self.child_model[self.child_path][item]

    def __setitem__(self, key, value):  # key is column id e.g COL_RECON
        self.child_model[self.child_path][key] = value

        # Changing the value in a column may result in moving the row's
        # position in the sorted model (if the column is a sort column).
        # Update the sorted path just in case.
        self.path = self.model.convert_child_path_to_path(self.child_path)