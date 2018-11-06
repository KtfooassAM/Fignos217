"""Script defining the left part of the common UI."""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *

from locations import Locations
from verticalScroll import VerticalScroll


class SendOrderCancelation(QObject):
    emitParameters = pyqtSignal(list)


class OrdersPanel(QWidget):
    """Class defining the widget filling the left column of the screen summing up the orders"""
    """ Add order to the list : OrdersPanel.add_order_widget((bar, quantity, drink)) """

    cancel_order = pyqtSignal(int)

    def __init__(self, place="reserve"):
        """Constructor."""
        QWidget.__init__(self)
        self.__place = place
        self.__init_UI()

    def __init_UI(self):
        """Method used to initialize the UI of the left panel."""

        # Set an absolute size
        self.setMinimumWidth(300)  # Arbitrary
        self.setMaximumWidth(300)

        # Creating a VerticalScroll area
        self.scroll_area = VerticalScroll(bottom_stretch=True)

        # Setting it up correctly
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll_area.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)

        # Creating main layout that only contains the scroll area
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Historique"))
        self.main_layout.addWidget(self.scroll_area)

        # Setting it as default layout
        self.setLayout(self.main_layout)

    def add_order_widget(self, order):
        """Method adding a new Order to the list."""

        # Creating a new label
        new_order = OrderWidget(order, self.__place)
        new_order.order_cancelled.connect(self.cancel_order)

        # Displaying it
        self.scroll_area.add_widget(new_order, 0)

        # Check if there are to many items already displayed
        if self.scroll_area.count() > 30:
            self.scroll_area.remove_widget(-1)

    def remove_order_widget(self, id):
        """Method called to remove a cancelled sale."""
        for i, w in enumerate(self.scroll_area.widgets_list):
            if int(w.id) == int(id):
                self.scroll_area.remove_widget(i)


class OrderWidget(QWidget):
    """ Class defining a basic notification line."""

    order_cancelled = pyqtSignal(int)

    def __init__(self, order, place=Locations.BAR):
        """Constructor."""
        QWidget.__init__(self)

        # Creating label
        self.id, self.drink, self.quantity, self.bar = order  # If location is bar, bar arg is None
        text = ''
        if place is Locations.RESERVE:
            text = "Bar {} : \n".format(str(self.bar.capitalize()))
        text += "{} q./b. de {}".format(str(self.quantity), str(self.drink))

        self.__init_UI(text)

    def __init_UI(self, text):
        """Method called to create the UI of the widget."""

        # Add layout of order
        layout = QHBoxLayout()

        # Creating label
        label = QLabel(text, self)

        # Creating cancel button
        self.cancel_button = QPushButton("X", self)
        self.cancel_button.setFixedWidth(30)
        self.cancel_button.setCheckable(True)
        self.cancel_button.clicked.connect(self.__button_clicked)

        # Adding label to the layout
        layout.addWidget(label)

        # Adding a stretch
        layout.addStretch()

        # Adding button to the layout
        layout.addWidget(self.cancel_button)

        # Adding layout to the Order
        self.setLayout(layout)

    def __button_clicked(self):
        """Method called when a cancel button is clicked"""

        # Changing the button label and disabling it
        self.cancel_button.setEnabled(False)

        # Send the cancelation signal
        self.order_cancelled.emit(int(self.id))


if __name__ == '__main__':
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    orders_panel = OrdersPanel()
    orders_panel.show()

    # Populating test data
    for i in range(60):
        orders_panel.add_order_widget((str(i), i % 3 + 1, "1"))

    # Launching the app
    sys.exit(app.exec_())

    # TO-DO:
    #     Add actions to buttons
