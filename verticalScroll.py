"""Script defining a vertical scroll area for our purpose"""

from PyQt5.QtWidgets import *


class VerticalScroll(QScrollArea):
    """Class defining an easy-to-use vertical scroll area"""

    def __init__(self, top_stretch=False, bottom_stretch=False):
        """Constructor"""

        QScrollArea.__init__(self)

        # Create an empty list of widget to display
        self.widgets_list = []

        # Initializing the UI
        self.top_stretch = top_stretch
        self.bottom_stretch = bottom_stretch
        self.__init_UI()

    def __init_UI(self):
        """Method setting up the UI for the VerticalScroll class"""

        ## Setting up the vertical bar
        # self.bar = self.verticalScrollBar()

        # Create the inner widget of the scroll area
        self.inner_widget = QWidget(self)
        self.setWidget(self.inner_widget)

        # Create a vertical layout inside the previous widget
        self.__layout = QVBoxLayout(self)
        self.inner_widget.setLayout(self.__layout)

        # More settings
        self.setWidgetResizable(True)

    def __clear_layout(self):
        """Method removing all the widgets from the layout"""

        # Test if layout is empty
        if self.__layout.count():
            for i in reversed(range(self.__layout.count())):
                widget = self.__layout.takeAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

    def _refresh(self):
        """Method refreshing the widgets in the vertical scroll area according to the widget list"""

        # Remove all the widgets from the layout
        self.__clear_layout()

        # Check if adding a top stretch is needed
        if self.top_stretch:
            self.__layout.addStretch()

        # Re-build layout from list
        for widget in self.widgets_list:
            self.__layout.addWidget(widget)

        # Check if adding a bottom stretch is needed
        if self.bottom_stretch:
            self.__layout.addStretch()

    def count(self):
        """Method returning the number of items displayed in the vertical scroll area"""

        return len(self.widgets_list)

    def add_widget(self, widget, position=None):
        """Method adding a widget to the vertical scroll area"""

        # Add the widget in the layout from the list, depending if a position is specified or not
        if position is not None:  # Do not remove is not None for case 'position=0'
            self.widgets_list.insert(position, widget)
        else:
            self.widgets_list.append(widget)

        # Refresh the scroll area
        self._refresh()

    def move_widget(self, widget, position):
        """Method moving a widget in a specified position in the vertical scroll area"""

        newwidget = self.widgets_list[widget]

        # Move the widget in the list at the specified position
        self.widgets_list.insert(newwidget, position)
        self.widgets_list.pop(self.widgets_list[widget])

        # Refresh the scroll area
        self._refresh()

    def remove_widget(self, widget_position):
        """Method removing a widget from the vertical scroll area according to its position."""

        # Remove the specified widget
        self.widgets_list.pop(widget_position)

        # Refresh the scroll area
        self._refresh()

    def clear(self):
        """Method removing all the widgets in the vertical scroll area"""

        # Clear the widgets list
        self.widgets_list = []

        # Refresh the scroll area
        self._refresh()


if __name__ == "__main__":
    # Importing modules used to run the app
    from PyQt5.QtWidgets import *
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    scroll = VerticalScroll(bottom_stretch=True)

    widgets = [QLabel("1"), QLabel("2"), QLabel("3"), QLabel("4")]
    for widget in widgets:
        scroll.add_widget(widget)

    scroll.remove_widget(0)

    button = QPushButton("Clear")
    button.clicked.connect(scroll.clear)
    scroll.add_widget(button)

    scroll.show()

    # Launching the app
    sys.exit(app.exec_())
